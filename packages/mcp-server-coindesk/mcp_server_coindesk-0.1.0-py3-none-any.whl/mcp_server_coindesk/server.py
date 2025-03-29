from typing import Final

import feedparser
from mcp.server.fastmcp import FastMCP

from mcp_server_coindesk.page import extract_newspage
from mcp_server_coindesk.utils import fetch_text_from_url

COINDESK_RSS_URL: Final[str] = "https://www.coindesk.com/arc/outboundfeeds/rss"


INSTRUCTIONS: Final[str] = """
This MCP server provides access to CoinDesk cryptocurrency and blockchain news content.

Available tools:
- recent_news: Fetches the latest news articles from CoinDesk's RSS feed
- read_news: Retrieves the full content of a specific news article using its URL

Usage guidelines:
1. Use recent_news to obtain recent headlines, links, timestamps, and article summaries
2. Use read_news with an article URL to fetch the complete article content
3. Process and present the news data according to your application requirements

Data handling:
- The RSS feed data includes article titles, links, publication timestamps, and summaries
- Full article content may contain text, embedded media references, and formatting elements
- Citation is recommended when republishing any content, referencing CoinDesk as the source

Rate limits and performance considerations:
- Implement appropriate caching mechanisms for frequently accessed content
- Avoid excessive requests to the underlying CoinDesk services
"""


mcp = FastMCP("MCP Server Coindesk", instructions=INSTRUCTIONS, log_level="ERROR")


@mcp.tool()
async def read_news(url: str) -> str:
    """
    Retrieves and extracts the full content of a specific news article from CoinDesk.

    Fetches the HTML content from the provided URL, processes it to extract
    structured news information including title, subtitle, author, publication date,
    and article content.

    Args:
        url (str): The complete URL of the CoinDesk news article to retrieve

    Returns:
        str: A formatted string containing the article's title, subtitle, author,
             publication information, and content preview

    Raises:
        HTTPStatusError: If the URL request fails
        Exception: If article parsing encounters errors
    """
    html = await fetch_text_from_url(url)
    newspage = extract_newspage(html)
    return str(newspage)


@mcp.tool()
async def recent_news() -> str:
    """
    Retrieves the latest cryptocurrency and blockchain news articles from CoinDesk's RSS feed.

    Fetches the current RSS feed from CoinDesk, parses it to extract information about
    recent articles, and returns a formatted list of news items including titles,
    links, publication timestamps, and summary content.

    Returns:
        str: A formatted string containing multiple news entries separated by '---',
             with each entry showing title, URL, publication time, and summary

    Raises:
        HTTPStatusError: If the RSS feed request fails
        Exception: If RSS parsing encounters errors
    """
    text = await fetch_text_from_url(COINDESK_RSS_URL)
    feed = feedparser.parse(text)
    return "\n---\n".join(
        f"{entry['title']}\n{entry['link']}\n{entry['updated']}\n{entry['summary']}" for entry in feed["entries"]
    )


def main() -> None:
    mcp.run()
