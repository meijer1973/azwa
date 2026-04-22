(function () {
  var THEME_LABELS = {
    "basisfunctionaliteiten-d5": "Basisfunctionaliteiten (D5)",
    "basisinfrastructuur-d6": "Basisinfrastructuur (D6)",
    "governance-en-regie": "Governance en regie",
    financiering: "Financiering",
    "monitoring-en-leren": "Monitoring en leren",
    "mentale-gezondheid": "Mentale gezondheid",
  };

  function escapeHtml(value) {
    return (value || "")
      .toString()
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function normalize(value) {
    return (value || "")
      .toString()
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");
  }

  async function initSearch() {
    const input = document.getElementById("site-search");
    const results = document.getElementById("search-results");
    if (!input || !results) {
      return;
    }

    let index = [];
    try {
      const response = await fetch(window.AZWA_SEARCH_INDEX_URL);
      if (response.ok) {
        index = await response.json();
      }
    } catch (error) {
      return;
    }

    const closeResults = function () {
      results.hidden = true;
      results.innerHTML = "";
    };

    input.addEventListener("input", function () {
      const query = normalize(input.value);
      if (query.length < 2) {
        closeResults();
        return;
      }

      const matches = index
        .filter(function (entry) {
          const haystack = normalize(
            [entry.title, entry.subtitle, entry.summary, (entry.aliases || []).join(" "), (entry.themes || []).join(" "), entry.page_type]
              .filter(Boolean)
              .join(" ")
          );
          return haystack.includes(query);
        })
        .slice(0, 8);

      if (!matches.length) {
        results.hidden = false;
        results.innerHTML = '<div class="search-results__link">Geen resultaten gevonden.</div>';
        return;
      }

      const items = matches
        .map(function (entry) {
          const href = (window.AZWA_SITE_ROOT || "./") + entry.url;
          return (
            '<li class="search-results__item">' +
            '<a class="search-results__link" href="' + escapeHtml(href) + '">' +
            escapeHtml(entry.title) +
            '<span class="search-results__meta">' +
            escapeHtml([entry.page_type_label, entry.subtitle].filter(Boolean).join(" | ")) +
            "</span>" +
            "</a>" +
            "</li>"
          );
        })
        .join("");

      results.hidden = false;
      results.innerHTML = '<ul class="search-results__list">' + items + "</ul>";
    });

    input.addEventListener("blur", function () {
      window.setTimeout(closeResults, 120);
    });
  }

  function initDashboardFilters() {
    const rows = Array.from(document.querySelectorAll("[data-dashboard-row]"));
    if (!rows.length) {
      return;
    }

    const filters = Array.from(document.querySelectorAll("[data-dashboard-filter]"));
    const emptyState = document.getElementById("dashboard-empty-state");
    const params = new URLSearchParams(window.location.search);

    filters.forEach(function (filter) {
      var key = filter.getAttribute("data-dashboard-filter");
      var initialValue = params.get(key);
      if (initialValue) {
        filter.value = initialValue;
      }
    });

    function applyFilters() {
      const active = {};
      filters.forEach(function (filter) {
        active[filter.getAttribute("data-dashboard-filter")] = normalize(filter.value);
      });

      let visibleCount = 0;
      rows.forEach(function (row) {
        const visible = filters.every(function (filter) {
          const key = filter.getAttribute("data-dashboard-filter");
          const selected = active[key];
          if (!selected) {
            return true;
          }
          return normalize(row.getAttribute("data-" + key)).includes(selected);
        });
        row.hidden = !visible;
        if (visible) {
          visibleCount += 1;
        }
      });

      if (emptyState) {
        emptyState.hidden = visibleCount !== 0;
      }
    }

    filters.forEach(function (filter) {
      filter.addEventListener("change", applyFilters);
    });

    applyFilters();
  }

  function initIssueFilters() {
    const cards = Array.from(document.querySelectorAll("[data-issue-card]"));
    if (!cards.length) {
      return;
    }

    const params = new URLSearchParams(window.location.search);
    const activeTheme = normalize(params.get("theme"));
    const sections = Array.from(document.querySelectorAll("[data-issue-section]"));
    const status = document.getElementById("issue-filter-status");
    const emptyState = document.getElementById("issue-filter-empty-state");

    if (!activeTheme) {
      return;
    }

    var visibleCount = 0;
    cards.forEach(function (card) {
      var matchesTheme = normalize(card.getAttribute("data-theme")).includes(activeTheme);
      card.hidden = !matchesTheme;
      if (matchesTheme) {
        visibleCount += 1;
      }
    });

    sections.forEach(function (section) {
      var hasVisibleCards = Boolean(section.querySelector("[data-issue-card]:not([hidden])"));
      section.hidden = !hasVisibleCards;
    });

    if (status) {
      var label = THEME_LABELS[params.get("theme")] || params.get("theme");
      status.hidden = false;
      status.innerHTML =
        'Filter actief op thema: <strong>' +
        escapeHtml(label) +
        '</strong>. <a href="index.html">Wis filter</a>';
    }

    if (emptyState) {
      emptyState.hidden = visibleCount !== 0;
    }
  }

  function revealHashTarget() {
    if (!window.location.hash) {
      return;
    }

    var targetId = decodeURIComponent(window.location.hash.slice(1));
    if (!targetId) {
      return;
    }

    var target = document.getElementById(targetId);
    if (!target) {
      return;
    }

    var current = target;
    while (current) {
      if (current.tagName === "DETAILS") {
        current.open = true;
      }
      current = current.parentElement;
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    initSearch();
    initDashboardFilters();
    initIssueFilters();
    revealHashTarget();
  });

  window.addEventListener("hashchange", revealHashTarget);
})();
