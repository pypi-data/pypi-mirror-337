from ..http import HttpClient
from .schemas import CreateTransactionPayloads, TransactionResponse, TransactionType


class Transaction:
    """交易操作类."""

    def __init__(self, client: HttpClient) -> None:
        self.client = client

    async def create(
        self,
        payload: CreateTransactionPayloads,
        access_token: str,
    ) -> TransactionResponse:
        """创建交易.

        Args:
            payload: 交易创建参数

        Returns:
            TransactionResponse: 交易响应数据

        """
        response = await self.client.post(
            "/transactions",
            json=payload.model_dump(),
            headers={"access-token": access_token},
        )
        return TransactionResponse(**response)


__all__ = [
    "CreateTransactionPayloads",
    "Transaction",
    "TransactionType",
    "TransactionResponse",
]
