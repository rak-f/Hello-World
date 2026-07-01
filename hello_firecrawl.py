#!/usr/bin/env python3
"""Hello World, via Firecrawl.

A tiny, self-contained example that runs a web search with Firecrawl and prints
the top results -- the "Hello World" of web search.

Usage:
    export FIRECRAWL_API_KEY="fc-..."   # see .env.example
    python hello_firecrawl.py [QUERY...]

Get a free API key and read the docs at https://docs.firecrawl.dev
"""

import os
import sys

from firecrawl import Firecrawl

DEFAULT_QUERY = "what is Firecrawl"
LIMIT = 5


def main() -> int:
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print(
            "FIRECRAWL_API_KEY is not set. Copy .env.example to .env and add "
            "your key, or export it in your shell. See https://docs.firecrawl.dev",
            file=sys.stderr,
        )
        return 1

    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else DEFAULT_QUERY
    firecrawl = Firecrawl(api_key=api_key)

    print(f"Searching for {query!r} ...\n")
    results = firecrawl.search(query, limit=LIMIT)

    web = results.web or []
    if not web:
        print("(no web results returned)")
        return 0

    print(f"Hello from Firecrawl! Top {len(web)} results:\n")
    for i, result in enumerate(web, start=1):
        print(f"{i}. {result.title or '(untitled)'}")
        print(f"   {result.url}")
        if result.description:
            print(f"   {result.description}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
