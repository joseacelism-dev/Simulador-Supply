# Fase 3 - Motor de Simulacion

## Objetivo

Crear el nucleo inicial del motor de simulacion de eventos discretos para **SCM SimLab 360**.

Esta fase habilita simulaciones por periodos, estados, decisiones, eventos, procesamiento, resultados e historial.

## Alcance Exacto

Incluye:

- Aplicacion Django `simulations`.
- Creacion de simulaciones asociadas a una empresa.
- Estados de simulacion.
- Periodos de simulacion.
- Registro de decisiones.
- Cierre y procesamiento de periodos.
- Registro de eventos generados por el motor.
- Resultados basicos por periodo.
- Pantallas para listar, crear, consultar y procesar simulaciones.
- Pruebas automaticas del flujo principal.

No incluye:

- Compras reales.
- Inventarios reales.
- Produccion real.
- Transporte.
- Devoluciones.
- Indicadores avanzados.
- Eventos aleatorios complejos.
- Procesos asincronos con Celery.

## Historias de Usuario

- Como estudiante, quiero crear una simulacion para una empresa propia.
- Como estudiante, quiero registrar decisiones por periodo.
- Como estudiante, quiero cerrar un periodo para que el sistema procese eventos y resultados.
- Como estudiante, quiero consultar el historial de decisiones y eventos.
- Como docente, quiero consultar las simulaciones realizadas por estudiantes.

## Casos de Uso

- Crear simulacion.
- Iniciar simulacion.
- Abrir periodo.
- Registrar decision.
- Cerrar periodo.
- Procesar periodo.
- Consultar eventos.
- Consultar resultados.

## Reglas de Negocio

- Solo estudiantes pueden crear simulaciones sobre empresas propias.
- Una simulacion pertenece a una empresa.
- Una simulacion conserva decisiones, eventos y resultados.
- Las decisiones solo se registran cuando existe un periodo abierto.
- Al cerrar un periodo, las decisiones quedan bloqueadas.
- El procesamiento genera eventos y resultados trazables.
- El estudiante no puede acceder a simulaciones de otro estudiante.
- El docente puede consultar simulaciones de todos los estudiantes.

## Estados de Simulacion

- `configuracion`
- `lista`
- `en_curso`
- `periodo_abierto`
- `decisiones_registradas`
- `procesando`
- `periodo_cerrado`
- `finalizada`
- `cancelada`

## Modelo de Datos

Entidades:

- `Simulation`
- `SimulationPeriod`
- `Decision`
- `SimulationEvent`
- `PeriodResult`

Relaciones:

- Una empresa tiene muchas simulaciones.
- Una simulacion tiene muchos periodos.
- Un periodo tiene muchas decisiones.
- Un periodo tiene muchos eventos.
- Un periodo tiene un resultado.

## Procesamiento Basico de Fase 3

El procesamiento inicial calcula resultados derivados de:

- Capital inicial de la empresa.
- Numero de productos registrados.
- Numero de materias primas.
- Numero de proveedores.
- Numero de clientes.
- Numero de decisiones del periodo.

Estos resultados no sustituyen indicadores avanzados. Funcionan como validacion temprana del motor y como base para conectar compras, inventarios y produccion en fases posteriores.

## Criterios de Aceptacion

- Un estudiante puede crear una simulacion para su empresa.
- Al crear una simulacion se crea el primer periodo abierto.
- Se pueden registrar decisiones en el periodo abierto.
- Al procesar el periodo se generan eventos y resultado.
- El periodo queda cerrado.
- La simulacion avanza al siguiente periodo o finaliza.
- El estudiante no puede consultar simulaciones ajenas.
- El docente puede consultar simulaciones generales.
- Las pruebas automaticas pasan.

