
from typing import Annotated, List
from pydantic import Field

from tasty_delivery.core.domain.entities.base import Base


class ClientAuth(Base):
    name: str = Field()
    email: str = Field()
    username: str = Field(max_length=11)
    scopes: Annotated[List, str] = Field([])
