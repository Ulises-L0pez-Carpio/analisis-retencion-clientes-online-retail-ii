# Convencion para la capa `data/processed/`

## Proposito
Esta convencion define como se nombran los datasets y las columnas en la capa `data/processed/`, que es la capa analitica central del proyecto. Su objetivo es mantener consistencia tecnica, trazabilidad metodologica y legibilidad de portafolio.

La decision no busca solo ordenar archivos. Tambien permite que los artefactos finales puedan entenderse con rapidez, tanto desde una lectura tecnica como desde una revision de proyecto.

## Alcance de la convencion
La convencion aplica exclusivamente a `data/processed/`, donde se concentran los datasets limpios, estandarizados y listos para analisis.

No aplica a:

- `data/raw/`, porque preserva el archivo original tal como fue obtenido;
- `data/interim/`, porque conserva la salida de ingesta con una estructura cercana a la fuente.

## Criterio general adoptado
La capa `processed` combina dos decisiones complementarias:

- nombres de archivo en espanol, porque forman parte de los entregables visibles del proyecto;
- nombres de columnas en ingles tecnico, porque mantienen continuidad con Python, SQL, Power BI y la nomenclatura original del dataset.

Sobre esa base, toda la capa sigue una forma comun:

- texto en minusculas;
- uso de ASCII;
- formato `snake_case`;
- version explicita en cada archivo;
- `parquet` como formato preferente.

## Convencion para nombres de archivos

### Estructura base
Los archivos de `processed` siguen el patron:

```text
<dominio>__<contenido>__v<n>.parquet
```

Esta estructura permite identificar de inmediato tres cosas: el area analitica a la que pertenece el dataset, el contenido principal que resume y la version de su esquema.

### Criterios de nombre
En esta capa, los nombres de archivo:

- usan minusculas y caracteres ASCII;
- mantienen `snake_case`;
- separan bloques semanticos con doble guion bajo `__`;
- incluyen version explicita como `v1`, `v2` o `v3`;
- evitan etiquetas vagas como `final`, `nuevo`, `ok` o `limpio_final`.

### Dominios recomendados
Los dominios elegidos responden a las principales salidas del caso:

- `transacciones`
- `clientes`
- `cohortes`
- `rfm`
- `metricas`

### Ejemplos representativos
- `transacciones__lineas_limpias__v1.parquet`
- `clientes__base_analitica__v1.parquet`
- `cohortes__retencion_mensual__v1.parquet`
- `rfm__segmentacion_clientes__v1.parquet`
- `metricas__resumen_ecommerce__v1.parquet`

## Convencion para nombres de columnas

### Criterio base
Las columnas se nombran en ingles tecnico y en `snake_case`, alineadas con la nomenclatura canonica del dataset cuando eso aporta claridad.

Esta decision busca que la capa analitica sea coherente con el ecosistema donde se consume: scripts en Python, consultas SQL, medidas en Power BI y documentacion tecnica del proyecto.

### Criterios de escritura
Las columnas:

- usan minusculas;
- se mantienen en ASCII;
- no incluyen espacios;
- no usan acentos;
- evitan puntos y guiones;
- no mezclan espanol e ingles dentro del mismo nombre;
- priorizan nombres semanticos claros por encima de abreviaturas ambiguas.

### Mapeo base desde la salida de ingesta

| Nombre en `interim` | Nombre canonico en `processed` | Nota |
| --- | --- | --- |
| `Invoice` | `invoice_no` | Factura o transaccion; si inicia con `C`, indica cancelacion. |
| `StockCode` | `stock_code` | Codigo de producto. |
| `Description` | `description` | Descripcion del producto. |
| `Quantity` | `quantity` | Cantidad por linea. |
| `InvoiceDate` | `invoice_datetime` | Fecha y hora de la transaccion. |
| `Price` | `unit_price_gbp` | Precio unitario en libras esterlinas. |
| `Customer ID` | `customer_id` | Identificador del cliente. |
| `Country` | `country` | Pais del cliente. |
| `origen_hoja` | `source_sheet` | Hoja del Excel origen. |
| `archivo_origen` | `source_file` | Archivo origen usado en la ingesta. |

## Convencion para columnas derivadas
Las columnas calculadas siguen una logica de prefijos y sufijos que hace mas clara su interpretacion:

- booleanos con prefijo `is_` o `has_`;
- conteos con prefijo `n_`;
- fechas sin hora con sufijo `_date`;
- fechas con hora con sufijo `_datetime`;
- periodos mensuales con sufijo `_month`;
- importes monetarios con sufijo `_gbp`;
- tasas con sufijo `_rate`;
- participaciones con sufijo `_share`.

### Ejemplos de columnas derivadas
- `is_cancellation`
- `line_revenue_gbp`
- `invoice_month`
- `first_purchase_month`
- `months_since_first_purchase`
- `is_retained_next_30d`
- `rfm_segment`

## Granularidad esperada de cada dataset
Cada archivo en `processed` debe responder a una sola granularidad principal. Esta definicion evita ambiguedades al momento de analizar, unir o visualizar la informacion.

Ejemplos:

- `transacciones__lineas_limpias__v1.parquet`: una fila por linea de transaccion;
- `clientes__base_analitica__v1.parquet`: una fila por cliente;
- `cohortes__retencion_mensual__v1.parquet`: una fila por cohorte y periodo;
- `rfm__segmentacion_clientes__v1.parquet`: una fila por cliente puntuado.

## Criterio de versionado
La version de un archivo cambia cuando el esquema o su interpretacion analitica cambian de manera relevante. Esto incluye casos como:

- renombre de columnas;
- columnas agregadas o eliminadas;
- cambio de granularidad;
- cambio de definicion de negocio que altere la lectura del dataset.

Una nueva corrida del mismo pipeline, sin cambios de esquema, no justifica por si sola un nuevo versionado.

## Valor metodologico dentro del proyecto
Esta convencion cumple un papel concreto dentro del portafolio:

- hace visible que el proyecto no solo limpia datos, sino que tambien define una capa analitica con criterios formales;
- facilita que los datasets finales sean entendibles para una revision rapida;
- alinea la presentacion del repositorio con el uso tecnico real de los datos.
