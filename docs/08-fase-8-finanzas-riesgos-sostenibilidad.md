# Fase 8 - Finanzas, Riesgos y Sostenibilidad

## Objetivo

Implementar la base de gestion financiera, riesgos operacionales y sostenibilidad para que la simulacion empiece a reflejar costos, flujo de caja, exposicion al riesgo e impacto ambiental.

## Alcance Exacto

Incluye:

- Aplicacion `finance`.
- Aplicacion `risks`.
- Aplicacion `sustainability`.
- Transacciones financieras por empresa.
- Resumen financiero con ingresos, costos, utilidad, margen y flujo de caja.
- Eventos de riesgo operacionales.
- Respuestas de mitigacion, prevencion, recuperacion o contingencia.
- Registros de sostenibilidad por periodo.
- Calculo de emisiones totales y porcentaje de residuos recuperados.
- Integracion con el motor de simulacion mediante eventos por flujo de caja negativo, riesgos abiertos y residuos/emisiones.

No incluye:

- Contabilidad completa.
- Integracion bancaria.
- Presupuesto por centro de costo.
- Modelos probabilisticos avanzados de riesgo.
- Huella de carbono certificada.

## Reglas de Negocio

- Solo se administran datos de empresas propias.
- Los ingresos aumentan flujo de caja.
- Los costos, gastos y penalizaciones reducen flujo de caja.
- El margen se calcula como utilidad sobre ingresos.
- Los eventos de riesgo pueden quedar abiertos, mitigados, recuperados o cerrados.
- Las acciones de respuesta deben asociarse a un evento de riesgo.
- Los indicadores ambientales no pueden aceptar valores negativos.

## Modelo de Datos

Entidades:

- `FinancialTransaction`
- `FinancialSnapshot`
- `RiskEvent`
- `RiskResponse`
- `SustainabilityRecord`

## Criterios de Aceptacion

- Un estudiante puede registrar transacciones financieras.
- El sistema puede generar un resumen financiero.
- Un estudiante puede registrar riesgos y respuestas.
- Un estudiante puede registrar indicadores ambientales.
- El motor genera eventos por riesgos abiertos, flujo de caja negativo y sostenibilidad.
- Las pruebas automaticas pasan.

