import re

from pydantic import HttpUrl


def extract_github_username(url: HttpUrl) -> str:
    url_str = str(url)
    match = re.search(r"github\.com/([^/]+)", url_str)
    return match.group(1) if match else url_str


def clean_url_display(url: HttpUrl) -> str:
    url_str = str(url)
    if url_str.endswith("/"):
        url_str = url_str[:-1]
    return url_str.replace("https://", "").replace("http://", "")
