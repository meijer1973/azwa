from __future__ import annotations

import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
EXTRACTED_DIR = REPO_ROOT / "data" / "extracted"
CLAIMS_MASTER_PATH = EXTRACTED_DIR / "claims" / "claims_master.jsonl"
REGIONAL_ROLES_PATH = REPO_ROOT / "data" / "curated" / "regional_roles_and_splits_almere_flevoland.json"
NULMETING_PATH = EXTRACTED_DIR / "workagenda_nulmeting_capacity.json"
OUTPUT_PATH = EXTRACTED_DIR / "d6_governance_collaboration.json"


D6_DIMENSIONS = [
    {
        "dimension_id": "d6_basisinfrastructuur",
        "label": "D6 sociale en gezonde basisinfrastructuur",
        "public_question": "Welke publieke bronnen maken duidelijk wat lokaal of regionaal onder de D6-basisinfrastructuur valt?",
        "topics": ["d6.basisinfrastructuur"],
        "local_validation_fields": [
            "lokale afbakening basisinfrastructuur",
            "relatie met sociale basis en GALA",
            "welke onderdelen al bestaan",
            "welke onderdelen nieuw of uit te breiden zijn",
        ],
    },
    {
        "dimension_id": "local_teams_and_wijkverbanden",
        "label": "Lokale teams en hechte wijkverbanden",
        "public_question": "Wie is aanspreekbaar voor lokale teams, wijkverbanden en verbinding met de eerste lijn?",
        "topics": ["d6.local_teams"],
        "local_validation_fields": [
            "welke lokale teams tellen mee",
            "wijkverbanden per gebied",
            "aanspreekpunt per wijk",
            "verbinding met huisartsen/eerstelijn",
        ],
    },
    {
        "dimension_id": "inloopvoorzieningen_en_steunpunten",
        "label": "Inloopvoorzieningen en laagdrempelige steun",
        "public_question": "Welke bronnen koppelen inloop, steunpunten, sociaal verwijzen of ontmoeting aan D6/D5?",
        "topics": ["d6.basisinfrastructuur", "d5.basisfunctionaliteiten_onderbouwd"],
        "local_validation_fields": [
            "bestaande inloopvoorzieningen",
            "laagdrempelige steunpunten",
            "openingstijden en toegankelijkheid",
            "uitvoerder en financier",
        ],
    },
    {
        "dimension_id": "regional_coordination",
        "label": "Regionale coordinatie en schaal",
        "public_question": "Welke bron onderscheidt IZA/AZWA-regio, GGD-regio, mandaatgemeente en uitvoeringsschaal?",
        "topics": ["governance.regional_coordination", "municipal.role_allocation"],
        "local_validation_fields": [
            "mandaatgemeente-besluit",
            "regionale tafel of bestuurlijke coalitie",
            "GGD-regio versus IZA/AZWA-regio",
            "zorgverzekeraar/zorgkantoorrol",
        ],
    },
    {
        "dimension_id": "monitoring_and_learning",
        "label": "Monitoring, leren en verantwoording",
        "public_question": "Wie monitort, leert en verantwoordt de samenwerking rond D6?",
        "topics": ["monitoring.other", "governance.regional_coordination"],
        "local_validation_fields": [
            "monitoringset",
            "wie rapporteert",
            "frequentie",
            "waar besluiten of bijsturing landen",
        ],
    },
]


RESPONSIBILITY_SLOTS = [
    {
        "slot_id": "decision",
        "label": "Besluitvorming",
        "public_question": "Welke publieke bron wijst aan waar het formele besluit of mandaat ligt?",
    },
    {
        "slot_id": "coordination",
        "label": "Coordinatie",
        "public_question": "Welke publieke bron wijst een coordinerende tafel, organisatie of rol aan?",
    },
    {
        "slot_id": "execution",
        "label": "Uitvoering",
        "public_question": "Welke publieke bron maakt duidelijk wie het onderdeel feitelijk uitvoert?",
    },
    {
        "slot_id": "finance",
        "label": "Financiering",
        "public_question": "Welke publieke bron koppelt middelen, opdracht of bekostiging aan dit onderdeel?",
    },
    {
        "slot_id": "monitoring",
        "label": "Monitoring en verantwoording",
        "public_question": "Welke publieke bron maakt monitoring, leren of verantwoording concreet?",
    },
]


DIMENSION_SLOT_PREFILL = {
    "d6_basisinfrastructuur": {
        "decision": ["gemeente_almere"],
        "coordination": ["gemeente_almere", "welzijn_sociaal_werk"],
        "execution": ["welzijn_sociaal_werk", "ggd_flevoland"],
        "finance": ["gemeente_almere", "zorgverzekeraar"],
        "monitoring": ["gemeente_almere", "ggd_flevoland"],
    },
    "local_teams_and_wijkverbanden": {
        "decision": ["gemeente_almere"],
        "coordination": ["gemeente_almere", "huisartsen_eerstelijn", "welzijn_sociaal_werk"],
        "execution": ["welzijn_sociaal_werk", "huisartsen_eerstelijn"],
        "finance": ["gemeente_almere", "zorgverzekeraar"],
        "monitoring": ["gemeente_almere"],
    },
    "inloopvoorzieningen_en_steunpunten": {
        "decision": ["gemeente_almere"],
        "coordination": ["welzijn_sociaal_werk", "gemeente_almere"],
        "execution": ["welzijn_sociaal_werk"],
        "finance": ["gemeente_almere"],
        "monitoring": ["gemeente_almere", "welzijn_sociaal_werk"],
    },
    "regional_coordination": {
        "decision": ["gemeente_almere", "zorgverzekeraar"],
        "coordination": ["zorgzaam_flevoland_flever", "gemeente_almere", "ggd_flevoland"],
        "execution": ["gemeente_almere", "ggd_flevoland", "zorgzaam_flevoland_flever"],
        "finance": ["gemeente_almere", "zorgverzekeraar"],
        "monitoring": ["zorgzaam_flevoland_flever", "ggd_flevoland", "gemeente_almere"],
    },
    "monitoring_and_learning": {
        "decision": ["gemeente_almere"],
        "coordination": ["ggd_flevoland", "zorgzaam_flevoland_flever"],
        "execution": ["ggd_flevoland", "gemeente_almere"],
        "finance": ["gemeente_almere"],
        "monitoring": ["ggd_flevoland", "gemeente_almere", "zorgzaam_flevoland_flever"],
    },
}


ACTOR_ROLES = [
    {
        "actor_id": "gemeente_almere",
        "actor": "Gemeente Almere",
        "public_role": "Lokale gemeente en in externe netwerkgegevens genoemd als mandaatgemeente voor de Flevolandse IZA/AZWA-route.",
        "source_status": "partly_source_backed_needs_local_mandate_validation",
        "validation_needed": ["formeel mandaatbesluit", "lokale eigenaar per D6-onderdeel", "college/raad rol"],
    },
    {
        "actor_id": "ggd_flevoland",
        "actor": "GGD Flevoland",
        "public_role": "Publieke gezondheidsdienst voor GGD-regio Flevoland; natuurlijke schaal voor GGD-uitgevoerde onderdelen.",
        "source_status": "source_backed_for_region_split",
        "validation_needed": ["welke D6-taken GGD uitvoert", "afbakening GGD-regio versus IZA/AZWA-regio"],
    },
    {
        "actor_id": "zorgzaam_flevoland_flever",
        "actor": "Zorgzaam Flevoland / Flever",
        "public_role": "Regionale beweging en ondersteuning vanuit het IZA-regioplan; ZonMw-bron noemt doorontwikkeling van de samenwerkingsstructuur.",
        "source_status": "source_backed_supporting_governance",
        "validation_needed": ["besluitvormende rol versus ondersteunende rol", "wie is aanspreekbaar per werkstroom"],
    },
    {
        "actor_id": "zorgverzekeraar",
        "actor": "Zorgverzekeraar / zorgkantoor",
        "public_role": "Partner in regionale samenwerking en financieringsafspraken; zorgkantoorregio valt niet samen met IZA/AZWA-regio.",
        "source_status": "source_backed_at_regional_split_level",
        "validation_needed": ["contracteerrol", "Zvw-financiering per target", "zorgkantoor versus IZA/AZWA-route"],
    },
    {
        "actor_id": "welzijn_sociaal_werk",
        "actor": "Welzijn en sociaal werk",
        "public_role": "Uitvoeringspartner voor sociale basis, ontmoeting, sociaal verwijzen en laagdrempelige steun.",
        "source_status": "public_sources_indicate_role_but_local_allocation_needed",
        "validation_needed": ["welke organisaties", "capaciteit", "opdracht en budget"],
    },
    {
        "actor_id": "huisartsen_eerstelijn",
        "actor": "Huisartsen en eerstelijn",
        "public_role": "Partner voor sociaal verwijzen, wijkverbanden en verbinding tussen zorg en sociaal domein.",
        "source_status": "public_sources_indicate_role_but_local_allocation_needed",
        "validation_needed": ["praktijknetwerken", "verwijsafspraken", "wijkverbanden"],
    },
]


ACTOR_ROLE_INDEX = {role["actor_id"]: role for role in ACTOR_ROLES}


def validation_status_for_actor(actor_id: str) -> str:
    actor = ACTOR_ROLE_INDEX.get(actor_id, {})
    source_status = actor.get("source_status", "")
    if source_status.startswith("source_backed"):
        return "public_role_source_backed_role_scope_still_needs_target_validation"
    return "public_role_hypothesis_needs_local_validation"


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def load_claims() -> list[dict[str, Any]]:
    if not CLAIMS_MASTER_PATH.exists():
        return []
    claims = []
    for line in CLAIMS_MASTER_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            claims.append(json.loads(line))
    return claims


def relevant_claims_for_topics(claims: list[dict[str, Any]], topics: list[str]) -> list[dict[str, Any]]:
    rows = []
    topic_set = set(topics)
    for claim in claims:
        topic = claim.get("topic")
        if topic in topic_set or (topic or "").startswith("d6.") or "governance" in (topic or ""):
            rows.append(
                {
                    "claim_id": claim.get("claim_id"),
                    "topic": topic,
                    "statement": claim.get("statement"),
                    "source_document_id": claim.get("source_document_id"),
                    "publisher": claim.get("publisher"),
                    "human_review_status": claim.get("human_review_status"),
                    "confidence": claim.get("confidence"),
                }
            )
    return rows


def build_dimension_rows(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for dimension in D6_DIMENSIONS:
        supporting_claims = relevant_claims_for_topics(claims, dimension["topics"])
        source_counts = Counter(claim["source_document_id"] for claim in supporting_claims if claim.get("source_document_id"))
        responsibility_matrix = build_responsibility_matrix(dimension["dimension_id"], supporting_claims)
        decision_questions = build_decision_questions(dimension, responsibility_matrix)
        rows.append(
            {
                **dimension,
                "source_claim_count": len(supporting_claims),
                "top_source_document_ids": [doc_id for doc_id, _count in source_counts.most_common(6)],
                "sample_claims": supporting_claims[:8],
                "public_coverage_status": "public_claims_present_needs_review" if supporting_claims else "public_gap",
                "responsibility_matrix": responsibility_matrix,
                "decision_questions": decision_questions,
                "review_note": "Claims support orientation only; use source passages before writing bestuurlijke text.",
            }
        )
    return rows


def build_responsibility_matrix(dimension_id: str, supporting_claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    topic_counts = Counter(claim.get("topic") for claim in supporting_claims if claim.get("topic"))
    source_document_ids = sorted(
        {claim.get("source_document_id") for claim in supporting_claims if claim.get("source_document_id")}
    )
    prefill = DIMENSION_SLOT_PREFILL.get(dimension_id, {})
    rows = []
    for slot in RESPONSIBILITY_SLOTS:
        candidate_actor_ids = prefill.get(slot["slot_id"], [])
        local_validation_fields = [
            f"{slot['label'].lower()}: bevestig actor, mandaat en bronpassage voor {dimension_id}",
            f"{slot['label'].lower()}: leg vast of dit lokaal, regionaal of gemengd wordt belegd",
        ]
        rows.append(
            {
                **slot,
                "candidate_actor_ids": candidate_actor_ids,
                "candidate_actors": [
                    ACTOR_ROLE_INDEX[actor_id]["actor"]
                    for actor_id in candidate_actor_ids
                    if actor_id in ACTOR_ROLE_INDEX
                ],
                "public_evidence_status": (
                    "public_claims_present_but_role_allocation_needs_validation"
                    if supporting_claims
                    else "public_gap_needs_local_or_new_public_source"
                ),
                "topic_counts": dict(sorted(topic_counts.items())),
                "source_document_ids": source_document_ids[:8],
                "actor_validation_status": {
                    actor_id: validation_status_for_actor(actor_id)
                    for actor_id in candidate_actor_ids
                },
                "local_validation_fields": local_validation_fields,
            }
        )
    return rows


def build_decision_questions(
    dimension: dict[str, Any],
    responsibility_matrix: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    questions = []
    for row in responsibility_matrix:
        candidate_actors = ", ".join(row["candidate_actors"]) if row["candidate_actors"] else "nog niet uit publieke bronnen af te leiden"
        questions.append(
            {
                "question_id": f"{dimension['dimension_id']}.{row['slot_id']}",
                "slot_id": row["slot_id"],
                "question": (
                    f"Wie is voor {dimension['label']} bestuurlijk of operationeel verantwoordelijk voor "
                    f"{row['label'].lower()}?"
                ),
                "public_prefill": candidate_actors,
                "decision_status": "local_validation_or_later_decision_needed",
            }
        )
    return questions


def build_payload() -> dict[str, Any]:
    claims = load_claims()
    regional_roles = load_json(REGIONAL_ROLES_PATH, {})
    nulmeting = load_json(NULMETING_PATH, {})
    dimensions = build_dimension_rows(claims)

    return {
        "layer_run_id": "phase25_4_d6_governance_collaboration_v1",
        "generated_on": date.today().isoformat(),
        "status": "active_sprint_support",
        "sprint": "25.4 D6 governance en samenwerking",
        "purpose": "Make D6 role allocation, scale, collaboration, monitoring, and remaining validation questions explicit from the public corpus.",
        "public_source_boundary": "Use public corpus and curated role/split guardrails first; non-public role allocation remains local validation or decision work.",
        "inputs": [
            "data/extracted/claims/claims_master.jsonl",
            "data/curated/regional_roles_and_splits_almere_flevoland.json",
            "data/extracted/workagenda_nulmeting_capacity.json",
        ],
        "summary": {
            "dimension_count": len(dimensions),
            "actor_role_count": len(ACTOR_ROLES),
            "responsibility_slot_count": len(RESPONSIBILITY_SLOTS),
            "responsibility_assignment_count": sum(
                len(row.get("responsibility_matrix", [])) for row in dimensions
            ),
            "decision_question_count": sum(len(row.get("decision_questions", [])) for row in dimensions),
            "dimensions_with_public_claims": sum(1 for row in dimensions if row["source_claim_count"] > 0),
            "local_validation_field_count": sum(len(row["local_validation_fields"]) for row in dimensions)
            + sum(len(row["validation_needed"]) for row in ACTOR_ROLES)
            + sum(
                len(slot.get("local_validation_fields", []))
                for row in dimensions
                for slot in row.get("responsibility_matrix", [])
            ),
            "nulmeting_target_count": (nulmeting.get("summary") or {}).get("target_count"),
        },
        "regional_guardrail": {
            "editorial_rule": regional_roles.get("editorial_rule"),
            "regional_splits": regional_roles.get("regional_splits", []),
            "regional_roles": regional_roles.get("regional_roles", []),
        },
        "responsibility_slots": RESPONSIBILITY_SLOTS,
        "actor_roles": ACTOR_ROLES,
        "dimensions": dimensions,
        "local_validation_workflow": [
            {
                "step": "publieke prefill controleren",
                "owner_hint": "research/beleid",
                "output": "bronpassages per D6-dimensie en verantwoordelijkheidsslot bevestigen of afwijzen",
            },
            {
                "step": "lokale medewerkerinvulling",
                "owner_hint": "gemeente Almere en relevante regionale partners",
                "output": "lokale teams, wijkverbanden, inloopvoorzieningen, uitvoerders en aanspreekpunten invullen",
            },
            {
                "step": "besluitvragen escaleren",
                "owner_hint": "bestuurlijke lijn",
                "output": "mandaat, budget, monitoring, schaalkeuze en eigenaarschap vaststellen waar bronnen geen antwoord geven",
            },
        ],
        "carry_forward": [
            "Validate formal Almere mandaatgemeente documentation before using as bestuurlijke fact beyond narrow public listings.",
            "Ask local staff which local teams, wijkverbanden, inloopvoorzieningen and social-basis partners should count for D6.",
            "Separate GGD-regio, IZA/AZWA-regio, zorgkantoorregio and local execution in all outward-facing material.",
            "Escalate unresolved ownership, budget, monitoring and scale choices as decision questions after local validation.",
        ],
    }


def main() -> None:
    payload = build_payload()
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"Dimensions with public claims: {payload['summary']['dimensions_with_public_claims']}")


if __name__ == "__main__":
    main()
