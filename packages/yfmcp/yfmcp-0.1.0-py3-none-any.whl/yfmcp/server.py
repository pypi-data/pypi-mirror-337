from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field
import yfinance as yf

# https://github.com/jlowin/fastmcp/issues/81#issuecomment-2714245145
mcp = FastMCP("Yahoo Finance MCP Server", log_level="ERROR")



@mcp.tool()
def get_ticker_info(symbol: Annotated[str, Field(description="The stock symbol")]) -> str:
    ticker =yf.Ticker(symbol)
    return str(ticker.info)
    
@mcp.tool()
def get_ticker_news(symbol: Annotated[str, Field(description="The stock symbol")]) -> str:
    ticker = yf.Ticker(symbol)
    news = ticker.get_news()
    return str(news)
    
def main():
    mcp.run()
