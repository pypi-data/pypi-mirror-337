from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from mcp_server_max.exchange import MAXExchange
from mcp_server_max.types import OrderType
from mcp_server_max.types import Side
from mcp_server_max.types import WalletType

exchange = MAXExchange()

# https://github.com/jlowin/fastmcp/issues/81#issuecomment-2714245145
mcp = FastMCP("MCP Server MAX", log_level="ERROR")


@mcp.tool()
async def get_markets() -> str:
    """Retrieve all available markets on the MAX exchange."""
    markets = await exchange.get_markets()
    return "\n".join(str(market) for market in markets)


@mcp.tool()
async def get_currencies() -> str:
    """Retrieve all available currencies on the MAX exchange."""
    currencies = await exchange.get_currencies()
    return "\n".join(str(currency) for currency in currencies)


@mcp.tool()
async def get_tickers(
    markets: Annotated[list[str], Field(description="List of market symbols, e.g., ['btcusdt', 'ethusdt']")],
) -> str:
    """Retrieve tickers for specified markets on the MAX exchange."""
    tickers = await exchange.get_tickers()
    return "\n".join(str(tickers[market]) for market in markets if market in tickers)


@mcp.tool()
async def submit_order(
    market: Annotated[str, Field(description="Market symbol, e.g., 'btcusdt'")],
    side: Annotated[Side, Field(description="Order side, either 'buy' or 'sell'")],
    volume: Annotated[float, Field(description="Total amount to sell/buy, an order could be partially executed")],
    wallet_type: Annotated[WalletType, Field(description="Wallet type, either 'spot' or 'm'")] = "spot",
    price: Annotated[float | None, Field(description="Price of a unit")] = None,
    # client_oid: str | None = None,
    stop_price: Annotated[float | None, Field(description="price to trigger a stop order")] = None,
    order_type: OrderType = "market",
    # group_id: int | None = None,
) -> str:
    """Submit an order to the MAX exchange.

    A confirmation prompt will display all order details for user review and require explicit approval before execution.
    """
    order = await exchange.submit_order(
        market=market,
        side=side,
        volume=volume,
        wallet_type=wallet_type,
        price=price,
        # client_oid=client_oid,
        stop_price=stop_price,
        order_type=order_type,
        # group_id=group_id,
    )
    return str(order)


@mcp.tool()
async def get_accounts() -> str:
    """Retrieve all available accounts on the MAX exchange."""
    accounts = await exchange.get_accounts()
    return "\n".join(str(account) for account in accounts)


def main():
    mcp.run()
