"""Raíz de composición: único lugar donde se conectan puertos con adaptadores."""
from flask import Flask
from flask_cors import CORS

from app.application.use_cases.place_order import PlaceOrder
from app.application.use_cases.products import CreateProduct, ListProducts
from app.domain.entities import Product
from app.infrastructure.persistence.sqlite_db import connect
from app.infrastructure.persistence.sqlite_repositories import (
    SqliteOrderRepository, SqliteProductRepository)
from app.infrastructure.web.routes import build_blueprint

SEED = [Product("Teclado mecánico", 89.90, 15), Product("Mouse inalámbrico", 29.50, 40),
        Product("Monitor 24\"", 149.00, 8), Product("Audífonos USB", 45.00, 20)]


def create_app(db_path: str = "shop.db") -> Flask:
    connection = connect(db_path)
    products = SqliteProductRepository(connection)
    orders = SqliteOrderRepository(connection)
    _seed_if_empty(products)

    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(build_blueprint(
        ListProducts(products), CreateProduct(products), PlaceOrder(products, orders)))
    return app


def _seed_if_empty(products: SqliteProductRepository) -> None:
    if not products.list_all():
        for product in SEED:
            products.save(product)


if __name__ == "__main__":
    create_app().run(port=5001, debug=True)
