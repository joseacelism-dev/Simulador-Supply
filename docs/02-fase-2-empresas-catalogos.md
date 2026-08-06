# Fase 2 - Empresas y Catalogos Base

## Objetivo

Permitir que el estudiante cree su empresa y configure los catalogos iniciales de la cadena de suministro.

## Alcance Exacto

Incluye:

- Cinco tipos de empresa iniciales.
- Creacion y consulta de empresas.
- Productos terminados.
- Materias primas.
- Proveedores.
- Clientes.
- Validacion de propiedad de datos por estudiante.
- Consulta docente de empresas creadas.
- Formularios y pantallas base en espanol.
- Pruebas automaticas de permisos y creacion.

No incluye:

- Compras.
- Inventarios.
- Produccion.
- Simulaciones.
- Pedidos.
- Transporte.
- Reportes.
- Visualizacion 2D o 3D.

## Historias de Usuario

- Como estudiante, quiero crear una empresa para iniciar mi cadena de suministro.
- Como estudiante, quiero seleccionar un tipo de empresa para adaptar el simulador a mi contexto.
- Como estudiante, quiero registrar productos terminados para definir mi portafolio inicial.
- Como estudiante, quiero registrar materias primas para preparar fases futuras de compras y produccion.
- Como estudiante, quiero registrar proveedores y clientes para representar los extremos de mi cadena.
- Como docente, quiero consultar las empresas creadas para revisar el avance de los estudiantes.

## Casos de Uso

- Registrar empresa.
- Listar mis empresas.
- Ver detalle de empresa.
- Crear producto.
- Crear materia prima.
- Crear proveedor.
- Crear cliente.
- Consultar empresas desde panel docente.

## Reglas de Negocio

- Solo usuarios con rol estudiante pueden crear empresas.
- Toda empresa pertenece a un estudiante.
- Un estudiante solo puede ver y administrar sus propias empresas.
- El docente puede consultar empresas, pero no se le asigna una empresa obligatoria.
- Los tipos de empresa iniciales quedan cargados por migracion de datos.
- Los catalogos se asocian a una empresa especifica.
- El codigo SKU de productos y materias primas no puede repetirse dentro de la misma empresa.

## Modelo de Datos

Entidades:

- `CompanyType`
- `Company`
- `Product`
- `RawMaterial`
- `Supplier`
- `Customer`

Relaciones:

- Un estudiante tiene muchas empresas.
- Una empresa pertenece a un tipo de empresa.
- Una empresa tiene muchos productos.
- Una empresa tiene muchas materias primas.
- Una empresa tiene muchos proveedores.
- Una empresa tiene muchos clientes.

## Permisos

Estudiante:

- Crear empresas propias.
- Crear catalogos dentro de sus empresas.
- Consultar solo sus datos.

Administrador docente:

- Consultar panel docente.
- Consultar empresas creadas por estudiantes.
- Consultar catalogos desde admin de Django.

## Criterios de Aceptacion

- Existen cinco tipos de empresa iniciales.
- Un estudiante puede crear una empresa.
- Un estudiante no puede ver empresas de otro estudiante.
- Un estudiante puede crear productos, materias primas, proveedores y clientes para su empresa.
- El docente puede consultar el listado general de empresas.
- Las pruebas automaticas pasan.

## Casos de Prueba

- Carga de cinco tipos de empresa.
- Creacion de empresa por estudiante.
- Restriccion de acceso entre estudiantes.
- Creacion de producto asociado a empresa propia.
- Acceso docente al listado general.

