#!/usr/bin/env python3
"""Substitui apenas o header pelo menu estilo site-modelo."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = "https://phorest.com/salon/spalenzaspa/book"

NAV_LINKS = [
    ("/", "Home"),
    ("/about-us/", "About Us"),
    ("/services/", "Services"),
    ("/contact/", "Contact"),
]

PAGE_ACTIVE = {
    "index.html": "/",
    "about-us/index.html": "/about-us/",
    "services/index.html": "/services/",
    "contact/index.html": "/contact/",
}

HEAD_EXTRA = """<link href="https://fonts.googleapis.com/css?family=Poppins:300,400,400i,500,600,700,800,900" rel="stylesheet" />
    <link rel="stylesheet" href="assets/css/nav-modelo.css" />"""

SCRIPT = '<script src="assets/js/nav-modelo.js"></script>'


def nav_items(active: str) -> str:
    lines = []
    for href, label in NAV_LINKS:
        cls = "nav-item active" if href == active else "nav-item"
        lines.append(f'<li class="{cls}"><a class="nav-link" href="{href}">{label}</a></li>')
    lines.append(
        f'<li class="nav-item btn-appointment"><a class="nav-link" href="{BOOK}" target="_blank" rel="noopener noreferrer">Book</a></li>'
    )
    return "\n".join(lines)


def build_nav(active: str) -> str:
    return f"""<nav class="navbar navbar-expand-lg bg-white">
<div class="container flex-column text-center">
<a class="navbar-brand mx-auto mb-2" href="/">
<span class="navbar-brand-text">Spalenza Spa<small>beauty salon &amp; wellness spa</small></span>
</a>
<button class="navbar-toggler collapsed" type="button" data-target="#main-nav" aria-expanded="false" aria-label="Toggle navigation">
<span class="navbar-toggler-icon"></span>
</button>
<div class="collapse navbar-collapse justify-content-center" id="main-nav">
<ul class="navbar-nav">
{nav_items(active)}
</ul>
</div>
</div>
</nav>"""


def apply(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT).as_posix()
    active = PAGE_ACTIVE.get(rel, f"/{path.parent.name}/" if path.name == "index.html" and path.parent != ROOT else "/")

    if "nav-modelo.css" not in html:
        html = html.replace(
            '<link rel="stylesheet" href="assets/css/responsive.css" />',
            '<link rel="stylesheet" href="assets/css/responsive.css" />\n    ' + HEAD_EXTRA,
            1,
        )

    if re.search(r"<nav class=\"navbar", html, re.I):
        html = re.sub(
            r"<nav class=\"navbar[^\"]*\"[^>]*>.*?</nav>",
            build_nav(active),
            html,
            count=1,
            flags=re.DOTALL | re.IGNORECASE,
        )
    else:
        html = re.sub(
            r"<header class=\"site-header\"[^>]*>.*?</header>",
            build_nav(active),
            html,
            count=1,
            flags=re.DOTALL | re.IGNORECASE,
        )

    if SCRIPT not in html:
        html = html.replace(
            "<script src=\"assets/js/navigation.js\"></script>",
            SCRIPT + "\n            <script src=\"assets/js/navigation.js\"></script>",
            1,
        )
        if SCRIPT not in html:
            html = html.replace("</body>", "    " + SCRIPT + "\n  </body>", 1)

    path.write_text(html, encoding="utf-8")


def main():
    targets = [ROOT / "index.html", *sorted(ROOT.glob("*/index.html"))]
    for p in targets:
        apply(p)
        print(p.relative_to(ROOT))


if __name__ == "__main__":
    main()
