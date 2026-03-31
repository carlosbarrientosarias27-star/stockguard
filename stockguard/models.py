"""Módulo de modelos de datos para StockGuard.

Define la estructura de datos principal del inventario.
"""

from dataclasses import dataclass


@dataclass
class Item:
    """Representa un artículo del inventario.

    Args:
        name (str): Nombre del artículo.
        qty (int): Cantidad en stock. Debe ser mayor que 0.
        price (float): Precio unitario. Debe ser mayor que 0.

    Raises:
        ValueError: Si qty <= 0 o price <= 0.
        TypeError: Si qty no es int o price no es float/int.

    Example:
        >>> item = Item(name="Tornillo", qty=100, price=0.50)
        >>> item.name
        'Tornillo'
        >>> Item(name="Tuerca", qty=-1, price=1.0)
        Traceback (most recent call last):
            ...
        ValueError: qty debe ser mayor que 0, recibido: -1
    """

    name: str
    qty: int
    price: float

    def __post_init__(self) -> None:
        """Valida los campos tras la inicialización.

        Raises:
            ValueError: Si qty <= 0 o price <= 0.
            TypeError: Si qty no es int o price no es float/int.
        """
        if not isinstance(self.qty, int):
            raise TypeError(
                f"qty debe ser int, recibido: {type(self.qty).__name__}"
            )
        if not isinstance(self.price, (int, float)):
            raise TypeError(
                f"price debe ser float, recibido: {type(self.price).__name__}"
            )
        if self.qty <= 0:
            raise ValueError(
                f"qty debe ser mayor que 0, recibido: {self.qty}"
            )
        if self.price <= 0:
            raise ValueError(
                f"price debe ser mayor que 0, recibido: {self.price}"
            )