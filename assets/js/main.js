document.addEventListener("DOMContentLoaded", function () {
  if (typeof initNavigation === "function") {
    initNavigation();
  }
  if (typeof initFaqAccordions === "function") {
    initFaqAccordions();
  }
  if (
    window.SPALENZA_BOOKING &&
    typeof window.SPALENZA_BOOKING.initBookingLinks === "function"
  ) {
    window.SPALENZA_BOOKING.initBookingLinks();
  }
});

