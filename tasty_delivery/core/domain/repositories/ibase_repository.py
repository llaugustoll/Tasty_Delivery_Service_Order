from abc import abstractmethod, ABC


class IBaseRepository(ABC):

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, _id):
        raise NotImplementedError

    @abstractmethod
    def create(self, obj):
        raise NotImplementedError

    @abstractmethod
    def update(self, _id, new_values):
        raise NotImplementedError

    @abstractmethod
    def delete(self, _id, current_user):
        raise NotImplementedError
