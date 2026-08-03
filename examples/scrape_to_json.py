#!/usr/bin/env python3
"""Scrape a page with Firecrawl and print structured JSON.

Uses the Firecrawl scrape endpoint with the `json` extraction format, which asks
an LLM to fill in a JSON Schema from the page content.

Usage:
    export FIRECRAWL_API_KEY=fc-...
    python examples/scrape_to_json.py https://example.com

Docs: https://docs.firecrawl.dev
"""

import json
import os
import sys

from firecrawl import Firecrawl

DEFAULT_URL = "https://example.com"

# Any JSON Schema works here; Firecrawl fills it in from the page.
PAGE_SUMMARY_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "description": "The page's main heading"},
        "summary": {"type": "string", "description": "One sentence about the page"},
        "topics": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Key topics mentioned on the page",
        },
    },
    "required": ["title", "summary"],
}


def main() -> int:
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print(
            "FIRECRAWL_API_KEY is not set. Get a key at https://firecrawl.dev",
            file=sys.stderr,
        )
        return 1

    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL

    firecrawl = Firecrawl(api_key=api_key)
    doc = firecrawl.scrape(
        url,
        formats=[{"type": "json", "schema": PAGE_SUMMARY_SCHEMA}],
    )

    print(json.dumps(doc.json, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
