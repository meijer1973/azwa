from __future__ import annotations

import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "data" / "raw" / "manifest.json"
INVENTORY_PATH = REPO_ROOT / "data" / "extracted" / "document_inventory.json"
WORKAGENDA_PATH = REPO_ROOT / "data" / "extracted" / "workagenda_d5_operational_requirements.json"
OUTPUT_PATH = REPO_ROOT / "data" / "extracted" / "local_source_strengthening_almere.json"


FOCUS_DOCUMENT_IDS = [
    "mun_almere_2024_2026_visie_gezondheidsbeleid",
    "mun_almere_2024_2034_maatschappelijke_agenda",
    "mun_almere_pga_transformatieplan",
    "mun_almere_pga_seo_businesscase_2024",
    "reg_flevoland_2023_regioplan_iza",
    "reg_flevoland_2023_regiobeeld",
    "nat_azwa_opdracht_werkagenda_d5_2026",
    "nat_azwa_format_werkagenda_d5_2026",
    "nat_azwa_toelichting_producten_proces_2026",
]


SOURCE_CANDIDATES = [
    {
        "candidate_id": "mun_almere_2024_2034_maatschappelijke_agenda_underlying_documents",
        "title": "Onderliggende stukken Maatschappelijke agenda 2024-2034",
        "publisher": "Raad van Almere / Documentwijzer",
        "source_url": "https://documentwijzer.raadvanalmere.nl/app/instrument/24161",
        "verification_status": "candidate_url_verified",
        "intake_status": "selected_documents_converted_and_ingested",
        "current_repository_status": "selected_primary_documents_present",
        "current_document_id": "mun_almere_2024_2034_maatschappelijke_agenda_beleidstekst",
        "why_it_matters": "Replaces the weaker Agendawijzer summary page with the council proposal, attachments, amendments, and adopted decision material.",
        "public_probe_status": "downloaded_public_notubiz_attachments",
        "usefulness_read": "High. The public dossier contains the policy text, raadsvoorstel, geamendeerd raadsvoorstel, besluitenlijsten, collegevoorstel, evaluation setup, ASD advice, and process documents.",
        "intake_recommendation": "review_ingested_claims_before_public_use",
        "recommended_for_corpus": [
            "Maatschappelijke agenda 2024-2034 (policy text)",
            "Raadsvoorstel Maatschappelijke agenda 2024-2034 - geamendeerd",
            "Besluitenlijst final decision route",
            "Opzet procesevaluatie en monitor Sociaal Domein",
        ],
        "exclude_or_defer": [
            "Gesprekswijzers and duplicate debate/process documents unless needed for decision history",
            "ASD advice and college reaction as supporting review material, not core policy baseline",
        ],
        "privacy_scope": "Public council documents only; avoid extracting personal contact details or speaker lists into public claims.",
        "unlocks": ["locality", "governance", "execution"],
        "workagenda_targets": [
            "laagdrempelige_steunpunten",
            "sociaal_verwijzen",
            "ketenaanpak_overgewicht_obesitas_volwassenen",
            "ontwikkelagenda_2_overige_initiatieven",
        ],
        "review_question": "Download the actual Documentwijzer attachments and decide which are primary policy sources versus supporting council-process records.",
    },
    {
        "candidate_id": "mun_almere_2024_2026_visie_gezondheidsbeleid_underlying_documents",
        "title": "Onderliggende stukken Visie Gezondheidsbeleid Almere 2024-2026",
        "publisher": "Raad van Almere / Documentwijzer",
        "source_url": "https://documentwijzer.raadvanalmere.nl/app/instrument/24118",
        "verification_status": "candidate_url_verified",
        "intake_status": "selected_documents_converted_and_ingested",
        "current_repository_status": "selected_primary_documents_present",
        "current_document_id": "mun_almere_2024_2026_visie_gezondheidsbeleid_beleidstekst",
        "why_it_matters": "Replaces the weaker Agendawijzer summary page with the adopted local health-policy text and decision trail.",
        "public_probe_status": "downloaded_public_notubiz_attachments",
        "usefulness_read": "High. The public dossier contains the adopted health vision, raadsvoorstel/geamendeerd raadsvoorstel, collegevoorstel, besluitenlijsten, ASD advice, and the GALA/Brede SPUK plan of approach.",
        "intake_recommendation": "review_ingested_claims_before_public_use",
        "recommended_for_corpus": [
            "Visie Gezondheidsbeleid Almere 2024-2026",
            "Raadsvoorstel Visie Gezondheidsbeleid Almere 2024-2026 - geamendeerd",
            "Besluitenlijst final decision route",
            "Integraal plan van aanpak 2024-2026 Brede SPUK/GALA publicatieversie",
        ],
        "exclude_or_defer": [
            "Gesprekswijzers and duplicate process documents unless needed for decision chronology",
            "ASD advice as supporting review material, not core policy baseline",
            "PGA transformatieplan attachment if it duplicates the already-ingested PGA source",
        ],
        "privacy_scope": "Public council documents only; avoid extracting personal contact details or speaker lists into public claims.",
        "unlocks": ["locality", "governance", "execution", "time"],
        "workagenda_targets": [
            "valpreventie",
            "ketenaanpak_overgewicht_obesitas_volwassenen",
            "kansrijke_start",
            "ketenaanpak_overgewicht_obesitas_kinderen",
        ],
        "review_question": "Download the actual Documentwijzer attachments and separate adopted policy text from motions, amendments, and debate notes.",
    },
    {
        "candidate_id": "mun_almere_2025_stand_van_zaken_gezondheidsbeleid_iza_gala",
        "title": "Raadsbrief Stand van zaken Gezondheidsbeleid (IZA en GALA)",
        "publisher": "Gemeente Almere / Raad van Almere",
        "source_url": None,
        "verification_status": "not_found_in_public_search_2026_04_24",
        "intake_status": "deferred_to_local_validation_workflow",
        "current_repository_status": "not_present",
        "current_document_id": None,
        "why_it_matters": "The deep-research note treats this as a likely local bridge source for IZA/GALA status, but it should not be used as fact until the primary source is found.",
        "public_probe_status": "not_found",
        "usefulness_read": "Unknown. No public source was found in the public-search probe, so the existence and contents cannot be treated as grounded.",
        "intake_recommendation": "do_not_block_public_workagenda_structure",
        "recommended_for_corpus": [],
        "exclude_or_defer": [
            "All claims depending on this source until a public document URL is found or local staff provide a usable source."
        ],
        "privacy_scope": "Do not use non-public correspondence or private mailbox copies.",
        "unlocks": ["locality", "governance", "money", "execution", "time"],
        "workagenda_targets": ["all_d5_workagenda_targets"],
        "review_question": "Treat as a later local-validation lookup; do not block the public-source workagenda structure on this document.",
    },
    {
        "candidate_id": "reg_ggd_flevoland_2024_gezondheidsmonitor_volwassenen_ouderen",
        "title": "Gezondheidsmonitor Volwassenen en Ouderen 2024",
        "publisher": "GGD Flevoland",
        "source_url": "https://www.ggdflevoland.nl/professional/kennis-en-advies/gezondheidsmonitors/gezondheids-monitor-volwassenen-en-ouderen/",
        "verification_status": "candidate_url_verified",
        "intake_status": "selected_table_books_ingested",
        "current_repository_status": "partially_present_selected_table_books",
        "current_document_id": None,
        "why_it_matters": "Provides current municipal baseline data for overgewicht, valrisico, eenzaamheid, mentale gezondheid, bewegen, and vulnerability.",
        "public_probe_status": "downloaded_public_ggd_table_books",
        "usefulness_read": "High. The public GGD page links municipality-level 2024 table books for adults and older residents. These directly support D5 nulmeting and capacity work.",
        "intake_recommendation": "use_ingested_table_books_for_sprint_25_3",
        "recommended_for_corpus": [
            "Tabellenboek Volwassenen 2024 Gemeenten",
            "Tabellenboek Ouderen 2024 Gemeenten",
        ],
        "exclude_or_defer": [
            "Province-only table books unless needed for comparison",
            "Narrative trend pages when the table books provide cleaner source data",
        ],
        "privacy_scope": "Aggregated public statistics only; no individual-level health data.",
        "unlocks": ["locality", "execution"],
        "workagenda_targets": [
            "valpreventie",
            "ketenaanpak_overgewicht_obesitas_volwassenen",
            "sociaal_verwijzen",
            "laagdrempelige_steunpunten",
        ],
        "review_question": "Ingest the adult and older-person tables separately and preserve municipality-level Almere rows for later capacity calculations.",
    },
    {
        "candidate_id": "reg_ggd_flevoland_2024_tabellenboek_volwassenen",
        "title": "Tabellenboek volwassenen 2024 - Flevoland alle gemeenten",
        "publisher": "GGD Flevoland",
        "source_url": "https://www.ggdflevoland.nl/app/uploads/sites/6/2024/12/Gezondheidsmonitor-Volwassenen-en-Ouderen-alle-gemeenten-van-Flevoland-2024_volwassenen-18-64.pdf",
        "verification_status": "source_url_verified",
        "intake_status": "ingested_formal_corpus",
        "current_repository_status": "present",
        "current_document_id": "reg_ggd_flevoland_2024_volwassenen_gemeenten",
        "why_it_matters": "Primary table source for adult Almere indicators needed in workagenda prioritization.",
        "public_probe_status": "downloaded_public_ggd_table_book",
        "usefulness_read": "High. The PDF contains municipality-level adult percentages for Almere, including overgewicht, obesitas, beweegrichtlijn, eenzaamheid, anxiety/depression risk, broze gezondheid, mantelzorg, and vrijwilligerswerk.",
        "intake_recommendation": "use_as_table_source_after_human_review",
        "recommended_for_corpus": ["Tabellenboek Volwassenen 2024 Gemeenten"],
        "exclude_or_defer": [],
        "privacy_scope": "Aggregated public statistics only; no individual-level health data.",
        "unlocks": ["locality", "execution"],
        "workagenda_targets": ["ketenaanpak_overgewicht_obesitas_volwassenen", "sociaal_verwijzen"],
        "review_question": "Add as raw regional source and keep table extraction separate from narrative policy claims.",
    },
    {
        "candidate_id": "reg_ggd_flevoland_valpreventie_almere",
        "title": "Valpreventie",
        "publisher": "GGD Flevoland",
        "source_url": "https://www.ggdflevoland.nl/positief-ouder-worden/valpreventie/",
        "verification_status": "source_url_verified",
        "intake_status": "ingested_formal_corpus",
        "current_repository_status": "present",
        "current_document_id": "reg_ggd_flevoland_valpreventie_almere",
        "why_it_matters": "Operational source for current Almere valpreventie intake/inloop signals and delivery context.",
        "public_probe_status": "downloaded_general_and_almere_specific_pages",
        "usefulness_read": "High for operational layer. The Almere-specific public page describes free inloop/no-registration, personal advice, course matching, and central coordinator follow-up within two weeks.",
        "intake_recommendation": "use_as_operational_context_after_human_review",
        "recommended_for_corpus": ["Valpreventie Gemeente Almere - GGD Flevoland"],
        "exclude_or_defer": ["General valpreventie landing page unless needed for regional comparison."],
        "privacy_scope": "Public service route only; do not extract form submissions or any resident-level data.",
        "unlocks": ["locality", "execution"],
        "workagenda_targets": ["valpreventie"],
        "review_question": "Extract only current operational routes and dates; avoid treating event announcements as durable policy.",
    },
    {
        "candidate_id": "reg_zonmw_doorontwikkeling_zorgzaam_flevoland",
        "title": "Doorontwikkeling Zorgzaam Flevoland naar een toekomstbestendige samenwerkingsstructuur",
        "publisher": "ZonMw",
        "source_url": "https://projecten.zonmw.nl/nl/project/doorontwikkeling-zorgzaam-flevoland-naar-een-toekomstbestendige-samenwerkingsstructuur",
        "verification_status": "source_url_verified",
        "intake_status": "ingested_formal_corpus",
        "current_repository_status": "present",
        "current_document_id": "reg_zonmw_doorontwikkeling_zorgzaam_flevoland",
        "why_it_matters": "Strengthens the regional governance story around Zorgzaam Flevoland, including Almere as responsible organization in a 2025-2027 development route.",
        "public_probe_status": "downloaded_public_project_page",
        "usefulness_read": "Medium-high. Useful for governance and regional collaboration, but it is a project registration rather than a formal policy decision.",
        "intake_recommendation": "use_as_supporting_governance_source_after_human_review",
        "recommended_for_corpus": ["ZonMw project page Doorontwikkeling Zorgzaam Flevoland"],
        "exclude_or_defer": ["Do not treat as adopted local policy or complete governance mandate."],
        "privacy_scope": "Use organization/project facts only; avoid named-person contact details.",
        "unlocks": ["governance", "locality", "execution"],
        "workagenda_targets": ["all_d5_workagenda_targets"],
        "review_question": "Check whether this is a project registration, grant decision, or substantive governance source before promoting it as evidence.",
    },
    {
        "candidate_id": "reg_mgn_flevoland_almere_mandaatgemeente",
        "title": "Alle netwerken - Mentale gezondheidsnetwerken",
        "publisher": "Mentale gezondheidsnetwerken",
        "source_url": "https://www.mentalegezondheidsnetwerken.nl/alle-netwerken/",
        "verification_status": "source_url_verified",
        "intake_status": "deferred_to_sanitized_role_extract",
        "current_repository_status": "covered_in_regional_role_guardrail_not_manifest",
        "current_document_id": None,
        "why_it_matters": "Clarifies that Almere is listed as mandaatgemeente for the Flevoland mental-health network and that Zeewolde is in a different listed route.",
        "public_probe_status": "downloaded_public_listing",
        "usefulness_read": "High for the narrow role question. The page supports Almere as mandaatgemeente for MGN Flevoland and separates Zeewolde into the Gezond Veluwe listing.",
        "intake_recommendation": "carry_forward_to_role_validation_workflow",
        "recommended_for_corpus": ["Mentale gezondheidsnetwerken listing, limited to network geography and role fields"],
        "exclude_or_defer": ["Named contact people, phone numbers, and email addresses."],
        "privacy_scope": "Contains public personal contact details; formal corpus extraction should suppress contact data and retain only organization/role/geography facts.",
        "unlocks": ["governance", "locality", "execution"],
        "workagenda_targets": ["mentale_gezondheidsnetwerken", "laagdrempelige_steunpunten", "sociaal_verwijzen"],
        "review_question": "Carry forward as a later role/geography validation task; do not block public-source workagenda structuring.",
    },
    {
        "candidate_id": "mun_almere_2024_programmarekening_pga_iza_gala",
        "title": "Programmarekening 2024",
        "publisher": "Gemeente Almere",
        "source_url": "https://almere.jaarverslag-2024.nl/assets/docs/Programmarekening_2024.pdf",
        "verification_status": "source_url_verified",
        "intake_status": "public_document_downloaded_for_assessment",
        "current_repository_status": "not_present",
        "current_document_id": None,
        "why_it_matters": "Potential municipal financial and execution-status source for PGA, IZA and GALA references in Almere's own accountability cycle.",
        "public_probe_status": "downloaded_public_pdf",
        "usefulness_read": "Medium. Useful for financial/accountability context, but very broad and not a clean first intake source for D5 operational requirements.",
        "intake_recommendation": "defer_or_ingest_later_as_financial_context",
        "recommended_for_corpus": [],
        "exclude_or_defer": ["Defer until money/governance sprint unless a specific PGA/IZA/GALA passage is needed."],
        "privacy_scope": "Public annual-account document; avoid irrelevant accounting or signature material in extracted claims.",
        "unlocks": ["money", "governance", "time", "execution"],
        "workagenda_targets": ["all_d5_workagenda_targets"],
        "review_question": "Use as a local accountability source, not as a replacement for the actual policy or workagenda documents.",
    },
    {
        "candidate_id": "nat_cbs_2025_bevolkingsgroei_almere",
        "title": "Bevolkingsgroei in 2024 afgenomen in de Randstad, toegenomen daarbuiten",
        "publisher": "CBS",
        "source_url": "https://www.cbs.nl/nl-nl/nieuws/2025/05/bevolkingsgroei-in-2024-afgenomen-in-de-randstad-toegenomen-daarbuiten",
        "verification_status": "source_url_verified",
        "intake_status": "public_html_downloaded_for_assessment",
        "current_repository_status": "not_present",
        "current_document_id": None,
        "why_it_matters": "Useful context for growth pressure, but exact workagenda calculations should use a chosen BRP/CBS peildatum.",
        "public_probe_status": "downloaded_public_news_page",
        "usefulness_read": "Low-medium for corpus. The article is useful context for growth pressure but should not be the denominator source for capacity calculations.",
        "intake_recommendation": "do_not_ingest_for_25_2_or_defer_as_context",
        "recommended_for_corpus": [],
        "exclude_or_defer": ["Use a stable CBS/BRP table in Sprint 25.3 instead of this news page for calculations."],
        "privacy_scope": "Aggregated public statistics only.",
        "unlocks": ["locality", "execution"],
        "workagenda_targets": ["sociaal_verwijzen", "valpreventie", "ketenaanpak_overgewicht_obesitas_kinderen"],
        "review_question": "Do not use news-rate figures as denominator data; choose a stable population table for calculations in Sprint 25.3.",
    },
]


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_index(manifest: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {entry["document_id"]: entry for entry in manifest}


def inventory_index(inventory: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {entry["document_id"]: entry for entry in inventory.get("documents", [])}


def summarize_existing_sources(
    manifest: list[dict[str, Any]],
    inventory: dict[str, Any],
) -> list[dict[str, Any]]:
    manifest_by_id = manifest_index(manifest)
    inventory_by_id = inventory_index(inventory)
    rows: list[dict[str, Any]] = []

    for document_id in FOCUS_DOCUMENT_IDS:
        manifest_entry = manifest_by_id.get(document_id)
        inventory_entry = inventory_by_id.get(document_id)
        if not manifest_entry and not inventory_entry:
            rows.append(
                {
                    "document_id": document_id,
                    "present_in_manifest": False,
                    "present_in_inventory": False,
                    "repository_status": "missing_from_current_formal_source_layer",
                }
            )
            continue

        source_classification = (inventory_entry or {}).get("source_classification")
        curation_bucket = (inventory_entry or {}).get("curation_bucket")
        repository_status = "present"
        if source_classification == "derivative" or curation_bucket == "context":
            repository_status = "present_but_weaker_or_contextual"

        rows.append(
            {
                "document_id": document_id,
                "title": (manifest_entry or inventory_entry or {}).get("title"),
                "short_title": (manifest_entry or inventory_entry or {}).get("short_title"),
                "publisher": (manifest_entry or inventory_entry or {}).get("publisher"),
                "source_url": (manifest_entry or inventory_entry or {}).get("source_url"),
                "file_path": (manifest_entry or inventory_entry or {}).get("file_path"),
                "jurisdiction_level": (manifest_entry or inventory_entry or {}).get("jurisdiction_level"),
                "document_type": (manifest_entry or inventory_entry or {}).get("document_type"),
                "source_classification": source_classification,
                "curation_bucket": curation_bucket,
                "present_in_manifest": manifest_entry is not None,
                "present_in_inventory": inventory_entry is not None,
                "repository_status": repository_status,
                "inventory_notes": (inventory_entry or {}).get("inventory_notes"),
            }
        )

    return rows


def build_gap_summary(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_unlock: Counter[str] = Counter()
    by_status: Counter[str] = Counter()
    by_intake: Counter[str] = Counter()

    for candidate in candidates:
        by_status[candidate["verification_status"]] += 1
        by_intake[candidate["intake_status"]] += 1
        for perspective in candidate["unlocks"]:
            by_unlock[perspective] += 1

    return [
        {"group": "verification_status", "counts": dict(sorted(by_status.items()))},
        {"group": "intake_status", "counts": dict(sorted(by_intake.items()))},
        {"group": "perspective_unlocked", "counts": dict(sorted(by_unlock.items()))},
    ]


def workagenda_target_index(workagenda: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {target["target_id"]: target for target in workagenda.get("targets", [])}


def annotate_target_source_needs(
    candidates: list[dict[str, Any]],
    workagenda: dict[str, Any],
) -> list[dict[str, Any]]:
    target_index = workagenda_target_index(workagenda)
    target_ids = sorted(target_index)
    rows: list[dict[str, Any]] = []

    for target_id in target_ids:
        related_candidates = [
            candidate
            for candidate in candidates
            if target_id in candidate.get("workagenda_targets", [])
            or "all_d5_workagenda_targets" in candidate.get("workagenda_targets", [])
        ]
        rows.append(
            {
                "target_id": target_id,
                "title": target_index[target_id].get("title"),
                "candidate_source_count": len(related_candidates),
                "candidate_source_ids": [candidate["candidate_id"] for candidate in related_candidates],
                "still_needs_local_decision": True,
                "note": (
                    "Candidate sources can strengthen baseline and role evidence, but local choices remain unset "
                    "until Almere or the regional table records target-specific decisions."
                ),
            }
        )

    return rows


def build_payload() -> dict[str, Any]:
    manifest = load_json(MANIFEST_PATH, [])
    inventory = load_json(INVENTORY_PATH, {"documents": []})
    workagenda = load_json(WORKAGENDA_PATH, {"targets": []})
    local_manifest_count = sum(1 for entry in manifest if entry.get("jurisdiction_level") == "municipal")
    regional_manifest_count = sum(1 for entry in manifest if entry.get("jurisdiction_level") == "regional")

    return {
        "layer_run_id": "phase25_2_local_source_strengthening_v1",
        "generated_on": date.today().isoformat(),
        "status": "completed_public_source_intake",
        "sprint": "25.2 Lokale bronversterking Almere",
        "summary": {
            "manifest_document_count": len(manifest),
            "municipal_manifest_document_count": local_manifest_count,
            "regional_manifest_document_count": regional_manifest_count,
            "candidate_source_count": len(SOURCE_CANDIDATES),
            "verified_or_candidate_url_count": sum(
                1
                for candidate in SOURCE_CANDIDATES
                if candidate["verification_status"] in {"source_url_verified", "candidate_url_verified"}
            ),
            "not_found_candidate_count": sum(
                1 for candidate in SOURCE_CANDIDATES if candidate["verification_status"].startswith("not_found")
            ),
        },
        "guardrail": (
            "This layer is a source-intake and review aid. Candidate sources are not claim facts until the primary "
            "source has been ingested or manually checked."
        ),
        "workflow_boundary": (
            "Sprint 25.2 closes when the public-source structure is filled as far as the public corpus allows. "
            "Missing non-public material, local staff validation, and decision requests are carryover workflow tasks, "
            "not blockers for this public-source intake sprint."
        ),
        "privacy_policy": (
            "Sprint 25.2 uses only public sources. Do not add private correspondence, non-public personal data, "
            "or resident-level health data. Public pages that contain named contacts may be used only for "
            "organization, role, geography, and policy facts; suppress phone numbers, email addresses, and "
            "named-person contact details in extracted claims and public text."
        ),
        "public_probe_folder": "docs/internal/source-intake/phase25.2-public-source-probe",
        "existing_focus_sources": summarize_existing_sources(manifest, inventory),
        "candidate_sources": SOURCE_CANDIDATES,
        "gap_summary": build_gap_summary(SOURCE_CANDIDATES),
        "target_source_needs": annotate_target_source_needs(SOURCE_CANDIDATES, workagenda),
        "next_actions": [
            "Review the generated claims from the selected Documentwijzer attachments before relying on them in public or bestuurlijke text.",
            "Review the ingested GGD Flevoland 2024 table-book claims before using them for Sprint 25.3 nulmeting calculations.",
            "Carry the MGN role/geography question forward to a sanitized role-validation workflow.",
            "Carry the missing 2 February 2025 raadsbrief forward to local-staff validation if public search remains exhausted.",
            "Use this layer to drive Sprint 25.3 nulmeting/capacity work, especially target-level denominators and current provision.",
        ],
    }


def main() -> None:
    payload = build_payload()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"Candidate sources: {payload['summary']['candidate_source_count']}")


if __name__ == "__main__":
    main()
