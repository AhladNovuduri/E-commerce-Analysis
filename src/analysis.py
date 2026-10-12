"""Reusable quality checks and feature engineering for the e-commerce analysis."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

REQUIRED_COLUMNS = {
    "Order_ID", "Order_Date", "Ship_Date", "Customer_ID", "Customer_Segment",
    "Region", "State", "Product_Category", "Sub_Category", "Product_Name",
    "Sales", "Quantity", "Discount", "Profit", "Shipping_Cost", "Payment_Mode",
}
DATE_COLUMNS = ("Order_Date", "Ship_Date")
NUMERIC_COLUMNS = ("Sales", "Quantity", "Discount", "Profit", "Shipping_Cost")


def load_data(path: str | Path) -> pd.DataFrame:
    """Load CSV data and enforce required schema without hiding data-quality issues."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path}. Run from the project root or pass the CSV path.")
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")
    for column in DATE_COLUMNS:
        df[column] = pd.to_datetime(df[column], errors="coerce")
    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    return df


def quality_report(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize completeness and distinct non-null values for each column."""
    report = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "missing_count": df.isna().sum(),
        "missing_pct": (df.isna().mean() * 100).round(2),
        "distinct_non_null": df.nunique(dropna=True),
    })
    report.index.name = "column"
    return report.sort_values(["missing_pct", "missing_count"], ascending=False)


def validation_checks(df: pd.DataFrame) -> dict[str, int]:
    """Count records needing investigation; never silently auto-correct data."""
    return {
        "row_count": len(df),
        "duplicate_full_rows": int(df.duplicated().sum()),
        "duplicate_order_ids": int(df["Order_ID"].duplicated().sum()),
        "invalid_order_dates": int(df["Order_Date"].isna().sum()),
        "invalid_ship_dates": int(df["Ship_Date"].isna().sum()),
        "negative_sales": int((df["Sales"] < 0).sum()),
        "non_positive_quantity": int((df["Quantity"] <= 0).sum()),
        "discount_below_zero": int((df["Discount"] < 0).sum()),
        "discount_above_one": int((df["Discount"] > 1).sum()),
        "ship_before_order": int((df["Ship_Date"] < df["Order_Date"]).fillna(False).sum()),
        "missing_profit": int(df["Profit"].isna().sum()),
        "missing_shipping_cost": int(df["Shipping_Cost"].isna().sum()),
    }


def add_analysis_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add monthly and shipping-latency fields without modifying the input."""
    out = df.copy()
    out["Order_Month"] = out["Order_Date"].dt.to_period("M").dt.to_timestamp()
    out["Ship_Lead_Days"] = (out["Ship_Date"] - out["Order_Date"]).dt.days
    out["Row_Profit_Margin"] = out["Profit"] / out["Sales"].where(out["Sales"].ne(0))
    out["Discount_Band"] = pd.cut(
        out["Discount"],
        bins=[-0.000001, 0, 0.05, 0.10, 0.20, 1.0],
        labels=["0%", ">0–5%", ">5–10%", ">10–20%", ">20%"],
        include_lowest=True,
    )
    return out


def summarize_by(df: pd.DataFrame, dimensions: str | Iterable[str]) -> pd.DataFrame:
    """Aggregate sales, profit, units, shipping costs, order count and profit coverage."""
    if isinstance(dimensions, str):
        dimensions = [dimensions]
    dimensions = list(dimensions)
    grouped = df.groupby(dimensions, dropna=False, observed=True)
    result = grouped.agg(
        rows=("Sales", "size"),
        sales=("Sales", "sum"),
        profit=("Profit", "sum"),
        profit_observed=("Profit", "count"),
        units=("Quantity", "sum"),
        shipping_cost=("Shipping_Cost", "sum"),
        orders=("Order_ID", "nunique"),
    ).reset_index()
    result["profit_coverage_pct"] = (result["profit_observed"] / result["rows"] * 100).round(2)
    result["profit_margin_pct"] = (
        result["profit"] / result["sales"].where(result["sales"].ne(0)) * 100
    ).round(2)
    return result
