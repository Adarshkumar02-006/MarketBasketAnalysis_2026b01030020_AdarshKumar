import os
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

np.random.seed(42)
random.seed(42)
os.makedirs("data/raw", exist_ok=True)

products = [
    ("SKU101", "Whole Milk 1L", "Dairy", 64.0),
    ("SKU102", "Brown Bread Loaf", "Bakery", 45.0),
    ("SKU103", "Salted Butter 100g", "Dairy", 58.0),
    ("SKU104", "Assam Tea Leaves 250g", "Beverages", 140.0),
    ("SKU105", "Marie Biscuits Pack", "Snacks", 30.0),
    ("SKU106", "Basmati Rice 1kg", "Staples", 125.0),
    ("SKU107", "Toor Dal 1kg", "Staples", 160.0),
    ("SKU108", "Fresh Paneer 200g", "Dairy", 90.0),
    ("SKU109", "Fresh Curd 400g", "Dairy", 36.0),
    ("SKU110", "Potato Chips Classic", "Snacks", 20.0),
    ("SKU111", "Cola Bottle 750ml", "Beverages", 40.0),
    ("SKU112", "Organic Bananas 6 pcs", "Produce", 48.0),
    ("SKU113", "Alphonso Mangoes 1kg", "Produce", 220.0),
    ("SKU114", "Farm Eggs 6 pcs", "Dairy", 54.0),
    ("SKU115", "Saffron Threads 1g", "Gourmet", 499.0),
]
df_prod = pd.DataFrame(products, columns=["product_id", "product_name", "category", "unit_price"])
df_prod.to_csv("data/raw/products_raw.csv", index=False)

bundles = [
    (["SKU101", "SKU102", "SKU103"], 0.25),
    (["SKU104", "SKU105"], 0.22),
    (["SKU106", "SKU107"], 0.20),
    (["SKU108", "SKU109"], 0.18),
    (["SKU110", "SKU111"], 0.15),
]

rows = []
start_dt = datetime(2026, 6, 1)
for i in range(1, 601):
    bid = f"BSK{i:04d}"
    cid = f"C{random.randint(100, 400)}"
    dt = (start_dt + timedelta(days=random.randint(0, 90))).strftime("%Y-%m-%d")
    region = random.choice(["North", "South", "West", "East"])
    if random.random() < 0.10:
        items = [random.choice(df_prod["product_id"].tolist())]
    else:
        base = random.choices([b[0] for b in bundles], weights=[b[1] for b in bundles])[0]
        extras = random.sample(df_prod["product_id"].tolist(), k=random.randint(0, 2))
        items = list(set(base + extras))
    for item in items:
        rows.append([bid, cid, item, random.randint(1, 4), dt, region])

df_tx = pd.DataFrame(rows, columns=["basket_id", "customer_id", "product_id", "quantity", "transaction_date", "store_region"])
df_tx = pd.concat([df_tx, df_tx.sample(20, random_state=42)], ignore_index=True)
df_tx.loc[df_tx.sample(15, random_state=7).index, "customer_id"] = np.nan
df_tx.to_csv("data/raw/transactions_raw.csv", index=False)
