# Procedimiento en AWS para la Entrega 3

Esta guia usa la infraestructura real que ya tienen:

- Region: `us-east-2`
- Source: `GitHub`
- ECR repo: `blacklist_microservice`
- ECS cluster: `black_list_cluster`
- ECS service: `Task-blacklist-service-9zso9ucm`

## 1. Confirmar infraestructura manual

Antes del pipeline automatico, valida en `us-east-2`:

1. El `Application Load Balancer` responde por Postman.
2. La tarea ECS manual esta en estado `Running`.
3. La imagen actual existe en `Amazon ECR`.
4. La base de datos esta accesible desde la tarea.

## 2. Configurar proyecto CodeBuild para Test

Crear un proyecto `blacklist-test` con:

- Source provider: `GitHub` o `CodePipeline`
- Buildspec: `buildspec.test.yml`
- Runtime: imagen administrada con Python `3.11`

Este proyecto solo corre:

- `pip install -r requirements.txt`
- `pytest --cov=app --cov-report=term-missing -q`

## 3. Configurar proyecto CodeBuild para Build

Crear un proyecto `blacklist-build` con:

- Source provider: `GitHub` o `CodePipeline`
- Privileged mode: `Enabled`
  Porque este proyecto construye una imagen Docker.
- Buildspec: `buildspec.build.yml`

Variables de entorno del proyecto:

- `AWS_ACCOUNT_ID=772829097543`
- `AWS_DEFAULT_REGION=us-east-2`
- `IMAGE_REPO_NAME=blacklist_microservice`
- `ECS_CONTAINER_NAME=blacklist-microservice`

Permisos importantes del role de CodeBuild:

- push a `Amazon ECR`
- leer artefactos del pipeline
- escribir logs

## 4. Configurar CodePipeline

Crear pipeline con estos stages:

1. `Source`
   - Provider: `GitHub (CodeStar connection)`
   - Rama: `master`

2. `Test`
   - Provider: `CodeBuild`
   - Project: `blacklist-test`

3. `Build`
   - Provider: `CodeBuild`
   - Project: `blacklist-build`

4. `Deploy`
   - Provider: `Amazon ECS`
   - Cluster: `black_list_cluster`
   - Service: `Task-blacklist-service-9zso9ucm`
   - Input artifact: el output de `Build`
   - File name: `imagedefinitions.json`

## 5. Que produce el stage Build

El build hace tres cosas:

1. Construye la imagen Docker del microservicio
2. La publica en `772829097543.dkr.ecr.us-east-2.amazonaws.com/blacklist_microservice`
3. Genera `imagedefinitions.json`

Ese archivo es el que consume el stage `Amazon ECS` de CodePipeline.

## 6. Escenarios de evidencia

### CI fallido

Romper una prueba y hacer push a `master`.

Evidencia:

- stage `Test` fallido
- logs de `pytest`

### CI exitoso y CD exitoso

Hacer un cambio sano y push a `master`.

Evidencia:

- `Test` exitoso
- `Build` exitoso
- `Deploy` exitoso
- nueva revision en ECS
- Postman funcionando contra el ALB

### CI exitoso y CD fallido

Hacer que `Test` y `Build` pasen, pero forzar error de despliegue.

Opciones controladas:

- usar un nombre de contenedor incorrecto temporalmente en `ECS_CONTAINER_NAME`
- apuntar el stage `Deploy` a un servicio equivocado temporalmente
- alterar el nombre del archivo `imagedefinitions.json`

Luego tomar capturas del fallo del stage `Amazon ECS`.

## 7. Nota importante

Para que el proyecto `Build` funcione:

- `Privileged mode` debe estar activado en CodeBuild
- el role del proyecto debe poder hacer push a ECR
- el source del pipeline debe ser el repo correcto de GitHub en `master`
