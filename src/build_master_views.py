from __future__ import annotations

import json
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CLAIMS_DIR = REPO_ROOT / "data" / "extracted" / "claims"
DOCUMENTS_DIR = REPO_ROOT / "data" / "extracted" / "documents"
MUNICIPAL_DIR = REPO_ROOT / "data" / "extracted" / "municipal"

CURRENT_INTERPRETATION_PATH = CLAIMS_DIR / "current_interpretation.json"
CONFLICT_REGISTER_PATH = CLAIMS_DIR / "conflict_register.json"
CLAIMS_MASTER_PATH = CLAIMS_DIR / "claims_master.jsonl"

MASTER_OUTPUT_PATH = CLAIMS_DIR / "d5_d6_master.json"
ALMERE_CURRENT_VIEW_PATH = MUNICIPAL_DIR / "almere_current_view.json"
ALMERE_LOCAL_DECISIONS_PATH = MUNICIPAL_DIR / "almere_local_decisions.json"

MASTER_VIEW_RUN_ID = "phase7_phase8_views_v2"
TODAY = date.today().isoformat()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def dedupe(values: list) -> list:
    seen: set[str] = set()
    ordered: list = []
    for value in values:
        marker = json.dumps(value, sort_keys=True, ensure_ascii=False)
        if marker in seen:
            continue
        seen.add(marker)
        ordered.append(value)
    return ordered


def load_document_map() -> dict[str, dict]:
    document_map: dict[str, dict] = {}
    for path in DOCUMENTS_DIR.glob("*.json"):
        payload = load_json(path)
        metadata = payload["metadata"]
        document_map[metadata["document_id"]] = metadata
    return document_map


def claim_map_from_master() -> dict[str, dict]:
    return {claim["claim_id"]: claim for claim in load_jsonl(CLAIMS_MASTER_PATH)}


def topic_map_from_interpretation() -> dict[str, dict]:
    payload = load_json(CURRENT_INTERPRETATION_PATH)
    return {entry["topic"]: entry for entry in payload["topics"]}


def current_claims_for(topic: str, topic_map: dict[str, dict], claim_map: dict[str, dict]) -> list[dict]:
    topic_entry = topic_map.get(topic, {})
    return [claim_map[claim_id] for claim_id in topic_entry.get("current_claim_ids", [])]


def historical_claims_for(topic: str, topic_map: dict[str, dict], claim_map: dict[str, dict]) -> list[dict]:
    topic_entry = topic_map.get(topic, {})
    return [claim_map[claim_id] for claim_id in topic_entry.get("historical_claim_ids", [])]


def source_documents_for_claims(claims: list[dict], document_map: dict[str, dict]) -> list[dict]:
    documents: list[dict] = []
    seen: set[str] = set()
    for claim in claims:
        document_id = claim["source_document_id"]
        if document_id in seen:
            continue
        seen.add(document_id)
        metadata = document_map[document_id]
        documents.append(
            {
                "document_id": document_id,
                "title": metadata["title"],
                "jurisdiction_level": metadata["jurisdiction_level"],
                "document_type": metadata["document_type"],
                "document_status": metadata["status"],
            }
        )
    return documents


def scope_for_claims(claims: list[dict]) -> str:
    jurisdictions = dedupe([claim["jurisdiction_level"] for claim in claims])
    if not jurisdictions:
        return "none"
    if len(jurisdictions) == 1:
        return jurisdictions[0]
    return "mixed"


def statements_for_claims(claims: list[dict]) -> list[str]:
    return [claim["statement"] for claim in claims]


def topic_bundle(topic: str, topic_map: dict[str, dict], claim_map: dict[str, dict], document_map: dict[str, dict]) -> dict:
    topic_entry = topic_map.get(topic)
    if topic_entry is None:
        return {
            "topic": topic,
            "summary": "Topic not present in the current interpretation output.",
            "claim_ids": [],
            "historical_claim_ids": [],
            "statements": [],
            "source_documents": [],
            "scope": "none",
            "confidence": 0.0,
            "needs_human_review": True,
        }

    current_claims = current_claims_for(topic, topic_map, claim_map)
    historical_claims = historical_claims_for(topic, topic_map, claim_map)
    return {
        "topic": topic,
        "summary": topic_entry["interpretation_summary"],
        "claim_ids": topic_entry["current_claim_ids"],
        "historical_claim_ids": topic_entry["historical_claim_ids"],
        "statements": statements_for_claims(current_claims),
        "source_documents": source_documents_for_claims(current_claims or historical_claims, document_map),
        "scope": scope_for_claims(current_claims),
        "confidence": topic_entry["confidence"],
        "needs_human_review": topic_entry["needs_human_review"],
    }


def flatten_claim_ids(topics: list[str], topic_map: dict[str, dict], include_historical: bool = False) -> list[str]:
    claim_ids: list[str] = []
    for topic in topics:
        topic_entry = topic_map.get(topic, {})
        claim_ids.extend(topic_entry.get("current_claim_ids", []))
        if include_historical:
            claim_ids.extend(topic_entry.get("historical_claim_ids", []))
    return dedupe(claim_ids)


def contains_document_prefix(claims: list[dict], prefix: str) -> bool:
    return any(claim["source_document_id"].startswith(prefix) for claim in claims)


def keyword_items(claims: list[dict], candidates: list[str]) -> list[str]:
    corpus = " ".join(claim["statement"].lower() for claim in claims)
    return [candidate for candidate in candidates if candidate.lower() in corpus]


def doc_refs_for_prefix(prefix: str, relevant_topics: list[str], topic_map: dict[str, dict], claim_map: dict[str, dict], document_map: dict[str, dict]) -> list[dict]:
    by_document: dict[str, set[str]] = {}
    for topic in relevant_topics:
        for claim in current_claims_for(topic, topic_map, claim_map):
            document_id = claim["source_document_id"]
            if not document_id.startswith(prefix):
                continue
            by_document.setdefault(document_id, set()).add(topic)

    refs: list[dict] = []
    for document_id in sorted(by_document):
        metadata = document_map[document_id]
        refs.append(
            {
                "document_id": document_id,
                "title": metadata["title"],
                "document_type": metadata["document_type"],
                "relevant_topics": sorted(by_document[document_id]),
            }
        )
    return refs


def unresolved_conflicts(conflict_register: dict) -> list[dict]:
    entries: list[dict] = []
    for conflict in conflict_register["conflicts"]:
        if conflict["resolution_status"] == "resolved":
            continue
        entries.append(
            {
                "conflict_id": conflict["conflict_id"],
                "topic": conflict["topic"],
                "conflict_type": conflict["conflict_type"],
                "resolution_status": conflict["resolution_status"],
                "recommended_resolution_rule": conflict["recommended_resolution_rule"],
                "notes": conflict["notes"],
            }
        )
    return entries


def obsolete_items(topic_map: dict[str, dict]) -> list[dict]:
    prefixes = ("d5.", "d6.", "finance.", "monitoring.", "timeline.", "municipal.")
    items: list[dict] = []
    for topic, entry in topic_map.items():
        if not topic.startswith(prefixes):
            continue
        if not entry["historical_claim_ids"] and not entry["superseded_claim_ids"]:
            continue
        if entry["current_claim_ids"]:
            note = "Current wording exists; older or draft wording remains preserved only for traceability."
        else:
            note = "Only historical wording is currently preserved for this topic."
        items.append(
            {
                "topic": topic,
                "historical_claim_ids": entry["historical_claim_ids"],
                "superseded_claim_ids": entry["superseded_claim_ids"],
                "note": note,
            }
        )
    return items


def uncertain_items(topic_map: dict[str, dict], document_map: dict[str, dict], claim_map: dict[str, dict]) -> list[dict]:
    items: list[dict] = []
    for topic, entry in topic_map.items():
        if not entry["needs_human_review"]:
            continue
        claims = current_claims_for(topic, topic_map, claim_map)
        items.append(
            {
                "topic": topic,
                "summary": entry["interpretation_summary"],
                "claim_ids": entry["current_claim_ids"],
                "source_documents": source_documents_for_claims(claims, document_map),
                "reason": "Current interpretation relies on contextual or lower-authority evidence and should be reviewed before firm local use.",
            }
        )
    return items


def build_d5_master(topic_map: dict[str, dict], claim_map: dict[str, dict], document_map: dict[str, dict]) -> dict:
    definition_claims = current_claims_for("d5.definition", topic_map, claim_map)
    underbouwde_claims = current_claims_for("d5.basisfunctionaliteiten_onderbouwd", topic_map, claim_map)
    ontwikkelagenda_claims = current_claims_for("d5.ontwikkelagenda", topic_map, claim_map)

    leefgebieden = []
    if definition_claims:
        leefgebieden = [
            "kansrijk opgroeien",
            "gezonde leefstijl",
            "mentale gezondheid",
            "vitaal ouder worden",
            "gezondheidsachterstanden verminderen",
        ]

    return {
        "definition": topic_bundle("d5.definition", topic_map, claim_map, document_map),
        "leefgebieden": {
            "items": leefgebieden,
            "source_claim_ids": flatten_claim_ids(["d5.definition"], topic_map),
            "note": "Derived from the signed AZWA D5 definition claim.",
        },
        "basisfunctionaliteiten_onderbouwd": {
            **topic_bundle("d5.basisfunctionaliteiten_onderbouwd", topic_map, claim_map, document_map),
            "known_items": keyword_items(
                underbouwde_claims + ontwikkelagenda_claims,
                ["sociaal verwijzen", "valpreventie"],
            ),
        },
        "ontwikkelagenda_1": {
            **topic_bundle("d5.ontwikkelagenda", topic_map, claim_map, document_map),
            "known_items": [],
            "coverage_note": (
                "The current corpus confirms that a development agenda exists, but it does not yet enumerate the specific ontwikkelagenda 1 items individually."
            ),
            "needs_human_review": True,
        },
        "ontwikkelagenda_2": {
            **topic_bundle("d5.ontwikkelagenda", topic_map, claim_map, document_map),
            "known_items": [],
            "coverage_note": (
                "The current corpus does not yet split named items between ontwikkelagenda 1 and deel 2, so this section stays intentionally incomplete."
            ),
            "needs_human_review": True,
        },
        "implementation_requirements": [
            topic_bundle("d5.regional_workagenda", topic_map, claim_map, document_map),
            topic_bundle("d5.cross_domain_collaboration", topic_map, claim_map, document_map),
            topic_bundle("d5.mentale_gezondheidsnetwerken", topic_map, claim_map, document_map),
            topic_bundle("d5.health_first_shift", topic_map, claim_map, document_map),
        ],
    }


def build_d6_master(topic_map: dict[str, dict], claim_map: dict[str, dict], document_map: dict[str, dict]) -> dict:
    d6_claims = current_claims_for("d6.basisinfrastructuur", topic_map, claim_map)
    infra_claims = current_claims_for("d6.digital_and_operational_infrastructure", topic_map, claim_map)
    basis_items = keyword_items(
        d6_claims,
        [
            "inloopvoorzieningen sociaal en gezond",
            "local teams",
            "burgerinitiatieven",
            "healthy-school work",
            "GGD coordination",
        ],
    )
    digital_items = keyword_items(
        infra_claims,
        [
            "RTP Almere",
            "RSO",
            "data infrastructure",
            "Monitoring@home",
            "shared information picture",
        ],
    )

    return {
        "definition": topic_bundle("d6.basisinfrastructuur", topic_map, claim_map, document_map),
        "basisinfrastructuur_items": {
            "national_items": basis_items,
            "regional_and_local_items": digital_items,
            "source_claim_ids": flatten_claim_ids(
                ["d6.basisinfrastructuur", "d6.digital_and_operational_infrastructure"],
                topic_map,
            ),
            "needs_human_review": topic_map["d6.digital_and_operational_infrastructure"]["needs_human_review"],
        },
        "governance_requirements": [
            topic_bundle("d6.local_teams", topic_map, claim_map, document_map),
            topic_bundle("governance.regional_coordination", topic_map, claim_map, document_map),
            topic_bundle("municipal.role_allocation", topic_map, claim_map, document_map),
        ],
        "infrastructure_requirements": [
            topic_bundle("d6.digital_and_operational_infrastructure", topic_map, claim_map, document_map),
            topic_bundle("municipal.implementation_translation", topic_map, claim_map, document_map),
        ],
    }


def build_open_questions(topic_map: dict[str, dict]) -> list[dict]:
    return [
        {
            "question_id": "oq_ontwikkelagenda_split",
            "question": "Which specific measures belong to ontwikkelagenda 1 and which belong to deel 2 within the signed D5 framework?",
            "derived_from_topics": ["d5.ontwikkelagenda"],
            "supporting_claim_ids": flatten_claim_ids(["d5.ontwikkelagenda"], topic_map, include_historical=True),
        },
        {
            "question_id": "oq_funding_instrument_choice",
            "question": "Which exact municipal funding instrument was ultimately chosen in the VNG/fund-manager/VWS process for D5/D6 middelen?",
            "derived_from_topics": ["finance.d5_d6.funding_instrument", "finance.d5_d6.municipal_funding"],
            "supporting_claim_ids": flatten_claim_ids(
                ["finance.d5_d6.funding_instrument", "finance.d5_d6.municipal_funding"],
                topic_map,
            ),
        },
        {
            "question_id": "oq_almere_local_teams",
            "question": "How will Almere concretely satisfy the national D6 local-team and hechte-wijkverband requirement in its own governance model?",
            "derived_from_topics": ["d6.local_teams", "municipal.local_structure"],
            "supporting_claim_ids": flatten_claim_ids(
                ["d6.local_teams", "municipal.local_structure"],
                topic_map,
                include_historical=True,
            ),
        },
        {
            "question_id": "oq_monitoring_alignment",
            "question": "How should Almere align its local learning and dashboard work with the national 2028 update cycle and the Flevoland monitoring plan?",
            "derived_from_topics": ["monitoring.framework", "monitoring.local_learning", "monitoring.update_2028"],
            "supporting_claim_ids": flatten_claim_ids(
                ["monitoring.framework", "monitoring.local_learning", "monitoring.update_2028"],
                topic_map,
                include_historical=True,
            ),
        },
    ]


def almere_item(item_id: str, topic: str, topic_map: dict[str, dict], claim_map: dict[str, dict], document_map: dict[str, dict]) -> dict:
    payload = topic_bundle(topic, topic_map, claim_map, document_map)
    return {
        "item_id": item_id,
        "topic": topic,
        "summary": payload["summary"],
        "claim_ids": payload["claim_ids"],
        "source_documents": payload["source_documents"],
        "scope": payload["scope"],
        "confidence": payload["confidence"],
        "needs_human_review": payload["needs_human_review"],
    }


def build_local_gaps(topic_map: dict[str, dict], claim_map: dict[str, dict]) -> list[dict]:
    gaps: list[dict] = []
    d5_workagenda_claims = current_claims_for("d5.regional_workagenda", topic_map, claim_map)
    if d5_workagenda_claims and not contains_document_prefix(d5_workagenda_claims, "mun_"):
        gaps.append(
            {
                "gap_id": "gap_almere_d5_workagenda_mapping",
                "summary": "No extracted Almere-specific workagenda claim yet maps the national D5 basisfunctionaliteiten to concrete local target groups, sequencing, or intervention choices.",
                "based_on_topics": ["d5.basisfunctionaliteiten_onderbouwd", "d5.regional_workagenda", "municipal.almere_initiatives"],
                "supporting_claim_ids": flatten_claim_ids(
                    ["d5.basisfunctionaliteiten_onderbouwd", "d5.regional_workagenda", "municipal.almere_initiatives"],
                    topic_map,
                ),
            }
        )

    if topic_map["d6.local_teams"]["current_claim_ids"] and not topic_map["municipal.local_structure"]["current_claim_ids"]:
        gaps.append(
            {
                "gap_id": "gap_almere_d6_local_structure",
                "summary": "No extracted current Almere claim yet confirms how the city will meet the national D6 local-team and hechte-wijkverband structure requirement.",
                "based_on_topics": ["d6.local_teams", "municipal.local_structure", "municipal.implementation_translation"],
                "supporting_claim_ids": flatten_claim_ids(
                    ["d6.local_teams", "municipal.local_structure", "municipal.implementation_translation"],
                    topic_map,
                    include_historical=True,
                ),
            }
        )

    gaps.append(
        {
            "gap_id": "gap_almere_funding_choices",
            "summary": "National funding rules and the start package are current, but no local decision file yet assigns owners, budgets, or priority use of those middelen in Almere.",
            "based_on_topics": ["finance.d5_d6.funding_instrument", "finance.d5_d6.municipal_funding"],
            "supporting_claim_ids": flatten_claim_ids(
                ["finance.d5_d6.funding_instrument", "finance.d5_d6.municipal_funding"],
                topic_map,
            ),
        }
    )

    gaps.append(
        {
            "gap_id": "gap_almere_monitoring_alignment",
            "summary": "The current claim set does not yet show an explicit Almere-level alignment between local monitoring, the Flevoland dashboard approach, and the national 2028 update cycle.",
            "based_on_topics": ["monitoring.framework", "monitoring.local_learning", "monitoring.update_2028"],
            "supporting_claim_ids": flatten_claim_ids(
                ["monitoring.framework", "monitoring.local_learning", "monitoring.update_2028"],
                topic_map,
                include_historical=True,
            ),
        }
    )

    return gaps


def build_local_dependencies(topic_map: dict[str, dict]) -> list[dict]:
    return [
        {
            "dependency_id": "dep_regional_digital_infrastructure",
            "dependency_type": "regional_infrastructure",
            "blocking_level": "high",
            "summary": "Almere's local D6 infrastructure depends on the Flevoland regional collaboration organization, shared data-availability vision, and information architecture track.",
            "based_on_topics": ["d6.digital_and_operational_infrastructure"],
            "supporting_claim_ids": flatten_claim_ids(["d6.digital_and_operational_infrastructure"], topic_map),
        },
        {
            "dependency_id": "dep_national_funding_channel",
            "dependency_type": "national_funding",
            "blocking_level": "high",
            "summary": "Almere depends on the national VNG/fund-manager/VWS process that selects the final funding instrument and start-package route for D5/D6 middelen.",
            "based_on_topics": ["finance.d5_d6.funding_instrument", "finance.d5_d6.municipal_funding"],
            "supporting_claim_ids": flatten_claim_ids(
                ["finance.d5_d6.funding_instrument", "finance.d5_d6.municipal_funding"],
                topic_map,
            ),
        },
        {
            "dependency_id": "dep_regional_role_allocation",
            "dependency_type": "regional_governance",
            "blocking_level": "medium",
            "summary": "Almere depends on clearer role allocation between municipality, social domain, insurers, providers, and the Flevoland governance structure.",
            "based_on_topics": ["municipal.role_allocation", "governance.regional_coordination"],
            "supporting_claim_ids": flatten_claim_ids(
                ["municipal.role_allocation", "governance.regional_coordination"],
                topic_map,
            ),
        },
        {
            "dependency_id": "dep_national_update_cycle",
            "dependency_type": "national_governance_cycle",
            "blocking_level": "medium",
            "summary": "Almere depends on the national D5/D6 governance, mid-term review, and 2028 content-update cycle when sequencing its own implementation.",
            "based_on_topics": ["timeline.d5_d6_implementation", "monitoring.mid_term_review", "monitoring.update_2028"],
            "supporting_claim_ids": flatten_claim_ids(
                ["timeline.d5_d6_implementation", "monitoring.mid_term_review", "monitoring.update_2028"],
                topic_map,
            ),
        },
    ]


def build_items_requiring_political_choice(topic_map: dict[str, dict]) -> list[dict]:
    return [
        {
            "choice_id": "choice_d5_prioritization",
            "choice_type": "sequencing",
            "question": "Which D5 interventions should Almere prioritize first in its local workagenda and for which target groups?",
            "based_on_topics": ["d5.basisfunctionaliteiten_onderbouwd", "d5.regional_workagenda", "municipal.almere_initiatives"],
            "supporting_claim_ids": flatten_claim_ids(
                ["d5.basisfunctionaliteiten_onderbouwd", "d5.regional_workagenda", "municipal.almere_initiatives"],
                topic_map,
            ),
        },
        {
            "choice_id": "choice_d6_governance_model",
            "choice_type": "governance",
            "question": "How should Almere organize ownership, coordination, and accountability for D6 local teams and wijkverbanden?",
            "based_on_topics": ["d6.local_teams", "municipal.role_allocation", "governance.local_coalition"],
            "supporting_claim_ids": flatten_claim_ids(
                ["d6.local_teams", "municipal.role_allocation", "governance.local_coalition"],
                topic_map,
            ),
        },
        {
            "choice_id": "choice_budget_distribution",
            "choice_type": "budget",
            "question": "How should Almere distribute available D5/D6-related means between direct interventions, enabling infrastructure, and broader prevention-first work?",
            "based_on_topics": ["finance.d5_d6.municipal_funding", "finance.local_alignment_goal", "municipal.almere_initiatives"],
            "supporting_claim_ids": flatten_claim_ids(
                ["finance.d5_d6.municipal_funding", "finance.local_alignment_goal", "municipal.almere_initiatives"],
                topic_map,
            ),
        },
        {
            "choice_id": "choice_monitoring_package",
            "choice_type": "monitoring",
            "question": "Which KPI set and review rhythm should Almere use to align local monitoring with the Flevoland dashboard and the national 2028 update cycle?",
            "based_on_topics": ["monitoring.framework", "monitoring.local_learning", "monitoring.update_2028"],
            "supporting_claim_ids": flatten_claim_ids(
                ["monitoring.framework", "monitoring.local_learning", "monitoring.update_2028"],
                topic_map,
            ),
        },
    ]


def build_master_payload(
    topic_map: dict[str, dict],
    claim_map: dict[str, dict],
    document_map: dict[str, dict],
    conflict_register: dict,
    current_interpretation: dict,
) -> dict:
    return {
        "view_run_id": MASTER_VIEW_RUN_ID,
        "generated_on": TODAY,
        "as_of_date": current_interpretation["as_of_date"],
        "source_interpretation_run_id": current_interpretation["interpretation_run_id"],
        "source_claim_extraction_runs": current_interpretation["source_claim_extraction_runs"],
        "d5": build_d5_master(topic_map, claim_map, document_map),
        "d6": build_d6_master(topic_map, claim_map, document_map),
        "finance": {
            "macro_framework": topic_bundle("finance.azwa_macro_framework", topic_map, claim_map, document_map),
            "funding_instrument": topic_bundle("finance.d5_d6.funding_instrument", topic_map, claim_map, document_map),
            "municipal_funding": topic_bundle("finance.d5_d6.municipal_funding", topic_map, claim_map, document_map),
            "regional_funding_context": topic_bundle("finance.regional_funding_path", topic_map, claim_map, document_map),
            "local_finance_signal": topic_bundle("finance.local_alignment_goal", topic_map, claim_map, document_map),
        },
        "timeline": {
            "national_milestones": topic_bundle("timeline.d5_d6_implementation", topic_map, claim_map, document_map),
            "rollout_2030": topic_bundle("timeline.rollout_2030", topic_map, claim_map, document_map),
            "financing_horizon": topic_bundle("timeline.d5_d6_financing_horizon", topic_map, claim_map, document_map),
            "regional_transformation_timing": topic_bundle("timeline.flevoland_transformatieagenda", topic_map, claim_map, document_map),
            "almere_local_horizon": topic_bundle("timeline.almere_2029", topic_map, claim_map, document_map),
        },
        "open_questions": build_open_questions(topic_map),
        "unresolved_conflicts": unresolved_conflicts(conflict_register),
    }


def build_almere_current_view_payload(
    topic_map: dict[str, dict],
    claim_map: dict[str, dict],
    document_map: dict[str, dict],
    conflict_register: dict,
    current_interpretation: dict,
) -> dict:
    relevant_topics = [
        "d5.definition",
        "d5.basisfunctionaliteiten_onderbouwd",
        "d5.ontwikkelagenda",
        "d5.regional_workagenda",
        "d5.cross_domain_collaboration",
        "d5.mentale_gezondheidsnetwerken",
        "d5.health_first_shift",
        "d6.basisinfrastructuur",
        "d6.local_teams",
        "d6.digital_and_operational_infrastructure",
        "municipal.implementation_translation",
        "municipal.role_allocation",
        "municipal.almere_context",
        "municipal.almere_initiatives",
        "finance.d5_d6.funding_instrument",
        "finance.d5_d6.municipal_funding",
        "finance.local_alignment_goal",
        "finance.regional_funding_path",
        "monitoring.framework",
        "monitoring.local_learning",
        "monitoring.update_2028",
        "timeline.almere_2029",
        "timeline.rollout_2030",
    ]

    return {
        "municipality_id": "GM0034",
        "municipality_name": "Almere",
        "view_run_id": MASTER_VIEW_RUN_ID,
        "generated_on": TODAY,
        "as_of_date": current_interpretation["as_of_date"],
        "source_interpretation_run_id": current_interpretation["interpretation_run_id"],
        "applicable_d5_items": [
            almere_item("almere_d5_definition", "d5.definition", topic_map, claim_map, document_map),
            almere_item("almere_d5_underbouwd", "d5.basisfunctionaliteiten_onderbouwd", topic_map, claim_map, document_map),
            almere_item("almere_d5_workagenda", "d5.regional_workagenda", topic_map, claim_map, document_map),
            almere_item("almere_d5_collaboration", "d5.cross_domain_collaboration", topic_map, claim_map, document_map),
            almere_item("almere_d5_mental_health", "d5.mentale_gezondheidsnetwerken", topic_map, claim_map, document_map),
            almere_item("almere_d5_health_first", "d5.health_first_shift", topic_map, claim_map, document_map),
        ],
        "applicable_d6_items": [
            almere_item("almere_d6_basis", "d6.basisinfrastructuur", topic_map, claim_map, document_map),
            almere_item("almere_d6_local_teams", "d6.local_teams", topic_map, claim_map, document_map),
            almere_item("almere_d6_digital_infra", "d6.digital_and_operational_infrastructure", topic_map, claim_map, document_map),
            almere_item("almere_d6_translation", "municipal.implementation_translation", topic_map, claim_map, document_map),
        ],
        "local_gaps": build_local_gaps(topic_map, claim_map),
        "local_dependencies": build_local_dependencies(topic_map),
        "relevant_regional_documents": doc_refs_for_prefix("reg_", relevant_topics, topic_map, claim_map, document_map),
        "relevant_municipal_documents": doc_refs_for_prefix("mun_", relevant_topics, topic_map, claim_map, document_map),
        "uncertain_items": uncertain_items(topic_map, document_map, claim_map),
        "obsolete_items": obsolete_items(topic_map),
        "unresolved_conflicts": unresolved_conflicts(conflict_register),
        "items_requiring_political_choice": build_items_requiring_political_choice(topic_map),
    }


def initialize_local_decisions_file() -> None:
    if ALMERE_LOCAL_DECISIONS_PATH.exists():
        print(f"Kept existing {ALMERE_LOCAL_DECISIONS_PATH.relative_to(REPO_ROOT).as_posix()}")
        return

    payload = {
        "municipality_id": "GM0034",
        "municipality_name": "Almere",
        "created_on": TODAY,
        "note": "Reserved for human-entered local policy choices. This file should not be overwritten automatically once decisions are added.",
        "decision_count": 0,
        "decisions": [],
    }
    ALMERE_LOCAL_DECISIONS_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {ALMERE_LOCAL_DECISIONS_PATH.relative_to(REPO_ROOT).as_posix()}")


def main() -> None:
    current_interpretation = load_json(CURRENT_INTERPRETATION_PATH)
    conflict_register = load_json(CONFLICT_REGISTER_PATH)
    topic_map = topic_map_from_interpretation()
    claim_map = claim_map_from_master()
    document_map = load_document_map()

    master_payload = build_master_payload(
        topic_map,
        claim_map,
        document_map,
        conflict_register,
        current_interpretation,
    )
    almere_current_view = build_almere_current_view_payload(
        topic_map,
        claim_map,
        document_map,
        conflict_register,
        current_interpretation,
    )

    CLAIMS_DIR.mkdir(parents=True, exist_ok=True)
    MUNICIPAL_DIR.mkdir(parents=True, exist_ok=True)

    MASTER_OUTPUT_PATH.write_text(json.dumps(master_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    ALMERE_CURRENT_VIEW_PATH.write_text(
        json.dumps(almere_current_view, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {MASTER_OUTPUT_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"Wrote {ALMERE_CURRENT_VIEW_PATH.relative_to(REPO_ROOT).as_posix()}")
    initialize_local_decisions_file()


if __name__ == "__main__":
    main()
