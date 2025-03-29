from .client import MAXRestClient
from .types import Currency
from .types import Market
from .types import Ticker


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
