from __future__ import annotations

import json
import re
import unicodedata
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCUMENT_DIR = REPO_ROOT / "data" / "extracted" / "documents"
AUTHORITY_RULES_PATH = REPO_ROOT / "config" / "authority_rules.json"
CLAIM_SCHEMA_PATH = REPO_ROOT / "data" / "schemas" / "claim.schema.json"
OUTPUT_DIR = REPO_ROOT / "data" / "extracted" / "claims"

CLAIM_EXTRACTION_RUN_ID = "phase4_top5_claims_v1"
TOP5_DOCUMENT_IDS = [
    "nat_azwa_2025_definitief",
    "nat_azwa_2025_onderhandelaarsakkoord",
    "nat_azwa_2026_cw31_kader_d5_d6",
    "reg_flevoland_2023_regioplan_iza",
    "mun_almere_pga_transformatieplan",
]


def normalize_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip().lower()
    text = unicodedata.normalize("NFKD", text)
    return text.encode("ascii", "ignore").decode("ascii")


def claim_id_for(statement_id: str) -> str:
    return f"clm__{statement_id}"


def unique_preserving_order(values: list) -> list:
    seen = set()
    ordered = []
    for value in values:
        marker = json.dumps(value, sort_keys=True, ensure_ascii=False)
        if marker in seen:
            continue
        seen.add(marker)
        ordered.append(value)
    return ordered


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_document(document_id: str) -> dict:
    return load_json(DOCUMENT_DIR / f"{document_id}.json")


def load_authority_model() -> tuple[dict[str, str], dict[str, dict]]:
    payload = load_json(AUTHORITY_RULES_PATH)
    return payload["document_type_to_instrument_type"], payload["instrument_types"]


def load_allowed_relation_types() -> set[str]:
    schema = load_json(CLAIM_SCHEMA_PATH)
    return set(schema["properties"]["relations"]["items"]["properties"]["type"]["enum"])


def applies_to_for(document_id: str) -> list[str]:
    if document_id.startswith("nat_"):
        return ["Netherlands", "all_regions", "all_municipalities"]
    if document_id.startswith("reg_"):
        return ["Flevoland", "Almere"]
    return ["Almere"]


def validity_status_for(document_id: str, source_statement_type: str) -> str:
    if document_id == "nat_azwa_2025_onderhandelaarsakkoord":
        return "historical"
    if document_id.startswith(("reg_", "mun_")) or source_statement_type == "contextual_relevance":
        return "contextual_active"
    return "active"


def confidence_for(jurisdiction_level: str, source_statement_type: str, topic: str) -> float:
    if source_statement_type == "contextual_relevance":
        base = 0.68
    elif jurisdiction_level == "national":
        base = 0.93
    elif jurisdiction_level == "regional":
        base = 0.84
    else:
        base = 0.82

    if topic.endswith(".other"):
        base -= 0.18
    elif topic.startswith(("d5.definition", "d6.basisinfrastructuur", "finance.d5_d6", "timeline.", "monitoring.")):
        base += 0.02

    return round(max(0.3, min(base, 0.98)), 2)


def human_review_status_for(source_statement_type: str, topic: str) -> str:
    if source_statement_type == "contextual_relevance" or topic.endswith(".other"):
        return "needs_human_review"
    return "seeded_from_document_extraction"


def classify_d5(document_id: str, statement: str) -> tuple[str, str, str]:
    normalized = normalize_text(statement)

    if document_id == "mun_almere_pga_transformatieplan":
        if "health first" in normalized or "right help in the right place" in normalized:
            return "d5.health_first_shift", "prevention_first", "local_strategy"
        return "d5.cross_domain_collaboration", "almere_neighbourhood_collaboration", "contextual_implementation_signal"

    if document_id == "reg_flevoland_2023_regioplan_iza":
        if "ecosysteem mentale gezondheid" in normalized or "samen sterker in de wijk" in normalized:
            return "d5.mentale_gezondheidsnetwerken", "flevoland_neighbourhood_model", "contextual_implementation_signal"
        return "d5.cross_domain_collaboration", "regional_domain_overstijgende_samenwerking", "contextual_implementation_signal"

    if "five life domains" in normalized or "five leefgebieden" in normalized or "organized around five life domains" in normalized:
        return "d5.definition", "five_leefgebieden", "definition"

    if "sociaal verwijzen" in normalized or "valpreventie" in normalized:
        if "ontwikkelagenda" in normalized:
            return "d5.ontwikkelagenda", "underbouwd_and_development_split", "development_commitment"
        return "d5.basisfunctionaliteiten_onderbouwd", "sociaal_verwijzen_and_valpreventie", "implementation_commitment"

    if "workagenda" in normalized or "workagendas" in normalized or "gereedschapskist" in normalized:
        return "d5.regional_workagenda", "regional_translation", "implementation_requirement"

    if "regional monitor" in normalized or "content update" in normalized or "structural financing conditions" in normalized:
        return "d5.implementation_enablers", "funding_monitoring_update_cycle", "implementation_commitment"

    if "goal" in normalized or "equal access" in normalized:
        return "d5.definition", "care_social_cooperation_goal", "definition"

    return "d5.other", "uncategorized", "implementation_requirement"


def classify_d6(document_id: str, statement: str) -> tuple[str, str, str]:
    normalized = normalize_text(statement)

    if (
        "rtp" in normalized
        or "rso" in normalized
        or "data infrastructure" in normalized
        or "digital infrastructure" in normalized
        or "information picture" in normalized
        or "monitoring@home" in normalized
    ):
        return "d6.digital_and_operational_infrastructure", "data_and_transfer_infrastructure", "implementation_condition"

    if "inloopvoorzieningen" in normalized or "basisinfrastructuur" in normalized or "basis in wijk" in normalized:
        if "goal" in normalized or "framed" in normalized:
            return "d6.basisinfrastructuur", "wijk_en_regio_basis", "definition"
        return "d6.basisinfrastructuur", "wijk_en_regio_basis", "implementation_requirement"

    if "local teams" in normalized or "hechte wijkverbanden" in normalized:
        return "d6.local_teams", "wijkverbanden", "implementation_requirement"

    if "ggd" in normalized or "regional structure" in normalized:
        return "d6.regional_coordination", "ggd_and_regional_coordination", "implementation_requirement"

    return "d6.other", "uncategorized", "implementation_requirement"


def classify_governance_and_finance(document_id: str, statement: str) -> tuple[str, str, str]:
    normalized = normalize_text(statement)

    if "financieringsvorm" in normalized or "financiele-verhoudingswet" in normalized or "fund managers" in normalized:
        return "finance.d5_d6.funding_instrument", "municipal_channel", "funding_channel"

    if "doorbraakmiddelen" in normalized:
        return "finance.d5_d6.municipal_funding", "doorbraakmiddelen", "funding_commitment"

    if "start package" in normalized or "startpakket" in normalized:
        return "finance.d5_d6.municipal_funding", "startpakket_2027_2028", "funding_commitment"

    if "spuk gala" in normalized or "spuk iza" in normalized or "transformatiemiddelen" in normalized or "concrete budgets" in normalized:
        return "finance.regional_funding_path", "spuk_and_transformation_funding", "funding_path"

    if "multi-year funding horizon" in normalized or "financial framework already runs through 2028" in normalized or "phased financing horizon" in normalized or "sectoral growth" in normalized or "budgetary agreements leading" in normalized:
        return "finance.azwa_macro_framework", "multi_year_horizon", "financial_framework"

    if "verbindende coalitie" in normalized or "workgroups" in normalized or "expert team" in normalized:
        return "governance.regional_coordination", "flevoland_transformation_governance", "governance_arrangement"

    if "broad local coalition" in normalized or "broad local coalition of almere municipality" in normalized:
        return "governance.local_coalition", "almere_transformation_coalition", "governance_arrangement"

    if "bestuurlijke afspraak" in normalized or "bestuurlijke afspraken" in normalized:
        return "governance.national_coordination", "bestuurlijke_afspraken", "governance_arrangement"

    if "future balance" in normalized or "better aligned" in normalized:
        return "finance.local_alignment_goal", "almere_balance", "local_goal"

    return "governance_and_finance.other", "uncategorized", "governance_arrangement"


def classify_timeline(document_id: str, statement: str) -> tuple[str, str, str]:
    normalized = normalize_text(statement)

    if "q4 2025" in normalized or "q1 2026" in normalized:
        return "timeline.d5_d6_implementation", "national_milestones", "timeline_commitment"

    if "2030" in normalized:
        return "timeline.rollout_2030", "landelijke_dekking", "timeline_commitment"

    if "2026 to 2031" in normalized or "2026 through 2031" in normalized or "phased financing horizon" in normalized:
        return "timeline.d5_d6_financing_horizon", "funding_window_2026_2031", "timeline_commitment"

    if "2029" in normalized:
        return "timeline.almere_2029", "local_impact_horizon", "timeline_commitment"

    if "first and second quarter of 2024" in normalized or "end of the second quarter" in normalized or "definite transformatieagenda" in normalized:
        return "timeline.flevoland_transformatieagenda", "q2_2024", "timeline_commitment"

    if "ongoing implementation status" in normalized or "transformation rather than a standalone project" in normalized:
        return "timeline.implementation_status", "ongoing_transformation", "status_assessment"

    return "timeline.other", "uncategorized", "timeline_commitment"


def classify_monitoring(document_id: str, statement: str) -> tuple[str, str, str]:
    normalized = normalize_text(statement)

    if "impact goals" in normalized or "reach by 2029" in normalized:
        return "monitoring.local_goal_tracking", "almere_2029_goals", "monitoring_commitment"

    if "mid-term review" in normalized:
        return "monitoring.mid_term_review", "mtr_2027", "monitoring_commitment"

    if "updated in 2028" in normalized or "updated in 2028 based on monitoring and evaluation" in normalized:
        return "monitoring.update_2028", "content_refresh", "monitoring_commitment"

    if (
        "three levels" in normalized
        or "process-output-outcome" in normalized
        or "process, output, and outcome" in normalized
        or "proces, beweging" in normalized
        or "doelgroepen" in normalized
    ):
        return "monitoring.framework", "process_output_outcome", "monitoring_framework"

    if "mechanism and implementation will be monitored" in normalized:
        return "monitoring.d5_operational_monitoring", "implementation_adjustment", "monitoring_commitment"

    if "dashboard" in normalized or "2024 monitoringsplan" in normalized:
        return "monitoring.regional_monitoring_plan", "dashboard_and_existing_data", "monitoring_framework"

    if "samen leren" in normalized or "monitoring and learning" in normalized:
        return "monitoring.local_learning", "almere_learning_cycle", "monitoring_framework"

    if "iza-based azwa monitoring" in normalized or "broader iza-based azwa monitoring and evaluation framework" in normalized:
        return "monitoring.framework", "iza_linkage", "monitoring_framework"

    return "monitoring.other", "uncategorized", "monitoring_commitment"


def classify_municipal_translation(document_id: str, statement: str) -> tuple[str, str, str]:
    normalized = normalize_text(statement)

    if document_id == "mun_almere_pga_transformatieplan":
        if "voorzorgcirkels" in normalized or "welzijn op recept" in normalized or "leefstijlloket" in normalized or "kansrijke omgeving" in normalized:
            return "municipal.almere_initiatives", "named_local_initiatives", "local_implementation"
        return "municipal.almere_context", "local_pressure_profile", "local_context"

    if "roles and responsibilities" in normalized:
        return "municipal.role_allocation", "implementation_responsibility", "governance_requirement"

    if "local teams" in normalized or "neighbourhood-level voorzieningen" in normalized:
        return "municipal.local_structure", "d6_local_delivery", "implementation_requirement"

    if "local tailoring" in normalized or "local needs" in normalized:
        return "municipal.implementation_translation", "regional_local_tailoring", "implementation_requirement"

    return "municipal.implementation_translation", "regional_and_municipal_execution", "implementation_requirement"


def classify_claim(document_id: str, section_name: str, statement: str) -> tuple[str, str, str]:
    if section_name == "d5":
        return classify_d5(document_id, statement)
    if section_name == "d6":
        return classify_d6(document_id, statement)
    if section_name == "governance_and_finance":
        return classify_governance_and_finance(document_id, statement)
    if section_name == "timeline_and_status":
        return classify_timeline(document_id, statement)
    if section_name == "monitoring_and_evaluation":
        return classify_monitoring(document_id, statement)
    if section_name == "municipal_translation":
        return classify_municipal_translation(document_id, statement)
    raise ValueError(f"Unsupported section: {section_name}")


def extract_source_location(item: dict) -> dict:
    evidence = item.get("evidence", [])
    pages = unique_preserving_order([entry.get("page") for entry in evidence])
    sections = unique_preserving_order([entry.get("section") for entry in evidence if entry.get("section")])
    evidence_quotes = unique_preserving_order([entry.get("evidence_quote") for entry in evidence if entry.get("evidence_quote")])
    return {
        "source_statement_ids": [item["statement_id"]],
        "pages": pages,
        "sections": sections,
        "evidence_quotes": evidence_quotes,
    }


def relation_specs() -> dict[str, list[dict]]:
    return {
        claim_id_for("nat_azwa_2025_definitief_d5_001"): [
            {
                "type": "supersedes",
                "target_claim_id": claim_id_for("nat_azwa_2025_onderhandelaarsakkoord_d5_001"),
                "note": "The signed AZWA replaces the earlier negotiation wording for the D5 structure.",
            }
        ],
        claim_id_for("nat_azwa_2025_definitief_d5_002"): [
            {
                "type": "clarifies",
                "target_claim_id": claim_id_for("nat_azwa_2025_onderhandelaarsakkoord_d5_001"),
                "note": "The final agreement sharpens the split between the underbouwde set and the development path.",
            }
        ],
        claim_id_for("nat_azwa_2025_definitief_d5_003"): [
            {
                "type": "clarifies",
                "target_claim_id": claim_id_for("nat_azwa_2025_onderhandelaarsakkoord_d5_002"),
                "note": "The final agreement keeps the regional workagenda logic but states it more clearly.",
            }
        ],
        claim_id_for("nat_azwa_2025_definitief_d6_001"): [
            {
                "type": "supersedes",
                "target_claim_id": claim_id_for("nat_azwa_2025_onderhandelaarsakkoord_d6_001"),
                "note": "The signed AZWA replaces the negotiation wording for the D6 basisinfrastructure package.",
            }
        ],
        claim_id_for("nat_azwa_2025_definitief_governance_and_finance_003"): [
            {
                "type": "clarifies",
                "target_claim_id": claim_id_for("nat_azwa_2025_onderhandelaarsakkoord_governance_and_finance_001"),
                "note": "The final agreement restates the funding-channel logic with the same VNG and fund-manager route.",
            }
        ],
        claim_id_for("nat_azwa_2025_definitief_timeline_and_status_001"): [
            {
                "type": "clarifies",
                "target_claim_id": claim_id_for("nat_azwa_2025_onderhandelaarsakkoord_timeline_and_status_001"),
                "note": "The final agreement retains and confirms the same milestone sequence.",
            }
        ],
        claim_id_for("nat_azwa_2025_definitief_monitoring_and_evaluation_001"): [
            {
                "type": "clarifies",
                "target_claim_id": claim_id_for("nat_azwa_2025_onderhandelaarsakkoord_monitoring_and_evaluation_002"),
                "note": "The final agreement confirms the IZA-based monitoring stack in more settled form.",
            }
        ],
        claim_id_for("nat_azwa_2026_cw31_kader_d5_d6_d5_001"): [
            {
                "type": "implements",
                "target_claim_id": claim_id_for("nat_azwa_2025_definitief_d5_001"),
                "note": "CW 3.1 operationalizes the signed D5 commitment in a fiscal-justification format.",
            }
        ],
        claim_id_for("nat_azwa_2026_cw31_kader_d5_d6_d5_002"): [
            {
                "type": "implements",
                "target_claim_id": claim_id_for("nat_azwa_2025_definitief_d5_002"),
                "note": "CW 3.1 turns the underbouwde D5 examples into a concrete implementation justification.",
            }
        ],
        claim_id_for("nat_azwa_2026_cw31_kader_d5_d6_d6_001"): [
            {
                "type": "implements",
                "target_claim_id": claim_id_for("nat_azwa_2025_definitief_d6_001"),
                "note": "CW 3.1 gives execution logic for the D6 basisinfrastructure obligation.",
            }
        ],
        claim_id_for("nat_azwa_2026_cw31_kader_d5_d6_governance_and_finance_001"): [
            {
                "type": "clarifies",
                "target_claim_id": claim_id_for("nat_azwa_2025_definitief_governance_and_finance_003"),
                "note": "CW 3.1 restates the municipal funding-channel choice in a compact explanatory sheet.",
            }
        ],
        claim_id_for("nat_azwa_2026_cw31_kader_d5_d6_monitoring_and_evaluation_001"): [
            {
                "type": "clarifies",
                "target_claim_id": claim_id_for("nat_azwa_2025_definitief_monitoring_and_evaluation_003"),
                "note": "CW 3.1 makes the implementation-monitoring and update logic more explicit.",
            }
        ],
        claim_id_for("mun_almere_pga_transformatieplan_d5_001"): [
            {
                "type": "derives_from",
                "target_claim_id": claim_id_for("reg_flevoland_2023_regioplan_iza_d5_002"),
                "note": "The Almere cooperation model sits within the broader Flevoland domain-overstijgende collaboration agenda.",
            }
        ],
        claim_id_for("mun_almere_pga_transformatieplan_d6_001"): [
            {
                "type": "depends_on",
                "target_claim_id": claim_id_for("reg_flevoland_2023_regioplan_iza_d6_001"),
                "note": "The local operational infrastructure depends on the regional digital and information architecture track.",
            }
        ],
        claim_id_for("mun_almere_pga_transformatieplan_monitoring_and_evaluation_001"): [
            {
                "type": "derives_from",
                "target_claim_id": claim_id_for("reg_flevoland_2023_regioplan_iza_monitoring_and_evaluation_002"),
                "note": "The local learning and monitoring approach follows the broader regional dashboard and reuse-of-data logic.",
            }
        ],
    }


def build_claim(item: dict, document_payload: dict, section_name: str, instrument_type: str, authority_weight: float) -> dict:
    statement = item["statement"]
    topic, subtopic, claim_type = classify_claim(document_payload["document_id"], section_name, statement)
    metadata = document_payload["metadata"]
    source_statement_type = item.get("statement_type", "direct_extraction")
    return {
        "claim_id": claim_id_for(item["statement_id"]),
        "topic": topic,
        "subtopic": subtopic,
        "claim_type": claim_type,
        "statement": statement,
        "source_document_id": document_payload["document_id"],
        "source_location": extract_source_location(item),
        "publisher": metadata["publisher"],
        "instrument_type": instrument_type,
        "jurisdiction_level": metadata["jurisdiction_level"],
        "document_status": metadata["status"],
        "authority_weight": authority_weight,
        "publication_date": metadata["publication_date"],
        "effective_from": metadata["publication_date"],
        "effective_to": None,
        "validity_status": validity_status_for(document_payload["document_id"], source_statement_type),
        "applies_to": applies_to_for(document_payload["document_id"]),
        "confidence": confidence_for(metadata["jurisdiction_level"], source_statement_type, topic),
        "human_review_status": human_review_status_for(source_statement_type, topic),
        "source_statement_type": source_statement_type,
        "claim_extraction_run_id": CLAIM_EXTRACTION_RUN_ID,
        "relations": [],
    }


def build_document_claims(document_id: str, authority_map: dict[str, str], instrument_profiles: dict[str, dict]) -> list[dict]:
    document_payload = load_document(document_id)
    document_type = document_payload["metadata"]["document_type"]
    instrument_type = authority_map[document_type]
    authority_weight = instrument_profiles[instrument_type]["authority_weight"]

    claims: list[dict] = []
    for section_name, section in document_payload["structured_content"].items():
        for item in section["items"]:
            claims.append(build_claim(item, document_payload, section_name, instrument_type, authority_weight))
    return claims


def validate_claims(claims: list[dict], allowed_relation_types: set[str]) -> None:
    required_fields = {
        "claim_id",
        "topic",
        "subtopic",
        "claim_type",
        "statement",
        "source_document_id",
        "source_location",
        "publisher",
        "jurisdiction_level",
        "document_status",
        "authority_weight",
        "publication_date",
        "effective_from",
        "effective_to",
        "validity_status",
        "applies_to",
        "confidence",
        "human_review_status",
        "relations",
    }
    claim_ids = set()

    for claim in claims:
        missing = required_fields - set(claim)
        if missing:
            missing_list = ", ".join(sorted(missing))
            raise ValueError(f"Claim {claim.get('claim_id')} is missing required fields: {missing_list}")

        claim_id = claim["claim_id"]
        if claim_id in claim_ids:
            raise ValueError(f"Duplicate claim id detected: {claim_id}")
        claim_ids.add(claim_id)

        if not claim["source_location"]["source_statement_ids"]:
            raise ValueError(f"Claim {claim_id} is missing source statement references")

        for relation in claim["relations"]:
            relation_type = relation["type"]
            if relation_type not in allowed_relation_types:
                raise ValueError(f"Claim {claim_id} uses unsupported relation type: {relation_type}")

    for claim in claims:
        for relation in claim["relations"]:
            if relation["target_claim_id"] not in claim_ids:
                raise ValueError(
                    f"Claim {claim['claim_id']} points to missing relation target {relation['target_claim_id']}"
                )


def write_outputs(claims_by_document: dict[str, list[dict]], source_runs: dict[str, str]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    master_path = OUTPUT_DIR / "claims_master.jsonl"
    with master_path.open("w", encoding="utf-8") as handle:
        for document_id in TOP5_DOCUMENT_IDS:
            for claim in claims_by_document[document_id]:
                handle.write(json.dumps(claim, ensure_ascii=False) + "\n")

    for document_id in TOP5_DOCUMENT_IDS:
        document_path = OUTPUT_DIR / f"{document_id}.json"
        payload = {
            "document_id": document_id,
            "claim_extraction_run_id": CLAIM_EXTRACTION_RUN_ID,
            "generated_on": date.today().isoformat(),
            "source_extraction_run_id": source_runs[document_id],
            "claim_count": len(claims_by_document[document_id]),
            "claims": claims_by_document[document_id],
        }
        document_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote {document_path.relative_to(REPO_ROOT).as_posix()}")

    print(f"Wrote {master_path.relative_to(REPO_ROOT).as_posix()}")


def main() -> None:
    authority_map, instrument_profiles = load_authority_model()
    allowed_relation_types = load_allowed_relation_types()
    relations_by_claim_id = relation_specs()

    claims_by_document: dict[str, list[dict]] = {}
    source_runs: dict[str, str] = {}

    for document_id in TOP5_DOCUMENT_IDS:
        document_payload = load_document(document_id)
        source_runs[document_id] = document_payload["extraction_run_id"]
        document_claims = build_document_claims(document_id, authority_map, instrument_profiles)
        for claim in document_claims:
            claim["relations"] = relations_by_claim_id.get(claim["claim_id"], [])
        claims_by_document[document_id] = document_claims

    all_claims = [claim for document_id in TOP5_DOCUMENT_IDS for claim in claims_by_document[document_id]]
    validate_claims(all_claims, allowed_relation_types)
    write_outputs(claims_by_document, source_runs)


if __name__ == "__main__":
    main()
