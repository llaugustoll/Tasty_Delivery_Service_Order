from abc import abstractmethod

from core.application.use_cases.ibase_use_case import IBaseUseCase


class IOrderCase(IBaseUseCase):
    @abstractmethod
    def update_status(self, _id: int, status: str):
        raise NotImplementedError
