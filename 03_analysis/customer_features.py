"""Customer-level feature engineering for the segmentation project.

Every notebook in this repository builds customer features through this module,
so the full-period table (NB01, NB03) and the calibration table used for holdout
validation (NB04) follow exactly the same rules.

Rules (see 02_documentation/analysis_charter.md, "Customer feature set"):
- Valid orders are Delivered, Shipped and Processing. Cancelled and Returned
  orders produce no revenue and are excluded from Frequency and Monetary.
- Recency uses the last order *placed*, whatever its status.
- Coupon, payment and cancel/return rates use every order placed.
- Category features use valid orders only.
"""

from pathlib import Path

import numpy as np
import pandas as pd

VALID_STATUSES = ["Delivered", "Shipped", "Processing"]
FAILED_STATUSES = ["Cancelled", "Returned"]

FULL_START, FULL_END = pd.Timestamp("2024-06-01"), pd.Timestamp("2026-06-30")
CALIBRATION_END = pd.Timestamp("2025-12-31")
HOLDOUT_START = pd.Timestamp("2026-01-01")


def load_data(data_dir):
    """Load the three processed tables and attach product category to each order."""
    data_dir = Path(data_dir)
    fact = pd.read_csv(
        data_dir / "Fact_Sales.csv",
        parse_dates=["order_date", "delivery_date", "registration_date"],
    )
    customers = pd.read_csv(data_dir / "Dim_Customers.csv", parse_dates=["registration_date"])
    products = pd.read_csv(data_dir / "Dim_Products.csv")
    fact = fact.merge(products[["product_id", "category"]], on="product_id", how="left", validate="m:1")
    return fact, customers, products


def build_customer_features(fact, customers, start, end, snapshot):
    """Return one row per customer who placed at least one order between start and end.

    Parameters
    ----------
    fact : order-level table from load_data (with `category`)
    customers : Dim_Customers
    start, end : inclusive order-date window
    snapshot : date Recency and tenure are measured to
    """
    window = fact[(fact["order_date"] >= start) & (fact["order_date"] <= end)].copy()
    window["is_valid"] = window["order_status"].isin(VALID_STATUSES)
    window["is_failed"] = window["order_status"].isin(FAILED_STATUSES)
    window["is_coupon"] = window["coupon_used"].eq("Yes")
    window["is_pct_coupon"] = window["coupon_code"].eq("SAVE10")
    window["is_cod"] = window["payment_mode"].eq("COD")
    window["is_electronics"] = window["category"].eq("Electronics")

    placed = window.groupby("customer_id").agg(
        orders_placed=("order_id", "count"),
        first_order_date=("order_date", "min"),
        last_order_date=("order_date", "max"),
        coupon_orders=("is_coupon", "sum"),
        pct_coupon_orders=("is_pct_coupon", "sum"),
        coupon_rate=("is_coupon", "mean"),
        cod_share=("is_cod", "mean"),
        cancel_return_rate=("is_failed", "mean"),
    )

    valid = window[window["is_valid"]]
    valid_agg = valid.groupby("customer_id").agg(
        frequency=("order_id", "count"),
        monetary=("total_amount", "sum"),
        coupon_discount=("coupon_discount", "sum"),
        gross_order_value=("order_value", "sum"),
        electronics_share=("is_electronics", "mean"),
        category_breadth=("category", "nunique"),
    )

    feats = placed.join(valid_agg, how="left")
    feats["frequency"] = feats["frequency"].fillna(0).astype(int)
    feats["monetary"] = feats["monetary"].fillna(0.0)
    feats["category_breadth"] = feats["category_breadth"].fillna(0).astype(int)
    feats["aov"] = np.where(feats["frequency"] > 0, feats["monetary"] / feats["frequency"].replace(0, np.nan), np.nan)
    feats["recency_days"] = (snapshot - feats["last_order_date"]).dt.days
    feats["pct_coupon_share"] = feats["pct_coupon_orders"] / feats["coupon_orders"].replace(0, np.nan)
    feats["digital_share"] = 1 - feats["cod_share"]

    profile = customers.set_index("customer_id")[
        ["customer_tier", "age_group", "state", "gender", "registration_date"]
    ]
    feats = feats.join(profile, how="left")
    feats["tenure_days"] = (snapshot - feats["registration_date"]).dt.days
    feats["registration_cohort"] = feats["registration_date"].dt.to_period("M").astype(str)

    columns = [
        # RFM
        "recency_days", "frequency", "monetary",
        # basket, promotion, payment, category, risk
        "aov", "coupon_rate", "pct_coupon_share", "cod_share", "digital_share",
        "electronics_share", "category_breadth", "cancel_return_rate",
        # supporting counts and dates
        "orders_placed", "coupon_orders", "coupon_discount", "gross_order_value",
        "first_order_date", "last_order_date",
        # profiling only (never clustered on)
        "customer_tier", "age_group", "state", "gender",
        "registration_date", "registration_cohort", "tenure_days",
    ]
    return feats[columns].sort_index()


def full_period_features(fact, customers):
    """Features for 1 Jun 2024 - 30 Jun 2026, snapshot 30 Jun 2026."""
    return build_customer_features(fact, customers, FULL_START, FULL_END, FULL_END)


def calibration_features(fact, customers):
    """Features for 1 Jun 2024 - 31 Dec 2025, snapshot 31 Dec 2025 (holdout validation)."""
    return build_customer_features(fact, customers, FULL_START, CALIBRATION_END, CALIBRATION_END)
