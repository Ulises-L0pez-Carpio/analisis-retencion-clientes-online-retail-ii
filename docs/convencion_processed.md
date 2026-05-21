# Convencion formal para la capa `data/processed/`

## Objetivo
Definir una regla estable y reproducible para nombrar datasets y columnas en la capa `processed` a partir de la fase 2 del proyecto.

## Alcance
Esta convencion aplica solo a `data/processed/`.

No aplica a:

- `data/raw/`, donde se preserva el archivo original;
- `data/interim/`, donde se mantiene la estructura de ingesta con nombres observados en el archivo fuente.

## Decision principal
La capa `processed` usara esta combinacion de criterios:

- nombres de archivo en español;
- nombres de columnas en ingles tecnico;
- todo en minusculas, ASCII y `snake_case`;
- version explicita en el nombre del archivo;
- `parquet` como formato por defecto.

## Convencion para nombres de archivos

### Regla base
Usar el patron:

```text
<dominio>__<contenido>__v<n>.parquet
```

### Reglas
- usar solo minusculas;
- usar caracteres ASCII;
- usar `snake_case`;
- separar bloques semanticos con doble guion bajo `__`;
- incluir siempre version explicita: `v1`, `v2`, `v3`, etc.;
- evitar nombres vagos como `final`, `nuevo`, `ok`, `limpio_final`.

### Dominios recomendados
- `transacciones`
- `clientes`
- `cohortes`
- `rfm`
- `metricas`

### Ejemplos validos
- `transacciones__lineas_limpias__v1.parquet`
- `clientes__base_analitica__v1.parquet`
- `cohortes__retencion_mensual__v1.parquet`
- `rfm__segmentacion_clientes__v1.parquet`
- `metricas__resumen_ecommerce__v1.parquet`

## Convencion para nombres de columnas

### Regla base
Usar nombres tecnicos en ingles, alineados con la nomenclatura canonica del dataset y normalizados a `snake_case`.

### Reglas
- usar solo minusculas;
- usar solo ASCII;
- no usar espacios;
- no usar acentos;
- no usar puntos ni guiones;
- no mezclar ingles y espanol dentro de la misma columna;
- preferir nombres semanticos claros antes que abreviaturas ambiguas.

### Mapeo base desde el archivo actual a `processed`

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

## Reglas para columnas derivadas
- booleanos: prefijo `is_` o `has_`
- conteos: prefijo `n_`
- fechas sin hora: sufijo `_date`
- fechas con hora: sufijo `_datetime`
- periodos mensuales: sufijo `_month`
- importes monetarios: sufijo `_gbp`
- tasas: sufijo `_rate`
- participaciones: sufijo `_share`

### Ejemplos de columnas derivadas
- `is_cancellation`
- `line_revenue_gbp`
- `invoice_month`
- `first_purchase_month`
- `months_since_first_purchase`
- `is_retained_next_30d`
- `rfm_segment`

## Regla de granularidad
Cada dataset en `processed` debe declarar implicitamente una sola granularidad principal.

Ejemplos:
- `transacciones__lineas_limpias__v1.parquet`: una fila por linea de transaccion.
- `clientes__base_analitica__v1.parquet`: una fila por cliente.
- `cohortes__retencion_mensual__v1.parquet`: una fila por cohorte y periodo.
- `rfm__segmentacion_clientes__v1.parquet`: una fila por cliente puntuado.

## Regla de versionado
Subir la version cuando cambie el esquema de forma incompatible, por ejemplo:

- renombre de columnas;
- columnas agregadas o eliminadas;
- cambio de granularidad;
- cambio de definicion de negocio que altere la interpretacion del dataset.

No subir version por una simple rerun del mismo pipeline sin cambios de esquema.

## Decision metodologica del proyecto
En este repositorio se adopta esta division deliberada:

- archivos visibles de `processed` en espanol, porque son artefactos de proyecto y portafolio;
- columnas tecnicas en ingles, porque mantienen consistencia con Python, SQL, Power BI y la nomenclatura original del dataset.

## Checklist antes de guardar un dataset en `processed`
- el nombre del archivo sigue el patron definido;
- la granularidad del dataset esta clara;
- las columnas siguen `snake_case` en ingles;
- los importes monetarios aclaran moneda si aplica;
- la version del archivo corresponde a su esquema real;
- el dataset se genera desde scripts reproducibles en `src/`.
