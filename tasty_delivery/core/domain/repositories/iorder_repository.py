
from abc import abstractmethod

from core.domain.repositories.ibase_repository import IBaseRepository


class IOrderRepository(IBaseRepository):

    @abstractmethod
    def update_status(self, _id, status):
        raise NotImplementedError
