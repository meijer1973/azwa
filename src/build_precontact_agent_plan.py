from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_JSON_PATH = ROOT / "data" / "workagenda" / "precontact_agent_plan.json"
OUTPUT_DOC_PATH = ROOT / "docs" / "review" / "precontact-agent-prompts.md"

TRACEABILITY_PATH = "data/workagenda/validation_workbook_traceability_map.json"
PREFILL_AUDIT_PATH = "data/workagenda/validation_workbook_prefill_audit.json"


def base_guardrails() -> list[str]:
    return [
        "This is pre-contact validation-readiness work, not stakeholder validation.",
        "Do not contact policymakers, municipal officers, providers, insurers, GGD/JGZ, finance/controller roles or partners.",
        "Do not settle D5 or D6 ownership, mandate, funding, formal classification or safe final wording.",
        "Do not treat Excel workbook text, generated JSON, dashboard text or deep-research reports as public source evidence.",
        "If a public source is found, mark it as a source-intake candidate; it must be ingested and checked through the repository pipeline before use.",
        "Return concise findings that reduce human workload before packet export.",
    ]


def shared_inputs() -> list[str]:
    return [
        "RESEARCH_AGENT_MAP.md",
        "docs/data-quality-roadmap.md",
        "docs/review/validation-instrument-register.md",
        "docs/review/validation-workbook-traceability-audit.md",
        "docs/review/validation-workbook-prefill-audit.md",
        TRACEABILITY_PATH,
        PREFILL_AUDIT_PATH,
        "docs/review/D5_validatieformat_werkagenda_Almere_v0.3.xlsx",
        "docs/review/Almere_D6_validatieformats.xlsx",
    ]


def agent_plans() -> list[dict[str, Any]]:
    return [
        {
            "agent_id": "p3_evidence_prefill_audit",
            "name": "Evidence-prefill audit agent",
            "dispatch_status": "prepared_not_sent",
            "purpose": "Check whether current workbook working views have enough repository/source support before humans see them.",
            "priority": 1,
            "inputs": shared_inputs()
            + [
                "data/workagenda/d5_status_matrix.json",
                "data/workagenda/d5_validation_tickets.json",
                "docs/review/almere_d6_deep_research_learnings.md",
                "docs/review/almere_d6_open_questions.md",
                "docs/review/almere_d6_validation_ticket_matrix.md",
            ],
            "focus": [
                "D5 tabs with missing current working view: Financiering, Governance rollen, Monitoring cyclus, D6 afhankelijkheden.",
                "Any row whose current working view is weak, overly broad, or not clearly source-backed.",
                "D6 tabs where safe wording depends on public evidence versus validation.",
            ],
            "may_resolve": [
                "Evidence-strength grading.",
                "Source-intake candidate identification.",
                "Safer pre-contact wording suggestions.",
            ],
            "must_not_resolve": [
                "Formal D5/D6 decisions.",
                "Local ownership or mandate.",
                "Funding allocation.",
                "Stakeholder validation status.",
            ],
            "deliverable_fields": [
                "workbook",
                "sheet",
                "vraag_id_or_component",
                "current_working_view",
                "evidence_strength",
                "missing_source",
                "source_candidate",
                "human_validation_still_needed",
                "safe_dutch_wording",
                "packet_change_recommendation",
            ],
        },
        {
            "agent_id": "p3_d5_source_update_watchlist",
            "name": "D5 source-update watchlist agent",
            "dispatch_status": "prepared_not_sent",
            "purpose": "Create a narrow watchlist for time-dependent D5 sources expected before workagenda drafting.",
            "priority": 2,
            "inputs": shared_inputs()
            + [
                "config/monthly_source_audit.json",
                "data/extracted/monthly_source_audit.json",
                "docs/internal/monthly-source-audit-2026-04-30.md",
                "data/site/timeline_register.json",
            ],
            "focus": [
                "D5 handreikingen expected end May.",
                "Handreiking Regionale Preventie Infrastructuur.",
                "Regioscan and rode-dradenanalyse.",
                "Ontwikkelagenda process for beproevende regio's.",
                "Finance updates for AZWA/D5, doorbraakmiddelen, Zvw and social-domain funding.",
            ],
            "may_resolve": [
                "Expected-source watchlist entries.",
                "Workbook tabs affected by each expected source.",
                "Action after source appears.",
            ],
            "must_not_resolve": [
                "Using expected sources as if they already exist.",
                "Filling local workagenda answers from watchlist entries.",
            ],
            "deliverable_fields": [
                "source",
                "expected_timing",
                "relevance",
                "workbook_tabs_affected",
                "trigger_for_action",
                "action_after_source_appears",
                "current_status",
            ],
        },
        {
            "agent_id": "p3_d5_d6_dependency_mapping",
            "name": "D5-D6 dependency mapping agent",
            "dispatch_status": "prepared_not_sent",
            "purpose": "Map D5 workagenda components to likely D6 prerequisites so D5 packets do not promise implementation without social-base infrastructure.",
            "priority": 3,
            "inputs": shared_inputs()
            + [
                "data/workagenda/d5_status_matrix.json",
                "data/workagenda/d5_validation_tickets.json",
                "data/extracted/municipal/almere_d6_responsibility_register.json",
                "docs/review/almere_d6_validation_ticket_matrix.md",
                "docs/review/almere_d6_open_questions.md",
            ],
            "focus": [
                "D5 rows where D6 dependency is possible or unknown.",
                "Dependencies around inloopvoorzieningen, wijkteams, JGZ/GGD, Samen Sterker, monitoring, digital infrastructure and informal support.",
                "Questions that should be asked together in stakeholder packets.",
            ],
            "may_resolve": [
                "Likely dependency mapping.",
                "Dependency validation question wording.",
                "Risk labels for D5 items blocked by unresolved D6 infrastructure.",
            ],
            "must_not_resolve": [
                "Whether a D6 component is formally settled.",
                "Which organization owns or funds the D6 component.",
            ],
            "deliverable_fields": [
                "d5_component",
                "likely_d6_dependency",
                "dependency_status",
                "affected_vraag_ids",
                "validation_question",
                "risk_if_unresolved",
                "recommended_packet",
            ],
        },
        {
            "agent_id": "p3_policymaker_readability",
            "name": "Policymaker readability agent",
            "dispatch_status": "prepared_not_sent",
            "purpose": "Make stakeholder-facing packet language plain Dutch and easy to answer.",
            "priority": 4,
            "inputs": shared_inputs(),
            "focus": [
                "Language flags in validation_workbook_prefill_audit.json.",
                "D6 terms such as evidence and social-base.",
                "Broad prompts in Gezonde School and Samen Sterker.",
                "Any internal terms: repository, register, prefill, inferred, source intake, top layer, pipeline, JSON, claim layer.",
            ],
            "may_resolve": [
                "Replacement wording.",
                "Question simplification.",
                "Packet instructions.",
            ],
            "must_not_resolve": [
                "Substantive policy answer choices beyond making the existing choices readable.",
                "Final workagenda wording approval.",
            ],
            "deliverable_fields": [
                "workbook",
                "sheet",
                "vraag_id_or_location",
                "issue_type",
                "current_text",
                "recommended_replacement",
                "priority",
                "reason",
            ],
        },
        {
            "agent_id": "p3_finance_risk_precheck",
            "name": "Finance-risk precheck agent",
            "dispatch_status": "prepared_not_sent",
            "purpose": "Identify where finance/controller validation is unavoidable before packet export.",
            "priority": 5,
            "inputs": shared_inputs()
            + [
                "data/workagenda/d5_status_matrix.json",
                "docs/review/almere_d6_validation_ticket_matrix.md",
                "docs/review/validation-workbook-prefill-audit.md",
            ],
            "focus": [
                "D5 finance workbook tab.",
                "D6 financing and budget-demarcation tab.",
                "Rows with mixed funding, unknown funding, project continuity or double-counting risk.",
                "Separation of AZWA-D5, AZWA-D6, SPUK/GALA, PGA/IZA, regular municipal funding, GGD contribution/plustaak and Zvw/insurer funding.",
            ],
            "may_resolve": [
                "Finance questions to ask controllers.",
                "Double-counting risk preclassification.",
                "Urgency for finance packet routing.",
            ],
            "must_not_resolve": [
                "Actual funding allocation.",
                "Controller confirmation.",
                "Insurer/Zvw commitment.",
            ],
            "deliverable_fields": [
                "component",
                "possible_funding_lines",
                "double_counting_risk",
                "controller_question",
                "zvw_or_insurer_question",
                "urgency",
                "evidence_needed",
            ],
        },
    ]


def prompt_for(agent: dict[str, Any]) -> str:
    sections = [
        "You are supporting the AZWA/IZA/GALA Almere repository during Sprint 33.P3: targeted pre-contact validation-readiness.",
        "",
        f"Task: {agent['name']}",
        "",
        "Purpose:",
        agent["purpose"],
        "",
        "Start from these repository inputs:",
        *[f"- `{item}`" for item in agent["inputs"]],
        "",
        "Focus only on:",
        *[f"- {item}" for item in agent["focus"]],
        "",
        "You may resolve:",
        *[f"- {item}" for item in agent["may_resolve"]],
        "",
        "You must not resolve:",
        *[f"- {item}" for item in agent["must_not_resolve"]],
        "",
        "Guardrails:",
        *[f"- {item}" for item in base_guardrails()],
        "",
        "Deliver a concise table with these fields:",
        *[f"- `{item}`" for item in agent["deliverable_fields"]],
        "",
        "Also include:",
        "- clear conclusions;",
        "- evidence used;",
        "- important uncertainties or conflicts;",
        "- practical implications for packet export.",
    ]
    return "\n".join(sections)


def build_plan() -> dict[str, Any]:
    agents = []
    for agent in agent_plans():
        agents.append({**agent, "prompt": prompt_for(agent)})

    return {
        "generated_on": date.today().isoformat(),
        "current_sprint": "Sprint 33.P3 - Pre-contact validation-readiness: targeted pre-contact agents",
        "purpose": "Prepare narrow agent assignments that reduce validation workload before policymaker contact.",
        "dispatch_status": "prepared_not_sent",
        "guardrails": base_guardrails(),
        "shared_inputs": shared_inputs(),
        "agents": agents,
        "next_step_after_agent_results": "Use results in Sprint 33.P4 to build filtered stakeholder packets; do not contact policymakers before the P7 send-readiness gate.",
    }


def render_markdown(plan: dict[str, Any]) -> str:
    lines = [
        "# Pre-contact Agent Prompts",
        "",
        "## Summary",
        "Current sprint: Sprint 33.P3 - Pre-contact validation-readiness: targeted pre-contact agents.",
        "",
        f"Generated on: {plan['generated_on']}.",
        "",
        "This file contains narrow, copy-ready agent prompts for pre-contact QA. These prompts are prepared, not sent. They are meant to reduce validation workload before stakeholder packets are built.",
        "",
        "## Guardrails",
        "",
    ]
    lines.extend(f"- {item}" for item in plan["guardrails"])
    lines.extend(
        [
            "",
            "## Agent Set",
            "",
            "| Agent | Priority | Purpose | Status |",
            "| --- | ---: | --- | --- |",
        ]
    )
    for agent in plan["agents"]:
        lines.append(
            f"| `{agent['agent_id']}` | {agent['priority']} | {agent['purpose']} | `{agent['dispatch_status']}` |"
        )

    for agent in plan["agents"]:
        lines.extend(
            [
                "",
                f"## {agent['name']}",
                "",
                f"Agent ID: `{agent['agent_id']}`",
                "",
                "```text",
                agent["prompt"],
                "```",
            ]
        )

    lines.extend(
        [
            "",
            "## Next Step",
            "",
            plan["next_step_after_agent_results"],
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    plan = build_plan()
    OUTPUT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON_PATH.write_text(
        json.dumps(plan, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    OUTPUT_DOC_PATH.write_text(render_markdown(plan), encoding="utf-8")
    print(f"Wrote {OUTPUT_JSON_PATH.relative_to(ROOT)}")
    print(f"Wrote {OUTPUT_DOC_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
