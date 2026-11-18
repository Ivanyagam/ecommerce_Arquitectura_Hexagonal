import sqlite3
from typing import Optional

from app.application.ports.repositories import OrderRepository, ProductRepository
from app.domain.entities import Order, Product


class SqliteProductRepository(ProductRepository):
    def __init__(self, connection: sqlite3.Connection):
        self._db = connection

    def list_all(self) -> list[Product]:
        rows = self._db.execute("SELECT * FROM products ORDER BY id").fetchall()
        return [self._to_entity(row) for row in rows]

    def find_by_id(self, product_id: int) -> Optional[Product]:
        row = self._db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
        return self._to_entity(row) if row else None

    def save(self, product: Product) -> Product:
        if product.id is None:
            return self._insert(product)
        return self._update(product)

    def _insert(self, product: Product) -> Product:
        cursor = self._db.execute(
            "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
            (product.name, product.price, product.stock),
        )
        self._db.commit()
        product.id = cursor.lastrowid
        return product

    def _update(self, product: Product) -> Product:
        self._db.execute(
            "UPDATE products SET name = ?, price = ?, stock = ? WHERE id = ?",
            (product.name, product.price, product.stock, product.id),
        )
        self._db.commit()
        return product

    @staticmethod
    def _to_entity(row: sqlite3.Row) -> Product:
        return Product(id=row["id"], name=row["name"], price=row["price"], stock=row["stock"])


class SqliteOrderRepository(OrderRepository):
    def __init__(self, connection: sqlite3.Connection):
        self._db = connection

    def save(self, order: Order) -> Order:
        cursor = self._db.execute(
            "INSERT INTO orders (customer_email) VALUES (?)", (order.customer_email,)
        )
        order.id = cursor.lastrowid
        self._db.executemany(
            "INSERT INTO order_lines VALUES (?, ?, ?, ?, ?)",
            [(order.id, l.product_id, l.product_name, l.unit_price, l.quantity) for l in order.lines],
        )
        self._db.commit()
        return order
