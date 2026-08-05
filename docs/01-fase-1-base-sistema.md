# Fase 1 - Base del Sistema

## Objetivo

Construir la base tecnica y funcional inicial de **SCM SimLab 360**:

- Proyecto Django.
- Usuario personalizado.
- Registro de estudiantes.
- Autenticacion.
- Roles.
- Panel basico para administrador docente.
- Panel basico para estudiante.
- Proteccion de rutas por rol.

## Alcance Exacto

Incluye:

- Configuracion inicial del proyecto Django.
- Aplicacion `accounts`.
- Modelo `User` personalizado basado en `AbstractUser`.
- Campo de rol con dos opciones:
  - `admin_docente`.
  - `estudiante`.
- Registro publico solo para estudiantes.
- Login y logout.
- Redireccion de usuarios segun rol.
- Plantillas HTML en espanol.
- Estilos base.
- Pruebas automaticas para registro, login y permisos.

No incluye:

- Empresas.
- Productos.
- Proveedores.
- Simulaciones.
- Inventarios.
- Produccion.
- Dashboards avanzados.
- Reportes.
- Visualizacion 2D o 3D.

## Arquitectura Propuesta

```text
config/
  settings.py
  urls.py
  wsgi.py
  asgi.py
apps/
  accounts/
    models.py
    forms.py
    views.py
    urls.py
    tests.py
templates/
  base.html
  accounts/
  dashboard/
static/
  css/
```

## Modelo de Usuario

El sistema usara un usuario personalizado desde el inicio para evitar migraciones costosas en fases futuras.

Campos principales:

- `username`
- `email`
- `first_name`
- `last_name`
- `role`
- `is_active`
- `is_staff`
- `date_joined`

Reglas:

- Todo usuario registrado desde la pagina publica queda como `estudiante`.
- El administrador docente se crea por comando `createsuperuser`.
- Solo usuarios autenticados pueden acceder a paneles.
- Un estudiante no puede entrar al panel docente.
- El administrador docente no usa el formulario publico para crearse.

## Modelo Inicial de Base de Datos

Tablas principales de Fase 1:

- `accounts_user`
- Tablas internas de Django para sesiones, permisos y grupos.

## Flujo de Registro

1. El estudiante abre `/accounts/registro/`.
2. Completa usuario, nombres, correo y contrasena.
3. El sistema valida el formulario.
4. El sistema crea el usuario con rol `estudiante`.
5. El sistema inicia sesion automaticamente.
6. El estudiante es enviado a `/panel/estudiante/`.

## Flujo de Autenticacion

1. El usuario abre `/accounts/login/`.
2. Ingresa usuario y contrasena.
3. Django valida credenciales.
4. El sistema redirige segun rol:
   - Administrador docente: `/panel/docente/`.
   - Estudiante: `/panel/estudiante/`.

## Permisos del Administrador Docente

En Fase 1 puede:

- Iniciar sesion.
- Ver panel docente.
- Consultar resumen inicial del sistema.
- Acceder al admin de Django si tiene `is_staff=True`.

## Permisos del Estudiante

En Fase 1 puede:

- Registrarse.
- Iniciar sesion.
- Ver su panel inicial.
- Cerrar sesion.

No puede:

- Acceder al panel docente.
- Crear empresas todavia.
- Ejecutar simulaciones todavia.

## Criterios de Aceptacion

- El proyecto Django arranca correctamente.
- Las migraciones se ejecutan sin errores.
- Existe un modelo de usuario personalizado.
- Un estudiante puede registrarse.
- El estudiante registrado recibe rol `estudiante`.
- El login redirige segun rol.
- El estudiante no puede acceder al panel docente.
- Las pruebas automaticas de Fase 1 pasan.

## Casos de Prueba

- Registro de estudiante valido.
- Registro asigna rol correcto.
- Login de estudiante redirige al panel estudiante.
- Usuario anonimo no accede a paneles.
- Estudiante autenticado no accede a panel docente.
- Administrador docente autenticado accede al panel docente.

