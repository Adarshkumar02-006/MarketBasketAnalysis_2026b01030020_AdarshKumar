CREATE OR REPLACE VIEW vw_market_basket_rules AS
WITH total_baskets AS (
    SELECT COUNT(DISTINCT basket_id) AS total_cnt FROM fact_basket_items
),
item_counts AS (
    SELECT product_id, COUNT(DISTINCT basket_id) AS item_cnt
    FROM fact_basket_items
    GROUP BY product_id
),
pair_counts AS (
    SELECT
        a.product_id AS prod_a,
        b.product_id AS prod_b,
        COUNT(DISTINCT a.basket_id) AS pair_cnt
    FROM fact_basket_items a
    JOIN fact_basket_items b
      ON a.basket_id = b.basket_id
     AND a.product_id < b.product_id
    GROUP BY a.product_id, b.product_id
)
SELECT
    p.prod_a AS antecedent_id,
    p1.product_name AS antecedent,
    p.prod_b AS consequent_id,
    p2.product_name AS consequent,
    p.pair_cnt AS pair_count,
    ROUND(p.pair_cnt / t.total_cnt, 4) AS support,
    ROUND(p.pair_cnt / ia.item_cnt, 4) AS confidence,
    ROUND((p.pair_cnt / ia.item_cnt) / (ib.item_cnt / t.total_cnt), 4) AS lift
FROM pair_counts p
CROSS JOIN total_baskets t
JOIN item_counts ia ON p.prod_a = ia.product_id
JOIN item_counts ib ON p.prod_b = ib.product_id
JOIN dim_products p1 ON p.prod_a = p1.product_id
JOIN dim_products p2 ON p.prod_b = p2.product_id;

SELECT * FROM vw_market_basket_rules
ORDER BY lift DESC, confidence DESC
FETCH FIRST 10 ROWS ONLY;
