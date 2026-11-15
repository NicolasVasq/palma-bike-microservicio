# Evidencias EP3 - Observabilidad, Orquestación y Cumplimiento

Este documento reúne la evidencia de la Evaluación Parcial N°3 de Ingeniería DevOps para el microservicio Palma Bike.

## Indicadores evaluados

### IE1. Configurar herramientas de monitoreo y logging

- Se integró `django-prometheus` para exponer métricas en `/metrics`.
- Se desarrolló el endpoint `/custom-metrics/` para reportar cobertura de pruebas, duración del despliegue y commit.
- Se añadieron `Prometheus` y `Grafana` al `docker-compose.yml`.
- Se provisionó automáticamente el datasource de Prometheus y el dashboard `Palma Bike - DevOps Dashboard`.
- Archivos clave:
  - `TestDjango/settings.py`
  - `TestDjango/urls.py`
  - `monitoring/metrics_view.py`
  - `monitoring/prometheus.yml`
  - `monitoring/grafana/dashboards/palma_bike_dashboard.json`
  - `docker-compose.yml`

### IE2. Desplegar microservicios en entorno orquestado

- Se crearon manifiestos de Kubernetes en `k8s/`.
- La imagen del contenedor se publica en GitHub Container Registry (`ghcr.io`) desde el pipeline.
- El despliegue incluye 2 réplicas, healthchecks, recursos y autoescalado (HPA).
- Archivos clave:
  - `k8s/01-namespace.yml`
  - `k8s/02-configmap.yml`
  - `k8s/03-secret.yml`
  - `k8s/05-deployment.yml`
  - `k8s/06-service.yml`
  - `k8s/07-hpa.yml`

### IE3. Crear dashboard con métricas clave

El dashboard de Grafana incluye:

- Disponibilidad del servicio.
- Cobertura de pruebas.
- Tiempo de despliegue.
- Errores registrados.
- Requests por segundo.
- Latencia promedio.
- Uso de CPU y memoria.

### IE4. Documentar integración en CI/CD y toma de decisiones

- Se actualizó `README.md` con secciones de observabilidad, Kubernetes y auditoría.
- El pipeline en `.github/workflows/ci.yml` documenta cada job y cómo las salidas de cobertura y duración alimentan las métricas personalizadas.

### IE5. Implementar políticas de cumplimiento y auditoría automatizada

- Script `scripts/compliance_audit.py` verifica:
  - Secretos hardcodeados.
  - Archivos `.env` versionados.
  - Dependencias sin versión.
  - Uso de `eval` / `exec`.
  - `DEBUG=True` en ramas principales.
- `SECRET_KEY` se eliminó del código y se inyecta mediante variable de entorno.
- El pipeline CI/CD incluye un job de `compliance` que bloquea etapas posteriores si falla.

### IE6. Demostrar detención del pipeline ante falla crítica

- Bandit se ejecuta con severidad mínima MEDIA y detiene el pipeline.
- Trivy escanea vulnerabilidades CRITICAL/HIGH y detiene el pipeline.
- El script de auditoría de cumplimiento retorna código de salida `1` ante problemas críticos.

## Instrucciones de ejecución local de la pila de monitoreo

```bash
export SECRET_KEY='django-insecure-cambiar-en-produccion'
docker compose up -d
```

- Aplicación: http://localhost:8000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin / admin123)

## Instrucciones de despliegue en Kubernetes

```bash
kubectl apply -f k8s/
```

> Recordar reemplazar el placeholder de `SECRET_KEY` en `k8s/03-secret.yml` antes de producción.

## Evidencias de pipeline

Las siguientes evidencias se obtienen desde GitHub Actions tras ejecutar el workflow:

- Reporte de cobertura: artefacto `coverage-report`.
- Reporte de Bandit: artefacto `bandit-report`.
- Reporte de Trivy: artefacto `trivy-results` (generado si hay fallas).
- Imagen publicada: `ghcr.io/nicolasvasq/palma-bike-microservicio`.

*Las capturas de pantalla del pipeline, dashboard y resultados se pueden agregar a esta carpeta una vez que GitHub Actions ejecute el flujo.*
