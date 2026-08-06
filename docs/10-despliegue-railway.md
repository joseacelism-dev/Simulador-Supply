# Fase 10 - Despliegue en Railway

Objetivo: publicar SCM SimLab 360 en Railway con PostgreSQL, archivos estaticos servidos por WhiteNoise y arranque productivo con Gunicorn.

## Configuracion incluida

- `gunicorn` como servidor WSGI de produccion.
- `whitenoise` para servir archivos estaticos desde Django.
- `dj-database-url` y `psycopg` para usar PostgreSQL por `DATABASE_URL`.
- `Procfile` y `railway.json` con comando de arranque.
- `.python-version` para fijar Python 3.12 en Railway.
- `.env.example` con variables requeridas.

## Variables recomendadas en Railway

En el servicio web:

- `SECRET_KEY`: valor secreto generado para Django.
- `DEBUG`: `False`.
- `ALLOWED_HOSTS`: `.railway.app` o el dominio final asignado.
- `CSRF_TRUSTED_ORIGINS`: `https://*.railway.app` o el dominio final con `https://`.
- `DATABASE_URL`: `${{Postgres.DATABASE_URL}}`.

## Servicios

Crear un proyecto Railway con:

- Servicio web conectado al repositorio de GitHub.
- Servicio PostgreSQL dentro del mismo proyecto.

Railway expone `DATABASE_URL` desde PostgreSQL; el servicio web debe referenciarlo para mantener los datos persistentes.
