#!/usr/bin/env python3
"""Substitui apenas o header pelo menu estilo site-modelo."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = "https://phorest.com/salon/spalenzaspa/book"

NAV_SLUGS = [
    ("", "Home"),
    ("about-us", "About Us"),
    ("services", "Services"),
    ("contact", "Contact"),
]

PAGE_ACTIVE = {
    "index.html": "",
    "about-us/index.html": "about-us",
    "services/index.html": "services",
    "contact/index.html": "contact",
}

SCRIPT = '<script src="{assets}js/nav-modelo.js"></script>'


def depth(path: Path) -> int:
    if path.parent == ROOT:
        return 0
    return len(path.parent.relative_to(ROOT).parts)


def asset_prefix(path: Path) -> str:
    d = depth(path)
    if d == 0:
        return "assets/"
    return "../" * d + "assets/"


def page_href(from_file: Path, slug: str) -> str:
    d = depth(from_file)
    if not slug:
        return "./" if d == 0 else "../" * d
    if d == 0:
        return f"{slug}/"
    return f"{'../' * d}{slug}/"


def head_extra(path: Path) -> str:
    assets = asset_prefix(path)
    return f"""<link href="https://fonts.googleapis.com/css?family=Poppins:300,400,400i,500,600,700,800,900" rel="stylesheet" />
    <link rel="stylesheet" href="{assets}css/nav-modelo.css" />"""


def nav_items(from_file: Path, active_slug: str) -> str:
    lines = []
    for slug, label in NAV_SLUGS:
        cls = "nav-item active" if slug == active_slug else "nav-item"
        href = page_href(from_file, slug)
        lines.append(f'<li class="{cls}"><a class="nav-link" href="{href}">{label}</a></li>')
    lines.append(
        f'<li class="nav-item btn-appointment"><a class="nav-link" href="{BOOK}" target="_blank" rel="noopener noreferrer">Book</a></li>'
    )
    return "\n".join(lines)


def build_nav(from_file: Path, active_slug: str) -> str:
    home = page_href(from_file, "")
    return f"""<nav class="navbar navbar-expand-lg bg-white">
<div class="container flex-column text-center">
<a class="navbar-brand mx-auto mb-2" href="{home}">
<span class="navbar-brand-text">Spalenza Spa<small>beauty salon &amp; wellness spa</small></span>
</a>
<button class="navbar-toggler collapsed" type="button" data-target="#main-nav" aria-expanded="false" aria-label="Toggle navigation">
<span class="navbar-toggler-icon"></span>
</button>
<div class="collapse navbar-collapse justify-content-center" id="main-nav">
<ul class="navbar-nav">
{nav_items(from_file, active_slug)}
</ul>
</div>
</div>
</nav>"""


def apply(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT).as_posix()
    active = PAGE_ACTIVE.get(rel, path.parent.name if path.parent != ROOT else "")

    assets = asset_prefix(path)
    responsive = f'{assets}css/responsive.css'

    if "nav-modelo.css" not in html:
        html = html.replace(
            f'<link rel="stylesheet" href="{assets}css/responsive.css" />',
            f'<link rel="stylesheet" href="{assets}css/responsive.css" />\n    ' + head_extra(path),
            1,
        )

    if re.search(r"<nav class=\"navbar", html, re.I):
        html = re.sub(
            r"<nav class=\"navbar[^\"]*\"[^>]*>.*?</nav>",
            build_nav(path, active),
            html,
            count=1,
            flags=re.DOTALL | re.IGNORECASE,
        )
    else:
        html = re.sub(
            r"<header class=\"site-header\"[^>]*>.*?</header>",
            build_nav(path, active),
            html,
            count=1,
            flags=re.DOTALL | re.IGNORECASE,
        )

    script = SCRIPT.format(assets=assets)
    nav_script = f'<script src="{assets}js/navigation.js"></script>'
    if script not in html:
        html = html.replace(
            nav_script,
            script + "\n            " + nav_script,
            1,
        )
        if script not in html:
            html = html.replace("</body>", "    " + script + "\n  </body>", 1)

    path.write_text(html, encoding="utf-8")


def main():
    targets = [ROOT / "index.html", *sorted(ROOT.glob("*/index.html"))]
    for p in targets:
        apply(p)
        print(p.relative_to(ROOT))


if __name__ == "__main__":
    main()
