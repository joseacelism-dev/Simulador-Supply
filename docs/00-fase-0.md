# Fase 0 - Preparacion del Proyecto

## Objetivo

Preparar el proyecto **SCM SimLab 360** antes de iniciar la construccion funcional de la plataforma.

Esta fase no desarrolla todavia modulos de negocio. Su finalidad es dejar claras las decisiones tecnicas, la organizacion del repositorio, el roadmap, los criterios de calidad y las reglas para avanzar de una fase a otra.

## Alcance

Incluye:

- Definicion del stack tecnologico.
- Definicion de arquitectura modular.
- Estructura inicial de carpetas.
- Roadmap por fases.
- Criterios de aceptacion de la Fase 0.
- Reglas de desarrollo y control de calidad.
- Preparacion del repositorio Git.

No incluye:

- Registro de usuarios.
- Inicio de sesion.
- Modelos Django.
- Base de datos funcional.
- Motor de simulacion.
- Modulos de compras, inventarios, produccion, distribucion o reportes.

## Producto Esperado

Al finalizar esta fase debe existir una base documental suficiente para iniciar la **Fase 1 - Base del sistema** sin improvisar la arquitectura.

## Decisiones Tecnicas Iniciales

El sistema se construira como una aplicacion web modular basada en Django.

La logica principal del negocio y de simulacion vivira en el backend. El frontend consumira datos ya procesados y no sera responsable de inventar resultados, indicadores o eventos.

La primera version priorizara:

- Solidez del modelo de datos.
- Seguridad basica.
- Separacion por roles.
- Trazabilidad de decisiones y eventos.
- Capacidad de crecer por modulos.

## Estructura Inicial Propuesta

```text
SIMULADOR SUPPLY/
  README.md
  docs/
    00-fase-0.md
    arquitectura.md
    roadmap.md
    reglas-desarrollo.md
  .gitignore
```

La estructura Django completa se creara en la Fase 1.

## Entregables

- Documento de Fase 0.
- Documento de arquitectura propuesta.
- Roadmap de desarrollo.
- Reglas de desarrollo.
- Archivo README inicial.
- Archivo .gitignore inicial.
- Repositorio Git local preparado.
- Remoto de GitHub configurado.

## Criterios de Aceptacion

La Fase 0 se considera completa cuando:

- Existe documentacion clara del alcance del proyecto.
- El roadmap por fases esta definido.
- La arquitectura propuesta esta documentada.
- Las reglas de desarrollo estan documentadas.
- El repositorio local esta inicializado.
- El remoto apunta a `https://github.com/joseacelism-dev/Simulador-Supply`.
- La Fase 1 tiene una entrada clara: construir la base del sistema.

## Riesgos Iniciales

- Intentar construir todos los modulos al mismo tiempo.
- Mezclar logica de simulacion en el frontend.
- Crear modelos demasiado rigidos que impidan agregar nuevos tipos de empresa.
- No probar cada fase antes de avanzar.
- Subestimar el motor de simulacion de eventos discretos.

## Siguiente Fase

La siguiente etapa es la **Fase 1 - Base del sistema**.

Antes de escribir codigo de la Fase 1 se debe presentar:

- Alcance exacto.
- Arquitectura Django.
- Estructura de carpetas.
- Modelo de usuario.
- Modelo inicial de base de datos.
- Flujo de registro.
- Flujo de autenticacion.
- Permisos por rol.
- Criterios de aceptacion.
- Casos de prueba.

