#!/usr/bin/env python3
"""Minimal Firecrawl example: scrape a single page into Markdown.

Firecrawl (https://docs.firecrawl.dev) turns any URL into clean,
LLM-ready Markdown. This script scrapes one page and prints the result —
a "Hello World" for the Firecrawl Python SDK.

Usage:
    export FIRECRAWL_API_KEY="fc-..."     # get a key at https://firecrawl.dev
    python examples/firecrawl_scrape.py [URL]

If no URL is given, it scrapes https://example.com.
"""

import os
import sys

from firecrawl import Firecrawl


def main() -> int:
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print(
            "Error: set FIRECRAWL_API_KEY first "
            "(see .env.example / https://firecrawl.dev).",
            file=sys.stderr,
        )
        return 1

    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"

    firecrawl = Firecrawl(api_key=api_key)
    doc = firecrawl.scrape(url, formats=["markdown"])

    print(f"# Scraped: {url}\n")
    print(doc.markdown or "(no markdown returned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
