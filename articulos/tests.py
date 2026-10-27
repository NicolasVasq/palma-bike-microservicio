import pytest
from django.db.utils import IntegrityError
from django.test import Client
from django.urls import reverse

from articulos.models import Marca, Producto


@pytest.mark.django_db
class TestModelosArticulos:
    """Pruebas unitarias para los modelos de la aplicación articulos."""

    def test_crear_marca(self):
        marca = Marca.objects.create(nombreMarca="Trek")
        assert marca.nombreMarca == "Trek"
        assert str(marca) == "Trek"

    def test_crear_producto(self):
        marca = Marca.objects.create(nombreMarca="Giant")
        producto = Producto.objects.create(
            nombre="Bicicleta Montaña",
            precio=350000,
            nombreMarca=marca,
            stock=10,
        )
        assert producto.nombre == "Bicicleta Montaña"
        assert producto.precio == 350000
        assert producto.stock == 10
        assert str(producto) == "Bicicleta Montaña"

    def test_stock_no_puede_ser_negativo(self):
        marca = Marca.objects.create(nombreMarca="Scott")
        producto = Producto(
            nombre="Bicicleta Ruta",
            precio=500000,
            nombreMarca=marca,
            stock=-1,
        )
        with pytest.raises(IntegrityError):
            producto.save()


class TestVistasInicio:
    """Pruebas de integración básicas para las vistas públicas."""

    def test_pagina_inicio_responde_200(self):
        cliente = Client()
        respuesta = cliente.get("/")
        assert respuesta.status_code == 200

    def test_pagina_nosotros_responde_200(self):
        cliente = Client()
        respuesta = cliente.get("/nosotros/")
        assert respuesta.status_code == 200
