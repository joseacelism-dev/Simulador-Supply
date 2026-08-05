# Reglas de Desarrollo

## Reglas Generales

- Desarrollar por fases.
- No mezclar modulos futuros dentro de fases tempranas.
- No eliminar funcionalidades ya aprobadas.
- No dejar funciones criticas sin validacion.
- Documentar formulas, reglas y supuestos.
- Usar datos de prueba realistas.
- Mantener la interfaz en espanol.

## Reglas de Simulacion

- No inventar resultados sin ejecutar formulas.
- No usar valores fijos como sustituto permanente de indicadores.
- No permitir inventarios negativos sin una regla explicita de pedidos pendientes.
- No permitir decisiones superiores al presupuesto disponible.
- No permitir decisiones superiores a la capacidad disponible.
- Guardar cada decision relevante.
- Guardar cada evento generado por el motor.
- Separar los resultados de cada simulacion.

## Reglas Tecnicas

- La logica principal debe estar en el backend.
- El frontend no debe calcular resultados finales criticos.
- Usar migraciones para cambios de base de datos.
- Usar servicios de dominio para reglas complejas.
- Usar pruebas unitarias en calculos e indicadores.
- Usar pruebas de integracion en flujos completos.
- Mantener configuraciones sensibles fuera del codigo.

## Control de Calidad

Cada fase debe entregar:

- Objetivo.
- Alcance.
- Historias de usuario.
- Casos de uso.
- Reglas de negocio.
- Modelo de datos.
- Migraciones.
- Backend.
- Frontend.
- Validaciones.
- Permisos.
- Pruebas.
- Instrucciones de instalacion.
- Instrucciones de uso.
- Criterios de aceptacion.
- Lista de archivos creados o modificados.

## Git

Convencion recomendada de ramas:

- `main`: version estable.
- `develop`: integracion de desarrollo.
- `fase-1-base-sistema`: trabajo de Fase 1.
- `fase-2-empresas-catalogos`: trabajo de Fase 2.

Convencion recomendada de commits:

- `docs: prepara fase 0`
- `feat: agrega registro de estudiantes`
- `fix: corrige validacion de permisos`
- `test: agrega pruebas de autenticacion`
- `chore: configura entorno de desarrollo`

