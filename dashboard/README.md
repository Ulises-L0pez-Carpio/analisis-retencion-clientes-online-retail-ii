# Dashboard Power BI

## Estado
Esta carpeta deja listo el paquete de definicion del dashboard para Power BI.

Incluye:

- especificacion funcional del tablero;
- mockup exportable para lectura rapida en GitHub.

## Archivos
- `power_bi_especificacion.md`
- `mockup_dashboard_retencion_rfm.svg`

## Fuente de datos
El dashboard debe consumir estos parquets:

- `data/processed/clientes__base_analitica__v1.parquet`
- `data/processed/cohortes__retencion_mensual__v1.parquet`
- `data/processed/rfm__segmentacion_clientes__v1.parquet`

## Nota practica
El entorno actual no incluye Power BI Desktop, por lo que no se genero un archivo `.pbix` real desde aqui.

Lo que si queda resuelto en el repositorio es la definicion completa del tablero: paginas, visuales, filtros, medidas esperadas y mockup visual para implementarlo sin ambiguedad.
