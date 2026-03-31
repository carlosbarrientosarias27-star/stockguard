"""Tests para el módulo storage.py de StockGuard.

Usa pytest-mock para aislar las operaciones de I/O y
verificar el comportamiento ante distintos escenarios.
"""

import json
import pytest
from unittest.mock import mock_open
from stockguard.storage import (
    load_inventory,
    save_inventory,
    add_item,
    update_price,
    get_total_value,
)


class TestLoadInventory:
    """Tests para load_inventory."""

    def test_archivo_no_existe_devuelve_lista_vacia(self, mocker):
        """Si el archivo no existe, debe devolver []."""
        # Arrange
        mocker.patch("stockguard.storage.os.path.exists", return_value=False)
        # Act
        result = load_inventory("no_existe.json")
        # Assert
        assert result == []

    def test_json_corrupto_devuelve_lista_vacia(self, mocker):
        """Si el JSON está corrupto, debe devolver [] sin lanzar excepción."""
        # Arrange
        mocker.patch("stockguard.storage.os.path.exists", return_value=True)
        mocker.patch(
            "builtins.open",
            mock_open(read_data="esto no es json {{{")
        )
        # Act
        result = load_inventory("corrupto.json")
        # Assert
        assert result == []

    def test_json_valido_devuelve_items(self, mocker):
        """Con un JSON válido, debe devolver la lista de artículos."""
        # Arrange
        fake_data = [{"name": "Tornillo", "qty": 10, "price": 0.5}]
        mocker.patch("stockguard.storage.os.path.exists", return_value=True)
        mocker.patch(
            "builtins.open",
            mock_open(read_data=json.dumps(fake_data))
        )
        # Act
        result = load_inventory("inventory.json")
        # Assert
        assert result == fake_data

    def test_json_vacio_devuelve_lista_vacia(self, mocker):
        """Un JSON con lista vacía debe devolver []."""
        # Arrange
        mocker.patch("stockguard.storage.os.path.exists", return_value=True)
        mocker.patch("builtins.open", mock_open(read_data="[]"))
        # Act
        result = load_inventory()
        # Assert
        assert result == []


class TestSaveInventory:
    """Tests para save_inventory."""

    def test_guarda_con_indent_2(self, mocker):
        """El JSON guardado debe usar indent=2."""
        # Arrange
        items = [{"name": "Tuerca", "qty": 5, "price": 0.1}]
        mock_file = mock_open()
        mocker.patch("builtins.open", mock_file)
        mock_json_dump = mocker.patch("stockguard.storage.json.dump")
        # Act
        save_inventory(items, "test.json")
        # Assert
        mock_json_dump.assert_called_once_with(
            items, mock_file(), indent=2, ensure_ascii=False
        )

    def test_abre_en_modo_escritura(self, mocker):
        """El archivo debe abrirse en modo 'w'."""
        # Arrange
        mock_file = mock_open()
        mocker.patch("builtins.open", mock_file)
        mocker.patch("stockguard.storage.json.dump")
        # Act
        save_inventory([], "test.json")
        # Assert
        mock_file.assert_called_once_with("test.json", "w", encoding="utf-8")


class TestAddItem:
    """Tests para add_item con validación."""

    def test_add_item_valido(self, mocker, tmp_path):
        """Añadir un ítem válido debe persistirlo correctamente."""
        # Arrange
        filepath = str(tmp_path / "inv.json")
        # Act
        add_item("Clavo", 100, 0.05, filepath)
        # Assert
        with open(filepath) as f:
            items = json.load(f)
        assert len(items) == 1
        assert items[0]["name"] == "Clavo"

    def test_add_item_qty_negativa_lanza_valueerror(self, mocker, tmp_path):
        """qty negativa debe lanzar ValueError."""
        filepath = str(tmp_path / "inv.json")
        with pytest.raises(ValueError, match="qty debe ser mayor que 0"):
            add_item("X", -1, 1.0, filepath)

    def test_add_item_price_cero_lanza_valueerror(self, mocker, tmp_path):
        """price=0 debe lanzar ValueError."""
        filepath = str(tmp_path / "inv.json")
        with pytest.raises(ValueError, match="price debe ser mayor que 0"):
            add_item("X", 1, 0, filepath)


class TestUpdatePrice:
    """Tests para update_price con validación."""

    def test_update_price_valido(self, tmp_path):
        """Actualizar precio con valor válido debe funcionar."""
        # Arrange
        filepath = str(tmp_path / "inv.json")
        add_item("Martillo", 2, 5.0, filepath)
        # Act
        update_price("Martillo", 7.5, filepath)
        # Assert
        with open(filepath) as f:
            items = json.load(f)
        assert items[0]["price"] == 7.5

    def test_update_price_negativo_lanza_valueerror(self, tmp_path):
        """new_price negativo debe lanzar ValueError."""
        filepath = str(tmp_path / "inv.json")
        with pytest.raises(ValueError, match="new_price debe ser mayor"):
            update_price("Martillo", -1.0, filepath)


class TestGetTotalValue:
    """Tests para get_total_value."""

    def test_inventario_vacio_devuelve_cero(self, mocker):
        """Con inventario vacío debe devolver 0.0."""
        mocker.patch("stockguard.storage.os.path.exists", return_value=False)
        assert get_total_value() == 0.0

    def test_calculo_correcto(self, tmp_path):
        """El valor total debe ser la suma de qty*price de cada ítem."""
        filepath = str(tmp_path / "inv.json")
        add_item("A", 10, 2.0, filepath)
        add_item("B", 5, 4.0, filepath)
        assert get_total_value(filepath) == pytest.approx(40.0)
