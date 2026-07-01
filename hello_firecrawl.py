#!/usr/bin/env python3
"""Hello World, via Firecrawl.

A tiny, self-contained example that scrapes a web page with Firecrawl and
prints its content as Markdown -- the "Hello World" of web data extraction.

Usage:
    export FIRECRAWL_API_KEY="fc-..."   # see .env.example
    python hello_firecrawl.py [URL]

Get a free API key and read the docs at https://docs.firecrawl.dev
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
            "your key, or export it in your shell. See https://docs.firecrawl.dev",
            file=sys.stderr,
        )
        return 1

    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    firecrawl = Firecrawl(api_key=api_key)

    print(f"Scraping {url} ...")
    doc = firecrawl.scrape(url, formats=["markdown"])

    title = getattr(doc.metadata, "title", None) if doc.metadata else None
    print(f"Hello from {title or url}!\n")
    print(doc.markdown or "(no markdown content returned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
