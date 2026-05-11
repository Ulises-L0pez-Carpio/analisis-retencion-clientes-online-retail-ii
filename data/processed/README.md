# Capa `data/processed/`

Esta carpeta almacenara los datasets limpios y estandarizados del proyecto.

## Convencion adoptada
- archivos en espanol;
- `snake_case`;
- version explicita en el nombre;
- formato por defecto `parquet`;
- columnas internas en ingles tecnico y `snake_case`.

## Patron de nombre
```text
<dominio>__<contenido>__v<n>.parquet
```

## Ejemplos
- `transacciones__base_general__v1.parquet`
- `transacciones__compras_validas__v1.parquet`
- `clientes__base_analitica__v1.parquet`
- `cohortes__retencion_mensual__v1.parquet`
- `rfm__segmentacion_clientes__v1.parquet`
- `rfm__segmentacion_clientes__v1.parquet`

## Artefactos generados actualmente
- `transacciones__base_general__v1.parquet`
- `transacciones__compras_validas__v1.parquet`
- `clientes__base_analitica__v1.parquet`
- `cohortes__retencion_mensual__v1.parquet`

## Referencia
La definicion completa esta en [docs/convencion_processed.md](</C:/Users/genes/Desktop/Ciencia de datos/analisis-retencion-clientes-online-retail-ii/docs/convencion_processed.md>).
