# Decisiones adoptadas para la fase 2

## Objetivo
Este documento convierte los hallazgos de la auditoria inicial en decisiones operativas para la fase 2 del proyecto.

La meta es reducir ambiguedad antes de implementar la limpieza reproducible en `src/` y antes de generar los primeros datasets en `data/processed/`.

## Principio general
La fase 2 diferenciara entre:

- una base general limpia y estandarizada;
- una base analitica de compras validas para retencion, cohortes y RFM.

Esto permite no perder trazabilidad del dato y, al mismo tiempo, construir metricas de negocio sobre una definicion mas estricta de compra valida.

## Decisiones operativas

| Tema | Decision adoptada | Justificacion | Impacto esperado |
| --- | --- | --- | --- |
| `CustomerID` faltante (`Customer ID`) | Se conservara en una base general, pero se excluira de toda base analitica a nivel cliente. | Sin identificador no se puede medir retencion, recurrencia ni RFM por cliente. | Las metricas customer-level trabajaran solo con clientes identificables. |
| Cancelaciones en `InvoiceNo` (`Invoice`) | Toda factura cuyo identificador empiece con `C` se considerara cancelacion. | La documentacion oficial del dataset lo define explicitamente asi. | Estas filas no entraran como compras validas. |
| `Quantity` negativa | Se tratara como linea no valida para compras, aunque no tenga prefijo `C`. | En la auditoria hubo lineas negativas fuera de facturas `C`, por lo que conviene una regla adicional mas robusta. | Se excluiran de ingresos, cohortes y RFM. |
| Duplicados exactos | Se eliminaran en `processed` despues de documentar su volumen. | Duplican ventas, cantidades y eventos si se mantienen. | La base procesada no debe inflar metricas por duplicacion tecnica. |
| `UnitPrice <= 0` (`Price <= 0`) | Se excluira de la base de compras validas y de metricas monetarias. | No representa una compra estandar util para medir valor monetario ni recurrencia comercial. | Evita distorsion en revenue, ticket y scoring RFM. |
| Alcance geografico | La base general y la base analitica v1 conservaran todos los paises. | El alcance del proyecto es ecommerce multicountry y `country` debe mantenerse como dimension analitica. | Cohortes, retencion y RFM podran analizarse para todo el conjunto y segmentarse por pais. |
| Tratamiento de moneda | No se aplicara conversion de tipo de cambio; el precio se mantendra en libras esterlinas. | La documentacion del dataset indica que `UnitPrice` esta expresado en sterling y, para esta fase, priorizamos consistencia y reproducibilidad. | Las metricas monetarias se reportaran en GBP para todos los paises. |

## Definicion de compra valida para la fase 2
Una linea sera considerada compra valida para analisis customer-level solo si cumple simultaneamente:

1. `customer_id` no es nulo.
2. `invoice_no` no empieza con `C`.
3. `quantity > 0`.
4. `unit_price_gbp > 0`.

## Efecto sobre los datasets futuros

### Base general limpia
Este dataset preservara el mayor contexto posible despues de limpieza tecnica minima.

Reglas previstas:

- elimina duplicados exactos;
- normaliza nombres de columnas a la convencion de `processed`;
- conserva todos los paises;
- conserva filas con problemas de negocio, pero con banderas de calidad.

Ejemplo de artefacto:

- `transacciones__base_general__v1.parquet`

### Base analitica de compras validas
Este dataset sera la fuente para cohortes, recurrencia y RFM.

Reglas previstas:

- parte de la base general limpia;
- filtra solo compras validas;
- conserva todos los paises;
- mantiene `country` como dimension explicita de analisis;
- mantiene `unit_price_gbp` y metricas monetarias en GBP sin conversion de moneda;
- deja una fila por linea de compra valida.

Ejemplo de artefacto:

- `transacciones__compras_validas__v1.parquet`

## Decisiones que quedan abiertas para una iteracion posterior
Todavia no se cierran en este paso:

- tratamiento de `StockCode` especiales;
- estrategia final para `Description` faltante;
- definicion exacta de devoluciones netas frente a cancelaciones.

## Siguiente paso recomendado
Implementar un script de limpieza reproducible en `src/` que:

- lea la capa `interim`;
- aplique estas reglas;
- genere la primera base en `processed` con nombres normalizados;
- deje columnas bandera para trazabilidad de decisiones.

## Cierre de fase
La fase 2 queda cerrada con estos artefactos ya operativos:

- `transacciones__base_general__v1.parquet`
- `transacciones__compras_validas__v1.parquet`
- `clientes__base_analitica__v1.parquet`
- `cohortes__retencion_mensual__v1.parquet`

La siguiente fase se apoya sobre esta base cerrada para construir segmentacion RFM y su capa de storytelling.
