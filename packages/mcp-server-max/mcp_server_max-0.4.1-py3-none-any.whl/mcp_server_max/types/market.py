from pydantic import BaseModel
from pydantic import Field


class Market(BaseModel):
    id: str = Field(..., description="unique market id")
    status: str | None = Field(default=None, description="market status")
    base_unit: str | None = Field(default=None, description="base unit")
    base_unit_precision: int | None = Field(default=None, description="fixed precision of base unit")
    min_base_amount: float | None = Field(default=None, description="minimum of base amount")
    quote_unit: str | None = Field(default=None, description="quote unit")
    quote_unit_precision: int | None = Field(default=None, description="fixed precision of quote unit")
    min_quote_amount: float | None = Field(default=None, description="minimum of quote amount")
    m_wallet_supported: bool | None = Field(default=None, description="m-wallet supported")
