# Dashboard de retencion, cohortes y segmentacion RFM

Dashboard en Power BI construido sobre el dataset `Online Retail II` para analizar comportamiento de compra recurrente entre diciembre de 2009 y diciembre de 2011.

## Presentacion del dashboard
Esta seccion resume la propuesta visual del caso y muestra las tres vistas principales utilizadas para comunicar los hallazgos del analisis.

La lectura del dashboard se apoya en las imagenes incluidas en esta carpeta y en la descripcion metodologica de cada pagina.

## Evidencia visual disponible
- `pagina1.png`
- `pagina2.png`
- `pagina3.png`

## Archivo de referencia tecnica
`dashboard_retencion_rfm_online_retail.pbix`

Se conserva como respaldo tecnico del trabajo realizado en Power BI.

## Fuente de datos
El dashboard consume tres archivos Parquet desde `data/processed/`:

| Archivo | Contenido |
| --- | --- |
| `clientes__base_analitica__v1.parquet` | 5,878 clientes con metricas de recurrencia, ingresos, recencia y pais principal |
| `cohortes__retencion_mensual__v1.parquet` | Retencion mensual por cohorte de primera compra, con aperturas por pais y alcance |
| `rfm__segmentacion_clientes__v1.parquet` | Segmentacion RFM con scores `R/F/M`, segmento final, recencia, frecuencia y valor monetario |

## Estructura del dashboard
### Pagina 1. Resumen ejecutivo
KPIs de clientes, recompra, ingresos, ticket promedio y retencion en horizontes M1, M3, M6 y M12. Tambien resume clientes e ingresos por segmento RFM, junto con la lectura geografica principal.

![Pagina 1 del dashboard](pagina1.png)

### Pagina 2. Retencion y cohortes
Heatmap de retencion por cohorte de primera compra frente a meses transcurridos. Distingue meses observables con retencion cero de meses todavia no observables e incorpora lectura de tendencia y tabla de detalle por cohorte.

![Pagina 2 del dashboard](pagina2.png)

### Pagina 3. Segmentacion RFM
Distribucion de clientes por segmento, dispersion entre frecuencia y valor monetario, lectura de recencia y tabla de clientes de mayor valor con formato condicional.

![Pagina 3 del dashboard](pagina3.png)

## Metricas principales
| Metrica | Descripcion |
| --- | --- |
| Clientes Totales | 5,878 clientes unicos |
| Tasa de recompra | 72.39% de clientes con mas de una orden |
| Ingresos totales | GBP 17.69M |
| Ticket Promedio | GBP 478.39 por orden |
| Retencion M1 | 23.15% |
| Segmentos RFM | 11 segmentos, incluyendo `champions`, `loyal_customers`, `at_risk` y `hibernating` |

## Narrativa del dashboard
1. Panorama: existe recompra relevante, pero el valor no esta distribuido de forma homogenea.
2. Cohortes: la retencion cae con rapidez en los primeros meses y cambia segun cohorte y contexto geografico.
3. Segmentacion: `champions` y grupos de alto valor deben protegerse; `hibernating` y `at_risk` requieren estrategias de reactivacion.
