# Resumen ejecutivo del proyecto

## Contexto
Proyecto de portafolio enfocado en retencion de clientes, cohortes y segmentacion RFM sobre el dataset `Online Retail II`.

La base analitica se construye con un pipeline reproducible en Python y deja artefactos listos para notebook, SQL y dashboard.

## Volumen de la corrida actual
| Indicador | Valor |
| --- | ---: |
| Filas en ingesta inicial | 1,067,371 |
| Duplicados exactos removidos | 12,133 |
| Filas en base general | 1,055,238 |
| Filas en compras validas | 793,609 |
| Clientes unicos en compras validas | 5,878 |
| Paises con compras validas | 41 |

## KPIs principales
| KPI | Valor |
| --- | ---: |
| Clientes totales | 5,878 |
| Repeat rate | 72.39% |
| Revenue total | GBP 17,685,460.64 |
| Ticket promedio por orden | GBP 478.39 |
| Retencion M1 | 23.15% |
| Retencion M3 | 24.51% |
| Retencion M6 | 21.78% |
| Retencion M12 | 22.34% |

## Lectura RFM
| Segmento | Clientes | Participacion |
| --- | ---: | ---: |
| `hibernating` | 2,372 | 40.35% |
| `champions` | 1,270 | 21.61% |
| `at_risk` | 992 | 16.88% |
| `potential_loyalists` | 662 | 11.26% |
| `loyal_customers` | 582 | 9.90% |

## Insight de negocio
- La base tiene una proporcion alta de clientes recurrentes, pero tambien un bloque importante de clientes dormidos (`hibernating`), lo que sugiere que recurrencia y reactivacion deben leerse juntas.
- El segmento `champions` concentra una parte desproporcionada del valor monetario acumulado.
- La combinacion de cohortes y RFM permite separar dos preguntas diferentes: quien vuelve y cuanto valor aporta cuando vuelve.

## Activos del repositorio
- Notebook de cohortes: [notebooks/02_matriz_retencion_cohortes.ipynb](../notebooks/02_matriz_retencion_cohortes.ipynb)
- Notebook de hallazgos: [notebooks/03_hallazgos_retencion.ipynb](../notebooks/03_hallazgos_retencion.ipynb)
- Notebook RFM: [notebooks/04_analisis_rfm.ipynb](../notebooks/04_analisis_rfm.ipynb)
- Metodologia RFM: [docs/metodologia_rfm.md](../docs/metodologia_rfm.md)
