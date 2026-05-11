# Especificacion del dashboard en Power BI

## Objetivo
Construir un dashboard de portafolio con tres vistas:

1. resumen ejecutivo;
2. retencion y cohortes;
3. segmentacion RFM.

## Tablas fuente
- `clientes__base_analitica__v1.parquet`
- `cohortes__retencion_mensual__v1.parquet`
- `rfm__segmentacion_clientes__v1.parquet`

## Modelo recomendado
### Tabla `clientes`
Uso:

- KPIs generales;
- filtros por pais;
- analisis de recurrencia y revenue.

### Tabla `cohortes`
Uso:

- matriz de retencion;
- tendencias por `cohort_index`;
- comparacion por `country` y `cohort_scope`.

### Tabla `rfm`
Uso:

- distribucion por segmentos;
- scorecards de valor y recencia;
- tabla de clientes por segmento.

## Pagina 1: resumen ejecutivo
Visuales:

- tarjetas con `clientes_totales`, `repeat_rate`, `revenue_total_gbp`, `ticket_promedio_gbp`;
- linea o barras para `retencion_m1`, `retencion_m3`, `retencion_m6`, `retencion_m12`;
- barras horizontales con conteo de clientes por `rfm_segment`;
- tabla corta con top paises por revenue y repeat rate.

Filtros:

- `primary_country`;
- `snapshot_month` o periodo;
- `rfm_segment`.

## Pagina 2: retencion y cohortes
Visuales:

- heatmap de retencion por `cohort_month` vs `cohort_index`;
- linea de retencion promedio por `cohort_index`;
- tabla de cohortes con `cohort_size`, `n_customers_active`, `retention_rate`, `total_revenue_gbp`.

Filtros:

- `cohort_scope`;
- `country`;
- `cohort_month`.

Regla visual:

- diferenciar meses no observables de meses observables con retencion cero.

## Pagina 3: segmentacion RFM
Visuales:

- barras por `rfm_segment`;
- scatter o bubble chart con `frequency_orders` vs `monetary_gbp`, color por `rfm_segment`;
- distribucion de `recency_days`;
- tabla de detalle con `customer_id`, `rfm_score`, `rfm_segment`, `monetary_gbp`, `frequency_orders`, `recency_days`.

Filtros:

- `rfm_segment`;
- `r_score`;
- `f_score`;
- `m_score`;
- `primary_country`.

## Medidas minimas sugeridas
- `Clientes Totales = DISTINCTCOUNT(clientes[customer_id])`
- `Repeat Rate = DIVIDE(CALCULATE(COUNTROWS(clientes), clientes[is_repeat_customer] = TRUE()), [Clientes Totales])`
- `Revenue Total GBP = SUM(clientes[total_revenue_gbp])`
- `Ticket Promedio GBP = DIVIDE(SUM(clientes[total_revenue_gbp]), SUM(clientes[n_orders]))`
- `Clientes Activos = SUM(cohortes[n_customers_active])`
- `Retencion = DIVIDE(SUM(cohortes[n_customers_active]), SUM(cohortes[cohort_size]))`
- `Clientes RFM = DISTINCTCOUNT(rfm[customer_id])`

## Criterios de lectura
- El dashboard debe explicar primero el tamaño y valor de la base.
- Despues debe mostrar que la retencion cae por cohortes y por tiempo.
- Finalmente debe dejar claro que no todos los clientes recurrentes aportan el mismo valor.
