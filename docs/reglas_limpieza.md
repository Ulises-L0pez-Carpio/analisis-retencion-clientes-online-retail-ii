# Reglas de limpieza para la fase 2

## Objetivo
Este documento resume las reglas de limpieza que ya quedaron adoptadas tras la auditoria inicial y separa los puntos cerrados de los que siguen pendientes.

## Nota de nomenclatura
En la definicion canonica del dataset aparecen variables como `InvoiceNo`, `UnitPrice` y `CustomerID`. En el archivo real cargado en este proyecto esas columnas aparecen como `Invoice`, `Price` y `Customer ID`.

En esta documentacion se usa la definicion canonica cuando se habla de negocio y la equivalencia real cuando hace falta para implementar.

## Reglas adoptadas

| Tema | Regla adoptada | Aplicacion |
| --- | --- | --- |
| `CustomerID` faltante (`Customer ID`) | Se conserva en la base general, pero se excluye de cualquier dataset analitico a nivel cliente. | Retencion, cohortes y RFM trabajaran solo con clientes identificables. |
| Cancelaciones en `InvoiceNo` (`Invoice`) | Si la factura comienza con `C`, la linea se clasifica como cancelacion. | No forma parte de compras validas. |
| `Quantity` negativa | Toda cantidad negativa se trata como linea no valida para compras, incluso sin prefijo `C`. | Se excluye de compras validas y metricas monetarias. |
| `UnitPrice <= 0` (`Price <= 0`) | Se trata como linea no valida para analisis monetario y compra valida. | Se excluye de ingresos, ticket y RFM. |
| Duplicados exactos | Se eliminaran al construir la capa `processed`. | Evita inflar volumen y metricas. |
| Alcance geografico | La base general y la base analitica v1 conservaran todos los paises. | Cohortes, retencion y RFM se construiran sobre el conjunto multicountry y podran segmentarse por pais. |
| Moneda | No se aplicara conversion de tipo de cambio. | `unit_price_gbp` se mantiene como precio en GBP para todos los paises. |

## Regla operativa de compra valida
Para fase 2, una compra valida debe cumplir todo lo siguiente:

1. `customer_id` no nulo.
2. `invoice_no` sin prefijo `C`.
3. `quantity > 0`.
4. `unit_price_gbp > 0`.

## Reglas cerradas para habilitar RFM
- La fuente unica para RFM sera `transacciones__compras_validas__v1.parquet`.
- La `frequency` de RFM se medira por orden unica y no por linea.
- La fecha de corte para RFM sera la ultima fecha observada del dataset en cada corrida reproducible.

## Reglas todavia pendientes

| Tema | Estado actual | Criterio pendiente |
| --- | --- | --- |
| `StockCode` especiales | Pendiente | Revisar codigos no comerciales o administrativos en una iteracion posterior de calidad analitica. |
| `Description` faltante | Pendiente | Determinar si puede recuperarse desde `StockCode` o si conviene excluir. |
| Devoluciones vs cancelaciones | Parcialmente resuelto | Aun puede requerirse una clasificacion mas fina en una iteracion posterior. |

## Principios de implementacion
- No modificar directamente archivos en `data/raw/`.
- Mantener trazabilidad entre la capa `interim` y la capa `processed`.
- Registrar cuantas filas entran y cuantas salen por cada filtro.
- Separar limpieza tecnica de decisiones de negocio.
- Implementar estas reglas en scripts reproducibles dentro de `src/`.

## Referencia
La justificacion detallada de estas decisiones esta en [docs/decisiones_fase_2.md](</C:/Users/genes/Desktop/Ciencia de datos/analisis-retencion-clientes-online-retail-ii/docs/decisiones_fase_2.md>).
