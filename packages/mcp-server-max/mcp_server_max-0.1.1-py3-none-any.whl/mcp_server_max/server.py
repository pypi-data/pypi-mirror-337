from mcp.server.fastmcp import FastMCP

from .exchange import MAXExchange

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
async def get_tickers() -> str:
    """Retrieve all available tickers on the MAX exchange."""
    tickers = await exchange.get_tickers()
    return "\n".join(str(ticker) for ticker in tickers.values())


@mcp.tool()
async def get_ticker(market: str) -> str:
    """Retrieve the ticker for a specific market symbol."""
    ticker = await exchange.get_ticker(market)
    return str(ticker)


def main():
    mcp.run()
