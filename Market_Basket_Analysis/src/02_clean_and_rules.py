import os
from collections import Counter
from itertools import combinations
import pandas as pd

os.makedirs("data/clean", exist_ok=True)
os.makedirs("docs", exist_ok=True)

tx = pd.read_csv("data/raw/transactions_raw.csv")
prod = pd.read_csv("data/raw/products_raw.csv")

log = []
missing_cust = int(tx["customer_id"].isna().sum())
tx["customer_id"] = tx["customer_id"].fillna("GUEST")
log.append(["Missing customer_id", "Imputed missing customer_id as GUEST", missing_cust])

before_dedup = len(tx)
tx = tx.groupby(["basket_id", "customer_id", "product_id", "transaction_date", "store_region"], as_index=False)["quantity"].sum()
log.append(["Duplicate lines in basket", "Summed quantity for duplicate (basket_id, product_id) lines", int(before_dedup - len(tx))])

tx = tx.merge(prod[["product_id", "unit_price"]], on="product_id", how="left")
tx["line_total"] = tx["quantity"] * tx["unit_price"]

tx.to_csv("data/clean/transactions_clean.csv", index=False)
prod.to_csv("data/clean/products_clean.csv", index=False)
pd.DataFrame(log, columns=["issue", "rule_applied", "rows_affected"]).to_csv("docs/data_quality_report.csv", index=False)

baskets = tx.groupby("basket_id")["product_id"].apply(lambda x: sorted(set(x)))
total_baskets = len(baskets)
item_cnt = Counter()
pair_cnt = Counter()

for items in baskets:
    for item in items:
        item_cnt[item] += 1
    if len(items) >= 2:
        for pair in combinations(items, 2):
            pair_cnt[pair] += 1

name_map = prod.set_index("product_id")["product_name"].to_dict()
rules = []
for (a, b), cnt in pair_cnt.items():
    supp_ab = cnt / total_baskets
    supp_a = item_cnt[a] / total_baskets
    supp_b = item_cnt[b] / total_baskets
    rules.append({
        "antecedent_id": a,
        "antecedent": name_map[a],
        "consequent_id": b,
        "consequent": name_map[b],
        "pair_count": cnt,
        "support": round(supp_ab, 4),
        "confidence": round(supp_ab / supp_a, 4),
        "lift": round((supp_ab / supp_a) / supp_b, 4),
    })

rules_df = pd.DataFrame(rules).sort_values(by=["lift", "confidence"], ascending=False)
rules_df.to_csv("data/clean/association_rules.csv", index=False)
