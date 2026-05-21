-- Resumen de compras validas.

WITH compras_validas AS (
    SELECT *
    FROM read_parquet('data/processed/transacciones__compras_validas__v1.parquet')
)
SELECT
    COUNT(*) AS n_lines,
    COUNT(DISTINCT invoice_no) AS n_orders,
    COUNT(DISTINCT customer_id) AS n_customers,
    COUNT(DISTINCT country) AS n_countries,
    SUM(line_revenue_gbp) AS revenue_total_gbp,
    SUM(line_revenue_gbp) / COUNT(DISTINCT invoice_no) AS avg_order_value_gbp
FROM compras_validas;
