#!/usr/bin/env python3
"""Scrape a single URL with Firecrawl and print the returned markdown.

Usage:
    export FIRECRAWL_API_KEY=fc-...
    python examples/firecrawl_scrape.py [url]

Firecrawl docs: https://docs.firecrawl.dev
"""

import os
import sys

from firecrawl import Firecrawl

DEFAULT_URL = "https://example.com"


def main():
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print(
            "FIRECRAWL_API_KEY is not set. Get a key at https://firecrawl.dev",
            file=sys.stderr,
        )
        return 1

    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    firecrawl = Firecrawl(api_key=api_key)
    doc = firecrawl.scrape(url, formats=["markdown"])
    print(doc.markdown or "")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
