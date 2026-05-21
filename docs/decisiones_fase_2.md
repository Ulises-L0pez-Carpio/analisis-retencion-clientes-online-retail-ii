# Decisiones adoptadas para la fase 2

## Proposito de la fase
La fase 2 tuvo como objetivo convertir la auditoria inicial del dataset en una capa de datos limpia, reproducible y util para analisis de negocio.

En esta etapa el trabajo ya no consistio solo en inspeccionar la fuente, sino en fijar criterios formales para distinguir entre:

- una base general con la mayor trazabilidad posible;
- una base analitica de compras validas, preparada para cohortes, retencion y RFM.

Esta separacion permitio conservar contexto del dato original y, al mismo tiempo, construir metricas sobre una definicion mas estricta de compra valida.

## Enfoque adoptado en la fase 2
La fase se resolvio mediante una limpieza reproducible orientada a tres metas:

- estandarizar la estructura de la informacion;
- documentar con claridad las reglas que afectan la lectura analitica;
- generar artefactos consistentes en `data/processed/` para las fases siguientes.

El criterio general fue no mezclar limpieza tecnica con interpretaciones de negocio sin antes dejar explicita la regla utilizada.

## Decisiones principales

| Tema | Decision adoptada | Justificacion | Impacto esperado |
| --- | --- | --- | --- |
| `CustomerID` faltante (`Customer ID`) | Se conserva en una base general, pero se excluye de la base analitica a nivel cliente. | Sin identificador no es posible medir retencion, recurrencia ni RFM por cliente. | Las metricas customer-level se calculan solo sobre clientes identificables. |
| Cancelaciones en `InvoiceNo` (`Invoice`) | Toda factura cuyo identificador empieza con `C` se clasifica como cancelacion. | La documentacion oficial del dataset lo define de esa manera. | Estas filas no participan como compras validas. |
| `Quantity` negativa | Se trata como linea no valida para compras, aun cuando no tenga prefijo `C`. | En la auditoria aparecieron lineas negativas fuera de facturas `C`, por lo que hacia falta una regla adicional. | Se excluyen de ingresos, cohortes y RFM. |
| Duplicados exactos | Se eliminan en `processed` despues de documentar su volumen. | Su permanencia inflaria ventas, cantidades y eventos observados. | La base procesada evita duplicacion tecnica de metricas. |
| `UnitPrice <= 0` (`Price <= 0`) | Se excluye de la base de compras validas y de las metricas monetarias. | No representa una compra estandar util para medir valor o recurrencia comercial. | Evita distorsiones en ingresos, ticket promedio y scoring RFM. |
| Alcance geografico | La base general y la base analitica v1 conservan todos los paises. | El caso se plantea como un ecommerce multicountry y `country` debe mantenerse como dimension analitica. | Cohortes, retencion y RFM pueden leerse en total y por pais. |
| Tratamiento de moneda | No se aplica conversion de tipo de cambio; el precio se conserva en libras esterlinas. | La documentacion del dataset indica que `UnitPrice` esta expresado en sterling y en esta fase se priorizo consistencia metodologica. | Las metricas monetarias se reportan en GBP para todo el proyecto. |

## Definicion de compra valida en esta fase
Para los analisis customer-level, una linea se considera compra valida solo si cumple simultaneamente:

1. `customer_id` no es nulo.
2. `invoice_no` no empieza con `C`.
3. `quantity > 0`.
4. `unit_price_gbp > 0`.

Esta definicion fue la base para separar la capa transaccional general de la capa analitica utilizada en cohortes, retencion y RFM.

## Artefactos que surgieron de la fase

### Base general limpia
Esta salida conserva el mayor contexto posible despues de la limpieza tecnica minima.

Su papel dentro del proyecto es servir como base trazable y estandarizada, sin descartar automaticamente todos los casos problematicos de negocio.

Elementos clave de esta capa:

- elimina duplicados exactos;
- normaliza nombres de columnas segun la convencion de `processed`;
- conserva todos los paises;
- mantiene filas con problemas de negocio, pero las deja identificables.

Artefacto representativo:

- `transacciones__base_general__v1.parquet`

### Base analitica de compras validas
Esta salida funciona como fuente directa para cohortes, recurrencia y RFM.

Su papel dentro del proyecto es ofrecer una lectura analitica consistente del comportamiento de compra, ya libre de casos que distorsionarian la interpretacion de negocio.

Elementos clave de esta capa:

- parte de la base general limpia;
- filtra solo compras validas;
- conserva todos los paises;
- mantiene `country` como dimension explicita de analisis;
- conserva `unit_price_gbp` y las metricas monetarias en GBP;
- deja una fila por linea de compra valida.

Artefacto representativo:

- `transacciones__compras_validas__v1.parquet`

## Temas que quedaron abiertos
La fase 2 cerro la limpieza principal, pero dejo algunos temas reservados para iteraciones posteriores:

- tratamiento de `StockCode` especiales;
- estrategia final para `Description` faltante;
- definicion mas fina de devoluciones netas frente a cancelaciones.

## Cierre de la fase 2
La fase 2 se considera cerrada cuando la limpieza reproducible y la estandarizacion de `processed` ya permiten construir salidas analiticas utilizables por las fases posteriores.

Los artefactos que materializan ese cierre son:

- `transacciones__base_general__v1.parquet`
- `transacciones__compras_validas__v1.parquet`
- `clientes__base_analitica__v1.parquet`
- `cohortes__retencion_mensual__v1.parquet`

Con esta base cerrada, el proyecto quedo listo para pasar a la construccion de segmentacion RFM y a la capa de narrativa analitica del caso.
