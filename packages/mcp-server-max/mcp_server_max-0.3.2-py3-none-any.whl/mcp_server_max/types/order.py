from datetime import datetime
from typing import Literal

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator

Side = Literal["buy", "sell"]
OrderType = Literal["market", "limit", "stop_market", "stop_limit", "post_only", "ioc_limit"]
OrderStatus = Literal["wait", "done", "cancel", "convert"]
WalletType = Literal["spot", "m"]


class Order(BaseModel):
    id: int | None = Field(default=None)
    wallet_type: str | None = Field(default=None)
    market: str | None = Field(default=None)
    client_oid: str | None = Field(default=None)
    group_id: int | None = Field(default=None)
    side: Side | None = Field(default=None)
    state: OrderStatus | None = Field(default=None)
    ord_type: OrderType | None = Field(default=None)
    price: float | None = Field(default=None)
    stop_price: float | None = Field(default=None)
    avg_price: float | None = Field(default=None)
    volume: float | None = Field(default=None)
    remaining_volume: float | None = Field(default=None)
    executed_volume: float | None = Field(default=None)
    trades_count: int | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)

    @field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def convert_datetime(cls, value: int | None) -> datetime | None:
        if value is None:
            return None

        print(value)
        return datetime.fromtimestamp(int(value / 1000))

    @field_validator("price", "stop_price", "avg_price", "remaining_volume", "executed_volume", mode="before")
    @classmethod
    def convert_float(cls, value: str | float | None) -> float | None:
        if value is None:
            return None
        elif isinstance(value, float):
            return value
        elif isinstance(value, str):
            return float(value)
        else:
            raise TypeError(f"Invalid type for value: {value}")
