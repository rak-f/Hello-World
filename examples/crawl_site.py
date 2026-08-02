#!/usr/bin/env python3
"""Crawl a small site with Firecrawl and save each page's markdown to a file.

Usage:
    export FIRECRAWL_API_KEY="fc-..."
    pip install -r examples/requirements.txt
    python examples/crawl_site.py https://example.com --limit 5 --out pages

Docs: https://docs.firecrawl.dev
"""

import argparse
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

from firecrawl import Firecrawl


def slugify(url: str) -> str:
    """Turn a page URL into a safe, readable markdown filename stem."""
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    stem = f"{parsed.netloc}-{path}" if path else parsed.netloc
    return re.sub(r"[^a-zA-Z0-9]+", "-", stem).strip("-").lower() or "page"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("url", help="URL to start crawling from")
    parser.add_argument(
        "--limit", type=int, default=5, help="maximum pages to crawl (default: 5)"
    )
    parser.add_argument(
        "--out", default="pages", help="output directory (default: pages)"
    )
    args = parser.parse_args()

    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print("FIRECRAWL_API_KEY is not set.", file=sys.stderr)
        return 1

    firecrawl = Firecrawl(api_key=api_key)
    job = firecrawl.crawl(args.url, limit=args.limit, formats=["markdown"])

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    for document in job.data:
        if not document.markdown:
            continue
        page_url = document.metadata.source_url or document.metadata.url or args.url
        path = out_dir / f"{slugify(page_url)}.md"
        path.write_text(document.markdown, encoding="utf-8")
        print(f"{page_url} -> {path}")
        written += 1

    print(
        f"\nstatus={job.status} pages={job.completed}/{job.total} "
        f"written={written} credits_used={job.credits_used}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
