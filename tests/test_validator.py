"""Tests para el módulo validator.py de StockGuard.

Cubre los casos base y edge cases de validate_qty y validate_price.
"""

import pytest
from stockguard.validator import validate_qty, validate_price


class TestValidateQty:
    """Tests para la función validate_qty."""

    def test_qty_positivo_devuelve_true(self):
        """Un entero positivo debe devolver True."""
        assert validate_qty(10) is True

    def test_qty_uno_devuelve_true(self):
        """El valor mínimo válido (1) debe devolver True."""
        assert validate_qty(1) is True

    def test_qty_cero_devuelve_false(self):
        """El límite 0 debe devolver False."""
        assert validate_qty(0) is False

    def test_qty_negativo_devuelve_false(self):
        """Un entero negativo debe devolver False."""
        assert validate_qty(-100) is False

    def test_qty_muy_alto_devuelve_true(self):
        """Un número muy alto debe ser válido (edge case)."""
        assert validate_qty(10_000_000) is True

    def test_qty_string_lanza_typeerror(self):
        """Un string debe lanzar TypeError."""
        with pytest.raises(TypeError, match="qty debe ser int"):
            validate_qty("5")  # type: ignore

    def test_qty_none_lanza_typeerror(self):
        """None debe lanzar TypeError (edge case propio)."""
        with pytest.raises(TypeError, match="qty debe ser int"):
            validate_qty(None)  # type: ignore

    def test_qty_bool_es_int_en_python(self):
        """bool es subclase de int en Python; True(1) válido, False(0) no."""
        # bool es subclase de int → isinstance(True, int) es True
        assert validate_qty(True) is True   # True == 1
        assert validate_qty(False) is False  # False == 0


class TestValidatePrice:
    """Tests para la función validate_price."""

    def test_price_positivo_devuelve_true(self):
        """Un float positivo debe devolver True."""
        assert validate_price(9.99) is True

    def test_price_entero_positivo_devuelve_true(self):
        """Un entero positivo también es válido."""
        assert validate_price(5) is True

    def test_price_cero_devuelve_false(self):
        """El límite 0 debe devolver False."""
        assert validate_price(0) is False

    def test_price_negativo_devuelve_false(self):
        """Un precio negativo debe devolver False."""
        assert validate_price(-0.01) is False

    def test_price_muy_pequeno_devuelve_true(self):
        """Un precio muy pequeño pero positivo es válido (edge case)."""
        assert validate_price(0.0001) is True

    def test_price_muy_alto_devuelve_true(self):
        """Un precio muy alto debe ser válido (edge case propio)."""
        assert validate_price(999_999.99) is True

    def test_price_string_lanza_typeerror(self):
        """Un string debe lanzar TypeError."""
        with pytest.raises(TypeError, match="price debe ser int o float"):
            validate_price("1.5")  # type: ignore

    def test_price_none_lanza_typeerror(self):
        """None debe lanzar TypeError (edge case propio)."""
        with pytest.raises(TypeError, match="price debe ser int o float"):
            validate_price(None)  # type: ignore