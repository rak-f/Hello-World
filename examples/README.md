# Examples

## Firecrawl: scrape a URL

[`scrape_url.py`](scrape_url.py) fetches a single page through the
[Firecrawl](https://docs.firecrawl.dev) API and prints it as Markdown.

### Setup

```sh
pip install -r requirements.txt
export FIRECRAWL_API_KEY="fc-..."   # get one at https://firecrawl.dev
```

### Run

```sh
python scrape_url.py                    # scrapes https://example.com
python scrape_url.py https://iana.org   # or pass your own URL
```

Output:

```
Title:   Example Domain
Source:  https://example.com
Status:  200
Credits: 1

# Example Domain

This domain is for use in documentation examples without needing permission. Avoid use in operations.

[Learn more](https://iana.org/domains/example)
```

The script exits with status 1 if `FIRECRAWL_API_KEY` is unset.

Firecrawl can also crawl, map, and search sites — see the
[Firecrawl docs](https://docs.firecrawl.dev) and the
[Python SDK reference](https://docs.firecrawl.dev/sdks/python).
