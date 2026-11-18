from dataclasses import dataclass, field
from typing import Optional

from .errors import InsufficientStock, InvalidOrder


@dataclass
class Product:
    name: str
    price: float
    stock: int
    id: Optional[int] = None

    def reserve(self, quantity: int) -> None:
        """Regla de negocio: descontar stock sólo si alcanza."""
        if quantity > self.stock:
            raise InsufficientStock(self.name, self.stock)
        self.stock -= quantity


@dataclass(frozen=True)
class OrderLine:
    product_id: int
    product_name: str
    unit_price: float
    quantity: int

    @property
    def subtotal(self) -> float:
        return round(self.unit_price * self.quantity, 2)


@dataclass
class Order:
    customer_email: str
    lines: list[OrderLine] = field(default_factory=list)
    id: Optional[int] = None

    def add_line(self, line: OrderLine) -> None:
        if line.quantity <= 0:
            raise InvalidOrder("La cantidad debe ser mayor que cero")
        self.lines.append(line)

    @property
    def total(self) -> float:
        return round(sum(line.subtotal for line in self.lines), 2)
