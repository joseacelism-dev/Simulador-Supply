# Fase 6 - Almacenamiento, Pedidos y Distribucion

## Objetivo

Implementar la base operativa para almacenar producto terminado, registrar pedidos de clientes y gestionar despachos hasta la entrega.

## Alcance Exacto

Incluye:

- Aplicacion `warehouses`.
- Aplicacion `orders`.
- Aplicacion `distribution`.
- Almacenes y ubicaciones.
- Stock de producto terminado.
- Ajustes de entrada de producto terminado.
- Pedidos de clientes y lineas de pedido.
- Estados de pedido.
- Transportadores, vehiculos y rutas.
- Despachos asociados a pedidos.
- Entrega de despachos.
- Validacion para no despachar sin stock disponible.
- Eventos del motor por pedidos pendientes y despachos retrasados.

No incluye:

- Picking por olas avanzado.
- Ubicaciones por estanteria detallada.
- Optimizacion de rutas.
- Integracion automatica desde produccion a producto terminado.
- Ultima milla avanzada.
- Costeo logistico completo.

## Reglas de Negocio

- Solo se administran datos de empresas propias.
- Un pedido pertenece a un cliente de la misma empresa.
- Las lineas de pedido usan productos de la misma empresa.
- No se permiten cantidades negativas ni iguales a cero.
- Un despacho solo puede crearse si hay stock suficiente.
- Al crear despacho se descuenta stock terminado.
- Al entregar despacho cambia el estado del pedido.
- El motor registra eventos por pedidos abiertos y despachos no entregados.

## Modelo de Datos

Entidades:

- `Warehouse`
- `WarehouseLocation`
- `FinishedGoodsStock`
- `CustomerOrder`
- `CustomerOrderLine`
- `Carrier`
- `Vehicle`
- `Route`
- `Shipment`

## Criterios de Aceptacion

- Un estudiante puede crear un almacen.
- Un estudiante puede crear stock terminado para un producto propio.
- Un estudiante puede crear un pedido.
- Un despacho descuenta stock terminado.
- No se permite despachar si no hay stock suficiente.
- Un despacho puede marcarse como entregado.
- Las pruebas automaticas pasan.

