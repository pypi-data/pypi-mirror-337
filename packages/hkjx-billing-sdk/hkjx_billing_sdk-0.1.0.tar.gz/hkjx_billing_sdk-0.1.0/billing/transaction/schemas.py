from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class TransactionType(str, Enum):
    """交易类型"""

    USER_RECHARGE = "user_recharge"
    """用户充值"""
    MODEL_TOKEN_CONSUMPTION = "model_token_consumption"
    """模型令牌消耗"""


class TransactionResponse(BaseModel):
    """交易响应"""

    id: str = Field(description="交易ID")


class CreateTransactionPayloads(BaseModel):
    """创建交易"""

    type: TransactionType = Field(description="交易类型")
    source_type: str | None = Field(
        default=None,
        description="交易源类型",
    )
    source_id: str | None = Field(
        default=None,
        description="交易源ID",
    )
    target_type: str | None = Field(
        default=None,
        description="目标对象类型",
    )
    target_id: str | None = Field(
        default=None,
        description="目标对象ID",
    )
    amount: float = Field(description="交易金额")
    currency: Literal["CNY", "USD"] = Field(
        default="CNY",
        description="货币单位，默认是人民币",
    )
