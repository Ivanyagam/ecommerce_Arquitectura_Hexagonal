class DomainError(Exception):
    """Base de los errores de negocio."""


class ProductNotFound(DomainError):
    def __init__(self, product_id: int):
        super().__init__(f"El producto {product_id} no existe")


class InsufficientStock(DomainError):
    def __init__(self, product_name: str, available: int):
        super().__init__(f"Stock insuficiente de '{product_name}': quedan {available}")


class InvalidOrder(DomainError):
    pass
