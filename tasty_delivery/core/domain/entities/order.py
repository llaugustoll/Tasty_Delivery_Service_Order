
from typing import List
from uuid import UUID
from pydantic import BaseModel, Field

from core.domain.entities.base import Base


class OrderIN(BaseModel):
    products: List[int] = Field(default=list())
    discount: float | None = Field(0, gte=0)
    total: float = Field(gte=0)


class OrderUpdate(BaseModel):
    products: List[int] | None = Field()
    discount: float | None = Field(gte=0)
    total: float | None = Field(gte=0)
    status: str | None = Field(None)


class OrderOUT(Base):
    order_id: int = Field(..., alias="order_id")
    client_id: str | None = Field()
    products: List[int] | None = Field()
    discount: float | None = Field(gte=0)
    total: float | None = Field(gte=0)
    status: str | None = Field()
