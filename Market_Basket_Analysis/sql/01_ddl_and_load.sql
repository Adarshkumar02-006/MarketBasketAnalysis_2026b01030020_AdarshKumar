CREATE TABLE dim_products (
    product_id   VARCHAR2(20) PRIMARY KEY,
    product_name VARCHAR2(100) NOT NULL,
    category     VARCHAR2(50) NOT NULL,
    unit_price   NUMBER(10, 2) CHECK (unit_price > 0)
);

CREATE TABLE fact_basket_items (
    basket_id        VARCHAR2(20) NOT NULL,
    customer_id      VARCHAR2(20) DEFAULT 'GUEST' NOT NULL,
    product_id       VARCHAR2(20) NOT NULL,
    quantity         NUMBER(8) CHECK (quantity > 0),
    transaction_date DATE NOT NULL,
    store_region     VARCHAR2(30) NOT NULL,
    line_total       NUMBER(12, 2),
    CONSTRAINT pk_basket_product PRIMARY KEY (basket_id, product_id),
    CONSTRAINT fk_prod FOREIGN KEY (product_id) REFERENCES dim_products(product_id)
);
