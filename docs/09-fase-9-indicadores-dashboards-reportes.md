# Fase 9 - Indicadores, Dashboards y Reportes

## Objetivo

Implementar indicadores operativos iniciales, dashboards de resultados, comparacion basica de simulaciones y exportacion CSV para analizar el desempeno de las empresas y simulaciones.

## Alcance Exacto

Incluye:

- Aplicacion `indicators`.
- Aplicacion `reports`.
- Calculo de KPIs iniciales.
- Registro de formula, resultado, unidad, meta, estado, semaforo, interpretacion y recomendacion.
- Dashboard general por empresa.
- Comparacion basica de simulaciones.
- Exportacion CSV de indicadores.
- Integracion con el motor de simulacion para generar indicadores al cerrar periodo.

No incluye:

- Reportes PDF finales.
- Excel avanzado.
- Graficos Chart.js profundos.
- Cubos analiticos.
- Reporteria multiusuario compleja.

## Indicadores Iniciales

- Nivel de servicio.
- Tasa de pedidos entregados.
- Tasa de devoluciones.
- Tasa de defectos.
- Margen operativo.
- Flujo de caja.
- Riesgos abiertos.
- Emisiones de transporte.
- Recuperacion de residuos.
- Puntaje operacional.

## Reglas de Negocio

- Los indicadores se calculan desde datos reales registrados en el backend.
- No se usan valores fijos como sustituto de resultados.
- Cada indicador debe incluir formula, resultado, unidad, meta, estado, semaforo, interpretacion y recomendacion.
- Los indicadores pertenecen a una empresa y opcionalmente a una simulacion/periodo.
- El exporte CSV debe respetar los datos del estudiante autenticado.

## Criterios de Aceptacion

- Un estudiante puede ver un dashboard de indicadores.
- El sistema puede generar indicadores para una empresa.
- Al procesar un periodo se generan indicadores de la simulacion.
- Se puede comparar dos o mas simulaciones.
- Se puede exportar CSV de indicadores.
- Las pruebas automaticas pasan.

