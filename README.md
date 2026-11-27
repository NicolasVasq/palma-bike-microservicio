# Palma Bike - Microservicio Django

Plataforma web de comercio electrónico para una tienda de bicicletas y repuestos. Este repositorio corresponde al microservicio backend desarrollado con Django, preparado como base para un pipeline DevOps de integración y despliegue continuo.

---

## Tabla de contenidos

1. [Descripción](#descripción)
2. [Tecnologías](#tecnologías)
3. [Instalación local](#instalación-local)
4. [Estrategia de ramificación](#estrategia-de-ramificación)
5. [Flujo de trabajo DevOps](#flujo-de-trabajo-devops)
6. [Convenciones del repositorio](#convenciones-del-repositorio)
7. [Automatización con GitHub Actions](#automatización-con-github-actions)
8. [Observabilidad y monitoreo](#observabilidad-y-monitoreo)
9. [Orquestación con Kubernetes](#orquestación-con-kubernetes)
10. [Auditoría de cumplimiento](#auditoría-de-cumplimiento)
11. [Créditos y uso de IA](#créditos-y-uso-de-ia)

---

## Descripción

Palma Bike WEB es un sitio web de comercio electrónico enfocado en la venta de bicicletas, repuestos y accesorios. El sistema incluye:

- Gestión de usuarios, registro, autenticación y recuperación de contraseñas.
- Catálogo de productos con imágenes, precios, marcas y stock.
- Carrito de compras y generación de boletas.
- Panel administrativo para la gestión del inventario.

Este microservicio fue desarrollado previamente en asignaturas anteriores y ahora se prepara como punto de partida para la implementación de prácticas DevOps.

---

## Tecnologías

- **Python** 3.13+
- **Django** 5.0.6
- **django-crispy-forms** 2.5
- **crispy-bootstrap4** 2025.6
- **Pillow** 13.0
- **SQLite** (base de datos por defecto en desarrollo)
- **Docker** / **Docker Compose** (contenerización y orquestación local)
- **GitHub Actions** (CI/CD)
- **pytest-django** y **pytest-cov** (pruebas automatizadas y cobertura)
- **Bandit** y **Trivy** (análisis de seguridad)
- **Dependabot** (gestión de dependencias)
- **Prometheus** y **Grafana** (métricas y dashboards)
- **Kubernetes** (orquestación en la nube)

---

## Instalación local

```bash
# 1. Clonar el repositorio
git clone https://github.com/NicolasVasq/palma-bike-microservicio.git
cd palma-bike-microservicio

# 2. Crear y activar entorno virtual
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# Windows CMD
venv\Scripts\activate.bat
# Linux / macOS
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Definir SECRET_KEY de Django
# Windows PowerShell
$env:SECRET_KEY='django-insecure-cambiar-en-produccion'
# Linux / macOS
export SECRET_KEY='django-insecure-cambiar-en-produccion'

# 5. Aplicar migraciones
python manage.py migrate

# 6. Ejecutar servidor de desarrollo
python manage.py runserver
```

El sitio estará disponible en `http://127.0.0.1:8000`.

---

## Estrategia de ramificación

Se adopta **GitFlow** como modelo de ramificación por las siguientes razones:

- Permite mantener una rama `main` estable y lista para producción.
- Permite integrar cambios de forma controlada en `develop`.
- Facilita el trabajo paralelo mediante ramas `feature/*`.
- Permite aplicar correcciones urgentes sin interferir el desarrollo activo mediante ramas `hotfix/*`.

### Ramas principales

| Rama      | Propósito                                                                     |
|-----------|-------------------------------------------------------------------------------|
| `main`    | Código estable y desplegable. Solo recibe merge desde `develop` o `hotfix/*`. |
| `develop` | Rama de integración continua. Recibe las funcionalidades terminadas.        |

### Ramas de soporte

| Rama                  | Propósito                                                                 |
|-----------------------|---------------------------------------------------------------------------|
| `feature/<nombre>`    | Desarrollo de nuevas funcionalidades. Se parte desde `develop`.           |
| `hotfix/<nombre>`     | Corrección urgente de errores en producción. Se parte desde `main`.       |
| `release/<version>`   | (Opcional) Preparación de una versión antes de pasar a `main`.            |

---

## Flujo de trabajo DevOps

```text
feature/*  ──►  develop  ──►  main
                  ▲            ▲
                  │            │
               hotfix/*  ───────┘
```

1. **Feature branches**: cada nueva funcionalidad se desarrolla en una rama `feature/<nombre>` partir de `develop`. Al finalizar, se abre un *pull request* hacia `develop`.
2. **Integración en develop**: `develop` acumula los cambios aprobados. Cada push a `develop` dispara el flujo de integración continua (CI) en GitHub Actions.
3. **Pull request a main**: cuando `develop` está lista, se abre un *pull request* hacia `main`. Este PR ejecuta validaciones de CI antes de permitir el merge.
4. **Hotfix**: si se detecta un error crítico en producción, se crea una rama `hotfix/<nombre>` desde `main`. Se corrige, se mergea a `main` y luego se sincroniza con `develop`.

---

## Convenciones del repositorio

### Mensajes de commit

Se utiliza el formato **Conventional Commits**:

```text
<tipo>(<alcance>): <descripción corta>

<cuerpo opcional>

<referencia a issue o tarea>
```

Tipos principales:

- `feat`: nueva funcionalidad.
- `fix`: corrección de error.
- `docs`: cambios en documentación.
- `style`: cambios de formato que no afectan el código.
- `refactor`: cambios de código que no añaden funcionalidad ni corrigen errores.
- `test`: adición o modificación de pruebas.
- `chore`: tareas de mantenimiento, configuración o dependencias.

Ejemplos:

```text
feat(articulos): agregar filtro por marca en catálogo de productos

fix(models): corregir import no utilizado en articulos/models.py

docs(readme): documentar estrategia de ramificación GitFlow
```

### Naming de ramas

```text
feature/<identificador>-descripcion-corta
hotfix/<identificador>-descripcion-corta
```

Ejemplos:

- `feature/001-documentar-estrategia-devops`
- `feature/002-configurar-github-actions`
- `hotfix/003-corregir-import-distutils`

### Flujos de merge

- **Feature → develop**: merge commit o squash merge, según se acuerde en el PR.
- **Develop → main**: merge commit obligatorio para conservar la trazabilidad.
- **Hotfix → main**: merge commit. Luego se actualiza `develop` con los cambios de `main`.

### Estrategia de revisión

- Todo cambio debe realizarse mediante *pull request*.
- Se requiere al menos una aprobación antes de mergear.
- La CI debe pasar correctamente antes de permitir el merge.
- Se recomienda usar descripciones claras en los PR y asociarlos a tareas.

---

## Automatización con GitHub Actions

El pipeline completo se encuentra en `.github/workflows/ci.yml` y se ejecuta en cada push a `main`, `develop`, `feature/*` o `hotfix/*`, y en cada pull request hacia `main` o `develop`.

### Disparadores

- Push a `main`, `develop`, `feature/*` y `hotfix/*`.
- Pull requests dirigidos a `main` o `develop`.

### Jobs del pipeline

1. **Auditoría de cumplimiento**: ejecuta `scripts/compliance_audit.py` y bloquea el pipeline si detecta secretos versionados, archivos `.env` commiteados o funciones peligrosas.
2. **Validación y pruebas**: instala dependencias, ejecuta `pytest --cov`, genera `coverage.xml`, verifica `manage.py check` y valida migraciones pendientes.
3. **Análisis estático de seguridad**: ejecuta Bandit en el código Python. Bloquea el pipeline ante severidad MEDIA o superior.
4. **Escaneo de secretos**: Gitleaks analiza el historial completo del repositorio en busca de credenciales filtradas y bloquea el pipeline ante cualquier detección.
5. **Build, escaneo y publicación**: construye una imagen Docker, la publica en GitHub Container Registry (`ghcr.io`), replica la publicación en Docker Hub (si los secrets `DOCKERHUB_USERNAME` y `DOCKERHUB_TOKEN` están configurados) y la escanea con Trivy. El reporte SARIF se almacena como artefacto.
6. **Despliegue simulado con monitoreo**: levanta el servicio con Docker Compose, ejecuta las **pruebas de aceptación** (`scripts/acceptance_tests.py`) contra las páginas funcionales y los endpoints de métricas, verifica la disponibilidad de Grafana y ejecuta `manage.py check` dentro del contenedor.

Además del pipeline, la **GitHub App de SonarCloud** analiza automáticamente cada pull request (análisis de calidad y seguridad de código nuevo) y su check "SonarCloud Code Analysis" bloquea el merge si detecta problemas críticos, funcionando como quality gate del repositorio.

---

## Contenerización

El proyecto incluye un `Dockerfile` basado en `python:3.13-alpine` para generar una imagen ligera y segura, junto con un `.dockerignore` que excluye archivos innecesarios.

### Imagen Docker

```bash
# Construir imagen
docker build -t palma-bike:latest .

# Ejecutar contenedor
docker run -p 8000:8000 palma-bike:latest
```

La imagen aplica migraciones automáticamente al iniciar y expone el servicio en el puerto `8000`.

---

## Orquestación con Docker Compose

El archivo `docker-compose.yml` permite levantar el microservicio de forma orquestada:

```bash
docker compose up -d
```

Incluye:
- Construcción automática de la imagen.
- Variables de entorno para configuración dinámica.
- Healthcheck periódico del servicio.
- Política de reinicio `unless-stopped`.

Para detener:

```bash
docker compose down
```

---

## Pruebas automatizadas

Se implementaron pruebas unitarias con **pytest-django**.

```bash
pytest
```

Las pruebas actuales cubren:
- Creación de marcas y productos.
- Validación de restricciones del modelo (stock no negativo).
- Respuesta de las vistas de inicio y nosotros.

---

## Seguridad

El pipeline integra múltiples capas de seguridad:

- **Bandit**: análisis estático del código Python. Bloquea el pipeline si detecta problemas de severidad MEDIA o superior.
- **Gitleaks**: escaneo de secretos sobre el historial completo de Git. Bloquea el pipeline ante cualquier credencial filtrada.
- **Trivy**: escaneo de vulnerabilidades en la imagen Docker. Publica un reporte SARIF como artefacto para análisis y trazabilidad.
- **Auditoría de cumplimiento**: script propio que verifica secretos hardcodeados, archivos `.env` versionados, versionado explícito de dependencias y uso de `eval/exec`.
- **Dependabot**: revisa semanalmente las dependencias de Python y GitHub Actions, generando pull requests automáticos cuando existen actualizaciones.
- **SonarCloud**: la GitHub App analiza automáticamente cada pull request (calidad y seguridad del código nuevo) y el check "SonarCloud Code Analysis" falla el PR ante vulnerabilidades críticas detectadas, bloqueando el merge.
- **Pinning de actions**: las actions nuevas del pipeline se fijan por hash SHA completo de commit (requisito de SonarCloud para blindaje de la cadena de suministro).

Si cualquier análisis crítico de seguridad o cumplimiento falla, el pipeline se bloquea y no continúa hacia el despliegue.

---

## Pruebas de aceptación

`scripts/acceptance_tests.py` define las pruebas de aceptación que deben pasar antes de autorizar un despliegue a producción. Validan contra una instancia en ejecución (Docker Compose en el pipeline, o el clúster Kubernetes):

- Páginas funcionales públicas: `/`, `/nosotros/`, `/articulos/tienda/`.
- Endpoints de observabilidad: `/metrics` (contiene `django_http_requests_total`) y `/custom-metrics/` (contiene `palma_bike_test_coverage_percent`).

```bash
BASE_URL=http://localhost:8000 python scripts/acceptance_tests.py
```

Cualquier prueba fallida bloquea el despliegue (código de salida 1).

---

## Despliegue automatizado simulado

Como parte del pipeline, una vez aprobados tests, build y seguridad, se realiza un despliegue simulado con Docker Compose dentro del runner de GitHub Actions:

1. Se levanta el servicio con `docker compose up -d --build`.
2. Se espera el inicio del contenedor.
3. Se ejecutan las **pruebas de aceptación** (`scripts/acceptance_tests.py`) contra las páginas funcionales y los endpoints de métricas.
4. Se verifica la salud de Grafana en el puerto `3000`.
5. Se ejecuta `python manage.py check` dentro del contenedor.
6. Se detienen los servicios con `docker compose down`.

Este flujo garantiza trazabilidad y validación del artefacto generado antes de considerarlo listo para un entorno real.

---

## Observabilidad y monitoreo

El microservicio expone métricas en `/metrics` gracias a `django-prometheus` y métricas personalizadas en `/custom-metrics/` que reflejan cobertura de pruebas, duración del despliegue y commit de git.

La pila de monitoreo se levanta junto con la aplicación:

```bash
export SECRET_KEY='django-insecure-cambiar-en-produccion'
docker compose up -d
```

Servicios disponibles:

| Servicio   | URL                      | Descripción                                |
|------------|--------------------------|--------------------------------------------|
| Web        | http://localhost:8000    | Microservicio Django                       |
| Prometheus | http://localhost:9090    | Recolección de series temporales           |
| Grafana    | http://localhost:3000   | Dashboards de DevOps (usuario `admin` / `admin123`) |

### Dashboard incluido

El dashboard `Palma Bike - DevOps Dashboard` se provisiona automáticamente en Grafana e incluye:

- Disponibilidad del servicio (`up`).
- Cobertura de pruebas (`palma_bike_test_coverage_percent`).
- Tiempo de despliegue (`palma_bike_deployment_duration_seconds`).
- Errores registrados (`django_http_exceptions_total`).
- Requests por segundo y latencia promedio.
- Uso de CPU y memoria del contenedor.

Los archivos de configuración se encuentran en `monitoring/`.

---

## Orquestación con Kubernetes

La carpeta `k8s/` contiene los manifiestos necesarios para desplegar el microservicio en un clúster de Kubernetes (EKS, GKE, AKS, minikube, kind, etc.):

```bash
kubectl apply -f k8s/
```

Incluye:

- `01-namespace.yml`: namespace `palma-bike`.
- `02-configmap.yml`: variables no sensibles (`DEBUG`, `ALLOWED_HOSTS`).
- `03-secret.yml`: placeholder de `SECRET_KEY` (reemplazar en producción).
- `05-deployment.yml`: despliegue con 2 réplicas, healthchecks y recursos.
- `06-service.yml`: servicio tipo `LoadBalancer`.
- `07-hpa.yml`: autoescalado horizontal según CPU y memoria.

La imagen del contenedor se publica en GitHub Container Registry como:

```text
ghcr.io/nicolasvasq/palma-bike-microservicio:latest
```

> Ver `k8s/README.md` para instrucciones detalladas.

---

## Auditoría de cumplimiento

El script `scripts/compliance_audit.py` verifica políticas mínimas de seguridad y calidad:

- No versionar secretos hardcodeados.
- No incluir archivos `.env` en el repositorio.
- No usar dependencias sin versionar.
- No usar funciones peligrosas (`eval` / `exec`).
- No dejar `DEBUG=True` en las ramas principales (`main` / `master`).

Puede ejecutarse localmente:

```bash
export SECRET_KEY='django-insecure-cambiar-en-produccion'
python scripts/compliance_audit.py
```

Si detecta alguna falla crítica, el pipeline se detiene automáticamente.

---

## Variables de entorno

| Variable | Descripción | Requerida en producción |
|----------|-------------|------------------------|
| `SECRET_KEY` | Clave secreta de Django | Sí |
| `DEBUG` | Modo depuración | Sí |
| `ALLOWED_HOSTS` | Hosts permitidos | Sí |
| `TEST_COVERAGE` | Porcentaje de cobertura expuesto en métricas | No |
| `DEPLOYMENT_DURATION` | Duración del despliegue en segundos | No |
| `BUILD_TIMESTAMP` | Timestamp UNIX del build | No |
| `GITHUB_SHA` | Hash del commit en el build | No |
| `EMAIL_HOST_USER` | Usuario SMTP | Sí |
| `EMAIL_HOST_PASSWORD` | Contraseña SMTP | Sí |
| `DEFAULT_FROM_EMAIL` | Remitente por defecto | Sí |

> **Nota:** en producción se deben sobrescribir todas las variables sensibles mediante secretos del orquestador (Kubernetes Secrets, GitHub Actions secrets, etc.).

---

## Créditos y uso de IA

- Proyecto base: **Palma Bike WEB**, desarrollado en asignaturas previas.
- Adaptación para flujo DevOps y CI/CD: realizado como Evaluación Parcial N°1, N°2 y N°3 de la asignatura Ingeniería DevOps (DOY0101).
- Se utilizó asistencia de IA (ChatGPT / OpenCode) para:
  - Mejorar la redacción de la documentación.
  - Estructurar el flujo de trabajo DevOps y la estrategia de ramificación.
  - Diseñar el pipeline de CI/CD, archivos de contenerización, monitoreo con Prometheus/Grafana, manifiestos de Kubernetes y políticas de auditoría.
- Las justificaciones técnicas, análisis y conclusiones son responsabilidad del estudiante.

---

## Licencia

Este proyecto se encuentra bajo la Licencia MIT.
