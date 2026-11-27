# Evaluación Final Transversal — Evidencias y decisiones

Este documento indexa las evidencias del repositorio contra los requisitos de la
Evaluación Final Transversal (DOY0101 Ingeniería DevOps) y registra las
decisiones técnicas adoptadas para el despliegue en la nube.

## Índice de requisitos del encargo

| # | Requisito del ET | Estado | Evidencia |
|---|---|---|---|
| 1 | Esquema de branches en GitHub (main + feature/* + hotfix/*) | Listo | Historial de 20+ ramas `feature/*` y `hotfix/*` fusionadas vía pull requests |
| 2 | Flujo demostrado con una característica nueva y un hotfix vía PR | Listo | EP1–EP3: `feature/pipeline-cicd-avanzado`, `hotfix/ci-ghcr-push`, `hotfix/ci-image-lowercase`, etc. |
| 3 | Documentación del propósito de cada branch | Listo | `README.md`, sección "Estrategia de ramificación" |
| 4 | Dockerfile y construcción de imagen | Listo | `Dockerfile` (python:3.13-alpine), job `build-and-scan` |
| 5 | Automatización con GitHub Actions | Listo | `.github/workflows/ci.yml`, 7 jobs |
| 6 | Pruebas unitarias en el pipeline | Listo | Job `test` (pytest --cov, coverage 55%) |
| 7 | **Publicación de la imagen en Docker Hub si las pruebas son exitosas** | Código listo | Pasos "Publicar imagen en Docker Hub" en `build-and-scan`, activados por los secrets `DOCKERHUB_USERNAME`/`DOCKERHUB_TOKEN`. Al ejecutarse tras `test`, la publicación solo ocurre si las pruebas pasaron. |
| 8 | Pipeline disparado en push a develop y PR a main | Listo | Triggers de `ci.yml` |
| 9 | **SonarQube en el pipeline para PRs a main** | Código listo | Job `sonarcloud` con `SonarSource/sonarcloud-github-action@v3`, activado por el secret `SONAR_TOKEN` |
| 10 | Análisis de dependencias y escaneo de secretos (Snyk, Dependabot, SonarQube) | Listo | Dependabot (`.github/dependabot.yml`), Gitleaks (job `security-secrets`), SonarCloud (job `sonarcloud`), auditoría propia (`scripts/compliance_audit.py`) |
| 11 | Pipeline interrumpido ante problemas críticos | Listo | Auditoría de cumplimiento (exit 1), Bandit (-ll), Gitleaks |
| 12 | **Despliegue continuo en Kubernetes** | Pendiente | Manifiestos listos en `k8s/`; falta clúster EKS |
| 13 | **Istio para redes y métricas** | Pendiente | Se instalará sobre EKS |
| 14 | **AWS CloudWatch para métricas** | Pendiente | CloudWatch Container Insights sobre EKS |
| 15 | Pruebas de aceptación antes de producción | Listo | `scripts/acceptance_tests.py`, ejecutado en el job `deploy-simulated`; reutilizable contra el clúster EKS |
| 16 | Políticas de GitHub con revisiones/aprobaciones para desplegar | Listo | Branch protection en `main` y `develop` (PR obligatorio) |

## Decisiones técnicas para la nube

### Elección: Amazon EKS

El docente indicó que faltaba uso de EKS/AWS. Se elige **EKS** porque cubre en un
solo servicio los requisitos de mayor ponderación del ET:

- **IE10 (orquestación, 15%)**: EKS es Kubernetes gestionado; los manifiestos de
  `k8s/` (Deployment 2 réplicas, Service LoadBalancer, HPA 2–5 pods) se aplican
  casi sin cambios.
- **IE11 (monitoreo y logging, 15%)**: CloudWatch Container Insights entrega
  métricas **y logs** de los pods en la consola AWS, complementando
  Prometheus/Grafana.
- **IE12**: Istio corre sobre EKS y CloudWatch es nativo de AWS.

### Gestión del costo de EKS

EKS no entra en el free tier (≈US$0.10/hora el plano de control, más nodos EC2).
Estrategia: **clúster de vida corta** — crear, desplegar, capturar evidencia de
la consola AWS y destruir (`eksctl delete cluster`). Una tarde de trabajo cuesta
≈US$2–3. Se evaluará además el acceso a créditos de AWS Academy.

### Jobs condicionales del pipeline

- La publicación en Docker Hub y el análisis de SonarCloud se activan mediante
  secrets (`DOCKERHUB_USERNAME`, `SONAR_TOKEN`) para que el pipeline quede
  verde sin cuentas externas y sea fácil demostrar la activación en vivo.

## Declaración de uso de inteligencia artificial

Siguiendo la pauta del ET, se declara que se utilizó asistencia de IA
(Claude/Codeium) como herramienta de apoyo para redactar scripts, configurar
workflows de GitHub Actions y estructurar documentación técnica. Las
decisiones de arquitectura, la elección de la estrategia de ramificación, el
diseño del pipeline y las justificaciones son del autor del proyecto. Todo el
código generado fue revisado, probado y validado antes de versionarse.

## Trabajo pendiente

1. Cuentas externas: AWS (o AWS Academy), Docker Hub, SonarCloud.
2. Ensayo local del despliegue Kubernetes (Docker Desktop + kind) antes de usar
   el clúster real.
3. Creación del clúster EKS, aplicación de manifiestos, Istio y CloudWatch.
4. Captura de evidencias de la consola AWS y destrucción del clúster.
