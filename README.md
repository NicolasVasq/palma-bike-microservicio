Palma Bike WEB
Descripción
Palma Bike WEB es un sitio web de comercio electrónico para una tienda de bicicletas y repuestos. El proyecto tiene como objetivo aumentar la visibilidad y eficiencia de las ventas, además de potenciar la imagen y alcance de la sucursal física.

Características
Gestión de Usuarios:

Registro y autenticación de usuarios.
Recuperación de contraseñas.
Perfiles de usuario para gestionar direcciones de envío, métodos de pago y preferencias.
Catálogo de Productos:

Visualización de productos con descripciones detalladas, precios y fotos.
Filtrado y búsqueda avanzada de productos por categorías, precios, marcas, etc.
Carrito de Compras:

Añadir y eliminar productos del carrito de compras.
Actualizar cantidades de productos en el carrito.
Visualización del resumen de compra con cálculo de precios y descuentos aplicados.
Proceso de Pago:

Pasarela de pago segura que acepta múltiples métodos de pago (tarjetas de crédito/débito, PayPal, transferencias bancarias, etc.).
Procesamiento de pagos y generación de recibos de compra.
Validación y verificación de pagos.
Gestión de Pedidos:

Generación y gestión de órdenes de compra.
Seguimiento del estado de los pedidos (procesado, enviado, entregado).
Notificaciones automáticas por email o SMS sobre el estado del pedido.
Gestión de Inventario:

Control y actualización automática del inventario en tiempo real.
Alertas de stock bajo.
Seguridad y Privacidad:

Implementación de protocolos de seguridad para proteger los datos del usuario.
Protección contra fraudes y ataques cibernéticos.
Requisitos del Sistema
Python 3.8+
Django 3.2+
PostgreSQL 12+
Node.js 14+ (para gestionar dependencias de frontend)
npm 6+ (para gestionar dependencias de frontend)
Instalación
Script Batch para Cargar el Proyecto
Para facilitar la configuración y carga del proyecto, hemos incluido un script batch (setup.bat) que automatiza gran parte del proceso de instalación y configuración.

Clonar el repositorio:

bash
Copiar código
git clone https://github.com/usuario/palma-bike-web.git
cd palma-bike-web
Ejecutar el script batch:

bash
Copiar código
setup.bat
Contenido del Script setup.bat
batch
Copiar código
@echo off
REM Crear y activar entorno virtual
python -m venv env
call env\Scripts\activate

REM Instalar dependencias del proyecto
pip install -r requirements.txt
npm install

REM Configurar base de datos
echo Configurando base de datos...
REM Aquí deberás agregar la configuración de la base de datos, por ejemplo, mediante la creación de un archivo .env o ajustando settings.py dinámicamente.

REM Migrar base de datos
python manage.py migrate

REM Ejecutar el servidor de desarrollo
python manage.py runserver

Credenciales de Administrador
Usuario: admin
Email: 
Contraseña: admin12345
Estructura del Proyecto
PBDjango/: Carpeta principal del proyecto.
cuentas/: Aplicación para la gestión de usuarios.
articulos/: Aplicación para la gestión del catálogo de productos.
cart/: Aplicación para la gestión del carrito de compras.
orders/: Aplicación para la gestión de pedidos.
templates/: Archivos HTML.
static/: Archivos estáticos (CSS, JS, imágenes).
Contribución
Haz un fork del repositorio.
Crea una nueva rama (git checkout -b feature/nueva-caracteristica).
Realiza tus cambios y haz commit (git commit -m 'Añadir nueva característica').
Sube los cambios a tu fork (git push origin feature/nueva-caracteristica).
Abre un Pull Request.
Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más información.