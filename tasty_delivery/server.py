from fastapi import FastAPI
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import PlainTextResponse
from pydantic import ValidationError

from adapter.api.controllers.order_controller import OrderController

from core.application.use_cases.order.order_case import OrderCase

from scripts.populate_database import populate


app = FastAPI(title="Tasty Delivery")


@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=422)


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=422)

# Orders
order_controller = OrderController(OrderCase)

app.include_router(order_controller.router)


@app.on_event("startup")
async def populate_database():
    populate()
