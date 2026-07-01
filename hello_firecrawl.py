#!/usr/bin/env python3
"""Hello World for Firecrawl.

Runs a small crawl (capped at a handful of pages, each fetched as clean
Markdown) and prints the title and URL of every page found — the web-crawling
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
# Keep the demo cheap and fast: crawl at most a few pages.
PAGE_LIMIT = 5


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
    job = firecrawl.crawl(url, limit=PAGE_LIMIT, formats=["markdown"])

    pages = job.data or []
    print(f"# Crawled {url} — {len(pages)} page(s) [status: {job.status}]\n")
    for i, doc in enumerate(pages, start=1):
        meta = doc.metadata
        source = (meta and meta.source_url) or url
        title = (meta and meta.title) or "(untitled)"
        print(f"{i}. {title} — {source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
