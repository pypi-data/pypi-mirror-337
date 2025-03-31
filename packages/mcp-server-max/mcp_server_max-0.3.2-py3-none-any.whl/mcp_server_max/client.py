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


def raise_for_status(response: httpx.Response) -> None:
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        error_details = {
            "status_code": response.status_code,
            "url": str(response.url),
            "method": response.request.method,
            "response_text": response.text,
        }
        logger.error(f"HTTP request failed: {error_details}")
        raise httpx.HTTPStatusError(
            f"HTTP request failed with status code {response.status_code}: {response.text}",
            request=e.request,
            response=response,
        ) from e


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
        method: Literal["GET", "POST", "DELETE"] = "GET",
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
                raise_for_status(resp)
            elif method == "POST":
                resp = await client.post(url=url, headers=self.headers, json=params)
                raise_for_status(resp)
            elif method == "DELETE":
                resp = await client.delete(url=url, headers=self.headers, params=params)
                raise_for_status(resp)

            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
        return resp.json()
