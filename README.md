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
| `requirments.txt` | Existing dependency list; filename is misspelled |

## Technology

Python, Pandas, NumPy, Matplotlib, Seaborn, and Jupyter Notebook (as listed in the dependency file).

## Getting Started

The notebook is not currently reproducible from a clean checkout: its first data-loading cell references `ecommerce_dirty_dataset.csv`, which is not included in this repository. The committed `e-commerce_cleaned.csv` is available, but the notebook's later cells repeat cleaning operations and must not be run against it without refactoring the notebook. The dependency list also omits SciPy, which the notebook imports.

Do not interpret the current notebook's charts or recommendations as validated results until the input file, execution path, and analysis logic have been repaired and checked.

```bash
git clone https://github.com/AhladNovuduri/E-commerce-Analysis.git
cd E-commerce-Analysis
# Open e-commerce_cleaned.csv to inspect the committed processed data.
# The notebook is not yet runnable from a clean checkout.
```

## Analysis Documentation To Complete

Before publishing specific conclusions, document:

- Dataset source, license, collection date, and attribution.
- Dataset grain, row/column counts, and data dictionary.
- Cleaning and feature-engineering decisions.
- EDA questions and methods.
- Reproducible charts and verified numerical findings.
- Limitations, sampling caveats, and future work.

## Reproducibility & Quality Checks

- [ ] Verify the notebook executes top-to-bottom from a clean kernel.
- [ ] Confirm all file paths are relative and case-correct.
- [ ] Remove or explain stale notebook outputs.
- [ ] Correct the dependency filename in a separate cleanup change.
- [ ] Add a concise environment/dependency specification.
- [ ] Add data provenance and licensing information.
- [ ] Add screenshots only from the actual notebook/report.
- [ ] Confirm whether the cleaned dataset may be redistributed.
- [ ] Establish whether one row is an order, an order line, or another grain before deduplicating by `Order_ID`.
- [ ] Replace undocumented value changes and IQR-mean imputation with source-backed, reviewable rules.
- [ ] Fix monthly grouping so month values are not combined across years.
- [ ] Correct the top-customer contribution calculation and document the repeat-customer threshold.

## Future Improvements

- Extract reusable transformations into Python modules where justified.
- Add data-validation checks for schema, nulls, duplicates, and value ranges.
- Add a small test suite for reusable transformation functions.
- Add a documented analysis summary with verified metrics.

## License

No repository license was visible in the inspected file inventory. Do not assume reuse or redistribution rights; add a license only after confirming ownership and dataset terms.

## Author

**Ahlad Novuduri** · [GitHub](https://github.com/AhladNovuduri)

