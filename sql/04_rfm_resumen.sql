-- Resumen ejecutivo por segmento RFM.

WITH rfm AS (
    SELECT *
    FROM read_parquet('data/processed/rfm__segmentacion_clientes__v1.parquet')
)
SELECT
    rfm_segment,
    COUNT(*) AS n_customers,
    SUM(monetary_gbp) AS revenue_total_gbp,
    AVG(recency_days) AS avg_recency_days,
    AVG(frequency_orders) AS avg_frequency_orders,
    AVG(m_score) AS avg_m_score
FROM rfm
GROUP BY rfm_segment
ORDER BY revenue_total_gbp DESC;
