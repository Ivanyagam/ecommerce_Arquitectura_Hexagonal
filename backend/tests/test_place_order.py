"""Se prueba el núcleo SIN Flask ni SQLite: gracias a los puertos usamos fakes en memoria."""
import pytest

from app.application.ports.repositories import OrderRepository, ProductRepository
from app.application.use_cases.place_order import PlaceOrder, RequestedItem
from app.domain.entities import Product
from app.domain.errors import InsufficientStock, InvalidOrder, ProductNotFound


class InMemoryProducts(ProductRepository):
    def __init__(self, *products):
        self._data = {p.id: p for p in products}

    def list_all(self): return list(self._data.values())
    def find_by_id(self, product_id): return self._data.get(product_id)
    def save(self, product): self._data[product.id] = product; return product


class InMemoryOrders(OrderRepository):
    def save(self, order): order.id = 1; return order


@pytest.fixture
def products():
    return InMemoryProducts(Product("Teclado", 10.0, 5, id=1), Product("Mouse", 4.5, 2, id=2))


@pytest.fixture
def place_order(products):
    return PlaceOrder(products, InMemoryOrders())


def test_calcula_el_total_y_descuenta_stock(place_order, products):
    order = place_order.execute("a@b.co", [RequestedItem(1, 2), RequestedItem(2, 1)])
    assert order.total == 24.5
    assert products.find_by_id(1).stock == 3


def test_falla_si_no_hay_stock(place_order):
    with pytest.raises(InsufficientStock):
        place_order.execute("a@b.co", [RequestedItem(2, 3)])


def test_falla_si_el_producto_no_existe(place_order):
    with pytest.raises(ProductNotFound):
        place_order.execute("a@b.co", [RequestedItem(99, 1)])


def test_falla_si_el_pedido_esta_vacio(place_order):
    with pytest.raises(InvalidOrder):
        place_order.execute("a@b.co", [])
