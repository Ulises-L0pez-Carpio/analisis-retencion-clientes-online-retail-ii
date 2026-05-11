-- Perfil de recurrencia de clientes.

WITH clientes AS (
    SELECT *
    FROM read_parquet('data/processed/clientes__base_analitica__v1.parquet')
)
SELECT
    primary_country,
    COUNT(*) AS n_customers,
    SUM(CASE WHEN is_repeat_customer THEN 1 ELSE 0 END) AS n_repeat_customers,
    AVG(CASE WHEN is_repeat_customer THEN 1.0 ELSE 0.0 END) AS repeat_rate,
    SUM(total_revenue_gbp) AS revenue_total_gbp,
    AVG(avg_order_value_gbp) AS avg_order_value_gbp
FROM clientes
GROUP BY primary_country
ORDER BY revenue_total_gbp DESC;
