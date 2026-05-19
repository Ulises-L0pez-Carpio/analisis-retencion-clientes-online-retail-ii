# Analisis de retencion de clientes, cohortes y segmentacion RFM

Caso de estudio de portafolio construido con Python, SQL y Power BI sobre el dataset `Online Retail II`.

## Resumen ejecutivo
Este proyecto responde una pregunta central de negocio: como medir recurrencia, retencion y valor de cliente en un ecommerce transaccional con datos historicos reales.

La solucion se construyo como un flujo reproducible end-to-end:

- ingesta y estandarizacion del dataset original;
- limpieza analitica con reglas de negocio explicitas;
- construccion de datasets procesados para analisis;
- analisis de cohortes y segmentacion RFM;
- traduccion de hallazgos a un dashboard ejecutivo en Power BI.

## Problema de negocio
Una tienda online puede tener buen volumen de ventas y aun asi perder clientes con rapidez o concentrar demasiado valor en pocos compradores. Este proyecto busca identificar:

- que proporcion de clientes vuelve a comprar;
- como evolucionan las cohortes de clientes en el tiempo;
- que paises muestran mejor recurrencia relativa;
- que segmentos concentran mayor valor;
- que grupos combinan alto valor historico con riesgo de abandono.

## Stack y entregables
- `Python`: pipeline reproducible de ingesta, limpieza y modelado analitico.
- `SQL`: consultas cortas para validar y explicar metricas clave.
- `Power BI`: dashboard final para comunicar hallazgos a negocio.
- `Jupyter`: exploracion, validacion y analisis intermedio.
- `Markdown`: documentacion metodologica y narrativa de portafolio.

## Resultado del proyecto
### Volumen procesado
| Indicador | Valor |
| --- | ---: |
| Filas en ingesta inicial | 1,067,371 |
| Duplicados exactos removidos | 12,133 |
| Filas en base general | 1,055,238 |
| Filas en compras validas | 793,609 |
| Clientes unicos | 5,878 |
| Paises con compras validas | 41 |

### KPIs principales
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

### Segmentos RFM mas relevantes
| Segmento | Clientes |
| --- | ---: |
| `hibernating` | 2,372 |
| `champions` | 1,270 |
| `at_risk` | 992 |
| `potential_loyalists` | 662 |
| `loyal_customers` | 582 |

## Principales hallazgos
- La recompra existe, pero convive con una base amplia de clientes inactivos; la retencion no se debe leer solo con un KPI agregado.
- El segmento `champions` concentra una parte desproporcionada del valor historico, por lo que retener clientes de alto valor importa mas que aumentar volumen sin foco.
- Cohortes y RFM responden preguntas complementarias: cohortes explica persistencia en el tiempo y RFM explica calidad comercial de la base.

## Que hace defendible este caso de estudio
- Tiene una separacion clara entre `raw`, `interim` y `processed`.
- Explicita reglas de limpieza y definiciones de negocio.
- Deja artefactos reproducibles en `src/` y pruebas automatizadas en `tests/`.
- Conecta analisis exploratorio, modelado analitico y capa de presentacion ejecutiva.
- Permite hablar tanto de decisiones tecnicas como de lectura de negocio en entrevista.

## Navegacion rapida para reclutadores
- Caso de estudio corto: [reports/caso_estudio_portafolio.md](/C:/Users/genes/Desktop/Ciencia%20de%20datos/analisis-retencion-clientes-online-retail-ii/reports/caso_estudio_portafolio.md)
- Resumen ejecutivo: [reports/resumen_ejecutivo_portafolio.md](/C:/Users/genes/Desktop/Ciencia%20de%20datos/analisis-retencion-clientes-online-retail-ii/reports/resumen_ejecutivo_portafolio.md)
- Dashboard y narrativa visual: [dashboard/README.md](/C:/Users/genes/Desktop/Ciencia%20de%20datos/analisis-retencion-clientes-online-retail-ii/dashboard/README.md)
- Metodologia RFM: [docs/metodologia_rfm.md](/C:/Users/genes/Desktop/Ciencia%20de%20datos/analisis-retencion-clientes-online-retail-ii/docs/metodologia_rfm.md)
- Reglas de limpieza: [docs/reglas_limpieza.md](/C:/Users/genes/Desktop/Ciencia%20de%20datos/analisis-retencion-clientes-online-retail-ii/docs/reglas_limpieza.md)
- Flujo de datos: [docs/flujo_datos.md](/C:/Users/genes/Desktop/Ciencia%20de%20datos/analisis-retencion-clientes-online-retail-ii/docs/flujo_datos.md)

## Estado del proyecto
- Fase 1 cerrada: estructura base, ingesta inicial, auditoria y documentacion inicial.
- Fase 2 cerrada: limpieza reproducible y estandarizacion de la capa `processed`.
- Fase 3 cerrada: segmentacion RFM reproducible, cohortes, y dashboard Power BI completo.

## Estructura del repositorio
```text
analisis-retencion-clientes-online-retail-ii/
|-- data/
|   |-- raw/
|   |-- interim/
|   `-- processed/
|-- dashboard/
|-- docs/
|-- notebooks/
|-- reports/
|-- sql/
|-- src/
|-- tests/
|-- README.md
`-- requirements.txt
```

## Componentes tecnicos
### Pipeline en `src/`
- `src/ingest.py`: ingesta inicial desde Excel.
- `src/process_transactions.py`: base general y compras validas.
- `src/process_customers.py`: base analitica de clientes.
- `src/process_cohorts.py`: base de cohortes mensual.
- `src/process_rfm.py`: segmentacion RFM reproducible.

### Notebooks
- `notebooks/01_auditoria_datos.ipynb`
- `notebooks/02_matriz_retencion_cohortes.ipynb`
- `notebooks/03_hallazgos_retencion.ipynb`
- `notebooks/04_analisis_rfm.ipynb`

### SQL y dashboard
- `sql/`: consultas de apoyo para metricas y validaciones.
- `dashboard/`: archivo `.pbix` y documentacion del tablero final.

## Pruebas
El proyecto incluye pruebas unitarias para transacciones, clientes, cohortes y RFM.

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

## Como regenerar el pipeline
```powershell
python -m src.ingest
python -m src.process_transactions
python -m src.process_customers
python -m src.process_cohorts
python -m src.process_rfm
python -m unittest discover -s tests -p "test_*.py"
```

## Fuente de datos
`Online Retail II`, UCI Machine Learning Repository.
