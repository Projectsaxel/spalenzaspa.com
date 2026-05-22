(function () {
  document.querySelectorAll(".navbar .navbar-toggler").forEach(function (btn) {
    var target = document.querySelector(btn.getAttribute("data-target"));
    if (!target) return;

    btn.addEventListener("click", function () {
      var open = target.classList.toggle("show");
      btn.classList.toggle("collapsed", !open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });
})();
