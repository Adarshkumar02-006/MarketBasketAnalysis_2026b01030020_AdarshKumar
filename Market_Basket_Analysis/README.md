# Market Basket Analysis

- **Domain:** Retail and e-commerce
- **Core Stack:** Python (Pandas, NumPy), Oracle SQL (DDL, views, self-joins), Power BI

## Repository Structure
- `src/01_generate_data.py` — Synthetic grocery/retail basket data generator with edge cases (single-item baskets, rare items, duplicate basket lines).
- `src/02_clean_and_rules.py` — Data cleaning script, data-quality report generator, and association rules engine (Support, Confidence, Lift).
- `sql/01_ddl_and_load.sql` — Oracle SQL schema DDL (`dim_products`, `fact_basket_items`).
- `sql/02_association_queries_and_views.sql` — Oracle SQL self-join view (`vw_market_basket_rules`) and Top 10 pairs query.
- `powerbi/DAX_Measures.txt` — DAX KPI definitions for Power BI pair matrix and slicers.
- `docs/data_quality_report.csv` — Audit log of data-quality fixes.

## Execution & Verification
1. Run `python src/01_generate_data.py`
2. Run `python src/02_clean_and_rules.py`
3. Execute `sql/01_ddl_and_load.sql` and `sql/02_association_queries_and_views.sql` in Oracle SQL to verify pair counts match `data/clean/association_rules.csv`.
