# Arquitectura Propuesta

## Vision General

**SCM SimLab 360** sera una plataforma web modular para simular cadenas de suministro completas.

La arquitectura debe permitir agregar progresivamente empresas, modulos, escenarios, indicadores, visualizaciones y reglas de simulacion sin reescribir el nucleo.

## Principios

- Backend como fuente principal de verdad.
- Modulos separados por dominio.
- Datos persistentes en PostgreSQL.
- Procesamiento asincrono para simulaciones complejas.
- Auditoria de decisiones y eventos.
- Interfaz en espanol.
- Pruebas por fase antes de avanzar.
- Preparacion para visualizacion 2D y 3D conectada al motor.

## Capas

### Capa de Presentacion

Responsable de:

- Formularios.
- Dashboards.
- Tablas.
- Alertas.
- Graficos.
- Visualizacion 2D.
- Visualizacion 3D.

Tecnologias:

- Templates Django.
- Tailwind CSS.
- HTMX.
- Alpine.js.
- Chart.js.
- SVG, Canvas y Three.js en fases posteriores.

### Capa de Aplicacion

Responsable de:

- Casos de uso.
- Validaciones.
- Permisos.
- Orquestacion de acciones del usuario.
- Servicios de negocio.

### Capa de Dominio

Responsable de:

- Reglas de negocio.
- Calculos de indicadores.
- Restricciones de presupuesto, capacidad e inventario.
- Estados de simulacion.
- Motor de eventos.

### Capa de Persistencia

Responsable de:

- Modelos Django.
- Migraciones.
- Consultas.
- Historial.
- Auditoria.

Base de datos propuesta:

- PostgreSQL en desarrollo avanzado y produccion.
- SQLite solo podria usarse temporalmente para pruebas locales iniciales si se decide simplificar la Fase 1.

## Modulos Django Previstos

La Fase 1 no creara todos estos modulos, pero la arquitectura debe preparar su incorporacion.

```text
apps/
  accounts/
  companies/
  products/
  suppliers/
  purchasing/
  demand/
  planning/
  inventory/
  production/
  mrp/
  warehouses/
  orders/
  transport/
  distribution/
  international_trade/
  quality/
  reverse_logistics/
  finance/
  risks/
  sustainability/
  simulations/
  indicators/
  reports/
  gamification/
  visualization_2d/
  visualization_3d/
  audit/
```

## Motor de Simulacion

El motor debe procesar periodos y eventos de forma trazable.

Estados previstos:

- Configuracion.
- Lista para iniciar.
- En curso.
- Periodo abierto.
- Decisiones registradas.
- Procesando.
- Periodo cerrado.
- Finalizada.
- Cancelada.

El motor debe:

- Validar decisiones.
- Procesar demanda.
- Procesar compras.
- Actualizar inventarios.
- Procesar produccion.
- Procesar transporte.
- Procesar entregas.
- Procesar devoluciones.
- Calcular costos.
- Calcular indicadores.
- Generar eventos aleatorios.
- Guardar eventos y resultados.

## Seguridad

Controles previstos:

- Usuario personalizado.
- Roles: administrador docente y estudiante.
- Proteccion CSRF.
- Validacion de formularios.
- Separacion de datos por estudiante o equipo.
- Auditoria de acciones importantes.
- Manejo seguro de variables de entorno.
- Restriccion de acceso por permisos.

## Escalabilidad Funcional

El sistema debe permitir:

- Agregar nuevos tipos de empresa.
- Agregar nuevos productos y reglas de negocio.
- Agregar escenarios.
- Incorporar mas indicadores.
- Activar visualizacion 2D y 3D sin modificar el nucleo de simulacion.
- Comparar simulaciones.

