from typing import Annotated
from typing import Final

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from mcp_server_max.exchange import MAXExchange
from mcp_server_max.types import OrderType
from mcp_server_max.types import Side
from mcp_server_max.types import WalletType

INSTRUCTIONS: Final[
    str
] = """This is the MAX Exchange trading interface. Use these tools to interact with cryptocurrency markets on the MAX exchange.

GENERAL WORKFLOW:
1. First, explore available markets with `get_markets()` and currencies with `get_currencies()`
2. Check account balances with `get_accounts()` before trading
3. For market information, use `get_tickers(markets=['symbol1', 'symbol2'])` with specific market symbols
4. When ready to trade, use `submit_order()` with proper parameters (always review confirmation before executing)
5. To monitor your open orders, use `get_open_orders()` to view pending trades
6. To cancel pending orders, use `cancel_orders()` with appropriate filters

IMPORTANT TRADING GUIDELINES:
- Always check account balances before placing orders
- Market symbols are typically in lowercase (e.g., 'btcusdt', 'ethusdt')
- For market orders, only specify volume (quantity) as price is determined by the market
- For limit orders, specify both price and volume
- The side parameter must be either 'buy' or 'sell'
- Double-check all parameters before confirming any order submission
- Consider starting with small test orders if uncertain

ORDER MANAGEMENT:
- Use `get_open_orders(wallet_type='spot', market='symbol')` to check your pending orders for a specific market
- Use `get_open_orders(wallet_type='spot')` to see all pending orders across markets
- Use `cancel_orders(wallet_type='spot', market='symbol', side='buy')` to cancel all buy orders for a specific market
- Use `cancel_orders(wallet_type='spot')` to cancel all pending orders across all markets (use with caution)

RISK WARNINGS:
- Cryptocurrency trading involves high risk
- Market orders execute immediately at current market prices
- The MAX exchange may have specific trading fees and rules
- Always verify order details carefully before confirmation
"""  # noqa: E501

# https://github.com/jlowin/fastmcp/issues/81#issuecomment-2714245145
mcp = FastMCP("MCP Server MAX", instructions=INSTRUCTIONS, log_level="ERROR")

exchange = MAXExchange()


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


@mcp.tool()
async def cancel_orders(
    wallet_type: Annotated[WalletType, Field(description="Wallet type, either 'spot' or 'm'")] = "spot",
    market: Annotated[str | None, Field(description="Market symbol, e.g., 'btcusdt'")] = None,
    side: Annotated[Side | None, Field(description="Order side, either 'buy' or 'sell'")] = None,
) -> str:
    """Cancel orders on the MAX exchange."""
    orders = await exchange.cancel_orders(
        wallet_type=wallet_type,
        market=market,
        side=side,
    )
    return "\n".join(str(order) for order in orders)


@mcp.tool()
async def get_open_orders(
    wallet_type: Annotated[WalletType, Field(description="Wallet type, either 'spot' or 'm'")] = "spot",
    market: Annotated[str | None, Field(description="Market symbol, e.g., 'btcusdt'")] = None,
) -> str:
    """Retrieve all open orders on the MAX exchange."""
    orders = await exchange.get_open_orders(wallet_type=wallet_type, market=market)
    return "\n".join(str(order) for order in orders)


def main():
    mcp.run()
