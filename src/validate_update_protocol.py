from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
UPDATES_PATH = REPO_ROOT / "config" / "site_updates.json"
INVENTORY_PATH = REPO_ROOT / "data" / "extracted" / "document_inventory.json"
OUTPUT_PATH = REPO_ROOT / "docs" / "internal" / "update-protocol-check-2026-04-29.md"

REQUIRED_UPDATE_FIELDS = {
    "update_id",
    "published_on",
    "title",
    "summary",
    "source_reference",
    "human_summary",
    "change_highlights",
    "key_points",
    "metrics",
    "affected_pages",
    "affected_document_ids",
    "highlighted_timeline_entry_keys",
}
REQUIRED_HUMAN_SUMMARY_FIELDS = {
    "intro",
    "what_happened",
    "what_changed",
    "why_it_matters",
}
FORBIDDEN_PUBLIC_JARGON = re.compile(
    r"dataset|claim\s*laag|bron\s*laag|pijplijn|pipeline|data/raw|manifest|"
    r"view\s*model|site-viewmodels|review_needed|source-backed|ingest(?:ed|ie|en|ion)?|"
    r"\bjson\b|\bqc\b|machine-gegenereerd",
    re.IGNORECASE,
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def inventory_document_ids() -> set[str]:
    inventory = load_json(INVENTORY_PATH)
    return {item["document_id"] for item in inventory["documents"]}


def is_iso_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def validate_updates() -> dict:
    payload = load_json(UPDATES_PATH)
    updates = payload.get("updates", [])
    document_ids = inventory_document_ids()
    issues: list[dict] = []
    seen_update_ids: set[str] = set()

    for index, update in enumerate(updates):
        update_id = update.get("update_id", f"index_{index}")
        missing = sorted(REQUIRED_UPDATE_FIELDS - set(update))
        if missing:
            issues.append({"update_id": update_id, "issue": "missing_required_fields", "detail": ", ".join(missing)})

        if update_id in seen_update_ids:
            issues.append({"update_id": update_id, "issue": "duplicate_update_id", "detail": update_id})
        seen_update_ids.add(update_id)

        if not is_iso_date(update.get("published_on", "")):
            issues.append({"update_id": update_id, "issue": "published_on_not_iso_date", "detail": update.get("published_on", "")})

        human_summary = update.get("human_summary", {})
        missing_summary = sorted(REQUIRED_HUMAN_SUMMARY_FIELDS - set(human_summary))
        if missing_summary:
            issues.append({"update_id": update_id, "issue": "missing_human_summary_fields", "detail": ", ".join(missing_summary)})
        for field_name in REQUIRED_HUMAN_SUMMARY_FIELDS:
            value = human_summary.get(field_name, "")
            if len(value) < 80:
                issues.append({"update_id": update_id, "issue": "human_summary_too_short", "detail": field_name})
            match = FORBIDDEN_PUBLIC_JARGON.search(value)
            if match:
                issues.append({"update_id": update_id, "issue": "public_jargon_in_human_summary", "detail": f"{field_name}: {match.group(0)}"})

        for highlight in update.get("change_highlights", []):
            if not highlight.get("summary") or not highlight.get("detail"):
                issues.append({"update_id": update_id, "issue": "change_highlight_missing_summary_or_detail", "detail": str(highlight)})

        for metric in update.get("metrics", []):
            if not {"label", "before", "after"}.issubset(metric):
                issues.append({"update_id": update_id, "issue": "metric_missing_required_fields", "detail": str(metric)})
            elif not isinstance(metric["before"], int) or not isinstance(metric["after"], int):
                issues.append({"update_id": update_id, "issue": "metric_values_not_int", "detail": metric.get("label", "")})

        for page in update.get("affected_pages", []):
            if not page.get("label") or not page.get("url"):
                issues.append({"update_id": update_id, "issue": "affected_page_missing_label_or_url", "detail": str(page)})

        for document_id in update.get("affected_document_ids", []):
            if document_id not in document_ids:
                issues.append({"update_id": update_id, "issue": "affected_document_id_not_in_inventory", "detail": document_id})

    return {
        "generated_on": date.today().isoformat(),
        "update_count": len(updates),
        "issue_count": len(issues),
        "issues": issues,
    }


def render_markdown(result: dict) -> str:
    lines = [
        "# Update Protocol Check",
        "",
        "## Summary",
        "Current sprint: Sprint 31.1 - Updateprotocol.",
        f"Generated on: {result['generated_on']}.",
        f"Updates checked: {result['update_count']}.",
        f"Blocking update-protocol issues found: {result['issue_count']}.",
        "",
    ]
    if result["issues"]:
        lines.append("## Issues")
        for issue in result["issues"]:
            lines.append(f"- `{issue['update_id']}`: `{issue['issue']}` - {issue['detail']}")
    else:
        lines.append("No blocking update-protocol issues found.")
    lines.extend(
        [
            "",
            "## Use",
            "Use this note as an internal control that `config/site_updates.json` is complete enough to drive the public updates page and internal dashboard mirror.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    result = validate_updates()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(render_markdown(result), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    if result["issue_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
