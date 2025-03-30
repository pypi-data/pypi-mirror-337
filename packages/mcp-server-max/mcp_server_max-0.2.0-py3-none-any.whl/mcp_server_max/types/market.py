from pydantic import BaseModel
from pydantic import Field


class Market(BaseModel):
    id: str = Field(..., description="unique market id")
    status: str = Field(..., description="market status")
    base_unit: str = Field(..., description="base unit")
    base_unit_precision: int = Field(..., description="fixed precision of base unit")
    min_base_amount: float = Field(..., description="minimum of base amount")
    quote_unit: str = Field(..., description="quote unit")
    quote_unit_precision: int = Field(..., description="fixed precision of quote unit")
    min_quote_amount: float = Field(..., description="minimum of quote amount")
    m_wallet_supported: bool = Field(..., description="m-wallet supported")
