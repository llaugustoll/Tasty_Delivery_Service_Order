
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from tasty_delivery.adapter.database.db import get_db
from tasty_delivery.core.application.use_cases.order.order_case import OrderCase
from tasty_delivery.core.domain.entities.order import OrderOUT, OrderIN, OrderUpdate
from tasty_delivery.core.domain.exceptions.exception_schema import ObjectNotFound, ObjectDuplicated


class OrderController:
    def __init__(self, order_case: OrderCase = None):
        self.router = APIRouter(tags=["Orders"], prefix="/orders")
        self.router.add_api_route(
            path="/",
            endpoint=self.orders,
            methods=["GET"],
            response_model=List[OrderOUT],
            status_code=200,
            response_model_exclude_none=True
        )
        self.router.add_api_route(
            path="/{id}",
            endpoint=self.order_by_id,
            methods=["GET"],
            response_model=OrderOUT,
            responses={
                200: {"model": OrderOUT},
                404: {"model": ObjectNotFound},
                409: {"model": ObjectDuplicated}
            },
            status_code=200,
            response_model_exclude_none=True
        )
        self.router.add_api_route(
            path="/",
            endpoint=self.create,
            methods=["POST"],
            response_model=OrderOUT,
            response_model_by_alias=True,
            responses={
                201: {"model": OrderOUT},
                409: {"model": ObjectDuplicated}
            },
            status_code=201,
            response_model_exclude_none=True
        )
        self.router.add_api_route(
            path="/{id}",
            endpoint=self.update,
            methods=["PUT"],
            response_model=OrderOUT,
            responses={
                200: {"model": OrderOUT},
                404: {"model": ObjectNotFound},
                409: {"model": ObjectDuplicated}
            },
            status_code=200,
            response_model_exclude_none=True
        )
        self.router.add_api_route(
            path="/{id}",
            endpoint=self.delete,
            methods=["DELETE"],
            response_model=None,
            responses={
                204: {"model": None},
                404: {"model": ObjectNotFound},
                409: {"model": ObjectDuplicated}
            },
            status_code=204,
            response_model_exclude_none=True
        )
        self.router.add_api_route(
            path="/status/{id}",
            endpoint=self.update_status,
            methods=["PUT"],
            response_model=OrderOUT,
            responses={
                200: {"model": OrderOUT},
                404: {"model": ObjectNotFound},
                409: {"model": ObjectDuplicated}
            },
            status_code=200,
            response_model_exclude_none=True
        )
        self.router.add_api_route(
            path="/client/{id}",
            endpoint=self.order_by_client,
            methods=["GET"],
            response_model=List[OrderOUT],
            responses={
                200: {"model": List[OrderOUT]},
                404: {"model": ObjectNotFound},
                409: {"model": ObjectDuplicated}
            },
            status_code=200,
            response_model_exclude_none=True
        )

        self._order_case = order_case

    async def orders(self, db=Depends(get_db)):
        """
        Lista todos os pedidos
        """
        return self._order_case(db).get_all()

    async def order_by_id(self, _id: int, db=Depends(get_db)):
        """
        Lista pedidos por {id}
        """
        return self._order_case(db).get_by_id(_id)

    async def order_by_client(self, client_id: UUID, db=Depends(get_db)):
        """
        Lista pedidos por {client_id}
        """
        return self._order_case(db).get_by_client(client_id)

    async def create(self, order: OrderIN, db=Depends(get_db)):
        """
        Cria um pedido
        """
        return self._order_case(db).create(order)

    async def update(self, _id: int, order_update: OrderUpdate, db=Depends(get_db)):
        """
        Atualiza um pedido
        * Necessário permissionamento de usuário
        """
        return await self._order_case(db).update(_id, order_update)

    async def delete(self, _id: int, db=Depends(get_db)):
        """
        Deleta um pedido
        * Necessário permissionamento de usuário
        """
        return self._order_case(db).delete(_id)

    async def update_status(self, _id: int, status: str, db=Depends(get_db)):
        """
        Atualiza status de um pedido
        * Necessário permissionamento de usuário
        """
        return self._order_case(db=db).update_status(_id, status)
