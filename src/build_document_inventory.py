from __future__ import annotations

import json
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "data" / "raw" / "manifest.json"
OUTPUT_PATH = REPO_ROOT / "data" / "extracted" / "document_inventory.json"


ANNOTATIONS = {
    "nat_azwa_2025_definitief": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": True,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Definitive national agreement text and the main normative source for AZWA-wide D5/D6 extraction.",
    },
    "nat_azwa_2025_onderhandelaarsakkoord": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": True,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Substantive predecessor agreement that is useful for tracing pre-final wording and commitments.",
    },
    "nat_azwa_2026_cw31_kader_d5_d6": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": True,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "The most targeted D5/D6 framework document in the corpus, including finance and evaluation framing.",
    },
    "reg_flevoland_2023_regioplan_iza": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Regional IZA implementation plan with strong governance, monitoring, and Almere relevance; "
            "it contains structured visuals, but not stable table evidence we currently want to treat as "
            "table-bearing for downstream extraction."
        ),
    },
    "mun_almere_pga_transformatieplan": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Core local implementation source for Almere, but not itself a D5/D6 source document.",
    },
    "nat_azwa_2026_cw31_kamerbrief": {
        "source_classification": "derivative",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": False,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Transmittal letter for the CW 3.1 annexes; useful for status and official framing rather than detailed extraction.",
    },
    "nat_azwa_2026_voortgang_kamerbrief": {
        "source_classification": "derivative",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Progress letter with important implementation, monitoring, and regionalization details for D5/D6 rollout.",
    },
    "nat_azwa_2025_aanbiedingsbrief": {
        "source_classification": "derivative",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Short offering letter that confirms signature status and gives limited interpretive context.",
    },
    "nat_iza_2022_integraal_zorgakkoord": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": True,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Upstream national agreement that provides the main pre-AZWA governance and monitoring context.",
    },
    "nat_gala_2023_gezond_en_actief_leven": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": True,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Upstream public-health and municipal implementation agreement relevant to prevention and social-basis context.",
    },
    "mun_almere_pga_seo_businesscase_2024": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": True,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Commissioned research and business-case report that can support local claim and impact interpretation.",
    },
    "reg_flevoland_2023_regiobeeld": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": False,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Regional baseline evidence report for needs, pressures, and context rather than normative policy "
            "content; the current corpus behaves as narrative/regional evidence, not as a reliable table source."
        ),
    },
    "nat_vng_azwa_faq_middelen": {
        "source_classification": "supporting_commentary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": False,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Practical VNG funding explainer; useful for implementation context but weaker than the underlying agreements.",
    },
    "nat_vng_azwa_faq_uitvoeringscapaciteit": {
        "source_classification": "supporting_commentary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Practical VNG implementation-capacity explainer with municipal relevance but low normative weight.",
    },
    "mun_almere_2024_2034_maatschappelijke_agenda": {
        "source_classification": "derivative",
        "curation_bucket": "context",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Agendawijzer summary page that points to underlying municipal documents rather than replacing them.",
    },
    "mun_almere_2024_2026_visie_gezondheidsbeleid": {
        "source_classification": "derivative",
        "curation_bucket": "context",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Agendawijzer summary page with useful local policy signals but not the full policy text.",
    },
    "mun_almere_sociaal_domein_informatiepagina": {
        "source_classification": "supporting_commentary",
        "curation_bucket": "context",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "General orientation page that links the local policy landscape but is not itself a source of detailed claims.",
    },
    "mun_almere_sociale_staat_gateway": {
        "source_classification": "supporting_commentary",
        "curation_bucket": "context",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": False,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Gateway page that should eventually be replaced by the linked underlying reports.",
    },
    "nat_dusi_spuk_transformatiemiddelen_2024_2028": {
        "source_classification": "derivative",
        "curation_bucket": "context",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Official DUS-I implementation page with concrete application and accountability deadlines for "
            "transformatiemiddelen; useful for timeline and municipal follow-up, but not itself the strongest norm."
        ),
    },
    "nat_wetten_spuk_transformatiemiddelen_regeling": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Formal regulation for SPUK transformatiemiddelen and therefore the strongest source in this repo "
            "for application windows, funding conditions, and accountability logic."
        ),
    },
    "nat_zorgakkoorden_azwa_programmapagina_2025": {
        "source_classification": "derivative",
        "curation_bucket": "context",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Official AZWA program page that aggregates updates, references, and practical follow-up material; "
            "useful for traceability and timeline discovery rather than as a standalone norm."
        ),
    },
    "mun_almere_begroting_2026_webpagina": {
        "source_classification": "derivative",
        "curation_bucket": "context",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Official Almere budget page that exposes local budget-cycle milestones and can later anchor "
            "municipal timing around financing and council decision moments."
        ),
    },
    "nat_bzk_gemeentefonds_cyclus": {
        "source_classification": "derivative",
        "curation_bucket": "context",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": False,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Official BZK information page for the gemeentefonds cycle; useful to anchor recurring financial "
            "moments such as the mei-, september-, and decembercirculaires in a source-backed way."
        ),
    },
    "nat_vng_gezond_en_actief_leven_2026": {
        "source_classification": "derivative",
        "curation_bucket": "context",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Current VNG subject page for IZA, GALA, and AZWA support for municipalities; it is a better active "
            "replacement for the earlier dead VNG topic URL and helps trace practical municipal support signals."
        ),
    },
    "nat_vng_ledenbrief_onderhandelaarsakkoord_azwa_2025": {
        "source_classification": "derivative",
        "curation_bucket": "context",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": True,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "VNG members letter on the AZWA negotiation agreement, including municipal framing, financing, and a "
            "clear Q3 2026 regioplan timing reference; lower-authority than national norm text but stronger than "
            "sector commentary."
        ),
    },
    "nat_sociaalwerknl_financiering_iza_azwa_2025": {
        "source_classification": "derivative",
        "curation_bucket": "context",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Sector commentary page that summarizes IZA/AZWA financing and mentions regional follow-up timing, "
            "including the additional regioplan trajectory; useful for timeline discovery and municipal follow-up, "
            "but intentionally treated as lower-authority duiding."
        ),
    },
    "mun_almere_raad_vergaderschema_2026": {
        "source_classification": "derivative",
        "curation_bucket": "context",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Official Raad van Almere schedule page with political-market, election, and council-transition moments "
            "that can anchor local governance timing around later D5/D6 follow-up."
        ),
    },
    "nat_vng_brief_azwa_financiering_webpagina_2026": {
        "source_classification": "derivative",
        "curation_bucket": "context",
        "contains_d5": True,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "VNG landing page for the 22 April 2026 AZWA financing update, linking the ledenbrief and the attached "
            "workagenda documents that structure the 2026 municipal follow-up."
        ),
    },
    "nat_vng_ledenbrief_azwa_financiering_2026": {
        "source_classification": "derivative",
        "curation_bucket": "context",
        "contains_d5": True,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Current VNG ledenbrief that explains the new AZWA financing route for gemeenten and points to the "
            "required D5 workagenda, webinar, and municipal approval moment in November 2026."
        ),
    },
    "nat_vws_brief_azwa_d5_d6_financieringsinstrument_2026": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Official VWS letter to VNG on the D5/D6 agreements and the financing instrument, including the move "
            "toward a new SPUK for 2027-2029 and the municipal implementation framing for 2026."
        ),
    },
    "nat_azwa_opdracht_werkagenda_d5_2026": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Operational source document for the D5 workagenda, with the concrete products, milestones, and "
            "regional-to-municipal process needed to unlock the AZWA middelen."
        ),
    },
    "nat_azwa_format_werkagenda_d5_2026": {
        "source_classification": "derivative",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Operational AZWA format for the D5 workagenda, useful for tracing which local and regional fields, "
            "planning elements, and implementation commitments are expected in 2026."
        ),
    },
    "nat_azwa_toelichting_producten_proces_2026": {
        "source_classification": "derivative",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Short process note that explains the D5 workagenda products, the relation to the regioplan, and the "
            "target dates around 26 May, mid-September, and 15 November 2026."
        ),
    },
    "reg_ggd_flevoland_2024_volwassenen_gemeenten": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": True,
        "contains_financing_logic": False,
        "contains_governance_logic": False,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Public GGD Flevoland municipality-level table book for adults aged 18-64. Use as aggregate baseline "
            "evidence for Sprint 25.3 nulmeting fields such as overgewicht, bewegen, eenzaamheid, mentale "
            "gezondheid, kwetsbaarheid, and participation. It is not individual-level health data."
        ),
    },
    "reg_ggd_flevoland_2024_ouderen_gemeenten": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": True,
        "contains_financing_logic": False,
        "contains_governance_logic": False,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Public GGD Flevoland municipality-level table book for residents aged 65 and older. Use as aggregate "
            "baseline evidence for Sprint 25.3 nulmeting fields such as valrisico, eenzaamheid, gezondheid, "
            "bewegen, kwetsbaarheid, mantelzorg, and participation. It is not individual-level health data."
        ),
    },
    "reg_ggd_flevoland_valpreventie_almere": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": False,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Public Almere-specific GGD Flevoland page for the valpreventie service route. Use only for current "
            "operational execution evidence such as inloop, referral, advice, and course matching; avoid treating "
            "event details as durable policy."
        ),
    },
    "reg_zonmw_doorontwikkeling_zorgzaam_flevoland": {
        "source_classification": "derivative",
        "curation_bucket": "context",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "ZonMw project registration for development of Zorgzaam Flevoland. Use as supporting governance and "
            "collaboration evidence only; it is not an adopted local policy document or a complete mandate source."
        ),
    },
    "mun_almere_2024_2026_visie_gezondheidsbeleid_beleidstekst": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Underlying municipal policy text for the Almere health-policy vision. It replaces the earlier "
            "Agendawijzer summary as the stronger local source for local prevention, health, and care-to-social-domain "
            "translation signals."
        ),
    },
    "mun_almere_2024_2026_visie_gezondheidsbeleid_raadsvoorstel_geamendeerd": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Amended council proposal for the Almere health-policy vision. Use for governance, decision route, "
            "and local framing; do not treat as a national norm source."
        ),
    },
    "mun_almere_2024_2026_visie_gezondheidsbeleid_besluitenlijst": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Council decision-list source for the health-policy vision route. Use for local decision traceability, "
            "not for substantive policy expansion beyond what the decision list itself records."
        ),
    },
    "mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": False,
        "contains_structured_tables": True,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Municipal plan of approach for Brede SPUK/GALA 2024-2026. Use for local prevention, financing, "
            "execution, and monitoring context; named officials or empty contact fields should not be promoted "
            "to public claims."
        ),
    },
    "mun_almere_2024_2034_maatschappelijke_agenda_beleidstekst": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Underlying municipal policy text for the Maatschappelijke agenda 2024-2034. It is the stronger "
            "local source for social-domain priorities, social basis, cooperation, monitoring, and long-term "
            "municipal context."
        ),
    },
    "mun_almere_2024_2034_maatschappelijke_agenda_raadsvoorstel_geamendeerd": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Amended council proposal for the Maatschappelijke agenda. Use for governance, decision route, and "
            "local social-domain framing; keep process text separate from adopted policy content."
        ),
    },
    "mun_almere_2024_2034_maatschappelijke_agenda_besluitenlijst": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Council decision-list source for the Maatschappelijke agenda route. Use for local decision "
            "traceability, not as a source for new substantive policy claims."
        ),
    },
    "mun_almere_2024_2034_maatschappelijke_agenda_opzet_evaluatie": {
        "source_classification": "derivative",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": True,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Supporting evaluation and monitoring setup for the social domain. Use for monitoring design and "
            "review questions, not as a replacement for the adopted Maatschappelijke agenda itself."
        ),
    },
    "mun_almere_2026_stevige_lokale_teams_raad": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Local council page for Stevige Lokale Teams and the youth/family investment fund; high-priority "
            "D6 responsibility evidence, but underlying Documentwijzer decision documents still need separate intake."
        ),
    },
    "mun_almere_wijkteams": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Public baseline source for the existing Almere wijkteam access and support route.",
    },
    "nat_vng_richtinggevend_kader_toegang_lokale_teams": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "National implementation framework for access, local teams and integrated services; use as assessment "
            "benchmark, not as an Almere decision."
        ),
    },
    "nat_tsd_basisfuncties_lokale_teams": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Assessment framework for low-threshold, nearby and integrated local teams in the social domain.",
    },
    "reg_ggd_flevoland_begroting_2026": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": True,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Current GGD Flevoland budget source for governance, JGZ, Kennis en Advies, prevention, plustaken, "
            "inwonerbijdrage and GGD-region scale."
        ),
    },
    "reg_ggd_flevoland_kennis_en_advies": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": False,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Public source for GGD Flevoland monitors, dashboards, epidemiology, data analysis and advice.",
    },
    "reg_ggd_flevoland_jgz_almere_profile": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Public source for JGZ Almere's 0-18 role, school links, youth support and care-chain function.",
    },
    "mun_almere_2026_stevige_lokale_teams_geamendeerd_raadsvoorstel": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": True,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Geamendeerd local council proposal for Stevige Lokale Teams. Use as high-value local decision "
            "evidence, while still separating source-backed text from D6 classification choices."
        ),
    },
    "mun_almere_2026_stevige_lokale_teams_raadsvoorstel": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": True,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Original local council proposal for Stevige Lokale Teams. Use for proposal logic and compare with "
            "the amended/adopted version before treating claims as settled."
        ),
    },
    "mun_almere_2026_stevige_lokale_teams_begrotingswijziging": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": True,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Budget-change attachment for the Stevige Lokale Teams council route. Use for local money-flow "
            "evidence, not for national AZWA/D6 financing conclusions."
        ),
    },
    "mun_almere_2026_stevige_lokale_teams_besluitenlijst": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Decision-list attachment for the Stevige Lokale Teams route. Use for decision traceability and "
            "voting/adoption status."
        ),
    },
    "mun_almere_samenwerkingsprojecten": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Public municipal project page for Samen Sterker in de Wijk and related Wonen & Zorg projects. "
            "Use as implementation evidence, not as formal D6 classification."
        ),
    },
    "mun_almere_pga_current_home": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Current public PGA homepage. Use for current implementation context and themes, not as a replacement "
            "for the formal PGA transformation plan."
        ),
    },
    "mun_almere_gezonde_scholen": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Municipal public page for Gezonde scholen in Almere. Use as source-backed local implementation "
            "evidence for the Gezonde School D6 validation row, not as formal D6 classification."
        ),
    },
    "mun_almere_gezond_in_almere": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Municipal health/prevention gateway that places Gezonde School and mentale gezondheid in the "
            "same Almere public-health context. Use as context, not as owner or funding evidence."
        ),
    },
    "reg_ggd_flevoland_gezonde_school": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "GGD Flevoland page for Gezonde School advisers and school health/wellbeing support. Use as "
            "regional implementation evidence; D6 ownership and mandate still need validation."
        ),
    },
    "reg_ggd_flevoland_ketenaanpak_gezond_gewicht_almere": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "GGD Flevoland page for Gezond Gewicht Almere and the Pact met impact reference. Use as stable "
            "public anchor for the healthy-school/collective-prevention evidence cluster when the referenced "
            "PDF URL is unavailable to the local pipeline."
        ),
    },
    "mun_almere_lea_2024_2028": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": (
            "Local Education Agenda page for Almere 2024-2028. Use for school-wellbeing, LEA partner and "
            "budget-context evidence; do not treat it as a D6 ownership decision."
        ),
    },
    "nat_zorgakkoorden_pga_20_miljoen_2024": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Official Zorgakkoorden/VWS news page confirming IZA funding for Positief Gezond Almere; context for PGA, not a D6 responsibility decision.",
    },
    "mun_almere_pga_regionaal_transferpunt": {
        "source_classification": "supporting_commentary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "PGA project page for RTP Almere/Flevoland. Use as implementation context for care coordination; do not treat as formal D6 classification.",
    },
    "reg_flevoziekenhuis_rtp_flevoland_2025": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Provider source showing RTP Flevoland is live, names its PGA origin and participating care actors; implementation evidence only.",
    },
    "reg_rtp_flevoland_home": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": False,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Live service page for RTP Flevoland, useful for operational scope and access details; not governance or funding evidence.",
    },
    "mun_almere_pga_rso_data_infrastructuur": {
        "source_classification": "supporting_commentary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "PGA page for RSO and data-infrastructure work. Use to source digital-exchange concepts, not final data-governance ownership.",
    },
    "reg_flevoziekenhuis_thuismonitoring": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": False,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Provider page proving active telemonitoring/thuismonitoring practice in Almere; relation to PGA Monitoring@home remains a validation question.",
    },
    "reg_ggd_flevoland_kadernota_2027": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": True,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "GGD strategic/budget framework with Kennis & Advies, monitoring, data and AZWA/GALA/IZA relevance; not an Almere D6 mandate decision.",
    },
    "reg_woonzorg_flevoland_beleidsplan_2026": {
        "source_classification": "supporting_commentary",
        "curation_bucket": "context",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Provider policy plan corroborating PGA participation, RSO/digitalization and care-coordination context; provider-side evidence only.",
    },
    "reg_npz_almere_pilot_viewer_acp": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "NPZ Almere project page for ACP/PZP viewer pilot and data-sharing use case; not a general D6 data-platform mandate.",
    },
    "reg_npz_almere_evaluatie_viewer_pzp_acp_2025": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Evaluation of the Almere PZP/ACP viewer pilot; useful for concrete ZNO/viewer implementation lessons and mandate questions.",
    },
    "nat_palliaweb_digitale_initiatieven_pzp": {
        "source_classification": "supporting_commentary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "National project overview that names the PGA PZP/ACP digital initiative and involved Almere/Flevoland organizations.",
    },
    "reg_npz_almere_jaarplan_2025": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "NPZ Almere year plan with PZP/ACP digital exchange goals and evaluation action; supports use-case evidence, not formal D6 classification.",
    },
    "mun_almere_welzijnskader_2020": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Municipal welfare framework for social base, meeting places, volunteers and mantelzorg; dated 2020, so use with current pages for live inventory.",
    },
    "mun_almere_subsidie_buurtontmoeting": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Current municipal service page for subsidy to low-threshold neighbourhood meeting places and activities; proves support route, not formal D6 classification.",
    },
    "mun_almere_nadere_regels_buurtontmoeting": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Municipal rules for neighbourhood meeting places and activities; strong public evidence for subsidy criteria, resident initiative and anti-double-funding checks.",
    },
    "mun_almere_wijkbudget": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Current municipal subsidy route for resident ideas for other residents; useful for citizen-initiative evidence and funding-gap review.",
    },
    "mun_almere_ondersteuning_mantelzorg": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Municipal service page for mantelzorg support through Wmo and VMCA; public informal-care support evidence only.",
    },
    "mun_almere_mantelzorgwaardering": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Municipal page for mantelzorgwaardering and VMCA advisory/support role; useful for finance and actor mapping, not D6 ownership.",
    },
    "mun_almere_sociaal_domein_aanbod_jeugd_gezin": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Official preventive-offer page that points to Sociale Kaart Flevoland and annual GGD information checks; referral/inventory evidence only.",
    },
    "mun_almere_sociale_veerkracht_almeerders": {
        "source_classification": "derivative",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Municipal-commissioned social-state advice for social base, volunteers, meeting places and social resilience; context/gap framing, not an implementation mandate.",
    },
    "mun_deschoor_buurtkamers": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": False,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Provider page naming live buurtkamers and low-threshold meeting functions; implementation inventory evidence, not municipal mandate proof.",
    },
    "mun_deschoor_initiatievenbureau": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Provider page for resident-initiative support across buurtcentra; useful for social-base partner mapping only.",
    },
    "mun_deschoor_buurtkracht": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": False,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Provider page for Buurtkracht and resident activities; use as implementation evidence for citizen initiatives.",
    },
    "mun_deschoor_opbouwwerk_almere": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Provider page for opbouwwerk in Almere, including relation to wijkteams and residents' initiatives; partner evidence only.",
    },
    "mun_vmca_meerjarenvisie_2022_2025": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "VMCA policy plan describing volunteer, mantelzorg and wijkteam contribution; partner evidence, not final D6 ownership.",
    },
    "mun_humanitas_almere": {
        "source_classification": "primary",
        "curation_bucket": "context",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": False,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Humanitas Almere local page for volunteer-supported themes; supporting partner evidence, weaker than municipal and commissioned sources.",
    },
    "mun_almere_almeers_preventieakkoord": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Municipal prevention-network page with initiatives, community themes and funding context; bridge evidence, not a D6 responsibility decision.",
    },
    "mun_almere_wijkteams_ontmoeting": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Wijkteams page for social contact, coffee moments and links to VMCA, Humanitas and De Schoor; current inloop/social-base access evidence.",
    },
    "reg_ggd_flevoland_kadernota_2025": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "GGD budget-framework source for GALA, Regiobeeld/Regioplan, PGA monitoring and public-health advisory roles; use as interface evidence, not as final D6 mandate.",
    },
    "reg_flever_zorgzaam_flevoland_project": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Flever project page describing Zorgzaam Flevoland as regional IZA-regioplan movement and Flever's resident-perspective support role; supporting role-split evidence.",
    },
    "reg_flever_meerjarenplan_2025_2028": {
        "source_classification": "primary",
        "curation_bucket": "context",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Flever policy plan for regional support, participation, network and research functions; useful for actor role-splitting, weaker than official governance sources.",
    },
    "reg_flever_inwoners_onderdeel_pga": {
        "source_classification": "primary",
        "curation_bucket": "context",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Flever page naming project-lead support for resident participation within PGA; use for narrow partner role evidence only.",
    },
    "reg_almere_zorglandschap_wmo": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Regional Almere page for Zorglandschap Wmo and mental-health support landscape; useful context for SSidW and regional Wmo scope.",
    },
    "reg_zorglandschap_wmo_uitvoeringsprogramma_2022": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Regional implementation programme source for Zorglandschap Wmo and Samen Sterker start, partners, method and expansion; not a D6 mandate.",
    },
    "reg_zorglandschap_wmo_monitor_2025": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Current regional monitor describing SSidW as cross-domain work between neighbourhood social domain and curative care; strong status evidence, not ownership proof.",
    },
    "reg_zonmw_samen_sterker_uitvoeringsplan": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "ZonMw implementation-subsidy page for SSidW pilots, partners and responsible organisation; use as programme/timeline evidence only.",
    },
    "reg_zonmw_samen_sterker_startsubsidie": {
        "source_classification": "primary",
        "curation_bucket": "context",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "ZonMw start-subsidy page for co-creation, 2021 pilots in Almere and Dronten and effect-monitoring intent; historical programme context.",
    },
    "mun_almere_pga_samen_sterker_wijk": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Row-specific PGA project page for SSidW target group, project window, partners and current Almere implementation context.",
    },
    "mun_almere_subsidieregister_2023": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": True,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Municipal subsidy register with a 2023 line for Samen Sterker in de Wijk; funding trace only, not structural D6 funding proof.",
    },
    "mun_almere_evaluatie_schakelteams_2021": {
        "source_classification": "primary",
        "curation_bucket": "context",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Municipal evaluation of schakelteams; useful interface evidence for neighbourhood mental-health support, not direct SSidW governance proof.",
    },
    "reg_samen_sterker_in_de_wijk_home": {
        "source_classification": "primary",
        "curation_bucket": "context",
        "contains_d5": False,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Current SSidW own site; useful as live implementation and learning/community source, lower-authority than municipal/regional/ZonMw sources.",
    },
}


def priority_label(priority_rank: int) -> str:
    if priority_rank <= 5:
        return "critical"
    if priority_rank <= 8:
        return "high"
    if priority_rank <= 12:
        return "medium"
    return "low"


def validate_annotations(document_ids: set[str]) -> None:
    annotation_ids = set(ANNOTATIONS)
    missing = sorted(document_ids - annotation_ids)
    unexpected = sorted(annotation_ids - document_ids)
    if missing or unexpected:
        parts = []
        if missing:
            parts.append(f"missing annotations for: {', '.join(missing)}")
        if unexpected:
            parts.append(f"unexpected annotation ids: {', '.join(unexpected)}")
        raise ValueError("; ".join(parts))


def build_inventory() -> dict:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    document_ids = {entry["document_id"] for entry in manifest}
    validate_annotations(document_ids)

    documents = []
    for entry in manifest:
        annotation = ANNOTATIONS[entry["document_id"]]
        source_format = Path(entry["file_path"]).suffix.lower().lstrip(".")
        traceability_mode = "page_based" if source_format == "pdf" else "section_chunk_based"
        documents.append(
            {
                "document_id": entry["document_id"],
                "source_number": entry["source_number"],
                "title": entry["title"],
                "short_title": entry["short_title"],
                "publisher": entry["publisher"],
                "publication_date": entry["publication_date"],
                "document_type": entry["document_type"],
                "jurisdiction_level": entry["jurisdiction_level"],
                "status": entry["status"],
                "source_url": entry["source_url"],
                "file_path": entry["file_path"],
                "source_format": source_format,
                "traceability_mode": traceability_mode,
                "source_classification": annotation["source_classification"],
                "curation_bucket": annotation["curation_bucket"],
                "contains_d5": annotation["contains_d5"],
                "contains_d6": annotation["contains_d6"],
                "contains_structured_tables": annotation["contains_structured_tables"],
                "contains_financing_logic": annotation["contains_financing_logic"],
                "contains_governance_logic": annotation["contains_governance_logic"],
                "contains_monitoring_evaluation_logic": annotation["contains_monitoring_evaluation_logic"],
                "contains_municipal_implications": annotation["contains_municipal_implications"],
                "priority_rank": entry["priority_rank"],
                "extraction_priority": priority_label(entry["priority_rank"]),
                "inventory_notes": annotation["inventory_notes"],
            }
        )

    documents.sort(key=lambda item: (item["priority_rank"], item["document_id"]))

    summary = {
        "document_count": len(documents),
        "priority_counts": {
            "critical": sum(1 for item in documents if item["extraction_priority"] == "critical"),
            "high": sum(1 for item in documents if item["extraction_priority"] == "high"),
            "medium": sum(1 for item in documents if item["extraction_priority"] == "medium"),
            "low": sum(1 for item in documents if item["extraction_priority"] == "low"),
        },
        "source_classification_counts": {
            "primary": sum(1 for item in documents if item["source_classification"] == "primary"),
            "derivative": sum(1 for item in documents if item["source_classification"] == "derivative"),
            "supporting_commentary": sum(
                1 for item in documents if item["source_classification"] == "supporting_commentary"
            ),
        },
        "topic_signal_counts": {
            "contains_d5": sum(1 for item in documents if item["contains_d5"]),
            "contains_d6": sum(1 for item in documents if item["contains_d6"]),
            "contains_structured_tables": sum(1 for item in documents if item["contains_structured_tables"]),
            "contains_financing_logic": sum(1 for item in documents if item["contains_financing_logic"]),
            "contains_governance_logic": sum(1 for item in documents if item["contains_governance_logic"]),
            "contains_monitoring_evaluation_logic": sum(
                1 for item in documents if item["contains_monitoring_evaluation_logic"]
            ),
            "contains_municipal_implications": sum(
                1 for item in documents if item["contains_municipal_implications"]
            ),
        },
    }

    return {
        "inventory_version": 1,
        "generated_on": date.today().isoformat(),
        "source_manifest": MANIFEST_PATH.relative_to(REPO_ROOT).as_posix(),
        "documents": documents,
        "summary": summary,
    }


def main() -> None:
    inventory = build_inventory()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"Prepared inventory for {inventory['summary']['document_count']} documents")


if __name__ == "__main__":
    main()
