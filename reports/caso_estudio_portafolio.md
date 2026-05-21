# Caso de estudio de portafolio

## Titulo
Analisis de retencion de clientes, cohortes y segmentacion RFM en ecommerce

## Situacion
El objetivo fue convertir un dataset transaccional real en un caso de negocio claro y bien sustentado para portafolio. La pregunta central no era solo cuantos clientes compraron, sino cuantos regresaron, como se comportaron sus cohortes y donde se concentraba el valor comercial.

## Objetivo analitico
Construir un flujo reproducible que permitiera:

- limpiar y estandarizar datos transaccionales;
- definir compras validas con criterios de negocio explicitos;
- medir recurrencia y retencion por cohortes;
- segmentar clientes con RFM;
- traducir resultados a un dashboard ejecutivo.

## Enfoque tecnico
1. Ingesta del Excel original y consolidacion de hojas.
2. Construccion de una base general y una base de compras validas.
3. Generacion de tablas analiticas para clientes, cohortes y RFM.
4. Validacion con notebooks, SQL y pruebas unitarias.
5. Entrega final en Power BI para consumo de negocio.

## Decisiones importantes
- El proyecto conserva la capa `raw` como referencia original del dataset y concentra la estandarizacion analitica en la capa `processed`.
- La capa `processed` adopta nombres de archivo en espanol para los entregables del portafolio y columnas tecnicas en ingles para mantener consistencia analitica.
- La definicion de compra valida considera solo transacciones con actividad comercial valida, por lo que excluye cancelaciones, cantidades no positivas, precios no positivos y clientes sin identificador.
- En la segmentacion RFM, la metrica `frequency` se calcula a nivel de orden unica para representar recurrencia real de compra y no volumen de lineas transaccionales.

## Resultados principales
- 5,878 clientes unicos analizados.
- 72.39% de tasa de recompra.
- GBP 17.69M de ingresos totales.
- 41 paises con compras validas.
- El segmento `hibernating` es el mas grande, pero `champions` concentra el mayor valor relativo.

## Valor de negocio
El caso demuestra que una base con buena recompra agregada puede seguir teniendo un problema de reactivacion. Tambien muestra por que cohortes y RFM deben leerse juntas: una explica persistencia temporal y la otra prioridad comercial.

## Que puede evaluar un reclutador aqui
- Criterio para transformar datos crudos en datasets analiticos.
- Capacidad de documentar supuestos y reglas de limpieza.
- Separacion entre exploracion, logica reusable y capa de presentacion.
- Capacidad para conectar analisis tecnico con narrativa de negocio.

## Activos recomendados para revisar
- README principal: [README.md](../README.md)
- Resumen ejecutivo: [reports/resumen_ejecutivo_portafolio.md](resumen_ejecutivo_portafolio.md)
- Dashboard: [dashboard/README.md](../dashboard/README.md)
- Metodologia RFM: [docs/metodologia_rfm.md](../docs/metodologia_rfm.md)
