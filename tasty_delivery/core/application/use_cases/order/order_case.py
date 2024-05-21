

from sqlalchemy.exc import IntegrityError

from adapter.database.models.order import Order as OrderDB
from adapter.repositories.order_repository import OrderRepository
from core.application.use_cases.order.iorder_case import IOrderCase
from core.domain.entities.order import OrderIN, OrderOUT, OrderUpdate
from core.domain.exceptions.exception import DuplicateObject, ObjectNotFound, InvalidStatus
from core.domain.value_objects.order_status import OrderStatus
from logger import logger


class OrderCase(IOrderCase):
    RECEBIDO = OrderStatus.RECEBIDO.name
    EM_PREPARACAO = OrderStatus.EM_PREPARACAO.name
    PRONTO = OrderStatus.PRONTO.name
    FINALIZADO = OrderStatus.FINALIZADO.name
    AVAILABLE_STATUS = (RECEBIDO, EM_PREPARACAO, PRONTO, FINALIZADO)

    def __init__(self, db=None, current_user=None):
        self.repository = OrderRepository(db)
        self.session = db
        self.current_user = current_user

    def get_all(self):
        results = self.repository.get_all()
        saida = []

        for order in results:
            order_out = {
                "order_id": order.id,
                "discount": order.discount,
                "total": order.total,
                "status": order.status,
                "products": []
            }

            saida.append(
                OrderOUT(**order_out)
            )

        return saida

    def get_by_id(self, _id):
        result = self.repository.get_by_id(_id)
        if not result:
            msg = f"Pedido {_id} não encontrado."
            logger.warning(msg)
            raise ObjectNotFound(msg, 404)

        order_out = {
            "order_id": result.id,
            "discount": result.discount,
            "total": result.total,
            "status": result.status,
            "products": []
        }

        return OrderOUT(**order_out)

    def create(self, order: OrderIN) -> OrderOUT:
        try:
            orderdb = OrderDB(
                total=order.total,
                discount=order.discount,
                status=OrderCase.RECEBIDO,
            )

            result = self.repository.create(orderdb)

            return OrderOUT(
                order_id=result.id,
                discount=orderdb.discount,
                total=orderdb.total,
                status=orderdb.status,
                products=order.products
            )

        except IntegrityError as e:
            msg = "Pedido já existente criado na base de dados."
            logger.warning(msg)
            raise DuplicateObject(msg, 409)
        except Exception as e:
            raise e

    def update_status(self, _id, status: str) -> OrderOUT:
        new_status = status.upper()

        if new_status not in OrderCase.AVAILABLE_STATUS:
            raise InvalidStatus(status_code=400, msg=f"Status {status} não é valido.")

        result = self.repository.update_status(
            _id,
            {"status": new_status, "updated_by": "1"}
        )

        return OrderOUT(
            order_id=result.id,
            discount=result.discount,
            total=result.total,
            status=result.status,
            products=[]
        )

    def update(self, _id, new_values: OrderUpdate) -> OrderOUT:
        order = self.repository.update(_id, new_values.model_dump(exclude_unset=True))
        if order:
            return self.get_by_id(_id)
        else:
            raise ObjectNotFound(f"Pedido {_id} não encontrado.", 404)

    def delete(self, _id):
        self.repository.delete(_id, self.current_user)
