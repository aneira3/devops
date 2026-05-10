# Entrega 3 - CI/CD sobre AWS Fargate

Este repositorio queda preparado para una pipeline con estos componentes:

- `GitHub` como repositorio fuente
- `CodeBuild` para pruebas unitarias
- `CodeBuild` para construccion y publicacion de imagen en `Amazon ECR`
- `CodePipeline` para orquestar CI/CD
- `Amazon ECS` para desplegar sobre `AWS Fargate`

## Flujo objetivo

1. `Source`
   - El codigo vive en `GitHub`.
2. `Test`
   - `CodeBuild` ejecuta `buildspec.test.yml`.
3. `Build`
   - `CodeBuild` ejecuta `buildspec.build.yml`.
   - construye la imagen Docker
   - la publica en `Amazon ECR`
   - genera `imagedefinitions.json`
4. `Deploy`
   - `CodePipeline` usa el provider `Amazon ECS` para actualizar el servicio ECS en Fargate.

## Archivos clave

- [buildspec.test.yml](/Users/aneira3/devops_proyecto_1_e1/buildspec.test.yml:1)
- [buildspec.build.yml](/Users/aneira3/devops_proyecto_1_e1/buildspec.build.yml:1)
- [blacklist-microservice/Dockerfile](/Users/aneira3/devops_proyecto_1_e1/blacklist-microservice/Dockerfile:1)

## Infraestructura ya identificada en AWS

- Region: `us-east-2`
- ECR repo: `772829097543.dkr.ecr.us-east-2.amazonaws.com/blacklist_microservice`
- ECS cluster: `black_list_cluster`
- ECS service: `Task-blacklist-service-9zso9ucm`
- ECS container name: `blacklist-microservice`

## Variables de entorno para el proyecto Build en CodeBuild

Configura estas variables en el proyecto que ejecuta `buildspec.build.yml`:

- `AWS_ACCOUNT_ID`
- `AWS_DEFAULT_REGION`
- `IMAGE_REPO_NAME`
- `ECS_CONTAINER_NAME`

Valores tipicos:

- `ECS_CONTAINER_NAME=blacklist-microservice`

## Infraestructura manual previa en AWS

Antes del pipeline automatizado hay que tener funcionando manualmente:

1. Un repositorio en `GitHub`
2. Un repositorio en `Amazon ECR`
3. Un cluster `ECS`
4. Un servicio `ECS Fargate`
5. Un `Application Load Balancer`
6. Una target group
7. Una base PostgreSQL accesible por la tarea

## Despliegue manual inicial en Fargate

Primero debe existir un despliegue manual funcionando para probar el microservicio.

Pasos sugeridos:

1. Crear repositorio ECR
2. Construir imagen localmente
3. Publicarla en ECR
4. Crear definicion de tarea ECS
5. Crear servicio Fargate apuntando a esa tarea
6. Configurar variables:
   - `DATABASE_URL`
   - `JWT_SECRET_KEY`
7. Validar por Postman

## Pipeline recomendado

`GitHub -> CodeBuild(Test) -> CodeBuild(Build) -> ECS Deploy(Fargate)`

## Evidencias que hay que producir

1. Un pipeline de CI fallido
2. Un pipeline CI + CD exitoso
3. Un pipeline CI exitoso y CD fallido

## Nota importante

Este repositorio ya no empaqueta un ZIP para Elastic Beanstalk en la etapa `Build`.
Ahora la salida del build es:

- una imagen publicada en `Amazon ECR`
- un `imagedefinitions.json`

Eso es lo que el stage `Amazon ECS` de CodePipeline necesita para actualizar el servicio en Fargate.
