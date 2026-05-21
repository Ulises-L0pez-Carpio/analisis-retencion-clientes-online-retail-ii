# Metodologia RFM del proyecto

## Objetivo
Este documento fija la primera definicion operativa de la segmentacion RFM para el proyecto de retencion de clientes sobre `Online Retail II`.

La meta es complementar cohortes y recurrencia con una lectura de valor por cliente que sea:

- reproducible desde `src/`;
- simple de explicar en entrevista;
- suficientemente robusta para dashboard y storytelling.

## Fuente de datos
La capa RFM se construye exclusivamente desde:

- `data/processed/transacciones__compras_validas__v1.parquet`

Esto implica que la segmentacion ya hereda las reglas de limpieza cerradas en Fase 2:

1. `customer_id` no nulo;
2. `invoice_no` sin prefijo `C`;
3. `quantity > 0`;
4. `unit_price_gbp > 0`.

## Unidad de analisis
La segmentacion se calcula a nivel cliente.

La `frequency` se mide por numero de ordenes unicas (`invoice_no`) y no por numero de lineas.

## Fecha de corte
La foto RFM usa una fecha de corte fija derivada del dataset:

- `snapshot_datetime = max(invoice_datetime)`

En la corrida actual:

- `snapshot_datetime = 2011-12-09 12:50:00`
- `snapshot_date = 2011-12-09`

## Definiciones metricas
### `recency_days`
Dias transcurridos entre `snapshot_date` y la ultima compra observada del cliente.

Interpretacion:

- menor valor = cliente mas reciente;
- mayor valor = cliente mas alejado de su ultima compra.

### `frequency_orders`
Numero de ordenes unicas del cliente.

Interpretacion:

- mayor valor = cliente con mas recurrencia transaccional.

### `monetary_gbp`
Revenue total acumulado del cliente en libras esterlinas a partir de compras validas.

Interpretacion:

- mayor valor = cliente con mayor contribucion monetaria historica.

## Scoring
Cada metrica se transforma a un score de `1` a `5` usando quintiles calculados sobre percentiles del conjunto de clientes.

Reglas:

- `r_score`: score mas alto para clientes mas recientes;
- `f_score`: score mas alto para clientes con mas ordenes;
- `m_score`: score mas alto para clientes con mayor revenue.

Notas metodologicas:

- el scoring usa percentiles y no cortes manuales;
- los empates se manejan con ranking promedio para mantener estabilidad;
- si una distribucion tiene muchos empates, algunos buckets pueden concentrar mas clientes que otros, pero la regla sigue siendo reproducible y defendible.

## `rfm_score`
Concatenacion textual de `r_score`, `f_score` y `m_score`.

Ejemplo:

- `455` significa recencia alta, frecuencia muy alta y valor monetario muy alto.

## Segmentos operativos
La taxonomia v1 del proyecto prioriza legibilidad para portafolio.

| Segmento | Regla |
| --- | --- |
| `champions` | `r_score >= 4` y `f_score >= 4` y `m_score >= 4` |
| `loyal_customers` | `r_score >= 3` y `f_score >= 4` y `m_score >= 3` |
| `potential_loyalists` | `r_score >= 4` y `f_score >= 2` y `m_score >= 2` |
| `at_risk` | `r_score <= 2` y (`f_score >= 3` o `m_score >= 3`) |
| `hibernating` | cualquier cliente no clasificado en las reglas anteriores |

## Resultado actual de la corrida
Con la corrida actual del proyecto:

- clientes segmentados: `5,878`;
- `champions`: `1,270`;
- `loyal_customers`: `582`;
- `potential_loyalists`: `662`;
- `at_risk`: `992`;
- `hibernating`: `2,372`.

## Limitaciones actuales
- No se ajusta por pais ni por ventana temporal movil.
- No se normaliza `monetary_gbp` por inflacion ni por tipo de cambio.
- No se modelan devoluciones netas complejas fuera de la definicion de compra valida adoptada.
- La segmentacion es descriptiva; no es un modelo predictivo de churn.

## Artefactos relacionados
- [src/process_rfm.py](../src/process_rfm.py)
- [tests/test_process_rfm.py](../tests/test_process_rfm.py)
- [data/processed/README.md](../data/processed/README.md)
