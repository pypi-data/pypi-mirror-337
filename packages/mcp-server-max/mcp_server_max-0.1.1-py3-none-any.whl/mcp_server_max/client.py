import base64
import hashlib
import hmac
import json
import os
import time
from typing import Any
from typing import Literal
from urllib.parse import urljoin

import httpx
from loguru import logger


class MAXRestClient:
    def __init__(
        self,
        api_key: str | None = None,
        api_secret: str | None = None,
        base_url: str = "https://max-api.maicoin.com",
    ) -> None:
        if api_key is None:
            api_key = os.getenv("MAX_API_KEY", "")
        self.api_key = api_key

        if api_secret is None:
            api_secret = os.getenv("MAX_API_SECRET", "")
        self.api_secret = api_secret

        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
        }

    def auth(self, path: str, params: dict[str, Any]) -> None:
        logger.info("Authenticating request")
        params_to_sign = {**params, "path": path}
        json_str = json.dumps(params_to_sign)

        payload = base64.b64encode(json_str.encode()).decode()

        signature = hmac.new(
            self.api_secret.encode(),
            payload.encode(),
            hashlib.sha256,
        ).hexdigest()

        self.headers.update(
            {
                "X-MAX-ACCESSKEY": self.api_key,
                "X-MAX-PAYLOAD": payload,
                "X-MAX-SIGNATURE": signature,
            }
        )

    async def make_request(
        self,
        path: str,
        method: Literal["GET", "POST"] = "GET",
        params: dict[str, Any] | None = None,
    ):
        params = params or {}
        params["nonce"] = int(time.time() * 1000)

        if self.api_key and self.api_secret:
            self.auth(path, params=params)

        url = urljoin(self.base_url, path)
        async with httpx.AsyncClient() as client:
            if method == "GET":
                resp = await client.get(url, headers=self.headers, params=params)
                resp.raise_for_status()
            else:
                resp = await client.post(url=url, headers=self.headers, data=params)
                resp.raise_for_status()

        return resp.json()

    async def get_historical_index_prices(
        self, currency: str, limit: int | None = None, timestamp: int | None = None, order: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get latest historical index prices.

        Args:
            currency (str): The currency to get historical index prices for.
            limit (int, optional): Number of data points to return.
            timestamp (int, optional): Last timestamp to retrieve.
            order (str, optional): Sort order, asc or desc.

        Returns:
            list[dict[str, Any]]: A list of historical index prices.
        """
        params: dict[str, Any] = {"currency": currency}
        if limit is not None:
            params["limit"] = limit
        if timestamp is not None:
            params["timestamp"] = timestamp
        if order is not None:
            params["order"] = order

        return await self.make_request("/api/v3/wallet/m/historical_index_prices", params=params)

    async def get_limits(self) -> dict[str, float]:
        """
        Get total available loan amount.

        Returns:
            dict[str, float]: A dictionary containing currency as key and available loan amount as value.
        """
        response = await self.make_request("/api/v3/wallet/m/limits")
        return {k: float(v) for k, v in response.items()}

    async def get_interest_rates(self) -> dict[str, dict[str, float]]:
        """
        Get latest interest rates of m-wallet.

        Returns:
            dict[str, dict[str, float]]: A dictionary containing currency as key and interest rates as value.
        """
        response = await self.make_request("/api/v3/wallet/m/interest_rates")
        result = {}
        for currency, rates in response.items():
            result[currency] = {
                "hourly_interest_rate": float(rates["hourly_interest_rate"]),
                "next_hourly_interest_rate": float(rates["next_hourly_interest_rate"]),
            }
        return result

    async def get_currencies(self) -> list[dict[str, Any]]:
        """
        Get all available currencies.

        Returns:
            list[dict[str, Any]]: A list of available currencies.
        """
        return await self.make_request("/api/v3/currencies")

    async def get_timestamp(self) -> dict[str, int]:
        """
        Get server current time, in seconds since Unix epoch.

        Returns:
            dict[str, int]: A dictionary containing timestamp.
        """
        return await self.make_request("/api/v3/timestamp")

    async def get_k_line(
        self, market: str, period: int, limit: int | None = None, timestamp: int | None = None
    ) -> list[list[int | float]]:
        """
        Get OHLC(k line) of a specific market.

        Args:
            market (str): The market to get k-line for.
            period (int): Time period of K line in minutes. Supported values: 1, 5, 15, 30, 60, 120, 240, 360, 720, 1440, 4320, 10080.
            limit (int, optional): Number of data points to return.
            timestamp (int, optional): Last timestamp to retrieve.

        Returns:
            list[list[int | float]]: A list of k-line data. Each item is [timestamp, open, high, low, close, volume].
        """  # noqa: E501
        params = {"market": market, "period": period}
        if limit is not None:
            params["limit"] = limit
        if timestamp is not None:
            params["timestamp"] = timestamp

        return await self.make_request("/api/v3/k", params=params)

    async def get_depth(self, market: str, limit: int | None = None, timestamp: int | None = None) -> dict[str, Any]:
        """
        Get depth of a specified market.

        Args:
            market (str): The market to get depth for.
            limit (int, optional): Number of data points to return.
            timestamp (int, optional): Last timestamp to retrieve.

        Returns:
            dict[str, Any]: An object containing ask and bid orders, and timestamp.
        """
        params: dict[str, Any] = {"market": market}
        if limit is not None:
            params["limit"] = limit
        if timestamp is not None:
            params["timestamp"] = timestamp

        return await self.make_request("/api/v3/depth", params=params)

    async def get_public_trades(
        self,
        market: str,
        limit: int | None = None,
        timestamp: int | None = None,
        from_id: int | None = None,
        to_id: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get recent trades on market, sorted in reverse creation order.

        Args:
            market (str): The market to get trades for.
            limit (int, optional): Number of trades to return.
            timestamp (int, optional): Last timestamp to retrieve.
            from_id (int, optional): Trade id to begin from.
            to_id (int, optional): Trade id to end at.

        Returns:
            list[dict[str, Any]]: A list of public trade data.
        """
        params: dict[str, Any] = {"market": market}
        if limit is not None:
            params["limit"] = limit
        if timestamp is not None:
            params["timestamp"] = timestamp
        if from_id is not None:
            params["from"] = from_id
        if to_id is not None:
            params["to"] = to_id

        return await self.make_request("/api/v3/trades", params=params)
