function initFaqAccordions() {
  var containers = document.querySelectorAll(".faq-list");
  if (!containers.length) return;

  containers.forEach(function (list) {
    // Initialize a11y attributes
    var items = list.querySelectorAll(".faq-item");
    items.forEach(function (item, index) {
      var button = item.querySelector(".faq-question");
      var answer = item.querySelector(".faq-answer");
      if (!(button instanceof HTMLButtonElement) || !(answer instanceof HTMLElement)) {
        return;
      }

      var idBase = "faq-" + (list.id || "group") + "-" + index;
      var answerId = answer.id || idBase + "-answer";
      answer.id = answerId;

      button.setAttribute("aria-controls", answerId);
      button.setAttribute("aria-expanded", item.classList.contains("is-open") ? "true" : "false");

      // Use hidden attribute for screen readers
      if (item.classList.contains("is-open")) {
        answer.hidden = false;
      } else {
        answer.hidden = true;
      }
    });

    list.addEventListener("click", function (event) {
      var target = event.target;
      if (!(target instanceof HTMLElement)) return;

      var button = target.closest(".faq-question");
      if (!button) return;

      var item = button.closest(".faq-item");
      if (!item) return;

      var isOpen = item.classList.contains("is-open");
      // close others inside same list
      list.querySelectorAll(".faq-item.is-open").forEach(function (openItem) {
        if (openItem !== item) {
          openItem.classList.remove("is-open");
          var openBtn = openItem.querySelector(".faq-question");
          var openAns = openItem.querySelector(".faq-answer");
          if (openBtn instanceof HTMLElement) openBtn.setAttribute("aria-expanded", "false");
          if (openAns instanceof HTMLElement) openAns.hidden = true;
        }
      });
      item.classList.toggle("is-open", !isOpen);

      // Update aria + hidden on the clicked item
      var answer = item.querySelector(".faq-answer");
      var expanded = !isOpen;
      if (button instanceof HTMLElement) {
        button.setAttribute("aria-expanded", expanded ? "true" : "false");
      }
      if (answer instanceof HTMLElement) {
        answer.hidden = !expanded;
      }
    });
  });
}

