
from uuid import UUID

from sqlalchemy import ForeignKey, Integer, Column
from sqlalchemy.orm import Mapped, mapped_column

from tasty_delivery.adapter.database.db import Base


class OrderProductAssociation(Base):
    __tablename__ = "order_product_association"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), primary_key=True)
    product_id: Mapped[UUID] = mapped_column(primary_key=True)
    quantity: Mapped[Integer] = Column(Integer)
