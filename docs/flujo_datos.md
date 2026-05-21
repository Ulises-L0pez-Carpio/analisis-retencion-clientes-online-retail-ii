# Flujo de datos del proyecto

## Proposito
Este documento describe como evoluciona el dataset dentro del proyecto, desde el archivo fuente original hasta las salidas analiticas utilizadas en notebooks, validaciones y visualizacion ejecutiva.

## Estructura general
El flujo de datos se organiza en tres capas consecutivas:

1. `data/raw/`
2. `data/interim/`
3. `data/processed/`

Esta separacion permite distinguir con claridad entre la fuente original, la salida de ingesta y la capa analitica final.

## Descripcion de las capas

### `data/raw/`
La carpeta `raw` conserva el archivo original del dataset `Online Retail II` y funciona como referencia base del proyecto.

En esta capa no se realizan modificaciones manuales. Su valor metodologico consiste en preservar la fuente tal como fue obtenida, de modo que cualquier transformacion posterior pueda rastrearse desde un punto de partida estable.

Archivo fuente actual:

- `online_retail_II.xlsx`

### `data/interim/`
La capa `interim` contiene la primera salida reproducible del proceso de ingesta. Su objetivo es consolidar el archivo original en una base de trabajo que facilite la auditoria inicial y prepare el terreno para la limpieza analitica.

Archivo intermedio actual:

- `online_retail_ii_ingesta_inicial.csv`

Este archivo es generado por [src/ingest.py](../src/ingest.py) y representa una consolidacion inicial del Excel original.

#### Contenido de `online_retail_ii_ingesta_inicial.csv`
La salida intermedia conserva la estructura original del dataset y agrega trazabilidad minima para identificar el origen de cada registro. En concreto:

- integra en una sola tabla las dos hojas del archivo Excel original;
- conserva los nombres de columnas observados en la fuente;
- convierte `InvoiceDate` a formato fecha;
- agrega `origen_hoja` para identificar de que hoja proviene cada fila;
- agrega `archivo_origen` para registrar el archivo de entrada utilizado.

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

#### Alcance de esta salida
La capa `interim` no debe interpretarse como una base analitica final. Todavia no incorpora decisiones de limpieza ni transformaciones orientadas al analisis de negocio. Por ello, en este punto el dataset aun:

- conserva filas con `Customer ID` faltante;
- incluye cancelaciones;
- mantiene cantidades negativas o no validas;
- conserva precios no positivos;
- no resuelve duplicados de negocio;
- no genera variables derivadas para cohortes o RFM.

#### Resumen de la corrida actual
Con el archivo fuente actualmente disponible en `data/raw/`, la ingesta produjo la siguiente salida:

- archivo fuente: `online_retail_II.xlsx`;
- hojas leidas: `Year 2009-2010` y `Year 2010-2011`;
- filas: `1,067,371`;
- columnas: `10`;
- rango de fechas: `2009-12-01 07:45:00` a `2011-12-09 12:50:00`.

### `data/processed/`
La capa `processed` concentra los datasets limpios, estandarizados y listos para el analisis del caso. Desde aqui se alimentan notebooks, validaciones y la capa visual del proyecto.

Esta capa adopta una convencion formal para asegurar consistencia tecnica y legibilidad de portafolio:

- formato preferente en `parquet`;
- nombres de archivo en español, `snake_case` y con version explicita;
- columnas en ingles tecnico, `snake_case`, alineadas con la nomenclatura canonica del dataset;
- formalizacion de renombres y estandarizacion dentro de esta capa, no en `raw` ni en `interim`.

Ejemplos de salidas analiticas esperadas:

- `transacciones__lineas_limpias__v1.parquet`
- `clientes__base_analitica__v1.parquet`
- `cohortes__retencion_mensual__v1.parquet`

La convencion completa se documenta en [docs/convencion_processed.md](convencion_processed.md).

## Regeneracion de la capa intermedia
Desde la raiz del proyecto, la ingesta puede reconstruirse con:

```powershell
python -m src.ingest
```

Si fuera necesario indicar explicitamente el archivo fuente, se puede usar:

```powershell
python -m src.ingest --input "data/raw/online_retail_II.xlsx"
```

## Lectura metodologica del flujo
- `raw` preserva el origen del dato.
- `interim` consolida y prepara la auditoria inicial.
- `processed` materializa la capa analitica utilizada para responder las preguntas del caso.
