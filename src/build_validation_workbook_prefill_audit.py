from __future__ import annotations

import json
import re
import zipfile
from datetime import date
from pathlib import Path
from typing import Any

try:
    from src.build_validation_workbook_traceability import (
        ROOT,
        WORKBOOKS,
        field_coverage,
        find_header_row,
        header_lookup,
        normalize,
        read_shared_strings,
        read_sheet_rows,
        sheet_summary,
        validation_rows,
        workbook_sheets,
    )
except ModuleNotFoundError:  # pragma: no cover - used when run as a script from /src
    from build_validation_workbook_traceability import (
        ROOT,
        WORKBOOKS,
        field_coverage,
        find_header_row,
        header_lookup,
        normalize,
        read_shared_strings,
        read_sheet_rows,
        sheet_summary,
        validation_rows,
        workbook_sheets,
    )


OUTPUT_JSON_PATH = ROOT / "data" / "workagenda" / "validation_workbook_prefill_audit.json"
OUTPUT_DOC_PATH = ROOT / "docs" / "review" / "validation-workbook-prefill-audit.md"

INTERNAL_LANGUAGE_PATTERNS = {
    "repository": r"\brepository\b",
    "register": r"\bregister\b",
    "prefill": r"\bprefill\b",
    "inferred": r"\binferred\b",
    "source_intake": r"\bsource[-_\s]?intake\b",
    "top_layer": r"\btop[-_\s]?layer\b|\btoplaag\b",
    "pipeline": r"\bpipeline\b",
    "json": r"\bjson\b",
    "claim_layer": r"\bclaim(?:laag| layer)?\b",
    "case_label": r"\bcase\s+[bc]\b",
}

NON_DUTCH_OR_TECHNICAL_TERMS = {
    "evidence": r"\bevidence\b",
    "social_base": r"\bsocial[-\s]?base\b",
}

BROAD_QUESTION_PATTERNS = {
    "generic_monitoring": r"wat volgen we om uitvoering, resultaten en effecten te beoordelen",
    "generic_owner": r"wie is verantwoordelijk eigenaar\??$",
}

ASSESSMENT_HEADERS = {
    "beoordeling werkvisie",
    "status lokale invulling",
    "validatiestatus",
    "selectie",
    "d6 relatie",
    "jgz classificatie",
    "taakclassificatie",
    "gebruik voor d6",
    "primaire rol",
    "rol almere",
    "controller bevestigd?",
    "lokale validatiestatus",
    "monitoringstatus",
    "afhankelijkheidsstatus",
}

CORRECTION_HEADERS = {
    "toelichting correctie",
    "toelichting",
    "correctie",
}


def all_sheet_text(rows: list[dict[str, object]]) -> str:
    chunks: list[str] = []
    for row in rows:
        values = row["values"]
        assert isinstance(values, dict)
        chunks.extend(str(value) for value in values.values() if value)
    return "\n".join(chunks)


def matching_patterns(text: str, patterns: dict[str, str]) -> list[str]:
    return [
        label
        for label, pattern in patterns.items()
        if re.search(pattern, text, flags=re.IGNORECASE)
    ]


def first_current_view(rows: list[dict[str, object]], headers: dict[int, str], summary: str) -> str:
    if summary:
        return summary.strip()
    normalized_to_index = {normalize(header): idx for idx, header in headers.items()}
    idx = normalized_to_index.get("huidige werkhypothese") or normalized_to_index.get("huidige werkvisie")
    if idx is None:
        return ""
    examples: list[str] = []
    for row in rows:
        values = row["values"]
        assert isinstance(values, dict)
        value = values.get(idx, "")
        if value:
            examples.append(value)
        if len(examples) >= 2:
            break
    return " / ".join(examples)


def clarify_regional_actor_shorthand(text: str) -> str:
    text = re.sub(
        r"of\s+Almere\s*/\s*Flevoland\s+een",
        "of er voor gemeente Almere en de relevante Flevoland-schaal een",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"of\s+Flevoland\s*/\s*Almere\s+een",
        "of er voor de relevante Flevoland-schaal en gemeente Almere een",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"\bAlmere\s*/\s*Flevoland\b",
        "gemeente Almere en de relevante Flevoland-schaal",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"\bFlevoland\s*/\s*Almere\b",
        "de relevante Flevoland-schaal en gemeente Almere",
        text,
        flags=re.IGNORECASE,
    )
    return text.replace("een route of plan heeft", "een route of plan is")


def normalized_headers(headers: dict[int, str]) -> set[str]:
    return {normalize(header) for header in headers.values()}


def has_assessment_field(headers: dict[int, str]) -> bool:
    return bool(normalized_headers(headers) & ASSESSMENT_HEADERS)


def has_correction_field(headers: dict[int, str]) -> bool:
    normalized = normalized_headers(headers)
    return any(any(marker in header for marker in CORRECTION_HEADERS) for header in normalized)


def question_findings(mapped_rows: list[dict[str, object]]) -> dict[str, Any]:
    blank_questions = [
        row["vraag_id"]
        for row in mapped_rows
        if not str(row.get("question_text", "")).strip()
    ]
    broad_questions = []
    for row in mapped_rows:
        text = str(row.get("question_text", ""))
        labels = matching_patterns(text, BROAD_QUESTION_PATTERNS)
        if labels:
            broad_questions.append(
                {
                    "vraag_id": row["vraag_id"],
                    "question_text": text,
                    "reason": labels,
                }
            )
    return {
        "blank_question_ids": blank_questions,
        "broad_question_flags": broad_questions,
    }


def sheet_recommendations(
    coverage: dict[str, bool],
    assessment: bool,
    correction: bool,
    jargon: list[str],
    non_dutch_terms: list[str],
    question_audit: dict[str, Any],
) -> list[str]:
    recommendations: list[str] = []
    if not coverage["current_working_view"]:
        recommendations.append("Add a concise current working view before stakeholder contact.")
    if not assessment:
        recommendations.append("Add or clarify a field for confirming/correcting the current working view.")
    if not correction:
        recommendations.append("Add or clarify a short correction/toelichting field.")
    if not coverage["evidence_reference"]:
        recommendations.append("Add an evidence type or evidence reference field.")
    if jargon:
        recommendations.append("Replace internal repository/data terms in human-facing text.")
    if non_dutch_terms:
        recommendations.append("Replace English/technical terms with plain Dutch policy language.")
    if question_audit["blank_question_ids"]:
        recommendations.append("Fill blank question text before packet export.")
    if question_audit["broad_question_flags"]:
        recommendations.append("Narrow broad monitoring/owner questions before packet export.")
    return recommendations


def build_audit() -> dict[str, Any]:
    workbook_entries: list[dict[str, Any]] = []
    all_sheet_entries: list[dict[str, Any]] = []
    for workbook in WORKBOOKS:
        with zipfile.ZipFile(workbook.path) as archive:
            shared_strings = read_shared_strings(archive)
            sheets = workbook_sheets(archive)
            sheet_entries: list[dict[str, Any]] = []
            for sheet_name, sheet_config in workbook.sheets.items():
                rows = read_sheet_rows(archive, sheets[sheet_name], shared_strings)
                header_row = find_header_row(rows)
                headers = header_lookup(header_row)
                summary = sheet_summary(rows, header_row)
                coverage = field_coverage(headers, summary)
                mapped_rows = validation_rows(rows, header_row, headers, sheet_config)
                text = all_sheet_text(rows)
                jargon = matching_patterns(text, INTERNAL_LANGUAGE_PATTERNS)
                non_dutch_terms = matching_patterns(text, NON_DUTCH_OR_TECHNICAL_TERMS)
                assessment = has_assessment_field(headers)
                correction = has_correction_field(headers)
                question_audit = question_findings(mapped_rows)
                current_view = clarify_regional_actor_shorthand(first_current_view(rows, headers, summary))
                entry = {
                    "sheet": sheet_name,
                    "component_id": sheet_config.component_id,
                    "mapped_validation_row_count": len(mapped_rows),
                    "has_current_working_view": coverage["current_working_view"],
                    "has_assessment_field": assessment,
                    "has_correction_field": correction,
                    "has_evidence_field": coverage["evidence_reference"],
                    "internal_jargon_flags": jargon,
                    "plain_language_flags": non_dutch_terms,
                    "blank_question_count": len(question_audit["blank_question_ids"]),
                    "broad_question_count": len(question_audit["broad_question_flags"]),
                    "broad_question_flags": question_audit["broad_question_flags"],
                    "current_view_sample": current_view[:500],
                    "recommendations": sheet_recommendations(
                        coverage,
                        assessment,
                        correction,
                        jargon,
                        non_dutch_terms,
                        question_audit,
                    ),
                }
                sheet_entries.append(entry)
                all_sheet_entries.append({"workbook_id": workbook.workbook_id, **entry})
        workbook_entries.append(
            {
                "workbook_id": workbook.workbook_id,
                "path": str(workbook.path.relative_to(ROOT)).replace("\\", "/"),
                "validation_domain": workbook.validation_domain,
                "sheet_count": len(sheet_entries),
                "mapped_validation_row_count": sum(
                    sheet["mapped_validation_row_count"] for sheet in sheet_entries
                ),
                "sheets_missing_current_working_view": [
                    sheet["sheet"] for sheet in sheet_entries if not sheet["has_current_working_view"]
                ],
                "sheets_missing_assessment_field": [
                    sheet["sheet"] for sheet in sheet_entries if not sheet["has_assessment_field"]
                ],
                "sheets_missing_correction_field": [
                    sheet["sheet"] for sheet in sheet_entries if not sheet["has_correction_field"]
                ],
                "sheets_missing_evidence_field": [
                    sheet["sheet"] for sheet in sheet_entries if not sheet["has_evidence_field"]
                ],
                "sheets_with_language_flags": [
                    sheet["sheet"]
                    for sheet in sheet_entries
                    if sheet["internal_jargon_flags"] or sheet["plain_language_flags"]
                ],
                "sheets_with_broad_questions": [
                    sheet["sheet"] for sheet in sheet_entries if sheet["broad_question_count"]
                ],
                "sheets": sheet_entries,
            }
        )
    return {
        "generated_on": date.today().isoformat(),
        "current_sprint": "Sprint 33.P2 - Pre-contact validation-readiness: prefill audit and current working views",
        "purpose": "Audit human-facing current working views, evidence instructions, correction fields and jargon in D5/D6 validation workbooks before stakeholder contact.",
        "guardrail": "This audit is a QA layer. It does not validate policy content or turn workbook text into source evidence.",
        "summary": {
            "sheet_count": len(all_sheet_entries),
            "mapped_validation_row_count": sum(
                sheet["mapped_validation_row_count"] for sheet in all_sheet_entries
            ),
            "sheets_missing_current_working_view": [
                sheet for sheet in all_sheet_entries if not sheet["has_current_working_view"]
            ],
            "sheets_missing_assessment_field": [
                sheet for sheet in all_sheet_entries if not sheet["has_assessment_field"]
            ],
            "sheets_missing_correction_field": [
                sheet for sheet in all_sheet_entries if not sheet["has_correction_field"]
            ],
            "sheets_missing_evidence_field": [
                sheet for sheet in all_sheet_entries if not sheet["has_evidence_field"]
            ],
            "sheets_with_language_flags": [
                sheet
                for sheet in all_sheet_entries
                if sheet["internal_jargon_flags"] or sheet["plain_language_flags"]
            ],
            "sheets_with_broad_questions": [
                sheet for sheet in all_sheet_entries if sheet["broad_question_count"]
            ],
        },
        "workbooks": workbook_entries,
    }


def status_label(sheet: dict[str, Any]) -> str:
    if sheet["recommendations"]:
        return "needs cleanup"
    return "ok"


def render_markdown(audit: dict[str, Any]) -> str:
    summary = audit["summary"]
    lines = [
        "# Validation Workbook Prefill Audit",
        "",
        "## Summary",
        "Sprint covered: Sprint 33.P2 - Pre-contact validation-readiness: prefill audit and current working views.",
        "",
        f"Generated on: {audit['generated_on']}.",
        "",
        "This audit checks whether the D5 and D6 validation workbooks are understandable before stakeholder contact. It checks current working views, answer/correction fields, evidence fields, broad questions and internal jargon. It does not validate the policy content.",
        "",
        "## Bottom Line",
        "",
        "The workbooks are usable as pre-contact drafts, but they still need packet cleanup before sending. D5 is stronger on row-level current working hypotheses and validation/evidence fields. D6 is stronger on short safe/unsafe wording blocks. The remaining work is to make those strengths consistent in the exported stakeholder packets.",
        "",
        "## Headline Counts",
        "",
        "| Check | Count |",
        "| --- | ---: |",
        f"| Human-facing sheets audited | {summary['sheet_count']} |",
        f"| Validation rows covered by traceability map | {summary['mapped_validation_row_count']} |",
        f"| Sheets missing a current working view | {len(summary['sheets_missing_current_working_view'])} |",
        f"| Sheets missing an assessment/selection field | {len(summary['sheets_missing_assessment_field'])} |",
        f"| Sheets missing a correction/toelichting field | {len(summary['sheets_missing_correction_field'])} |",
        f"| Sheets missing an evidence field | {len(summary['sheets_missing_evidence_field'])} |",
        f"| Sheets with language cleanup flags | {len(summary['sheets_with_language_flags'])} |",
        f"| Sheets with broad-question flags | {len(summary['sheets_with_broad_questions'])} |",
        "",
        "## Workbook Findings",
        "",
    ]
    for workbook in audit["workbooks"]:
        lines.extend(
            [
                f"### {workbook['validation_domain']} Workbook",
                "",
                f"Path: `{workbook['path']}`",
                "",
                "| Sheet | Status | Main cleanup need |",
                "| --- | --- | --- |",
            ]
        )
        for sheet in workbook["sheets"]:
            cleanup = "; ".join(sheet["recommendations"]) if sheet["recommendations"] else "No immediate prefill cleanup flagged."
            lines.append(f"| {sheet['sheet']} | {status_label(sheet)} | {cleanup} |")
        lines.append("")

    lines.extend(
        [
            "## Cross-workbook Findings",
            "",
            "- The workbooks already avoid the biggest anti-pattern: they do not ask stakeholders to start from a blank sheet.",
            "- D5 component sheets usually contain row-level `Huidige werkhypothese`, status, correction and evidence columns.",
            "- D6 component sheets usually contain concise current working view, safe wording and unsafe wording blocks.",
            "- Some D5 matrix tabs are operational control sheets rather than stakeholder-friendly tabs; they need current-view or instruction cleanup before packet export.",
            "- Some D6 text still uses English or technical wording such as `evidence` or `social-base`; replace this with plain Dutch in outgoing packets.",
            "- Monitoring rows still contain generic prompts that should be narrowed before sending to busy stakeholders.",
            "",
            "## Required Before Sending",
            "",
            "- Keep generated `vraag_id` values from the traceability map in outgoing packets.",
            "- Add or preserve a concise current working view for each exported tab.",
            "- Add a clear confirm/correct choice where the current workbook only has open text.",
            "- Keep evidence fields visible in every packet.",
            "- Replace internal or English technical terms in stakeholder-facing text.",
            "- Narrow broad monitoring questions into concrete validation choices where possible.",
            "",
            "## Next Step",
            "",
            "Sprint 33.P3 should prepare targeted pre-contact agents. Use agents only for evidence-prefill audit, policymaker readability, D5-D6 dependency mapping, finance-risk precheck and the end-May handreiking watchlist. Do not start broad D5 or D6 research.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    audit = build_audit()
    OUTPUT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON_PATH.write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    OUTPUT_DOC_PATH.write_text(render_markdown(audit), encoding="utf-8")
    print(f"Wrote {OUTPUT_JSON_PATH.relative_to(ROOT)}")
    print(f"Wrote {OUTPUT_DOC_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
