from .http import HttpClient
from .product import Product
from .transaction import Transaction


class HkJingXiuBilling:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.http_client = HttpClient(base_url=base_url)
        self.product = Product(self.http_client)
        self.transaction = Transaction(self.http_client)


__all__ = ["HkJingXiuBilling"]
