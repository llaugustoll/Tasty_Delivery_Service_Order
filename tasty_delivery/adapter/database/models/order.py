from datetime import datetime

from sqlalchemy import Column, String, Float, Boolean, TIMESTAMP, Integer

from adapter.database.db import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    total = Column(Float)
    discount = Column(Float)
    status = Column(String)

    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)
