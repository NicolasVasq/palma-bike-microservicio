"""Genera la presentacion EP3 de Palma Bike (maximo 3 slides)."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

VERDE = RGBColor(0x1B, 0x5E, 0x20)
VERDE_OSCURO = RGBColor(0x0D, 0x33, 0x11)
AZUL = RGBColor(0x0A, 0x4D, 0x8C)
GRIS = RGBColor(0x33, 0x38, 0x3C)
GRIS_CLARO = RGBColor(0xF2, 0xF4, 0xF3)
BLANCO = RGBColor(0xFF, 0xFF, 0xFF)
NARANJO = RGBColor(0xE6, 0x7E, 0x22)

FUENTE = "Segoe UI"


def agregar_texto(slide, texto, izquierda, arriba, ancho, alto, tamano=18,
                   color=GRIS, negrita=False, alineacion=PP_ALIGN.LEFT,
                   interlineado=1.0):
    caja = slide.shapes.add_textbox(izquierda, arriba, ancho, alto)
    marco = caja.text_frame
    marco.word_wrap = True
    lineas = texto.split("\n")
    for i, linea in enumerate(lineas):
        parrafo = marco.paragraphs[0] if i == 0 else marco.add_paragraph()
        parrafo.text = linea
        parrafo.alignment = alineacion
        parrafo.line_spacing = interlineado
        parrafo.space_after = Pt(4)
        for fragmento in parrafo.runs:
            fragmento.font.name = FUENTE
            fragmento.font.size = Pt(tamano)
            fragmento.font.bold = negrita
            fragmento.font.color.rgb = color
    return caja


def agregar_rectangulo(slide, izquierda, arriba, ancho, alto, color):
    forma = slide.shapes.add_shape(1, izquierda, arriba, ancho, alto)
    forma.fill.solid()
    forma.fill.fore_color.rgb = color
    forma.line.fill.background()
    return forma


def bullets(slide, items, izquierda, arriba, ancho, alto, tamano=16):
    caja = slide.shapes.add_textbox(izquierda, arriba, ancho, alto)
    marco = caja.text_frame
    marco.word_wrap = True
    for i, (titulo, detalle) in enumerate(items):
        parrafo = marco.paragraphs[0] if i == 0 else marco.add_paragraph()
        run_t = parrafo.add_run()
        run_t.text = titulo + ": "
        run_t.font.name = FUENTE
        run_t.font.size = Pt(tamano)
        run_t.font.bold = True
        run_t.font.color.rgb = VERDE_OSCURO
        run_d = parrafo.add_run()
        run_d.text = detalle
        run_d.font.name = FUENTE
        run_d.font.size = Pt(tamano)
        run_d.font.color.rgb = GRIS
        parrafo.space_after = Pt(10)
        parrafo.line_spacing = 1.05
    return caja


prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
en_blanco = prs.slide_layouts[6]

# ======================= SLIDE 1: PORTADA =======================
s1 = prs.slides.add_slide(en_blanco)
agregar_rectangulo(s1, 0, 0, prs.slide_width, prs.slide_height, VERDE_OSCURO)
agregar_rectangulo(s1, 0, Inches(5.1), prs.slide_width, Inches(2.4), VERDE)
agregar_texto(
    s1,
    "PALMA BIKE",
    Inches(0.8), Inches(1.5), Inches(11.7), Inches(1.6),
    tamano=66, color=BLANCO, negrita=True,
)
agregar_texto(
    s1,
    "Microservicio Django con pipeline DevOps de extremo a extremo",
    Inches(0.85), Inches(2.9), Inches(11.7), Inches(0.8),
    tamano=24, color=RGBColor(0xB9, 0xE4, 0xBB),
)
agregar_texto(
    s1,
    "Evaluacion Parcial 3  -  Ingenieria DevOps (DOY0101)",
    Inches(0.85), Inches(3.7), Inches(11.7), Inches(0.6),
    tamano=20, color=RGBColor(0x9C, 0xD8, 0x9F), negrita=True,
)
agregar_texto(
    s1,
    "Nicolas Vasquez",
    Inches(0.85), Inches(5.6), Inches(6), Inches(0.6),
    tamano=26, color=BLANCO, negrita=True,
)
agregar_texto(
    s1,
    "github.com/NicolasVasq/palma-bike-microservicio",
    Inches(0.85), Inches(6.3), Inches(9), Inches(0.6),
    tamano=18, color=RGBColor(0xD6, 0xF0, 0xD8),
)
agregar_texto(
    s1,
    "Tienda online de bicicletas, repuestos y accesorios",
    Inches(6.5), Inches(5.65), Inches(6), Inches(1),
    tamano=16, color=BLANCO, alineacion=PP_ALIGN.RIGHT,
)

# ================ SLIDE 2: CASO DE USO / APLICACION ================
s2 = prs.slides.add_slide(en_blanco)
agregar_rectangulo(s2, 0, 0, prs.slide_width, Inches(1.35), VERDE)
agregar_texto(
    s2,
    "Caso de uso: e-commerce de bicicletas",
    Inches(0.6), Inches(0.25), Inches(12), Inches(0.9),
    tamano=32, color=BLANCO, negrita=True,
)
bullets(
    s2,
    [
        ("Aplicacion",
         "plataforma web de comercio electronico para venta de bicicletas, repuestos y accesorios (Palma Bike)."),
        ("Funcionalidades",
         "catalogo de productos con imagenes, precios, marcas y stock; carrito de compras y generacion de boletas; registro, autenticacion y recuperacion de contrasena; panel administrativo de inventario."),
        ("Stack de desarrollo",
         "Python 3.13 + Django 5, SQLite, pytest-django; contenerizado con Docker y Docker Compose."),
        ("Que anade la EP3",
         "monitoreo con Prometheus y Grafana, endpoint de metricas personalizadas, manifiestos de Kubernetes para despliegue orquestado y auditoria automatica de cumplimiento en el pipeline."),
    ],
    Inches(0.6), Inches(1.7), Inches(12.1), Inches(4.6),
    tamano=17,
)
agregar_rectangulo(s2, Inches(0.6), Inches(5.9), Inches(12.1), Inches(1.1), GRIS_CLARO)
agregar_texto(
    s2,
    "Flujo DevOps:  auditoria de cumplimiento  ->  pruebas con cobertura  ->  Bandit  ->  build Docker + Trivy  ->  publicacion en GHCR  ->  despliegue simulado con verificacion de metricas",
    Inches(0.8), Inches(6.1), Inches(11.7), Inches(0.8),
    tamano=14, color=AZUL, negrita=True,
)

# ================ SLIDE 3: EVIDENCIA DE EJECUCION ================
s3 = prs.slides.add_slide(en_blanco)
agregar_rectangulo(s3, 0, 0, prs.slide_width, Inches(1.35), AZUL)
agregar_texto(
    s3,
    "Evidencia de ejecucion",
    Inches(0.6), Inches(0.25), Inches(12), Inches(0.9),
    tamano=32, color=BLANCO, negrita=True,
)
bullets(
    s3,
    [
        ("Pipeline CI/CD en GitHub Actions (rama main)",
         "5 jobs encadenados: auditoria de cumplimiento, pytest-cov (cobertura 55%), Bandit, build + Trivy y despliegue simulado. Ultima ejecucion exitosa: 2 min 46 s."),
        ("Imagen publicada",
         "ghcr.io/nicolasvasq/palma-bike-microservicio:latest, generada automaticamente en cada merge a main."),
        ("Monitoreo verificado en ejecucion",
         "el deploy simulado comprueba /, /metrics (Prometheus), /custom-metrics/ (cobertura y duracion de despliegue) y /api/health de Grafana."),
        ("Despliegue orquestado",
         "manifiestos Kubernetes listos para EKS/AKS/GKE: 2 replicas, healthchecks, HPA por CPU/memoria y LoadBalancer."),
    ],
    Inches(0.6), Inches(1.65), Inches(12.1), Inches(4.4),
    tamano=16,
)
agregar_rectangulo(s3, Inches(0.6), Inches(5.85), Inches(12.1), Inches(1.2), VERDE_OSCURO)
agregar_texto(
    s3,
    "Repositorio:  github.com/NicolasVasq/palma-bike-microservicio/n- Pipeline:  pestaña Actions, workflow \"CI/CD Pipeline\" (exitoso en main)",
    Inches(0.85), Inches(6.05), Inches(11.7), Inches(0.9),
    tamano=15, color=BLANCO, negrita=True,
)

prs.save(r"docs\ep3\EP3_Palma_Bike_Presentacion.pptx")
print("Presentacion generada: docs/ep3/EP3_Palma_Bike_Presentacion.pptx")
