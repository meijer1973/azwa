from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "config" / "monthly_source_audit.json"
RAW_MANIFEST_PATH = REPO_ROOT / "data" / "raw" / "manifest.json"
SOURCE_CANDIDATES_PATH = REPO_ROOT / "data" / "raw" / "source_intake_candidates.json"
OUTPUT_JSON_PATH = REPO_ROOT / "data" / "extracted" / "monthly_source_audit.json"
OUTPUT_MD_PATH = REPO_ROOT / "docs" / "internal" / "monthly-source-audit-2026-04-30.md"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def parse_date(value: str) -> date:
    return date.fromisoformat(value)


def status_for_watch_item(item: dict, manifest_ids: set[str], as_of: date) -> str:
    if item["candidate_document_id"] in manifest_ids:
        return "ingested"
    expected_from = parse_date(item["expected_from"])
    expected_by = parse_date(item["expected_by"])
    if as_of < expected_from:
        return "not_due_yet"
    if as_of <= expected_by:
        return "watch_due"
    return "overdue"


def live_link_check(url: str, timeout: int = 12) -> dict:
    request = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": "AZWA-source-audit/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return {"checked": True, "ok": 200 <= response.status < 400, "status_code": response.status, "final_url": response.url}
    except urllib.error.HTTPError as exc:
        if exc.code in {403, 405}:
            get_request = urllib.request.Request(url, headers={"User-Agent": "AZWA-source-audit/1.0"})
            try:
                with urllib.request.urlopen(get_request, timeout=timeout) as response:
                    return {"checked": True, "ok": 200 <= response.status < 400, "status_code": response.status, "final_url": response.url}
            except Exception as get_exc:  # noqa: BLE001 - audit should capture, not crash.
                return {"checked": True, "ok": False, "status_code": getattr(get_exc, "code", None), "error": str(get_exc)}
        if 300 <= exc.code < 400:
            return {
                "checked": True,
                "ok": None,
                "review_needed": True,
                "status_code": exc.code,
                "error": str(exc),
                "note": "Redirect handling needs manual review; this is not treated as a dead link by itself.",
            }
        return {"checked": True, "ok": False, "status_code": exc.code, "error": str(exc)}
    except Exception as exc:  # noqa: BLE001 - audit should capture, not crash.
        return {"checked": True, "ok": False, "status_code": None, "error": str(exc)}


def skipped_link_check() -> dict:
    return {"checked": False, "ok": None, "status_code": None, "note": "live link check not requested"}


def format_link_label(link: dict) -> str:
    if not link.get("checked"):
        return "not checked"
    if link.get("review_needed"):
        return f"{link.get('status_code')} review"
    return f"{link.get('status_code')} {'ok' if link.get('ok') else 'issue'}"


def candidate_source_rows(candidates: dict, live: bool) -> list[dict]:
    rows: list[dict] = []
    for item in candidates.get("candidate_sources", []):
        link = live_link_check(item["source_url"]) if live else skipped_link_check()
        rows.append(
            {
                "proposed_document_id": item["proposed_document_id"],
                "title": item["title"],
                "publisher": item["publisher"],
                "priority": item["priority"],
                "ingestion_status": item["ingestion_status"],
                "source_url": item["source_url"],
                "link_check": link,
                "note": item.get("ingestion_note"),
            }
        )
    return rows


def pending_timeline_rows(candidates: dict) -> list[dict]:
    return [
        item
        for item in candidates.get("candidate_timeline_items", [])
        if item.get("status") != "ingested_context_source"
    ]


def watchlist_rows(config: dict, manifest_ids: set[str], as_of: date, live: bool) -> list[dict]:
    rows: list[dict] = []
    for item in config["watchlist"]:
        status = status_for_watch_item(item, manifest_ids, as_of)
        link = live_link_check(item["official_watch_url"]) if live else skipped_link_check()
        rows.append(
            {
                **item,
                "audit_status": status,
                "link_check": link,
            }
        )
    return rows


def build_audit(as_of: date, live: bool) -> dict:
    config = load_json(CONFIG_PATH)
    manifest = load_json(RAW_MANIFEST_PATH)
    candidates = load_json(SOURCE_CANDIDATES_PATH)
    manifest_ids = {item["document_id"] for item in manifest}
    candidate_rows = candidate_source_rows(candidates, live)
    watch_rows = watchlist_rows(config, manifest_ids, as_of, live)
    pending_timeline = pending_timeline_rows(candidates)
    candidate_status_counts = Counter(row["ingestion_status"] for row in candidate_rows)
    watch_status_counts = Counter(row["audit_status"] for row in watch_rows)
    live_link_issues = [
        row
        for row in candidate_rows + watch_rows
        if row["link_check"].get("checked") and row["link_check"].get("ok") is False
    ]
    live_link_review_items = [
        row
        for row in candidate_rows + watch_rows
        if row["link_check"].get("checked") and row["link_check"].get("review_needed")
    ]
    pending_replacements = [
        row for row in candidate_rows if row["ingestion_status"] == "pending_replacement"
    ]

    return {
        "audit_id": config["audit_id"],
        "generated_on": as_of.isoformat(),
        "live_link_check": live,
        "summary": {
            "candidate_source_count": len(candidate_rows),
            "watchlist_count": len(watch_rows),
            "pending_timeline_item_count": len(pending_timeline),
            "pending_replacement_count": len(pending_replacements),
            "live_link_issue_count": len(live_link_issues),
            "live_link_review_count": len(live_link_review_items),
            "candidate_status_counts": dict(candidate_status_counts),
            "watch_status_counts": dict(watch_status_counts),
        },
        "watchlist": watch_rows,
        "candidate_sources": candidate_rows,
        "pending_timeline_items": pending_timeline,
        "pending_replacements": pending_replacements,
        "live_link_issues": live_link_issues,
        "live_link_review_items": live_link_review_items,
        "source_boundary": "Pending sources and watchlist items are not public evidence until they are saved, added to the raw manifest, processed by the pipeline and represented in generated layers.",
    }


def render_markdown(audit: dict) -> str:
    summary = audit["summary"]
    lines = [
        "# Monthly Source Audit",
        "",
        "## Summary",
        "Current sprint: Sprint 31.2 - Maandelijkse bronaudit.",
        f"Generated on: {audit['generated_on']}.",
        f"Live link check: {audit['live_link_check']}.",
        f"Watchlist items: {summary['watchlist_count']}.",
        f"Candidate sources: {summary['candidate_source_count']}.",
        f"Pending timeline items: {summary['pending_timeline_item_count']}.",
        f"Pending replacements: {summary['pending_replacement_count']}.",
        f"Live link issues: {summary['live_link_issue_count']}.",
        f"Live link review items: {summary['live_link_review_count']}.",
        "",
        f"Boundary: {audit['source_boundary']}",
        "",
        "## Expected Source Watchlist",
        "",
        "| Source | Status | Expected window | Intake rule | Link check |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in audit["watchlist"]:
        link = item["link_check"]
        lines.append(
            f"| {item['title']} | `{item['audit_status']}` | {item['expected_from']} to {item['expected_by']} | {item['intake_rule']} | {format_link_label(link)} |"
        )

    lines.extend(
        [
            "",
            "## Pending Replacements",
            "",
        ]
    )
    if audit["pending_replacements"]:
        for item in audit["pending_replacements"]:
            link = item["link_check"]
            note = item.get("note") or "No note"
            lines.append(f"- `{item['proposed_document_id']}`: {item['title']} ({format_link_label(link)}). {note}")
    else:
        lines.append("- No pending replacements.")

    lines.extend(
        [
            "",
            "## Pending Timeline Items",
            "",
        ]
    )
    if audit["pending_timeline_items"]:
        for item in audit["pending_timeline_items"]:
            lines.append(f"- {item['date_label']} - {item['subject']}: `{item['status']}`. {item['source_hint']}")
    else:
        lines.append("- No pending timeline items.")

    lines.extend(
        [
            "",
            "## Link Issues",
            "",
        ]
    )
    if audit["live_link_issues"]:
        for item in audit["live_link_issues"]:
            check = item["link_check"]
            item_id = item.get("proposed_document_id") or item.get("watch_id")
            title = item["title"]
            lines.append(f"- `{item_id}`: {title} returned `{check.get('status_code')}` / {check.get('error', 'no error detail')}.")
    else:
        lines.append("- No live link issues found, or live link check was not requested.")

    lines.extend(
        [
            "",
            "## Link Review Items",
            "",
        ]
    )
    if audit["live_link_review_items"]:
        for item in audit["live_link_review_items"]:
            check = item["link_check"]
            item_id = item.get("proposed_document_id") or item.get("watch_id")
            title = item["title"]
            lines.append(f"- `{item_id}`: {title} returned `{check.get('status_code')}` / {check.get('note', check.get('error', 'manual review needed'))}.")
    else:
        lines.append("- No live link review items found, or live link check was not requested.")

    lines.extend(
        [
            "",
            "## Use",
            "Use this audit as a monthly internal source-control note. Do not turn watchlist or pending items into claims, timeline facts or public text until formal intake and pipeline processing have happened.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", default=load_json(CONFIG_PATH)["as_of_date"])
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()

    audit = build_audit(parse_date(args.as_of), args.live)
    write_json(OUTPUT_JSON_PATH, audit)
    OUTPUT_MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD_PATH.write_text(render_markdown(audit), encoding="utf-8")
    print(f"Wrote {OUTPUT_JSON_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {OUTPUT_MD_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
