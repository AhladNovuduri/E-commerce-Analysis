import pandas as pd

from src.analysis import add_analysis_features, quality_report, summarize_by, validation_checks


def sample_data():
    return pd.DataFrame({
        "Order_ID": [1, 2, 3],
        "Order_Date": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-02-01"]),
        "Ship_Date": pd.to_datetime(["2024-01-03", "2024-01-02", "2024-02-04"]),
        "Customer_ID": [10, 20, 10],
        "Customer_Segment": ["Consumer", None, "Corporate"],
        "Region": ["East", "West", "East"],
        "State": ["A", "B", "A"],
        "Product_Category": ["X", "Y", "X"],
        "Sub_Category": ["x1", "y1", "x1"],
        "Product_Name": ["P1", "P2", "P1"],
        "Sales": [100.0, 200.0, 100.0],
        "Quantity": [1, 2, 1],
        "Discount": [0.0, 0.1, 0.2],
        "Profit": [20.0, None, 10.0],
        "Shipping_Cost": [5.0, 7.0, 6.0],
        "Payment_Mode": ["Cash", "Card", "Cash"],
    })


def test_quality_report_counts_missing_values():
    report = quality_report(sample_data())
    assert report.loc["Customer_Segment", "missing_count"] == 1
    assert report.loc["Profit", "missing_pct"] == round(100 / 3, 2)


def test_validation_checks_flags_ship_before_order():
    checks = validation_checks(sample_data())
    assert checks["ship_before_order"] == 1
    assert checks["row_count"] == 3


def test_month_feature_and_lead_time():
    out = add_analysis_features(sample_data())
    assert out["Order_Month"].dt.strftime("%Y-%m").tolist() == ["2024-01", "2024-01", "2024-02"]
    assert out["Ship_Lead_Days"].tolist() == [2, 0, 3]


def test_summary_margin_uses_aggregated_totals():
    summary = summarize_by(sample_data(), "Product_Category").set_index("Product_Category")
    assert summary.loc["X", "sales"] == 200
    assert summary.loc["X", "profit"] == 30
    assert summary.loc["X", "profit_margin_pct"] == 15.0
    assert summary.loc["Y", "profit_coverage_pct"] == 0.0
