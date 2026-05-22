#!/usr/bin/env python3
"""Remove .html de links internos e canonical (páginas na raiz do site)."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKIP_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "tel:",
    "#",
    "assets/",
    "site-modelo/",
)


def strip_html_href(match: re.Match) -> str:
    quote = match.group(1)
    url = match.group(2)
    if any(url.startswith(p) for p in SKIP_PREFIXES):
        return match.group(0)
    if url.endswith(".html"):
        url = url[:-5]
    if url == "index":
        url = "./"
    return f'href={quote}{url}{quote}'


def process_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    original = text

    text = re.sub(
        r'<link rel="canonical" href="https://spalenzaspa\.com/([^"]*?)\.html"',
        r'<link rel="canonical" href="https://spalenzaspa.com/\1"',
        text,
    )

    text = re.sub(
        r'href=(["\'])([^"\']+)\1',
        strip_html_href,
        text,
    )

    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"updated {path.name}")


def main():
    for html in sorted(ROOT.glob("*.html")):
        process_file(html)


if __name__ == "__main__":
    main()
