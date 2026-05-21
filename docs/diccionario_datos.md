# Diccionario de datos del proyecto

## Proposito
Este documento resume las variables principales del dataset `Online Retail II` y explica como se interpretan dentro del proyecto, desde la fuente original hasta la capa analitica final.

Su funcion no es repetir toda la documentacion oficial del dataset, sino dejar clara la relacion entre:

- la nomenclatura canonica de origen;
- los nombres observados en el archivo realmente utilizado;
- y los nombres normalizados que alimentan la capa `processed`.

## Variables base del dataset
La estructura principal del caso se apoya en las siguientes variables originales:

| Variable canonica | Tipo | Descripcion |
| --- | --- | --- |
| `InvoiceNo` | nominal | Numero de factura o transaccion. Si inicia con `C`, indica cancelacion. |
| `StockCode` | nominal | Codigo de producto. |
| `Description` | nominal | Descripcion del producto. |
| `Quantity` | numerica | Cantidad de unidades por linea. |
| `InvoiceDate` | fecha-hora | Fecha y hora de la transaccion. |
| `UnitPrice` | numerica | Precio unitario en libras esterlinas. |
| `CustomerID` | nominal | Identificador unico del cliente. |
| `Country` | nominal | Pais de residencia del cliente. |

## Correspondencia con el archivo fuente del proyecto
El archivo `data/raw/online_retail_II.xlsx` no replica exactamente la nomenclatura canonica. Por eso, el proyecto documenta la equivalencia entre ambos esquemas antes de la normalizacion analitica.

| Variable canonica | Nombre en el archivo fuente | Lectura dentro del proyecto |
| --- | --- | --- |
| `InvoiceNo` | `Invoice` | Se interpreta como identificador de transaccion; el prefijo `C` sigue indicando cancelacion. |
| `StockCode` | `StockCode` | Se conserva sin cambio en la fuente. |
| `Description` | `Description` | Se conserva sin cambio en la fuente. |
| `Quantity` | `Quantity` | Se conserva sin cambio en la fuente. |
| `InvoiceDate` | `InvoiceDate` | Se conserva sin cambio en la fuente. |
| `UnitPrice` | `Price` | En el archivo fuente el precio aparece como `Price`. |
| `CustomerID` | `Customer ID` | Se conserva con espacio en la fuente original. |
| `Country` | `Country` | Se conserva sin cambio en la fuente. |

## Variables de trazabilidad agregadas en la ingesta
La salida de ingesta incorpora dos columnas adicionales para identificar el origen de cada registro:

| Variable en `interim` | Descripcion |
| --- | --- |
| `origen_hoja` | Hoja del Excel desde la que se leyó el registro. |
| `archivo_origen` | Archivo utilizado durante la ingesta. |

Estas columnas permiten rastrear la procedencia de los datos antes de la estandarizacion final.

## Nomenclatura analitica en `processed`
En la capa `processed`, las variables se normalizan a nombres tecnicos en ingles y en `snake_case`, de acuerdo con la convencion adoptada para el proyecto.

| Nombre en fuente o `interim` | Nombre en `processed` | Uso principal |
| --- | --- | --- |
| `Invoice` | `invoice_no` | Identificador de factura o transaccion. |
| `StockCode` | `stock_code` | Codigo de producto. |
| `Description` | `description` | Descripcion del producto. |
| `Quantity` | `quantity` | Cantidad por linea. |
| `InvoiceDate` | `invoice_datetime` | Fecha y hora de la transaccion. |
| `Price` | `unit_price_gbp` | Precio unitario en GBP. |
| `Customer ID` | `customer_id` | Identificador del cliente. |
| `Country` | `country` | Pais del cliente. |
| `origen_hoja` | `source_sheet` | Hoja de origen en el Excel. |
| `archivo_origen` | `source_file` | Archivo utilizado en la ingesta. |

## Variables derivadas mas relevantes
La fase final del proyecto no se limita a renombrar columnas. Tambien construye variables derivadas que hacen posible el analisis de recurrencia, cohortes y RFM.

Entre las mas importantes se encuentran:

| Variable derivada | Significado |
| --- | --- |
| `is_cancellation` | Marca lineas asociadas a cancelaciones. |
| `is_missing_customer_id` | Identifica filas sin cliente asignado. |
| `has_nonpositive_quantity` | Marca cantidades no validas para compra. |
| `has_nonpositive_unit_price` | Marca precios no validos para lectura monetaria. |
| `is_valid_purchase` | Resume la regla de compra valida adoptada en la fase 2. |
| `line_revenue_gbp` | Ingreso monetario por linea. |
| `invoice_month` | Mes de la transaccion, util para cohortes. |
| `first_purchase_month` | Primer mes de compra del cliente. |
| `cohort_month` | Cohorte asignada a partir de la primera compra. |
| `cohort_index` | Distancia en meses respecto a la cohorte inicial. |
| `recency_days` | Dias desde la ultima compra hasta la fecha de corte. |
| `frequency_orders` | Numero de ordenes unicas por cliente. |
| `monetary_gbp` | Valor monetario acumulado del cliente. |
| `rfm_score` | Combinacion de los componentes de recencia, frecuencia y valor. |
| `rfm_segment` | Segmento final asignado al cliente. |

## Lectura metodologica del diccionario
El diccionario acompaña la evolucion del proyecto en tres niveles:

- en `raw`, preserva la estructura original del archivo fuente;
- en `interim`, agrega trazabilidad sin alterar todavia la logica analitica;
- en `processed`, consolida la nomenclatura final que alimenta notebooks, pruebas, cohortes, RFM y dashboard.

## Estado del documento
Este diccionario refleja la fase final del proyecto y ya no debe leerse como una referencia provisional de auditoria inicial. Su papel actual es servir como puente entre la fuente original, la normalizacion tecnica y la capa analitica presentada en el portafolio.
