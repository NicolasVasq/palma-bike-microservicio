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
8. [Créditos y uso de IA](#créditos-y-uso-de-ia)

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
- **GitHub Actions** (CI/CD)

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

# 4. Aplicar migraciones
python manage.py migrate

# 5. Ejecutar servidor de desarrollo
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

El repositorio incluye un workflow básico de CI ubicado en `.github/workflows/ci.yml`.

### Disparadores

- Cada push a la rama `develop`.
- Cada pull request dirigido a la rama `main`.

### Tareas

- Checkout del código.
- Configuración de Python 3.13.
- Instalación de dependencias desde `requirements.txt`.
- Validación de sintaxis con `manage.py check`.
- Ejecución de migraciones para confirmar consistencia del modelo.

Este workflow es el primer paso hacia un pipeline de CI/CD completo.

---

## Créditos y uso de IA

- Proyecto base: **Palma Bike WEB**, desarrollado en asignaturas previas.
- Adaptación para flujo DevOps: realizado como Evaluación Parcial N°1 de la asignatura Ingeniería DevOps (DOY0101).
- Se utilizó asistencia de IA (ChatGPT / OpenCode) para:
  - Mejorar la redacción de la documentación.
  - Estructurar el flujo de trabajo DevOps y la estrategia de ramificación.
- Las justificaciones técnicas, análisis y conclusiones son responsabilidad del estudiante.

---

## Licencia

Este proyecto se encuentra bajo la Licencia MIT.
