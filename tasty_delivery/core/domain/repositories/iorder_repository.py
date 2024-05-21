
from abc import abstractmethod

from tasty_delivery.core.domain.repositories.ibase_repository import IBaseRepository


class IOrderRepository(IBaseRepository):

    @abstractmethod
    def get_by_client(self, client_id):
        raise NotImplementedError

    @abstractmethod
    def update_status(self, _id, status):
        raise NotImplementedError
