from ..http import HttpClient
from .schemas import CreateProductTokenRequest, ProductToken


class Product:
    """产品操作类."""

    def __init__(self, client: HttpClient) -> None:
        self.client = client

    async def create_token(self, request: CreateProductTokenRequest) -> ProductToken:
        """创建产品令牌.

        Args:
            request: 创建产品令牌请求

        Returns:
            ProductToken: 产品令牌

        """
        response = await self.client.post("/products/tokens", json=request.model_dump())
        return ProductToken(**response)


__all__ = ["Product", "CreateProductTokenRequest", "ProductToken"]
