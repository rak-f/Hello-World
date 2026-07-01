#!/usr/bin/env python3
"""Hello, Firecrawl — a tiny web-search example for the Hello-World repo.

Runs one live Firecrawl web search and prints the top results. It is the
"Hello World" of Firecrawl: the smallest real program that talks to the API.

Usage:
    export FIRECRAWL_API_KEY=fc-...      # get a key at https://firecrawl.dev
    python3 hello_firecrawl.py           # uses the default query
    python3 hello_firecrawl.py "your search query here"

Docs: https://docs.firecrawl.dev
"""
import os
import sys

from firecrawl import Firecrawl

DEFAULT_QUERY = "Hello World"


def main() -> int:
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print(
            "FIRECRAWL_API_KEY is not set. Copy .env.example, add your key "
            "(https://firecrawl.dev), and export it before running.",
            file=sys.stderr,
        )
        return 1

    query = " ".join(sys.argv[1:]) or DEFAULT_QUERY
    firecrawl = Firecrawl(api_key=api_key)

    print(f"Searching Firecrawl for: {query!r}\n")
    results = firecrawl.search(query, limit=5)

    web_results = results.web or []
    if not web_results:
        print("No results found.")
        return 0

    for i, result in enumerate(web_results, start=1):
        print(f"{i}. {result.title}")
        print(f"   {result.url}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
