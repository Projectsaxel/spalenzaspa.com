#!/usr/bin/env python3
"""Apply King Spa shell to Spalenza HTML pages (one-time build helper)."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted(ROOT.glob("*.html"))
SKIP = {"site-modelo"}

BOOK = "https://phorest.com/salon/spalenzaspa/book"

NAV = [
    ("index.html", "Home"),
    ("about-us.html", "About Us"),
    ("services.html", "Services"),
    ("contact.html", "Contact"),
]


def nav_html(active: str) -> str:
    items = []
    for href, label in NAV:
        cls = ' class="nav-item active"' if href == active else ' class="nav-item"'
        items.append(f'<li{cls}><a class="nav-link" href="{href}">{label}</a></li>')
    book_cls = ' class="nav-item btn-appointment active"' if active == "book" else ' class="nav-item btn-appointment"'
    items.append(
        f'<li{book_cls}><a class="nav-link" href="{BOOK}" target="_blank" rel="noopener noreferrer">Book Now</a></li>'
    )
    return "\n".join(items)


def extract_head(html: str) -> str:
    m = re.search(r"<head[^>]*>(.*?)</head>", html, re.DOTALL | re.IGNORECASE)
    if not m:
        return ""
    head = m.group(1)
    head = re.sub(
        r'<link[^>]*href="assets/css/[^"]*"[^>]*>\s*',
        "",
        head,
        flags=re.IGNORECASE,
    )
    return head.strip()


def extract_main(html: str) -> str:
    m = re.search(r"<main[^>]*>(.*?)</main>", html, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else ""


def extract_body_class(html: str) -> str:
    m = re.search(r'<body[^>]*class="([^"]*)"', html, re.IGNORECASE)
    return m.group(1) if m else ""


def transform_main(content: str) -> str:
    content = content.replace('class="btn btn-secondary"', 'class="btn btn-default"')
    content = content.replace('class="btn btn-dark btn-sm"', 'class="btn btn-default btn-sm"')
    content = content.replace('class="btn btn-dark"', 'class="btn btn-default"')
    return content


FOOTER = """<footer id="footer">
<div class="footer-top">
<div class="container">
<div class="row">
<div class="col-md-4">
<div class="footer-widget">
<h3>Spalenza Spa</h3>
<p>Beauty salon &amp; wellness spa in Danvers, MA — serving the North Shore since 2017.</p>
</div>
</div>
<div class="col-md-4">
<div class="footer-widget">
<h3>Quick Links</h3>
<ul>
<li><a href="index.html">Home</a></li>
<li><a href="services.html">Services</a></li>
<li><a href="spa-packages-membership-danvers-ma.html">Packages &amp; Membership</a></li>
<li><a href="about-us.html">About Us</a></li>
<li><a href="contact.html">Contact</a></li>
</ul>
</div>
</div>
<div class="col-md-4">
<div class="footer-widget">
<h3>Contact Info</h3>
<ul>
<li><i class="fa fa-map-marker" aria-hidden="true"></i> 75 Newbury Street, Suite D, Danvers, MA 01923</li>
<li><i class="fa fa-phone" aria-hidden="true"></i> <a href="tel:+19788801400">(978) 880-1400</a></li>
<li><i class="fa fa-envelope" aria-hidden="true"></i> <a href="mailto:spalenzaspaadm@gmail.com">spalenzaspaadm@gmail.com</a></li>
</ul>
</div>
</div>
</div>
</div>
</div>
<div class="footer-bottom">
<div class="container">
<div class="row">
<div class="col-sm-12 col-md-6">
<div class="copyright">
<p>Spalenza Spa, LLC. &copy; All rights reserved.</p>
</div>
</div>
<div class="col-sm-12 col-md-6">
<ul class="social-icons pull-right">
<li><a href="https://www.facebook.com/spalenzaatm/" target="_blank" rel="noopener noreferrer"><i class="fa fa-facebook"></i></a></li>
<li><a href="https://www.instagram.com/spalenzaspa/" target="_blank" rel="noopener noreferrer"><i class="fa fa-instagram"></i></a></li>
<li><a href="https://www.yelp.com/biz/spalenza-spa-danvers-2" target="_blank" rel="noopener noreferrer"><i class="fa fa-yelp"></i></a></li>
</ul>
</div>
</div>
</div>
</div>
</footer>
<div class="back-top"><a href="#"><i class="fa fa-angle-up"></i></a></div>"""

SCRIPTS = """
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/wow/1.1.2/wow.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.3.4/owl.carousel.min.js"></script>
<script src="assets/js/spalenza-theme.js"></script>
<script src="assets/js/booking-config.js"></script>
<script src="assets/js/faq.js"></script>
<script src="assets/js/main.js"></script>
"""


def build_page(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    active = path.name
    head_inner = extract_head(html)
    main = transform_main(extract_main(html))
    body_class = extract_body_class(html)

    shell = f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_inner}
<link rel="stylesheet" href="assets/vendor/css/vendor.bundle.css" />
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" crossorigin="anonymous" referrerpolicy="no-referrer" />
<link href="https://fonts.googleapis.com/css?family=Poppins:300,400,400i,500,600,700,800,900" rel="stylesheet" />
<link rel="stylesheet" href="assets/vendor/css/theme.css" />
<link rel="stylesheet" href="assets/css/spalenza-legacy.css" />
</head>
<body class="{body_class}">
<nav class="navbar navbar-expand-lg bg-white">
<div class="container flex-column text-center">
<a class="navbar-brand mx-auto mb-2" href="index.html">
<span class="navbar-brand-text">Spalenza Spa<small>beauty salon &amp; wellness spa</small></span>
</a>
<button class="navbar-toggler collapsed" type="button" data-toggle="collapse" data-target="#main-nav" aria-expanded="false" aria-label="Toggle navigation">
<span class="navbar-toggler-icon"></span>
</button>
<div class="collapse navbar-collapse justify-content-center" id="main-nav">
<ul class="navbar-nav">
{nav_html(active)}
</ul>
</div>
</div>
</nav>
<main>
{main}
</main>
<section class="section-spacing inverse-bg book-cta-bar">
<div class="container">
<div class="row align-items-center">
<div class="col-md-8">
<div class="appoinment-text wow fadeIn">
<h2>Book Online</h2>
<p>Schedule your visit at Spalenza Spa in Danvers, MA. Gift cards and memberships available.</p>
<p>Call us: <a href="tel:+19788801400">(978) 880-1400</a> or book online below.</p>
<a href="{BOOK}" class="btn btn-primary" target="_blank" rel="noopener noreferrer">Click to book</a>
</div>
</div>
<div class="col-md-4 text-md-right text-center wow fadeIn">
<a href="{BOOK}" class="btn btn-default" target="_blank" rel="noopener noreferrer">Gift Cards</a>
</div>
</div>
</div>
</section>
{FOOTER}
{SCRIPTS}
</body>
</html>
"""
    return shell


def main():
    for path in PAGES:
        if path.name in SKIP:
            continue
        out = build_page(path)
        path.write_text(out, encoding="utf-8")
        print(f"Updated {path.name}")


if __name__ == "__main__":
    main()
