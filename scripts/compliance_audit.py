#!/usr/bin/env python
"""
Auditoría de cumplimiento para el microservicio Palma Bike.

Verifica políticas de seguridad y calidad antes de permitir que el pipeline
continúe con etapas críticas como la construcción de la imagen o el despliegue.

Código de salida:
    0: cumplimiento aceptado
    1: falla crítica, el pipeline debe detenerse
"""
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Reglas de severidad
CRITICAL = "CRITICAL"
WARNING = "WARNING"


def log(level: str, message: str) -> None:
    """Imprime un mensaje de auditoría etiquetado."""
    print(f"[{level}] {message}")


def check_hardcoded_secrets() -> list[str]:
    """Detecta patrones de secretos hardcodeados en el código fuente."""
    issues: list[str] = []
    patterns = {
        "SECRET_KEY": re.compile(r"SECRET_KEY\s*=\s*[\"'][^\"']+[\"']"),
        "API_KEY": re.compile(r"API[_]?KEY\s*=\s*[\"'][^\"']+[\"']"),
        "PASSWORD": re.compile(r"PASSWORD\s*=\s*[\"'][^\"']+[\"']"),
        "PRIVATE_KEY": re.compile(r"BEGIN\s+(RSA|OPENSSH|DSA|EC)\s+PRIVATE\s+KEY"),
    }

    excluded_dirs = {"venv", ".git", "__pycache__", "migrations", "node_modules"}
    target_exts = {".py", ".yml", ".yaml", ".json", ".sh", ".env"}

    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in excluded_dirs for part in path.parts):
            continue
        if path.suffix not in target_exts and path.name not in {".env", "docker-compose.yml"}:
            continue

        content = read_text_file(path)

        for name, pattern in patterns.items():
            if pattern.search(content):
                issues.append(
                    f"Posible secreto '{name}' hardcodeado en {path.relative_to(REPO_ROOT)}"
                )

    return issues


def check_committed_env_files() -> list[str]:
    """Verifica que no haya archivos .env o .env.* en el repositorio."""
    issues: list[str] = []
    for path in REPO_ROOT.iterdir():
        if path.name.startswith(".env"):
            issues.append(f"Archivo de entorno potencialmente expuesto: {path.name}")
    return issues


def read_text_file(path: Path) -> str:
    """Lee un archivo de texto intentando UTF-8 y UTF-16."""
    encodings = ["utf-8", "utf-16"]
    for encoding in encodings:
        try:
            return path.read_text(encoding=encoding)
        except UnicodeError:
            continue
    return path.read_text(encoding="utf-8", errors="ignore")


def check_dependency_versioning() -> list[str]:
    """Verifica que requirements.txt use versiones explícitas."""
    issues: list[str] = []
    req_file = REPO_ROOT / "requirements.txt"
    if req_file.exists():
        for line in read_text_file(req_file).splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "==" not in line and ">=" not in line:
                issues.append(f"Dependencia sin versionar en requirements.txt: {line}")
    return issues


def check_dangerous_functions() -> list[str]:
    """Detecta uso de funciones eval/exec en Python."""
    issues: list[str] = []
    pattern = re.compile(r"\b(eval|exec)\s*\(")
    for path in REPO_ROOT.rglob("*.py"):
        if any(part in {"venv", ".git", "__pycache__", "migrations"} for part in path.parts):
            continue
        content = read_text_file(path)
        if pattern.search(content):
            issues.append(f"Uso de eval/exec detectado en {path.relative_to(REPO_ROOT)}")
    return issues


def check_debug_in_production_branch() -> list[str]:
    """Advierte sobre DEBUG=True en settings.py (riesgo para ramas principales)."""
    issues: list[str] = []
    settings_file = REPO_ROOT / "TestDjango" / "settings.py"
    if settings_file.exists():
        content = settings_file.read_text(encoding="utf-8")
        if re.search(r"\bDEBUG\s*=\s*True", content):
            issues.append("DEBUG=True en TestDjango/settings.py; revisar antes de desplegar a producción")
    return issues


def main() -> int:
    """Ejecuta todas las verificaciones y decide si el pipeline debe continuar."""
    critical: list[str] = []
    warnings: list[str] = []

    log(WARNING, "Iniciando auditoría de cumplimiento...")

    hardcoded = check_hardcoded_secrets()
    if hardcoded:
        critical.extend(hardcoded)

    env_files = check_committed_env_files()
    if env_files:
        critical.extend(env_files)

    versioning = check_dependency_versioning()
    if versioning:
        warnings.extend(versioning)

    dangerous = check_dangerous_functions()
    if dangerous:
        critical.extend(dangerous)

    debug_branch = check_debug_in_production_branch()
    current_branch = os.environ.get("GITHUB_REF_NAME", os.environ.get("CI_BRANCH", "unknown"))
    if debug_branch and current_branch in {"main", "master"}:
        critical.extend(debug_branch)
    elif debug_branch:
        warnings.extend(debug_branch)

    print("\n--- Resumen de auditoría ---")
    print(f"Errores críticos: {len(critical)}")
    print(f"Advertencias:     {len(warnings)}")

    for issue in critical:
        log(CRITICAL, issue)
    for issue in warnings:
        log(WARNING, issue)

    if critical:
        print("\nAuditoría FALLIDA: se detectaron problemas críticos. El pipeline se detendrá.")
        return 1

    print("\nAuditoría exitosa: no se detectaron problemas críticos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
