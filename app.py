"""Run with: streamlit run app.py"""
from pathlib import Path

import pandas as pd
import streamlit as st

from src.analysis import REQUIRED_COLUMNS, add_analysis_features, load_data, summarize_by

st.set_page_config(page_title="E-commerce Analytics", page_icon="📊", layout="wide")
st.title("E-commerce Sales & Profitability")
st.caption("Explore sales, profit coverage, product mix, and fulfillment. Validate data quality before acting on findings.")

DEFAULT_DATA = Path(__file__).parent / "e-commerce_cleaned.csv"
uploaded = st.sidebar.file_uploader("Upload a CSV (optional)", type=["csv"])
try:
    if uploaded is not None:
        raw = pd.read_csv(uploaded)
        missing = REQUIRED_COLUMNS.difference(raw.columns)
        if missing:
            st.error(f"Missing required columns: {sorted(missing)}")
            st.stop()
        df = raw
        for c in ("Order_Date", "Ship_Date"):
            df[c] = pd.to_datetime(df[c], errors="coerce")
        for c in ("Sales", "Quantity", "Discount", "Profit", "Shipping_Cost"):
            df[c] = pd.to_numeric(df[c], errors="coerce")
    else:
        df = load_data(DEFAULT_DATA)
except Exception as exc:
    st.error(f"Could not load data: {exc}")
    st.stop()

df = add_analysis_features(df)
st.sidebar.header("Filters")
regions = sorted(df["Region"].dropna().astype(str).unique())
categories = sorted(df["Product_Category"].dropna().astype(str).unique())
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
selected_categories = st.sidebar.multiselect("Product category", categories, default=categories)
valid_dates = df["Order_Date"].dropna()
if valid_dates.empty:
    st.error("No valid Order_Date values are available.")
    st.stop()
min_date, max_date = valid_dates.min().date(), valid_dates.max().date()
date_range = st.sidebar.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
filtered = df[
    df["Region"].astype(str).isin(selected_regions)
    & df["Product_Category"].astype(str).isin(selected_categories)
]
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    filtered = filtered[filtered["Order_Date"].dt.date.between(date_range[0], date_range[1])]

sales = filtered["Sales"].sum(min_count=1)
profit = filtered["Profit"].sum(min_count=1)
profit_coverage = filtered["Profit"].notna().mean() * 100 if len(filtered) else 0
margin = profit / sales * 100 if pd.notna(sales) and sales != 0 and pd.notna(profit) else float("nan")
orders = filtered["Order_ID"].nunique()
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Sales", f"{sales:,.2f}" if pd.notna(sales) else "—")
c2.metric("Observed profit", f"{profit:,.2f}" if pd.notna(profit) else "—")
c3.metric("Profit margin", f"{margin:.2f}%" if pd.notna(margin) else "—")
c4.metric("Distinct order IDs", f"{orders:,}")
c5.metric("Profit data coverage", f"{profit_coverage:.1f}%")
st.caption("Currency is not labeled because the dataset's currency has not been independently confirmed. Profit sums exclude missing values; coverage is shown alongside.")

left, right = st.columns(2)
with left:
    st.subheader("Monthly sales and profit")
    monthly = filtered.groupby("Order_Month", dropna=True).agg(sales=("Sales", "sum"), profit=("Profit", "sum")).reset_index().set_index("Order_Month")
    st.line_chart(monthly)
with right:
    st.subheader("Category performance")
    category = summarize_by(filtered, "Product_Category").sort_values("sales", ascending=False)
    st.bar_chart(category.set_index("Product_Category")[["sales", "profit"]])

st.subheader("Discount bands")
discount = summarize_by(
    filtered.assign(Discount_Band=filtered["Discount_Band"].astype("string").fillna("Unknown")),
    "Discount_Band",
)
st.dataframe(
    discount[["Discount_Band", "rows", "sales", "profit", "profit_coverage_pct", "profit_margin_pct"]],
    use_container_width=True, hide_index=True,
)

st.subheader("Regional performance")
region = summarize_by(filtered, "Region").sort_values("sales", ascending=False)
st.dataframe(
    region[["Region", "rows", "orders", "sales", "profit", "profit_coverage_pct", "profit_margin_pct"]],
    use_container_width=True, hide_index=True,
)

st.subheader("Data-quality checks")
checks = {
    "Rows in current view": len(filtered),
    "Missing profit": int(filtered["Profit"].isna().sum()),
    "Missing shipping cost": int(filtered["Shipping_Cost"].isna().sum()),
    "Missing segment": int(filtered["Customer_Segment"].isna().sum()),
    "Invalid order date": int(filtered["Order_Date"].isna().sum()),
    "Ship date before order date": int((filtered["Ship_Date"] < filtered["Order_Date"]).fillna(False).sum()),
    "Duplicate full rows": int(filtered.duplicated().sum()),
}
st.dataframe(pd.DataFrame([{"Check": k, "Count": v} for k, v in checks.items()]), use_container_width=True, hide_index=True)
st.warning("These are descriptive views. Discount and shipping associations are not causal effects. Confirm row grain, currency, duplicate order IDs, and missing-data patterns before operational use.")
