# Fase 5 - Produccion y MRP

## Objetivo

Implementar la base de produccion y planificacion de requerimientos de materiales para conectar productos terminados, BOM, ordenes de produccion e inventario de materias primas.

## Alcance Exacto

Incluye:

- Aplicacion `production`.
- Aplicacion `mrp`.
- Listas de materiales o BOM.
- Lineas de BOM por materia prima.
- Centros de trabajo basicos.
- Maquinas basicas.
- Ordenes de produccion.
- Estados de orden de produccion.
- Validacion de inventario antes de liberar produccion.
- Consumo de materias primas al completar orden.
- Registro de mermas y costos estimados.
- Planes MRP.
- Lineas MRP con necesidades brutas, inventario disponible, necesidades netas y ordenes planificadas.
- Integracion inicial con el motor de simulacion mediante eventos de ordenes abiertas y faltantes de materiales.

No incluye:

- Programacion avanzada.
- Secuenciacion de maquinas.
- OEE completo.
- Producto terminado en inventario.
- Subcontratacion.
- Mantenimiento avanzado.
- Produccion continua detallada.

## Reglas de Negocio

- Solo estudiantes pueden crear BOM y ordenes para empresas propias.
- Una BOM pertenece a un producto de la misma empresa.
- Cada linea de BOM consume una materia prima de la misma empresa.
- No se permiten cantidades iguales o inferiores a cero.
- Una orden de produccion requiere una BOM.
- No se puede completar una orden si no hay materia prima suficiente.
- El consumo de materias primas genera movimientos de inventario.
- MRP calcula necesidades netas sin permitir valores negativos.

## Modelo de Datos

Entidades:

- `BillOfMaterials`
- `BillOfMaterialsLine`
- `WorkCenter`
- `Machine`
- `ProductionOrder`
- `MRPPlan`
- `MRPLine`

## Criterios de Aceptacion

- Un estudiante puede crear una BOM para un producto propio.
- Un estudiante puede crear una orden de produccion.
- El sistema valida materiales requeridos contra inventario disponible.
- Completar una orden consume inventario y registra movimientos.
- MRP genera lineas con necesidades brutas, disponibles, netas y ordenes planificadas.
- El motor de simulacion registra eventos por ordenes de produccion abiertas y faltantes.
- Las pruebas automaticas pasan.

