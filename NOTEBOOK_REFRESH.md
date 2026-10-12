# Notebook refresh guide

The legacy notebook has saved outputs and at least one dataset filename that does not match the checked-in CSV. Before extending the analysis:

1. Start with imports and load `e-commerce_cleaned.csv` using a path relative to the repository root.
2. Run `quality_report(df)` and `validation_checks(df)`; review anomalies before filtering or imputing.
3. Use `add_analysis_features(df)` to create month and shipping lead time.
4. Aggregate profit margin as `sum(Profit) / sum(Sales)`; do not average row-level margins to get an overall margin.
5. For discounts, compare multiple metrics and report sample size and profit coverage by band.
6. Restart the kernel and run all cells before saving. Clear stale outputs if they make the notebook unnecessarily large.

A suggested narrative is: business questions → data audit → preparation decisions → sales/profit trends → product/category and geographic performance → discounts and fulfillment → recommendations → limitations.
