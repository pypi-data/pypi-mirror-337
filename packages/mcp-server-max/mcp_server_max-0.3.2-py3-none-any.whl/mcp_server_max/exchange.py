from __future__ import annotations

from datetime import datetime
from typing import Any
from typing import Literal

from .client import MAXRestClient
from .types import Account
from .types import Currency
from .types import Market
from .types import Order
from .types import OrderType
from .types import Side
from .types import Ticker
from .types import WalletType


class MAXExchange:
    def __init__(self) -> None:
        self.client = MAXRestClient()

        self._markets: dict[str, Market] = {}
        self._currencies: dict[str, Currency] = {}

    async def initialize(self) -> MAXExchange:
        if not self._markets:
            markets = await self.get_markets()
            self._markets = {m.id: m for m in markets}

        if not self._currencies:
            currencies = await self.get_currencies()
            self._currencies = {c.currency: c for c in currencies}

        return self

    async def get_markets(self) -> list[Market]:
        """
        Get all available markets.

        Returns:
            list[Market]: A list of available markets.
        """
        data = await self.client.make_request("/api/v3/markets")
        return [Market.model_validate(d) for d in data]

    async def get_currencies(self) -> list[Currency]:
        """Get all available currencies

        Returns:
            list[Currency]: A list of available currencies.
        """
        data = await self.client.make_request("/api/v3/currencies")
        return [Currency.model_validate(d) for d in data]

    async def get_index_price(self, symbol: str) -> float:
        data = await self.get_all_index_prices()
        return data[symbol]

    async def get_all_index_prices(self) -> dict[str, float]:
        """Get latest index prices of m-wallet

        Returns:
            dict[str, float]: A dictionary containing market id(symbol) as key and index price as value.
        """
        resp = await self.client.make_request("/api/v3/wallet/m/index_prices")
        return {k: float(v) for k, v in resp.items()}

    async def get_tickers(self) -> dict[str, Ticker]:
        """Get latest tickers of all markets

        Returns:
            dict[str, Ticker]: A dictionary containing market id(symbol) as key and Ticker object as value.
        """
        resp = await self.client.make_request("/api/v2/tickers")
        return {k: Ticker.model_validate(v | {"market": k}) for k, v in resp.items()}

    async def get_ticker(self, market: str) -> Ticker:
        """Get latest ticker of a specific market

        Args:
            market (str): The market symbol to get the ticker for.
        Returns:
            Ticker: The latest ticker of the specified market.
        """
        resp = await self.client.make_request("/api/v3/ticker", params={"market": market})
        return Ticker.model_validate(resp | {"market": market})

    async def get_open_orders(
        self,
        wallet_type: WalletType = "spot",
        market: str | None = None,
        dt: datetime | None = None,  # timestamp
        order_by: Literal["asc", "desc", "asc_updated_at", "desc_updated_at"] = "desc",
        limit: int = 50,  # 1~1000
    ) -> list[Order]:
        if limit < 1 or limit > 1000:
            raise ValueError("limit must be between 1 and 1000")

        params: dict[str, Any] = {}
        if market is not None:
            params["market"] = market

        if dt is not None:
            params["dt"] = int(dt.timestamp() * 1000)

        if order_by is not None:
            params["order_by"] = order_by

        resp = await self.client.make_request(f"/api/v3/wallet/{wallet_type}/orders/open", method="GET", params=params)
        return [Order.model_validate(d) for d in resp]

    async def get_closed_orders(
        self,
        wallet_type: WalletType = "spot",
        market: str | None = None,
        dt: datetime | None = None,  # timestamp
        order_by: Literal["asc", "desc", "asc_updated_at", "desc_updated_at"] = "desc",
        limit: int = 50,  # 1~1000
    ) -> list[Order]:
        if limit < 1 or limit > 1000:
            raise ValueError("limit must be between 1 and 1000")

        params: dict[str, Any] = {}
        if market is not None:
            params["market"] = market

        if dt is not None:
            params["dt"] = int(dt.timestamp() * 1000)

        if order_by is not None:
            params["order_by"] = order_by

        resp = await self.client.make_request(
            f"/api/v3/wallet/{wallet_type}/orders/closed", method="GET", params=params
        )
        return [Order.model_validate(d) for d in resp]

    async def submit_order(
        self,
        market: str,
        side: Side,
        volume: float,
        wallet_type: WalletType = "spot",
        price: float | None = None,
        client_oid: str | None = None,
        stop_price: float | None = None,
        order_type: OrderType = "market",
        group_id: int | None = None,
    ) -> Order:
        params: dict[str, Any] = {
            "market": market,
            "side": side,
            "volume": str(volume),
        }

        if price is not None:
            params["price"] = str(price)

        if client_oid is not None:
            params["client_oid"] = client_oid
        if stop_price is not None:
            params["stop_price"] = str(stop_price)

        if order_type is not None:
            params["ord_type"] = order_type

        if group_id is not None:
            params["group_id"] = group_id

        resp = await self.client.make_request(f"/api/v3/wallet/{wallet_type}/order", method="POST", params=params)
        return Order.model_validate(resp)

    async def cancel_orders(
        self,
        wallet_type: WalletType = "spot",
        market: str | None = None,
        side: Side | None = None,
        group_id: int | None = None,
    ) -> list[dict[str, str | Order]]:
        params: dict[str, Any] = {}
        if market is not None:
            params["market"] = market

        if side is not None:
            params["side"] = side

        if group_id is not None:
            params["group_id"] = group_id

        resp = await self.client.make_request(f"/api/v3/wallet/{wallet_type}/orders", method="DELETE", params=params)

        return [{"error": d["error"], "order": Order.model_validate(d["order"])} for d in resp]

    async def cancel_order(self, order_id: int | None = None, client_oid: str | None = None) -> dict[str, bool]:
        params: dict[str, int | str] = {}
        if order_id is not None:
            params["id"] = order_id

        if client_oid is not None:
            params["client_oid"] = client_oid

        resp = await self.client.make_request("/api/v3/order", method="DELETE", params=params)
        return resp

    async def get_accounts(self, wallet_type: WalletType = "spot", currency: str | None = None) -> list[Account]:
        params = {}
        if currency is not None:
            if currency not in self._currencies:
                raise ValueError(f"Invalid currency: {currency}")
            params["currency"] = currency

        resp = await self.client.make_request(f"/api/v3/wallet/{wallet_type}/accounts", method="GET", params=params)
        return [Account.model_validate(d) for d in resp]
