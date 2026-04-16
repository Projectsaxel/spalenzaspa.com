function initNavigation() {
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");

  if (!header || !toggle || !nav) return;

  // Ensure initial aria state
  toggle.setAttribute("aria-expanded", "false");

  // Mobile toggle
  toggle.addEventListener("click", function () {
    var isOpen = header.classList.toggle("is-nav-open");
    toggle.classList.toggle("is-open", isOpen);
    toggle.setAttribute("aria-expanded", String(isOpen));
  });

  // Services dropdown is handled by native <details>/<summary> markup + CSS.

  // Close mobile nav when clicking a link
  nav.addEventListener("click", function (event) {
    var target = event.target;
    if (
      target instanceof HTMLElement &&
      target.tagName === "A" &&
      header.classList.contains("is-nav-open")
    ) {
      header.classList.remove("is-nav-open");
      toggle.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    }
  });

  // Sticky header effect on scroll
  var lastScrollY = window.scrollY;
  window.addEventListener("scroll", function () {
    var current = window.scrollY;
    if (current > 24 && current > lastScrollY) {
      header.classList.add("site-header--scrolled");
    } else if (current < 12) {
      header.classList.remove("site-header--scrolled");
    }
    lastScrollY = current;
  });
}

