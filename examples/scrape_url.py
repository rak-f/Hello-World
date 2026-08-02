#!/usr/bin/env python3
"""Scrape a single URL with Firecrawl and print it as Markdown.

Usage:
    export FIRECRAWL_API_KEY="fc-..."
    python scrape_url.py [URL]

Docs: https://docs.firecrawl.dev
"""

import os
import sys

from firecrawl import Firecrawl

DEFAULT_URL = "https://example.com"
PREVIEW_CHARS = 500


def main() -> int:
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print(
            "FIRECRAWL_API_KEY is not set. Get a key at https://firecrawl.dev "
            "and export it before running this script.",
            file=sys.stderr,
        )
        return 1

    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL

    firecrawl = Firecrawl(api_key=api_key)
    document = firecrawl.scrape(url, formats=["markdown"])

    metadata = document.metadata
    print(f"Title:   {metadata.title}")
    print(f"Source:  {metadata.source_url}")
    print(f"Status:  {metadata.status_code}")
    print(f"Credits: {metadata.credits_used}")
    print()

    markdown = document.markdown or ""
    print(markdown[:PREVIEW_CHARS])
    if len(markdown) > PREVIEW_CHARS:
        print(f"\n... ({len(markdown)} characters total)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
