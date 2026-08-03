#!/usr/bin/env python3
"""List the URLs of a site using Firecrawl's map endpoint.

Usage:
    pip install -r examples/requirements.txt
    export FIRECRAWL_API_KEY=fc-...
    python examples/extract_links.py https://example.com --limit 20

Docs: https://docs.firecrawl.dev/api-reference/endpoint/map
"""

import argparse
import os
import sys

from firecrawl import Firecrawl


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("url", help="root URL to map, e.g. https://example.com")
    parser.add_argument(
        "--limit", type=int, default=20, help="maximum number of URLs to return"
    )
    parser.add_argument("--search", help="only return URLs matching this text")
    args = parser.parse_args()

    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print(
            "FIRECRAWL_API_KEY is not set. Get a key at https://firecrawl.dev",
            file=sys.stderr,
        )
        return 1

    firecrawl = Firecrawl(api_key=api_key)
    result = firecrawl.map(args.url, limit=args.limit, search=args.search)

    for link in result.links:
        print(link.url)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
