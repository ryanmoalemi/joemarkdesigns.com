(function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");

  function closeNav() {
    if (!nav || !toggle) return;
    nav.classList.remove("is-open");
    toggle.setAttribute("aria-expanded", "false");
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", closeNav);
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") closeNav();
    });
  }

  var dialog = document.getElementById("plan-dialog");
  var image = document.getElementById("plan-dialog-img");
  var title = document.getElementById("plan-dialog-title");
  if (!dialog || !image || !title) return;

  document.querySelectorAll("[data-plan]").forEach(function (link) {
    link.addEventListener("click", function (event) {
      if (typeof dialog.showModal !== "function") return;
      event.preventDefault();
      title.textContent = link.getAttribute("data-plan") || "Sample drawing";
      image.src = link.getAttribute("href");
      image.alt = link.getAttribute("data-plan-alt") || title.textContent;
      dialog.showModal();
    });
  });

  var closeButton = dialog.querySelector(".dialog-close");
  if (closeButton) {
    closeButton.addEventListener("click", function () {
      dialog.close();
    });
  }

  dialog.addEventListener("click", function (event) {
    var bounds = dialog.getBoundingClientRect();
    var inside =
      event.clientX >= bounds.left &&
      event.clientX <= bounds.right &&
      event.clientY >= bounds.top &&
      event.clientY <= bounds.bottom;
    if (!inside) dialog.close();
  });
})();
