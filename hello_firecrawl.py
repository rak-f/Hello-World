#!/usr/bin/env python3
"""Hello World for Firecrawl.

Scrapes a web page and prints it as clean Markdown — the web-scraping
equivalent of "Hello World!". Uses the official Firecrawl Python SDK.

Setup:
    pip install -r requirements.txt
    cp .env.example .env   # then paste your key, or just export it:
    export FIRECRAWL_API_KEY="fc-..."

Run:
    python hello_firecrawl.py [URL]

Get a key and read the docs at https://docs.firecrawl.dev
"""

import os
import sys

from firecrawl import Firecrawl

DEFAULT_URL = "https://example.com"


def main() -> int:
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print(
            "FIRECRAWL_API_KEY is not set. Copy .env.example to .env and add "
            "your key, or run: export FIRECRAWL_API_KEY=fc-...",
            file=sys.stderr,
        )
        return 1

    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL

    firecrawl = Firecrawl(api_key=api_key)
    doc = firecrawl.scrape(url, formats=["markdown"])

    print(f"# Scraped {url}\n")
    print(doc.markdown or "(no markdown returned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
