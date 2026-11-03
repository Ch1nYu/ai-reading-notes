// Site behaviour: theme switch, home filters (FLIP + highlight), reveals, note TOC and progress.
(function () {
  "use strict";
  var doc = document.documentElement;
  var reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var EASE = "cubic-bezier(0.16, 1, 0.3, 1)";

  // ---- Scroll reveal -------------------------------------------------------
  // Items revealed in the same frame get increasing --i for a stagger.
  var revealIO = "IntersectionObserver" in window && !reduced
    ? new IntersectionObserver(function (entries) {
        var batch = 0;
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          en.target.style.setProperty("--i", batch++);
          en.target.classList.add("is-in");
          revealIO.unobserve(en.target);
        });
      }, { rootMargin: "0px 0px -8% 0px" })
    : null;
  var reveal = function (els) {
    Array.prototype.forEach.call(els, function (el) {
      el.setAttribute("data-reveal", "");
      if (revealIO) revealIO.observe(el); else el.classList.add("is-in");
    });
  };

  // ---- Theme switch: circular wipe from the toggle -----------------------
  var toggle = document.querySelector(".theme-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var next = doc.dataset.theme === "dark" ? "light" : "dark";
      var set = function () { doc.dataset.theme = next; localStorage.setItem("theme", next); };
      if (!document.startViewTransition || reduced) { set(); return; }
      var r = toggle.getBoundingClientRect();
      var x = r.left + r.width / 2, y = r.top + r.height / 2;
      var radius = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
      document.startViewTransition(set).ready.then(function () {
        doc.animate(
          { clipPath: ["circle(0px at " + x + "px " + y + "px)", "circle(" + radius + "px at " + x + "px " + y + "px)"] },
          { duration: 560, easing: EASE, pseudoElement: "::view-transition-new(root)" }
        );
      });
    });
  }

  // ---- Home ---------------------------------------------------------------
  var list = document.querySelector(".note-list");
  if (list) {
    var rows = Array.prototype.slice.call(list.querySelectorAll(".note-row"));
    var input = document.querySelector("[data-search]");
    var typeButtons = document.querySelectorAll("[data-type-filter]");
    var topicButtons = document.querySelectorAll("[data-topic-filter]");
    var countEl = document.querySelector("[data-count]");
    var emptyEl = document.querySelector(".empty");
    var thumb = document.querySelector(".segmented__thumb");
    var params = new URLSearchParams(location.search);
    var state = { q: params.get("q") || "", type: params.get("type") || "", topic: params.get("topic") || "" };

    // Keep original text so highlights can be rebuilt on every keystroke.
    rows.forEach(function (row) {
      row._title = row.querySelector(".note-row__title a");
      row._summary = row.querySelector(".note-row__summary");
      row._titleText = row._title.textContent;
      row._summaryText = row._summary.textContent;
    });
    var escapeHtml = function (s) {
      return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
    };
    var escapeRe = function (s) { return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); };
    var highlight = function (el, text, re) {
      if (!re) { el.textContent = text; return; }
      el.innerHTML = escapeHtml(text).replace(re, '<mark class="hit">$1</mark>');
    };

    var moveThumb = function () {
      var active = document.querySelector('[data-type-filter][aria-pressed="true"]');
      if (!thumb || !active) return;
      thumb.style.width = active.offsetWidth + "px";
      thumb.style.transform = "translateX(" + active.offsetLeft + "px)";
    };

    var setCount = function (n) {
      if (countEl.textContent === String(n)) return;
      countEl.textContent = n;
      countEl.classList.remove("tick");
      void countEl.offsetWidth; // restart animation
      countEl.classList.add("tick");
    };

    var apply = function (animate) {
      var terms = state.q.toLowerCase().split(/\s+/).filter(Boolean);
      var re = terms.length ? new RegExp("(" + terms.map(escapeRe).join("|") + ")", "gi") : null;

      // FLIP: remember where visible rows were.
      var before = new Map();
      if (animate && !reduced) rows.forEach(function (r) { if (!r.hidden) before.set(r, r.getBoundingClientRect().top); });

      var shown = 0;
      rows.forEach(function (row) {
        var ok = (!state.type || row.dataset.type === state.type) &&
          (!state.topic || (" " + row.dataset.topics + " ").indexOf(" " + state.topic + " ") !== -1) &&
          terms.every(function (t) { return row.dataset.text.indexOf(t) !== -1; });
        row.hidden = !ok;
        if (ok) {
          shown++;
          highlight(row._title, row._titleText, re);
          highlight(row._summary, row._summaryText, re);
        }
      });

      if (animate && !reduced) {
        var entering = 0;
        rows.forEach(function (row) {
          if (row.hidden) return;
          row.classList.add("is-in"); // filtering overrides scroll reveal
          var top = row.getBoundingClientRect().top;
          if (before.has(row)) {
            var dy = before.get(row) - top;
            if (Math.abs(dy) > 1) row.animate([{ transform: "translateY(" + dy + "px)" }, { transform: "none" }], { duration: 420, easing: EASE });
          } else if (top < innerHeight) {
            row.animate(
              [{ opacity: 0, transform: "translateY(14px) scale(0.985)" }, { opacity: 1, transform: "none" }],
              { duration: 420, easing: EASE, delay: Math.min(entering++, 8) * 45, fill: "backwards" }
            );
          }
        });
      }

      setCount(shown);
      emptyEl.hidden = shown !== 0;
      typeButtons.forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.typeFilter === state.type)); });
      topicButtons.forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.topicFilter === state.topic)); });
      moveThumb();

      var p = new URLSearchParams();
      if (state.q) p.set("q", state.q);
      if (state.type) p.set("type", state.type);
      if (state.topic) p.set("topic", state.topic);
      var qs = p.toString();
      history.replaceState(null, "", location.pathname + (qs ? "?" + qs : "") + location.hash);
    };

    var typing;
    input.value = state.q;
    input.addEventListener("input", function () {
      clearTimeout(typing);
      typing = setTimeout(function () { state.q = input.value.trim(); apply(true); }, 90);
    });
    typeButtons.forEach(function (b) {
      b.addEventListener("click", function () { state.type = b.dataset.typeFilter; apply(true); });
    });
    topicButtons.forEach(function (b) {
      b.addEventListener("click", function () {
        state.topic = state.topic === b.dataset.topicFilter ? "" : b.dataset.topicFilter;
        apply(true);
      });
    });
    document.querySelectorAll("[data-topic-link]").forEach(function (a) {
      a.addEventListener("click", function (e) {
        e.preventDefault();
        state.topic = a.dataset.topicLink;
        document.getElementById("notes").scrollIntoView();
        apply(true);
      });
    });
    document.querySelector("[data-reset]").addEventListener("click", function () {
      state = { q: "", type: "", topic: "" };
      input.value = "";
      apply(true);
    });
    // "/" focuses search, Escape clears it.
    document.addEventListener("keydown", function (e) {
      if (e.key === "/" && document.activeElement !== input) { e.preventDefault(); input.focus(); }
      else if (e.key === "Escape" && document.activeElement === input) { input.value = ""; state.q = ""; apply(true); }
    });
    addEventListener("resize", moveThumb);
    if (document.fonts) document.fonts.ready.then(moveThumb);

    // Morph the clicked title into the note page heading.
    list.addEventListener("click", function (e) {
      var a = e.target.closest(".note-row__title a");
      if (a) a.closest(".note-row__title").style.viewTransitionName = "note-title";
    });
    addEventListener("pageshow", function () {
      list.querySelectorAll(".note-row__title").forEach(function (t) { t.style.viewTransitionName = ""; });
    });

    apply(false);
    reveal(rows.filter(function (r) { return !r.hidden; }));
    reveal(document.querySelectorAll(".index__head, .filters, .topic-index .section-title, .topic-grid li"));

    // Count up the hero stats.
    if (!reduced) {
      document.querySelectorAll("[data-countup]").forEach(function (el, i) {
        var target = +el.textContent, start = null;
        el.textContent = "0";
        var step = function (t) {
          if (start === null) start = t + 450 + i * 90;
          var p = Math.min(1, Math.max(0, (t - start) / 900));
          el.textContent = Math.round(target * (1 - Math.pow(1 - p, 4)));
          if (p < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
      });
    }
  }

  // ---- Note: reveal, reading progress, TOC current section ---------------
  var prose = document.querySelector(".prose");
  if (prose) {
    reveal(prose.querySelectorAll(":scope > h2, :scope > h3, :scope > .table-wrap, :scope > .abstract, :scope > ul"));
    reveal(document.querySelectorAll(".note__foot"));

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
    // Current section = last heading scrolled past the top quarter of the viewport.
    var headings = Array.prototype.slice.call(prose.querySelectorAll("h2[id], h3[id]"));
    var current = null, ticking = false;
    var updateToc = function () {
      ticking = false;
      var line = innerHeight * 0.25, active = null;
      for (var i = 0; i < headings.length; i++) {
        if (headings[i].getBoundingClientRect().top <= line) active = headings[i]; else break;
      }
      var link = active ? links[active.id] : null;
      if (link === current) return;
      if (current) current.removeAttribute("aria-current");
      if (link) link.setAttribute("aria-current", "true");
      current = link;
    };
    if (headings.length) {
      addEventListener("scroll", function () {
        if (!ticking) { ticking = true; requestAnimationFrame(updateToc); }
      }, { passive: true });
      updateToc();
    }
  }
})();
