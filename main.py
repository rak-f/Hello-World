"""Hello World — now with a real Firecrawl scrape.

Demonstrates a minimal-but-real Firecrawl integration: scrape a single page
and print its Markdown.

Usage:
    python main.py [URL]   # defaults to https://example.com
"""

import sys

from firecrawl import Firecrawl

import config


def scrape_page(url: str) -> str:
    """Scrape ``url`` with Firecrawl and return the page as Markdown."""
    firecrawl = Firecrawl(api_key=config.require_api_key())
    doc = firecrawl.scrape(url, formats=["markdown"])
    return doc.markdown or ""


def main() -> None:
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    print(f"Hello World! Scraping {url} with Firecrawl...\n")
    print(scrape_page(url))


if __name__ == "__main__":
    main()
