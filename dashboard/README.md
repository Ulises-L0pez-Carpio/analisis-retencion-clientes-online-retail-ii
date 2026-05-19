# Dashboard de retencion, cohortes y segmentacion RFM

Dashboard en Power BI construido sobre el dataset Online Retail II (UCI Machine Learning Repository). Analiza el comportamiento de compra recurrente de clientes minoristas entre 2009 y 2010.

## Archivo

`dashboard_retencion_rfm_online_retail.pbix` — abrir con Power BI Desktop.

## Fuente de datos

El dashboard consume tres archivos Parquet desde `data/processed/`:

| Archivo | Contenido |
|---------|-----------|
| `clientes__base_analitica__v1.parquet` | 5,878 clientes con metricas de recurrencia, revenue, recencia y pais |
| `cohortes__retencion_mensual__v1.parquet` | Retencion mensual por cohorte de primera compra, desglosada por pais y scope |
| `rfm__segmentacion_clientes__v1.parquet` | Segmentacion RFM con scores R/F/M, segmento asignado, recencia, frecuencia y valor monetario |

## Estructura del dashboard

### Pagina 1 — Resumen Ejecutivo
KPIs principales del negocio: clientes totales, tasa de recompra, revenue total, ticket promedio. Retencion en horizontes clave (M1, M3, M6, M12). Clientes y revenue por segmento RFM. Top 10 paises.

### Pagina 2 — Retencion y cohortes
Heatmap de retencion por cohorte de primera compra vs meses transcurridos, diferenciando meses observables con retencion cero de meses aun no observables. Linea de retencion promedio con referencia al 50 %. Tabla de detalle por cohorte.

### Pagina 3 — Segmentacion RFM
Distribucion de clientes por segmento RFM. Histograma de recencia apilado por segmento. Scatter plot de frecuencia vs valor monetario con escalas logaritmicas y lineas de mediana. Top 100 clientes por valor monetario con formato condicional por segmento.

## Metricas principales

| Metrica | Descripcion |
|---------|-------------|
| Clientes Totales | 5,878 clientes unicos |
| Repeat Rate | 72.4 % de clientes con mas de una orden |
| Revenue Total | GBP 17.69M |
| Ticket Promedio | GBP 478 por orden |
| Retencion M1 | ~23 % (promedio primer mes post-cohorte) |
| Segmentos RFM | 11 segmentos: champions, loyal_customers, potential_loyalists, at_risk, hibernating, cant_lose_them, need_attention, new_customers, about_to_sleep, promising, lost_customers |

## Narrativa del dashboard

1. **Panorama**: la base tiene 5,878 clientes, 72 % recompra, pero el valor se concentra en pocos.
2. **Dinamica**: la retencion decae fuerte tras el primer mes y varia entre cohortes y paises.
3. **Segmentacion accionable**: los champions generan desproporcionadamente mas revenue; hibernating es el grupo mas grande y representa una oportunidad de reactivacion.
