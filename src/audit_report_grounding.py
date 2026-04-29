from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "docs" / "rapporten" / "report-status.json"
OUTPUT_PATH = REPO_ROOT / "docs" / "internal" / "report-grounding-audit-2026-04-29.md"


INTERNAL_LAYER_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"\bdata/site\b",
        r"\bdata/extracted\b",
        r"\bsite_almere_view\.json\b",
        r"\balmere_current_view\.json\b",
        r"\bclaims_master\.jsonl\b",
        r"\bcurrent_interpretation\.json\b",
        r"\bqc_report\.json\b",
        r"\bAlmere-view\b",
        r"\bclaimlaag\b",
        r"\bpipeline\b",
        r"\bQC-rapportage\b",
        r"\bde dataset\b",
        r"\bde repository\b",
    ]
]

EXACT_FTE_PATTERN = re.compile(r"\b\d+,\d+\s*fte\b", re.IGNORECASE)
APPENDIX_PATTERN = re.compile(r"^\s*-\s*Bijlage\s+[A-Z]:", re.MULTILINE)
FINAL_INTERNAL_PLANNING_PATTERN = re.compile(
    r"\b(uiterlijk in Q[1-4] 2026|April-mei 2026|Mei-juni 2026|Juni-juli 2026|Q4 2026: vaststelling)\b",
    re.IGNORECASE,
)


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def current_public_reports() -> list[dict]:
    manifest = load_manifest()
    return [report for report in manifest["reports"] if report.get("public_facing_candidate")]


def line_number_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def find_pattern_issues(text: str, path: str, issue_type: str, patterns: list[re.Pattern[str]]) -> list[dict]:
    issues: list[dict] = []
    for pattern in patterns:
        for match in pattern.finditer(text):
            issues.append(
                {
                    "path": path,
                    "line": line_number_for_offset(text, match.start()),
                    "issue_type": issue_type,
                    "match": match.group(0),
                }
            )
    return issues


def audit_report(report: dict) -> dict:
    path = REPO_ROOT / report["path"]
    text = path.read_text(encoding="utf-8")
    issues: list[dict] = []
    issues.extend(find_pattern_issues(text, report["path"], "internal_datalayer_language", INTERNAL_LAYER_PATTERNS))
    issues.extend(find_pattern_issues(text, report["path"], "exact_fte_claim", [EXACT_FTE_PATTERN]))
    issues.extend(find_pattern_issues(text, report["path"], "appendix_list_requires_real_files", [APPENDIX_PATTERN]))
    issues.extend(find_pattern_issues(text, report["path"], "final_internal_planning_language", [FINAL_INTERNAL_PLANNING_PATTERN]))
    return {
        "path": report["path"],
        "title": report["title"],
        "status": report["status"],
        "issue_count": len(issues),
        "issues": issues,
    }


def build_audit() -> dict:
    reports = current_public_reports()
    report_results = [audit_report(report) for report in reports]
    issue_count = sum(result["issue_count"] for result in report_results)
    return {
        "generated_on": date.today().isoformat(),
        "manifest_path": str(MANIFEST_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "report_count": len(reports),
        "issue_count": issue_count,
        "reports": report_results,
        "superseded_reports": [
            report
            for report in load_manifest()["reports"]
            if not report.get("public_facing_candidate") and report["status"].startswith("superseded")
        ],
    }


def render_markdown(audit: dict) -> str:
    lines = [
        "# Report Grounding Audit",
        "",
        "## Summary",
        f"Current sprint: Sprint 30.3 - Beleidsdocumenten en rapporten.",
        f"Generated on: {audit['generated_on']}.",
        f"Manifest: `{audit['manifest_path']}`.",
        f"Public-review candidates checked: {audit['report_count']}.",
        f"Blocking report-grounding issues found: {audit['issue_count']}.",
        "",
        "This internal note checks current report candidates for internal datalayer language, exact FTE claims, appendix lists that require real files, and final-sounding internal planning language. Superseded drafts are tracked but not treated as public-review candidates.",
        "",
        "## Current Public-Review Candidates",
    ]
    for result in audit["reports"]:
        lines.extend(
            [
                "",
                f"### {result['title']}",
                f"Path: `{result['path']}`.",
                f"Status: `{result['status']}`.",
                f"Issues: {result['issue_count']}.",
            ]
        )
        if result["issues"]:
            for issue in result["issues"]:
                lines.append(
                    f"- Line {issue['line']}: `{issue['issue_type']}` matched `{issue['match']}`."
                )
        else:
            lines.append("- No blocking report-grounding issues found by this audit.")

    lines.extend(["", "## Superseded Drafts", ""])
    for report in audit["superseded_reports"]:
        lines.append(f"- `{report['path']}`: {report['notes']}")

    lines.extend(
        [
            "",
            "## Use",
            "Use this note as an internal control, not as public-facing report text. A clean audit does not prove policy correctness; it only checks that current report candidates avoid the main Sprint 30.3 anti-patterns.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    audit = build_audit()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(render_markdown(audit), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    if audit["issue_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
