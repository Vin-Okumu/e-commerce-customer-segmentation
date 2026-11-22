<h1 align="center">
Feature Dictionary
</h1>

This document describes every column in the two customer-level tables built by [`01_customer_features.ipynb`](../03_analysis/01_customer_features.ipynb) using [`customer_features.py`](../03_analysis/customer_features.py).

| Table | Orders used | Snapshot date | Customers |
|---|---|---|---|
| `01_data/output/customer_features_full.csv` | 1 Jun 2024 – 30 Jun 2026 | 30 Jun 2026 | 39,914 |
| `01_data/output/customer_features_calibration.csv` | 1 Jun 2024 – 31 Dec 2025 | 31 Dec 2025 | 39,640 |

Both tables have one row per customer who placed at least one order in the period, keyed on `customer_id`, with the same 24 columns.

## Order status rules

| Term | Order statuses | Used for |
|---|---|---|
| **Orders placed** | All five statuses | Recency, coupon rate, COD share, cancel/return rate |
| **Valid orders** | Delivered, Shipped, Processing | Frequency, Monetary, AOV, category features |
| **Failed orders** | Cancelled, Returned | Cancel/return rate |

Recency uses orders placed because placing an order shows the customer is still engaged, even if the order later fails.

## Columns

### Clustering candidates

| Column | Definition | Range (full period, customers with valid orders) |
|---|---|---|
| `recency_days` | Days from the last order placed to the snapshot date | 0 – 758 |
| `frequency` | Number of valid orders | 1 – 18 (0 for customers with no valid orders) |
| `monetary` | Sum of `total_amount` on valid orders (₹) | ₹94 – ₹906,815 |
| `aov` | `monetary ÷ frequency` (₹). Blank when `frequency` is 0 | ₹94 – ₹341,702 |
| `coupon_rate` | Share of orders placed that used a coupon | 0 – 1 |
| `cod_share` | Share of orders placed paid by cash on delivery | 0 – 1 |
| `electronics_share` | Share of valid orders in the Electronics category. Blank when `frequency` is 0 | 0 – 1 |
| `category_breadth` | Number of distinct categories across valid orders | 1 – 3 (0 when `frequency` is 0) |
| `cancel_return_rate` | Share of orders placed that were cancelled or returned | 0 – 0.75 |

### Profiling-only behaviour

| Column | Definition |
|---|---|
| `pct_coupon_share` | Share of coupon orders that used `SAVE10` (10% off) rather than a flat ₹ coupon. Blank for customers who never used a coupon |
| `digital_share` | `1 − cod_share`: share of orders paid by UPI or card. Mirrors `cod_share`, so it is not clustered on |

### Supporting counts and dates

| Column | Definition |
|---|---|
| `orders_placed` | Number of orders placed, all statuses |
| `coupon_orders` | Number of orders placed that used a coupon |
| `coupon_discount` | Sum of `coupon_discount` on valid orders (₹) |
| `gross_order_value` | Sum of `order_value` on valid orders, before coupons and shipping (₹) |
| `first_order_date` | Date of the first order placed in the period |
| `last_order_date` | Date of the last order placed in the period |

### Customer profile (never clustered on)

Taken from `Dim_Customers`. Used only to describe and validate segments.

| Column | Definition |
|---|---|
| `customer_tier` | Silver, Gold or Platinum, as assigned by the business |
| `age_group` | Age band |
| `state` | Customer state |
| `gender` | Customer gender |
| `registration_date` | Date the customer registered |
| `registration_cohort` | Registration month (`YYYY-MM`), 12 cohorts from 2023-06 to 2024-05 |
| `tenure_days` | Days from registration to the snapshot date |

## Treatment decisions from NB01

| Decision | Reason *[NB01]* |
|---|---|
| Customers with no valid orders are kept in the tables but excluded from clustering | 66 customers (0.17%) in the full period have no spend, basket or category mix to compare |
| `frequency`, `monetary` and `aov` are log-transformed before clustering | Spend is right-skewed (skewness 1.40); AOV is more skewed still (2.08) |
| `pct_coupon_share` is profiling only | Undefined for the 28.3% of customers who never used a coupon |
| Clustering uses log Frequency and log AOV instead of log Monetary (proposed, confirmed in NB03) | Monetary and AOV correlate at ρ = 0.88; log Monetary = log Frequency + log AOV, so nothing is lost |
| `cancel/return rate` and a Recency transformation are tested in NB03 | Cancel/return rate is mostly zero; Recency has a long tail (skewness 1.69) |
