"""
Vista que expone métricas personalizadas de despliegue y calidad para Prometheus.
Los valores se inyectan mediante variables de entorno desde el pipeline CI/CD.
"""
import os
import time
from django.http import HttpResponse
from prometheus_client import CollectorRegistry, Gauge, generate_latest, CONTENT_TYPE_LATEST


def custom_metrics(request):
    """Expone métricas de cobertura, duración de despliegue y timestamp de build."""
    registry = CollectorRegistry()

    coverage = Gauge(
        'palma_bike_test_coverage_percent',
        'Porcentaje de cobertura de pruebas del microservicio',
        registry=registry,
    )
    coverage.set(float(os.environ.get('TEST_COVERAGE', '0')))

    duration = Gauge(
        'palma_bike_deployment_duration_seconds',
        'Tiempo total del despliegue en segundos',
        registry=registry,
    )
    duration.set(float(os.environ.get('DEPLOYMENT_DURATION', '0')))

    build_ts = Gauge(
        'palma_bike_build_timestamp',
        'Timestamp UNIX del build',
        registry=registry,
    )
    build_ts.set(float(os.environ.get('BUILD_TIMESTAMP', str(time.time()))))

    commit_hash = Gauge(
        'palma_bike_commit_hash_info',
        'Información del commit de git',
        ['commit_hash'],
        registry=registry,
    )
    commit_hash.labels(commit_hash=os.environ.get('GITHUB_SHA', 'unknown')).set(1)

    data = generate_latest(registry)
    return HttpResponse(data, content_type=CONTENT_TYPE_LATEST)
