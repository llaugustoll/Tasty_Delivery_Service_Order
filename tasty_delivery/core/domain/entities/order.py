
from pydantic import BaseModel, Field

from tasty_delivery.core.domain.entities.base import Base


class OrderIN(BaseModel):
    products: List[Product] = Field()
    discount: float | None = Field(0, gte=0)
    total: float = Field(gte=0)


class OrderUpdate(BaseModel):
    products: List[Product] | None = Field()
    discount: float | None = Field(gte=0)
    total: float | None = Field(gte=0)
    status: str | None = Field(None)


class OrderOUT(Base):
    order_id: int = Field(..., alias="order_id")
    products: List[Product] | None = Field()
    discount: float | None = Field(gte=0)
    total: float | None = Field(gte=0)
    status: str | None = Field()
