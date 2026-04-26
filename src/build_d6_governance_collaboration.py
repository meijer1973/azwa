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
            "laag­drempelige steunpunten",
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
        rows.append(
            {
                **dimension,
                "source_claim_count": len(supporting_claims),
                "top_source_document_ids": [doc_id for doc_id, _count in source_counts.most_common(6)],
                "sample_claims": supporting_claims[:8],
                "public_coverage_status": "public_claims_present_needs_review" if supporting_claims else "public_gap",
                "review_note": "Claims support orientation only; use source passages before writing bestuurlijke text.",
            }
        )
    return rows


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
            "dimensions_with_public_claims": sum(1 for row in dimensions if row["source_claim_count"] > 0),
            "local_validation_field_count": sum(len(row["local_validation_fields"]) for row in dimensions)
            + sum(len(row["validation_needed"]) for row in ACTOR_ROLES),
            "nulmeting_target_count": (nulmeting.get("summary") or {}).get("target_count"),
        },
        "regional_guardrail": {
            "editorial_rule": regional_roles.get("editorial_rule"),
            "regional_splits": regional_roles.get("regional_splits", []),
            "regional_roles": regional_roles.get("regional_roles", []),
        },
        "actor_roles": ACTOR_ROLES,
        "dimensions": dimensions,
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
