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


def main() -> int:
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print("FIRECRAWL_API_KEY is not set", file=sys.stderr)
        return 1

    query = " ".join(sys.argv[1:]) or DEFAULT_QUERY
    firecrawl = Firecrawl(api_key=api_key)

    results = firecrawl.search(query, limit=3)
    if not results.web:
        print(f"No web results for {query!r}", file=sys.stderr)
        return 1

    top = results.web[0]
    print(f"Top result: {top.title}\n{top.url}\n")

    document = firecrawl.scrape(top.url, formats=["markdown"])
    markdown = document.markdown or ""
    print(markdown[:PREVIEW_CHARS])
    if len(markdown) > PREVIEW_CHARS:
        print(f"\n... ({len(markdown)} characters total)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
