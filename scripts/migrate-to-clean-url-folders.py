#!/usr/bin/env python3
"""
Cria slug/index.html para cada página e remove o .html na raiz.
Atualiza links internos para caminhos absolutos na raiz (/slug/).
"""

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKIP = {"index.html"}
INTERNAL_PAGES = set()


def collect_pages():
    for html in ROOT.glob("*.html"):
        if html.name not in SKIP:
            INTERNAL_PAGES.add(html.stem)


def migrate_files():
    for html in sorted(ROOT.glob("*.html")):
        if html.name in SKIP:
            continue
        slug = html.stem
        dest_dir = ROOT / slug
        dest_dir.mkdir(exist_ok=True)
        dest = dest_dir / "index.html"
        shutil.copy2(html, dest)
        html.unlink()
        print(f"migrated {html.name} -> {slug}/index.html")


def fix_link_url(url: str) -> str:
    if any(
        url.startswith(p)
        for p in ("http://", "https://", "mailto:", "tel:", "#", "//", "/")
    ):
        return url
    if url in ("./", ".", ""):
        return "/"
    if url.endswith(".html"):
        url = url[:-5]
    if url.endswith("/"):
        return "/" + url
    if url in INTERNAL_PAGES:
        return f"/{url}/"
    return "/" + url


def fix_attr(html: str, attr: str) -> str:
    def repl(match: re.Match) -> str:
        quote = match.group(1)
        url = match.group(2)
        return f'{attr}={quote}{fix_link_url(url)}{quote}'

    return re.sub(
        rf'{attr}=(["\'])([^"\']+)\1',
        repl,
        html,
    )


def update_links_in_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    original = text
    text = fix_attr(text, "href")
    text = fix_attr(text, "src")
    text = fix_attr(text, "action")
    text = re.sub(
        r'<link rel="canonical" href="https://spalenzaspa\.com/([^"]*?)\.html"',
        r'<link rel="canonical" href="https://spalenzaspa.com/\1"',
        text,
    )
    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"links updated {path.relative_to(ROOT)}")


def update_all_html():
    targets = [ROOT / "index.html"]
    targets.extend(ROOT.glob("*/index.html"))
    for path in targets:
        update_links_in_file(path)


def main():
    collect_pages()
    migrate_files()
    collect_pages()
    update_all_html()
    print("done")


if __name__ == "__main__":
    main()
