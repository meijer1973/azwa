(function () {
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
  }

  document.addEventListener("DOMContentLoaded", function () {
    initSearch();
    initDashboardFilters();
  });
})();
