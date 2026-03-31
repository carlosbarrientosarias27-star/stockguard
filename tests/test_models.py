"""Tests para el módulo models.py de StockGuard.

Verifica la creación correcta de Items y que se lanzan
las excepciones adecuadas ante datos inválidos.
"""

import pytest
from stockguard.models import Item


class TestItemCreacion:
    """Tests de creación válida de Item."""

    def test_item_valido(self):
        """Creación de un Item con datos válidos."""
        # Arrange / Act
        item = Item(name="Tornillo", qty=10, price=1.5)
        # Assert
        assert item.name == "Tornillo"
        assert item.qty == 10
        assert item.price == 1.5

    def test_item_precio_minimo(self):
        """Item con precio muy pequeño pero positivo (edge case)."""
        item = Item(name="Arandela", qty=1000, price=0.001)
        assert item.price == 0.001

    def test_item_qty_muy_grande(self):
        """Item con cantidad muy grande (edge case)."""
        item = Item(name="Clavo", qty=9_999_999, price=0.01)
        assert item.qty == 9_999_999

    def test_item_precio_entero(self):
        """Item con precio expresado como entero (válido)."""
        item = Item(name="Martillo", qty=5, price=10)
        assert item.price == 10


class TestItemValidacionQty:
    """Tests de validación del campo qty."""

    def test_qty_cero_lanza_valueerror(self):
        """qty=0 debe lanzar ValueError."""
        with pytest.raises(ValueError, match="qty debe ser mayor que 0"):
            Item(name="X", qty=0, price=1.0)

    def test_qty_negativo_lanza_valueerror(self):
        """qty=-5 debe lanzar ValueError."""
        with pytest.raises(ValueError, match="qty debe ser mayor que 0"):
            Item(name="X", qty=-5, price=1.0)

    def test_qty_string_lanza_typeerror(self):
        """qty como string debe lanzar TypeError."""
        with pytest.raises(TypeError, match="qty debe ser int"):
            Item(name="X", qty="10", price=1.0)  # type: ignore

    def test_qty_float_lanza_typeerror(self):
        """qty como float debe lanzar TypeError (edge case)."""
        with pytest.raises(TypeError, match="qty debe ser int"):
            Item(name="X", qty=3.5, price=1.0)  # type: ignore


class TestItemValidacionPrice:
    """Tests de validación del campo price."""

    def test_price_cero_lanza_valueerror(self):
        """price=0 debe lanzar ValueError."""
        with pytest.raises(ValueError, match="price debe ser mayor que 0"):
            Item(name="X", qty=1, price=0)

    def test_price_negativo_lanza_valueerror(self):
        """price=-1 debe lanzar ValueError."""
        with pytest.raises(ValueError, match="price debe ser mayor que 0"):
            Item(name="X", qty=1, price=-1)

    def test_price_string_lanza_typeerror(self):
        """price como string debe lanzar TypeError."""
        with pytest.raises(TypeError, match="price debe ser float"):
            Item(name="X", qty=1, price="1.5")  # type: ignore