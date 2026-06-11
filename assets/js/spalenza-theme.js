(function ($) {
  "use strict";

  if (typeof WOW !== "undefined") {
    new WOW({ mobile: false }).init();
  }

  if ($.fn.owlCarousel && $(".testimonial-carousel").length) {
    $(".testimonial-carousel").owlCarousel({
      items: 1,
      loop: true,
      autoplay: true,
      autoplayTimeout: 6000,
      dots: true,
      nav: false,
    });
  }

  $(window).on("scroll", function () {
    if ($(this).scrollTop() > 200) {
      $(".back-top").fadeIn();
    } else {
      $(".back-top").fadeOut();
    }
  });

  $(".back-top a").on("click", function (e) {
    e.preventDefault();
    $("html, body").animate({ scrollTop: 0 }, 600);
  });

  $(".navbar-toggler").on("click", function () {
    $(this).toggleClass("collapsed");
  });
})(jQuery);
