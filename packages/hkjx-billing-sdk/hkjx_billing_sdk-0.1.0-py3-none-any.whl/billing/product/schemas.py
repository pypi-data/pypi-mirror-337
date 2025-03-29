from typing import Optional
from pydantic import BaseModel, Field


class CreateProductTokenRequest(BaseModel):
    """创建产品令牌请求

    Attributes:
        appid: 应用ID
        secret: 应用密钥
        expires: 令牌有效期(天)，默认1天
    """

    appid: str = Field(..., description="应用ID")
    secret: str = Field(..., description="应用密钥")



class ProductToken(BaseModel):
    """产品令牌

    Attributes:
        appid: 应用ID
        product_id: 产品ID
        created_at: 创建时间
        expires_at: 过期时间
    """

    appid: str = Field(..., description="应用ID")
    product_id: str = Field(..., description="产品ID")
    access_token: str = Field(..., description="访问令牌")
    created_at: str = Field(..., description="创建时间")
    expires_at: str = Field(..., description="过期时间")
