#!/usr/bin/env python3
"""Adiciona banner de imagem compacto no hero das páginas de serviço."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SERVICE_PAGES = {
    "japanese-head-spa-massachusetts/index.html": (
        "assets/img/services/japanese-head-spa.jpg",
        "Japanese Head Spa at Spalenza Spa in Danvers, MA",
    ),
    "laser-hair-removal-danvers-ma/index.html": (
        "assets/img/services/laser-hair-removal.jpg",
        "Laser hair removal at Spalenza Spa in Danvers, MA",
    ),
    "hydrafacial-danvers-ma/index.html": (
        "assets/img/services/hydrafacial.jpg",
        "HydraFacial treatment at Spalenza Spa in Danvers, MA",
    ),
    "massage-body-wellness-danvers-ma/index.html": (
        "assets/img/services/massage.jpg",
        "Massage therapy at Spalenza Spa in Danvers, MA",
    ),
    "spa-packages-membership-danvers-ma/index.html": (
        "assets/img/services/membership.jpg",
        "Spa membership at Spalenza Spa in Danvers, MA",
    ),
    "chemical-peels-facials-danvers-ma/index.html": (
        "assets/img/services/hydrafacial.jpg",
        "Facial and peel treatments at Spalenza Spa in Danvers, MA",
    ),
    "facial-skin-treatments-danvers-ma/index.html": (
        "assets/img/services/hydrafacial.jpg",
        "Facial skin treatments at Spalenza Spa in Danvers, MA",
    ),
    "mens-spa-danvers-ma/index.html": (
        "assets/img/services/massage.jpg",
        "Men's spa services at Spalenza Spa in Danvers, MA",
    ),
    "microblading-danvers-ma/index.html": (
        "assets/img/services/eyebrows.jpg",
        "Microblading at Spalenza Spa in Danvers, MA",
    ),
    "eyes-brows-permanent-makeup-danvers-ma/index.html": (
        "assets/img/services/eyebrows.jpg",
        "Brows and lashes at Spalenza Spa in Danvers, MA",
    ),
    "hair-removal-danvers-ma/index.html": (
        "assets/img/services/waxing.jpg",
        "Hair removal services at Spalenza Spa in Danvers, MA",
    ),
    "injectables-wellness-danvers-ma/index.html": (
        "assets/img/services/hot-stone.jpg",
        "Wellness and injectable consultations at Spalenza Spa in Danvers, MA",
    ),
}


def transform_hero(html: str, img: str, alt: str) -> str:
    if "service-hero-banner" in html:
        return html

    match = re.search(
        r'<section class="page-hero"[^>]*>(.*?)</section>',
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )
    if not match:
        return html

    inner = match.group(1)
    eyebrow = re.search(r"<p class=\"eyebrow\"[^>]*>.*?</p>", inner, flags=re.DOTALL)
    title = re.search(r"<h1 class=\"page-title\"[^>]*>.*?</h1>", inner, flags=re.DOTALL)
    if not eyebrow or not title:
        return html

    rest = inner.replace(eyebrow.group(0), "", 1).replace(title.group(0), "", 1)

    new_section = f"""<section class="page-hero page-hero--service">
        <div class="service-hero-banner">
          <img
            src="{img}"
            alt="{alt}"
            width="1920"
            height="400"
            loading="eager"
          />
          <div class="service-hero-overlay">
            <div class="service-hero-caption container">
              {eyebrow.group(0)}
              {title.group(0)}
            </div>
          </div>
        </div>
        {rest.strip()}
      </section>"""

    return html[: match.start()] + new_section + html[match.end() :]


def main():
    for name, (img, alt) in SERVICE_PAGES.items():
        path = ROOT / name
        if not path.exists():
            path = ROOT / name.replace("/index.html", ".html")
        if not path.exists():
            print(f"skip missing {name}")
            continue
        text = path.read_text(encoding="utf-8")
        updated = transform_hero(text, img, alt)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            print(f"updated {name}")
        else:
            print(f"unchanged {name}")


if __name__ == "__main__":
    main()
