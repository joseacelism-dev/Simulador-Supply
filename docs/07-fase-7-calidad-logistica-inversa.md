# Fase 7 - Calidad y Logistica Inversa

## Objetivo

Implementar la base de gestion de calidad y logistica inversa para registrar inspecciones, no conformidades, reclamos, devoluciones, disposicion y recuperacion de valor.

## Alcance Exacto

Incluye:

- Aplicacion `quality`.
- Aplicacion `reverse_logistics`.
- Inspecciones de calidad sobre productos.
- No conformidades.
- Reclamos de cliente.
- Solicitudes de devolucion asociadas a pedidos.
- Lineas de devolucion por producto.
- Inspeccion de devoluciones.
- Decisiones de disposicion: reintegrar, reparar, reacondicionar, reciclar, reutilizar, disposicion final, reembolso o cambio.
- Calculo de valor recuperado.
- Integracion inicial con el motor de simulacion mediante eventos por reclamos, no conformidades y devoluciones abiertas.

No incluye:

- Trazabilidad por lote completa.
- Retiro masivo de producto.
- Disposicion ambiental avanzada.
- Garantias complejas.
- Integracion contable de reembolsos.

## Reglas de Negocio

- Solo se gestionan datos de empresas propias.
- Una inspeccion pertenece a un producto de la misma empresa.
- Una no conformidad puede quedar abierta, en revision, resuelta o rechazada.
- Una solicitud de devolucion pertenece a un pedido de la misma empresa.
- No se permiten cantidades de devolucion iguales o inferiores a cero.
- Una devolucion inspeccionada puede recibir una decision de disposicion.
- El valor recuperado no puede ser negativo.

## Modelo de Datos

Entidades:

- `QualityInspection`
- `NonConformance`
- `CustomerComplaint`
- `ReturnRequest`
- `ReturnLine`
- `ReturnInspection`
- `DispositionDecision`

## Criterios de Aceptacion

- Un estudiante puede crear una inspeccion de calidad.
- Una inspeccion puede registrar unidades conformes y no conformes.
- Un estudiante puede registrar un reclamo.
- Un estudiante puede crear una solicitud de devolucion.
- Una devolucion puede inspeccionarse y recibir disposicion.
- El motor genera eventos por reclamos, no conformidades y devoluciones abiertas.
- Las pruebas automaticas pasan.

