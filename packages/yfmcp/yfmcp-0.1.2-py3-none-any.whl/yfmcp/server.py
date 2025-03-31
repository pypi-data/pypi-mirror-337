from typing import Annotated

import yfinance as yf
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from yfinance.const import SECTOR_INDUSTY_MAPPING

from .types import Market

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


@mcp.tool()
def get_market(
    market: Annotated[Market, Field(description=f"The market to get, available markets are {', '.join(Market)}.")],
) -> str:
    m = yf.Market(market.value)
    return str(m.status) + "\n" + str(m.summary)


@mcp.tool()
def get_sector_industy_mapping() -> str:
    lines = []
    for k, v in SECTOR_INDUSTY_MAPPING.items():
        lines.append(f"{k}: {v}")
    return "\n".join(lines)


@mcp.tool()
def get_sector(
    sector: Annotated[
        str, Field(description="The sector to get, use get_sector_industy_mapping() to get available sectors.")
    ],
) -> str:
    s = yf.Sector(sector)
    return "\n\n".join(
        [
            f"<overview>\n{s.overview}\n</overview>",
            f"<top_companies>\n{s.top_companies}\n</top_companies>",
            f"<top_etfs>\n{s.top_etfs}\n</top_etfs>",
            f"<top_mutual_funds>\n{s.top_mutual_funds}\n</top_mutual_funds>",
            f"<research_reports>\n{s.research_reports}\n</research_reports>",
        ]
    )


@mcp.tool()
def get_industry(
    industry: Annotated[
        str, Field(description="The industry to get, use get_sector_industy_mapping() to get available industries.")
    ],
) -> str:
    i = yf.Industry(industry)
    return "\n\n".join(
        [
            f"<overview>\n{i.overview}\n</overview>",
            f"<top_growth_companies>\n{i.top_growth_companies}\n</top_growth_companies>",
            f"<top_companies>\n{i.top_companies}\n</top_companies>",
            f"<top_performing_companies>\n{i.top_performing_companies}\n</top_performing_companies>",
            f"<research_reports>\n{i.research_reports}\n</research_reports>",
        ]
    )


def main():
    mcp.run()
