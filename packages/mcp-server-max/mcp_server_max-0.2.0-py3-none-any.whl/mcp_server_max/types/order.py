from datetime import datetime
from typing import Literal

from pydantic import BaseModel
from pydantic import field_validator

Side = Literal["buy", "sell"]
OrderType = Literal["market", "limit", "stop_market", "stop_limit", "post_only", "ioc_limit"]
OrderStatus = Literal["wait", "done", "cancel", "convert"]

WalletType = Literal["spot", "m"]


class Order(BaseModel):
    id: int
    wallet_type: str
    market: str
    client_oid: str | None
    group_id: int | None
    side: Side
    state: OrderStatus
    ord_type: OrderType
    price: float | None
    stop_price: float | None
    avg_price: float | None
    volume: float | None
    remaining_volume: float | None
    executed_volume: float | None
    trades_count: int | None
    created_at: datetime | None
    updated_at: datetime | None

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

        if isinstance(value, str):
            return float(value)

        return value
