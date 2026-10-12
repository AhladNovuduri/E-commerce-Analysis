# E-commerce Sales & Profitability Analytics

A business-focused exploratory data analysis (EDA) project investigating sales performance, profitability, customer segments, product categories, discounting, and fulfillment in an e-commerce dataset.

> **Project status:** Exploratory analysis. Business recommendations should be validated against the cleaned data and analysis assumptions before operational use.

## Business objectives

This project is designed to answer questions such as:

- How do sales and profit change over time?
- Which categories, sub-categories, regions, and customer segments contribute most to sales and profit?
- Are high discounts associated with lower profit margins?
- How long does fulfillment take, and how does delivery time vary by region or category?
- Which products have strong sales but weak or negative profitability?
- What data-quality issues could materially affect the conclusions?

## Dataset

The repository currently includes `e-commerce_cleaned.csv` and a notebook named `Work_File.ipynb`. The notebook's recorded outputs show **100,500 rows and 16 columns**.

| Field | Description |
| --- | --- |
| `Order_ID` | Order identifier |
| `Order_Date`, `Ship_Date` | Order and shipment dates |
| `Customer_ID`, `Customer_Segment` | Customer identifier and segment |
| `Region`, `State` | Geography |
| `Product_Category`, `Sub_Category`, `Product_Name` | Product dimensions |
| `Sales`, `Profit`, `Shipping_Cost` | Monetary measures (currency should be confirmed from the source) |
| `Quantity`, `Discount` | Order quantity and discount |
| `Payment_Mode` | Payment method |

**Data caveat:** The notebook's saved outputs show missing values in `Customer_Segment`, `Profit`, and `Shipping_Cost`. Do not silently replace missing profit or cost with zero. Validate date ranges, duplicate identifiers, numeric ranges, and the meaning/grain of each row before calculating KPIs. Confirm currency and whether each row represents an order, order line, or item.

## Key metrics

The analysis should report metrics using clearly defined denominators:

- **Total sales:** sum of `Sales`.
- **Total profit:** sum of non-missing `Profit`, with coverage reported.
- **Profit margin:** total profit divided by total sales, not the average of row-level margins.
- **Units sold:** sum of `Quantity`.
- **Average order value:** total sales divided by distinct orders, only if `Order_ID` represents an order and the data grain supports this calculation.
- **Shipping lead time:** `Ship_Date - Order_Date` in days; flag negative durations.
- **Discount analysis:** compare sales, profit, and margin by discount band while accounting for category and product mix.

## Recommended analysis workflow

1. **Audit:** inspect schema, row grain, duplicates, missingness, date validity, and numeric ranges.
2. **Prepare:** parse dates, standardize column labels/categories, retain missingness flags, and document any exclusion or imputation.
3. **Explore:** analyze monthly trends, category/sub-category, region/state, customer segment, payment method, products, and discount bands.
4. **Validate:** test whether apparent relationships are robust to missing-data handling, outliers, and segment mix.
5. **Communicate:** present concise findings, limitations, and measurable follow-up actions.
6. **Operationalize:** use the same metric definitions in notebooks, dashboard, and written report.

## Repository contents

- `Work_File.ipynb` — current exploratory analysis notebook.
- `e-commerce_cleaned.csv` — cleaned dataset used for analysis.
- `E-Commerce EDA Report.pdf` — detailed report.
- `EDA_Exe_Summary.pdf` — executive summary.
- `DATA ANALYST PROJECT.docx` — supplementary project document.

## Run locally

Python 3.10+ is recommended. From the repository root:

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
jupyter lab
```

Open `Work_File.ipynb` in Jupyter and run cells from top to bottom. The notebook should load the checked-in dataset via a path relative to the project root, rather than relying on an untracked local CSV.

## Next improvements

- Add a reusable data-validation and feature-engineering module.
- Refactor the notebook into a clean, restart-and-run workflow with narrative markdown and no stale outputs.
- Add automated checks for required columns, valid dates, missingness, duplicates, and metric reconciliation.
- Build an interactive Streamlit dashboard with date, region, product, and segment filters.
- Add a small set of regression tests and a reproducible environment file.
- Replace generic recommendations with evidence-backed findings and quantified opportunities.

## Interpretation and limitations

This is observational data. Correlation between discount, shipping cost, and profit does not by itself establish causation. Findings may be biased by missing data, extreme observations, seasonality, customer/product mix, or ambiguity in row grain. Report coverage and uncertainty alongside headline KPIs; avoid claiming that a specific policy will increase profit without a suitable experiment or stronger causal design.
