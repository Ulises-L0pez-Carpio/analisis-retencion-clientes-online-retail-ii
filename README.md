# Analisis de retencion de clientes, cohortes y segmentacion RFM

Proyecto de portafolio end-to-end con Python, SQL y Power BI usando el dataset `Online Retail II`.

## Problema de negocio
El objetivo es entender como compran y vuelven a comprar los clientes en un ecommerce multicountry.

El proyecto busca responder preguntas como:

- que proporcion de clientes vuelve a comprar;
- como cambian las cohortes con el tiempo;
- que paises muestran mejor recurrencia relativa;
- que clientes concentran mas valor;
- que grupos combinan alto riesgo de abandono con alto valor historico.

## Dataset
Fuente: `Online Retail II` de UCI Machine Learning Repository.

Caracteristicas relevantes:

- datos transaccionales entre diciembre de 2009 y diciembre de 2011;
- variables de factura, producto, cantidad, fecha, precio, cliente y pais;
- moneda original en libras esterlinas;
- estructura adecuada para retencion, cohortes y RFM.

## Estado del proyecto
- Fase 1 cerrada: estructura base, ingesta inicial, auditoria y documentacion inicial.
- Fase 2 cerrada: limpieza reproducible y estandarizacion de la capa `processed`.
- Fase 3 iniciada: segmentacion RFM reproducible y narrativa para dashboard.

## Pipeline de datos
El flujo del proyecto sigue tres capas:

1. `data/raw/`
2. `data/interim/`
3. `data/processed/`

Reglas clave:

- `raw` no se modifica manualmente;
- `interim` conserva una copia de trabajo reproducible;
- `processed` concentra datasets limpios, versionados y listos para analisis.

## Reglas de negocio adoptadas
La definicion operativa de compra valida es:

1. `customer_id` no nulo.
2. `invoice_no` sin prefijo `C`.
3. `quantity > 0`.
4. `unit_price_gbp > 0`.

Ademas:

- se conservan todos los paises;
- se eliminan duplicados exactos en `processed`;
- la moneda se mantiene en GBP;
- la `frequency` de RFM se mide por orden unica, no por linea.

Mas detalle en:

- [docs/reglas_limpieza.md](docs/reglas_limpieza.md)
- [docs/decisiones_fase_2.md](docs/decisiones_fase_2.md)
- [docs/metodologia_rfm.md](docs/metodologia_rfm.md)

## Artefactos procesados actuales
### `transacciones__base_general__v1.parquet`
Base maestra de transacciones procesadas con normalizacion, tipos, deduplicacion y banderas de calidad.

### `transacciones__compras_validas__v1.parquet`
Subconjunto de compras validas que alimenta cohortes, clientes y RFM.

### `clientes__base_analitica__v1.parquet`
Base a nivel cliente con recencia, recurrencia, revenue y pais principal.

### `cohortes__retencion_mensual__v1.parquet`
Base de cohortes mensual con retencion y metricas operativas por cohorte.

### `rfm__segmentacion_clientes__v1.parquet`
Segmentacion RFM reproducible con `recency_days`, `frequency_orders`, `monetary_gbp`, scores `R/F/M` y segmento final.

## Resultados de la corrida actual
### Volumen del pipeline
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

### Distribucion RFM
| Segmento | Clientes |
| --- | ---: |
| `hibernating` | 2,372 |
| `champions` | 1,270 |
| `at_risk` | 992 |
| `potential_loyalists` | 662 |
| `loyal_customers` | 582 |

## Lectura ejecutiva
- La recurrencia existe, pero convive con un bloque grande de clientes dormidos, lo que vuelve importante la lectura de reactivacion.
- `champions` concentra una fraccion desproporcionada del valor historico, por lo que no basta con mirar solo repeat rate.
- Cohortes y RFM responden preguntas complementarias: quien vuelve a comprar y cuanto valor aporta cuando vuelve.

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
|-- AGENTS.md
|-- README.md
`-- requirements.txt
```

## Scripts en `src/`
- `src/ingest.py`: ingesta inicial desde Excel.
- `src/process_transactions.py`: base general y compras validas.
- `src/process_customers.py`: base analitica de clientes.
- `src/process_cohorts.py`: base de cohortes mensual.
- `src/process_rfm.py`: segmentacion RFM reproducible.

## Notebooks
- `notebooks/01_auditoria_datos.ipynb`
- `notebooks/02_matriz_retencion_cohortes.ipynb`
- `notebooks/03_hallazgos_retencion.ipynb`
- `notebooks/04_analisis_rfm.ipynb`

## SQL y dashboard
- En `sql/` quedan consultas cortas para reproducir metricas clave del proyecto.
- En `dashboard/` queda la especificacion completa del tablero y un mockup visual para Power BI.
- El archivo `.pbix` no se genero desde este entorno porque Power BI Desktop no esta disponible aqui.

## Pruebas
El proyecto incluye pruebas unitarias para transacciones, clientes, cohortes y RFM.

Comando:

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

## Como regenerar el pipeline
1. Ejecutar la ingesta inicial:

```powershell
python -m src.ingest
```

2. Generar transacciones procesadas:

```powershell
python -m src.process_transactions
```

3. Generar base de clientes:

```powershell
python -m src.process_customers
```

4. Generar cohortes:

```powershell
python -m src.process_cohorts
```

5. Generar RFM:

```powershell
python -m src.process_rfm
```

6. Ejecutar pruebas:

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

## Entregables para reclutadores
- pipeline reproducible en `src/`;
- documentacion de decisiones y supuestos;
- notebooks de exploracion y hallazgos;
- resumen ejecutivo en `reports/`;
- consultas SQL orientadas a entrevista;
- paquete de definicion visual para Power BI en `dashboard/`.
