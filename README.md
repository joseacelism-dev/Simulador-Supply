# SCM SimLab 360

Plataforma web educativa para simular cadenas de suministro integrales en contextos universitarios.

El proyecto se desarrollara progresivamente por fases. La primera version completa debe permitir que estudiantes creen empresas, configuren cadenas de suministro, ejecuten simulaciones por periodos, tomen decisiones y analicen resultados mediante indicadores, dashboards y reportes.

## Repositorio

Repositorio remoto previsto:

https://github.com/joseacelism-dev/Simulador-Supply

## Estado Actual

Fase actual implementada: **Fase 9 - Indicadores, dashboards y reportes**.

El proyecto ya incluye:

- Documentacion de Fase 0, Fase 1 y Fase 2.
- Base Django.
- Usuario personalizado.
- Registro e inicio de sesion.
- Roles de administrador docente y estudiante.
- Paneles iniciales por rol.
- Empresas por estudiante.
- Cinco tipos de empresa iniciales.
- Catalogos base de productos, materias primas, proveedores y clientes.
- Simulaciones por empresa.
- Periodos, decisiones, eventos y resultados basicos.
- Ordenes de compra para materias primas.
- Inventario inicial de materias primas, movimientos, EOQ y punto de reorden.
- BOM, ordenes de produccion y consumo de materias primas.
- MRP inicial con necesidades netas y ordenes planificadas.
- Almacenes, stock terminado, pedidos, transportadores, rutas y despachos.
- Inspecciones de calidad, reclamos, devoluciones y disposicion de retornos.
- Transacciones financieras, riesgos operacionales e indicadores ambientales.
- Indicadores, dashboard general, comparacion de simulaciones y exporte CSV.

## Stack Propuesto

Backend:

- Python
- Django
- Django REST Framework cuando sea necesario
- PostgreSQL
- Redis
- Celery
- Django Channels

Frontend:

- HTML5
- Tailwind CSS
- HTMX
- Alpine.js
- Chart.js
- SVG o Canvas para visualizacion 2D
- Three.js para visualizacion 3D

Infraestructura:

- Git y GitHub
- Docker
- Docker Compose
- Variables de entorno
- Railway para despliegue

## Documentacion

- [Plan de Fase 0](docs/00-fase-0.md)
- [Plan de Fase 1](docs/01-fase-1-base-sistema.md)
- [Plan de Fase 2](docs/02-fase-2-empresas-catalogos.md)
- [Plan de Fase 3](docs/03-fase-3-motor-simulacion.md)
- [Plan de Fase 4](docs/04-fase-4-aprovisionamiento-inventarios.md)
- [Plan de Fase 5](docs/05-fase-5-produccion-mrp.md)
- [Plan de Fase 6](docs/06-fase-6-almacenamiento-pedidos-distribucion.md)
- [Plan de Fase 7](docs/07-fase-7-calidad-logistica-inversa.md)
- [Plan de Fase 8](docs/08-fase-8-finanzas-riesgos-sostenibilidad.md)
- [Plan de Fase 9](docs/09-fase-9-indicadores-dashboards-reportes.md)
- [Arquitectura propuesta](docs/arquitectura.md)
- [Roadmap por fases](docs/roadmap.md)
- [Reglas de desarrollo](docs/reglas-desarrollo.md)
