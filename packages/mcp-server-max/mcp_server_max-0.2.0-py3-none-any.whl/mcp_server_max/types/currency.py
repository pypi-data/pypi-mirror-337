from pydantic import BaseModel
from pydantic import field_validator


class Network(BaseModel):
    token_contract_address: str | None
    precision: int
    id: str
    network_protocol: str
    deposit_confirmations: int
    withdrawal_fee: float
    min_withdrawal_amount: float
    withdrawal_enabled: bool
    deposit_enabled: bool
    need_memo: bool


class Staking(BaseModel):
    stake_flag: bool
    unstake_flag: bool


class Currency(BaseModel):
    currency: str
    type: str
    precision: int
    m_wallet_supported: bool
    m_wallet_mortgageable: bool
    m_wallet_borrowable: bool
    min_borrow_amount: float | None
    networks: list[Network]
    staking: Staking | None

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
