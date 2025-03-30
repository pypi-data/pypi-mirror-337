import os
from .const import DEFAULT_URL


def get_base_url(url: str | None = None) -> str:
    """Return the base URL with the trailing slash stripped.
    If the URL is a Falsy value, tries to retrieve URL from environment
    and if it's Falsy anyway return the default URL.
    Returns:
        The base URL
    """
    if not url:
        url = os.getenv("OUTLINE_URL")
        if not url:
            return DEFAULT_URL
    return url.rstrip("/")


def get_token(token: str | None = None) -> str:
    if not token:
        token = os.getenv('OUTLINE_TOKEN')
    return token
