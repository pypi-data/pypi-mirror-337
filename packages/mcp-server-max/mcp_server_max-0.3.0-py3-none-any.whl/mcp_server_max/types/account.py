from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator


class Account(BaseModel):
    currency: str | None = Field(default=None, description="Currency code, e.g., 'btc', 'eth'")
    balance: float | None = Field(default=None, description="Available balance")
    locked: float | None = Field(default=None, description="Locked balance")
    staked: float | None = Field(default=None, description="Staked balance, if applicable")

    @field_validator("balance", "locked", "staked", mode="before")
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
