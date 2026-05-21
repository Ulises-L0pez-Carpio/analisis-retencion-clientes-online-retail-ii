# Diccionario de datos inicial

## Objetivo
Este documento resume la definicion oficial de las variables principales del dataset `Online Retail II` y aclara como aparecen nombradas en el archivo real usado en este proyecto.

## Definicion canonica de variables
La documentacion del dataset describe las variables asi:

| Variable canonica | Tipo | Descripcion |
| --- | --- | --- |
| `InvoiceNo` | nominal | Numero de factura. Entero de 6 digitos asignado de forma unica a cada transaccion. Si inicia con `C`, indica cancelacion. |
| `StockCode` | nominal | Codigo de producto. Numero de 5 digitos asignado a cada producto distinto. |
| `Description` | nominal | Nombre o descripcion del producto. |
| `Quantity` | numerica | Cantidad de unidades por item dentro de la transaccion. |
| `InvoiceDate` | numerica / fecha-hora | Fecha y hora en que se genero la transaccion. |
| `UnitPrice` | numerica | Precio unitario del producto en libras esterlinas. |
| `CustomerID` | nominal | Numero de cliente. Identificador unico de 5 digitos por cliente. |
| `Country` | nominal | Pais de residencia del cliente. |

## Correspondencia con el archivo cargado en este proyecto
El Excel disponible en `data/raw/online_retail_II.xlsx` no usa exactamente todos los nombres canonicos. En esta fase preservamos los nombres originales del archivo y documentamos la equivalencia.

| Variable canonica | Nombre en el archivo actual | Nota |
| --- | --- | --- |
| `InvoiceNo` | `Invoice` | En el archivo real la factura aparece como `Invoice`. El prefijo `C` sigue indicando cancelacion. |
| `StockCode` | `StockCode` | Coincide con la definicion oficial. |
| `Description` | `Description` | Coincide con la definicion oficial. |
| `Quantity` | `Quantity` | Coincide con la definicion oficial. |
| `InvoiceDate` | `InvoiceDate` | Coincide con la definicion oficial. |
| `UnitPrice` | `Price` | En el archivo real el precio unitario aparece como `Price`. |
| `CustomerID` | `Customer ID` | En el archivo real aparece con espacio: `Customer ID`. |
| `Country` | `Country` | Coincide con la definicion oficial. |

## Variables agregadas en la ingesta inicial
El script [src/ingest.py](../src/ingest.py) agrega dos columnas para trazabilidad:

| Variable | Descripcion |
| --- | --- |
| `origen_hoja` | Hoja del Excel desde la que se leyo el registro. |
| `archivo_origen` | Nombre del archivo Excel utilizado en la ingesta. |

## Criterio adoptado en la fase 1
- Se preservan los nombres originales del archivo en `raw` e `interim`.
- En la documentacion y auditoria se explicita el mapeo hacia la nomenclatura canonica.
- Si en una fase posterior se decide normalizar nombres, ese cambio debe ocurrir en la capa procesada y quedar documentado.

## Notas
- Este diccionario es inicial y debe refinarse despues de revisar casos especiales de `StockCode`, valores faltantes y reglas de limpieza.
- La diferencia entre nombres canonicos y nombres observados en el archivo es importante para evitar confusiones en notebook, SQL y dashboard.
