"""Puertos de salida: lo que la aplicación necesita del mundo exterior."""
from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities import Order, Product


class ProductRepository(ABC):
    @abstractmethod
    def list_all(self) -> list[Product]: ...

    @abstractmethod
    def find_by_id(self, product_id: int) -> Optional[Product]: ...

    @abstractmethod
    def save(self, product: Product) -> Product: ...


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> Order: ...
