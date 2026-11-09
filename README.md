# E-commerce Data Analysis

Exploratory data analysis project using Python and Jupyter Notebook, supported by a cleaned dataset and exported analytical reports.


## Project Contents

| File | Purpose |
|---|---|
| `Work_File.ipynb` | Main Jupyter notebook |
| `e-commerce_cleaned.csv` | Cleaned dataset |
| `E-Commerce EDA Report.pdf` | Supporting EDA report |
| `EDA_Exe_Summary.pdf` | Executive summary |
| `DATA ANALYST PROJECT.docx` | Supporting project document |
| `requirements.txt` | Python dependencies for the EDA notebook |

## Technology

Python, Pandas, NumPy, Matplotlib, and Jupyter Notebook.

## Reproducible EDA

`Work_File.ipynb` now performs exploratory analysis directly on the committed `e-commerce_cleaned.csv`. It does not rerun undocumented cleaning steps or claim that the original preprocessing can be reproduced. The original `ecommerce_dirty_dataset.csv` is absent.

Create an environment and install the notebook's dependencies:

```bash
git clone https://github.com/AhladNovuduri/E-commerce-Analysis.git
cd E-commerce-Analysis
python -m venv .venv
# Activate the environment for your operating system.
python -m pip install -r requirements.txt
jupyter notebook Work_File.ipynb
```

Run the notebook from the repository root. It reports the inspected data-quality checks and generates descriptive tables and charts. It preserves all rows and values; it does not impute, cap, or remove observations.

The refactored notebook was executed top-to-bottom from a clean kernel with the dependencies in `requirements.txt` (10 code cells; no execution errors). On the committed file it reports 100,000 rows and 23 columns, zero exact duplicate rows, no missing or repeated `Order_ID`, no missing customer IDs, no missing or unparseable order/ship dates, and no ship-before-order records. These checks validate the file's internal consistency only; they do not establish the original source or business meaning.

## Data provenance and limitations

The dataset source, license, collection context, intended row grain, and original cleaning steps are not documented. Numeric units and the definitions of sales and profit also need confirmation. Treat results as descriptive of the committed processed file, not as causal or independently verified business findings.

## Reproducibility & Quality Checks

- [x] Verify the notebook executes top-to-bottom from a clean kernel in an environment with `requirements.txt` installed.
- [x] Confirm the source notebook reads the CSV by a repository-relative path.
- [x] Keep the source notebook free of saved execution outputs; the local verification copy is separate.
- [x] Use a correctly named dependency specification containing only packages used by the notebook.
- [ ] Add verified data provenance and licensing information.
- [ ] Add screenshots only from the actual notebook/report.
- [ ] Confirm whether the cleaned dataset may be redistributed.
- [x] Preserve rows and do not deduplicate by `Order_ID` until the source grain is established.
- [x] Keep the analysis on the committed processed data and avoid repeating undocumented cleaning transformations.
- [x] Group time trends by calendar month and year.
- [x] Remove unverified customer-contribution and repeat-customer claims from the rewritten notebook.

## Future Improvements

- Extract reusable transformations into Python modules where justified.
- Add data-validation checks for schema, nulls, duplicates, and value ranges.
- Add a small test suite for reusable transformation functions.
- Add a documented analysis summary with verified metrics.

## License

No repository license was visible in the inspected file inventory. Do not assume reuse or redistribution rights; add a license only after confirming ownership and dataset terms.

## Author

**Ahlad Novuduri** · [GitHub](https://github.com/AhladNovuduri)

