"""Configuration for the Firecrawl integration.

Settings are read from the environment, with an optional local ``.env`` file
for convenience. Never hardcode secrets here — set ``FIRECRAWL_API_KEY`` in
your environment (or in a local, git-ignored ``.env``).
"""

import os
from pathlib import Path


def _load_dotenv(path: Path) -> None:
    """Load ``KEY=value`` pairs from a local .env file into the environment.

    Existing environment variables take precedence, so this never overrides
    a value the caller has already exported.
    """
    if not path.exists():
        return
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


_load_dotenv(Path(__file__).resolve().parent / ".env")

FIRECRAWL_API_KEY = os.environ.get("FIRECRAWL_API_KEY")


def require_api_key() -> str:
    """Return the Firecrawl API key or raise a helpful error if it's missing."""
    if not FIRECRAWL_API_KEY:
        raise RuntimeError(
            "FIRECRAWL_API_KEY is not set. Copy .env.example to .env and add "
            "your key, or export FIRECRAWL_API_KEY in your environment."
        )
    return FIRECRAWL_API_KEY
