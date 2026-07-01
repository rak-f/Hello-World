#!/usr/bin/env python3
"""Hello World for Firecrawl.

A tiny, self-contained example that turns any web page into clean Markdown
using the Firecrawl API (https://docs.firecrawl.dev).

Usage:
    export FIRECRAWL_API_KEY=fc-...          # get a key at https://firecrawl.dev
    python hello_firecrawl.py                # scrape this repo's GitHub page
    python hello_firecrawl.py scrape https://example.com
    python hello_firecrawl.py search "Hello World site:github.com"
"""

import argparse
import os
import sys

from firecrawl import Firecrawl

# The canonical "Hello World" page — this very repository on GitHub.
DEFAULT_URL = "https://github.com/octocat/Hello-World"


def get_client() -> Firecrawl:
    """Build a Firecrawl client from the FIRECRAWL_API_KEY environment variable."""
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        sys.exit(
            "FIRECRAWL_API_KEY is not set. Grab a free key at https://firecrawl.dev "
            "and `export FIRECRAWL_API_KEY=fc-...` (see .env.example)."
        )
    return Firecrawl(api_key=api_key)


def scrape(url: str) -> None:
    """Scrape a single URL and print its Markdown content."""
    firecrawl = get_client()
    doc = firecrawl.scrape(url, formats=["markdown"])
    markdown = doc.markdown or ""
    print(f"# Scraped {url} ({len(markdown)} chars of Markdown)\n")
    print(markdown)


def search(query: str, limit: int) -> None:
    """Search the web and print the top results."""
    firecrawl = get_client()
    results = firecrawl.search(query, limit=limit)
    for i, result in enumerate(results.web or [], start=1):
        print(f"{i}. {result.title}\n   {result.url}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command")

    p_scrape = sub.add_parser("scrape", help="Scrape a URL to Markdown")
    p_scrape.add_argument("url", nargs="?", default=DEFAULT_URL)

    p_search = sub.add_parser("search", help="Search the web")
    p_search.add_argument("query")
    p_search.add_argument("--limit", type=int, default=5)

    args = parser.parse_args()

    if args.command == "search":
        search(args.query, args.limit)
    else:
        # No subcommand (or "scrape") -> scrape a URL, defaulting to this repo.
        scrape(getattr(args, "url", DEFAULT_URL))


if __name__ == "__main__":
    main()
