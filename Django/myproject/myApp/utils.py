import io
import os
import re
import urllib.request
from urllib.parse import urlparse


INDENT = 0.25
LIST_INDENT = 0.5
MAX_INDENT = 5.5


def get_filename_from_url(url: str) -> str:
    return os.path.basename(urlparse(url).path)


def is_url(value: str) -> bool:
    parts = urlparse(value)
    return all([parts.scheme, parts.netloc, parts.path])


def fetch_image(url: str):
    try:
        with urllib.request.urlopen(url) as response:
            return io.BytesIO(response.read())
    except urllib.error.URLError:
        return None


def remove_last_occurrence(items, value):
    try:
        items.pop(len(items) - items[::-1].index(value) - 1)
    except ValueError:
        pass


def remove_whitespace(text: str, leading=False, trailing=False) -> str:
    if leading:
        text = re.sub(r"^\s*\n+\s*", "", text)
    if trailing:
        text = re.sub(r"\s*\n+\s*$", "", text)
    text = re.sub(r"\s*\n\s*", " ", text)
    return re.sub(r"\s+", " ", text)


def delete_paragraph(paragraph):
    p = paragraph._element
    p.getparent().remove(p)
    p._p = p._element = None