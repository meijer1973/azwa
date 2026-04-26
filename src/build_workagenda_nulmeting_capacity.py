from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
EXTRACTED_DIR = REPO_ROOT / "data" / "extracted"
WORKAGENDA_PATH = EXTRACTED_DIR / "workagenda_d5_operational_requirements.json"
LOCAL_SOURCE_PATH = EXTRACTED_DIR / "local_source_strengthening_almere.json"
OUTPUT_PATH = EXTRACTED_DIR / "workagenda_nulmeting_capacity.json"


CBS_ALMERE_2025 = {
    "source_id": "cbs_kwb_2025_almere_verified_live",
    "title": "CBS Kerncijfers wijken en buurten 2025 - Almere gemeente",
    "source_url": "https://www.cbs.nl/nl-nl/cijfers/detail/86165NED",
    "verification": "Verified from CBS OData table 86165NED on 2026-04-26; row Codering_3 GM0034, SoortRegio_2 Gemeente.",
    "peildatum": "2025-01-01",
    "status": "verified_public_denominator_not_yet_manifest_source",
    "values": {
        "population_total": 229574,
        "population_0_15": 41399,
        "population_15_25": 28014,
        "population_25_45": 67600,
        "population_45_65": 60051,
        "population_65_plus": 32510,
        "households_total": 98394,
        "population_density_per_km2": 1777,
    },
}


GGD_INDICATORS = {
    "adult": {
        "source_document_id": "reg_ggd_flevoland_2024_volwassenen_gemeenten",
        "source_title": "GGD Flevoland Tabellenboek volwassenen 2024 - gemeenten",
        "status": "public_table_book_ingested_needs_human_review",
        "indicators": [
            {"indicator_id": "adult_overweight_moderate_pct", "label": "Matig overgewicht 18-64", "value": 37, "unit": "%", "page": 11},
            {"indicator_id": "adult_obesity_pct", "label": "Ernstig overgewicht/obesitas 18-64", "value": 21, "unit": "%", "page": 11},
            {"indicator_id": "adult_meets_movement_guideline_pct", "label": "Voldoet aan beweegrichtlijn 18-64", "value": 47, "unit": "%", "page": 11},
            {"indicator_id": "adult_fallen_once_or_more_pct", "label": "Een of meer keer gevallen 18-64", "value": 14, "unit": "%", "page": 10},
            {"indicator_id": "adult_strong_loneliness_pct", "label": "Sterk eenzaam 18-64", "value": 21, "unit": "%", "page": 14},
            {"indicator_id": "adult_high_anxiety_depression_risk_pct", "label": "Hoog risico angststoornis/depressie 18-64", "value": 14, "unit": "%", "page": 14},
            {"indicator_id": "adult_brittle_health_pct", "label": "Broze gezondheid 18-64", "value": 37, "unit": "%", "page": 15},
            {"indicator_id": "adult_informal_carer_pct", "label": "Mantelzorger 18-64", "value": 11, "unit": "%", "page": 16},
        ],
    },
    "older": {
        "source_document_id": "reg_ggd_flevoland_2024_ouderen_gemeenten",
        "source_title": "GGD Flevoland Tabellenboek ouderen 2024 - gemeenten",
        "status": "public_table_book_ingested_needs_human_review",
        "indicators": [
            {"indicator_id": "older_fall_concern_pct", "label": "Bezorgd om te vallen 65+", "value": 31, "unit": "%", "page": 10},
            {"indicator_id": "older_fallen_once_or_more_pct", "label": "Een of meer keer gevallen 65+", "value": 24, "unit": "%", "page": 10},
            {"indicator_id": "older_fallen_twice_or_more_pct", "label": "Twee keer of vaker gevallen 65+", "value": 10, "unit": "%", "page": 10},
            {"indicator_id": "older_obesity_pct", "label": "Ernstig overgewicht/obesitas 65+", "value": 16, "unit": "%", "page": 11},
            {"indicator_id": "older_meets_movement_guideline_pct", "label": "Voldoet aan beweegrichtlijn 65+", "value": 37, "unit": "%", "page": 11},
            {"indicator_id": "older_strong_loneliness_pct", "label": "Sterk eenzaam 65+", "value": 15, "unit": "%", "page": 14},
            {"indicator_id": "older_high_anxiety_depression_risk_pct", "label": "Hoog risico angststoornis/depressie 65+", "value": 8, "unit": "%", "page": 14},
            {"indicator_id": "older_brittle_health_pct", "label": "Broze gezondheid 65+", "value": 32, "unit": "%", "page": 15},
            {"indicator_id": "older_informal_carer_pct", "label": "Mantelzorger 65+", "value": 20, "unit": "%", "page": 16},
        ],
    },
}


TARGET_PUBLIC_BASELINE = {
    "laagdrempelige_steunpunten": {
        "public_evidence": [
            "GGD-indicatoren voor eenzaamheid, angst/depressierisico en broze gezondheid geven publieke urgentiesignalen.",
        ],
        "indicator_ids": [
            "adult_strong_loneliness_pct",
            "older_strong_loneliness_pct",
            "adult_high_anxiety_depression_risk_pct",
            "older_high_anxiety_depression_risk_pct",
        ],
        "local_fill_fields": [
            "bestaande steunpunten die mogen meetellen",
            "openingstijden en toegankelijkheid",
            "wijk- of stadsdeeldekking",
            "uitvoerder/eigenaar",
            "formatie of coordinatiecapaciteit",
            "budget en financieringsbron",
        ],
    },
    "sociaal_verwijzen": {
        "public_evidence": [
            "Landelijke werkagenda-bron geeft richtinggevende capaciteit: 60 verwijzingen per 10.000 inwoners en 0,2-0,5 fte brugfunctie per 10.000 inwoners.",
            "CBS 2025 denominator maakt een eerste indicatieve Almere-rekensom mogelijk.",
        ],
        "indicator_ids": ["adult_brittle_health_pct", "older_brittle_health_pct"],
        "calculations": ["sociaal_verwijzen_referrals_per_year", "sociaal_verwijzen_bridge_fte_range"],
        "local_fill_fields": [
            "huidige verwijsroute",
            "aantal verwijzingen huidig",
            "brugfunctionaris-fte huidig",
            "aanbieders en afspraken met eerste lijn",
            "monitoringregistratie",
        ],
    },
    "mentale_gezondheidsnetwerken": {
        "public_evidence": [
            "GGD-indicatoren geven publieke urgentiesignalen; MGN-rol/geografie is carry-over naar geschoonde validatie.",
        ],
        "indicator_ids": [
            "adult_high_anxiety_depression_risk_pct",
            "older_high_anxiety_depression_risk_pct",
            "adult_strong_loneliness_pct",
            "older_strong_loneliness_pct",
        ],
        "local_fill_fields": [
            "geschoonde MGN-rol/geografie",
            "huidige netwerkafspraken",
            "aanmeldroute",
            "capaciteit per partner",
            "mandaat en besluitstatus",
        ],
    },
    "valpreventie": {
        "public_evidence": [
            "GGD Valpreventie Almere beschrijft publieke inloop/risico-inschatting en cursusmatching.",
            "GGD-tabellenboek ouderen geeft publieke valindicatoren voor Almere.",
            "Landelijke werkagenda-richting noemt valrisico-inschatting bij 14% van de 65-plussers.",
        ],
        "indicator_ids": [
            "older_fall_concern_pct",
            "older_fallen_once_or_more_pct",
            "older_fallen_twice_or_more_pct",
            "older_meets_movement_guideline_pct",
        ],
        "calculations": ["valpreventie_risk_assessments_14pct_65plus"],
        "local_fill_fields": [
            "cursuscapaciteit",
            "aanbieders per wijk/stadsdeel",
            "wachttijden",
            "doorverwijsroute vanuit inloop",
            "structureel beweegaanbod",
            "budget en eigenaarschap",
        ],
    },
    "ketenaanpak_overgewicht_obesitas_volwassenen": {
        "public_evidence": [
            "GGD-tabellenboek volwassenen geeft publieke Almere-indicatoren voor overgewicht, obesitas en bewegen.",
        ],
        "indicator_ids": [
            "adult_overweight_moderate_pct",
            "adult_obesity_pct",
            "adult_meets_movement_guideline_pct",
        ],
        "local_fill_fields": [
            "GLI-capaciteit",
            "leefstijl- en beweegaanbod",
            "centrale zorgcoordinatie",
            "wijkspreiding",
            "wachttijden",
            "financieringsmix Zvw/gemeente/GALA/PGA",
        ],
    },
    "kansrijke_start": {
        "public_evidence": [
            "CBS 2025 geeft publieke leeftijdsdenominatoren; lokale coalitie-, capaciteit- en interventiekeuzes zijn nog invulvelden.",
        ],
        "indicator_ids": [],
        "local_fill_fields": [
            "coalitie Kansrijke Start",
            "doelgroepdefinitie",
            "huidig interventieaanbod",
            "bereik en locaties",
            "eigenaar en uitvoerders",
            "besluitstatus",
        ],
    },
    "integrale_gezinspoli": {
        "public_evidence": [
            "Publieke corpuslaag bevat nog geen Almeerse capaciteit of besluit voor een integrale gezinspoli.",
        ],
        "indicator_ids": [],
        "local_fill_fields": [
            "bestaat er een gezinspoli of vergelijkbare route",
            "kernteam en vaste gezichten",
            "MDO-afspraken",
            "taakverschuiving",
            "capaciteit",
            "besluitstatus",
        ],
    },
    "nu_niet_zwanger": {
        "public_evidence": [
            "Werkagenda noemt structurele coordinatie en expertise; publieke Almere-capaciteit is nog niet in de corpuslaag gevonden.",
        ],
        "indicator_ids": [],
        "local_fill_fields": [
            "regionale of lokale organisatievorm",
            "coordinator/expertise",
            "aangesloten professionals",
            "anticonceptiebudget",
            "bereik",
            "GGD-regio versus IZA/AZWA-regio keuze",
        ],
    },
    "ketenaanpak_overgewicht_obesitas_kinderen": {
        "public_evidence": [
            "CBS 2025 geeft publieke jeugdleeftijdsdenominatoren; specifieke jeugdgezondheids- en CZV/kinder-GLI-capaciteit is nog invulveld.",
        ],
        "indicator_ids": [],
        "local_fill_fields": [
            "CZV-capaciteit",
            "kinder-GLI-aanbod",
            "jeugdgezondheidsindicatoren",
            "school/wijkspreiding",
            "regionale coordinatie",
            "financiering",
        ],
    },
    "ontwikkelagenda_1_nieuw_beproeven": {
        "public_evidence": [
            "Alleen vullen wanneer publieke bron of lokale validatie aangeeft dat Almere/Flevoland dit wil beproeven.",
        ],
        "indicator_ids": [],
        "local_fill_fields": [
            "gekozen aanpak",
            "onderbouwing",
            "beschikbare capaciteit",
            "financiering zonder verdringing",
            "besluitstatus",
        ],
    },
    "ontwikkelagenda_2_overige_initiatieven": {
        "public_evidence": [
            "Alleen opnemen als publieke bron of lokale validatie aangeeft dat dit praktisch nodig is.",
        ],
        "indicator_ids": [],
        "local_fill_fields": [
            "initiatief",
            "relatie met D5",
            "lokale eigenaar",
            "capaciteit",
            "financiering",
            "besluitstatus",
        ],
    },
}


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def indicator_index() -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for age_group, source in GGD_INDICATORS.items():
        for indicator in source["indicators"]:
            rows[indicator["indicator_id"]] = {
                **indicator,
                "age_group": age_group,
                "source_document_id": source["source_document_id"],
                "source_title": source["source_title"],
                "source_status": source["status"],
            }
    return rows


def build_calculations(population: dict[str, int]) -> dict[str, dict[str, Any]]:
    total = population["population_total"]
    older = population["population_65_plus"]
    return {
        "sociaal_verwijzen_referrals_per_year": {
            "label": "Richtinggevend aantal verwijzingen sociaal verwijzen per jaar",
            "formula": "population_total / 10000 * 60",
            "value": round(total / 10000 * 60),
            "unit": "verwijzingen per jaar",
            "basis": "Landelijke richtingwaarde uit werkagenda-bron, toegepast op CBS 2025 Almere totaal.",
            "status": "indicative_public_calculation_needs_local_validation",
        },
        "sociaal_verwijzen_bridge_fte_range": {
            "label": "Richtinggevende brugfunctionaris-capaciteit",
            "formula": "population_total / 10000 * 0.2 to population_total / 10000 * 0.5",
            "min_value": round(total / 10000 * 0.2, 1),
            "max_value": round(total / 10000 * 0.5, 1),
            "unit": "fte",
            "basis": "Landelijke richtingwaarde uit werkagenda-bron, toegepast op CBS 2025 Almere totaal.",
            "status": "indicative_public_calculation_needs_local_validation",
        },
        "valpreventie_risk_assessments_14pct_65plus": {
            "label": "Richtinggevend aantal valrisico-inschattingen bij 14% van 65-plussers",
            "formula": "population_65_plus * 0.14",
            "value": round(older * 0.14),
            "unit": "valrisico-inschattingen",
            "basis": "Landelijke richtingwaarde uit werkagenda-bron, toegepast op CBS 2025 Almere 65-plus.",
            "status": "indicative_public_calculation_needs_local_validation",
        },
    }


def build_target_rows(workagenda: dict[str, Any], indicators: dict[str, dict[str, Any]], calculations: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for target in workagenda.get("targets", []):
        baseline = TARGET_PUBLIC_BASELINE.get(target["target_id"], {})
        target_indicators = [indicators[indicator_id] for indicator_id in baseline.get("indicator_ids", []) if indicator_id in indicators]
        target_calculations = [
            {**calculations[calculation_id], "calculation_id": calculation_id}
            for calculation_id in baseline.get("calculations", [])
            if calculation_id in calculations
        ]
        public_field_count = len(target_indicators) + len(target_calculations) + len(baseline.get("public_evidence", []))
        local_fill_fields = baseline.get("local_fill_fields", [])
        rows.append(
            {
                "target_id": target["target_id"],
                "title": target.get("title"),
                "workagenda_status": target.get("workagenda_status"),
                "required_in_workagenda": target.get("required_in_workagenda"),
                "leefgebied": target.get("leefgebied"),
                "public_baseline_status": "partly_filled_from_public_sources" if public_field_count else "public_gap_only",
                "public_evidence": baseline.get("public_evidence", []),
                "public_indicators": target_indicators,
                "indicative_calculations": target_calculations,
                "local_fill_fields": local_fill_fields,
                "local_fill_count": len(local_fill_fields),
                "decision_needed": [
                    "prioritering_2027_2030",
                    "lokale_eigenaar",
                    "budget",
                    "monitoringafspraak",
                    "formele_besluitstatus",
                ],
                "review_note": (
                    "Use public evidence to prefill the workagenda. Leave local capacity, exact providers, budget, "
                    "ownership, and decisions as validation fields when public sources do not support them."
                ),
            }
        )
    return rows


def build_payload() -> dict[str, Any]:
    workagenda = load_json(WORKAGENDA_PATH, {"targets": []})
    local_sources = load_json(LOCAL_SOURCE_PATH, {})
    indicators = indicator_index()
    calculations = build_calculations(CBS_ALMERE_2025["values"])
    targets = build_target_rows(workagenda, indicators, calculations)
    filled_targets = [target for target in targets if target["public_baseline_status"] == "partly_filled_from_public_sources"]

    return {
        "layer_run_id": "phase25_3_workagenda_nulmeting_capacity_v1",
        "generated_on": date.today().isoformat(),
        "status": "active_sprint_support",
        "sprint": "25.3 Nulmeting en capaciteit werkagenda",
        "purpose": (
            "Prefill the workagenda structure as far as public sources allow, while marking capacity, provider, "
            "ownership, budget, and decision gaps for local staff validation or later decisions."
        ),
        "public_source_boundary": (
            "Only public corpus sources and a verified public CBS denominator are used. Missing non-public knowledge is "
            "represented as local_fill_fields or decision_needed, not inferred."
        ),
        "inputs": [
            "data/extracted/workagenda_d5_operational_requirements.json",
            "data/extracted/local_source_strengthening_almere.json",
            "data/intermediate/source_markdown/reg_ggd_flevoland_2024_volwassenen_gemeenten.md",
            "data/intermediate/source_markdown/reg_ggd_flevoland_2024_ouderen_gemeenten.md",
            "CBS OData 86165NED row GM0034 verified on 2026-04-26",
        ],
        "summary": {
            "target_count": len(targets),
            "targets_with_public_prefill": len(filled_targets),
            "targets_public_gap_only": len(targets) - len(filled_targets),
            "indicator_count": len(indicators),
            "indicative_calculation_count": len(calculations),
            "local_fill_field_count": sum(target["local_fill_count"] for target in targets),
            "manifest_document_count_at_start": (local_sources.get("summary") or {}).get("manifest_document_count"),
        },
        "denominators": {
            "almere_population_2025": CBS_ALMERE_2025,
        },
        "indicator_sources": GGD_INDICATORS,
        "calculations": calculations,
        "targets": targets,
        "carry_forward": [
            "Review GGD percentage extraction against source pages before using in bestuurlijke text.",
            "Add the CBS denominator as a formal manifest source if the layer becomes public-facing or audit-critical.",
            "Ask local employees to fill current aanbod, capaciteit/fte, wachttijden, wijkspreiding, budget, owner, and decision status where public sources are silent.",
            "Escalate unresolved prioritization, budget, owner, and scale choices as decision questions after local validation.",
        ],
    }


def main() -> None:
    payload = build_payload()
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"Targets with public prefill: {payload['summary']['targets_with_public_prefill']}")


if __name__ == "__main__":
    main()
