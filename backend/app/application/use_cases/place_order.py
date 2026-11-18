from dataclasses import dataclass

from app.application.ports.repositories import OrderRepository, ProductRepository
from app.domain.entities import Order, OrderLine, Product
from app.domain.errors import InvalidOrder, ProductNotFound


@dataclass(frozen=True)
class RequestedItem:
    product_id: int
    quantity: int


class PlaceOrder:
    """Caso de uso: crear un pedido y descontar el stock."""

    def __init__(self, products: ProductRepository, orders: OrderRepository):
        self._products = products
        self._orders = orders

    def execute(self, customer_email: str, items: list[RequestedItem]) -> Order:
        self._ensure_not_empty(items)
        order = Order(customer_email=customer_email)
        for item in items:
            product = self._find_product(item.product_id)
            self._reserve_and_add(order, product, item.quantity)
        return self._orders.save(order)

    @staticmethod
    def _ensure_not_empty(items: list[RequestedItem]) -> None:
        if not items:
            raise InvalidOrder("El pedido debe tener al menos un producto")

    def _find_product(self, product_id: int) -> Product:
        product = self._products.find_by_id(product_id)
        if product is None:
            raise ProductNotFound(product_id)
        return product

    def _reserve_and_add(self, order: Order, product: Product, quantity: int) -> None:
        product.reserve(quantity)
        self._products.save(product)
        order.add_line(OrderLine(product.id, product.name, product.price, quantity))
