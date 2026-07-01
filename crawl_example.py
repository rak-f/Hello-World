"""Hello World for Firecrawl — crawl a site and print what was found.

Firecrawl's crawl endpoint discovers the pages under a URL and returns each
one as clean, LLM-ready markdown. This script runs a small, bounded crawl and
prints a short summary of the pages it collected.

Usage:
    export FIRECRAWL_API_KEY=fc-...      # see .env.example
    python crawl_example.py [start_url] [limit]

Docs: https://docs.firecrawl.dev
"""

import os
import sys

from firecrawl import Firecrawl

# A small, public docs site makes for a friendly default crawl target.
DEFAULT_URL = "https://docs.firecrawl.dev"
DEFAULT_LIMIT = 5


def main() -> int:
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print("FIRECRAWL_API_KEY is not set — see .env.example.", file=sys.stderr)
        return 1

    start_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_LIMIT

    firecrawl = Firecrawl(api_key=api_key)

    print(f"Crawling {start_url} (up to {limit} pages)...")
    job = firecrawl.crawl(start_url, limit=limit, formats=["markdown"])

    pages = job.data or []
    print(f"Status: {job.status} — {len(pages)} page(s), {job.credits_used} credit(s) used.\n")
    for page in pages:
        meta = page.metadata
        url = (meta.source_url or meta.url) if meta else "?"
        markdown = page.markdown or ""
        print(f"- {url} ({len(markdown)} chars of markdown)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
