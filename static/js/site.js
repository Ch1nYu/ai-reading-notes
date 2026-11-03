// Site behaviour: theme toggle, home filters, note TOC highlight, reading progress.
(function () {
  "use strict";
  var doc = document.documentElement;

  // ---- Theme toggle -------------------------------------------------------
  var toggle = document.querySelector(".theme-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var next = doc.dataset.theme === "dark" ? "light" : "dark";
      doc.dataset.theme = next;
      localStorage.setItem("theme", next);
    });
  }

  // ---- Home: search + type + topic filters, synced to the URL ------------
  var list = document.querySelector(".note-list");
  if (list) {
    var rows = Array.prototype.slice.call(list.querySelectorAll(".note-row"));
    var input = document.querySelector("[data-search]");
    var typeButtons = document.querySelectorAll("[data-type-filter]");
    var topicButtons = document.querySelectorAll("[data-topic-filter]");
    var countEl = document.querySelector("[data-count]");
    var emptyEl = document.querySelector(".empty");
    var params = new URLSearchParams(location.search);
    var state = { q: params.get("q") || "", type: params.get("type") || "", topic: params.get("topic") || "" };

    var apply = function () {
      var terms = state.q.toLowerCase().split(/\s+/).filter(Boolean);
      var shown = 0;
      rows.forEach(function (row) {
        var ok = (!state.type || row.dataset.type === state.type) &&
          (!state.topic || (" " + row.dataset.topics + " ").indexOf(" " + state.topic + " ") !== -1) &&
          terms.every(function (t) { return row.dataset.text.indexOf(t) !== -1; });
        row.hidden = !ok;
        if (ok) shown++;
      });
      countEl.textContent = shown;
      emptyEl.hidden = shown !== 0;
      typeButtons.forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.typeFilter === state.type)); });
      topicButtons.forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.topicFilter === state.topic)); });

      var p = new URLSearchParams();
      if (state.q) p.set("q", state.q);
      if (state.type) p.set("type", state.type);
      if (state.topic) p.set("topic", state.topic);
      var qs = p.toString();
      history.replaceState(null, "", location.pathname + (qs ? "?" + qs : "") + location.hash);
    };

    input.value = state.q;
    input.addEventListener("input", function () { state.q = input.value.trim(); apply(); });
    typeButtons.forEach(function (b) {
      b.addEventListener("click", function () { state.type = b.dataset.typeFilter; apply(); });
    });
    topicButtons.forEach(function (b) {
      b.addEventListener("click", function () {
        state.topic = state.topic === b.dataset.topicFilter ? "" : b.dataset.topicFilter;
        apply();
      });
    });
    document.querySelectorAll("[data-topic-link]").forEach(function (a) {
      a.addEventListener("click", function (e) {
        e.preventDefault();
        state.topic = a.dataset.topicLink;
        apply();
        document.getElementById("notes").scrollIntoView();
      });
    });
    document.querySelector("[data-reset]").addEventListener("click", function () {
      state = { q: "", type: "", topic: "" };
      input.value = "";
      apply();
    });
    // "/" focuses search, Escape clears it.
    document.addEventListener("keydown", function (e) {
      if (e.key === "/" && document.activeElement !== input) { e.preventDefault(); input.focus(); }
      else if (e.key === "Escape" && document.activeElement === input) { input.value = ""; state.q = ""; apply(); }
    });
    apply();
  }

  // ---- Note: reading progress + TOC current section ----------------------
  var prose = document.querySelector(".prose");
  if (prose) {
    var bar = document.querySelector(".progress span");
    var onScroll = function () {
      var rect = prose.getBoundingClientRect();
      var total = rect.height - innerHeight * 0.6;
      var ratio = total > 0 ? Math.min(1, Math.max(0, -rect.top / total)) : 1;
      bar.style.transform = "scaleX(" + ratio + ")";
    };
    addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    // On narrow screens the TOC sits above the text; start it collapsed.
    var tocDetails = document.querySelector(".toc details");
    if (tocDetails && matchMedia("(max-width: 1023px)").matches) tocDetails.open = false;

    var links = {};
    document.querySelectorAll(".toc a").forEach(function (a) { links[a.getAttribute("href").slice(1)] = a; });
    var headings = prose.querySelectorAll("h2[id], h3[id]");
    if (headings.length && "IntersectionObserver" in window) {
      var current = null;
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting && links[en.target.id]) {
            if (current) current.removeAttribute("aria-current");
            current = links[en.target.id];
            current.setAttribute("aria-current", "true");
          }
        });
      }, { rootMargin: "-15% 0px -75% 0px" });
      headings.forEach(function (h) { io.observe(h); });
    }
  }
})();
