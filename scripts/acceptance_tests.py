#!/usr/bin/env python
"""
Pruebas de aceptación para el microservicio Palma Bike.

Validan, contra una instancia en ejecución (local, Docker Compose o
Kubernetes), que las páginas funcionales y los endpoints de métricas
respondan correctamente antes de autorizar un despliegue a producción.

Uso:
    BASE_URL=http://localhost:8000 python scripts/acceptance_tests.py

Código de salida:
    0: todas las pruebas de aceptación pasaron
    1: al menos una prueba falló, el despliegue debe detenerse
"""
import http.client
import os
import sys
from urllib.parse import urlparse

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000").rstrip("/")

CHECKS = [
    ("Página de inicio", "/", None),
    ("Página nosotros", "/nosotros/", None),
    ("Tienda de productos", "/articulos/tienda/", None),
    ("Métricas Prometheus", "/metrics", "django_http_requests_total"),
    ("Métricas personalizadas", "/custom-metrics/", "palma_bike_test_coverage_percent"),
]


def log(status: str, message: str) -> None:
    print(f"[{status}] {message}")


def run_check(name: str, path: str, expected_content: str | None) -> bool:
    url = f"{BASE_URL}{path}"
    parsed = urlparse(BASE_URL)
    try:
        if parsed.scheme == "https":
            conn = http.client.HTTPSConnection(parsed.hostname, parsed.port or 443, timeout=60)
        else:
            conn = http.client.HTTPConnection(parsed.hostname, parsed.port or 80, timeout=60)
        try:
            conn.request("GET", path)
            response = conn.getresponse()
            status = response.status
            body = response.read().decode("utf-8", errors="replace")
        finally:
            conn.close()
    except Exception as exc:
        log("FAIL", f"{name} -> {url} no responde ({exc})")
        return False

    if status != 200:
        log("FAIL", f"{name} -> {url} devolvió HTTP {status}")
        return False

    if expected_content and expected_content not in body:
        log("FAIL", f"{name} -> {url} no contiene el contenido esperado '{expected_content}'")
        return False

    log("PASS", f"{name} -> {url}")
    return True


def main() -> None:
    print(f"=== Pruebas de aceptación contra {BASE_URL} ===")
    results = [run_check(name, path, content) for name, path, content in CHECKS]
    passed = sum(results)
    print(f"\nResultado: {passed}/{len(results)} pruebas de aceptación superadas")

    if passed != len(results):
        log("FAIL", "El despliegue a producción queda bloqueado por pruebas de aceptación fallidas")
        sys.exit(1)

    log("PASS", "Todas las pruebas de aceptación superadas: despliegue autorizado")


if __name__ == "__main__":
    main()
