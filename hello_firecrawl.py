#!/usr/bin/env python3
"""Hello World, via Firecrawl.

A tiny, self-contained example that creates a Firecrawl monitor -- a scheduled,
recurring check that watches a URL for changes -- prints it, then cleans it up.
The "Hello World" of web monitoring.

A monitor is a persistent resource on your account, so this example deletes the
one it creates (pass --keep to leave it running).

Usage:
    export FIRECRAWL_API_KEY="fc-..."   # see .env.example
    python hello_firecrawl.py [URL] [--keep]

Get a free API key and read the docs at https://docs.firecrawl.dev
"""

import os
import sys

from firecrawl import Firecrawl

DEFAULT_URL = "https://example.com"


def main() -> int:
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print(
            "FIRECRAWL_API_KEY is not set. Copy .env.example to .env and add "
            "your key, or export it in your shell. See https://docs.firecrawl.dev",
            file=sys.stderr,
        )
        return 1

    args = sys.argv[1:]
    keep = "--keep" in args
    urls = [a for a in args if a != "--keep"]
    url = urls[0] if urls else DEFAULT_URL

    firecrawl = Firecrawl(api_key=api_key)

    print(f"Creating a monitor for {url} ...")
    monitor = firecrawl.create_monitor(
        name="Hello Firecrawl monitor",
        schedule={"text": "every 30 minutes", "timezone": "UTC"},
        goal=f"Alert when the content of {url} changes.",
        targets=[{"type": "scrape", "urls": [url]}],
    )

    print("\nHello from Firecrawl! Created monitor:")
    print(f"  id:       {monitor.id}")
    print(f"  name:     {monitor.name}")
    print(f"  status:   {monitor.status}")
    print(f"  schedule: {monitor.schedule.text or monitor.schedule.cron}")
    print(f"  next run: {monitor.next_run_at}")

    if keep:
        print("\n--keep given; leaving the monitor running.")
    else:
        firecrawl.delete_monitor(monitor.id)
        print("\nCleaned up (deleted the monitor). Pass --keep to leave it running.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
