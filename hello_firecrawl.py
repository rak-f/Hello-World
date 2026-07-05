#!/usr/bin/env python3
"""Hello, Firecrawl!

A tiny "Hello World" for Firecrawl: scrape a single web page and print it
back as clean Markdown. This is the smallest real thing you can do with the
Firecrawl API and a natural companion to this repository's Hello World theme.

Usage:
    export FIRECRAWL_API_KEY="fc-..."      # get one at https://firecrawl.dev
    python3 hello_firecrawl.py [URL]

Docs: https://docs.firecrawl.dev
"""

import os
import sys

from firecrawl import Firecrawl

# A friendly default so the script does something useful with no arguments.
DEFAULT_URL = "https://example.com"


def main() -> int:
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print(
            "error: FIRECRAWL_API_KEY is not set.\n"
            "Get a key at https://firecrawl.dev and run:\n"
            '  export FIRECRAWL_API_KEY="fc-..."',
            file=sys.stderr,
        )
        return 1

    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL

    firecrawl = Firecrawl(api_key=api_key)
    doc = firecrawl.scrape(url, formats=["markdown"])

    title = getattr(doc.metadata, "title", None) if doc.metadata else None
    print(f"# Hello from Firecrawl 👋  ({title or url})\n")
    print(doc.markdown or "(no markdown returned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
