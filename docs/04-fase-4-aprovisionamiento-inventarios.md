# Fase 4 - Aprovisionamiento e Inventarios

## Objetivo

Implementar los modulos iniciales de compras e inventarios para conectar proveedores, materias primas, ordenes de compra, lead time y existencias.

## Alcance Exacto

Incluye:

- Aplicacion `purchasing`.
- Aplicacion `inventory`.
- Ordenes de compra para materias primas.
- Lineas de orden de compra.
- Estados de compra.
- Fecha esperada de recepcion basada en lead time del proveedor.
- Inventario de materias primas.
- Movimientos de inventario.
- Recepcion de ordenes de compra.
- EOQ.
- Punto de reorden.
- Stock de seguridad.
- Alertas basicas de inventario bajo.
- Integracion inicial con el motor de simulacion.

No incluye:

- Aprobaciones complejas.
- Compras internacionales.
- Costos de importacion.
- Inventario de producto terminado.
- Produccion.
- MRP.
- Almacenamiento por ubicaciones.

## Historias de Usuario

- Como estudiante, quiero crear ordenes de compra para abastecer materias primas.
- Como estudiante, quiero ver las ordenes pendientes y recibidas.
- Como estudiante, quiero recibir una orden de compra para actualizar inventario.
- Como estudiante, quiero consultar existencias por materia prima.
- Como estudiante, quiero calcular EOQ, punto de reorden y stock de seguridad.
- Como estudiante, quiero recibir alertas cuando el inventario sea bajo.

## Reglas de Negocio

- Solo se pueden crear compras para empresas propias.
- Una orden de compra pertenece a un proveedor de la misma empresa.
- Una linea de compra pertenece a una materia prima de la misma empresa.
- No se permiten cantidades iguales o inferiores a cero.
- No se permite recibir dos veces una orden ya recibida.
- La recepcion genera movimientos de inventario.
- El inventario disponible no puede ser negativo.
- El punto de reorden se calcula como demanda durante lead time mas stock de seguridad.
- EOQ se calcula con la formula clasica: raiz cuadrada de `(2 * demanda anual * costo de ordenar) / costo anual de mantener`.

## Modelo de Datos

Entidades:

- `PurchaseOrder`
- `PurchaseOrderLine`
- `InventoryItem`
- `InventoryMovement`
- `InventoryPolicy`

## Criterios de Aceptacion

- Un estudiante puede crear una orden de compra para su empresa.
- El sistema calcula fecha esperada segun lead time del proveedor.
- Una orden puede recibirse y actualizar inventario.
- La recepcion crea movimientos de inventario.
- Se puede crear una politica de inventario por materia prima.
- El sistema calcula EOQ, punto de reorden y stock de seguridad.
- El motor de simulacion registra eventos de compras pendientes e inventario bajo.
- Las pruebas automaticas pasan.

