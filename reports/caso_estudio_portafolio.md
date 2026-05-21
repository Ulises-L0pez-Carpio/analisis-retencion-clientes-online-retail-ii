# Caso de estudio de portafolio

## Titulo
Analisis de retencion de clientes, cohortes y segmentacion RFM en ecommerce

## Situacion
El objetivo fue convertir un dataset transaccional real en un caso de negocio defendible para portafolio. La pregunta central no era solo cuantos clientes compraron, sino cuantos regresaron, como se comportaron sus cohortes y donde se concentraba el valor comercial.

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
- `raw` se mantiene intocable como fuente de verdad.
- `processed` usa nombres de archivo en espanol y columnas tecnicas en ingles.
- La definicion de compra valida excluye cancelaciones, cantidades no positivas, precios no positivos y clientes sin identificador.
- La `frequency` de RFM se mide por orden unica, no por linea de detalle.

## Resultados principales
- 5,878 clientes unicos analizados.
- 72.39% de repeat rate.
- GBP 17.69M de revenue total.
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
