from app.application.ports.repositories import ProductRepository
from app.domain.entities import Product


class ListProducts:
    def __init__(self, products: ProductRepository):
        self._products = products

    def execute(self) -> list[Product]:
        return self._products.list_all()


class CreateProduct:
    def __init__(self, products: ProductRepository):
        self._products = products

    def execute(self, name: str, price: float, stock: int) -> Product:
        return self._products.save(Product(name=name, price=price, stock=stock))
