from typing import Annotated

import yfinance as yf
from mcp.server.fastmcp import FastMCP
from pydantic import Field

# https://github.com/jlowin/fastmcp/issues/81#issuecomment-2714245145
mcp = FastMCP("Yahoo Finance MCP Server", log_level="ERROR")


@mcp.tool()
def get_ticker_info(symbol: Annotated[str, Field(description="The stock symbol")]) -> str:
    ticker = yf.Ticker(symbol)
    return str(ticker.info)


@mcp.tool()
def get_ticker_news(symbol: Annotated[str, Field(description="The stock symbol")]) -> str:
    ticker = yf.Ticker(symbol)
    news = ticker.get_news()
    return str(news)


@mcp.tool()
def search_quote(
    query: Annotated[str, Field(description="The search query")],
    max_results: Annotated[int, Field(description="The maximum number of results")] = 8,
) -> str:
    search = yf.Search(query, max_results=max_results)
    return str(search.quotes)


@mcp.tool()
def search_news(
    query: Annotated[str, Field(description="The search query")],
    news_count: Annotated[int, Field(description="The number of news articles")] = 8,
) -> str:
    search = yf.Search(query, news_count=news_count)
    assert len(search.news) == news_count, f"Expected {news_count} news articles, but got {len(search.news)}"
    return str(search.news)


def main():
    mcp.run()
