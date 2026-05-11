-- Retencion promedio por edad de cohorte para la vista global.

WITH cohortes AS (
    SELECT *
    FROM read_parquet('data/processed/cohortes__retencion_mensual__v1.parquet')
    WHERE cohort_scope = 'all_countries'
)
SELECT
    cohort_index,
    SUM(cohort_size) AS cohort_size_total,
    SUM(n_customers_active) AS n_customers_active_total,
    SUM(n_customers_active) * 1.0 / SUM(cohort_size) AS retention_rate_weighted,
    SUM(total_revenue_gbp) AS revenue_total_gbp
FROM cohortes
GROUP BY cohort_index
ORDER BY cohort_index;
