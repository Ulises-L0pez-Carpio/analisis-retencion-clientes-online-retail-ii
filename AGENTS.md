# AGENTS.md

## Proposito
Este repositorio contiene un proyecto de portafolio sobre retencion de clientes, recurrencia de compra, cohortes y segmentacion RFM usando el dataset Online Retail II.

## Reglas del proyecto
- Todo lo visible para reclutadores debe estar en espanol.
- La logica reutilizable debe vivir en `src/`; los notebooks se usan para exploracion y validacion.
- No sobrescribas datos en `data/raw/`.
- No avances de fase sin cerrar claramente la fase actual.
- Explica antes cualquier cambio que cree o modifique archivos.
- Prioriza una estructura limpia, reproducible y defendible en entrevista.

## Convenciones de trabajo
- Usa nombres de archivos claros y consistentes.
- Documenta supuestos de negocio, limpieza y definiciones metricas.
- Manten separacion entre datos crudos, intermedios y procesados.
- En `data/processed/`, usa archivos en espanol, `snake_case`, con version explicita.
- En columnas de `data/processed/`, usa nombres tecnicos en ingles, `snake_case`, basados en la nomenclatura canonica del dataset.
- Si una decision tecnica es ambigua, elige la opcion mas razonable para un proyecto de portafolio junior/intermedio.

## Estado por fases
- Fase 1 cerrada: estructura base, ingesta inicial, auditoria y documentacion inicial.
- Fase 2 cerrada: limpieza reproducible y estandarizacion de la capa `processed`.
- Fase 3 cerrada: segmentacion RFM reproducible, cohortes, y dashboard Power BI completo (3 paginas, 36 visuales, 36 medidas DAX).
