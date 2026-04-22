from __future__ import annotations

import html
import json
import posixpath
from pathlib import Path, PurePosixPath
from string import Template


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data" / "site"
DIST_DIR = REPO_ROOT / "dist"
TEMPLATE_PATH = REPO_ROOT / "templates" / "base.html"
TAXONOMY_PATH = REPO_ROOT / "config" / "site_taxonomy.json"
ASSETS_DIR = REPO_ROOT / "assets"
TIMELINE_VIEW_PATH = DATA_DIR / "site_timeline_view.json"
THEMES_VIEW_PATH = DATA_DIR / "site_themes_view.json"
REFERENCE_VIEW_PATH = DATA_DIR / "site_reference_view.json"
SOURCES_VIEW_PATH = DATA_DIR / "site_sources_view.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def split_route_parts(route: str) -> tuple[str, str, str]:
    fragment = ""
    query = ""
    base_route = route
    if "#" in base_route:
        base_route, fragment = base_route.split("#", 1)
    if "?" in base_route:
        base_route, query = base_route.split("?", 1)
    return base_route or "/", query, fragment


def route_to_output_path(route: str) -> PurePosixPath:
    route, _, _ = split_route_parts(route)
    if route == "/":
        return PurePosixPath("index.html")
    normalized = route.strip("/")
    return PurePosixPath(normalized) / "index.html"


def relative_link(current_route: str, target_route: str) -> str:
    target_route, query, fragment = split_route_parts(target_route)
    current_path = route_to_output_path(current_route)
    if target_route.startswith("/assets/"):
        target_path = PurePosixPath(target_route.lstrip("/"))
    elif target_route == "/search-index.json":
        target_path = PurePosixPath("search-index.json")
    else:
        target_path = route_to_output_path(target_route)
    relative = posixpath.relpath(str(target_path), start=str(current_path.parent))
    if query:
        relative = f"{relative}?{query}"
    if fragment:
        return f"{relative}#{fragment}"
    return relative


def root_prefix(route: str) -> str:
    path = route_to_output_path(route)
    depth = len(path.parts) - 1
    return "./" if depth == 0 else "../" * depth


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    ensure_parent(path)
    path.write_text(content, encoding="utf-8")


def esc(value: str | None) -> str:
    return html.escape(value or "")


def render_navigation(current_route: str, navigation: list[dict]) -> str:
    links = []
    for item in navigation:
        url = item["url"]
        active = current_route == url or (url != "/" and current_route.startswith(url))
        classes = "site-nav__link"
        if active:
            classes += " site-nav__link--active"
        links.append(
            f'<a class="{classes}" data-priority="{esc(item["priority"])}" href="{esc(relative_link(current_route, url))}">{esc(item["label"])}</a>'
        )
    return "".join(links)


def render_breadcrumbs(current_route: str, crumbs: list[tuple[str, str]]) -> str:
    if not crumbs:
        return ""
    parts = []
    for label, url in crumbs[:-1]:
        parts.append(f'<a href="{esc(relative_link(current_route, url))}">{esc(label)}</a>')
    parts.append(f"<span>{esc(crumbs[-1][0])}</span>")
    return '<nav class="breadcrumbs" aria-label="Broodkruimelpad">' + " / ".join(parts) + "</nav>"


def page_intro(title: str, summary: str, meta_items: list[str], notice: str | None = None) -> str:
    meta_html = "".join(f'<span class="page-meta__item">{esc(item)}</span>' for item in meta_items if item)
    notice_html = f'<div class="notice">{esc(notice)}</div>' if notice else ""
    return (
        notice_html
        + '<header class="page-header">'
        + f'<h1 class="page-header__title">{esc(title)}</h1>'
        + f'<p class="page-header__summary">{esc(summary)}</p>'
        + f'<div class="page-meta">{meta_html}</div>'
        + "</header>"
    )


def render_tag_row(current_route: str, tags: list[str], review_note: str | None = None, review_href: str | None = None) -> str:
    tag_html = "".join(f'<span class="tag">{esc(tag)}</span>' for tag in tags if tag)
    if review_note:
        if review_href:
            tag_html += f'<a class="tag tag--review tag--link" href="{esc(relative_link(current_route, review_href))}">{esc(review_note)}</a>'
        else:
            tag_html += f'<span class="tag tag--review">{esc(review_note)}</span>'
    return f'<div class="tag-row">{tag_html}</div>' if tag_html else ""


def issue_type_label(issue_type: str) -> str:
    labels = {
        "decision": "besluitvraag",
        "action": "opvolgactie",
        "dependency": "afhankelijkheid",
        "risk": "risico",
    }
    return labels.get(issue_type, issue_type)


def render_card(
    title: str,
    body: str,
    meta: list[str] | None = None,
    footer: str | None = None,
    href: str | None = None,
    whole_card: bool = False,
) -> str:
    title_html = f'<h3 class="card__title"><a href="{esc(href)}">{esc(title)}</a></h3>' if href and not whole_card else f'<h3 class="card__title">{esc(title)}</h3>'
    meta_html = ""
    if meta:
        meta_html = "".join(f'<div class="card__meta">{esc(item)}</div>' for item in meta if item)
    footer_html = f'<div class="card__footer">{footer}</div>' if footer else ""
    if href and whole_card:
        return f'<a class="card card--link" href="{esc(href)}">{title_html}<p>{body}</p>{meta_html}{footer_html}</a>'
    return f'<article class="card">{title_html}<p>{body}</p>{meta_html}{footer_html}</article>'


def render_summary_boxes(current_route: str, items: list[dict]) -> str:
    blocks = []
    for item in items:
        href = item.get("page_url")
        title = item.get("title") or item.get("reason_label") or ""
        if href:
            blocks.append(
                f'<a class="summary-box summary-box--link" href="{esc(relative_link(current_route, href))}">'
                + f'<span class="summary-box__metric">{esc(str(item["metric"]))}</span>'
                + f'<h3 class="card__title">{esc(title)}</h3>'
                + f'<p>{esc(item["summary"])}</p>'
                + "</a>"
            )
        else:
            blocks.append(
                '<article class="summary-box">'
                + f'<span class="summary-box__metric">{esc(str(item["metric"]))}</span>'
                + f'<h3 class="card__title">{esc(title)}</h3>'
                + f'<p>{esc(item["summary"])}</p>'
                + "</article>"
            )
    return '<div class="summary-grid">' + "".join(blocks) + "</div>"


def render_link_pills(current_route: str, items: list[dict]) -> str:
    if not items:
        return ""
    links = []
    for item in items:
        links.append(f'<a class="tag tag--link" href="{esc(relative_link(current_route, item["href"]))}">{esc(item["label"])}</a>')
    return '<div class="tag-row tag-row--links">' + "".join(links) + "</div>"


def render_document_refs(current_route: str, document_refs: list[dict]) -> str:
    if not document_refs:
        return '<div class="empty-state">Geen bronverwijzingen beschikbaar.</div>'
    items = []
    for ref in document_refs:
        target = relative_link(current_route, ref["page_url"]) if ref.get("page_url") else ref["source_url"]
        items.append(
            "<li>"
            + f'<strong><a href="{esc(target)}">{esc(ref["title"])}</a></strong><br>'
            + f'<span class="list-meta">{esc(ref["publisher"])} | {esc(ref["publication_date"] or "datum onbekend")} | {esc(ref["jurisdiction_level"])}</span><br>'
            + f'<span class="list-meta">Relevante onderwerpen: {esc(", ".join(ref.get("topics", [])))}</span>'
            + "</li>"
        )
    return '<ul class="stack-list">' + "".join(items) + "</ul>"


def render_evidence_refs(current_route: str, evidence_refs: list[dict]) -> str:
    if not evidence_refs:
        return '<div class="empty-state">Geen bronverwijzingen beschikbaar.</div>'
    items = []
    seen: set[tuple[str, str]] = set()
    for evidence in evidence_refs:
        dedupe_key = (evidence["document_id"], evidence["topic_label"])
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        target = relative_link(current_route, evidence["page_url"]) if evidence.get("page_url") else evidence["source_url"]
        note = f'<br><span class="list-meta">{esc(evidence["authority_note"])}</span>' if evidence.get("authority_note") else ""
        items.append(
            "<li>"
            + f'<strong><a href="{esc(target)}">{esc(evidence["document_title"])}</a></strong><br>'
            + f'<span class="list-meta">{esc(evidence["publisher"])} | {esc(evidence["publication_date"] or "datum onbekend")} | {esc(evidence["topic_label"])}</span>'
            + note
            + "</li>"
        )
    return '<ul class="stack-list">' + "".join(items) + "</ul>"


def render_decision_card(current_route: str, decision: dict) -> str:
    tags = [decision["status"], decision["linked_domain_label"]]
    body = (
        f"{esc(decision['decision_question'])}<br>"
        f'<span class="list-meta">Waarom nodig: {esc(decision["why_decision_required"])}</span><br>'
        f'<span class="list-meta">Volgende formele stap: {esc(decision["next_formal_step"])}</span><br>'
        f'<span class="list-meta">Gevolg bij uitblijven: {esc(decision["consequences_of_non_decision"])}</span>'
    )
    review_href = None
    if decision.get("review_note") and decision.get("review_details"):
        review_href = f'{decision["page_url"]}{decision["review_details"]["section_url"]}'
    footer = render_tag_row(current_route, tags, decision.get("review_note"), review_href=review_href)
    card_html = render_card(
        decision["title"],
        body,
        meta=[decision["responsible_level"]],
        footer=footer,
        href=relative_link(current_route, decision["page_url"]),
    )
    return (
        '<div class="issue-card" data-issue-card="decision" '
        + f'data-theme="{esc(",".join(decision.get("linked_theme_ids", [])))}">'
        + card_html
        + "</div>"
    )


def render_action_card(current_route: str, action: dict) -> str:
    tags = [action["status"], action["linked_domain_label"]]
    body = (
        f"{esc(action['action_statement'])}<br>"
        f'<span class="list-meta">Beoogd resultaat: {esc(action["intended_outcome"])}</span><br>'
        f'<span class="list-meta">Volgende mijlpaal: {esc(action["next_milestone"])}</span><br>'
        f'<span class="list-meta">Gevolg bij uitblijven: {esc(action["consequences_if_not_followed_up"])}</span>'
    )
    footer = render_tag_row(current_route, tags)
    card_html = render_card(
        action["title"],
        body,
        meta=[action["owner"]],
        footer=footer,
        href=relative_link(current_route, action["page_url"]),
    )
    return (
        '<div class="issue-card" data-issue-card="action" '
        + f'data-theme="{esc(",".join(action.get("linked_theme_ids", [])))}">'
        + card_html
        + "</div>"
    )


def render_home(route: str, home_view: dict) -> str:
    sections = [
        '<section class="section"><h2>Bestuurlijk overzicht</h2>'
        + f'<div class="notice">{esc(home_view["executive_summary"])}</div></section>',
        '<section class="section"><h2>Huidige besluitvragen</h2><div class="card-grid">'
        + "".join(render_decision_card(route, item) for item in home_view["top_decisions"])
        + "</div></section>",
        '<section class="section"><h2>Huidige opvolgacties</h2><div class="card-grid">'
        + "".join(render_action_card(route, item) for item in home_view["top_actions"])
        + "</div></section>",
        '<section class="section"><h2>Huidige implementatiestatus</h2>'
        + render_summary_boxes(route, home_view["implementation_status_blocks"])
        + "</section>",
        '<section class="section"><h2>Belangrijkste risico\'s en afhankelijkheden</h2><div class="card-grid">'
        + "".join(
            render_card(
                item["title"],
                esc(item["summary"]),
                meta=[item["linked_domain"]],
                href=relative_link(route, item["page_url"]),
            )
            for item in home_view["key_risks"] + home_view["key_dependencies"]
        )
        + "</div></section>",
        '<section class="section"><h2>Nabije tijdlijn</h2><ul class="stack-list">'
        + "".join(
            "<li>"
            + f'<strong><a href="{esc(relative_link(route, item["page_url"]))}">{esc(item["date_label"])} - {esc(item["title"])}</a></strong><br>'
            + f'<span class="list-meta">{esc(item["linked_domain"])}</span><br>'
            + esc(item["summary"])
            + "</li>"
            for item in home_view["near_term_timeline"]
        )
        + "</ul></section>",
        '<section class="section"><h2>Strategische thema\'s</h2><div class="card-grid">'
        + "".join(
            render_card(
                item["title"],
                esc(item["summary"]),
                footer=render_link_pills(
                    route,
                    [
                        {"label": f'{item["linked_decision_count"]} besluitvragen', "href": item["decision_page_url"]},
                        {"label": f'{item["linked_action_count"]} opvolgacties', "href": item["action_page_url"]},
                    ],
                ),
                href=relative_link(route, item["page_url"]),
            )
            for item in home_view["featured_themes"]
        )
        + "</div></section>",
        '<section class="section"><h2>Recente wijzigingen in de bronbasis</h2><ul class="stack-list">'
        + "".join(
            "<li>"
            + f'<strong><a href="{esc(item["source_url"])}">{esc(item["title"])}</a></strong><br>'
            + f'<span class="list-meta">{esc(item["publication_date"])} | {esc(item["document_type"])}</span>'
            + "</li>"
            for item in home_view["recent_changes"]
        )
        + "</ul></section>",
        '<section class="section"><h2>Ondersteunende navigatie</h2><div class="card-grid">'
        + "".join(
            render_card(
                item["label"],
                "Secundaire toegang voor naslag en bronverwijzing.",
                href=relative_link(route, item["url"]),
                whole_card=True,
            )
            for item in home_view["supporting_navigation"]
        )
        + "</div></section>",
    ]
    return "".join(sections)


def render_almere(route: str, almere_view: dict) -> str:
    sections = [
        '<section class="section" id="huidig-beeld"><h2>Huidig bestuurlijk beeld</h2>'
        + f'<div class="notice">{esc(almere_view["current_picture"])}</div></section>',
        '<section class="section" id="landelijke-basis-zichtbaar"><h2>Landelijke basis die in de bronbasis zichtbaar is</h2><ul class="stack-list">'
        + "".join(
            "<li>"
            + f'<strong>{esc(item["title"])}</strong><br>'
            + esc(item["summary"])
            + "<br>"
            + f'<span class="list-meta">{esc(item["scope_label"])}</span>'
            + "</li>"
            for item in almere_view["expected_municipal_responsibilities"]
        )
        + "</ul></section>",
        '<section class="section" id="wat-al-in-beeld-is"><h2>Wat in de huidige bronbasis al zichtbaar is</h2><ul class="stack-list">'
        + "".join(
            "<li>"
            + f'<strong>{esc(item["title"])}</strong><br>'
            + esc(item["summary"])
            + "</li>"
            for item in almere_view["current_local_state"]
        )
        + "</ul></section>",
        '<section class="section" id="lokale-hiaten"><h2>Belangrijkste hiaten</h2><ul class="stack-list">'
        + "".join(
            "<li>"
            + f'<strong>{esc(item["title"])}</strong><br>'
            + esc(item["summary"])
            + "</li>"
            for item in almere_view["local_gaps"]
        )
        + "</ul></section>",
        '<section class="section" id="leiding-en-regie"><h2>Wat bestuurlijke regie vraagt</h2><ul class="stack-list">'
        + "".join(f"<li>{esc(item)}</li>" for item in almere_view["leadership_requirements"])
        + "</ul></section>",
        '<section class="section"><h2>Huidige besluitvragen</h2><div class="card-grid">'
        + "".join(render_decision_card(route, item) for item in almere_view["current_decisions"])
        + "</div></section>",
        '<section class="section"><h2>Huidige opvolgacties</h2><div class="card-grid">'
        + "".join(render_action_card(route, item) for item in almere_view["current_actions"])
        + "</div></section>",
        '<section class="section" id="menselijke-duiding"><h2>Menselijke duiding en reviewpunten</h2>'
        + render_summary_boxes(route, almere_view["review_reason_summary"])
        + "".join(
            '<section class="section section--nested" id="'
            + esc(group["anchor_id"])
            + '"><h3>'
            + esc(group["reason_label"])
            + "</h3><p>"
            + esc(group["summary"])
            + '</p><ul class="stack-list">'
            + "".join(
                "<li>"
                + f'<strong>{esc(item["document_title"])}</strong>'
                + (f'<br><span class="list-meta">Onderwerp: {esc(item["topic_label"])}</span>' if item.get("topic_label") else "")
                + "<br>"
                + esc(item["summary"])
                + "<br>"
                + f'<span class="list-meta">Aanbevolen vervolgstap: {esc(item["recommended_action"])}</span>'
                + "</li>"
                for item in group["items"]
            )
            + "</ul></section>"
            for group in almere_view["review_groups"]
        )
        + "</section>",
        '<section class="section" id="externe-afhankelijkheden"><h2>Externe afhankelijkheden</h2><ul class="stack-list">'
        + "".join(
            "<li>"
            + f'<strong>{esc(item["title"])}</strong><br>'
            + esc(item["summary"])
            + "<br>"
            + f'<span class="list-meta">Volgende stap: {esc(item["next_step"])}</span>'
            + "</li>"
            for item in almere_view["external_dependencies"]
        )
        + "</ul></section>",
        '<section class="section" id="onzekerheden"><h2>Ondersteunende bronverwijzing</h2>'
        + render_evidence_refs(route, almere_view["evidence_refs"])
        + "</section>",
    ]
    return "".join(sections)


def render_decisions_index(route: str, decisions: list[dict]) -> str:
    grouped: dict[str, list[dict]] = {
        "open_decisions": [],
        "partly_resolved": [],
        "blocked": [],
        "awaiting_clarification": [],
    }
    for item in decisions:
        grouped[item["status_group"]].append(item)

    labels = {
        "open_decisions": "Open besluitvragen",
        "partly_resolved": "Gedeeltelijk ingevulde besluitvragen",
        "blocked": "Geblokkeerde besluitvragen",
        "awaiting_clarification": "Besluitvragen die wachten op verduidelijking",
    }
    sections = []
    for key, title in labels.items():
        items = grouped[key]
        if not items:
            continue
        sections.append(
            f'<section class="section" data-issue-section="{esc(key)}"><h2>{esc(title)}</h2><div class="card-grid">'
            + "".join(render_decision_card(route, item) for item in items)
            + "</div></section>"
        )
    return (
        '<section class="section"><div id="issue-filter-status" class="notice" hidden></div>'
        '<div id="issue-filter-empty-state" class="empty-state" hidden>Geen besluitvragen gevonden voor het actieve themafilter.</div></section>'
        + "".join(sections)
    )


def render_actions_index(route: str, actions: list[dict]) -> str:
    grouped: dict[str, list[dict]] = {
        "not_started": [],
        "in_preparation": [],
        "underway": [],
        "blocked": [],
    }
    for item in actions:
        grouped[item["status_group"]].append(item)

    labels = {
        "not_started": "Nog niet gestarte opvolgacties",
        "in_preparation": "Opvolgacties in voorbereiding",
        "underway": "Lopende uitwerking zichtbaar",
        "blocked": "Opvolgacties die geblokkeerd zijn door afhankelijkheden",
    }
    sections = []
    for key, title in labels.items():
        items = grouped[key]
        if not items:
            continue
        sections.append(
            f'<section class="section" data-issue-section="{esc(key)}"><h2>{esc(title)}</h2><div class="card-grid">'
            + "".join(render_action_card(route, item) for item in items)
            + "</div></section>"
        )
    return (
        '<section class="section"><div id="issue-filter-status" class="notice" hidden></div>'
        '<div id="issue-filter-empty-state" class="empty-state" hidden>Geen opvolgacties gevonden voor het actieve themafilter.</div></section>'
        + "".join(sections)
    )


def render_dashboard(route: str, dashboard_view: dict) -> str:
    rows = []
    for row in dashboard_view["rows"]:
        theme_value = ", ".join(row["linked_theme_ids"]) if row["linked_theme_ids"] else ""
        rows.append(
            "<tr "
            + 'data-dashboard-row '
            + f'data-type="{esc(row["issue_type"])}" '
            + f'data-domain="{esc(row["linked_domain"])}" '
            + f'data-status="{esc(row["status"])}" '
            + f'data-theme="{esc(theme_value)}">'
            + f'<td>{esc(row["title"])}</td>'
            + f'<td>{esc(issue_type_label(row["issue_type"]))}</td>'
            + f'<td>{esc(row["linked_domain"])}</td>'
            + f'<td>{esc(row["status"])}</td>'
            + f'<td>{esc(row["owner"])}</td>'
            + f'<td>{esc(row["next_milestone"])}</td>'
            + f'<td>{esc(row["dependencies"])}</td>'
            + f'<td>{esc(row["consequences_of_non_follow_up"])}</td>'
            + f'<td><a href="{esc(relative_link(route, row["linked_page_url"]))}">Open</a></td>'
            + "</tr>"
        )
    return (
        '<section class="section"><h2>Filters</h2><div class="filters">'
        + '<label><span class="search-label">Type</span><select class="filter-select" data-dashboard-filter="type"><option value="">Alles</option><option value="decision">Besluitvraag</option><option value="action">Opvolgactie</option><option value="dependency">Afhankelijkheid</option><option value="risk">Risico</option></select></label>'
        + '<label><span class="search-label">Domein</span><select class="filter-select" data-dashboard-filter="domain"><option value="">Alles</option><option value="D5">D5</option><option value="D6">D6</option><option value="D5 en D6">D5 en D6</option></select></label>'
        + '<label><span class="search-label">Status</span><select class="filter-select" data-dashboard-filter="status"><option value="">Alles</option><option value="open">open</option><option value="gedeeltelijk">gedeeltelijk</option><option value="geblokkeerd">geblokkeerd</option><option value="wacht">wacht op duiding</option><option value="voorbereiding">voorbereiding</option></select></label>'
        + '<label><span class="search-label">Thema</span><select class="filter-select" data-dashboard-filter="theme"><option value="">Alles</option><option value="basisfunctionaliteiten-d5">Basisfunctionaliteiten (D5)</option><option value="basisinfrastructuur-d6">Basisinfrastructuur (D6)</option><option value="governance-en-regie">Governance en regie</option><option value="financiering">Financiering</option><option value="monitoring-en-leren">Monitoring en leren</option></select></label>'
        + "</div></section>"
        + '<section class="section"><h2>Bestuurlijk overzicht</h2><table class="data-table"><thead><tr><th>Issue</th><th>Type</th><th>Domein</th><th>Status</th><th>Eigenaar</th><th>Volgende mijlpaal</th><th>Afhankelijkheden</th><th>Gevolg bij uitblijven</th><th>Link</th></tr></thead><tbody>'
        + "".join(rows)
        + '</tbody></table><div id="dashboard-empty-state" class="empty-state" hidden>Geen resultaten voor de huidige filterselectie.</div></section>'
    )


def render_detail_page(route: str, model: dict, page_type: str) -> str:
    sections = [
        '<section class="section"><h2>'
        + ("Besluitvraag" if page_type == "decision" else "Opvolgactie")
        + "</h2><div class=\"notice\">"
        + esc(model["scope_note"])
        + "</div></section>"
    ]

    if page_type == "decision":
        sections.extend(
            [
                f'<section class="section"><h2>Besluitvraag</h2><p>{esc(model["decision_question"])}</p></section>',
                f'<section class="section"><h2>Huidige werkrichting</h2><p>{esc(model["current_working_direction"])}</p></section>',
                f'<section class="section"><h2>Waarom dit bestuurlijk relevant is</h2><p>{esc(model["why_it_matters_for_leadership"])}</p></section>',
                '<section class="section"><h2>Huidige beleidsbasis</h2>' + render_document_refs(route, model["policy_basis"]) + "</section>",
                f'<section class="section"><h2>Huidige situatie in Almere</h2><p>{esc(model["current_situation_almere"]["summary"])}</p></section>',
                '<section class="section"><h2>Mogelijke opties op basis van de huidige bronbasis</h2><ul class="stack-list">'
                + "".join(
                    "<li>"
                    + f'<strong>{esc(option["title"])}</strong><br>'
                    + f'{esc(option["summary"])}'
                    + "</li>"
                    for option in model["options"]
                )
                + "</ul></section>",
                '<section class="section"><h2>Vergelijking van opties</h2><table class="data-table"><thead><tr><th>Optie</th><th>Bestuurlijke duidelijkheid</th><th>Afhankelijkheid van anderen</th><th>Statuscontext</th></tr></thead><tbody>'
                + "".join(
                    "<tr>"
                    + f'<td>{esc(next(option["title"] for option in model["options"] if option["option_id"] == item["option_id"]))}</td>'
                    + f'<td>{esc(item["bestuurlijke_duidelijkheid"])}</td>'
                    + f'<td>{esc(item["afhankelijkheid_van_anderen"])}</td>'
                    + f'<td>{esc(item["huidige_statuscontext"])}</td>'
                    + "</tr>"
                    for item in model["option_comparison"]
                )
                + "</tbody></table></section>",
                f'<section class="section"><h2>Gevolgen als geen besluit volgt</h2><p>{esc(model["consequences_of_non_decision"])}</p></section>',
                '<section class="section"><h2>Afhankelijkheden en randvoorwaarden</h2><ul class="stack-list">'
                + "".join(
                    "<li>"
                    + f'<strong>{esc(dep["title"])}</strong><br>'
                    + esc(dep["summary"])
                    + "</li>"
                    for dep in model["dependencies"]
                )
                + "</ul></section>",
                f'<section class="section"><h2>Volgende formele stap</h2><p>{esc(model["next_formal_step"])}</p></section>',
            ]
        )
        if model.get("review_details"):
            sections.append(
                '<section class="section" id="menselijke-duiding"><h2>Menselijke duiding</h2>'
                + f'<div class="notice">{esc(model["review_details"]["note"])}</div>'
                + '<ul class="stack-list">'
                + "".join(
                    "<li>"
                    + f'<strong>{esc(item["topic_label"])}</strong><br>'
                    + f'<span class="list-meta">{esc(item["reason_label"])}</span><br>'
                    + esc(item["summary"])
                    + "<br>"
                    + f'<span class="list-meta">Aanbevolen vervolgstap: {esc(item["recommended_action"])}</span>'
                    + "</li>"
                    for item in model["review_details"]["issues"]
                )
                + "</ul>"
                + (
                    '<h3>Bronnen die extra duiding vragen</h3><ul class="stack-list">'
                    + "".join(
                        "<li>"
                        + f'<strong>{esc(item["document_title"])}</strong><br>'
                        + f'<span class="list-meta">{esc(item["publisher"])} | {esc(item["publication_date"] or "datum onbekend")} | {esc(item["topic_label"])}</span><br>'
                        + esc(item["summary"])
                        + "</li>"
                        for item in model["review_details"]["source_signals"]
                    )
                    + "</ul>"
                    if model["review_details"]["source_signals"]
                    else ""
                )
                + "</section>"
            )
        sections.append('<section class="section"><h2>Bronbasis</h2>' + render_evidence_refs(route, model["supporting_evidence"]) + "</section>")
    else:
        sections.extend(
            [
                f'<section class="section"><h2>Opvolgactie</h2><p>{esc(model["action_statement"])}</p></section>',
                f'<section class="section"><h2>Waarom bestuurlijke actie nodig is</h2><p>{esc(model["why_leadership_action_required"])}</p></section>',
                f'<section class="section"><h2>Beoogd resultaat</h2><p>{esc(model["intended_outcome"])}</p></section>',
                f'<section class="section"><h2>Huidige status</h2><p>{esc(model["current_status_detail"])}</p></section>',
                f'<section class="section"><h2>Eigenaar en deelnemers</h2><p>{esc(model["owner"])}</p><p class="muted">Betrokkenen: {esc(", ".join(model["participants"]))}</p></section>',
                '<section class="section"><h2>Afhankelijkheden</h2><ul class="stack-list">'
                + "".join(
                    "<li>"
                    + f'<strong>{esc(dep["title"])}</strong><br>'
                    + esc(dep["summary"])
                    + "</li>"
                    for dep in model["dependencies"]
                )
                + "</ul></section>",
                '<section class="section"><h2>Voorgestelde volgorde</h2><ol>'
                + "".join(f"<li>{esc(step)}</li>" for step in model["proposed_sequence"])
                + "</ol></section>",
                f'<section class="section"><h2>Beoogd opleverproduct</h2><p>{esc(model["expected_deliverable"])}</p></section>',
                '<section class="section"><h2>Tijd en mijlpalen</h2><ul class="stack-list">'
                + "".join(
                    "<li>"
                    + f'<strong>{esc(item["label"])}</strong><br>'
                    + esc(item["value"])
                    + "</li>"
                    for item in model["timing_and_milestones"]
                )
                + "</ul></section>",
                f'<section class="section"><h2>Gevolgen als de actie niet wordt opgepakt</h2><p>{esc(model["consequences_if_not_followed_up"])}</p></section>',
                '<section class="section"><h2>Bronbasis</h2>' + render_evidence_refs(route, model["supporting_evidence"]) + "</section>",
            ]
        )
    return "".join(sections)


def render_timeline(route: str, timeline_view: dict) -> str:
    return (
        '<section class="section"><h2>Beleidsmomenten en mijlpalen</h2><ul class="stack-list">'
        + "".join(
            "<li id=\""
            + esc(item["entry_id"])
            + "\">"
            + f'<strong>{esc(item["date_label"])} - {esc(item["title"])}</strong><br>'
            + f'<span class="list-meta">{esc(item["linked_domain"])} | {esc(item["relation_type"])}</span><br>'
            + esc(item["summary"])
            + "<br>"
            + f'<span class="list-meta">Gevolg voor Almere: {esc(item["consequence_for_almere"])}</span>'
            + (
                "<br>"
                + f'<span class="list-meta">Bron: <a href="{esc(item["source_url"])}">{esc(item["source_label"])}</a></span>'
                if item.get("source_url")
                else f'<br><span class="list-meta">{esc(item["source_label"])}</span>'
            )
            + "</li>"
            for item in timeline_view["entries"]
        )
        + "</ul></section>"
    )


def render_themes_index(route: str, themes_view: dict) -> str:
    return (
        '<section class="section"><h2>Strategische thema\'s</h2><div class="card-grid">'
        + "".join(
            render_card(
                theme["title"],
                theme["summary"],
                footer=render_link_pills(
                    route,
                    [
                        {"label": f'{theme["linked_decision_count"]} besluitvragen', "href": f'/decisions/?theme={theme["theme_id"]}'},
                        {"label": f'{theme["linked_action_count"]} opvolgacties', "href": f'/actions/?theme={theme["theme_id"]}'},
                    ],
                ),
                href=relative_link(route, theme["page_url"]),
            )
            for theme in themes_view["themes"]
        )
        + "</div></section>"
    )


def render_theme_detail(route: str, theme: dict) -> str:
    return (
        '<section class="section"><h2>Themasamenvatting</h2><div class="notice">'
        + esc(theme["summary"])
        + "</div></section>"
        + '<section class="section"><h2>Relevante D5/D6-onderdelen</h2><ul class="stack-list">'
        + "".join(
            "<li>"
            + f'<strong>{esc(item["title"])}</strong><br>'
            + f'<span class="list-meta">{esc(item["scope_label"])}</span>'
            + ("<br><span class=\"list-meta\">Menselijke duiding blijft nodig.</span>" if item["needs_human_review"] else "")
            + "</li>"
            for item in theme["relevant_d5_d6_items"]
        )
        + "</ul></section>"
        + '<section class="section"><h2>Huidige interpretatie</h2><ul class="stack-list">'
        + "".join(
            "<li>"
            + f'<strong><a href="{esc(relative_link(route, item["page_url"]))}">{esc(item["title"])}</a></strong><br>'
            + f'<span class="list-meta">{esc(item["status"])} | betrouwbaarheid {esc(item["confidence_label"])}</span>'
            + ("<br><span class=\"list-meta\">Menselijke duiding gemarkeerd in de referentielaag.</span>" if item["needs_human_review"] else "")
            + "</li>"
            for item in theme["current_interpretation"]
        )
        + "</ul></section>"
        + '<section class="section"><h2>Implicaties voor Almere</h2><ul class="stack-list">'
        + "".join(
            "<li>"
            + f'<strong><a href="{esc(relative_link(route, item["page_url"]))}">{esc(item["title"])}</a></strong><br>'
            + esc(item["summary"])
            + "</li>"
            for item in theme["almere_implications"]
        )
        + "</ul></section>"
        + '<section class="section"><h2>Gekoppelde besluitvragen</h2><ul class="stack-list">'
        + "".join(
            "<li>"
            + f'<strong><a href="{esc(relative_link(route, item["page_url"]))}">{esc(item["title"])}</a></strong><br>'
            + f'<span class="list-meta">{esc(item["status"])}</span>'
            + "</li>"
            for item in theme["linked_decisions"]
        )
        + "</ul></section>"
        + '<section class="section"><h2>Gekoppelde opvolgacties</h2><ul class="stack-list">'
        + "".join(
            "<li>"
            + f'<strong><a href="{esc(relative_link(route, item["page_url"]))}">{esc(item["title"])}</a></strong><br>'
            + f'<span class="list-meta">{esc(item["status"])}</span>'
            + "</li>"
            for item in theme["linked_actions"]
        )
        + "</ul></section>"
        + '<section class="section"><h2>Afhankelijkheden</h2><ul class="stack-list">'
        + "".join(
            "<li>"
            + f'<strong><a href="{esc(relative_link(route, item["page_url"]))}">{esc(item["title"])}</a></strong><br>'
            + esc(item["summary"])
            + "</li>"
            for item in theme["dependencies"]
        )
        + "</ul></section>"
        + '<section class="section"><h2>Bronbasis</h2>'
        + render_document_refs(route, theme["source_basis"])
        + "</section>"
        + '<section class="section"><h2>Gerelateerde referentieonderwerpen</h2><ul class="stack-list">'
        + "".join(
            "<li>"
            + f'<strong><a href="{esc(relative_link(route, item["page_url"]))}">{esc(item["title"])}</a></strong><br>'
            + f'<span class="list-meta">{esc(item["status"])}</span>'
            + "</li>"
            for item in theme["related_reference_topics"]
        )
        + "</ul></section>"
    )


def render_reference(route: str, reference_view: dict) -> str:
    sections = [
        '<section class="section"><h2>Hoe deze naslag te gebruiken</h2><div class="notice">Gebruik deze laag voor begrippen, bronsporen en onderwerpsoverzicht. Besluitvragen en opvolgacties blijven leidend voor bestuurlijke opvolging.</div></section>',
        '<section class="section"><h2>Onderwerpsoverzicht</h2><div class="card-grid">'
        + "".join(
            render_card(
                domain,
                f'{len(topics)} onderwerp(en) in deze groep.',
                footer=render_link_pills(route, [{"label": topic["title"], "href": topic["page_url"]} for topic in topics[:4]]),
                href=relative_link(route, "/reference/topics/"),
            )
            for domain, topics in reference_view["domain_groups"].items()
        )
        + "</div></section>",
        '<section class="section"><h2>Uitgelichte onderwerpen</h2><div class="card-grid">'
        + "".join(
            render_card(
                topic["title"],
                topic["definition"],
                meta=[topic["status"], topic["linked_domain"]],
                href=relative_link(route, topic["page_url"]),
                whole_card=True,
            )
            for topic in reference_view["featured_topics"]
        )
        + "</div></section>",
        '<section class="section"><h2>Belangrijkste bronhouders</h2><ul class="stack-list">'
        + "".join(
            "<li>"
            + f'<strong>{esc(item["publisher"])}</strong><br>'
            + f'<span class="list-meta">{esc(str(item["document_count"]))} bron(nen) in de huidige referentielaag</span>'
            + "</li>"
            for item in reference_view["publishers"]
        )
        + "</ul></section>",
    ]
    return "".join(sections)


def render_reference_topics_index(route: str, topics: list[dict]) -> str:
    return (
        '<section class="section"><h2>Onderwerpen</h2><div class="card-grid">'
        + "".join(
            render_card(
                topic["title"],
                topic["definition"],
                meta=[topic["status"], topic["linked_domain"]],
                href=relative_link(route, topic["page_url"]),
                whole_card=True,
            )
            for topic in topics
        )
        + "</div></section>"
    )


def render_reference_topic_detail(route: str, topic: dict) -> str:
    return (
        '<section class="section"><h2>Definitie</h2><div class="notice">'
        + esc(topic["definition"])
        + "</div></section>"
        + f'<section class="section"><h2>Status</h2><p>{esc(topic["status"])}. Betrouwbaarheidsniveau: {esc(topic["confidence_label"])}.</p></section>'
        + '<section class="section"><h2>Gekoppelde thema\'s</h2><ul class="stack-list">'
        + "".join(
            "<li>"
            + f'<strong><a href="{esc(relative_link(route, item["page_url"]))}">{esc(item["title"])}</a></strong>'
            + "</li>"
            for item in topic["linked_themes"]
        )
        + "</ul></section>"
        + '<section class="section"><h2>Gekoppelde besluitvragen</h2><ul class="stack-list">'
        + "".join(
            "<li>"
            + f'<strong><a href="{esc(relative_link(route, item["page_url"]))}">{esc(item["title"])}</a></strong><br>'
            + f'<span class="list-meta">{esc(item["status"])}</span>'
            + "</li>"
            for item in topic["linked_decisions"]
        )
        + "</ul></section>"
        + '<section class="section"><h2>Gekoppelde opvolgacties</h2><ul class="stack-list">'
        + "".join(
            "<li>"
            + f'<strong><a href="{esc(relative_link(route, item["page_url"]))}">{esc(item["title"])}</a></strong><br>'
            + f'<span class="list-meta">{esc(item["status"])}</span>'
            + "</li>"
            for item in topic["linked_actions"]
        )
        + "</ul></section>"
        + '<section class="section"><h2>Bronbasis</h2>'
        + render_document_refs(route, topic["source_basis"])
        + "</section>"
        + '<section class="section"><h2>Tijdlijnnotities</h2><ul class="stack-list">'
        + "".join(
            "<li>"
            + f'<strong>{esc(item["date_label"])} - <a href="{esc(relative_link(route, item["page_url"]))}">{esc(item["title"])}</a></strong><br>'
            + f'<span class="list-meta">{esc(item["status"])}</span>'
            + "</li>"
            for item in topic["timeline_notes"]
        )
        + "</ul></section>"
        + '<section class="section"><h2>Gerelateerde onderwerpen</h2><ul class="stack-list">'
        + "".join(
            "<li>"
            + f'<strong><a href="{esc(relative_link(route, item["page_url"]))}">{esc(item["title"])}</a></strong>'
            + "</li>"
            for item in topic["related_topics"]
        )
        + "</ul></section>"
    )


def render_sources_index(route: str, sources_view: dict) -> str:
    return (
        '<section class="section"><h2>Bronnenoverzicht</h2><div class="card-grid">'
        + "".join(
            render_card(
                source["metadata"]["title"],
                source["summary"],
                meta=[
                    source["metadata"]["publisher"],
                    source["metadata"]["publication_date"] or "datum onbekend",
                    source["metadata"]["document_type_label"],
                    source["metadata"]["source_classification_label"],
                ],
                href=relative_link(route, source["page_url"]),
                whole_card=True,
            )
            for source in sources_view["sources"]
        )
        + "</div></section>"
    )


def render_source_detail(route: str, source: dict) -> str:
    metadata = source["metadata"]
    return (
        '<section class="section"><h2>Metadata</h2><ul class="stack-list">'
        + "<li>"
        + f'<strong>Uitgever</strong><br>{esc(metadata["publisher"])}'
        + "</li><li>"
        + f'<strong>Publicatiedatum</strong><br>{esc(metadata["publication_date"] or "datum onbekend")}'
        + "</li><li>"
        + f'<strong>Type bron</strong><br>{esc(metadata["document_type_label"])} | {esc(metadata["source_classification_label"])}'
        + "</li><li>"
        + f'<strong>Originele bron</strong><br><a href="{esc(metadata["source_url"])}">{esc(metadata["source_url"])}</a>'
        + "</li></ul></section>"
        + f'<section class="section"><h2>Korte samenvatting</h2><div class="notice">{esc(source["summary"])}</div></section>'
        + f'<section class="section"><h2>Wat deze bron toevoegt</h2><p>{esc(source["what_changed_or_added"])}</p></section>'
        + f'<section class="section"><h2>D5-relevantie</h2><p>{esc(source["d5_relevance"])}</p></section>'
        + f'<section class="section"><h2>D6-relevantie</h2><p>{esc(source["d6_relevance"])}</p></section>'
        + '<section class="section"><h2>Extractiesignalen</h2><ul class="stack-list">'
        + f'<li><strong>Gestructureerde tabel</strong><br>{esc("ja" if source["structured_signals"]["contains_structured_table"] else "nee")}</li>'
        + f'<li><strong>D5-items</strong><br>{esc(str(source["structured_signals"]["d5_item_count"]))}</li>'
        + f'<li><strong>D6-items</strong><br>{esc(str(source["structured_signals"]["d6_item_count"]))}</li>'
        + f'<li><strong>Governance/financiering-items</strong><br>{esc(str(source["structured_signals"]["governance_item_count"]))}</li>'
        + f'<li><strong>Tijdlijn/status-items</strong><br>{esc(str(source["structured_signals"]["timeline_item_count"]))}</li>'
        + "</ul></section>"
        + '<section class="section"><h2>Gekoppelde claims</h2><ul class="stack-list">'
        + "".join(
            "<li>"
            + f'<strong><a href="{esc(relative_link(route, item["page_url"]))}">{esc(item["title"])}</a></strong><br>'
            + f'<span class="list-meta">{esc(str(item["claim_count"]))} claim(s)</span>'
            + "</li>"
            for item in source["linked_claims"]
        )
        + "</ul></section>"
        + '<section class="section"><h2>Gekoppelde besluitvragen en acties</h2><ul class="stack-list">'
        + "".join(
            "<li>"
            + f'<strong><a href="{esc(relative_link(route, item["page_url"]))}">{esc(item["title"])}</a></strong><br>'
            + f'<span class="list-meta">{esc(item["status"])}</span>'
            + "</li>"
            for item in source["linked_decisions"] + source["linked_actions"]
        )
        + "</ul></section>"
        + '<section class="section"><h2>Gekoppelde thema\'s</h2><ul class="stack-list">'
        + "".join(
            "<li>"
            + f'<strong><a href="{esc(relative_link(route, item["page_url"]))}">{esc(item["title"])}</a></strong>'
            + "</li>"
            for item in source["linked_themes"]
        )
        + "</ul></section>"
        + '<section class="section"><h2>Gerelateerde bronnen</h2><ul class="stack-list">'
        + "".join(
            "<li>"
            + f'<strong><a href="{esc(relative_link(route, item["page_url"]))}">{esc(item["title"])}</a></strong>'
            + "</li>"
            for item in source["related_sources"]
        )
        + "</ul></section>"
    )


def render_placeholder(route: str, title: str) -> str:
    return (
        '<section class="section"><h2>Deze sectie volgt in een volgende bouwstap</h2>'
        + "<p>De navigatiestructuur is al aanwezig, maar de inhoudelijke uitwerking van deze sectie wordt in een volgende repo-fase gegenereerd.</p>"
        + '<p><a href="' + esc(relative_link(route, "/")) + '">Terug naar Start</a></p></section>'
    )


def render_page(
    route: str,
    title: str,
    summary: str,
    content: str,
    navigation: list[dict],
    site_info: dict,
    as_of_date: str,
    generated_on: str,
    body_class: str,
    crumbs: list[tuple[str, str]] | None = None,
    notice: str | None = None,
) -> str:
    template = Template(TEMPLATE_PATH.read_text(encoding="utf-8"))
    return template.substitute(
        lang=site_info["language"],
        page_title=f"{title} | {site_info['site_title']}",
        page_description=summary,
        stylesheet_url=relative_link(route, "/assets/site.css"),
        script_url=relative_link(route, "/assets/site.js"),
        search_index_url=relative_link(route, "/search-index.json"),
        site_root=root_prefix(route),
        home_url=relative_link(route, "/"),
        site_title=site_info["site_title"],
        scope_statement=site_info["scope_statement"],
        navigation=render_navigation(route, navigation),
        breadcrumbs=render_breadcrumbs(route, crumbs or []),
        page_intro=page_intro(title, summary, [f"Peildatum {as_of_date}", f"Gegenereerd {generated_on}"], notice=notice),
        content=content,
        as_of_date=as_of_date,
        generated_on=generated_on,
        body_class=body_class,
    )


def build_search_index(
    home_view: dict,
    almere_view: dict,
    decisions: list[dict],
    actions: list[dict],
    dashboard_view: dict,
    timeline_view: dict,
    themes_view: dict,
    reference_view: dict,
    reference_topics: list[dict],
    sources_view: dict,
) -> list[dict]:
    index = [
        {
            "title": "Start",
            "subtitle": "Bestuurlijk overzicht",
            "summary": home_view["executive_summary"],
            "aliases": ["start", "overzicht"],
            "themes": [],
            "domains": [],
            "url": route_to_output_path("/").as_posix(),
            "page_type": "home",
            "page_type_label": "Pagina",
        },
        {
            "title": "Almere",
            "subtitle": "Huidig gemeentelijk beeld",
            "summary": almere_view["current_picture"],
            "aliases": ["gemeente almere", "lokale situatie"],
            "themes": [],
            "domains": ["D5", "D6"],
            "url": route_to_output_path("/almere/").as_posix(),
            "page_type": "almere",
            "page_type_label": "Pagina",
        },
        {
            "title": "Besluitvragen",
            "subtitle": "Overzicht van mogelijke besluitvragen",
            "summary": "Machine-gegenereerde mogelijke besluitvragen op basis van de huidige openbare bronbasis.",
            "aliases": ["besluiten", "bestuurlijke keuzes"],
            "themes": [],
            "domains": ["D5", "D6"],
            "url": route_to_output_path("/decisions/").as_posix(),
            "page_type": "decisions",
            "page_type_label": "Pagina",
        },
        {
            "title": "Opvolgacties",
            "subtitle": "Overzicht van mogelijke opvolgacties",
            "summary": "Machine-gegenereerde mogelijke opvolgacties op basis van de huidige openbare bronbasis.",
            "aliases": ["acties", "vervolgstappen"],
            "themes": [],
            "domains": ["D5", "D6"],
            "url": route_to_output_path("/actions/").as_posix(),
            "page_type": "actions",
            "page_type_label": "Pagina",
        },
        {
            "title": "Dashboard",
            "subtitle": "Executief monitoringsbeeld",
            "summary": "Scanbare tabel met besluitvragen, opvolgacties, afhankelijkheden en risico's.",
            "aliases": ["monitoring", "overzicht"],
            "themes": [],
            "domains": ["D5", "D6"],
            "url": route_to_output_path("/dashboard/").as_posix(),
            "page_type": "dashboard",
            "page_type_label": "Pagina",
        },
        {
            "title": "Tijdlijn",
            "subtitle": "Beleidsmomenten en mijlpalen",
            "summary": "Chronologisch overzicht van bronwijzigingen en toekomstige mijlpalen in de AZWA D5/D6-lijn.",
            "aliases": ["tijdlijn", "mijlpalen", "beleidsmomenten"],
            "themes": [],
            "domains": ["D5", "D6"],
            "url": route_to_output_path("/timeline/").as_posix(),
            "page_type": "timeline",
            "page_type_label": "Pagina",
        },
        {
            "title": "Thema's",
            "subtitle": "Strategische thema's",
            "summary": "Themagewijs overzicht van bestuurlijke lijnen, besluitvragen en opvolgacties.",
            "aliases": ["thema", "strategische thema's"],
            "themes": [],
            "domains": ["D5", "D6"],
            "url": route_to_output_path("/themes/").as_posix(),
            "page_type": "themes",
            "page_type_label": "Pagina",
        },
        {
            "title": "Referentie",
            "subtitle": "Naslag en onderwerpsoverzicht",
            "summary": "Naslaglaag met onderwerpen, bronhouders en begripsmatige koppelingen.",
            "aliases": ["naslag", "onderwerpen", "referentie"],
            "themes": [],
            "domains": ["D5", "D6"],
            "url": route_to_output_path("/reference/").as_posix(),
            "page_type": "reference",
            "page_type_label": "Pagina",
        },
        {
            "title": "Bronnen",
            "subtitle": "Bronindex",
            "summary": "Volledige index van bronpagina's en documentdetails die aan de site ten grondslag liggen.",
            "aliases": ["bronbasis", "documenten", "bronnen"],
            "themes": [],
            "domains": ["D5", "D6"],
            "url": route_to_output_path("/sources/").as_posix(),
            "page_type": "sources",
            "page_type_label": "Pagina",
        },
    ]
    for decision in decisions:
        index.append(
            {
                "title": decision["title"],
                "subtitle": decision["decision_question"],
                "summary": decision["why_decision_required"],
                "aliases": decision["linked_theme_ids"],
                "themes": decision["linked_theme_ids"],
                "domains": [decision["linked_domain_label"]],
                "url": route_to_output_path(decision["page_url"]).as_posix(),
                "page_type": "decision",
                "page_type_label": "Besluitvraag",
            }
        )
    for action in actions:
        index.append(
            {
                "title": action["title"],
                "subtitle": action["action_statement"],
                "summary": action["current_status_detail"],
                "aliases": action["linked_theme_ids"],
                "themes": action["linked_theme_ids"],
                "domains": [action["linked_domain_label"]],
                "url": route_to_output_path(action["page_url"]).as_posix(),
                "page_type": "action",
                "page_type_label": "Opvolgactie",
            }
        )
    for theme in themes_view["themes"]:
        index.append(
            {
                "title": theme["title"],
                "subtitle": "Strategisch thema",
                "summary": theme["summary"],
                "aliases": [theme["theme_id"]],
                "themes": [theme["theme_id"]],
                "domains": ["D5", "D6"],
                "url": route_to_output_path(theme["page_url"]).as_posix(),
                "page_type": "theme",
                "page_type_label": "Thema",
            }
        )
    for topic in reference_topics:
        index.append(
            {
                "title": topic["title"],
                "subtitle": topic["status"],
                "summary": topic["definition"],
                "aliases": [topic["topic_id"]],
                "themes": topic["linked_theme_ids"],
                "domains": [topic["linked_domain"]],
                "url": route_to_output_path(topic["page_url"]).as_posix(),
                "page_type": "reference_topic",
                "page_type_label": "Onderwerp",
            }
        )
    for source in sources_view["sources"]:
        index.append(
            {
                "title": source["metadata"]["title"],
                "subtitle": source["metadata"]["publisher"],
                "summary": source["summary"],
                "aliases": [source["source_id"], source["metadata"].get("short_title", "")],
                "themes": [item["theme_id"] for item in source["linked_themes"]],
                "domains": [],
                "url": route_to_output_path(source["page_url"]).as_posix(),
                "page_type": "source",
                "page_type_label": "Bron",
            }
        )
    return index


def copy_assets() -> None:
    for asset_name in ("site.css", "site.js"):
        source_path = ASSETS_DIR / asset_name
        target_path = DIST_DIR / "assets" / asset_name
        write_text(target_path, source_path.read_text(encoding="utf-8"))


def main() -> None:
    navigation = load_json(TAXONOMY_PATH)["navigation"]
    site_info = load_json(TAXONOMY_PATH)["site"]
    home_view = load_json(DATA_DIR / "site_home_view.json")
    almere_view = load_json(DATA_DIR / "site_almere_view.json")
    dashboard_view = load_json(DATA_DIR / "dashboard_view.json")
    timeline_view = load_json(TIMELINE_VIEW_PATH)
    themes_view = load_json(THEMES_VIEW_PATH)
    reference_view = load_json(REFERENCE_VIEW_PATH)
    sources_view = load_json(SOURCES_VIEW_PATH)
    decisions = [load_json(path) for path in sorted((DATA_DIR / "decision_view_models").glob("*.json"))]
    actions = [load_json(path) for path in sorted((DATA_DIR / "action_view_models").glob("*.json"))]
    theme_models = [load_json(path) for path in sorted((DATA_DIR / "theme_view_models").glob("*.json"))]
    reference_topics = [load_json(path) for path in sorted((DATA_DIR / "reference_topic_view_models").glob("*.json"))]
    source_models = [load_json(path) for path in sorted((DATA_DIR / "source_view_models").glob("*.json"))]

    copy_assets()
    write_text(DIST_DIR / ".nojekyll", "")

    pages = [
        (
                "/",
                render_page(
                    "/",
                    "Start",
                    "Compact bestuurlijk overzicht voor Almere op basis van de huidige AZWA D5/D6-bronbasis.",
                    render_home("/", home_view),
                    navigation,
                    site_info,
                    home_view["as_of_date"],
                    home_view["generated_on"],
                    "page-home",
                    crumbs=[("Start", "/")],
                ),
            ),
        (
            "/almere/",
            render_page(
                "/almere/",
                "Almere",
                "Huidig gemeentelijk beeld, hiaten, afhankelijkheden en bestuurlijke vervolgvragen voor Almere.",
                render_almere("/almere/", almere_view),
                navigation,
                site_info,
                almere_view["as_of_date"],
                almere_view["generated_on"],
                "page-almere",
                crumbs=[("Start", "/"), ("Almere", "/almere/")],
            ),
        ),
        (
            "/decisions/",
            render_page(
                "/decisions/",
                "Besluitvragen",
                "Machine-gegenereerde mogelijke besluitvragen op basis van de huidige openbare bronbasis.",
                render_decisions_index("/decisions/", decisions),
                navigation,
                site_info,
                home_view["as_of_date"],
                home_view["generated_on"],
                "page-decisions",
                crumbs=[("Start", "/"), ("Besluitvragen", "/decisions/")],
                notice="Deze pagina toont mogelijke besluitvragen op basis van de huidige bronbasis. Dit zijn geen vastgestelde gemeentelijke besluiten.",
            ),
        ),
        (
            "/actions/",
            render_page(
                "/actions/",
                "Opvolgacties",
                "Machine-gegenereerde mogelijke opvolgacties op basis van de huidige openbare bronbasis.",
                render_actions_index("/actions/", actions),
                navigation,
                site_info,
                home_view["as_of_date"],
                home_view["generated_on"],
                "page-actions",
                crumbs=[("Start", "/"), ("Opvolgacties", "/actions/")],
                notice="Deze pagina toont mogelijke opvolgacties op basis van de huidige bronbasis. Dit zijn geen vastgestelde opdrachten.",
            ),
        ),
        (
            "/dashboard/",
            render_page(
                "/dashboard/",
                "Dashboard",
                "Scanbaar bestuurlijk overzicht van besluitvragen, opvolgacties, afhankelijkheden en risico's.",
                render_dashboard("/dashboard/", dashboard_view),
                navigation,
                site_info,
                dashboard_view["as_of_date"],
                dashboard_view["generated_on"],
                "page-dashboard",
                crumbs=[("Start", "/"), ("Dashboard", "/dashboard/")],
            ),
        ),
        (
            "/timeline/",
            render_page(
                "/timeline/",
                "Tijdlijn",
                "Beleidsmomenten, bronwijzigingen en toekomstige mijlpalen voor de AZWA D5/D6-lijn van Almere.",
                render_timeline("/timeline/", timeline_view),
                navigation,
                site_info,
                timeline_view["as_of_date"],
                timeline_view["generated_on"],
                "page-timeline",
                crumbs=[("Start", "/"), ("Tijdlijn", "/timeline/")],
            ),
        ),
        (
            "/themes/",
            render_page(
                "/themes/",
                "Thema's",
                "Strategisch overzicht van de hoofdthema's, gekoppelde besluitvragen en opvolgacties.",
                render_themes_index("/themes/", themes_view),
                navigation,
                site_info,
                themes_view["as_of_date"],
                themes_view["generated_on"],
                "page-themes",
                crumbs=[("Start", "/"), ("Thema's", "/themes/")],
            ),
        ),
        (
            "/reference/",
            render_page(
                "/reference/",
                "Referentie",
                "Naslaglaag met onderwerpen, bronhouders en koppelingen naar de bestuurlijke site-onderdelen.",
                render_reference("/reference/", reference_view),
                navigation,
                site_info,
                reference_view["as_of_date"],
                reference_view["generated_on"],
                "page-reference",
                crumbs=[("Start", "/"), ("Referentie", "/reference/")],
            ),
        ),
        (
            "/reference/topics/",
            render_page(
                "/reference/topics/",
                "Onderwerpen",
                "Volledige index van onderwerpen in de huidige referentielaag.",
                render_reference_topics_index("/reference/topics/", reference_topics),
                navigation,
                site_info,
                reference_view["as_of_date"],
                reference_view["generated_on"],
                "page-reference-topics",
                crumbs=[("Start", "/"), ("Referentie", "/reference/"), ("Onderwerpen", "/reference/topics/")],
            ),
        ),
        (
            "/sources/",
            render_page(
                "/sources/",
                "Bronnen",
                "Volledige index van de bronnen die aan de huidige site en claimlaag ten grondslag liggen.",
                render_sources_index("/sources/", sources_view),
                navigation,
                site_info,
                sources_view["as_of_date"],
                sources_view["generated_on"],
                "page-sources",
                crumbs=[("Start", "/"), ("Bronnen", "/sources/")],
            ),
        ),
    ]

    for decision in decisions:
        pages.append(
            (
                decision["page_url"],
                render_page(
                    decision["page_url"],
                    decision["title"],
                    decision["decision_question"],
                    render_detail_page(decision["page_url"], decision, "decision"),
                    navigation,
                    site_info,
                    decision["as_of_date"],
                    home_view["generated_on"],
                    "page-decision-detail",
                    crumbs=[("Start", "/"), ("Besluitvragen", "/decisions/"), (decision["title"], decision["page_url"])],
                ),
            )
        )

    for action in actions:
        pages.append(
            (
                action["page_url"],
                render_page(
                    action["page_url"],
                    action["title"],
                    action["action_statement"],
                    render_detail_page(action["page_url"], action, "action"),
                    navigation,
                    site_info,
                    action["as_of_date"],
                    home_view["generated_on"],
                    "page-action-detail",
                    crumbs=[("Start", "/"), ("Opvolgacties", "/actions/"), (action["title"], action["page_url"])],
                ),
            )
        )

    for theme in theme_models:
        pages.append(
            (
                theme["page_url"],
                render_page(
                    theme["page_url"],
                    theme["title"],
                    theme["summary"],
                    render_theme_detail(theme["page_url"], theme),
                    navigation,
                    site_info,
                    themes_view["as_of_date"],
                    themes_view["generated_on"],
                    "page-theme-detail",
                    crumbs=[("Start", "/"), ("Thema's", "/themes/"), (theme["title"], theme["page_url"])],
                ),
            )
        )

    for topic in reference_topics:
        pages.append(
            (
                topic["page_url"],
                render_page(
                    topic["page_url"],
                    topic["title"],
                    topic["definition"],
                    render_reference_topic_detail(topic["page_url"], topic),
                    navigation,
                    site_info,
                    reference_view["as_of_date"],
                    reference_view["generated_on"],
                    "page-reference-topic-detail",
                    crumbs=[("Start", "/"), ("Referentie", "/reference/"), ("Onderwerpen", "/reference/topics/"), (topic["title"], topic["page_url"])],
                ),
            )
        )

    for source in source_models:
        pages.append(
            (
                source["page_url"],
                render_page(
                    source["page_url"],
                    source["metadata"]["title"],
                    source["summary"],
                    render_source_detail(source["page_url"], source),
                    navigation,
                    site_info,
                    sources_view["as_of_date"],
                    sources_view["generated_on"],
                    "page-source-detail",
                    crumbs=[("Start", "/"), ("Bronnen", "/sources/"), (source["metadata"]["title"], source["page_url"])],
                ),
            )
        )

    for route, title in (("/reference/glossary/", "Begrippenlijst"),):
        pages.append(
            (
                route,
                render_page(
                    route,
                    title,
                    "De begrippenlijst volgt uit de onderwerpenset van de referentielaag.",
                    render_reference_topics_index(route, reference_topics),
                    navigation,
                    site_info,
                    reference_view["as_of_date"],
                    home_view["generated_on"],
                    "page-reference-glossary",
                    crumbs=[("Start", "/"), ("Referentie", "/reference/"), (title, route)],
                ),
            )
        )

    for route, content in pages:
        output_path = DIST_DIR / route_to_output_path(route)
        write_text(output_path, content)

    search_index = build_search_index(
        home_view,
        almere_view,
        decisions,
        actions,
        dashboard_view,
        timeline_view,
        themes_view,
        reference_view,
        reference_topics,
        sources_view,
    )
    write_text(DIST_DIR / "search-index.json", json.dumps(search_index, indent=2, ensure_ascii=False) + "\n")
    write_text(
        DIST_DIR / "site-build.json",
        json.dumps(
            {
                "generated_on": home_view["generated_on"],
                "page_count": len(pages),
                "search_index_entries": len(search_index),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
    )

    print(f"Wrote {len(pages)} HTML pages to {DIST_DIR.relative_to(REPO_ROOT).as_posix()}")
    print(f"Wrote {len(search_index)} search index entries")


if __name__ == "__main__":
    main()
