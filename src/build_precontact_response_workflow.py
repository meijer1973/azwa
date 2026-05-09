from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKET_INDEX_PATH = ROOT / "data" / "workagenda" / "precontact_stakeholder_packets.json"
DRY_RUN_PATH = ROOT / "data" / "workagenda" / "precontact_internal_dry_run.json"
OUTPUT_JSON_PATH = ROOT / "data" / "workagenda" / "precontact_response_workflow.json"
OUTPUT_DOC_PATH = ROOT / "docs" / "review" / "precontact-response-workflow.md"

REQUIRED_RETURN_FIELDS = [
    "vraag_id",
    "stakeholderpakket",
    "answer",
    "evidence_type",
    "evidence_reference",
    "correction_or_note",
    "not_my_domain_reroute",
]

TARGET_ARTIFACTS: dict[str, dict[str, str]] = {
    "d5_validation_log": {
        "path": "data/workagenda/d5_validation_log.json",
        "status": "planned_no_answers_yet",
        "purpose": "D5 stakeholder confirmations, corrections, weak confirmations, unknowns and conflicts.",
    },
    "d6_validation_log": {
        "path": "data/workagenda/d6_validation_log.json",
        "status": "planned_no_answers_yet",
        "purpose": "D6 stakeholder confirmations, corrections, weak confirmations, unknowns and conflicts.",
    },
    "d5_finance_matrix": {
        "path": "data/workagenda/d5_finance_matrix.json",
        "status": "planned_no_answers_yet",
        "purpose": "D5 funding line, structural/project status, double-counting risk and controller/Zvw confirmation.",
    },
    "d6_finance_matrix": {
        "path": "data/workagenda/d6_finance_matrix.json",
        "status": "planned_no_answers_yet",
        "purpose": "D6 funding line, structural/project status, double-counting risk and controller confirmation.",
    },
    "d5_decision_register": {
        "path": "data/workagenda/d5_decision_register.json",
        "status": "planned_no_answers_yet",
        "purpose": "D5 policy, governance, phasing and workagenda decision tickets.",
    },
    "d6_decision_register": {
        "path": "data/workagenda/d6_decision_register.json",
        "status": "planned_no_answers_yet",
        "purpose": "D6 classification, mandate, owner, funding and safe-wording decision tickets.",
    },
    "d5_d6_dependency_map": {
        "path": "data/workagenda/d5_d6_dependency_map.json",
        "status": "planned_no_answers_yet",
        "purpose": "D6 preconditions and blockers per D5 component.",
    },
    "d5_status_matrix": {
        "path": "data/workagenda/d5_status_matrix.json",
        "status": "existing_update_target",
        "purpose": "D5 delivery status per component and workagenda field.",
    },
    "d6_responsibility_register": {
        "path": "data/extracted/municipal/almere_d6_responsibility_register.json",
        "status": "existing_update_target_after_validation_only",
        "purpose": "D6 responsibility register; no row may become settled without direct evidence.",
    },
    "source_update_log": {
        "path": "data/workagenda/d5_source_update_log.json",
        "status": "planned_no_answers_yet",
        "purpose": "New public sources named by stakeholders, handreiking updates and source-intake follow-up.",
    },
    "ict_privacy_register": {
        "path": "data/workagenda/ict_privacy_decision_register.json",
        "status": "planned_no_answers_yet",
        "purpose": "ICT/privacy/data-accountability issues that cannot be resolved from the validation packet answer alone.",
    },
}

ROUTE_DEFINITIONS: dict[str, dict[str, Any]] = {
    "validation_log_or_decision_ticket": {
        "primary_targets": ["d5_validation_log"],
        "conditional_targets": ["d5_decision_register", "source_update_log"],
        "status_update_target": "d5_status_matrix",
    },
    "validation_log_or_finance_ticket": {
        "primary_targets": ["d5_validation_log"],
        "conditional_targets": ["d5_finance_matrix", "d5_decision_register", "source_update_log"],
        "status_update_target": "d5_status_matrix",
    },
    "decision_register_or_validation_log": {
        "primary_targets": ["d5_decision_register", "d5_validation_log"],
        "conditional_targets": ["source_update_log"],
        "status_update_target": "d5_status_matrix",
    },
    "finance_matrix_update": {
        "primary_targets": ["d5_finance_matrix"],
        "conditional_targets": ["d5_validation_log", "d5_decision_register", "source_update_log"],
        "status_update_target": "d5_status_matrix",
    },
    "status_matrix_update": {
        "primary_targets": ["d5_status_matrix", "d5_validation_log"],
        "conditional_targets": ["source_update_log"],
        "status_update_target": "d5_status_matrix",
    },
    "decision_ticket_or_status_matrix_update": {
        "primary_targets": ["d5_decision_register", "d5_status_matrix"],
        "conditional_targets": ["d5_validation_log", "source_update_log"],
        "status_update_target": "d5_status_matrix",
    },
    "validation_log_or_ict_privacy_ticket": {
        "primary_targets": ["d5_validation_log"],
        "conditional_targets": ["ict_privacy_register", "source_update_log"],
        "status_update_target": "d5_status_matrix",
    },
    "d5_d6_dependency_map_update": {
        "primary_targets": ["d5_d6_dependency_map"],
        "conditional_targets": ["d5_validation_log", "d6_validation_log", "d6_decision_register"],
        "status_update_target": "d5_status_matrix",
    },
    "d6_validation_log_or_decision_ticket": {
        "primary_targets": ["d6_validation_log"],
        "conditional_targets": ["d6_decision_register", "source_update_log"],
        "status_update_target": "d6_responsibility_register",
    },
    "d6_validation_log_or_register_update": {
        "primary_targets": ["d6_validation_log"],
        "conditional_targets": ["d6_responsibility_register", "d6_decision_register", "source_update_log"],
        "status_update_target": "d6_responsibility_register",
    },
    "d6_validation_log_or_ict_privacy_ticket": {
        "primary_targets": ["d6_validation_log"],
        "conditional_targets": ["ict_privacy_register", "d6_decision_register", "source_update_log"],
        "status_update_target": "d6_responsibility_register",
    },
    "d6_finance_matrix_or_decision_ticket": {
        "primary_targets": ["d6_finance_matrix"],
        "conditional_targets": ["d6_validation_log", "d6_decision_register", "source_update_log"],
        "status_update_target": "d6_responsibility_register",
    },
}

ANSWER_OUTCOME_RULES = [
    {
        "outcome": "confirmed_with_evidence",
        "processing": "First classify the evidence. If a high-quality public source is named, ingest and verify it through top layers before treating it as source-backed. If the evidence is a stakeholder/internal confirmation, record it as validation evidence and update only the directly supported field.",
        "may_update_status": True,
    },
    {
        "outcome": "confirmed_without_evidence",
        "processing": "Record as low-authority human confirmation; do not mark ready, confirmed or settled.",
        "may_update_status": False,
    },
    {
        "outcome": "partly_correct",
        "processing": "Update the working view and keep review_needed until the correction and evidence are clear.",
        "may_update_status": False,
    },
    {
        "outcome": "incorrect",
        "processing": "Correct the working view, keep review_needed and create a decision ticket if a policy choice is needed.",
        "may_update_status": False,
    },
    {
        "outcome": "not_my_domain",
        "processing": "Do not treat as substantive validation; reroute using not_my_domain_reroute and keep the original vraag_id.",
        "may_update_status": False,
    },
    {
        "outcome": "unknown",
        "processing": "Keep unresolved and preserve the open question.",
        "may_update_status": False,
    },
    {
        "outcome": "conflict",
        "processing": "Escalate to review_needed or decision register; do not force a conclusion.",
        "may_update_status": False,
    },
    {
        "outcome": "decision_needed",
        "processing": "Create or update a decision ticket with owner, options, deadline and evidence after decision.",
        "may_update_status": False,
    },
    {
        "outcome": "finance_needed",
        "processing": "Route to finance matrix or finance/controller ticket; no funding wording becomes confirmed.",
        "may_update_status": False,
    },
    {
        "outcome": "ict_privacy_needed",
        "processing": "Route to ICT/privacy register; no data-accountability wording becomes confirmed.",
        "may_update_status": False,
    },
    {
        "outcome": "public_source_found",
        "processing": "Add the public source to source intake first; ingest, run pipeline and verify top layers before using as source evidence.",
        "may_update_status": False,
    },
]

AUTHORITY_LEVELS = [
    {
        "level": "source_ingested_and_top_layer_verified",
        "authority": "high",
        "meaning": "A credible public source has been added to the source corpus, processed by the pipeline and verified in the relevant top data layer.",
        "allowed_effect": "May support source-backed updates when the source directly answers the field.",
    },
    {
        "level": "formal_decision_or_controller_confirmation",
        "authority": "high_for_validation",
        "meaning": "A formal local/regional decision, budget line, controller confirmation or internal mandate document is named or attached.",
        "allowed_effect": "May support validation, finance or decision-register updates; it is not a public corpus source unless separately ingested as a public source.",
    },
    {
        "level": "stakeholder_confirmation_with_evidence_reference",
        "authority": "medium_for_validation",
        "meaning": "A stakeholder answer names a role, document, decision or evidence path but the evidence has not yet been independently processed.",
        "allowed_effect": "Record in validation log; update only cautiously and keep evidence follow-up open where needed.",
    },
    {
        "level": "human_input_without_source_backup",
        "authority": "low",
        "meaning": "A human answer provides a conclusion but no credible source, document, decision, budget line or evidence path.",
        "allowed_effect": "Record as low-authority confirmation only; do not mark ready, confirmed, source-backed or settled.",
    },
    {
        "level": "new_public_source_named_not_ingested",
        "authority": "candidate",
        "meaning": "A reviewer names a potentially useful public source that is not yet in the corpus.",
        "allowed_effect": "Add to source-update/source-intake queue first; no substantive status change until ingestion and top-layer verification.",
    },
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_route_counts(packet_index: dict[str, Any]) -> tuple[Counter[str], Counter[str]]:
    packet_row_counts: Counter[str] = Counter()
    unique_row_counts: Counter[str] = Counter()
    seen: set[tuple[str, str, str]] = set()
    for packet in packet_index["packets"]:
        for row in packet["rows"]:
            route = row["repo_update_effect"]
            packet_row_counts[route] += 1
            unique_key = (row["workbook_id"], row["vraag_id"], route)
            if unique_key not in seen:
                unique_row_counts[route] += 1
                seen.add(unique_key)
    return packet_row_counts, unique_row_counts


def route_coverage(packet_index: dict[str, Any]) -> list[dict[str, Any]]:
    packet_counts, unique_counts = collect_route_counts(packet_index)
    coverage = []
    for route in sorted(packet_counts):
        definition = ROUTE_DEFINITIONS[route]
        coverage.append(
            {
                "repo_update_effect": route,
                "packet_row_count": packet_counts[route],
                "unique_vraag_id_count": unique_counts[route],
                "primary_targets": definition["primary_targets"],
                "conditional_targets": definition["conditional_targets"],
                "status_update_target": definition["status_update_target"],
            }
        )
    return coverage


def target_usage(coverage: list[dict[str, Any]]) -> list[dict[str, Any]]:
    usage: dict[str, dict[str, Any]] = defaultdict(lambda: {"routes": set(), "unique_vraag_id_count": 0})
    for route in coverage:
        targets = set(route["primary_targets"]) | set(route["conditional_targets"]) | {route["status_update_target"]}
        for target in targets:
            usage[target]["routes"].add(route["repo_update_effect"])
            usage[target]["unique_vraag_id_count"] += route["unique_vraag_id_count"]

    out = []
    for target_id, target in sorted(TARGET_ARTIFACTS.items()):
        out.append(
            {
                "target_id": target_id,
                **target,
                "route_count": len(usage[target_id]["routes"]),
                "routes": sorted(usage[target_id]["routes"]),
                "possible_unique_vraag_id_count": usage[target_id]["unique_vraag_id_count"],
            }
        )
    return out


def build_workflow() -> dict[str, Any]:
    packet_index = load_json(PACKET_INDEX_PATH)
    dry_run = load_json(DRY_RUN_PATH)
    coverage = route_coverage(packet_index)
    unknown_routes = sorted(
        {
            row["repo_update_effect"]
            for packet in packet_index["packets"]
            for row in packet["rows"]
            if row["repo_update_effect"] not in ROUTE_DEFINITIONS
        }
    )

    return {
        "generated_on": date.today().isoformat(),
        "current_sprint": "Sprint 33.P6 - Pre-contact validation-readiness: repository/workflow integration",
        "status": "repository_workflow_defined_no_answers_imported",
        "human_validation_status": "no_stakeholder_answers_yet",
        "p5_human_dry_run_status": dry_run["human_dry_run_status"],
        "gate_effect": "P6 is repository-side complete when this workflow is generated and tested; P7 remains blocked until the P5 human dry run is completed.",
        "source_inputs": [
            str(PACKET_INDEX_PATH.relative_to(ROOT)).replace("\\", "/"),
            str(DRY_RUN_PATH.relative_to(ROOT)).replace("\\", "/"),
        ],
        "return_contract": {
            "required_fields": REQUIRED_RETURN_FIELDS,
            "human_input_channel_rule": "Human reviewers enter answers in the Excel validation workbooks. CSV packet files are machine/export/import artifacts and should not be the normal human entry surface.",
            "csv_machine_rule": "CSV files may be generated or machine-edited by repository tooling only; preserve vraag_id, stakeholderpakket and evidence fields exactly.",
            "identity_rule": "Every returned answer must preserve vraag_id and stakeholderpakket; do not merge answers by question text.",
            "evidence_rule": "Confirmed answers require evidence_type and evidence_reference before they can update status, finance, decision or register layers.",
            "source_rule": "New public sources named in responses go to source intake first and are not substantive evidence until processed through the pipeline and verified in top data layers.",
            "unsupported_human_input_rule": "Human input without credible evidence is recorded as low-authority validation input and cannot make a field source-backed, ready, confirmed or settled.",
        },
        "authority_levels": AUTHORITY_LEVELS,
        "answer_outcome_rules": ANSWER_OUTCOME_RULES,
        "target_artifacts": target_usage(coverage),
        "route_definitions": [
            {
                "repo_update_effect": route,
                **definition,
            }
            for route, definition in sorted(ROUTE_DEFINITIONS.items())
        ],
        "route_coverage": coverage,
        "quality_gates": [
            {
                "gate": "excel_for_human_input",
                "rule": "Human reviewers use Excel workbooks; CSV packet files are machine-processing artifacts.",
            },
            {
                "gate": "unsupported_human_input_low_authority",
                "rule": "Human input without source/document/decision/budget evidence is low-authority validation input and cannot settle a field.",
            },
            {
                "gate": "source_ingestion_before_source_backing",
                "rule": "Named public sources must be ingested and verified in top data layers before becoming source-backed evidence.",
            },
            {
                "gate": "no_silent_source_claims",
                "rule": "Stakeholder answers, finance confirmations and decisions are validation evidence, not corpus source claims.",
            },
            {
                "gate": "no_settled_without_evidence",
                "rule": "No D6 register row can move to settled unless classification, owner, executor/coordinator, scale, funding and evidence are directly supported.",
            },
            {
                "gate": "weak_confirmation_stays_open",
                "rule": "Confirmation without evidence is logged but cannot make a field ready for drafting.",
            },
            {
                "gate": "conflicts_escalate",
                "rule": "Conflicting responses create review_needed or decision tickets; the repository team does not choose between them by inference.",
            },
            {
                "gate": "not_my_domain_reroutes",
                "rule": "Not-my-domain answers keep the original vraag_id and are rerouted rather than counted as negative validation.",
            },
        ],
        "unknown_routes": unknown_routes,
        "ready_for_p7": False,
        "p7_blockers": [
            "P5 human internal dry run is pending.",
            "No stakeholder packets may be sent before P7 send-readiness gate.",
            "No returned stakeholder answers exist yet.",
        ],
    }


def render_markdown(workflow: dict[str, Any]) -> str:
    lines = [
        "# Pre-contact Response Workflow",
        "",
        "## Summary",
        f"Current sprint: {workflow['current_sprint']}.",
        "",
        f"Generated on: {workflow['generated_on']}.",
        "",
        f"Status: `{workflow['status']}`.",
        "",
        f"Human validation status: `{workflow['human_validation_status']}`.",
        "",
        f"P5 human dry-run status: `{workflow['p5_human_dry_run_status']}`.",
        "",
        f"Gate effect: {workflow['gate_effect']}",
        "",
        "This file defines how returned D5/D6 packet answers must be processed. It does not import answers and it does not authorize stakeholder contact.",
        "",
        "## Return Contract",
        "",
        "| Rule | Meaning |",
        "| --- | --- |",
        f"| Required fields | `{', '.join(workflow['return_contract']['required_fields'])}` |",
        f"| Human input channel rule | {workflow['return_contract']['human_input_channel_rule']} |",
        f"| CSV machine rule | {workflow['return_contract']['csv_machine_rule']} |",
        f"| Identity rule | {workflow['return_contract']['identity_rule']} |",
        f"| Evidence rule | {workflow['return_contract']['evidence_rule']} |",
        f"| Source rule | {workflow['return_contract']['source_rule']} |",
        f"| Unsupported human input rule | {workflow['return_contract']['unsupported_human_input_rule']} |",
        "",
        "## Authority Levels",
        "",
        "| Level | Authority | Meaning | Allowed effect |",
        "| --- | --- | --- | --- |",
    ]
    for level in workflow["authority_levels"]:
        lines.append(
            f"| `{level['level']}` | `{level['authority']}` | {level['meaning']} | {level['allowed_effect']} |"
        )

    lines.extend(
        [
        "",
        "## Answer Outcomes",
        "",
        "| Outcome | May update status? | Processing rule |",
        "| --- | --- | --- |",
        ]
    )
    for rule in workflow["answer_outcome_rules"]:
        may_update = "yes" if rule["may_update_status"] else "no"
        lines.append(f"| `{rule['outcome']}` | {may_update} | {rule['processing']} |")

    lines.extend(
        [
            "",
            "## Route Coverage",
            "",
            "| Repo update effect | Unique vraag IDs | Packet rows | Primary targets | Conditional targets | Status target |",
            "| --- | ---: | ---: | --- | --- | --- |",
        ]
    )
    for route in workflow["route_coverage"]:
        lines.append(
            f"| `{route['repo_update_effect']}` | {route['unique_vraag_id_count']} | {route['packet_row_count']} | `{', '.join(route['primary_targets'])}` | `{', '.join(route['conditional_targets'])}` | `{route['status_update_target']}` |"
        )

    lines.extend(
        [
            "",
            "## Target Artifacts",
            "",
            "| Target | Status | Path | Purpose |",
            "| --- | --- | --- | --- |",
        ]
    )
    for target in workflow["target_artifacts"]:
        lines.append(f"| `{target['target_id']}` | `{target['status']}` | `{target['path']}` | {target['purpose']} |")

    lines.extend(["", "## Quality Gates", ""])
    for gate in workflow["quality_gates"]:
        lines.append(f"- `{gate['gate']}`: {gate['rule']}")

    lines.extend(
        [
            "",
            "## P7 Blockers",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in workflow["p7_blockers"])
    lines.extend(
        [
            "",
            "## Next Step",
            "",
            "P7 send-readiness cannot open until the P5 human dry run is completed and any packet fixes are made. If answers return later, process them through this workflow instead of editing status, finance, decision or D6 register layers directly.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    workflow = build_workflow()
    OUTPUT_JSON_PATH.write_text(
        json.dumps(workflow, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    OUTPUT_DOC_PATH.write_text(render_markdown(workflow), encoding="utf-8")
    print(f"Wrote {OUTPUT_JSON_PATH.relative_to(ROOT)}")
    print(f"Wrote {OUTPUT_DOC_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
