from __future__ import annotations

import json
import re
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS_MATRIX = ROOT / "data" / "workagenda" / "d5_status_matrix.json"
VALIDATION_TICKETS = ROOT / "data" / "workagenda" / "d5_validation_tickets.json"
OUTPUT = ROOT / "data" / "workagenda" / "almere_regional_workagenda_input_objects.json"


SOURCE_LAYERS = [
    "data/workagenda/d5_status_matrix.json",
    "data/workagenda/d5_validation_tickets.json",
    "data/workagenda/d5_validation_packets.json",
    "data/workagenda/d5_stuurmodel.json",
    "data/extracted/workagenda_d5_operational_requirements.json",
    "data/extracted/workagenda_nulmeting_capacity.json",
    "data/extracted/municipal/almere_d6_responsibility_register.json",
    "data/site/source_view_models/zorgakkoorden-werkagenda-handvatten.json",
    "data/site/source_view_models/format-werkagenda-azwa.json",
    "data/site/source_view_models/opdracht-werkagenda-d5-azwa.json",
    "data/site/source_view_models/toelichting-werkagenda-d5-azwa.json",
]

VALPREVENTIE_SOURCE_LAYERS = [
    "data/site/source_view_models/ggd-valpreventie-almere.json",
    "data/site/source_view_models/ketendocument-valpreventie-almere.json",
    "data/extracted/documents/reg_ggd_flevoland_valpreventie_almere.json",
    "data/extracted/documents/reg_ggd_flevoland_valpreventie_almere_ketendocument_2026.json",
    "data/extracted/claims/reg_ggd_flevoland_valpreventie_almere.json",
    "data/extracted/claims/reg_ggd_flevoland_valpreventie_almere_ketendocument_2026.json",
]

NATIONAL_SOURCE_REF = {
    "source_id": "nat_zorgakkoorden_werkagenda_handvatten_2026",
    "title": "Handvatten voor het opstellen van de regionale werkagenda",
    "use_for": [
        "regional workagenda process",
        "D5/D6 relation",
        "formal adoption deadline",
    ],
    "authority": "national_process_source",
    "confidence": "high",
}

VALPREVENTIE_SOURCE_REFS = [
    {
        "source_id": "reg_ggd_flevoland_valpreventie_almere",
        "title": "Valpreventie Gemeente Almere",
        "use_for": [
            "public Almere route",
            "walk-in",
            "risk assessment",
            "course matching",
        ],
        "authority": "regional_operational_source",
        "confidence": "medium",
    },
    {
        "source_id": "reg_ggd_flevoland_valpreventie_almere_ketendocument_2026",
        "title": "Ketendocument Valpreventie Almere",
        "use_for": [
            "chain approach",
            "roles",
            "finance signals",
            "monitoring signals",
        ],
        "authority": "regional_implementation_source",
        "confidence": "medium",
    },
]

TICKET_PRIORITY = {
    "local_status_capacity": 1,
    "governance_roles": 2,
    "finance_controller": 3,
    "d6_dependency": 4,
    "decision_phasing": 5,
    "scope_choice": 6,
}

QUESTION_ANSWER_TYPES = {
    "local_status_capacity": "controlled_status_plus_evidence",
    "governance_roles": "role_confirmation_plus_evidence",
    "finance_controller": "finance_controller_confirmation",
    "d6_dependency": "dependency_status_plus_evidence",
    "decision_phasing": "decision_or_phasing_status",
    "scope_choice": "scope_choice_plus_rationale",
}

STATUS_GAP_RULES = [
    (
        "finance_status",
        "finance",
        "controllercheck_nodig",
        "finance_validation_gap",
        "validated funding route and continuity status",
        True,
    ),
    (
        "governance_status",
        "governance",
        "eigenaar_onbekend",
        "governance_validation_gap",
        "validated owner, coordinator, executor and mandate",
        True,
    ),
    (
        "capacity_status",
        "capacity",
        "indicatief",
        "capacity_gap",
        "validated local coverage, capacity and constraints",
        True,
    ),
    (
        "monitoring_status",
        "monitoring",
        "concept",
        "monitoring_gap",
        "validated monitoring, data owner and learning-cycle arrangement",
        True,
    ),
    (
        "decision_status",
        "decision",
        "besluit_nodig",
        "decision_or_phasing_gap",
        "decision owner, phasing route and status before final drafting",
        True,
    ),
]

D6_GAP_STATUSES = {"mogelijk", "onbekend", "nog_te_valideren"}

FIELD_STATUS_GAPS = {
    "C": "local_validation_gap",
    "D": "decision_or_phasing_gap",
    "E": "finance_validation_gap",
    "G": "monitoring_gap",
}

VALPREVENTIE_LOCAL_ELEMENTS = [
    "walk-in route",
    "fall-risk assessment",
    "course matching",
    "intervention route",
    "possible connection to structural sport and exercise offer",
]

DO_NOT_CLAIM_STANDARD = [
    "fully funded",
    "structurally secured",
    "owner confirmed",
    "capacity confirmed",
    "regional dependency resolved",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def build_process_context() -> dict[str, Any]:
    return {
        "sender": {
            "organisation": "Gemeente Almere",
            "role": "local input provider for regional workagenda",
        },
        "recipient": {
            "organisation": "regional workagenda process",
            "role": "regional consolidation and drafting",
        },
        "regional_process_owner": {
            "organisation": "mandaatgemeente and preferente zorgverzekeraar",
            "role": "prepare regional workagenda with regional partners",
            "source_id": "nat_zorgakkoorden_werkagenda_handvatten_2026",
        },
        "formal_workagenda_deadline": {
            "date": "2026-11-15",
            "description": "Regional workagenda adopted by colleges",
            "status": "source_backed",
            "source_id": "nat_zorgakkoorden_werkagenda_handvatten_2026",
        },
        "almere_internal_submission_target": {
            "date": "2026-09-15",
            "description": "Target date for Almere to send structured input to the regional workagenda process",
            "status": "planning_assumption",
            "source_backing": "internal_planning_or_user_supplied; not national formal deadline",
        },
    }


def component_slug(component_id: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "-", component_id.upper()).strip("-")


def concept_handoff_ready(row: dict[str, Any]) -> bool:
    return bool(row.get("public_evidence")) or row.get("public_foundation") in {"sterk", "deels"} or bool(
        row.get("required_in_workagenda")
    )


def confidence_for(row: dict[str, Any]) -> str:
    foundation = row.get("public_foundation")
    if foundation == "sterk":
        return "medium"
    if foundation == "deels":
        return "medium-low"
    return "low"


def unresolved_reasons(row: dict[str, Any]) -> list[dict[str, str]]:
    fields = [
        "local_validation_status",
        "decision_status",
        "finance_status",
        "capacity_status",
        "governance_status",
        "monitoring_status",
        "d6_dependency_status",
    ]
    reasons = [{"field": field, "status": str(row[field])} for field in fields if row.get(field)]
    for value in row.get("local_fill_fields", []):
        reasons.append({"field": "local_fill_field", "status": str(value)})
    for value in row.get("decision_needed", []):
        reasons.append({"field": "decision_needed", "status": str(value)})
    return reasons


def build_gap_summary(row: dict[str, Any]) -> dict[str, Any]:
    component = row["target_id"]
    gaps: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    def add_gap(
        field: str,
        current_state: str,
        needed_for_region: str,
        gap_type: str,
        blocking_for_final_workagenda: bool,
    ) -> None:
        key = (field, gap_type)
        if key in seen:
            return
        seen.add(key)
        gaps.append(
            {
                "gap_id": f"{component_slug(component)}-GAP-{component_slug(field)}",
                "field": field,
                "current_state": current_state,
                "needed_for_region": needed_for_region,
                "gap_type": gap_type,
                "blocking_for_final_workagenda": blocking_for_final_workagenda,
            }
        )

    for status_field, field, trigger, gap_type, needed, blocks in STATUS_GAP_RULES:
        if row.get(status_field) == trigger:
            add_gap(field, str(row[status_field]), needed, gap_type, blocks)

    if row.get("d6_dependency_status") in D6_GAP_STATUSES:
        add_gap(
            "d6_dependency",
            str(row.get("d6_dependency_status")),
            "validated D6 dependency map and any critical prerequisites for this D5 component",
            "d6_dependency_mapping_gap",
            True,
        )

    for field_name, cell in row.get("field_statuses", {}).items():
        code = cell.get("status_code")
        if code not in FIELD_STATUS_GAPS:
            continue
        blockers = cell.get("blockers", [])
        needed = cell.get("reason", "Validation or decision detail needed before final workagenda use.")
        add_gap(
            field_name,
            code,
            needed,
            FIELD_STATUS_GAPS[code],
            code in {"C", "D", "E", "G"},
        )
        for blocker in blockers:
            add_gap(
                str(blocker),
                "unconfirmed",
                "explicit validation, decision or evidence path before final workagenda use",
                FIELD_STATUS_GAPS[code],
                code in {"C", "D", "E", "G"},
            )

    ready = concept_handoff_ready(row)
    confirmed = bool(row.get("ready_for_workagenda_drafting"))
    return {
        "overall_gap_type": "workagenda_input_gap",
        "can_send_as_concept": ready,
        "can_send_as_confirmed_position": confirmed,
        "main_gaps": gaps,
    }


def ticket_type(ticket_id: str) -> str:
    return ticket_id.rsplit("__", 1)[-1]


def build_priority_questions(
    component_id: str,
    ticket_ids: list[str],
    ticket_lookup: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    sorted_ticket_ids = sorted(ticket_ids, key=lambda item: TICKET_PRIORITY.get(ticket_type(item), 99))
    questions: list[dict[str, Any]] = []
    for index, ticket_id in enumerate(sorted_ticket_ids[:5], start=1):
        ticket_item = ticket_lookup.get(ticket_id)
        if not ticket_item:
            continue
        type_name = ticket_item.get("ticket_type", ticket_type(ticket_id))
        questions.append(
            {
                "question_id": f"{component_slug(component_id)}-ALMERE-Q{index}",
                "source_ticket_id": ticket_id,
                "question": ticket_item.get("question", ""),
                "answer_type": QUESTION_ANSWER_TYPES.get(type_name, "controlled_answer_plus_evidence"),
                "priority": "high" if index <= 3 else "medium",
                "evidence_required": True,
            }
        )
    return questions


def actors_from_row(row: dict[str, Any]) -> list[dict[str, str]]:
    raw_owner = row.get("action_owner", "Nog te bepalen")
    names = [part.strip() for part in str(raw_owner).split(";") if part.strip()]
    return [
        {
            "name": name,
            "role": "validation_or_handoff_actor",
            "source": "data/workagenda/d5_status_matrix.json?action_owner",
        }
        for name in names
    ]


def build_decision_requests(row: dict[str, Any]) -> list[dict[str, Any]]:
    requests = []
    for index, item in enumerate(row.get("decision_needed", []), start=1):
        requests.append(
            {
                "request_id": f"{component_slug(row['target_id'])}-DECISION-{index:02d}",
                "decision_area": item,
                "question": f"Confirm the regional or Almere decision route for {item} before this becomes a confirmed workagenda position.",
                "status": row.get("decision_status", "unknown"),
                "needed_for": "final_workagenda_position",
            }
        )
    if not row.get("required_in_workagenda"):
        requests.insert(
            0,
            {
                "request_id": f"{component_slug(row['target_id'])}-DECISION-SCOPE",
                "decision_area": "scope_choice",
                "question": "Decide whether this optional or conditional item should be included in the regional workagenda process.",
                "status": row.get("decision_status", "scopekeuze_nodig"),
                "needed_for": "first_handoff_scope",
            },
        )
    return requests


def build_policy_input(row: dict[str, Any]) -> dict[str, Any]:
    title = row["title"]
    required = bool(row.get("required_in_workagenda"))
    if required:
        summary = (
            f"Almere can send {title} as concept input for the regional workagenda, with public-source "
            "foundation and explicit unresolved validation, finance, governance, decision and D6-dependency gaps."
        )
        proposed = (
            "Use as concept D5 input with validation gaps. Do not write as a confirmed Almere workagenda "
            "position until local validation, finance/controller check, governance ownership and D6 dependency "
            "mapping are resolved or explicitly escalated."
        )
    else:
        summary = (
            f"Almere can only send {title} as a scope-choice item unless Almere or the region chooses to include it."
        )
        proposed = (
            "Use as optional scope input only. Do not include as a required D5 position without an explicit scope "
            "decision and follow-up validation route."
        )
    return {
        "summary_for_region": summary,
        "proposed_workagenda_position": proposed,
        "confidence": confidence_for(row),
        "public_foundation": row.get("public_foundation", "onbekend"),
        "local_validation_status": row.get("local_validation_status", "onbekend"),
        "drafting_guardrail": "Concept input is not a confirmed local policy position or final regional workagenda text.",
    }


def unresolved_gap_phrase(gaps: list[dict[str, Any]]) -> str:
    preferred = [
        "ownership",
        "finance",
        "capacity",
        "monitoring",
        "D6 dependencies",
        "decision/phasing",
    ]
    fields = {gap["field"] for gap in gaps}
    selected = []
    if "governance" in fields or "lokale_eigenaar" in fields:
        selected.append("ownership")
    if "finance" in fields or "budget" in fields:
        selected.append("finance")
    if "capacity" in fields or "aantallen_capaciteit" in fields:
        selected.append("capacity")
    if "monitoring" in fields or "monitoringafspraak" in fields:
        selected.append("monitoring")
    if "d6_dependency" in fields or "d6_afhankelijkheden" in fields:
        selected.append("D6 dependencies")
    if "decision" in fields or "prioritering_2027_2030" in fields or "formele_besluitstatus" in fields:
        selected.append("decision/phasing")
    selected = [item for item in preferred if item in selected]
    return ", ".join(selected) if selected else "the listed validation gaps"


def recommended_wording(row: dict[str, Any], gaps: list[dict[str, Any]]) -> str:
    if row["target_id"] == "valpreventie":
        return (
            "Almere ziet valpreventie als een logisch D5-onderdeel voor de regionale werkagenda. "
            "Openbare bronnen tonen een bestaande uitvoeringsroute met inloop, risico-inschatting en "
            "cursusmatching. Voor definitieve werkagendavorming moeten eigenaarschap, financiering, "
            "capaciteit, monitoring en D6-afhankelijkheden nog gericht worden gevalideerd."
        )
    if not row.get("required_in_workagenda"):
        return (
            f"Almere ziet {row['title']} als een optioneel of conditioneel onderwerp voor de regionale "
            "werkagenda. Dit kan alleen als scopevraag worden meegegeven; opname als werkagendapositie "
            "vraagt eerst om een expliciete keuze van Almere en/of het regionale proces."
        )
    return (
        f"Almere ziet {row['title']} als een relevant D5-onderdeel voor de regionale werkagenda. "
        f"Openbare bronnen geven een {row.get('public_foundation', 'onbekende')} basis voor opname. "
        f"Almere kan dit als conceptinput aanleveren, maar {unresolved_gap_phrase(gaps)} moeten nog "
        "worden gevalideerd voordat dit als bevestigde werkagendapositie kan worden gebruikt."
    )


def source_refs_for(row: dict[str, Any]) -> list[dict[str, Any]]:
    refs = [NATIONAL_SOURCE_REF]
    if row["target_id"] == "valpreventie":
        refs.extend(VALPREVENTIE_SOURCE_REFS)
    for source_id in row.get("evidence", {}).get("operational_requirement_source_ids", []):
        if source_id == NATIONAL_SOURCE_REF["source_id"] or any(ref["source_id"] == source_id for ref in refs):
            continue
        refs.append(
            {
                "source_id": source_id,
                "title": source_id,
                "use_for": ["D5 operational requirement context"],
                "authority": "repository_source_layer_reference",
                "confidence": "medium",
            }
        )
    return refs


def derived_layers_for(row: dict[str, Any]) -> list[str]:
    layers = [
        "data/workagenda/d5_status_matrix.json",
        "data/workagenda/d5_validation_tickets.json",
        "data/workagenda/d5_stuurmodel.json",
        "data/extracted/workagenda_d5_operational_requirements.json",
        "data/extracted/workagenda_nulmeting_capacity.json",
        "data/extracted/municipal/almere_d6_responsibility_register.json",
    ]
    if row["target_id"] == "valpreventie":
        layers.extend(VALPREVENTIE_SOURCE_LAYERS)
    return layers


def build_finance_input(row: dict[str, Any]) -> dict[str, Any]:
    signals: list[str] = []
    finance_cell = row.get("field_statuses", {}).get("financiering", {})
    signals.extend(finance_cell.get("evidence", []))
    if row["target_id"] == "valpreventie":
        signals.append(
            "Ketendocument contains finance/declaration signals, but controller validation and continuity status remain unresolved."
        )
    return {
        "almere_current_position": row.get("finance_status", "onbekend"),
        "known_signals": signals,
        "to_send_to_region": "Finance/controller route and continuity status must remain explicit validation items.",
        "do_not_claim": DO_NOT_CLAIM_STANDARD,
    }


def build_monitoring_input(row: dict[str, Any]) -> dict[str, Any]:
    candidates: list[str] = []
    if row.get("public_indicator_count", 0):
        candidates.append(f"public_indicator_count={row['public_indicator_count']}")
    if row.get("indicative_calculation_count", 0):
        candidates.append(f"indicative_calculation_count={row['indicative_calculation_count']}")
    if row["target_id"] == "valpreventie":
        candidates.append("ketendocument monitoring and registration signals, still to be validated")
    return {
        "almere_current_position": row.get("monitoring_status", "onbekend"),
        "candidate_indicators": candidates,
        "to_send_to_region": "Send candidate monitoring signals as validation needs, not as a settled monitoring arrangement.",
    }


def build_target_state(row: dict[str, Any]) -> dict[str, list[str]]:
    if row.get("required_in_workagenda"):
        needs = [
            "validated current local status and coverage",
            "validated owner, coordinator, executor and partner roles",
            "finance/controller confirmation for funding route and continuity",
            "D6 dependency status and any critical prerequisites",
            "decision or phasing route toward regional workagenda drafting",
        ]
        minimum = [
            "component title and D5 classification",
            "public evidence basis from the status matrix",
            "explicit unresolved gaps",
            "priority validation questions and ticket IDs",
            "safe handoff wording that avoids confirmed-position claims",
        ]
    else:
        needs = [
            "scope decision on whether to include the optional or conditional item",
            "follow-up validation route if included",
        ]
        minimum = [
            "scope-choice question",
            "public evidence or weak-source limitation",
            "reason not to treat as required workagenda content yet",
        ]
    return {
        "what_region_needs_from_almere": needs,
        "minimum_viable_input": minimum,
        "not_needed_in_first_submission": [
            "full validation workbook answer set",
            "final finance/controller proof for every unresolved field",
            "confirmed governance mandate where it has not yet been validated",
            "final college-adopted workagenda wording",
        ],
    }


def build_risk_assessment(row: dict[str, Any], gaps: list[dict[str, Any]]) -> dict[str, Any]:
    risk = row.get("risk", "onbekend")
    if risk == "rood":
        overall = "High risk for final workagenda use until validation and decisions are resolved."
    elif risk == "geel":
        overall = "Usable for concept handoff with visible validation gaps."
    elif risk == "grijs":
        overall = "Scope or applicability risk; do not treat as required workagenda content yet."
    else:
        overall = "Risk status unknown."
    return {
        "risk_code": risk,
        "overall": overall,
        "risk_to_submission": "Low if sent as concept input with explicit gaps; higher if framed as confirmed.",
        "risk_to_final_workagenda": "Blocking gaps remain until validation, finance/controller, governance and D6 dependency questions are resolved.",
        "main_reasons": [gap["gap_type"] for gap in gaps[:8]],
    }


def build_handoff_links(row: dict[str, Any]) -> list[dict[str, str]]:
    links = [
        {
            "label": "D5 status matrix row",
            "path": "data/workagenda/d5_status_matrix.json",
            "use": "component status, evidence, gaps and risk",
        },
        {
            "label": "D5 validation tickets",
            "path": "data/workagenda/d5_validation_tickets.json",
            "use": "priority validation questions",
        },
    ]
    if row["target_id"] == "valpreventie":
        links.extend(
            [
                {
                    "label": "GGD Valpreventie Almere source view",
                    "path": "data/site/source_view_models/ggd-valpreventie-almere.json",
                    "use": "public route, walk-in, risk assessment and course matching",
                },
                {
                    "label": "Ketendocument Valpreventie Almere source view",
                    "path": "data/site/source_view_models/ketendocument-valpreventie-almere.json",
                    "use": "chain approach, finance, role and monitoring signals",
                },
            ]
        )
    return links


def build_object(
    row: dict[str, Any],
    tickets_by_component: dict[str, list[str]],
    ticket_lookup: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    component_id = row["target_id"]
    ready = concept_handoff_ready(row)
    confirmed = bool(row.get("ready_for_workagenda_drafting"))
    ticket_ids = tickets_by_component.get(component_id, [])
    gap_summary = build_gap_summary(row)
    main_gaps = gap_summary["main_gaps"]

    # Most object fields below are conservative transformations of generated
    # steering layers. They are not new source claims or stakeholder validation.
    return {
        "input_id": f"ALMERE-D5-{component_slug(component_id)}-INPUT-001",
        "component_id": component_id,
        "title": row["title"],
        "domain": None,
        "d5_or_d6": "D5",
        "component_type": row.get("category"),
        "required_in_workagenda": bool(row.get("required_in_workagenda")),
        "local_action_deadline": {
            "date": row.get("deadline"),
            "status": "status_matrix_local_action_deadline" if row.get("deadline") else "not_provided",
            "source": "data/workagenda/d5_status_matrix.json?deadline",
        },
        "almere_submission": {
            "submission_status": "concept_input" if ready else "not_ready_for_handoff",
            "concept_handoff_ready": ready,
            "confirmed_position_ready": confirmed,
            "recommended_submission_type": "confirmed_position"
            if confirmed
            else "concept_with_validation_gaps",
            "reason_not_confirmed": [] if confirmed else unresolved_reasons(row),
        },
        "almere_policy_input": build_policy_input(row),
        "current_state": {
            "known_from_public_sources": row.get("public_evidence", []),
            "known_or_indicated_local_elements": VALPREVENTIE_LOCAL_ELEMENTS
            if component_id == "valpreventie"
            else [],
            "unknown_or_unconfirmed": row.get("local_fill_fields", []),
        },
        "target_state_for_regional_workagenda": build_target_state(row),
        "gap_summary": gap_summary,
        "decision_requests_for_region": build_decision_requests(row),
        "validation_needed_before_or_after_submission": {
            "status": "limited_validation_needed" if not confirmed else "no_validation_needed",
            "do_not_overload_first_contact": True,
            "validation_ticket_ids": ticket_ids,
            "priority_questions": build_priority_questions(component_id, ticket_ids, ticket_lookup),
        },
        "actors": actors_from_row(row),
        "finance_input": build_finance_input(row),
        "monitoring_input": build_monitoring_input(row),
        "d6_dependency_input": {
            "status": row.get("d6_dependency_status", "onbekend"),
            "hints": row.get("d6_dependency_hints", []),
            "to_send_to_region": "Send as possible or unresolved D6 dependencies unless validation confirms otherwise.",
        },
        "risk_assessment": build_risk_assessment(row, main_gaps),
        "handoff_to_region": {
            "recommended_wording": recommended_wording(row, main_gaps),
            "attachments_or_links": build_handoff_links(row),
            "not_to_include_in_first_handoff": [
                "unvalidated stakeholder answers",
                "claims that funding, ownership, capacity or D6 dependencies are confirmed",
                "full workbook choice sets unless the recipient needs the detailed validation instrument",
            ],
        },
        "evidence_package": {
            "source_refs": source_refs_for(row),
            "public_evidence": row.get("public_evidence", []),
            "evidence_limitations": [
                "Generated data layers are not public sources.",
                "Public-source signals do not equal confirmed local policy, finance, ownership or capacity.",
                "The 2026-09-15 Almere submission target is a planning assumption, not the national formal deadline.",
            ],
        },
        "traceability": {
            "derived_from_repository_layers": derived_layers_for(row),
            "is_source_claim": False,
            "is_almere_input_model": True,
            "safe_public_use": "Use as internal/regional handoff preparation with explicit gaps; do not cite as source evidence.",
        },
    }


def build_summary(objects: list[dict[str, Any]]) -> dict[str, Any]:
    risk_counts = Counter(item["risk_assessment"]["risk_code"] for item in objects)
    return {
        "object_count": len(objects),
        "required_component_count": sum(1 for item in objects if item["required_in_workagenda"]),
        "concept_handoff_ready_count": sum(
            1 for item in objects if item["almere_submission"]["concept_handoff_ready"]
        ),
        "confirmed_position_ready_count": sum(
            1 for item in objects if item["almere_submission"]["confirmed_position_ready"]
        ),
        "risk_counts": dict(sorted(risk_counts.items())),
        "formal_workagenda_deadline": "2026-11-15",
        "almere_internal_submission_target": "2026-09-15",
        "status_note": (
            "Objects support concept handoff with visible gaps; they do not make any component a confirmed "
            "Almere position unless confirmed_position_ready is true."
        ),
    }


def build_layer() -> dict[str, Any]:
    matrix = load_json(STATUS_MATRIX)
    tickets = load_json(VALIDATION_TICKETS)
    ticket_lookup = {item["ticket_id"]: item for item in tickets["tickets"]}
    tickets_by_component = tickets["tickets_by_component"]
    objects = [build_object(row, tickets_by_component, ticket_lookup) for row in matrix["rows"]]
    source_layers = SOURCE_LAYERS + VALPREVENTIE_SOURCE_LAYERS
    return {
        "schema_id": "ALMERE-REGIONAL-WORKAGENDA-INPUT-V1",
        "generated_on": date.today().isoformat(),
        "status": "generated_concept_layer",
        "purpose": "Structured Almere input objects for the regional AZWA/D5-D6 workagenda process.",
        "source_layers": source_layers,
        "process_context": build_process_context(),
        "summary": build_summary(objects),
        "objects": objects,
    }


def main() -> None:
    write_json(OUTPUT, build_layer())


if __name__ == "__main__":
    main()
