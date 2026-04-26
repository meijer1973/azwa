from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO_ROOT / "config"
DATA_DIR = REPO_ROOT / "data"
EXTRACTED_DIR = DATA_DIR / "extracted"
DOCS_DIR = REPO_ROOT / "docs"

AUDIT_PATH = EXTRACTED_DIR / "data_quality_audit.json"
REVIEW_QUEUE_PATH = EXTRACTED_DIR / "review_queue.json"
CLAIMS_MASTER_PATH = EXTRACTED_DIR / "claims" / "claims_master.jsonl"
PERSPECTIVES_PATH = CONFIG_DIR / "data_quality_perspectives.json"
REGIONAL_ROLES_PATH = DATA_DIR / "curated" / "regional_roles_and_splits_almere_flevoland.json"
ROADMAP_PATH = DOCS_DIR / "data-quality-roadmap.md"
SITE_UPDATES_PATH = DATA_DIR / "site" / "site_updates_view.json"
WORKAGENDA_D5_PATH = EXTRACTED_DIR / "workagenda_d5_operational_requirements.json"
LOCAL_SOURCE_STRENGTHENING_PATH = EXTRACTED_DIR / "local_source_strengthening_almere.json"
OUTPUT_PATH = DOCS_DIR / "internal" / "review-dashboard.html"

ISSUE_TYPES = {
    "bronprobleem": "Source authority, source coverage, or evidence status needs review.",
    "extractieprobleem": "Extraction output may contain technical noise, fragments, or parsing artifacts.",
    "claimprobleem": "Claim grouping, conflict, topic mapping, or claim structure needs review.",
    "interpretatieprobleem": "Human interpretation is needed before treating the item as a policy fact.",
    "tekstprobleem": "Text is too rough for public-facing Dutch publication.",
}

LOCALITY_SCOPES = {
    "almere": {
        "label": "Almere",
        "description": "Items grounded in Almere municipal sources, Almere-specific documents, or Almere-specific review prompts.",
    },
    "iza_azwa_regio_flevoland": {
        "label": "IZA/AZWA-regio Flevoland",
        "description": "Items grounded in the Flevoland IZA/AZWA regional route or the regional role/split guardrail.",
    },
    "general_locality": {
        "label": "General or unclear locality",
        "description": "Locality items that are municipal/regional in a broad sense but are not specific enough to assign to Almere or the IZA/AZWA-regio Flevoland.",
    },
}

REVIEW_REASON_TO_ISSUE_TYPES = {
    "authority_unclear": ["bronprobleem", "interpretatieprobleem"],
    "municipality_relevance_inferred": ["interpretatieprobleem"],
    "unresolved_conflict": ["claimprobleem", "interpretatieprobleem"],
}

ROUGH_CODE_TO_ISSUE_TYPES = {
    "raw_letterhead": ["extractieprobleem", "tekstprobleem"],
    "encoding_noise": ["extractieprobleem", "tekstprobleem"],
    "english_summary": ["tekstprobleem"],
    "bullet_or_heading_fragment": ["extractieprobleem", "tekstprobleem"],
    "fragment_too_short": ["extractieprobleem", "tekstprobleem"],
    "long_raw_excerpt": ["tekstprobleem"],
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_claims() -> list[dict[str, Any]]:
    claims: list[dict[str, Any]] = []
    for line in CLAIMS_MASTER_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            claims.append(json.loads(line))
    return claims


def repo_path(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def output_relative_link(repo_relative_path: str) -> str:
    target = REPO_ROOT / repo_relative_path
    if not target.exists():
        return repo_relative_path
    return Path("../../").joinpath(repo_relative_path).as_posix()


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "item"


def perspective_ids_for_claim(claim: dict[str, Any], perspective_config: dict[str, Any]) -> list[str]:
    topic = claim.get("topic") or ""
    jurisdiction_level = claim.get("jurisdiction_level")
    perspective_ids: list[str] = []

    for perspective in perspective_config["perspectives"]:
        perspective_id = perspective["perspective_id"]
        topic_prefixes = perspective.get("topic_prefixes", [])
        topic_ids = perspective.get("topic_ids", [])
        jurisdiction_hints = perspective.get("jurisdiction_level_hints", [])

        if any(topic.startswith(prefix) for prefix in topic_prefixes):
            perspective_ids.append(perspective_id)
            continue
        if topic in topic_ids:
            perspective_ids.append(perspective_id)
            continue
        if jurisdiction_level in jurisdiction_hints:
            perspective_ids.append(perspective_id)

    return sorted(set(perspective_ids))


def perspective_ids_for_topic(topic: str | None, perspective_config: dict[str, Any]) -> list[str]:
    if not topic:
        return []
    perspective_ids: list[str] = []
    for perspective in perspective_config["perspectives"]:
        perspective_id = perspective["perspective_id"]
        if any(topic.startswith(prefix) for prefix in perspective.get("topic_prefixes", [])):
            perspective_ids.append(perspective_id)
        elif topic in perspective.get("topic_ids", []):
            perspective_ids.append(perspective_id)
    return sorted(set(perspective_ids))


def derive_perspectives_from_claim_ids(
    claim_ids: list[str],
    claim_index: dict[str, dict[str, Any]],
    perspective_config: dict[str, Any],
) -> list[str]:
    perspective_ids: set[str] = set()
    for claim_id in claim_ids:
        claim = claim_index.get(claim_id)
        if claim:
            perspective_ids.update(perspective_ids_for_claim(claim, perspective_config))
    return sorted(perspective_ids)


def locality_scopes_for_claim(claim: dict[str, Any]) -> list[str]:
    scopes: set[str] = set()
    document_id = claim.get("source_document_id") or ""
    topic = claim.get("topic") or ""
    applies_to = [str(value).lower() for value in claim.get("applies_to") or []]

    if document_id.startswith("mun_almere") or any("almere" in value for value in applies_to):
        scopes.add("almere")
    if document_id.startswith("reg_flevoland") or any("flevoland" in value for value in applies_to):
        scopes.add("iza_azwa_regio_flevoland")
    if not scopes and (topic.startswith("municipal.") or claim.get("jurisdiction_level") in {"municipal", "regional"}):
        scopes.add("general_locality")
    return sorted(scopes)


def locality_scopes_for_item(
    item: dict[str, Any],
    claim_index: dict[str, dict[str, Any]],
) -> list[str]:
    scopes: set[str] = set()
    document_id = item.get("document_id") or ""
    topic = item.get("topic") or ""
    source_paths = [link.get("path", "") for link in item.get("source_links") or []]

    if document_id.startswith("mun_almere") or any("mun_almere" in path or "site_almere" in path for path in source_paths):
        scopes.add("almere")
    if (
        document_id.startswith("reg_flevoland")
        or item.get("origin") == "regional_role_review"
        or any("reg_flevoland" in path or "regional_roles_and_splits" in path for path in source_paths)
    ):
        scopes.add("iza_azwa_regio_flevoland")

    for claim_id in item.get("sample_claim_ids") or []:
        claim = claim_index.get(claim_id)
        if claim:
            scopes.update(locality_scopes_for_claim(claim))

    if not scopes and "locality" in item.get("perspective_ids", []):
        if topic.startswith("municipal.") or topic.startswith("timeline.") or topic.startswith("monitoring."):
            scopes.add("general_locality")
    return sorted(scopes)


def add_locality_scopes(
    items: list[dict[str, Any]],
    claim_index: dict[str, dict[str, Any]],
) -> None:
    for item in items:
        item["locality_scope_ids"] = locality_scopes_for_item(item, claim_index)


def claim_ids_from_review_item(item: dict[str, Any]) -> list[str]:
    related_ids = item.get("related_ids") or {}
    return list(related_ids.get("sample_claim_ids") or [])


def issue_types_for_rough_codes(issue_codes: list[str]) -> list[str]:
    issue_types: set[str] = set()
    for code in issue_codes:
        issue_types.update(ROUGH_CODE_TO_ISSUE_TYPES.get(code, ["tekstprobleem"]))
    return sorted(issue_types)


def source_links(paths: list[str]) -> list[dict[str, str]]:
    links: list[dict[str, str]] = []
    for path in paths:
        links.append({"path": path, "href": output_relative_link(path)})
    return links


def make_item(
    *,
    item_id: str,
    origin: str,
    title: str,
    summary: str,
    issue_types: list[str],
    perspective_ids: list[str],
    status: str = "open",
    severity: str = "review",
    reason_code: str | None = None,
    document_id: str | None = None,
    topic: str | None = None,
    action: str | None = None,
    source_paths: list[str] | None = None,
    sample_claim_ids: list[str] | None = None,
    evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "item_id": item_id,
        "origin": origin,
        "title": title,
        "summary": summary,
        "issue_types": sorted(set(issue_types)),
        "perspective_ids": sorted(set(perspective_ids)),
        "status": status,
        "severity": severity,
        "reason_code": reason_code,
        "document_id": document_id,
        "topic": topic,
        "action": action,
        "source_links": source_links(source_paths or []),
        "sample_claim_ids": sample_claim_ids or [],
        "evidence": evidence or {},
    }


def review_queue_items(
    review_queue: dict[str, Any],
    claim_index: dict[str, dict[str, Any]],
    perspective_config: dict[str, Any],
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for review_item in review_queue.get("items", []):
        claim_ids = claim_ids_from_review_item(review_item)
        perspectives = derive_perspectives_from_claim_ids(claim_ids, claim_index, perspective_config)
        perspectives.extend(perspective_ids_for_topic(review_item.get("topic"), perspective_config))
        reason_code = review_item.get("reason_code")
        issue_types = REVIEW_REASON_TO_ISSUE_TYPES.get(reason_code, ["claimprobleem"])
        items.append(
            make_item(
                item_id=review_item.get("review_item_id") or f"review-{len(items) + 1}",
                origin="review_queue",
                title=review_item.get("summary") or "Review queue item",
                summary=review_item.get("summary") or "",
                issue_types=issue_types,
                perspective_ids=perspectives,
                status=review_item.get("status") or "open",
                severity=review_item.get("severity") or "review",
                reason_code=reason_code,
                document_id=review_item.get("document_id"),
                topic=review_item.get("topic"),
                action=review_item.get("recommended_action"),
                source_paths=review_item.get("source_paths") or [],
                sample_claim_ids=claim_ids,
                evidence=review_item.get("evidence") or {},
            )
        )
    return items


def audit_topic_items(audit: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    topic_audit = audit.get("topic_bucket_audit") or {}
    for bucket_name, title_prefix in (
        ("broad_rest_topics", "Broad rest topic"),
        ("high_volume_topics", "High-volume topic"),
    ):
        for topic_item in topic_audit.get(bucket_name, []):
            topic = topic_item.get("topic") or "unknown"
            issue_types = ["claimprobleem"]
            if topic_item.get("needs_human_review"):
                issue_types.append("interpretatieprobleem")
            items.append(
                make_item(
                    item_id=f"{bucket_name}-{slug(topic)}",
                    origin=bucket_name,
                    title=f"{title_prefix}: {topic}",
                    summary=topic_item.get("interpretation_summary") or "",
                    issue_types=issue_types,
                    perspective_ids=topic_item.get("perspective_ids") or [],
                    reason_code="needs_human_review" if topic_item.get("needs_human_review") else None,
                    topic=topic,
                    action="Review whether this topic bucket should be split before deeper text or claim cleanup.",
                    sample_claim_ids=topic_item.get("sample_claim_ids") or [],
                    evidence={
                        "current_claim_count": topic_item.get("current_claim_count"),
                        "historical_claim_count": topic_item.get("historical_claim_count"),
                        "confidence": topic_item.get("confidence"),
                        "sample_documents": topic_item.get("sample_documents") or [],
                    },
                )
            )
    return items


def audit_mapping_gap_items(audit: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    claims_audit = ((audit.get("perspective_coverage") or {}).get("claims") or {})
    for gap in claims_audit.get("topic_mapping_gaps") or []:
        topic = gap.get("topic") or "unknown"
        items.append(
            make_item(
                item_id=f"mapping-gap-{slug(topic)}",
                origin="topic_mapping_gap",
                title=f"Perspective mapping gap: {topic}",
                summary=f"{gap.get('claim_without_perspective_count', 0)} claim(s) do not map to a perspective.",
                issue_types=["claimprobleem"],
                perspective_ids=[],
                reason_code="missing_perspective_mapping",
                topic=topic,
                action="Decide whether the topic belongs in an existing perspective or needs a more specific topic split.",
                sample_claim_ids=gap.get("sample_claim_ids") or [],
            )
        )
    return items


def rough_claim_items(audit: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    rough = audit.get("rough_publication_claims") or {}
    for rough_item in rough.get("claims") or []:
        issue_codes = rough_item.get("issue_codes") or []
        claim_id = rough_item.get("claim_id") or f"rough-{len(items) + 1}"
        items.append(
            make_item(
                item_id=f"rough-{claim_id}",
                origin="rough_publication_claim",
                title=f"Rough claim text: {claim_id}",
                summary=rough_item.get("statement_excerpt") or "",
                issue_types=issue_types_for_rough_codes(issue_codes),
                perspective_ids=rough_item.get("perspective_ids") or [],
                reason_code=", ".join(issue_codes) if issue_codes else "rough_claim_text",
                document_id=rough_item.get("document_id"),
                topic=rough_item.get("topic"),
                action="Rewrite or re-extract before using this claim text in public-facing publication.",
                sample_claim_ids=[claim_id],
            )
        )
    return items


def site_text_risk_items(audit: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    risks = audit.get("site_text_risks") or {}
    for risk in risks.get("files") or []:
        path = risk.get("path") or "unknown"
        sample_claims = risk.get("sample_claims") or []
        issue_codes = sorted({code for claim in sample_claims for code in claim.get("issue_codes", [])})
        claim_ids = [claim.get("claim_id") for claim in sample_claims if claim.get("claim_id")]
        summary = f"{risk.get('rough_claim_count', 0)} rough claim(s) are referenced by this site view model."
        items.append(
            make_item(
                item_id=f"site-risk-{slug(path)}",
                origin="site_text_risk",
                title=f"Site text risk: {path}",
                summary=summary,
                issue_types=issue_types_for_rough_codes(issue_codes) or ["tekstprobleem"],
                perspective_ids=[],
                reason_code=", ".join(issue_codes) if issue_codes else "site_text_risk",
                action="Clean the underlying claims or generated summary before relying on this view for public text.",
                source_paths=[path],
                sample_claim_ids=claim_ids,
                evidence={"page_group": risk.get("page_group"), "sample_claims": sample_claims[:5]},
            )
        )
    return items


def regional_review_items(regional_roles: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not regional_roles:
        return []
    items: list[dict[str, Any]] = []
    for role in regional_roles.get("regional_roles") or []:
        if role.get("source_status") != "human_claim_needs_verification":
            continue
        role_id = role.get("role_id") or f"regional-{len(items) + 1}"
        items.append(
            make_item(
                item_id=f"regional-{role_id}",
                origin="regional_role_review",
                title=f"Regional role review: {role.get('actor') or role_id}",
                summary=role.get("claim") or role.get("review_question") or "",
                issue_types=["bronprobleem", "interpretatieprobleem"],
                perspective_ids=["governance", "locality", "execution"],
                reason_code="human_claim_needs_verification",
                action=role.get("review_question"),
                source_paths=[
                    "docs/regional-roles-and-splits-almere-flevoland.md",
                    repo_path(REGIONAL_ROLES_PATH),
                ],
                evidence={"agent_warning": role.get("agent_warning")},
            )
        )
    return items


def build_perspective_summary(
    audit: dict[str, Any],
    items: list[dict[str, Any]],
    perspective_config: dict[str, Any],
) -> list[dict[str, Any]]:
    claim_counts = {
        item["perspective_id"]: item
        for item in ((audit.get("perspective_coverage") or {}).get("claims") or {}).get("claims_by_perspective", [])
    }
    summaries: list[dict[str, Any]] = []
    for perspective in perspective_config["perspectives"]:
        perspective_id = perspective["perspective_id"]
        related_items = [item for item in items if perspective_id in item.get("perspective_ids", [])]
        issue_counts: Counter[str] = Counter()
        origin_counts: Counter[str] = Counter()
        for item in related_items:
            origin_counts[item["origin"]] += 1
            for issue_type in item.get("issue_types", []):
                issue_counts[issue_type] += 1
        claim_info = claim_counts.get(perspective_id, {})
        summaries.append(
            {
                "perspective_id": perspective_id,
                "title": perspective["title"],
                "question": perspective["question"],
                "claim_count": claim_info.get("claim_count", 0),
                "topic_count": claim_info.get("topic_count", 0),
                "open_item_count": len(related_items),
                "issue_counts": dict(sorted(issue_counts.items())),
                "origin_counts": dict(sorted(origin_counts.items())),
            }
        )
    return summaries


def build_issue_type_summary(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for issue_type, description in ISSUE_TYPES.items():
        related_items = [item for item in items if issue_type in item.get("issue_types", [])]
        origin_counts = Counter(item["origin"] for item in related_items)
        perspective_counts: Counter[str] = Counter()
        for item in related_items:
            for perspective_id in item.get("perspective_ids", []):
                perspective_counts[perspective_id] += 1
        summaries.append(
            {
                "issue_type": issue_type,
                "description": description,
                "open_item_count": len(related_items),
                "origin_counts": dict(sorted(origin_counts.items())),
                "perspective_counts": dict(sorted(perspective_counts.items())),
            }
        )
    return summaries


def build_locality_scope_summary(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for scope_id, scope in LOCALITY_SCOPES.items():
        related_items = [item for item in items if scope_id in item.get("locality_scope_ids", [])]
        issue_counts: Counter[str] = Counter()
        origin_counts: Counter[str] = Counter()
        for item in related_items:
            origin_counts[item["origin"]] += 1
            for issue_type in item.get("issue_types", []):
                issue_counts[issue_type] += 1
        summaries.append(
            {
                "scope_id": scope_id,
                "label": scope["label"],
                "description": scope["description"],
                "open_item_count": len(related_items),
                "issue_counts": dict(sorted(issue_counts.items())),
                "origin_counts": dict(sorted(origin_counts.items())),
            }
        )
    return summaries


def izwa_flevoland_definition(regional_roles: dict[str, Any] | None) -> dict[str, Any]:
    if not regional_roles:
        return {}
    for split in regional_roles.get("regional_splits") or []:
        if split.get("split_id") == "iza_azwa_regio_flevoland":
            return {
                "label": split.get("label"),
                "region_type": split.get("region_type"),
                "almere_position": split.get("almere_position"),
                "included_municipalities": split.get("included_municipalities") or [],
                "excluded_or_exception": split.get("not_in_this_split_or_exception") or [],
                "source_status": split.get("source_status"),
                "agent_warning": split.get("agent_warning"),
                "source_ids": split.get("source_ids") or [],
            }
    return {}


def parse_sprint_ledger() -> dict[str, Any]:
    text = ROADMAP_PATH.read_text(encoding="utf-8")
    rows: list[dict[str, str]] = []
    in_table = False

    for line in text.splitlines():
        if line.startswith("| Sprint | Status |"):
            in_table = True
            continue
        if not in_table:
            continue
        if line.startswith("| ---"):
            continue
        if not line.startswith("|"):
            break

        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 3:
            continue
        sprint, status, note = cells
        rows.append({"sprint": sprint, "status": status, "note": note})

    current = next((row for row in rows if "Huidige volgende sprint" in row["note"]), None)
    if current is None:
        current = next((row for row in rows if row["status"] == "open"), None)

    completed_count = sum(1 for row in rows if row["status"] == "completed")
    open_count = sum(1 for row in rows if row["status"] == "open")
    history = list(reversed([row for row in rows if row["status"] == "completed"]))[:6]

    return {
        "path": repo_path(ROADMAP_PATH),
        "href": output_relative_link(repo_path(ROADMAP_PATH)),
        "rows": rows,
        "current": current,
        "history": history,
        "completed_count": completed_count,
        "open_count": open_count,
    }


def build_dashboard_data() -> dict[str, Any]:
    audit = load_json(AUDIT_PATH)
    review_queue = load_json(REVIEW_QUEUE_PATH)
    perspective_config = load_json(PERSPECTIVES_PATH)
    regional_roles = load_json(REGIONAL_ROLES_PATH) if REGIONAL_ROLES_PATH.exists() else None
    public_updates = load_json(SITE_UPDATES_PATH) if SITE_UPDATES_PATH.exists() else {"updates": []}
    workagenda_d5 = load_json(WORKAGENDA_D5_PATH) if WORKAGENDA_D5_PATH.exists() else {}
    local_source_strengthening = load_json(LOCAL_SOURCE_STRENGTHENING_PATH) if LOCAL_SOURCE_STRENGTHENING_PATH.exists() else {}
    sprint_ledger = parse_sprint_ledger()
    claims = load_claims()
    claim_index = {claim["claim_id"]: claim for claim in claims}

    items: list[dict[str, Any]] = []
    items.extend(review_queue_items(review_queue, claim_index, perspective_config))
    items.extend(audit_topic_items(audit))
    items.extend(audit_mapping_gap_items(audit))
    items.extend(rough_claim_items(audit))
    items.extend(site_text_risk_items(audit))
    items.extend(regional_review_items(regional_roles))
    add_locality_scopes(items, claim_index)

    origins = sorted({item["origin"] for item in items})
    open_items = [item for item in items if item.get("status") == "open"]
    source_paths = [
        repo_path(AUDIT_PATH),
        repo_path(REVIEW_QUEUE_PATH),
        repo_path(PERSPECTIVES_PATH),
        repo_path(CLAIMS_MASTER_PATH),
        repo_path(ROADMAP_PATH),
        repo_path(SITE_UPDATES_PATH),
    ]
    if workagenda_d5:
        source_paths.append(repo_path(WORKAGENDA_D5_PATH))
    if local_source_strengthening:
        source_paths.append(repo_path(LOCAL_SOURCE_STRENGTHENING_PATH))
    if regional_roles:
        source_paths.append(repo_path(REGIONAL_ROLES_PATH))

    return {
        "generated_on": date.today().isoformat(),
        "title": "Internal Review Dashboard",
        "subtitle": "Local-only workbench for current sprint status, cleanup targets, and open data-quality issues.",
        "language_note": (
            "Internal developer/agent UI uses English technical framing. Dutch domain labels are kept where "
            "they come from the roadmap, corpus, or review taxonomy."
        ),
        "public_boundary_note": (
            "This file is an internal repository artifact. It is not linked from dist/ and does not belong "
            "to the public-facing GitHub Pages site."
        ),
        "maintenance_policy": (
            "When sprint status, current sprint, cleanup targets, source coverage, review data, or public update history "
            "changes, rerun src/build_internal_review_dashboard.py before committing so this dashboard shows the "
            "latest plan state."
        ),
        "inputs": [{"path": path, "href": output_relative_link(path)} for path in source_paths],
        "audit_summary": audit.get("summary") or {},
        "review_summary": review_queue.get("summary") or {},
        "items": items,
        "origins": origins,
        "issue_types": [
            {"issue_type": issue_type, "description": description}
            for issue_type, description in ISSUE_TYPES.items()
        ],
        "locality_scopes": [
            {"scope_id": scope_id, **scope}
            for scope_id, scope in LOCALITY_SCOPES.items()
        ],
        "perspectives": build_perspective_summary(audit, items, perspective_config),
        "issue_type_summary": build_issue_type_summary(items),
        "locality_scope_summary": build_locality_scope_summary(items),
        "sprint_ledger": sprint_ledger,
        "next_cleanup_targets": audit.get("next_cleanup_targets") or [],
        "public_updates": {
            "path": repo_path(SITE_UPDATES_PATH),
            "href": output_relative_link(repo_path(SITE_UPDATES_PATH)),
            "generated_on": public_updates.get("generated_on"),
            "as_of_date": public_updates.get("as_of_date"),
            "title": public_updates.get("title", "Updates"),
            "updates": public_updates.get("updates") or [],
        },
        "workagenda_d5": {
            "path": repo_path(WORKAGENDA_D5_PATH),
            "href": output_relative_link(repo_path(WORKAGENDA_D5_PATH)),
            **workagenda_d5,
        } if workagenda_d5 else {},
        "local_source_strengthening": {
            "path": repo_path(LOCAL_SOURCE_STRENGTHENING_PATH),
            "href": output_relative_link(repo_path(LOCAL_SOURCE_STRENGTHENING_PATH)),
            **local_source_strengthening,
        } if local_source_strengthening else {},
        "regional_guardrails": {
            "path": "docs/regional-roles-and-splits-almere-flevoland.md",
            "href": output_relative_link("docs/regional-roles-and-splits-almere-flevoland.md"),
            "editorial_rule": (regional_roles or {}).get("editorial_rule"),
            "iza_azwa_regio_flevoland": izwa_flevoland_definition(regional_roles),
            "review_prompts": [
                role for role in (regional_roles or {}).get("regional_roles", [])
                if role.get("source_status") == "human_claim_needs_verification"
            ],
        },
        "totals": {
            "dashboard_item_count": len(items),
            "open_dashboard_item_count": len(open_items),
            "review_queue_items": len(review_queue.get("items") or []),
            "rough_claim_items": len((audit.get("rough_publication_claims") or {}).get("claims") or []),
            "site_text_risk_files": len((audit.get("site_text_risks") or {}).get("files") or []),
        },
    }


def render_html(data: dict[str, Any]) -> str:
    json_blob = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{data["title"]} - AZWA</title>
  <style>
    :root {{
      --bg: #f8fafc;
      --panel: #ffffff;
      --line: #d7dee8;
      --text: #17202a;
      --muted: #5f6c7b;
      --strong: #0f2f4a;
      --accent: #0b6e69;
      --accent-soft: #e5f3f1;
      --warn: #8a4b00;
      --warn-soft: #fff2d9;
      --bad: #8b1f1f;
      --bad-soft: #fae5e5;
      --code: #eef2f7;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: Arial, Helvetica, sans-serif;
      font-size: 15px;
      line-height: 1.45;
    }}
    a {{ color: #0b5cad; }}
    header {{
      border-bottom: 1px solid var(--line);
      background: #ffffff;
      padding: 24px 32px 18px;
    }}
    .tabbar {{
      position: sticky;
      top: 0;
      z-index: 5;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      padding: 10px 32px;
      border-bottom: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.96);
    }}
    .tab-button {{
      min-height: 34px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: #fff;
      color: var(--text);
      padding: 6px 12px;
      font: inherit;
      cursor: pointer;
    }}
    .tab-button.active {{
      background: var(--strong);
      border-color: var(--strong);
      color: #fff;
    }}
    .tab-panel[hidden] {{ display: none; }}
    main {{ padding: 24px 32px 40px; }}
    h1 {{ margin: 0 0 8px; font-size: 28px; letter-spacing: 0; color: var(--strong); }}
    h2 {{ margin: 0 0 14px; font-size: 19px; letter-spacing: 0; color: var(--strong); }}
    h3 {{ margin: 0 0 8px; font-size: 16px; letter-spacing: 0; }}
    p {{ margin: 0 0 10px; }}
    .subtle {{ color: var(--muted); }}
    .meta-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 14px;
    }}
    .pill {{
      display: inline-flex;
      align-items: center;
      min-height: 28px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: #fff;
      color: var(--text);
      padding: 4px 10px;
      font-size: 13px;
      white-space: nowrap;
    }}
    .pill.accent {{ background: var(--accent-soft); border-color: #b7dcd8; color: #07514d; }}
    .pill.warn {{ background: var(--warn-soft); border-color: #f0cf8a; color: var(--warn); }}
    .status-completed {{ color: #0a5a35; font-weight: 700; }}
    .status-open {{ color: var(--warn); font-weight: 700; }}
    .toolbar {{
      display: grid;
      grid-template-columns: minmax(220px, 2fr) repeat(4, minmax(150px, 1fr));
      gap: 12px;
      margin-bottom: 18px;
      align-items: end;
    }}
    label {{ display: block; color: var(--muted); font-size: 12px; margin-bottom: 4px; }}
    input, select {{
      width: 100%;
      min-height: 38px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fff;
      color: var(--text);
      padding: 8px 10px;
      font: inherit;
    }}
    section {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
      margin-bottom: 18px;
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(5, minmax(120px, 1fr));
      gap: 12px;
    }}
    .metric {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
      background: #fbfdff;
    }}
    .metric strong {{ display: block; font-size: 26px; margin-bottom: 2px; color: var(--strong); }}
    .metric span {{ color: var(--muted); font-size: 13px; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ border-bottom: 1px solid var(--line); padding: 9px 8px; text-align: left; vertical-align: top; }}
    th {{ font-size: 12px; text-transform: uppercase; color: var(--muted); background: #fbfdff; }}
    tbody tr:hover {{ background: #f7fbff; }}
    .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }}
    .grid-3 {{ display: grid; grid-template-columns: 1.2fr 1fr 1fr; gap: 18px; }}
    .items-header {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: baseline;
      margin-bottom: 12px;
    }}
    .item {{
      border-top: 1px solid var(--line);
      padding: 14px 0;
    }}
    .item:first-of-type {{ border-top: 0; padding-top: 0; }}
    .item-title {{ font-weight: 700; margin-bottom: 6px; }}
    .item-summary {{ margin-bottom: 8px; color: #263441; }}
    .tag-row {{ display: flex; flex-wrap: wrap; gap: 6px; margin: 8px 0; }}
    .tag {{
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      border-radius: 999px;
      padding: 3px 8px;
      background: var(--code);
      color: #293745;
      font-size: 12px;
      white-space: nowrap;
    }}
    .tag.issue {{ background: var(--warn-soft); color: var(--warn); }}
    .tag.perspective {{ background: var(--accent-soft); color: #07514d; }}
    .tag.origin {{ background: #e7edf7; color: #244464; }}
    .tag.locality {{ background: #f0e8ff; color: #4b267d; }}
    .item-detail {{
      color: var(--muted);
      font-size: 13px;
      display: grid;
      gap: 4px;
    }}
    code {{
      background: var(--code);
      border-radius: 4px;
      padding: 2px 4px;
      font-family: Consolas, Monaco, monospace;
      font-size: 12px;
    }}
    ul.compact {{ margin: 8px 0 0; padding-left: 18px; }}
    .ledger-table tbody tr.current {{ background: #fff8e8; }}
    .empty {{ color: var(--muted); padding: 16px 0; }}
    @media (max-width: 980px) {{
      header, main {{ padding-left: 18px; padding-right: 18px; }}
      .tabbar {{ padding-left: 18px; padding-right: 18px; }}
      .toolbar, .grid-2, .grid-3 {{ grid-template-columns: 1fr; }}
      .metrics {{ grid-template-columns: repeat(2, minmax(120px, 1fr)); }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Internal Review Dashboard</h1>
    <p class="subtle">{data["subtitle"]}</p>
    <div class="meta-row">
      <span class="pill accent">Generated: {data["generated_on"]}</span>
      <span class="pill">Local file, not dist/</span>
      <span class="pill warn">Internal technical categories</span>
    </div>
  </header>
  <nav class="tabbar" aria-label="Dashboard tabs">
    <button class="tab-button active" type="button" data-tab="overview">Overview</button>
    <button class="tab-button" type="button" data-tab="local-sources">Local Sources</button>
    <button class="tab-button" type="button" data-tab="workagenda">Werkagenda</button>
    <button class="tab-button" type="button" data-tab="sprint-history">Sprint History</button>
    <button class="tab-button" type="button" data-tab="public-updates">Public Updates Mirror</button>
    <button class="tab-button" type="button" data-tab="open-items">Open Items</button>
  </nav>
  <main>
    <div class="tab-panel" data-tab-panel="overview">
      <section>
        <h2>Scope</h2>
        <p>{data["language_note"]}</p>
        <p class="subtle">{data["public_boundary_note"]}</p>
        <p class="subtle"><strong>Update policy:</strong> {data["maintenance_policy"]}</p>
        <p class="subtle">Inputs: <span id="inputLinks"></span></p>
      </section>

      <section>
        <h2>Sprint Ledger</h2>
        <div id="sprintLedger"></div>
      </section>

      <section>
        <h2>Cleanup Items</h2>
        <div id="cleanupTargets"></div>
      </section>

      <section>
        <h2>Dashboard Metrics</h2>
        <div class="metrics" id="metrics"></div>
      </section>

      <div class="grid-2">
        <section>
          <h2>Perspective Summary</h2>
          <div id="perspectiveSummary"></div>
        </section>
        <section>
          <h2>Issue Type Summary</h2>
          <div id="issueSummary"></div>
        </section>
      </div>

      <section>
        <h2>Locality Split</h2>
        <p class="subtle">The broad Locality perspective is split here into Almere-specific and IZA/AZWA-regio Flevoland items. General locality items are kept separate when the current data does not support a more specific assignment.</p>
        <div id="localitySummary"></div>
      </section>

      <section>
        <h2>Regional Guardrail</h2>
        <p id="regionalRule"></p>
        <div id="regionDefinition"></div>
        <p><a id="regionalLink" href="#">Open regional roles guide</a></p>
        <div id="regionalPrompts"></div>
      </section>
    </div>

    <div class="tab-panel" data-tab-panel="local-sources" hidden>
      <section>
        <h2>Local Source Strengthening</h2>
        <p class="subtle">Internal mirror of <a id="localSourcesLink" href="#"><code id="localSourcesPath"></code></a>. Candidate sources are source-intake tasks, not claim facts.</p>
        <div class="metrics" id="localSourceMetrics"></div>
      </section>

      <section>
        <h2>Candidate Sources</h2>
        <div id="localSourceCandidates"></div>
      </section>

      <section>
        <h2>Target Source Needs</h2>
        <div id="targetSourceNeeds"></div>
      </section>
    </div>

    <div class="tab-panel" data-tab-panel="sprint-history" hidden>
      <section>
        <h2>Sprint History</h2>
        <div id="sprintHistory"></div>
      </section>
    </div>

    <div class="tab-panel" data-tab-panel="workagenda" hidden>
      <section>
        <h2>D5 Werkagenda Operational Layer</h2>
        <p class="subtle">Internal mirror of <a id="workagendaSourceLink" href="#"><code id="workagendaSourcePath"></code></a>. Concept status is a review aid, not an adopted Almere decision.</p>
        <div class="metrics" id="workagendaMetrics"></div>
      </section>

      <section>
        <h2>Targets</h2>
        <div id="workagendaTargets"></div>
      </section>

      <section>
        <h2>Finance Guardrails</h2>
        <div id="workagendaFinance"></div>
      </section>
    </div>

    <div class="tab-panel" data-tab-panel="public-updates" hidden>
      <section>
        <h2>Public Updates Mirror</h2>
        <p class="subtle">Mirror of the public-facing update data from <code>data/site/site_updates_view.json</code>. This tab preserves the data-update history used by the public site while keeping this dashboard internal.</p>
        <div id="publicUpdates"></div>
      </section>
    </div>

    <div class="tab-panel" data-tab-panel="open-items" hidden>
      <section>
        <h2>Filters</h2>
        <div class="toolbar">
          <div>
            <label for="search">Search</label>
            <input id="search" type="search" placeholder="document, claim, topic, reason, summary">
          </div>
          <div>
            <label for="perspectiveFilter">Perspective</label>
            <select id="perspectiveFilter"></select>
          </div>
          <div>
            <label for="issueFilter">Issue type</label>
            <select id="issueFilter"></select>
          </div>
          <div>
            <label for="localityFilter">Locality scope</label>
            <select id="localityFilter"></select>
          </div>
          <div>
            <label for="originFilter">Origin</label>
            <select id="originFilter"></select>
          </div>
        </div>
      </section>

      <section>
        <div class="items-header">
          <h2>Open Items</h2>
          <p class="subtle" id="itemCount"></p>
        </div>
        <div id="items"></div>
      </section>
    </div>
  </main>

  <script id="dashboard-data" type="application/json">{json_blob}</script>
  <script>
    const DATA = JSON.parse(document.getElementById('dashboard-data').textContent);
    const state = {{ search: '', perspective: 'all', issue: 'all', locality: 'all', origin: 'all' }};

    const byId = (id) => document.getElementById(id);
    const esc = (value) => String(value ?? '').replace(/[&<>"']/g, ch => ({{
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }}[ch]));
    const pretty = (value) => String(value || '').replaceAll('_', ' ');
    const localityLabelMap = Object.fromEntries(DATA.locality_scopes.map(scope => [scope.scope_id, scope.label]));
    const localityLabel = (value) => localityLabelMap[value] || pretty(value);

    function optionList(select, values, label) {{
      select.innerHTML = `<option value="all">All ${{label}}</option>` +
        values.map(value => `<option value="${{esc(value)}}">${{esc(pretty(value))}}</option>`).join('');
    }}

    function localityOptionList(select) {{
      select.innerHTML = '<option value="all">All locality scopes</option>' +
        DATA.locality_scopes.map(scope => `<option value="${{esc(scope.scope_id)}}">${{esc(scope.label)}}</option>`).join('');
    }}

    function initFilters() {{
      optionList(byId('perspectiveFilter'), DATA.perspectives.map(p => p.perspective_id), 'perspectives');
      optionList(byId('issueFilter'), DATA.issue_types.map(i => i.issue_type), 'issue types');
      localityOptionList(byId('localityFilter'));
      optionList(byId('originFilter'), DATA.origins, 'origins');
      byId('search').addEventListener('input', event => {{ state.search = event.target.value.toLowerCase(); render(); }});
      byId('perspectiveFilter').addEventListener('change', event => {{ state.perspective = event.target.value; render(); }});
      byId('issueFilter').addEventListener('change', event => {{ state.issue = event.target.value; render(); }});
      byId('localityFilter').addEventListener('change', event => {{ state.locality = event.target.value; render(); }});
      byId('originFilter').addEventListener('change', event => {{ state.origin = event.target.value; render(); }});
    }}

    function filteredItems() {{
      return DATA.items.filter(item => {{
        if (state.perspective !== 'all' && !item.perspective_ids.includes(state.perspective)) return false;
        if (state.issue !== 'all' && !item.issue_types.includes(state.issue)) return false;
        if (state.locality !== 'all' && !(item.locality_scope_ids || []).includes(state.locality)) return false;
        if (state.origin !== 'all' && item.origin !== state.origin) return false;
        if (!state.search) return true;
        const haystack = [
          item.item_id, item.origin, item.title, item.summary, item.reason_code, item.document_id, item.topic,
          item.action, ...(item.sample_claim_ids || []), ...(item.perspective_ids || []), ...(item.issue_types || []),
          ...(item.locality_scope_ids || [])
        ].join(' ').toLowerCase();
        return haystack.includes(state.search);
      }});
    }}

    function renderInputs() {{
      byId('inputLinks').innerHTML = DATA.inputs.map(input =>
        `<a href="${{esc(input.href)}}"><code>${{esc(input.path)}}</code></a>`
      ).join(', ');
    }}

    function initTabs() {{
      const buttons = Array.from(document.querySelectorAll('[data-tab]'));
      const panels = Array.from(document.querySelectorAll('[data-tab-panel]'));
      buttons.forEach(button => {{
        button.addEventListener('click', () => {{
          const target = button.dataset.tab;
          buttons.forEach(item => item.classList.toggle('active', item === button));
          panels.forEach(panel => {{
            panel.hidden = panel.dataset.tabPanel !== target;
          }});
        }});
      }});
    }}

    function renderMetrics(items) {{
      const issueTypes = new Set(items.flatMap(item => item.issue_types));
      const localityScopes = new Set(items.flatMap(item => item.locality_scope_ids || []));
      const reviewItems = items.filter(item => item.origin === 'review_queue').length;
      const roughItems = items.filter(item => item.origin === 'rough_publication_claim').length;
      const metrics = [
        ['Dashboard items', items.length],
        ['Review queue', reviewItems],
        ['Rough claim text', roughItems],
        ['Issue types', issueTypes.size],
        ['Locality scopes', localityScopes.size || 0]
      ];
      byId('metrics').innerHTML = metrics.map(([label, value]) =>
        `<div class="metric"><strong>${{esc(value)}}</strong><span>${{esc(label)}}</span></div>`
      ).join('');
    }}

    function renderSprintLedger() {{
      const ledger = DATA.sprint_ledger || {{}};
      const rows = ledger.rows || [];
      const currentSprint = ledger.current ? ledger.current.sprint : '';
      const visibleRows = rows.filter(row => row.status === 'open' || row.sprint === currentSprint).slice(0, 10);
      const tableRows = visibleRows.map(row => {{
        const isCurrent = row.sprint === currentSprint;
        const statusClass = row.status === 'completed' ? 'status-completed' : 'status-open';
        return `<tr class="${{isCurrent ? 'current' : ''}}">
          <td><strong>${{esc(row.sprint)}}</strong>${{isCurrent ? '<br><span class="pill warn">Current</span>' : ''}}</td>
          <td class="${{statusClass}}">${{esc(row.status)}}</td>
          <td>${{esc(row.note || '')}}</td>
        </tr>`;
      }}).join('');
      const currentBlock = ledger.current ? `<p><strong>Current sprint:</strong> ${{esc(ledger.current.sprint)}} <span class="status-open">${{esc(ledger.current.status)}}</span></p>` : '<p class="empty">No current sprint marked.</p>';
      byId('sprintLedger').innerHTML = `
        ${{currentBlock}}
        <p class="subtle">Source: <a href="${{esc(ledger.href || '#')}}"><code>${{esc(ledger.path || '')}}</code></a>. Completed: ${{esc(ledger.completed_count || 0)}}. Open: ${{esc(ledger.open_count || 0)}}.</p>
        <table class="ledger-table">
          <thead><tr><th>Sprint</th><th>Status</th><th>Note</th></tr></thead>
          <tbody>${{tableRows}}</tbody>
        </table>`;
    }}

    function renderSprintHistory() {{
      const ledger = DATA.sprint_ledger || {{}};
      const history = ledger.history || [];
      if (!history.length) {{
        byId('sprintHistory').innerHTML = '<p class="empty">No completed sprints recorded yet.</p>';
        return;
      }}
      const rows = history.map(row => `<tr>
        <td><strong>${{esc(row.sprint)}}</strong></td>
        <td class="status-completed">${{esc(row.status)}}</td>
        <td>${{esc(row.note || '')}}</td>
      </tr>`).join('');
      byId('sprintHistory').innerHTML = `<p class="subtle">Most recent completed sprints from the roadmap.</p>
        <table class="ledger-table">
          <thead><tr><th>Sprint</th><th>Status</th><th>Evidence / note</th></tr></thead>
          <tbody>${{rows}}</tbody>
        </table>`;
    }}

    function renderPublicUpdates() {{
      const publicUpdates = DATA.public_updates || {{}};
      const updates = publicUpdates.updates || [];
      if (!updates.length) {{
        byId('publicUpdates').innerHTML = '<p class="empty">No public updates recorded.</p>';
        return;
      }}
      const updateCards = updates.map(update => {{
        const metrics = (update.metrics || []).map(metric => {{
          const delta = metric.delta_label || (Number.isFinite(metric.delta) ? String(metric.delta) : '');
          return `<div class="metric"><strong>${{esc(metric.after ?? '')}}</strong><span>${{esc(metric.label || '')}} ${{delta ? `(${{esc(delta)}})` : ''}}</span></div>`;
        }}).join('');
        const keyPoints = (update.key_points || []).map(point => `<li>${{esc(point)}}</li>`).join('');
        const highlights = (update.change_highlights || []).map(highlight =>
          `<li><strong>${{esc(highlight.summary || '')}}</strong><br><span class="subtle">${{esc(highlight.detail || '')}}</span></li>`
        ).join('');
        const source = update.source_reference || {{}};
        return `<article class="item">
          <div class="item-title">${{esc(update.published_on || '')}} - ${{esc(update.title || update.update_id || '')}}</div>
          <div class="item-summary">${{esc(update.summary || '')}}</div>
          <div class="tag-row">
            <span class="tag origin">public update</span>
            <span class="tag perspective">${{esc(update.update_id || '')}}</span>
          </div>
          <div class="item-detail">
            ${{source.title || source.label ? `<div><strong>Source:</strong> ${{esc(source.title || source.label)}} ${{source.publisher ? `(${{esc(source.publisher)}})` : ''}}</div>` : ''}}
            ${{update.page_url ? `<div><strong>Public page path:</strong> <code>${{esc(update.page_url)}}</code></div>` : ''}}
            ${{publicUpdates.path ? `<div><strong>Mirror source:</strong> <a href="${{esc(publicUpdates.href || '#')}}"><code>${{esc(publicUpdates.path)}}</code></a></div>` : ''}}
          </div>
          ${{metrics ? `<div class="metrics" style="margin-top: 12px;">${{metrics}}</div>` : ''}}
          ${{keyPoints ? `<h3 style="margin-top: 14px;">Key points</h3><ul class="compact">${{keyPoints}}</ul>` : ''}}
          ${{highlights ? `<h3 style="margin-top: 14px;">Change highlights</h3><ul class="compact">${{highlights}}</ul>` : ''}}
        </article>`;
      }}).join('');
      byId('publicUpdates').innerHTML = `<p class="subtle">As of ${{esc(publicUpdates.as_of_date || '')}}, generated ${{esc(publicUpdates.generated_on || '')}}.</p>${{updateCards}}`;
    }}

    function renderWorkagenda() {{
      const workagenda = DATA.workagenda_d5 || {{}};
      byId('workagendaSourceLink').href = workagenda.href || '#';
      byId('workagendaSourcePath').textContent = workagenda.path || '';
      const targets = workagenda.targets || [];
      const required = targets.filter(target => target.required_in_workagenda).length;
      const statuses = new Set(targets.map(target => target.workagenda_status));
      const reviewThemes = workagenda.open_review_themes || [];
      byId('workagendaMetrics').innerHTML = [
        ['Targets', targets.length],
        ['Required', required],
        ['Status groups', statuses.size],
        ['Review themes', reviewThemes.length],
        ['Run', workagenda.layer_run_id || '']
      ].map(([label, value]) => `<div class="metric"><strong>${{esc(value)}}</strong><span>${{esc(label)}}</span></div>`).join('');

      if (!targets.length) {{
        byId('workagendaTargets').innerHTML = '<p class="empty">No workagenda layer generated yet.</p>';
      }} else {{
        byId('workagendaTargets').innerHTML = `<table>
          <thead><tr><th>Target</th><th>Status</th><th>Scale / finance</th><th>Review questions</th></tr></thead>
          <tbody>${{targets.map(target => `
            <tr>
              <td><strong>${{esc(target.title)}}</strong><br><code>${{esc(target.target_id)}}</code><br><span class="subtle">${{esc(target.leefgebied || '')}}</span></td>
              <td>${{target.required_in_workagenda ? '<span class="pill accent">Required</span>' : '<span class="pill">Conditional</span>'}}<br><code>${{esc(target.workagenda_status || '')}}</code><br><span class="subtle">${{esc(target.almere_concept_status || '')}}</span></td>
              <td><span class="subtle">${{esc(target.scale_hint || '')}}</span><br>${{(target.finance_stream_hints || []).map(stream => `<span class="tag issue">${{esc(stream)}}</span>`).join('')}}</td>
              <td><ul class="compact">${{(target.review_questions || []).slice(0, 3).map(question => `<li>${{esc(question)}}</li>`).join('')}}</ul></td>
            </tr>`).join('')}}</tbody>
        </table>`;
      }}

      const finance = ((workagenda.finance_linking_model || {{}}).finance_streams || []);
      byId('workagendaFinance').innerHTML = finance.length ? `<table>
        <thead><tr><th>Stream</th><th>Status</th><th>Claims</th></tr></thead>
        <tbody>${{finance.map(stream => `<tr>
          <td><strong>${{esc(stream.label || stream.stream_id)}}</strong><br><code>${{esc(stream.stream_id || '')}}</code></td>
          <td>${{esc(stream.status || '')}}</td>
          <td>${{(stream.source_claim_ids || []).slice(0, 5).map(id => `<code>${{esc(id)}}</code>`).join(' ')}}</td>
        </tr>`).join('')}}</tbody>
      </table><p class="subtle">${{esc((workagenda.finance_linking_model || {{}}).review_rule || '')}}</p>` : '<p class="empty">No finance streams recorded.</p>';
    }}

    function renderLocalSources() {{
      const layer = DATA.local_source_strengthening || {{}};
      byId('localSourcesLink').href = layer.href || '#';
      byId('localSourcesPath').textContent = layer.path || '';
      const summary = layer.summary || {{}};
      const candidates = layer.candidate_sources || [];
      const targetNeeds = layer.target_source_needs || [];
      byId('localSourceMetrics').innerHTML = [
        ['Candidates', summary.candidate_source_count || candidates.length || 0],
        ['Verified URLs', summary.verified_or_candidate_url_count || 0],
        ['Not found', summary.not_found_candidate_count || 0],
        ['Municipal docs', summary.municipal_manifest_document_count || 0],
        ['Regional docs', summary.regional_manifest_document_count || 0]
      ].map(([label, value]) => `<div class="metric"><strong>${{esc(value)}}</strong><span>${{esc(label)}}</span></div>`).join('');

      if (!candidates.length) {{
        byId('localSourceCandidates').innerHTML = '<p class="empty">No local source strengthening layer generated yet.</p>';
      }} else {{
        byId('localSourceCandidates').innerHTML = `<table>
          <thead><tr><th>Source</th><th>Status</th><th>Why it matters</th><th>Review</th></tr></thead>
          <tbody>${{candidates.map(candidate => `
            <tr>
              <td><strong>${{esc(candidate.title)}}</strong><br><code>${{esc(candidate.candidate_id)}}</code><br>${{candidate.source_url ? `<a href="${{esc(candidate.source_url)}}">source URL</a>` : '<span class="subtle">No public URL verified</span>'}}</td>
              <td><span class="tag origin">${{esc(candidate.verification_status || '')}}</span><br><span class="tag issue">${{esc(candidate.intake_status || '')}}</span><br><span class="subtle">${{esc(candidate.current_repository_status || '')}}</span></td>
              <td>${{esc(candidate.why_it_matters || '')}}<br>${{candidate.intake_recommendation ? `<strong>Recommendation:</strong> ${{esc(candidate.intake_recommendation)}}<br>` : ''}}${{(candidate.unlocks || []).map(value => `<span class="tag perspective">${{esc(value)}}</span>`).join('')}}</td>
              <td>${{esc(candidate.review_question || '')}}</td>
            </tr>`).join('')}}</tbody>
        </table>`;
      }}

      byId('targetSourceNeeds').innerHTML = targetNeeds.length ? `<table>
        <thead><tr><th>Target</th><th>Candidate sources</th><th>Note</th></tr></thead>
        <tbody>${{targetNeeds.map(row => `<tr>
          <td><strong>${{esc(row.title || row.target_id)}}</strong><br><code>${{esc(row.target_id || '')}}</code></td>
          <td>${{esc(row.candidate_source_count || 0)}}<br>${{(row.candidate_source_ids || []).slice(0, 5).map(id => `<code>${{esc(id)}}</code>`).join(' ')}}</td>
          <td>${{esc(row.note || '')}}</td>
        </tr>`).join('')}}</tbody>
      </table>` : '<p class="empty">No target source needs recorded.</p>';
    }}

    function countFor(items, predicate) {{
      return items.filter(predicate).length;
    }}

    function renderPerspectiveSummary(items) {{
      const rows = DATA.perspectives.map(p => {{
        const visible = countFor(items, item => item.perspective_ids.includes(p.perspective_id));
        return `<tr>
          <td><strong>${{esc(p.title)}}</strong><br><span class="subtle">${{esc(p.question)}}</span></td>
          <td>${{esc(p.claim_count)}}</td>
          <td>${{esc(p.topic_count)}}</td>
          <td>${{esc(p.open_item_count)}}</td>
          <td>${{esc(visible)}}</td>
        </tr>`;
      }}).join('');
      byId('perspectiveSummary').innerHTML = `<table>
        <thead><tr><th>Perspective</th><th>Claims</th><th>Topics</th><th>All items</th><th>Visible</th></tr></thead>
        <tbody>${{rows}}</tbody>
      </table>`;
    }}

    function renderIssueSummary(items) {{
      const rows = DATA.issue_type_summary.map(issue => {{
        const visible = countFor(items, item => item.issue_types.includes(issue.issue_type));
        return `<tr>
          <td><strong>${{esc(issue.issue_type)}}</strong><br><span class="subtle">${{esc(issue.description)}}</span></td>
          <td>${{esc(issue.open_item_count)}}</td>
          <td>${{esc(visible)}}</td>
        </tr>`;
      }}).join('');
      byId('issueSummary').innerHTML = `<table>
        <thead><tr><th>Issue type</th><th>All items</th><th>Visible</th></tr></thead>
        <tbody>${{rows}}</tbody>
      </table>`;
    }}

    function renderLocalitySummary(items) {{
      const rows = DATA.locality_scope_summary.map(scope => {{
        const visible = countFor(items, item => (item.locality_scope_ids || []).includes(scope.scope_id));
        return `<tr>
          <td><strong>${{esc(scope.label)}}</strong><br><span class="subtle">${{esc(scope.description)}}</span></td>
          <td>${{esc(scope.open_item_count)}}</td>
          <td>${{esc(visible)}}</td>
        </tr>`;
      }}).join('');
      byId('localitySummary').innerHTML = `<table>
        <thead><tr><th>Locality scope</th><th>All items</th><th>Visible</th></tr></thead>
        <tbody>${{rows}}</tbody>
      </table>`;
    }}

    function renderRegional() {{
      byId('regionalRule').textContent = DATA.regional_guardrails.editorial_rule || 'No regional guardrail configured.';
      byId('regionalLink').href = DATA.regional_guardrails.href || '#';
      const region = DATA.regional_guardrails.iza_azwa_regio_flevoland || {{}};
      const included = (region.included_municipalities || []).join(', ');
      const excluded = (region.excluded_or_exception || []).join(' ');
      byId('regionDefinition').innerHTML = region.label ? `<table>
        <tbody>
          <tr><th>Region</th><td><strong>${{esc(region.label)}}</strong> <span class="subtle">(${{esc(region.region_type || '')}})</span></td></tr>
          <tr><th>Included municipalities</th><td>${{esc(included)}}</td></tr>
          <tr><th>Excluded / exception</th><td>${{esc(excluded || 'None recorded')}}</td></tr>
          <tr><th>Almere position</th><td>${{esc(region.almere_position || '')}}</td></tr>
          <tr><th>Warning</th><td>${{esc(region.agent_warning || '')}}</td></tr>
        </tbody>
      </table>` : '';
      const prompts = DATA.regional_guardrails.review_prompts || [];
      byId('regionalPrompts').innerHTML = prompts.length ? `<ul class="compact">${{prompts.map(prompt =>
        `<li><strong>${{esc(prompt.actor || prompt.role_id)}}:</strong> ${{esc(prompt.review_question || prompt.claim || '')}}</li>`
      ).join('')}}</ul>` : '<p class="empty">No open regional review prompts.</p>';
    }}

    function renderCleanupTargets() {{
      const targets = DATA.next_cleanup_targets || [];
      byId('cleanupTargets').innerHTML = targets.length ? `<table>
        <thead><tr><th>Target</th><th>Reason</th><th>Suggested sprint</th></tr></thead>
        <tbody>${{targets.map(target => `<tr>
          <td><strong>${{esc(target.title || target.target_id)}}</strong><br><code>${{esc(target.target_id)}}</code></td>
          <td>${{esc(target.reason || '')}}</td>
          <td>${{esc(target.suggested_sprint || '')}}</td>
        </tr>`).join('')}}</tbody>
      </table>` : '<p class="empty">No cleanup targets recorded.</p>';
    }}

    function renderItems(items) {{
      byId('itemCount').textContent = `${{items.length}} visible of ${{DATA.items.length}} total`;
      if (!items.length) {{
        byId('items').innerHTML = '<p class="empty">No items match the current filters.</p>';
        return;
      }}
      byId('items').innerHTML = items.map(item => {{
        const tags = [
          ...item.issue_types.map(value => `<span class="tag issue">${{esc(value)}}</span>`),
          ...item.perspective_ids.map(value => `<span class="tag perspective">${{esc(value)}}</span>`),
          ...(item.locality_scope_ids || []).map(value => `<span class="tag locality">${{esc(localityLabel(value))}}</span>`),
          `<span class="tag origin">${{esc(item.origin)}}</span>`
        ].join('');
        const links = (item.source_links || []).map(link =>
          `<a href="${{esc(link.href)}}"><code>${{esc(link.path)}}</code></a>`
        ).join(', ');
        const claims = (item.sample_claim_ids || []).slice(0, 8).map(id => `<code>${{esc(id)}}</code>`).join(' ');
        return `<article class="item">
          <div class="item-title">${{esc(item.title)}}</div>
          <div class="item-summary">${{esc(item.summary)}}</div>
          <div class="tag-row">${{tags}}</div>
          <div class="item-detail">
            ${{item.action ? `<div><strong>Action:</strong> ${{esc(item.action)}}</div>` : ''}}
            ${{item.document_id ? `<div><strong>Document:</strong> <code>${{esc(item.document_id)}}</code></div>` : ''}}
            ${{item.topic ? `<div><strong>Topic:</strong> <code>${{esc(item.topic)}}</code></div>` : ''}}
            ${{item.reason_code ? `<div><strong>Reason:</strong> <code>${{esc(item.reason_code)}}</code></div>` : ''}}
            ${{links ? `<div><strong>Sources:</strong> ${{links}}</div>` : ''}}
            ${{claims ? `<div><strong>Sample claims:</strong> ${{claims}}</div>` : ''}}
          </div>
        </article>`;
      }}).join('');
    }}

    function render() {{
      const items = filteredItems();
      renderMetrics(items);
      renderPerspectiveSummary(items);
      renderIssueSummary(items);
      renderLocalitySummary(items);
      renderItems(items);
    }}

    initTabs();
    initFilters();
    renderInputs();
    renderSprintLedger();
    renderSprintHistory();
    renderPublicUpdates();
    renderWorkagenda();
    renderLocalSources();
    renderRegional();
    renderCleanupTargets();
    render();
  </script>
</body>
</html>
"""


def main() -> None:
    data = build_dashboard_data()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(render_html(data), encoding="utf-8")
    print(f"Wrote {repo_path(OUTPUT_PATH)}")
    print(f"Dashboard items: {data['totals']['dashboard_item_count']}")


if __name__ == "__main__":
    main()
