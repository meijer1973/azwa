from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKET_INDEX_PATH = ROOT / "data" / "workagenda" / "precontact_stakeholder_packets.json"
OUTPUT_JSON_PATH = ROOT / "data" / "workagenda" / "precontact_internal_dry_run.json"
OUTPUT_DOC_PATH = ROOT / "docs" / "review" / "precontact-internal-dry-run.md"

REQUIRED_CSV_FIELDS = {
    "vraag_id",
    "answer",
    "evidence_type",
    "evidence_reference",
    "correction_or_note",
    "not_my_domain_reroute",
}

CASE_DEFINITIONS = [
    {
        "case_id": "P5-CASE-001",
        "case_type": "d5_tab_answerability",
        "packet_id": "welzijn_sociale_basis",
        "vraag_id": "D5-SV-001",
        "reviewer_role": "policy_or_subject_reviewer",
        "instruction": "Test whether a busy social-base reviewer can answer a D5 sociaal-verwijzen row without opening the full workbook.",
        "expected_processing_route": "validation_log_or_decision_ticket",
    },
    {
        "case_id": "P5-CASE-002",
        "case_type": "d6_tab_answerability",
        "packet_id": "wijkteams_slt_leads",
        "vraag_id": "D6-WIJK-001",
        "reviewer_role": "subject_reviewer",
        "instruction": "Test whether a Wijkteams/SLT reviewer can classify the D6 relation from the packet row and evidence fields.",
        "expected_processing_route": "d6_validation_log_or_register_update",
    },
    {
        "case_id": "P5-CASE-003",
        "case_type": "finance_row",
        "packet_id": "finance_controller",
        "vraag_id": "D5-NNZ-004",
        "reviewer_role": "finance_reviewer",
        "instruction": "Test whether finance can evaluate a component-level budget question now that the separate D5 finance tab has been removed.",
        "expected_processing_route": "validation_log_or_finance_ticket",
    },
    {
        "case_id": "P5-CASE-004",
        "case_type": "evidence_field",
        "packet_id": "gemeente_almere_sociaal_domein_d6",
        "vraag_id": "D6-SLT-001",
        "reviewer_role": "policy_reviewer",
        "instruction": "Test whether a formal-decision interpretation can be answered only with an explicit evidence type and reference.",
        "expected_processing_route": "d6_validation_log_or_decision_ticket",
    },
    {
        "case_id": "P5-CASE-005",
        "case_type": "not_my_domain_reroute",
        "packet_id": "zorgverzekeraar_zvw",
        "vraag_id": "D5-SV-001",
        "reviewer_role": "data_repository_reviewer",
        "instruction": "Test whether a reviewer can mark a row as not-my-domain and route it to the better owner without losing vraag_id traceability.",
        "expected_processing_route": "reroute_or_validation_log_note",
        "expected_reroute_candidates": [
            "welzijn_sociale_basis",
            "gemeente_almere_sociaal_domein_d5",
        ],
    },
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def packet_by_id(packet_index: dict[str, Any], packet_id: str) -> dict[str, Any]:
    for packet in packet_index["packets"]:
        if packet["packet_id"] == packet_id:
            return packet
    raise KeyError(packet_id)


def row_by_id(packet: dict[str, Any], vraag_id: str) -> dict[str, Any]:
    for row in packet["rows"]:
        if row["vraag_id"] == vraag_id:
            return row
    raise KeyError(f"{packet['packet_id']}::{vraag_id}")


def csv_headers(path: str) -> set[str]:
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as handle:
        return set(next(csv.reader(handle)))


def build_dry_run() -> dict[str, Any]:
    packet_index = load_json(PACKET_INDEX_PATH)
    cases: list[dict[str, Any]] = []

    for definition in CASE_DEFINITIONS:
        packet = packet_by_id(packet_index, definition["packet_id"])
        row = row_by_id(packet, definition["vraag_id"])
        headers = csv_headers(packet["csv_path"])
        cases.append(
            {
                **definition,
                "packet_label": packet["label"],
                "packet_csv_path": packet["csv_path"],
                "workbook_path": row["workbook_path"],
                "human_entry_surface": "excel_workbook",
                "repository_traceability_surface": "csv_packet_reference",
                "csv_fields_present": sorted(headers & REQUIRED_CSV_FIELDS),
                "missing_required_csv_fields": sorted(REQUIRED_CSV_FIELDS - headers),
                "domain": row["domain"],
                "workbook_id": row["workbook_id"],
                "sheet": row["sheet"],
                "sheet_row": row["sheet_row"],
                "component_id": row["component_id"],
                "question_text": row["question_text"],
                "antwoordtype": row["antwoordtype"],
                "repo_update_effect": row["repo_update_effect"],
                "bewijstype_verplicht": row["bewijstype_verplicht"],
                "pass_criteria": [
                    "Reviewer can find the indicated workbook sheet and row without repository help.",
                    "Reviewer can understand what is being asked in the Excel workbook.",
                    "Reviewer can choose an answer, mark unknown, or mark not-my-domain.",
                    "Reviewer can name evidence type and evidence reference when claiming confirmation.",
                    "Repository reviewer can map the Excel answer back to vraag_id and packet_id using the dry-run case reference.",
                    "Repository team can route the answer to the expected processing route.",
                ],
                "failure_triggers": [
                    "Question requires a broad explanation instead of a choice or short correction.",
                    "Reviewer cannot tell whether evidence is required.",
                    "Reviewer needs raw CSV or repository JSON to answer the human-facing question.",
                    "Not-my-domain answer has no clear reroute target.",
                    "Answer would silently become a source claim instead of a validation record.",
                ],
            }
        )

    automated_checks = [
        {
            "check_id": "P5-AUTO-001",
            "check": "Packet index loads and contains prepared packets.",
            "status": "pass" if packet_index["packet_count"] >= 15 else "fail",
        },
        {
            "check_id": "P5-AUTO-002",
            "check": "All packet drafts remain prepared_not_sent.",
            "status": "pass"
            if packet_index["dispatch_status"] == "prepared_not_sent"
            and all(packet["dispatch_status"] == "prepared_not_sent" for packet in packet_index["packets"])
            else "fail",
        },
        {
            "check_id": "P5-AUTO-003",
            "check": "Required dry-run cases are resolvable to exact packet rows.",
            "status": "pass" if len(cases) == len(CASE_DEFINITIONS) else "fail",
        },
        {
            "check_id": "P5-AUTO-004",
            "check": "Dry-run CSVs expose answer, evidence and not-my-domain fields.",
            "status": "pass"
            if all(not case["missing_required_csv_fields"] for case in cases)
            else "fail",
        },
        {
            "check_id": "P5-AUTO-005",
            "check": "Packet sizes remain reviewable.",
            "status": "pass" if max(packet["row_count"] for packet in packet_index["packets"]) <= 80 else "fail",
        },
    ]

    return {
        "generated_on": date.today().isoformat(),
        "current_sprint": "Sprint 33.P5 - Pre-contact validation-readiness: internal dry run",
        "repository_check_status": "completed",
        "human_dry_run_status": "pending_internal_reviewers",
        "gate_effect": "Blocks P7 send-readiness until human reviewers complete the cases; does not block P6 workflow integration.",
        "source_inputs": [str(PACKET_INDEX_PATH.relative_to(ROOT)).replace("\\", "/")],
        "reviewer_roles": [
            {
                "role": "policy_reviewer",
                "tests": "Plain-language policy meaning, safe wording and decision-risk clarity.",
            },
            {
                "role": "finance_reviewer",
                "tests": "Funding-line, structural/project and double-counting questions.",
            },
            {
                "role": "data_repository_reviewer",
                "tests": "Vraag_id preservation, answer-processing route and not-my-domain rerouting.",
            },
            {
                "role": "subject_reviewer",
                "tests": "Whether a domain expert can answer from the filtered packet alone.",
            },
        ],
        "automated_checks": automated_checks,
        "cases": cases,
        "human_completion_required": [
            "Select 2-4 internal reviewers before stakeholder contact.",
            "Have them complete the five dry-run cases in the human-facing Excel workbooks, using workbook path, sheet and row from this note.",
            "For D5 cases, test the owner/party/action-holder dropdowns and report whether an expected owner option is missing.",
            "Use CSV packet paths only as repository traceability/export references, not as the normal human entry surface.",
            "Record time-to-answer, confusing wording, missing dropdown options, evidence ambiguity and reroute clarity.",
            "Apply workbook or packet fixes before the P7 send-readiness gate.",
        ],
    }


def render_markdown(dry_run: dict[str, Any]) -> str:
    lines = [
        "# Pre-contact Internal Dry Run",
        "",
        "## Summary",
        f"Current sprint: {dry_run['current_sprint']}.",
        "",
        f"Generated on: {dry_run['generated_on']}.",
        "",
        "This file defines the internal dry-run cases for the prepared D5/D6 stakeholder packets. It is not a stakeholder validation record and it does not authorize contact with policymakers.",
        "",
        "Human reviewers should work in the Excel validation workbooks, not in raw CSV files. The CSV packet paths below are repository traceability references: they help the repository team verify that returned answers can be mapped back to `vraag_id`, packet routing and processing targets.",
        "",
        f"Repository check status: `{dry_run['repository_check_status']}`.",
        "",
        f"Human dry-run status: `{dry_run['human_dry_run_status']}`.",
        "",
        f"Gate effect: {dry_run['gate_effect']}",
        "",
        "## Automated Checks",
        "",
        "| Check | Status |",
        "| --- | --- |",
    ]
    for check in dry_run["automated_checks"]:
        lines.append(f"| {check['check']} | `{check['status']}` |")

    lines.extend(
        [
            "",
            "## Reviewer Roles",
            "",
            "| Role | What to test |",
            "| --- | --- |",
        ]
    )
    for role in dry_run["reviewer_roles"]:
        lines.append(f"| `{role['role']}` | {role['tests']} |")

    lines.extend(
        [
            "",
            "## What The Human Reviewer Should Do",
            "",
            "1. Open the workbook named in the case detail.",
            "2. Go to the listed sheet and row.",
            "3. Answer only that row using the workbook's dropdowns, short note fields and evidence fields. For D5 owner, party or action-holder fields, choose from the dropdown where possible and use `Anders, toelichten` only when the list is missing the right option.",
            "4. If the row is outside the reviewer's domain, choose or write `niet mijn domein` and name the better owner if known.",
            "5. Record whether the row was easy to understand, what evidence would be attached, and whether any dropdown option was missing.",
            "6. Do not use the CSV as the human form. The repository team uses the CSV path only to check traceability and export shape.",
            "",
            "The dry run tests usability and processability. It is not asking reviewers to validate all D5/D6 content and it does not create stakeholder evidence.",
            "",
            "## Dry-run Cases",
            "",
            "| Case | Packet | Vraag ID | Test | Expected route |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for case in dry_run["cases"]:
        lines.append(
            f"| `{case['case_id']}` | `{case['packet_id']}` | `{case['vraag_id']}` | {case['instruction']} | `{case['expected_processing_route']}` |"
        )

    lines.extend(["", "## Case Details", ""])
    for case in dry_run["cases"]:
        answer_instruction = (
            "- Use the workbook dropdowns and evidence fields to answer just this row. Check whether owner/party/action-holder dropdowns are sufficient."
            if case["domain"] == "D5"
            else "- Use the workbook dropdowns and evidence fields to answer just this row."
        )
        lines.extend(
            [
                f"### {case['case_id']} - {case['case_type']}",
                "",
                f"Packet: `{case['packet_id']}` ({case['packet_label']})",
                "",
                f"Human workbook: `{case['workbook_path']}`",
                "",
                f"Repository CSV reference: `{case['packet_csv_path']}`",
                "",
                f"Vraag ID: `{case['vraag_id']}`",
                "",
                f"Sheet: `{case['sheet']}` row `{case['sheet_row']}`",
                "",
                f"Question: {case['question_text']}",
                "",
                f"Reviewer role: `{case['reviewer_role']}`",
                "",
                f"Expected processing route: `{case['expected_processing_route']}`",
                "",
                "What the reviewer does:",
                "",
                f"- Open `{case['workbook_path']}`.",
                f"- Go to sheet `{case['sheet']}`, row `{case['sheet_row']}`.",
                answer_instruction,
                "- Note whether wording, answer options or evidence instructions need improvement before stakeholder contact.",
                "",
                "Pass criteria:",
                "",
            ]
        )
        lines.extend(f"- {item}" for item in case["pass_criteria"])
        lines.extend(["", "Failure triggers:", ""])
        lines.extend(f"- {item}" for item in case["failure_triggers"])
        if case.get("expected_reroute_candidates"):
            lines.extend(["", "Expected reroute candidates:", ""])
            lines.extend(f"- `{item}`" for item in case["expected_reroute_candidates"])
        lines.append("")

    lines.extend(
        [
            "## Human Completion Required",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in dry_run["human_completion_required"])
    lines.extend(
        [
            "",
            "## Next Step",
            "",
            "Sprint 33.P6 can proceed with repository/workflow integration while this human dry run is pending. Sprint 33.P7 send-readiness remains blocked until internal reviewers complete these cases and any required packet fixes are made.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    dry_run = build_dry_run()
    OUTPUT_JSON_PATH.write_text(
        json.dumps(dry_run, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    OUTPUT_DOC_PATH.write_text(render_markdown(dry_run), encoding="utf-8")
    print(f"Wrote {OUTPUT_JSON_PATH.relative_to(ROOT)}")
    print(f"Wrote {OUTPUT_DOC_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
