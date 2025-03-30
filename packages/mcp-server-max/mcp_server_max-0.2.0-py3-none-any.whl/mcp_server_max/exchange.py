from .client import MAXRestClient
from .types import Currency
from .types import Market
from .types import Ticker
from .types.order import Order
from .types.order import OrderType
from .types.order import Side
from .types.order import WalletType


class MAXExchange:
    def __init__(self) -> None:
        self.client = MAXRestClient()

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
            list[Ticker]: A list of latest tickers.
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
        # https://max-api.maicoin.com/api/v3/wallet/{path_wallet_type}/order

        params = {
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

        print(params)
        resp = await self.client.make_request(f"/api/v3/wallet/{wallet_type}/order", method="POST", params=params)
        return Order.model_validate(resp)
