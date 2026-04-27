from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
EXTRACTED_DIR = REPO_ROOT / "data" / "extracted"
MUNICIPAL_DIR = EXTRACTED_DIR / "municipal"
D6_GOVERNANCE_PATH = EXTRACTED_DIR / "d6_governance_collaboration.json"
OUTPUT_PATH = MUNICIPAL_DIR / "almere_d6_responsibility_register.json"


PUBLIC_SOURCE_CANDIDATES = [
    {
        "source_id": "mun_almere_2026_stevige_lokale_teams_raad",
        "title": "Stevige Lokale Teams en inzet Investeringsfonds jeugd en gezin",
        "publisher": "Raad van Almere",
        "source_url": "https://raadvanalmere.nl/article/stevige-lokale-teams-en-inzet-investeringsfonds-jeugd-en-gezin1",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_27",
        "why_it_matters": (
            "Candidate local decision source for one recognizable team per wijk, professionals with mandate, "
            "continuous regie, 2026 start in two wijkteamgebieden, and involvement of JGZ Almere and wijkteams."
        ),
        "intake_action": "Verify council page and Documentwijzer 26006 attachments; ingest selected decision documents.",
    },
    {
        "source_id": "mun_almere_wijkteams",
        "title": "Wijkteams Almere",
        "publisher": "Wijkteams Almere / Gemeente Almere",
        "source_url": "https://wijkteams.almere.nl/",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_27",
        "why_it_matters": "Baseline public source for existing local access and wijkteam support structure.",
        "intake_action": "Add as municipal implementation source for D6 access and social infrastructure.",
    },
    {
        "source_id": "nat_vng_richtinggevend_kader_toegang_lokale_teams",
        "title": "Richtinggevend kader: toegang, lokale teams en integrale dienstverlening",
        "publisher": "VNG",
        "source_url": "https://vng.nl/publicaties/richtinggevend-kader-toegang-lokale-teams-en-integrale-dienstverlening",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "pdf_downloaded_2026_04_27",
        "why_it_matters": (
            "National assessment frame for access, local teams and integrated services; useful as benchmark, "
            "not as an Almere decision."
        ),
        "intake_action": "Add as national implementation benchmark and preserve distinction from local decisions.",
    },
    {
        "source_id": "nat_tsd_basisfuncties_lokale_teams",
        "title": "Basisfuncties voor lokale teams",
        "publisher": "Toezicht Sociaal Domein",
        "source_url": "https://www.toezichtsociaaldomein.nl/documenten/2021/10/06/basisfuncties-voor-lokale-teams",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_27",
        "why_it_matters": "Quality and assessment framework for low-threshold, nearby and integrated local teams.",
        "intake_action": "Add as assessment framework for Wijkteams Almere and Stevige Lokale Teams.",
    },
    {
        "source_id": "reg_ggd_flevoland_begroting_2026",
        "title": "Begroting 2026 GGD Flevoland",
        "publisher": "GGD Flevoland",
        "source_url": "https://www.ggdflevoland.nl/app/uploads/sites/6/2025/10/Begroting-2026-GGD-Flevoland.pdf",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "pdf_downloaded_2026_04_27",
        "why_it_matters": (
            "Current public source for GGD governance, JGZ, Kennis en Advies, prevention, finance, "
            "plustaken and GGD-region scale."
        ),
        "intake_action": "Add as regional raw PDF and link to D6 GGD/JGZ/monitoring responsibilities.",
    },
    {
        "source_id": "reg_ggd_flevoland_kennis_en_advies",
        "title": "Kennis en Advies",
        "publisher": "GGD Flevoland",
        "source_url": "https://www.ggdflevoland.nl/professional/kennis-en-advies/",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_27",
        "why_it_matters": "Public source for monitors, dashboards, epidemiology, data analysis and advice.",
        "intake_action": "Add as monitoring and knowledge source.",
    },
    {
        "source_id": "reg_ggd_flevoland_jgz_almere_profile",
        "title": "Profiel Jeugdgezondheidszorg",
        "publisher": "GGD Flevoland",
        "source_url": "https://www.ggdflevoland.nl/professional/jeugdgezondheidszorg/",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_27",
        "why_it_matters": "Public source for JGZ Almere 0-18, school links, youth support and care-chain role.",
        "intake_action": "Add as D6/JGZ implementation evidence.",
    },
    {
        "source_id": "mun_almere_samen_sterker_in_de_wijk_story",
        "title": "Samen Sterker in de Wijk",
        "publisher": "Gemeente Almere",
        "source_url": "https://www.almere.nl/zorg-en-welzijn/wonen-en-zorg/informatie-voor-onze-inwoners/verhalen-over-wonen-en-zorg/zorgvrager-en-zorgdrager/samen-sterker-in-de-wijk",
        "repository_status": "candidate_public_source_not_ingested",
        "verification_status": "search_result_available_but_direct_download_returned_404_2026_04_27",
        "why_it_matters": "Public narrative source for mental-health neighbourhood cooperation and one-plan/steungroep logic.",
        "intake_action": "Add as supporting local implementation source; avoid treating interview text as formal mandate.",
    },
    {
        "source_id": "mun_almere_samenwerkingsprojecten",
        "title": "Samenwerkingsprojecten",
        "publisher": "Gemeente Almere",
        "source_url": "https://www.almere.nl/zorg-en-welzijn/wonen-en-zorg/informatie-voor-onze-partners/samenwerkingsprojecten",
        "repository_status": "candidate_public_source_not_ingested",
        "verification_status": "search_result_available_but_direct_download_returned_404_2026_04_27",
        "why_it_matters": "Public source for Samen Sterker in de Wijk partners, pilots, netwerkteams, learning cycle and related local projects.",
        "intake_action": "Add as implementation source for mental-health wijk infrastructure and partner mapping.",
    },
]


COMPONENTS = [
    {
        "component_id": "inloopvoorzieningen_sociaal_en_gezond",
        "component_label": "Inloopvoorzieningen sociaal en gezond",
        "existing_almere_provision": None,
        "required_upgrade": "Local inventory needed: which existing inloop/social-base facilities count as D6 infrastructure.",
        "owner": None,
        "executors": [],
        "cooperation_partners": ["social work", "GGD/JGZ", "citizen initiatives", "informal support"],
        "scale": "almere_local_needs_validation",
        "funding_sources": ["unknown_needs_decision"],
        "decision_status": "review_needed",
        "evidence_sources": ["data/extracted/d6_governance_collaboration.json"],
        "confidence": "low",
        "open_issue": "National D6 norm exists, but local Almere inventory and formal classification are not yet source-backed.",
    },
    {
        "component_id": "wijkteams_almere",
        "component_label": "Wijkteams Almere",
        "existing_almere_provision": "Public page confirms wijkteams as local support route with wijkwerkers from diverse care and welfare organizations.",
        "required_upgrade": "Map governance, mandate, partners, wijk coverage, relation to D6 and relation to Stevige Lokale Teams.",
        "owner": "Gemeente Almere needs confirmation",
        "executors": ["wijkwerkers", "care and welfare organizations represented in wijkteams"],
        "cooperation_partners": ["Gemeente Almere", "zorg- en welzijnsorganisaties"],
        "scale": "almere_local",
        "funding_sources": ["unknown_needs_decision"],
        "decision_status": "source_backed_prefill",
        "evidence_sources": ["mun_almere_wijkteams"],
        "confidence": "medium",
        "open_issue": "Baseline function is public, but formal D6 classification and responsibility allocation remain unsettled.",
    },
    {
        "component_id": "stevige_lokale_teams",
        "component_label": "Stevige Lokale Teams",
        "existing_almere_provision": "Candidate council source indicates a 2026 start in two wijkteamgebieden and involvement of JGZ Almere and wijkteams.",
        "required_upgrade": "Ingest council dossier and underlying Documentwijzer documents before using as settled local decision evidence.",
        "owner": "Almere council/college line needs source-passage confirmation",
        "executors": ["JGZ Almere", "wijkteams", "schools and childcare partners"],
        "cooperation_partners": ["social and pedagogical basis", "specialists", "schools", "childcare", "JGZ Almere", "wijkteams"],
        "scale": "almere_local",
        "funding_sources": ["Investeringsfonds Jeugd en Gezin candidate", "unknown_needs_source_confirmation"],
        "decision_status": "source_backed_prefill",
        "evidence_sources": ["mun_almere_2026_stevige_lokale_teams_raad"],
        "confidence": "medium",
        "open_issue": "Direct page/search evidence is strong enough for intake priority, but underlying decision documents must be ingested.",
    },
    {
        "component_id": "jgz_almere",
        "component_label": "JGZ Almere",
        "existing_almere_provision": "GGD Flevoland public profile describes JGZ Almere as 0-18 jeugdgezondheidszorg with broader local configuration.",
        "required_upgrade": "Link JGZ Almere to SLT, school, Kansrijke Start, mental-health prevention and local team roles.",
        "owner": "JGZ Almere / GGD Flevoland, municipal governance needs confirmation",
        "executors": ["JGZ Almere"],
        "cooperation_partners": ["schools", "huisartsen", "Passend Onderwijs", "wijkteams", "jeugdhulp"],
        "scale": "almere_local_with_ggd_flevoland_governance",
        "funding_sources": ["GGD/JGZ funding needs source-specific split"],
        "decision_status": "source_backed_prefill",
        "evidence_sources": ["reg_ggd_flevoland_jgz_almere_profile", "reg_ggd_flevoland_begroting_2026"],
        "confidence": "medium",
        "open_issue": "Operational role is public, but exact D6 ownership and budget status need local validation.",
    },
    {
        "component_id": "ggd_flevoland_coordination",
        "component_label": "GGD Flevoland-coordinatie",
        "existing_almere_provision": "GGD Begroting 2026 is a candidate source for governance, public health, prevention and municipal contribution context.",
        "required_upgrade": "Ingest the 2026 budget and connect relevant sections to D6 governance, JGZ, Gezond Leven and monitoring.",
        "owner": "GGD Flevoland under six-municipality governance",
        "executors": ["GGD Flevoland"],
        "cooperation_partners": ["Flevoland municipalities", "Zorgzaam Flevoland/PGA", "public-health and prevention partners"],
        "scale": "ggd_regio_flevoland",
        "funding_sources": ["inwonerbijdrage", "municipal subsidies/plustaken", "other source-specific funding"],
        "decision_status": "source_backed_prefill",
        "evidence_sources": ["reg_ggd_flevoland_begroting_2026"],
        "confidence": "medium",
        "open_issue": "Separate GGD-region tasks from IZA/AZWA-region and Almere-local execution.",
    },
    {
        "component_id": "gezonde_school_mentale_gezonde_school",
        "component_label": "Gezonde School / mentale gezonde school",
        "existing_almere_provision": None,
        "required_upgrade": "Find Almere-specific implementation source and link to GGD/JGZ and schools.",
        "owner": None,
        "executors": ["GGD/JGZ candidate", "schools candidate"],
        "cooperation_partners": ["schools", "GGD/JGZ", "municipality", "youth partners"],
        "scale": "almere_local_or_ggd_regio_needs_validation",
        "funding_sources": ["unknown_needs_decision"],
        "decision_status": "review_needed",
        "evidence_sources": ["reg_ggd_flevoland_jgz_almere_profile"],
        "confidence": "low",
        "open_issue": "National D6 direction is clear, but local Almere implementation evidence still needs source intake.",
    },
    {
        "component_id": "kennis_advies_monitoring_dashboards",
        "component_label": "Kennis & Advies / monitoring / dashboards",
        "existing_almere_provision": "GGD Kennis en Advies page describes monitors, dashboards, epidemiology, data analysis and advice.",
        "required_upgrade": "Map which dashboards and monitors are used for D6 workagenda steering and who owns reporting.",
        "owner": "GGD Flevoland candidate, decision owner needs confirmation",
        "executors": ["GGD Flevoland Kennis en Advies"],
        "cooperation_partners": ["municipality", "regional programme structures", "knowledge institutions"],
        "scale": "ggd_regio_flevoland_with_almere_use",
        "funding_sources": ["unknown_needs_source_specific_split"],
        "decision_status": "source_backed_prefill",
        "evidence_sources": ["reg_ggd_flevoland_kennis_en_advies", "reg_ggd_flevoland_begroting_2026"],
        "confidence": "medium",
        "open_issue": "Public monitoring function is clear; D6-specific steering arrangement is not yet settled.",
    },
    {
        "component_id": "samen_sterker_wijk_mental_health",
        "component_label": "Samen Sterker in de Wijk / mentale-gezondheidswijkinfrastructuur",
        "existing_almere_provision": "Almere public pages describe Samen Sterker in de Wijk, partners, pilots, one-plan logic, steunkring and learning meetings.",
        "required_upgrade": "Decide whether this is formal D6 infrastructure, adjacent infrastructure or supporting implementation evidence.",
        "owner": "shared responsibility needs validation",
        "executors": ["Zorgplatform Flevoland partners", "local professionals and ervaringsdeskundigen"],
        "cooperation_partners": ["Triade", "GGZ Centraal", "Amethist", "Kwintes", "Leger des Heils", "GGD Flevoland", "Gemeente Almere"],
        "scale": "almere_local_and_regional_project_scale",
        "funding_sources": ["unknown_needs_decision"],
        "decision_status": "source_backed_prefill",
        "evidence_sources": ["mun_almere_samen_sterker_in_de_wijk_story", "mun_almere_samenwerkingsprojecten"],
        "confidence": "medium",
        "open_issue": "Public implementation evidence exists, but formal D6 classification and funding line are not settled.",
    },
    {
        "component_id": "pga_zorgzaam_flevoland_interface",
        "component_label": "Positief Gezond Almere / Zorgzaam Flevoland-interface",
        "existing_almere_provision": "Existing corpus includes PGA and Zorgzaam/Flevoland context.",
        "required_upgrade": "Update current cooperation evidence and separate PGA, Zorgzaam Flevoland/Flever and AZWA workagenda roles.",
        "owner": "shared programme roles need validation",
        "executors": [],
        "cooperation_partners": ["Gemeente Almere", "Zorgzaam Flevoland/Flever", "care and welfare partners"],
        "scale": "almere_local_and_iza_azwa_regio_flevoland",
        "funding_sources": ["PGA transformation funding candidate", "AZWA/D5/D6 funding needs separation"],
        "decision_status": "review_needed",
        "evidence_sources": ["mun_almere_pga_transformatieplan", "reg_zonmw_doorontwikkeling_zorgzaam_flevoland"],
        "confidence": "medium",
        "open_issue": "Avoid merging PGA transformation plan, AZWA workagenda and regular municipal funding without source-specific evidence.",
    },
    {
        "component_id": "digital_operational_infrastructure",
        "component_label": "Digitale en operationele infrastructuur",
        "existing_almere_provision": None,
        "required_upgrade": "Map RTP Almere, RSO, Monitoring@home and shared information picture only after source confirmation.",
        "owner": None,
        "executors": [],
        "cooperation_partners": [],
        "scale": "programme_or_project_scale_needs_validation",
        "funding_sources": ["unknown_needs_decision"],
        "decision_status": "review_needed",
        "evidence_sources": ["data/extracted/d6_governance_collaboration.json"],
        "confidence": "low",
        "open_issue": "Advice flags this component, but current register has no settled public Almere source.",
    },
    {
        "component_id": "citizen_initiatives_informal_support",
        "component_label": "Burgerinitiatieven en informele steun",
        "existing_almere_provision": None,
        "required_upgrade": "Inventory social-base partners, citizen initiatives, informal networks and relation to inloop/social support.",
        "owner": None,
        "executors": ["citizen initiatives candidate", "volunteer/informal support candidate"],
        "cooperation_partners": ["social work", "VMCA candidate", "De Schoor candidate", "neighbourhood networks"],
        "scale": "almere_local",
        "funding_sources": ["unknown_needs_decision"],
        "decision_status": "review_needed",
        "evidence_sources": ["data/extracted/d6_governance_collaboration.json"],
        "confidence": "low",
        "open_issue": "Needs public local source intake before partner names or ownership are used as facts.",
    },
    {
        "component_id": "funding_budget_alignment",
        "component_label": "Financiering en budgetafbakening",
        "existing_almere_provision": "National funding architecture is present in the existing corpus; Almere-specific D6 allocation is not settled.",
        "required_upgrade": "Map AZWA-D6, D5 workagenda, SPUK IZA, Brede SPUK/GALA, PGA transformation funding, municipal regular budget and Zvw lines per component.",
        "owner": "municipality and regional workagenda governance need component-specific validation",
        "executors": [],
        "cooperation_partners": ["mandaatgemeente", "preferente zorgverzekeraar", "financial controllers", "regional table"],
        "scale": "mixed_scale_must_be_split",
        "funding_sources": ["unknown_needs_decision"],
        "decision_status": "decision_needed",
        "evidence_sources": ["data/extracted/workagenda_d5_operational_requirements.json"],
        "confidence": "medium",
        "open_issue": "This is the main anti-dubbeltelling control point for D6.",
    },
]


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def enrich_component(component: dict[str, Any], source_index: dict[str, dict[str, Any]]) -> dict[str, Any]:
    evidence = []
    for source_id in component["evidence_sources"]:
        source = source_index.get(source_id)
        if source:
            evidence.append(
                {
                    "source_id": source_id,
                    "title": source["title"],
                    "source_url": source["source_url"],
                    "repository_status": source["repository_status"],
                    "verification_status": source["verification_status"],
                }
            )
        else:
            evidence.append({"source_id": source_id, "repository_status": "existing_repository_layer_or_prior_source"})

    human_review_needed = component["decision_status"] != "settled"
    return {
        **component,
        "evidence": evidence,
        "human_review_needed": human_review_needed,
        "fact_interpretation_proposal_status": (
            "public_prefill_needs_local_validation"
            if component["decision_status"] in {"source_backed_prefill", "review_needed"}
            else "decision_needed"
        ),
    }


def build_payload() -> dict[str, Any]:
    d6_governance = load_json(D6_GOVERNANCE_PATH, {})
    source_index = {source["source_id"]: source for source in PUBLIC_SOURCE_CANDIDATES}
    components = [enrich_component(component, source_index) for component in COMPONENTS]

    return {
        "layer_run_id": "phase25_4b_almere_d6_responsibility_register_v1",
        "generated_on": date.today().isoformat(),
        "status": "active_sprint_support",
        "sprint": "25.4b D6 Almere responsibility pack",
        "purpose": (
            "Create an execution-oriented D6 Almere register that separates public prefill, "
            "local validation, decision needs, scale, funding, and evidence status."
        ),
        "public_source_boundary": (
            "This register is public-source prefill. It does not settle local ownership, execution, "
            "budget or D6 classification without ingested decision sources or local validation."
        ),
        "inputs": [
            "docs/phase25-sprint25.4-d6-almere-responsibility-pack-plan.md",
            "data/extracted/d6_governance_collaboration.json",
            "public URL verification performed 2026-04-26",
        ],
        "summary": {
            "component_count": len(components),
            "candidate_source_count": len(PUBLIC_SOURCE_CANDIDATES),
            "source_backed_prefill_count": sum(
                1 for component in components if component["decision_status"] == "source_backed_prefill"
            ),
            "review_needed_count": sum(1 for component in components if component["decision_status"] == "review_needed"),
            "decision_needed_count": sum(1 for component in components if component["decision_status"] == "decision_needed"),
            "d6_prefill_dimension_count": (d6_governance.get("summary") or {}).get("dimension_count"),
        },
        "scale_guardrail": (
            "Keep Almere-local, IZA/AZWA-regio Flevoland, GGD-regio Flevoland, zorgkantoorregio "
            "and project/programme scale separate in every D6 row."
        ),
        "public_source_candidates": PUBLIC_SOURCE_CANDIDATES,
        "components": components,
        "next_actions": [
            "Ingest the highest-priority verified public sources into data/raw/manifest.json.",
            "Convert council Documentwijzer attachments for Stevige Lokale Teams to page-markdown before claim extraction.",
            "Regenerate inventory, structural extraction, claims, D6 layers, QC and dashboard after formal source intake.",
            "Ask local employees to validate D6 classification, owner, executor, budget and monitoring fields after public-source exhaustion.",
        ],
    }


def main() -> None:
    payload = build_payload()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"Components: {payload['summary']['component_count']}")


if __name__ == "__main__":
    main()
