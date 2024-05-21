

from sqlalchemy.exc import IntegrityError

from adapter.database.models.order import Order as OrderDB
from adapter.database.models.order_product_association import OrderProductAssociation
from adapter.repositories.order_repository import OrderRepository
from core.application.use_cases.order.iorder_case import IOrderCase
from core.domain.entities.order import OrderIN, OrderOUT, OrderUpdate, Product
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
            products_out = []

            order_out = {
                "order_id": order.id,
                "client_id": order.client_id,
                "discount": order.discount,
                "total": order.total,
                "status": order.status
            }

            for product in order.products:
                products_out.append({
                    "product_id": product.id,
                    "price": product.price,
                    "quantity": product.order_association[0].quantity,
                    "obs": product.order_association[0].obs,
                })

            saida.append(
                OrderOUT(**order_out, products=products_out)
            )

        return saida

    def get_by_id(self, _id):
        result = self.repository.get_by_id(_id)
        if not result:
            msg = f"Pedido {_id} não encontrado."
            logger.warning(msg)
            raise ObjectNotFound(msg, 404)

        products_out = []

        order_out = {
            "order_id": result.id,
            "client_id": result.client_id,
            "discount": result.discount,
            "total": result.total,
            "status": result.status
        }

        for product in result.products:
            products_out.append({
                "product_id": product.id,
                "price": product.price,
                "quantity": product.order_association[0].quantity,
                "obs": product.order_association[0].obs,
            })

        return OrderOUT(**order_out, products=products_out)

    def create(self, order: OrderIN) -> OrderOUT:
        associations = []
        client_id = self.current_user.id if self.current_user else None
        try:
            orderdb = OrderDB(
                total=order.total,
                discount=order.discount,
                status=OrderCase.RECEBIDO,
                client_id=client_id,
            )

            for product in order.products:
                association = OrderProductAssociation(
                    order=orderdb,
                    product=product.product_id,
                    quantity=product.quantity,
                )
                associations.append(association)

            result = self.repository.create(associations)

            return OrderOUT(
                order_id=result[0].order_id,
                client_id=orderdb.client_id,
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

        client_id = self.current_user.id if self.current_user else None

        if new_status not in OrderCase.AVAILABLE_STATUS:
            raise InvalidStatus(status_code=400, msg=f"Status {status} não é valido.")

        result = self.repository.update_status(
            _id,
            {"status": new_status, "updated_by": client_id.id}
        )

        return OrderOUT(
            order_id=result.id,
            client_id=result.client_id,
            discount=result.discount,
            total=result.total,
            status=result.status,
            products=[
                Product(
                    product_id=product.id,
                    quantity=product.order_association[0].quantity,
                ) for product in result.products
            ]
        )

    def update(self, _id, new_values: OrderUpdate) -> OrderOUT:
        order = self.repository.update(_id, new_values.model_dump(exclude_unset=True))
        if order:
            return self.get_by_id(_id)
        else:
            raise ObjectNotFound(f"Pedido {_id} não encontrado.", 404)

    def delete(self, _id):
        self.repository.delete(_id, self.current_user)
