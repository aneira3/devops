# Procedimiento en AWS

Esta guia deja el flujo completo para la entrega:

- `Source` en CodePipeline
- `Test` en CodeBuild
- `Build` en CodeBuild
- despliegue manual en Elastic Beanstalk

## 1. Verificar repositorio y rama

Antes de entrar a AWS confirma:

- repo correcto en GitHub
- rama que usaras para la entrega, por ejemplo `master`
- archivos presentes en la raiz del repo:
  - `buildspec.test.yml`
  - `buildspec.build.yml`

## 2. Crear proyecto CodeBuild para Test

En `AWS CodeBuild`:

1. Ir a `Build projects`
2. Clic en `Create build project`
3. Nombre sugerido: `blacklist-test`

Configurar:

- Source provider: `GitHub` si lo creas directo en CodeBuild, o `CodePipeline` si lo crearas desde el pipeline
- Environment image: `Managed image`
- Operating system: `Ubuntu`
- Runtime: `Standard`
- Image: una que soporte `Python 3.11`
- Buildspec:
  - `Use a buildspec file`
  - `buildspec.test.yml`

Guardar el proyecto.

## 3. Crear proyecto CodeBuild para Build

En `AWS CodeBuild`:

1. Clic en `Create build project`
2. Nombre sugerido: `blacklist-build`

Configurar:

- Source provider: `GitHub` si lo creas directo en CodeBuild, o `CodePipeline` si lo crearas desde el pipeline
- Environment image: `Managed image`
- Operating system: `Ubuntu`
- Runtime: `Standard`
- Image: una que soporte `Python 3.11`
- Buildspec:
  - `Use a buildspec file`
  - `buildspec.build.yml`

Guardar el proyecto.

## 4. Crear CodePipeline

En `AWS CodePipeline`:

1. Ir a `Pipelines`
2. Clic en `Create pipeline`
3. Nombre sugerido: `blacklist-pipeline`
4. Service role: dejar que AWS cree una automaticamente
5. Artifact store: dejar bucket S3 administrado por AWS o crear uno nuevo

## 5. Configurar stage Source

En la etapa `Source`:

- Source provider: `GitHub (via CodeStar connection)`
- Conectar la cuenta de GitHub si AWS lo solicita
- Seleccionar:
  - repositorio correcto
  - rama de entrega, por ejemplo `master`

Si aparece configuracion de triggers:

- Event: `Push`
- Branch filter: la rama de entrega

## 6. Configurar stage Test

Agregar un stage llamado `Test`:

- Action provider: `AWS CodeBuild`
- Input artifact: el artefacto de `Source`
- Project name: `blacklist-test`

## 7. Configurar stage Build

Agregar un stage llamado `Build`:

- Action provider: `AWS CodeBuild`
- Input artifact: el artefacto de `Source` o la salida anterior segun la consola
- Project name: `blacklist-build`

No agregar stage `Deploy`.

## 8. Ejecutar pipeline exitoso

Con el pipeline creado:

1. Hacer commit a la rama monitoreada
2. Hacer push
3. Esperar a que corra `Source -> Test -> Build`

Debes validar:

- `Test` en estado `Succeeded`
- `Build` en estado `Succeeded`
- en logs de CodeBuild aparezca `23 passed`
- exista el artefacto `blacklist-microservice-eb.zip`

## 9. Desplegar manualmente en Elastic Beanstalk

En `AWS Elastic Beanstalk`:

1. Crear una aplicacion
2. Crear un `Web server environment`
3. Plataforma: `Docker`
4. En `Application code`, subir manualmente el archivo `blacklist-microservice-eb.zip`
5. Crear el environment

Cuando quede desplegado:

- copiar la URL publica
- probarla con Postman

Pruebas sugeridas:

- `GET /health`
- `POST /token`
- `POST /blacklists`
- `GET /blacklists/<email>`

## 10. Ejecutar pipeline fallido

Para la evidencia de fallo:

1. Romper una prueba de forma controlada
2. Hacer commit y push
3. Esperar que falle el stage `Test`
4. Tomar capturas del error
5. Revertir el cambio
6. Volver a ejecutar pipeline exitoso

## 11. Evidencias para el documento

Tomar capturas de:

- configuracion de los dos proyectos de CodeBuild
- configuracion del pipeline
- pipeline exitoso
- logs del stage `Test`
- logs del stage `Build`
- artefacto generado
- pipeline fallido
- error puntual de pruebas
- environment de Elastic Beanstalk
- URL funcionando en Postman

## 12. Guion corto para sustentar

Orden recomendado para el video:

1. mostrar repo y archivos `buildspec`
2. mostrar pruebas locales o explicar su cobertura
3. mostrar proyecto `blacklist-test`
4. mostrar proyecto `blacklist-build`
5. mostrar pipeline con 3 stages
6. mostrar ejecucion exitosa
7. mostrar artefacto generado
8. mostrar Elastic Beanstalk desplegado
9. mostrar Postman contra la URL de AWS
10. mostrar una ejecucion fallida y explicar el hallazgo
