# Flujo de datos del proyecto

## Objetivo
Este documento explica como se mueve el dataset dentro del proyecto y que representa cada capa de datos.

## Flujo definido
El flujo de datos del proyecto queda organizado asi:

1. `data/raw/`
2. `data/interim/`
3. `data/processed/`

## Que va en cada carpeta

### `data/raw/`
Aqui vive el archivo original descargado del dataset `Online Retail II`.

Reglas:

- no debe modificarse manualmente;
- funciona como fuente de verdad del proyecto;
- cualquier proceso reproducible debe partir desde aqui.

Archivo actual detectado:

- `online_retail_II.xlsx`

### `data/interim/`
Aqui se guardan copias de trabajo generadas por scripts reproducibles, antes de la limpieza final.

Archivo actual generado:

- `online_retail_ii_ingesta_inicial.csv`

Este archivo fue creado por [src/ingest.py](</C:/Users/genes/Desktop/Ciencia de datos/analisis-retencion-clientes-online-retail-ii/src/ingest.py>) y representa la salida inicial de la ingesta.

#### Que contiene exactamente `online_retail_ii_ingesta_inicial.csv`

Contenido:

- union de las dos hojas del Excel original en un solo dataset;
- nombres de columnas originales conservados;
- columna `InvoiceDate` convertida a formato fecha;
- columna `origen_hoja` para identificar de que hoja vino cada fila;
- columna `archivo_origen` para registrar el archivo fuente utilizado.

Columnas presentes:

- `Invoice`
- `StockCode`
- `Description`
- `Quantity`
- `InvoiceDate`
- `Price`
- `Customer ID`
- `Country`
- `origen_hoja`
- `archivo_origen`

#### Que no hace todavia esta salida
El archivo intermedio no aplica limpieza analitica final. Todavia no:

- elimina filas con `Customer ID` faltante;
- excluye cancelaciones;
- corrige cantidades negativas;
- trata precios no positivos;
- resuelve duplicados;
- genera variables de cohortes o RFM.

#### Resumen de la corrida actual
Con el archivo actual en `data/raw/`, la ingesta produjo:

- archivo fuente: `online_retail_II.xlsx`;
- hojas leidas: `Year 2009-2010` y `Year 2010-2011`;
- filas: `1,067,371`;
- columnas: `10`;
- rango de fechas: `2009-12-01 07:45:00` a `2011-12-09 12:50:00`.

### `data/processed/`
Aqui viviran los datasets limpios, estandarizados y listos para analisis, SQL y dashboard.

Reglas de esta capa:

- el formato por defecto sera `parquet`;
- los nombres de archivo estaran en espanol, en `snake_case`, con version explicita;
- los nombres de columnas estaran en ingles tecnico, en `snake_case`, usando la nomenclatura canonica del dataset;
- cualquier renombrado formal debe ocurrir aqui, no en `raw` ni en `interim`.

Ejemplos esperados:

- `transacciones__lineas_limpias__v1.parquet`
- `clientes__base_analitica__v1.parquet`
- `cohortes__retencion_mensual__v1.parquet`

La convencion completa esta documentada en [docs/convencion_processed.md](</C:/Users/genes/Desktop/Ciencia de datos/analisis-retencion-clientes-online-retail-ii/docs/convencion_processed.md>).

## Como regenerar la capa intermedia
Desde la raiz del proyecto:

```powershell
python -m src.ingest
```

Si hubiera mas de un Excel en `data/raw/`, se puede indicar uno de forma explicita:

```powershell
python -m src.ingest --input "data/raw/online_retail_II.xlsx"
```

## Rol de cada capa
- `raw`: preserva el dato original sin intervenirlo.
- `interim`: acelera auditoria y preparacion inicial sin tocar la fuente.
- `processed`: concentra la estandarizacion analitica para consumo de notebooks, SQL y dashboard.
