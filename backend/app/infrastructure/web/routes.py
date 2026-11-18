from dataclasses import asdict

from flask import Blueprint, jsonify, request

from app.application.use_cases.place_order import PlaceOrder, RequestedItem
from app.application.use_cases.products import CreateProduct, ListProducts
from app.domain.errors import DomainError, ProductNotFound


def build_blueprint(list_products: ListProducts, create_product: CreateProduct,
                    place_order: PlaceOrder) -> Blueprint:
    api = Blueprint("api", __name__, url_prefix="/api")

    @api.get("/products")
    def get_products():
        return jsonify([asdict(p) for p in list_products.execute()])

    @api.post("/products")
    def post_product():
        body = request.get_json()
        product = create_product.execute(body["name"], float(body["price"]), int(body["stock"]))
        return jsonify(asdict(product)), 201

    @api.post("/orders")
    def post_order():
        body = request.get_json()
        items = [RequestedItem(i["productId"], i["quantity"]) for i in body.get("items", [])]
        order = place_order.execute(body.get("email", ""), items)
        return jsonify({"id": order.id, "total": order.total}), 201

    @api.errorhandler(DomainError)
    def handle_domain_error(error: DomainError):
        status = 404 if isinstance(error, ProductNotFound) else 422
        return jsonify({"error": str(error)}), status

    return api
