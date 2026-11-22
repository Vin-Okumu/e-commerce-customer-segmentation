<h1 align="center">Processed Data</h1>

The three tables in this folder are **copied unchanged** from [e-commerce-sales-analytics](https://github.com/Vin-Okumu/e-commerce-sales-analytics/tree/main/01_data/processed), the first project in this series. Both projects therefore work from exactly the same numbers.

| File | Rows | Grain |
|---|---|---|
| `Fact_Sales.csv` | 250,000 | One order (one product per order) |
| `Dim_Customers.csv` | 40,000 | One customer |
| `Dim_Products.csv` | 2,000 | One product |

## Provenance

- **Source commit:** [`e1f9fbd`](https://github.com/Vin-Okumu/e-commerce-sales-analytics/commit/e1f9fbdb2d61f046591a61e5937de99ca1b5aa84) of e-commerce-sales-analytics (17 Nov 2026), the last commit that changed its `01_data/processed/` folder.
- **How they were produced:** cleaning and feature engineering in that repository's [`02_data_preparation.ipynb`](https://github.com/Vin-Okumu/e-commerce-sales-analytics/blob/main/03_preparation/02_data_preparation.ipynb). The steps and validation results are in its [processed data log](https://github.com/Vin-Okumu/e-commerce-sales-analytics/blob/main/01_data/processed/README.md).
- **Field definitions:** the first project's [data dictionary](https://github.com/Vin-Okumu/e-commerce-sales-analytics/blob/main/02_documentation/data_dictionary.md).

## Integrity check

SHA-256 checksums of the copied files. They are identical to the files in the source repository at the commit above.

| File | SHA-256 |
|---|---|
| `Dim_Customers.csv` | `0d6a42e8183e0ca535eb6a10a519250f3dc32969d8ebe71ef1021b7e53af2966` |
| `Dim_Products.csv` | `eae11b023813f871c9f291be096be50ad583512f171c7d28018d9ac317421130` |
| `Fact_Sales.csv` | `a759c361380cefab0c4fb133a2583072b0eb0c038a83470e2b181eb1de85f138` |

To verify your copy:

```bash
sha256sum 01_data/processed/*.csv
```

`01_customer_features.ipynb` also checks that these files reproduce the headline figures published in the first project's analysis report before any new analysis is done.
