<script>
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    // Target all H2 elements inside the main content area
    var contentArea = document.getElementById("quarto-document-content") ||
                      document.querySelector(".quarto-container main") ||
                      document.querySelector("main");

    if (!contentArea) return;

    var h2s = Array.from(contentArea.querySelectorAll("h2"));

    h2s.forEach(function (h2, idx) {
      // Collect all sibling elements until the next H1 or H2
      var siblings = [];
      var next = h2.nextElementSibling;

      while (next && !["H1", "H2"].includes(next.tagName)) {
        siblings.push(next);
        next = next.nextElementSibling;
      }

      if (siblings.length === 0) return;

      // Build accordion wrapper
      var wrapper = document.createElement("div");
      wrapper.className = "section-accordion";
      h2.parentNode.insertBefore(wrapper, h2);

      // Header row (the h2 becomes the toggle)
      var header = document.createElement("div");
      header.className = "section-accordion-header";

      // Move h2 into header
      var h2Clone = document.createElement("h2");
      h2Clone.innerHTML = h2.innerHTML;
      h2Clone.id = h2.id;  // preserve anchor
      h2.replaceWith(h2Clone);

      var chevron = document.createElement("span");
      chevron.className = "section-accordion-chevron";
      chevron.innerHTML = "&#9660;"; // ▼

      header.appendChild(h2Clone);
      header.appendChild(chevron);
      wrapper.appendChild(header);

      // Body
      var body = document.createElement("div");
      body.className = "section-accordion-body";
      siblings.forEach(function (el) { body.appendChild(el); });
      wrapper.appendChild(body);

      // Toggle behaviour
      var open = true;

      header.addEventListener("click", function () {
        open = !open;
        body.style.display = open ? "" : "none";
        chevron.classList.toggle("collapsed", !open);
      });
    });
  });
})();
</script>
