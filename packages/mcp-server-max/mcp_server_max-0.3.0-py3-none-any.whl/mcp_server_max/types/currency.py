from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator


class Network(BaseModel):
    token_contract_address: str | None = Field(default=None)
    precision: int | None = Field(default=None)
    id: str | None = Field(default=None)
    network_protocol: str | None = Field(default=None)
    deposit_confirmations: int | None = Field(default=None)
    withdrawal_fee: float | None = Field(default=None)
    min_withdrawal_amount: float | None = Field(default=None)
    withdrawal_enabled: bool | None = Field(default=None)
    deposit_enabled: bool | None = Field(default=None)
    need_memo: bool | None = Field(default=None)


class Staking(BaseModel):
    stake_flag: bool | None = Field(default=None)
    unstake_flag: bool | None = Field(default=None)


class Currency(BaseModel):
    currency: str = Field(..., description="Currency code, e.g., 'btc', 'eth'")
    type: str | None = Field(default=None)
    precision: int | None = Field(default=None)
    m_wallet_supported: bool | None = Field(default=None)
    m_wallet_mortgageable: bool | None = Field(default=None)
    m_wallet_borrowable: bool | None = Field(default=None)
    min_borrow_amount: float | None = Field(default=None)
    networks: list[Network] = Field(default_factory=list)
    staking: Staking | None = Field(default=None)

    @field_validator("min_borrow_amount", mode="before")
    @classmethod
    def convert_float(cls, value: str | float | None) -> float | None:
        if value is None:
            return None
        elif isinstance(value, float):
            return value
        elif value == "":
            return None
        else:
            return float(value)
