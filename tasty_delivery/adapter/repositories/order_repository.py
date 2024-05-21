
from typing import List

from sqlalchemy.exc import IntegrityError

from adapter.database.models.order import Order as OrderDb
from core.domain.repositories.iorder_repository import IOrderRepository


class OrderRepository(IOrderRepository):
    def __init__(self, db=None):
        self.db = db

    def get_all(self) -> List[OrderDb]:
        result = self.db.query(OrderDb).all()
        return result

    def get_by_id(self, _id) -> OrderDb:
        return self.db.query(OrderDb).filter(OrderDb.id == _id).scalar()

    def create(self, obj):
        try:
            self.db.add_all(obj)
            self.db.flush()
            # self.db.refresh(obj)
            self.db.commit()
        except IntegrityError as err:
            raise err
        except Exception as e:
            raise e
        return obj

    def update(self, _id, new_values):
        self.db.query(OrderDb).filter(OrderDb.id == _id).update(new_values)
        self.db.flush()
        self.db.commit()
        return self.get_by_id(_id)

    def delete(self, _id, status):
        order = self.db.query(OrderDb).filter(OrderDb.id == _id).scalar()
        if order:
            self.db.delete(order)
            self.db.commit()
        return None

    def get_by_client(self, client_id) -> List[OrderDb]:
        return self.db.query(OrderDb).filter(OrderDb.client_id == client_id).all()

    def update_status(self, _id, status):
        self.db.query(OrderDb).filter(OrderDb.id == _id).update(status)
        self.db.flush()
        self.db.commit()
        return self.get_by_id(_id)
