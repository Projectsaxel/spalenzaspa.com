/*
==================================================
SPALENZA SPA — PHOREST BOOKING CONFIG
Edit service-specific URLs below.
If a service URL is blank, the general booking URL will be used automatically.
==================================================
*/

(function () {
  "use strict";

  var PHOREST_GENERAL_BOOKING =
    "https://www.phorest.com/salon/spalenzaspa/book/serviceselection";
  var PHOREST_MEMBERSHIP = "https://www.phorest.com/salon/spalenzaspa/buy/membership";
  var PHOREST_GIFT_CARDS = "https://gift-cards.phorest.com/salons/spalenzaspa";

  // Keys are stable identifiers used in HTML data attributes.
  // Leave values empty to use PHOREST_GENERAL_BOOKING automatically.
  var SERVICE_BOOKING_LINKS = {
    hydrafacial: "",
    "chemical-peels-facials": "",
    "massage-body-wellness": "",
    "laser-hair-removal": "",
    microblading: "",
    "injectables-wellness": "",
    "japanese-head-spa": "",
    "spa-packages-membership": "",
    "mens-spa": "",
    "facial-skin-treatments": "",
    "hair-removal": "",
    "eyes-brows-permanent-makeup": "",
  };

  function isValidUrl(value) {
    if (typeof value !== "string") return false;
    var v = value.trim();
    if (!v) return false;
    try {
      // Accept absolute URLs only for booking targets
      var u = new URL(v);
      return u.protocol === "https:" || u.protocol === "http:";
    } catch (e) {
      return false;
    }
  }

  function getBookingUrl(params) {
    params = params || {};
    var bookingType = typeof params.bookingType === "string" ? params.bookingType : "";
    var serviceKey = typeof params.serviceKey === "string" ? params.serviceKey : "";

    if (bookingType === "membership") return PHOREST_MEMBERSHIP;
    if (bookingType === "gift-cards") return PHOREST_GIFT_CARDS;
    if (bookingType === "general") return PHOREST_GENERAL_BOOKING;

    if (serviceKey) {
      var candidate = SERVICE_BOOKING_LINKS[serviceKey];
      if (isValidUrl(candidate)) return candidate.trim();
      return PHOREST_GENERAL_BOOKING;
    }

    return PHOREST_GENERAL_BOOKING;
  }

  function ensureExternalAttrs(a, href) {
    if (!(a instanceof HTMLAnchorElement)) return;
    if (typeof href !== "string") return;
    if (/^https?:\/\//i.test(href)) {
      a.target = "_blank";
      a.rel = "noopener noreferrer";
    }
  }

  function initBookingLinks() {
    var nodes = document.querySelectorAll("[data-booking-type], [data-service]");
    if (!nodes.length) return;

    nodes.forEach(function (node) {
      if (!(node instanceof HTMLAnchorElement)) return;

      var bookingType = node.getAttribute("data-booking-type") || "";
      var serviceKey = node.getAttribute("data-service") || "";

      var href = getBookingUrl({ bookingType: bookingType, serviceKey: serviceKey });
      node.href = href;
      ensureExternalAttrs(node, href);
    });
  }

  window.SPALENZA_BOOKING = {
    PHOREST_GENERAL_BOOKING: PHOREST_GENERAL_BOOKING,
    PHOREST_MEMBERSHIP: PHOREST_MEMBERSHIP,
    PHOREST_GIFT_CARDS: PHOREST_GIFT_CARDS,
    SERVICE_BOOKING_LINKS: SERVICE_BOOKING_LINKS,
    getBookingUrl: getBookingUrl,
    initBookingLinks: initBookingLinks,
  };
})();

