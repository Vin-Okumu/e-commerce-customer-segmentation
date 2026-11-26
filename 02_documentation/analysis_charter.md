<h1 align="center">
Analysis Charter
</h1>

<p align="center">
<b>E-Commerce Customer Segmentation: RFM and K-Means Analysis of Who Drives, and Who Threatens, Revenue</b>
</p>

## Project Purpose

### Background

This project follows on from [e-commerce-sales-analytics](https://github.com/Vin-Okumu/e-commerce-sales-analytics), a six-page Power BI analysis of 250,000 orders from an Indian e-commerce retailer. That project established that:

- revenue for Jan–Jun 2026 was flat year on year (₹1.41 bn, −0.07%) *[Report §1]*;
- repeat customers produced 77.3% of revenue *[Report §3.4]*;
- Platinum-tier customers (71% of active customers) produced 90.0% of revenue *[Report §3.3]*;
- Electronics produced 72.7% of revenue *[Report §3.2]*.

Its recommendations were to make retention the main growth lever, protect Platinum customers while moving Silver and Gold up, and reduce dependence on Electronics through cross-selling *[Report §4]*. Each of those recommendations needs a list of **which customers** to act on, and the dashboard did not produce one. Two charter questions were also left for a later phase: discount efficiency (Q3) and customer value by tenure and cohort (Q7) *[Report §5]*.

This project builds that customer layer.

### Business Objective

Segment the retailer's customers by how they actually buy, measure the revenue each segment produces and the revenue each segment puts at risk, and turn the segments into specific retention, promotion and cross-sell actions.

The analysis uses Python (pandas, scikit-learn) for feature engineering, RFM scoring and K-means clustering, and presents the results as segment profiles, a customer-level scored file and an action playbook.

**Core analytical question:**

> *Which groups of customers drive and threaten our revenue, how do they behave, and what should we do differently for each one?*

### The executive's view

The questions below are framed the way the retailer's leadership would ask them. Each one becomes an objective.

| # | Executive question | Objective |
|---|---|---|
| 1 | "Beyond Silver, Gold and Platinum, who are our customers really?" | Build a behaviour-based segmentation |
| 2 | "Is our tier programme rewarding the right people?" | Test the loyalty tiers against real behaviour |
| 3 | "Who is slipping away, how much revenue goes with them, and do customers get more valuable over time?" | Measure lapse risk and the revenue tied to it |
| 4 | "Are coupons building loyalty, or subsidising people who would buy anyway?" | Judge whether coupons are worth what they cost |
| 5 | "Which customers can help us depend less on Electronics?" | Find who can reduce the Electronics dependence |
| 6 | "Where should the next rupee of retention and marketing spend go?" | Turn the segments into an action plan |

The objectives progress from **description** (who the customers are) to **validation** (does the segmentation hold up against tiers and future behaviour), then **diagnosis** (lapse, coupons, category concentration) and finally **action** (the playbook).

---

## Data

### Source

The processed tables from the first project, `01_data/processed/` in [e-commerce-sales-analytics](https://github.com/Vin-Okumu/e-commerce-sales-analytics). They are copied into this repository unchanged, so both projects work from the same numbers.

| Table | Rows | Grain | Used for |
|---|---|---|---|
| `Fact_Sales` | 250,000 | One order (one product per order) | Every customer-level feature |
| `Dim_Customers` | 40,000 | One customer | Tier, registration date, age group, state (profiling and validation only) |
| `Dim_Products` | 2,000 | One product | Product category, for category mix |

- **Period:** 1 June 2024 to 30 June 2026 (25 months).
- **Customers with at least one order:** 39,914 *[Dictionary, Data model]*.
- **Market and currency:** India, Indian rupees (₹).

### Time windows

| Window | Dates | Purpose |
|---|---|---|
| Full period | 1 Jun 2024 – 30 Jun 2026 | Final segmentation and the customer-level scored file. Snapshot date: **30 Jun 2026** |
| Calibration | 1 Jun 2024 – 31 Dec 2025 (19 months) | Fit a separate version of the segmentation for validation. Snapshot date: **31 Dec 2025** |
| Holdout | 1 Jan 2026 – 30 Jun 2026 (6 months) | Check what calibration segments actually did next (Objective 3). Matches the first project's reporting period |

### Where the figures in this project come from

Every figure in this repository has one of two sources, and each one is cited:

1. **Reported in the first project.** Cited to the document and section where it appears, for example *[Report §3.4]*.
2. **Calculated in this project.** Cited to the notebook that calculates it, for example *[Notebook 1]*.

This charter is written before any analysis is run in this repository, so the only figures it contains come from the first project. Questions that need new figures are listed below and answered in the notebooks.

**Source key**

| Tag | Document |
|---|---|
| *Report* | [`analysis_report.md`](https://github.com/Vin-Okumu/e-commerce-sales-analytics/blob/main/02_documentation/analysis_report.md) in e-commerce-sales-analytics |
| *Dictionary* | [`data_dictionary.md`](https://github.com/Vin-Okumu/e-commerce-sales-analytics/blob/main/02_documentation/data_dictionary.md) in e-commerce-sales-analytics |
| *Notebook 1–Notebook 6* | Notebooks `03_analysis/01`–`06` in this repository |

### What the first project established

| Finding | Source | Why it matters here |
|---|---|---|
| 13,404 customers (43% of active customers) placed only one order in Jan–Jun 2026, while 17,436 (57%) placed two or more | Report §3.4 | "One-time" was measured **within a six-month window**. This project measures purchase history over the full 25 months, to see whether these customers are truly new to repeat buying or are existing customers who have slowed down |
| Repeat customers are worth about 2.6 times as much as one-time customers and produce 77.3% of revenue | Report §3.4 | Retention is the main lever, so Recency and Frequency are central to the segmentation |
| Platinum customers are 71% of active customers and produce 90.0% of revenue; repeat rates are 60.2% (Platinum), 51.9% (Gold) and 41.5% (Silver) | Report §3.3 | The tier system lines up with spend, but tier is partly assigned on spend (README, *Notes on scope*), so it cannot be used as a clustering feature |
| Electronics produces 72.7% of revenue, with an average order value of ₹64,966 against ₹914–₹21,178 for other categories | Report §3.2 | Category mix and order value are likely to separate customers, and Electronics dependence is a business risk to target |
| Coupon discounts were ₹14.8 M, 1.04% of gross order value, and 20% of orders used a coupon | Report §3.2 | Coupons are cheap overall. Whether they change customer behaviour has not been tested (deferred charter Q3) |
| Coupons used: `SAVE10` (10% of order value), `FLAT50` (₹50) and `DIWALI100` (₹100) | Dictionary, *Fact_Sales* | Percentage and flat coupons can be compared |
| UPI is used for 51% of orders, cash on delivery for 33%, debit card for 11% and credit card for 4% | Report §3.5 | Payment mix varies enough to be a feature |
| Cancelled and returned orders account for about 10% of orders and ₹138.5 M (9.8%) of NTV | Report §3.5 | A customer's cancel/return rate is a candidate risk feature |
| All customers registered between 1 Jun 2023 and 31 May 2024; orders run from 1 Jun 2024 | Dictionary, *Dim_Customers* and *Fact_Sales* | The customer base is closed: nobody new joins during the data period, which keeps cohort and tenure comparisons clean |
| `total_orders` and `total_spent` in the customer file match the transactions for only 28.7% of customers | Report §5 | All customer metrics must be calculated from `Fact_Sales` |
| The data is likely synthetic (very even status split and delivery-day spread) | Report §5 | Clusters may be weakly separated, and this must be reported honestly |

### Data questions to answer first (Notebook 1)

These questions shape how the features are built:

- How many orders does each customer place over the full 25 months, and how many customers have only one order in their whole history?
- Of the 13,404 customers who bought once in Jan–Jun 2026, how many had bought before?
- How many customers who ordered between Jun 2024 and Dec 2025 placed no order in Jan–Jun 2026?
- How is Recency (days since last order) distributed at the 30 Jun 2026 snapshot?
- How skewed is spend per customer, and does it need a log transformation?
- What share of orders (not revenue) is Electronics, and how many customers never buy Electronics or buy nothing else?
- How many distinct categories does each customer buy from?
- How does order value differ between coupon and non-coupon orders, and how many customers never use a coupon?
- Does the cancel/return rate differ by payment method?

---

## Customer feature set

All features are calculated per customer from `Fact_Sales`. The `total_orders` and `total_spent` columns in `Dim_Customers` match the transaction data for only 28.7% of customers *[Report §5]*, so they are not used.

### Order status rule

- **Valid orders** are Delivered, Shipped and Processing. Cancelled and Returned orders are excluded from Frequency and Monetary because they produce no revenue.
- **Recency** uses the last order **placed**, whatever its status, because placing an order shows the customer is still engaged.
- Each customer's cancel/return rate is kept as a separate feature, so failed orders are measured rather than ignored.

### Features

| Group | Feature | Definition | Treatment |
|---|---|---|---|
| RFM | Recency | Days from last order placed to snapshot date | Scaled |
| RFM | Frequency | Number of valid orders | Log-transformed, scaled |
| RFM | Monetary | Sum of `total_amount` on valid orders | Log-transformed, scaled |
| Basket | Average order value | Monetary ÷ Frequency | Log-transformed, scaled. Checked for overlap with Monetary |
| Promotion | Coupon rate | Share of orders using any coupon | Scaled |
| Promotion | Percentage-coupon share | Share of coupon orders using `SAVE10` (10% off) rather than a flat ₹ coupon | Profiling only, if too sparse to cluster on |
| Payment | COD share | Share of orders paid cash on delivery | Scaled |
| Payment | Digital share | Share of orders paid by UPI or card | Profiling only. Mirrors COD share, so it is not clustered on |
| Category | Electronics share | Share of valid orders in Electronics | Scaled |
| Category | Category breadth | Number of distinct categories bought (1–3) | Scaled |
| Risk | Cancel/return rate | Share of orders cancelled or returned | Scaled. Tested for inclusion |
| Profiling only | Tier, age group, state, gender, tenure, registration cohort | From `Dim_Customers` | **Not clustered on.** Used to describe and validate segments |

Category mix is summarised as Electronics share plus category breadth, instead of 7 raw category shares. Seven shares would dominate the distance calculation in K-means and produce clusters that only reflect category.

### Core formulas

Recency

$$ Recency = Snapshot\ Date - Last\ Order\ Date $$

Frequency

$$ Frequency = COUNT(Valid\ Orders) $$

Monetary

$$ Monetary = \sum TotalAmount_{valid} $$

Average order value

$$ AOV = \frac{Monetary}{Frequency} $$

Coupon rate

$$ Coupon\ Rate = \frac{Orders\ with\ Coupon}{Total\ Orders} $$

Electronics share

$$ Electronics\ Share = \frac{Valid\ Electronics\ Orders}{Valid\ Orders} $$

---

## Objective 1 — Find out what customer groups we actually have

**Executive question:** *"Beyond Silver, Gold and Platinum, who are our customers really?"*

### Decision being supported

Management needs one shared set of customer segments that marketing, CRM and leadership all use, based on how customers buy rather than on a tier label.

### Key questions

- How many distinct behavioural groups exist?
- What separates them: recency, spend, basket size, category, coupons or payment?
- How much revenue does each group produce, and how many customers does it hold?
- Do K-means clusters tell a better story than standard rule-based RFM scoring?

### Hypothesis

Category mix (especially Electronics share) and spend will separate customers more strongly than coupon use or payment mode.

### Analysis

1. **Rule-based RFM baseline.** Score each customer 1–5 on Recency, Frequency and Monetary using quintiles. Map the scores to standard RFM segments (Champions, Loyal, At Risk, Hibernating and so on).
2. **K-means segmentation.** Cluster customers on the feature set above, after transforming and scaling.
3. **Choosing the number of clusters (k)** for k = 2 to 10, using four tests together:
   - the elbow in within-cluster variance;
   - the silhouette score;
   - stability across 50 bootstrap resamples, measured with the adjusted Rand index;
   - whether each cluster is large enough and distinct enough to act on.
4. **Feature check.** Check correlations between features and drop any that duplicate another.
5. **Visualise** the clusters on a two-dimensional projection (PCA) and with feature profile charts.
6. **Compare** the K-means clusters with the rule-based RFM segments in a cross-tabulation.

### Metrics

Customers, share of customers, revenue, share of revenue, mean Recency, Frequency, Monetary and AOV, coupon rate, COD share, Electronics share and category breadth, all per segment.

### Success measure

Between 4 and 7 segments that are stable across resamples (mean adjusted Rand index of at least 0.8), each holding at least 3% of customers, with profiles a marketer can act on. The silhouette score and stability are reported honestly, even if they are weak.

### Output

A named segment for every customer, plus a one-page profile card per segment.

---

## Objective 2 — Test whether the loyalty tiers match real behaviour

**Executive question:** *"Is our tier programme rewarding the right people?"*

### Decision being supported

Decide whether the tier rules need changing, and which customers should be upgraded or targeted for win-back.

### Key questions

- How closely do the K-means segments line up with Silver, Gold and Platinum?
- Which Silver and Gold customers behave like the best customers?
- Which Platinum customers are lapsing or spending little?
- How much revenue sits in each mismatch?

### Hypothesis

Tier is partly assigned on spend, so it lines up with Monetary but not with Recency. Some Platinum customers are lapsing, and some Silver and Gold customers already behave like top customers.

### Analysis

- Cross-tabulate segment against tier, as counts and as revenue.
- Measure agreement with Cramér's V and the adjusted Rand index.
- Flag two groups:
  - **Under-tiered:** Silver or Gold customers in a top-value segment.
  - **Over-tiered:** Platinum customers in a lapsing or low-value segment.

### Metrics

Customers and ₹ value per tier–segment cell, agreement scores, and the size of the under-tiered and over-tiered groups.

### Success measure

Counts and ₹ value for customers who should move up a tier and for Platinum customers who are drifting away.

### Output

A tier–segment matrix and two lists of customers, one to upgrade and one for Platinum win-back.

---

## Objective 3 — Measure lapse risk and the revenue tied to it

**Executive question:** *"Who is slipping away, how much revenue goes with them, and do customers get more valuable over time?"*

This objective also covers deferred charter **Q7** from the first project (customer value by tenure and cohort).

### Decision being supported

Decide who to target for win-back, how early to step in, and whether long-standing customers deserve different treatment.

### Key questions

- Which segments have the highest lapse rate?
- How much revenue is at risk in each segment?
- Does the segmentation predict who actually stops buying?
- How long a gap between orders signals that a customer is lapsing?
- Do customers become more or less valuable as their tenure grows?
- Which registration cohorts hold their value best?

### Hypothesis

Segments with low Recency or falling Frequency at the end of 2025 account for most of the customers who bought between Jun 2024 and Dec 2025 but placed no order in Jan–Jun 2026. The size of that group is calculated in Notebook 1.

### Analysis

1. **Holdout validation.**
   - Rebuild the features and segments using only calibration data, with a snapshot date of 31 Dec 2025.
   - Measure each segment's actual behaviour in Jan–Jun 2026: the share that ordered again, and the revenue they produced.
   - Compare the rule-based RFM segments with the K-means segments on how well they separate customers who lapsed from those who stayed. Use lift over the average and the area under the ROC curve of a simple recency-based score.
2. **Revenue at risk.** For each segment, multiply the number of lapsing customers by their average spend per six months during calibration.
3. **Purchase gap.** Measure the distribution of days between orders, to set a practical "lapsed" threshold. For example, a customer is lapsed if their gap exceeds the 90th percentile of normal gaps.
4. **Cohort and tenure.**
   - Group customers by registration month (12 cohorts).
   - Track orders and spend by months since registration.
   - Test whether spend per period rises or falls with tenure.

### Metrics

Lapse rate

$$ Lapse\ Rate = \frac{Calibration\ Customers\ with\ No\ Holdout\ Order}{Calibration\ Customers} $$

Revenue at risk

$$ Revenue\ at\ Risk = Lapsing\ Customers \times Average\ Six\text{-}Month\ Spend $$

Lift

$$ Lift = \frac{Segment\ Lapse\ Rate}{Overall\ Lapse\ Rate} $$

### Success measure

- A lapse rate and ₹ at risk for each segment.
- Evidence that the segments separate lapsers from customers who stayed better than chance.
- A ranked win-back list.
- A clear answer on whether value builds or fades with tenure.

### Output

A lapse-risk table, a cohort heatmap, a recommended lapse threshold in days, and a ranked win-back list.

---

## Objective 4 — Judge whether coupons are worth what they cost

**Executive question:** *"Are coupons building loyalty, or subsidising people who would buy anyway?"*

This objective covers deferred charter **Q3** from the first project (discount efficiency).

### Decision being supported

Decide which segments should receive coupons, which type of coupon to use, and where discounting can stop.

### Key questions

- Which segments depend most on coupons?
- How much does each segment cost in coupon discounts?
- Do coupon users spend more per order than non-users in the same segment?
- Do coupon users keep buying longer, or lapse less, than non-users?
- Do 10%-off coupons (`SAVE10`) and flat coupons (`FLAT50`, `DIWALI100`) attract different customers?

### Hypothesis

Coupons cost little overall (1.04% of gross order value *[Report §3.2]*) and do little to raise order value, but they may be linked to customers continuing to buy in certain segments. The order-value comparison is calculated in Notebook 1 and broken down by segment in Notebook 5.

### Analysis

- Coupon rate, coupon cost and AOV with and without coupons, by segment.
- Holdout lapse rate for coupon users against non-users, within each segment, so customers are compared with similar customers.
- Coupon type mix by segment.
- Coupon cost as a share of segment revenue.

### Metrics

Coupon cost rate

$$ Coupon\ Cost\ Rate = \frac{\sum CouponDiscount}{\sum OrderValue} $$

AOV difference

$$ AOV\ Difference = AOV_{coupon} - AOV_{no\ coupon} $$

### Success measure

For each segment: coupon cost as a share of spend, the AOV difference, and the difference in repeat buying between coupon users and non-users.

All results are labelled as **associations, not proof of cause**. Customers choose whether to use coupons, so a fair test of cause would need a controlled experiment. The charter recommends one as a next step.

### Output

A coupon efficiency table by segment, with a recommendation (keep, target or reduce) for each.

---

## Objective 5 — Find who can reduce the Electronics dependence

**Executive question:** *"Which customers can help us depend less on Electronics?"*

### Decision being supported

Decide who to target for cross-selling, and with which category.

### Key questions

- Which segments rely most on Electronics?
- Which high-value customers buy only or mostly Electronics?
- Which categories do Electronics buyers already buy alongside it?
- How much revenue could cross-selling realistically add?

### Hypothesis

High-spending customers who mostly buy Electronics are both the biggest concentration risk and the best cross-sell target.

### Analysis

- Group customers by Electronics share: Electronics-led (more than 50% of valid orders), mixed (1–50%) and non-Electronics (0%).
- Cross-tabulate these groups with segment and with Monetary.
- Count which categories appear together in customers' baskets, to find the most natural next category for Electronics-led customers.
- Size the opportunity under a stated assumption. For example: "if 10% of Electronics-led high spenders add one order in their most likely next category at that category's average order value".

### Metrics

Electronics share of revenue by segment, customers per group, category pairs bought together, and estimated cross-sell revenue.

### Success measure

The size of each cross-sell target group, and a revenue estimate with its assumption stated.

### Output

A cross-sell target list and a recommended next category for each segment.

---

## Objective 6 — Turn the segments into an action plan

**Executive question:** *"Where should the next rupee of retention and marketing spend go?"*

This is the synthesis objective, picking up from Q12 in the first project.

### Decision being supported

Rank the segments by value at stake and give each one a clear treatment that management can fund and track.

### Playbook contents (one card per segment)

| Field | Source |
|---|---|
| Size and share of revenue | Objective 1 |
| Behaviour summary | Objective 1 |
| Tier mismatch | Objective 2 |
| Lapse risk and ₹ at risk | Objective 3 |
| Coupon response | Objective 4 |
| Cross-sell potential | Objective 5 |
| Recommended action and offer | Synthesis |
| KPI to track | Synthesis |

### Prioritisation framework

| Situation | Action |
|---|---|
| High value, recent and frequent | **Protect:** priority service and early access, no discounts needed |
| High value but lapsing | **Win back:** personal outreach, timed to the lapse threshold |
| Mid value with growing frequency | **Develop:** cross-sell into the next likely category |
| Coupon-dependent with low value | **Review discounting:** limit or switch to flat coupons |
| Low value and lapsed | **Deprioritise:** low-cost automated contact only |

### Success measure

Segments ranked by ₹ value at stake, each with one action and one KPI.

### Output

The segment playbook, a scored customer-level file (`customer_id`, segment, RFM scores, lapse flag, cross-sell flag) that marketing could load into a CRM, and an executive summary.

---

## Assumptions and limitations

- **Revenue, not profit.** The data has no cost-of-goods information, so all values describe revenue. "Value at stake" means revenue at stake.
- **Likely synthetic data.** The first project noted very even distributions (order statuses split 80/5/5/5/5, delivery days spread almost uniformly) *[Report §5]*. Clusters may be weakly separated. If so, this is reported with the silhouette and stability scores, not hidden.
- **Tier is partly spend-based.** Tier is excluded from clustering and used only for validation, so the comparison in Objective 2 is not circular.
- **Coupon findings are associations.** Customers choose to use coupons, so coupon results cannot prove cause.
- **Shipped and Processing orders are counted as valid** although they have not been delivered yet. Their share of the most recent orders will be reported so readers can judge the effect.
- **The customer base is closed.** All customers registered before the data period, so the project says nothing about acquiring new customers.

## Planned deliverables

| Deliverable | Description |
|---|---|
| `03_analysis/01_customer_features.ipynb` | Builds the customer-level table and checks feature quality |
| `03_analysis/02_rfm_baseline.ipynb` | Rule-based RFM scoring and segments |
| `03_analysis/03_kmeans_segmentation.ipynb` | Choosing k, clustering, stability checks and profiling |
| `03_analysis/04_validation_tier_and_holdout.ipynb` | Objectives 2 and 3 |
| `03_analysis/05_coupons_and_cross_sell.ipynb` | Objectives 4 and 5 |
| `03_analysis/06_segment_playbook.ipynb` | Objective 6: calculates every figure in the playbook, sizes the recommended trials and builds the scored customer file *(added during the project, so that playbook figures are calculated in a notebook)* |
| `04_report/segment_playbook.md` | Objective 6 playbook and executive summary |
| `04_report/figures/` | Charts used in the README and playbook |
| `01_data/output/customer_segments.csv` | Scored customer-level file |

## Planned repository structure

```
e-commerce-customer-segmentation/
├── 01_data/
│   ├── processed/        # copied from e-commerce-sales-analytics, unchanged
│   └── output/           # customer-level features and segment assignments
├── 02_documentation/
│   ├── analysis_charter.md
│   └── feature_dictionary.md
├── 03_analysis/          # notebooks 01–06
├── 04_report/
│   ├── segment_playbook.md
│   └── figures/
├── requirements.txt
├── LICENSE
└── README.md
```
