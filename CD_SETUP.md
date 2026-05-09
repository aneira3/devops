# Entrega 3 - CI/CD sobre AWS Fargate

Este repositorio queda preparado para una pipeline con estos componentes:

- `GitHub` como repositorio fuente
- `CodeBuild` para pruebas unitarias
- `CodeBuild` para construccion y publicacion de imagen en `Amazon ECR`
- `CodePipeline` para orquestar CI/CD
- `CodeDeploy` para desplegar sobre `Amazon ECS` con `AWS Fargate`

## Flujo objetivo

1. `Source`
   - El codigo vive en `GitHub`.
2. `Test`
   - `CodeBuild` ejecuta `buildspec.test.yml`.
3. `Build`
   - `CodeBuild` ejecuta `buildspec.build.yml`.
   - construye la imagen Docker
   - la publica en `Amazon ECR`
   - genera `deployment/taskdef.json`
   - genera `deployment/appspec.yaml`
4. `Deploy`
   - `CodeDeploy` toma esos artefactos y actualiza el servicio ECS en Fargate.

## Archivos clave

- [buildspec.test.yml](/Users/aneira3/devops_proyecto_1_e1/buildspec.test.yml:1)
- [buildspec.build.yml](/Users/aneira3/devops_proyecto_1_e1/buildspec.build.yml:1)
- [deployment/appspec.yaml](/Users/aneira3/devops_proyecto_1_e1/deployment/appspec.yaml:1)
- [deployment/taskdef.template.json](/Users/aneira3/devops_proyecto_1_e1/deployment/taskdef.template.json:1)
- [blacklist-microservice/Dockerfile](/Users/aneira3/devops_proyecto_1_e1/blacklist-microservice/Dockerfile:1)

## Infraestructura ya identificada en AWS

- Region: `us-east-2`
- ECR repo: `772829097543.dkr.ecr.us-east-2.amazonaws.com/blacklist_microservice`
- ECS cluster: `black_list_cluster`
- ECS service: `Task-blacklist-service-9zso9ucm`
- ECS task family: `Task-blacklist`
- ECS container name: `blacklist-microservice`
- CloudWatch Logs group: `/ecs/Task-blacklist`

## Variables de entorno para el proyecto Build en CodeBuild

Configura estas variables en el proyecto que ejecuta `buildspec.build.yml`:

- `AWS_ACCOUNT_ID`
- `AWS_DEFAULT_REGION`
- `IMAGE_REPO_NAME`
- `ECS_EXECUTION_ROLE_ARN`
- `ECS_TASK_ROLE_ARN`
- `ECS_TASK_FAMILY`
- `ECS_CONTAINER_NAME`
- `ECS_CONTAINER_PORT`
- `ECS_TASK_CPU`
- `ECS_TASK_MEMORY`
- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `ECS_LOG_GROUP`

Valores tipicos:

- `ECS_CONTAINER_PORT=5000`
- `ECS_TASK_CPU=1024`
- `ECS_TASK_MEMORY=3072`

## Infraestructura manual previa en AWS

Antes del pipeline automatizado hay que tener funcionando manualmente:

1. Un repositorio en `GitHub`
2. Un repositorio en `Amazon ECR`
3. Un cluster `ECS`
4. Un servicio `ECS Fargate`
5. Un `Application Load Balancer`
6. Una target group
7. Una deployment application y deployment group en `CodeDeploy`
8. Una base PostgreSQL accesible por la tarea

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

`GitHub -> CodeBuild(Test) -> CodeBuild(Build) -> CodeDeploy(ECS/Fargate)`

## Evidencias que hay que producir

1. Un pipeline de CI fallido
2. Un pipeline CI + CD exitoso
3. Un pipeline CI exitoso y CD fallido

## Nota importante

Este repositorio ya no empaqueta un ZIP para Elastic Beanstalk en la etapa `Build`.
Ahora la salida del build es:

- una imagen publicada en `Amazon ECR`
- un `taskdef.json`
- un `appspec.yaml`

Eso es lo que `CodeDeploy` necesita para ECS/Fargate.
