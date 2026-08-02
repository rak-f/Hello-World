"""Search the web with Firecrawl and scrape the top result as markdown.

Usage:
    export FIRECRAWL_API_KEY=fc-...
    python examples/search_and_scrape.py "hello world program"

Docs: https://docs.firecrawl.dev
"""

import os
import sys

from firecrawl import Firecrawl

DEFAULT_QUERY = "hello world program"
PREVIEW_CHARS = 500

# Bounds how long a single HTTP request may block locally. Without it the SDK
# passes timeout=None to requests, so a server that accepts the connection and
# then never responds blocks indefinitely.
# The SDK already retries failed requests 3x with exponential backoff.
HTTP_TIMEOUT_SECONDS = 60

# Server-side render budget, in MILLISECONDS (min 1000). Note the SDK docstring
# claims seconds; the API rejects values below 1000, so milliseconds it is.
SCRAPE_TIMEOUT_MS = 30_000


def main() -> int:
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print("FIRECRAWL_API_KEY is not set", file=sys.stderr)
        return 1

    query = " ".join(sys.argv[1:]) or DEFAULT_QUERY
    firecrawl = Firecrawl(api_key=api_key, timeout=HTTP_TIMEOUT_SECONDS)

    results = firecrawl.search(query, limit=3)
    if not results.web:
        print(f"No web results for {query!r}", file=sys.stderr)
        return 1

    top = results.web[0]
    print(f"Top result: {top.title}\n{top.url}\n")

    document = firecrawl.scrape(
        top.url, formats=["markdown"], timeout=SCRAPE_TIMEOUT_MS
    )
    markdown = document.markdown or ""
    print(markdown[:PREVIEW_CHARS])
    if len(markdown) > PREVIEW_CHARS:
        print(f"\n... ({len(markdown)} characters total)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
