# Integracion Continua con AWS CodePipeline, CodeBuild y Elastic Beanstalk

Este repositorio quedo preparado para el flujo que pidio el profesor:

- `Source`: descargar el codigo desde GitHub.
- `Test`: ejecutar pruebas unitarias.
- `Build`: generar el artefacto para despliegue.
- `Deploy`: manual en Elastic Beanstalk, fuera del pipeline.

## Archivos clave del repositorio

- [buildspec.test.yml](/Users/aneira3/devops_proyecto_1_e1/buildspec.test.yml:1): instala dependencias y ejecuta `pytest`.
- [buildspec.build.yml](/Users/aneira3/devops_proyecto_1_e1/buildspec.build.yml:1): genera el archivo `blacklist-microservice-eb.zip`.
- [blacklist-microservice/Procfile](/Users/aneira3/devops_proyecto_1_e1/blacklist-microservice/Procfile:1): define el arranque WSGI para Elastic Beanstalk Python.
- [blacklist-microservice/application.py](/Users/aneira3/devops_proyecto_1_e1/blacklist-microservice/application.py:9): ajustado para que los tests usen SQLite temporal sin tocar PostgreSQL.

## Estado actual validado

- `23` pruebas exitosas.
- `82%` de cobertura total.
- El artefacto para Elastic Beanstalk se genera desde el contenido de `blacklist-microservice/`, sin carpeta padre.

## Proyecto Test en CodeBuild

Crear un proyecto llamado, por ejemplo, `blacklist-test`.

Configuracion recomendada:

- Source provider: `GitHub` o `CodePipeline`.
- Buildspec: `Use a buildspec file`.
- Buildspec name: `buildspec.test.yml`.
- Runtime: imagen administrada de Ubuntu con Python `3.11`.

Este proyecto debe ejecutar:

- instalacion de dependencias
- suite unitaria con cobertura

## Proyecto Build en CodeBuild

Crear un segundo proyecto llamado, por ejemplo, `blacklist-build`.

Configuracion recomendada:

- Source provider: `GitHub` o `CodePipeline`.
- Buildspec: `Use a buildspec file`.
- Buildspec name: `buildspec.build.yml`.
- Runtime: imagen administrada de Ubuntu con Python `3.11`.

Este proyecto debe generar:

- `artifacts/blacklist-microservice-eb.zip`

## Estructura del pipeline en CodePipeline

Crear un pipeline con tres stages:

1. `Source`
   - Provider: GitHub mediante CodeStar connection.
   - Branch: la rama que definan para la entrega, por ejemplo `master`.

2. `Test`
   - Provider: AWS CodeBuild.
   - Project: `blacklist-test`.

3. `Build`
   - Provider: AWS CodeBuild.
   - Project: `blacklist-build`.

No agregar stage de `Deploy`, porque la entrega pide CI y no CD automatizado.

## Trigger automatico por commit

En la accion `Source` del pipeline:

- Event: `Push`
- Branch filter: la rama de entrega, por ejemplo `master`

Con eso, cada commit en la rama configurada dispara automaticamente el pipeline.

## Despliegue manual a Elastic Beanstalk

La aplicacion si debe quedar desplegada en AWS, pero manualmente.

Flujo recomendado:

1. Crear una aplicacion en Elastic Beanstalk.
2. Crear un environment tipo `Web server environment`.
3. Elegir plataforma `Python 3.11`.
4. Tomar el archivo `blacklist-microservice-eb.zip` generado por la etapa `Build`.
5. Subirlo manualmente como nueva version de la aplicacion.
6. Desplegar esa version en el environment.

## Que contiene el artefacto para Beanstalk

El ZIP generado deja en la raiz del bundle los archivos que Elastic Beanstalk necesita:

- `application.py`
- `Procfile`
- `requirements.txt`
- `app/`
- `.ebextensions/`

No incluye:

- `tests/`
- cache de pytest
- archivos de cobertura
- `Dockerfile`
- `docker-compose.yml`

## Evidencias para el documento

Pipeline exitoso:

- Captura del pipeline en `Succeeded`.
- Captura del stage `Test` pasando.
- Captura del stage `Build` pasando.
- Captura del log con `23 passed`.
- Captura del artefacto `.zip` generado.

Pipeline fallido:

- Romper una prueba de forma controlada.
- Hacer commit en la rama monitoreada.
- Capturar pipeline en `Failed`.
- Capturar el fallo en el stage `Test`.

Elastic Beanstalk:

- Captura del environment desplegado.
- URL publica funcionando.
- Prueba en Postman contra la URL de AWS.

## Nota practica

En la consola de AWS debes configurar explicitamente:

- `buildspec.test.yml` para el proyecto de `Test`
- `buildspec.build.yml` para el proyecto de `Build`
