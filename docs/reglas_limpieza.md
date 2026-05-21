# Reglas de limpieza para la fase 2

## Objetivo
Este documento resume las reglas de limpieza que ya quedaron adoptadas tras la auditoria inicial y separa los puntos cerrados de los que siguen pendientes.

## Nota de nomenclatura
En la definicion canonica del dataset aparecen variables como `InvoiceNo`, `UnitPrice` y `CustomerID`. En el archivo real utilizado en este proyecto esas columnas aparecen como `Invoice`, `Price` y `Customer ID`.

En esta documentacion se usa la definicion canonica cuando se habla de negocio y la equivalencia real cuando hace falta para implementar.

## Reglas adoptadas

| Tema | Regla adoptada | Aplicacion |
| --- | --- | --- |
| `CustomerID` faltante (`Customer ID`) | Se conserva en la base general, pero se excluye de cualquier dataset analitico a nivel cliente. | Retencion, cohortes y RFM se calculan solo sobre clientes identificables. |
| Cancelaciones en `InvoiceNo` (`Invoice`) | Si la factura comienza con `C`, la linea se clasifica como cancelacion. | No forma parte de compras validas. |
| `Quantity` negativa | Toda cantidad negativa se trata como linea no valida para compras, incluso sin prefijo `C`. | Se excluye de compras validas y metricas monetarias. |
| `UnitPrice <= 0` (`Price <= 0`) | Se trata como linea no valida para analisis monetario y compra valida. | Se excluye de ingresos, ticket y RFM. |
| Duplicados exactos | Se eliminan al construir la capa `processed`. | Evita inflar volumen y metricas. |
| Alcance geografico | La base general y la base analitica v1 conservan todos los paises. | Cohortes, retencion y RFM se construyen sobre el conjunto multicountry y pueden segmentarse por pais. |
| Moneda | No se aplica conversion de tipo de cambio. | `unit_price_gbp` se mantiene como precio en GBP para todos los paises. |

## Definicion de compra valida
En la fase 2, una compra valida se define por el cumplimiento simultaneo de los siguientes criterios:

1. `customer_id` no nulo.
2. `invoice_no` sin prefijo `C`.
3. `quantity > 0`.
4. `unit_price_gbp > 0`.

## Criterios cerrados para habilitar RFM
- La fuente unica para RFM es `transacciones__compras_validas__v1.parquet`.
- La `frequency` de RFM se mide por orden unica y no por linea.
- La fecha de corte para RFM corresponde a la ultima fecha observada del dataset en cada corrida reproducible.

## Reglas todavia pendientes

| Tema | Estado actual | Criterio pendiente |
| --- | --- | --- |
| `StockCode` especiales | Pendiente | Revisar codigos no comerciales o administrativos en una iteracion posterior de calidad analitica. |
| `Description` faltante | Pendiente | Determinar si puede recuperarse desde `StockCode` o si conviene excluir. |
| Devoluciones vs cancelaciones | Parcialmente resuelto | Aun puede requerirse una clasificacion mas fina en una iteracion posterior. |

## Criterios metodologicos de limpieza
- La capa `raw` se conserva como referencia original del dataset, sin intervenciones directas sobre los archivos fuente.
- La transicion entre `interim` y `processed` mantiene trazabilidad suficiente para explicar como evoluciona la base a lo largo del pipeline.
- Cada filtro relevante se documenta con su impacto en volumen para hacer visible el efecto de las decisiones de limpieza.
- La limpieza tecnica se distingue de las decisiones de negocio para evitar mezclar problemas de calidad con criterios analiticos.
- Estas reglas se materializan en scripts reproducibles dentro de `src/`, de modo que el proceso pueda repetirse y auditarse.

## Referencia
La justificacion detallada de estas decisiones esta en [docs/decisiones_fase_2.md](decisiones_fase_2.md).
