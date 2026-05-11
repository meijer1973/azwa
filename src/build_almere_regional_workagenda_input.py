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
OPERATIONAL_REQUIREMENTS = ROOT / "data" / "extracted" / "workagenda_d5_operational_requirements.json"
NULMETING_CAPACITY = ROOT / "data" / "extracted" / "workagenda_nulmeting_capacity.json"
LOCAL_SOURCE_STRENGTHENING = ROOT / "data" / "extracted" / "local_source_strengthening_almere.json"
OUTPUT = ROOT / "data" / "workagenda" / "almere_regional_workagenda_input_objects.json"


SOURCE_LAYERS = [
    "data/workagenda/d5_status_matrix.json",
    "data/workagenda/d5_validation_tickets.json",
    "data/workagenda/d5_validation_packets.json",
    "data/workagenda/d5_stuurmodel.json",
    "data/extracted/workagenda_d5_operational_requirements.json",
    "data/extracted/workagenda_nulmeting_capacity.json",
    "data/extracted/local_source_strengthening_almere.json",
    "data/extracted/municipal/almere_d6_responsibility_register.json",
    "data/raw/national/nat_azwa_format_werkagenda_d5_2026.docx",
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

MUNICIPAL_DELIVERY_TARGET_DATE = "2026-09-15"
REGIONAL_ADOPTION_DEADLINE = "2026-11-15"

WORKAGENDA_REQUIRED_SECTIONS = [
    {
        "section_id": "urgency_and_problem",
        "label": "urgentie en opgave",
        "what_to_prepare": "why this component matters for Almere and the regional workagenda",
    },
    {
        "section_id": "current_local_situation",
        "label": "huidige lokale situatie",
        "what_to_prepare": "what is already arranged, what is visible from sources and what still needs local confirmation",
    },
    {
        "section_id": "target_ambition",
        "label": "ambitie richting 2030",
        "what_to_prepare": "the intended direction, coverage and scale for the regional workagenda period",
    },
    {
        "section_id": "target_design",
        "label": "ontwerp van de aanpak",
        "what_to_prepare": "roles, route, partners, D6 dependencies and working agreements",
    },
    {
        "section_id": "project_objectives_and_gap",
        "label": "doelen en verschil met huidige situatie",
        "what_to_prepare": "the limited set of gaps and decision points needed for first regional drafting",
    },
    {
        "section_id": "financial_plan",
        "label": "financieel plan",
        "what_to_prepare": "funding route, continuity status and controller validation needs",
    },
    {
        "section_id": "monitoring_and_learning",
        "label": "monitoring en lerende cyclus",
        "what_to_prepare": "candidate indicators, data owner and how learning will be organised",
    },
    {
        "section_id": "milestone_planning",
        "label": "mijlpalenplanning",
        "what_to_prepare": "municipal delivery by 15 September 2026 and later regional consolidation toward adoption",
    },
]

FORMAT_SOURCE_REF = {
    "source_id": "nat_azwa_format_werkagenda_d5_2026",
    "title": "Format werkagenda basisfunctionaliteiten AZWA",
    "source_url": "https://vng.nl/sites/default/files/2026-04/format-voor-de-werkagenda-azwa.docx",
    "repository_paths": [
        "data/raw/national/nat_azwa_format_werkagenda_d5_2026.docx",
        "data/site/source_view_models/format-werkagenda-azwa.json",
    ],
    "authority": "national_format_source",
    "confidence": "high",
}

FORMAT_INFORMATION_STATUS_MODEL = [
    {
        "status_id": "confirmed_decision",
        "meaning": "May be used as settled workagenda text because a local or regional decision/validation record supports it.",
        "may_use_for_concept": True,
        "may_use_as_confirmed_workagenda_text": True,
    },
    {
        "status_id": "source_backed_current_information",
        "meaning": "Supported by public or source-backed current information, but not itself a local decision.",
        "may_use_for_concept": True,
        "may_use_as_confirmed_workagenda_text": False,
    },
    {
        "status_id": "likely_or_indicated",
        "meaning": "Indicated by current sources, actor hints or implementation signals; needs local confirmation before final use.",
        "may_use_for_concept": True,
        "may_use_as_confirmed_workagenda_text": False,
    },
    {
        "status_id": "planning_assumption",
        "meaning": "Useful planning assumption, such as Almere's 15 September delivery target; not a national formal deadline.",
        "may_use_for_concept": True,
        "may_use_as_confirmed_workagenda_text": False,
    },
    {
        "status_id": "validation_needed",
        "meaning": "Needs stakeholder, owner, capacity, monitoring or D6 validation before final workagenda use.",
        "may_use_for_concept": True,
        "may_use_as_confirmed_workagenda_text": False,
    },
    {
        "status_id": "finance_controller_validation_needed",
        "meaning": "Finance route, continuity, double-counting or controller check still needs validation.",
        "may_use_for_concept": True,
        "may_use_as_confirmed_workagenda_text": False,
    },
    {
        "status_id": "local_decision_needed",
        "meaning": "Requires an Almere or regional scope, phasing, ownership or priority decision.",
        "may_use_for_concept": True,
        "may_use_as_confirmed_workagenda_text": False,
    },
    {
        "status_id": "not_available_yet",
        "meaning": "No usable input found in the current generated layer.",
        "may_use_for_concept": False,
        "may_use_as_confirmed_workagenda_text": False,
    },
]

REGIONAL_PREVENTION_INFRASTRUCTURE_FORMAT_FIELDS = [
    {
        "field_id": "rpi_explanation",
        "label": "Toelichting op RPI",
        "format_question": "Omschrijf beknopt hoe de regionale preventie-infrastructuur in de regio is georganiseerd.",
    },
    {
        "field_id": "regional_health_goals",
        "label": "Regionale gezondheidsdoelen",
        "format_question": "Omschrijf welke gezamenlijke gezondheidsdoelen in de regio zijn vastgesteld.",
    },
    {
        "field_id": "financial_resources",
        "label": "Financiële middelen",
        "format_question": "Omschrijf de financieringsafspraken over de coördinatie en uitvoering.",
    },
    {
        "field_id": "regional_cooperation_agreements",
        "label": "Regionale samenwerkingsafspraken",
        "format_question": "Omschrijf welke afspraken er zijn gemaakt omtrent verantwoordelijkheid.",
    },
    {
        "field_id": "responsibility_distribution",
        "label": "Verantwoordelijkheidsverdeling",
        "format_question": "Omschrijf hoe samenwerking over domeinen heen en aanspreekbaarheid op rollen is georganiseerd.",
    },
    {
        "field_id": "knowledge_and_monitoring",
        "label": "Kennis en monitoring",
        "format_question": "Omschrijf de regionale monitoring van voortgang, digitalisering en de gezamenlijke leer- en datacyclus.",
    },
]

LEEFGEBIED_FORMAT_FIELDS = [
    {
        "field_id": "health_goals",
        "label": "Gezondheidsdoelen",
        "format_question": "Welke concrete regionale gezondheidsdoelen gericht op gezondheid en welzijn heeft de regio voor het leefgebied?",
    },
    {
        "field_id": "scope_and_coherence",
        "label": "Scope en samenhang",
        "format_question": "Wat valt er binnen het leefgebied en hoe is samenhang met andere leefgebieden geborgd en benut?",
    },
    {
        "field_id": "organisation_and_roles",
        "label": "Organisatie en rollen",
        "format_question": "Hoe zijn verantwoordelijkheid, eigenaarschap en uitvoeringscapaciteit voor het leefgebied geborgd?",
    },
]

COMPONENT_FORMAT_FIELDS = [
    {
        "field_id": "urgency",
        "source_stage_label": "IST",
        "project_vocabulary_group": "current_state",
        "label": "Urgentie",
        "format_question": "Wat is er bekend over de urgentie van deze basisfunctionaliteit of aanpak in de regio?",
    },
    {
        "field_id": "current_situation",
        "source_stage_label": "IST",
        "project_vocabulary_group": "current_state",
        "label": "Situatie",
        "format_question": "In hoeverre is deze basisfunctionaliteit of aanpak al aanwezig in de regio?",
    },
    {
        "field_id": "ambition",
        "source_stage_label": "SOLL",
        "project_vocabulary_group": "target_state",
        "label": "Ambitie",
        "format_question": "Wat is vastgesteld als regionaal dekkend aanbod en wat is nodig om daartoe te komen?",
    },
    {
        "field_id": "design_choices",
        "source_stage_label": "SOLL",
        "project_vocabulary_group": "target_state",
        "label": "Ontwerp",
        "format_question": "Welke expliciete keuzes zijn gemaakt in de invulling en welke keuzes moeten nog worden gemaakt?",
    },
    {
        "field_id": "project_objectives",
        "source_stage_label": "GAP",
        "project_vocabulary_group": "gap_summary",
        "label": "Projectdoelstellingen",
        "format_question": "Omschrijf de SMART-afspraken die zijn gemaakt.",
    },
    {
        "field_id": "financial_plan",
        "source_stage_label": "GAP",
        "project_vocabulary_group": "gap_summary",
        "label": "Financieel plan",
        "format_question": "Welke financiële middelen worden ingezet voor dit onderdeel?",
    },
    {
        "field_id": "monitoring",
        "source_stage_label": "GAP",
        "project_vocabulary_group": "gap_summary",
        "label": "Monitoring",
        "format_question": "Hoe worden voortgang, prestaties en risico's gevolgd en gerapporteerd?",
    },
    {
        "field_id": "milestone_planning",
        "source_stage_label": "GAP",
        "project_vocabulary_group": "gap_summary",
        "label": "Mijlpalenplanning",
        "format_question": "Welke kwartaalactiviteiten, verantwoordelijken en deelresultaten zijn afgesproken?",
    },
]

FORMAT_COMPONENT_CONTEXT = {
    "laagdrempelige_steunpunten": {
        "format_item_id": "2a",
        "format_item_title": "Laagdrempelige steunpunten",
        "leefgebied": "Mentale gezondheid",
        "component_kind_in_format": "basisfunctionaliteit",
        "format_match_status": "direct_match",
    },
    "sociaal_verwijzen": {
        "format_item_id": "2b",
        "format_item_title": "Sociaal verwijzen",
        "leefgebied": "Mentale gezondheid",
        "component_kind_in_format": "basisfunctionaliteit",
        "format_match_status": "direct_match",
    },
    "mentale_gezondheidsnetwerken": {
        "format_item_id": "2c",
        "format_item_title": "Mentale gezondheidsnetwerken",
        "leefgebied": "Mentale gezondheid",
        "component_kind_in_format": "ontwikkelagenda_1_lopend",
        "format_match_status": "direct_match",
    },
    "kansrijke_start": {
        "format_item_id": "3a",
        "format_item_title": "Kansrijke Start",
        "leefgebied": "Kansrijk opgroeien",
        "component_kind_in_format": "basisfunctionaliteit",
        "format_match_status": "direct_match",
    },
    "nu_niet_zwanger": {
        "format_item_id": "3a.1",
        "format_item_title": "Nu Niet Zwanger",
        "leefgebied": "Kansrijk opgroeien",
        "component_kind_in_format": "basisfunctionaliteit",
        "format_match_status": "direct_match",
    },
    "integrale_gezinspoli": {
        "format_item_id": "3a.2",
        "format_item_title": "Integrale gezinspoli",
        "leefgebied": "Kansrijk opgroeien",
        "component_kind_in_format": "basisfunctionaliteit",
        "format_match_status": "direct_match",
    },
    "ketenaanpak_overgewicht_obesitas_kinderen": {
        "format_item_id": "3b",
        "format_item_title": "Ketenaanpak overgewicht en obesitas kinderen",
        "leefgebied": "Kansrijk opgroeien",
        "component_kind_in_format": "ontwikkelagenda_1_lopend",
        "format_match_status": "direct_match",
    },
    "ketenaanpak_overgewicht_obesitas_volwassenen": {
        "format_item_id": "4a",
        "format_item_title": "Ketenaanpak overgewicht en obesitas volwassenen",
        "leefgebied": "Leefstijl",
        "component_kind_in_format": "basisfunctionaliteit",
        "format_match_status": "direct_match",
    },
    "valpreventie": {
        "format_item_id": "5a",
        "format_item_title": "Valpreventie",
        "leefgebied": "Vitaal ouder worden/ouderen",
        "component_kind_in_format": "basisfunctionaliteit",
        "format_match_status": "direct_match",
    },
    "ontwikkelagenda_1_nieuw_beproeven": {
        "format_item_id": "aggregate",
        "format_item_title": "Nieuwe onderdelen ontwikkelagenda 1",
        "leefgebied": "Meerdere leefgebieden",
        "component_kind_in_format": "aggregate",
        "format_match_status": "aggregate_for_multiple_optional_format_items",
        "note": "The VNG format splits this into separate optional items such as rookvrije start, rookvrije thuiszorg, rookvrije wijkaanpak, ketenaanpak dementie and multiproblematiek.",
    },
    "ontwikkelagenda_2_overige_initiatieven": {
        "format_item_id": "outside_core_format",
        "format_item_title": "Ontwikkelagenda 2 en overige initiatieven",
        "leefgebied": "Nog te kiezen",
        "component_kind_in_format": "optional_or_outside_core_format",
        "format_match_status": "no_direct_vng_format_item",
    },
}

CURATED_COMPONENT_ENRICHMENT: dict[str, dict[str, list[dict[str, Any]]]] = {
    "valpreventie": {
        "implementation_progress_signals": [
            {
                "signal_id": "valpreventie_inloop_route",
                "statement": (
                    "GGD Flevoland beschrijft voor Almere een vrij toegankelijk inloopmoment "
                    "waar professionals met inwoners naar het valrisico kijken."
                ),
                "authority": "regional_operational_source",
                "validation_status": "source_backed_public_route_not_capacity_confirmation",
                "source_ids": ["reg_ggd_flevoland_valpreventie_almere"],
                "claim_ids": ["clm__reg_ggd_flevoland_valpreventie_almere_d5_001"],
            },
            {
                "signal_id": "valpreventie_course_matching",
                "statement": (
                    "De publieke route beschrijft dat met inwoners wordt besproken of zij een cursus "
                    "valpreventie kunnen volgen en welke cursus past; dit wijst op een bestaande "
                    "toeleidingsroute, maar bevestigt geen actuele capaciteit of wachttijd."
                ),
                "authority": "regional_operational_source",
                "validation_status": "source_backed_route_signal_capacity_unconfirmed",
                "source_ids": ["reg_ggd_flevoland_valpreventie_almere"],
                "claim_ids": ["clm__reg_ggd_flevoland_valpreventie_almere_d5_002"],
            },
            {
                "signal_id": "valpreventie_free_walk_in_signal",
                "statement": (
                    "De GGD-pagina noemt vrije inloop, geen aanmelding nodig en gratis toegang voor "
                    "de eerste route naar cursusdeelname."
                ),
                "authority": "regional_operational_source",
                "validation_status": "source_backed_public_access_signal_not_finance_confirmation",
                "source_ids": ["reg_ggd_flevoland_valpreventie_almere"],
                "claim_ids": ["clm__reg_ggd_flevoland_valpreventie_almere_d5_003"],
            },
            {
                "signal_id": "valpreventie_chain_steps",
                "statement": (
                    "Het ketendocument beschrijft ketenstappen zoals signaleren, valrisicotest, "
                    "passende interventies en aansluiting op structureel sport- en beweegaanbod."
                ),
                "authority": "regional_implementation_source",
                "validation_status": "implementation_route_signal_local_status_still_to_validate",
                "source_ids": ["reg_ggd_flevoland_valpreventie_almere_ketendocument_2026"],
                "claim_ids": ["clm__reg_ggd_flevoland_valpreventie_almere_ketendocument_2026_d6_003"],
            },
        ],
        "party_and_role_signals": [
            {
                "party_or_role": "GGD Flevoland",
                "indicated_role": "publieke route en informatievoorziening voor valpreventie in Almere",
                "authority": "regional_operational_source",
                "validation_status": "visible_in_public_source",
                "source_ids": ["reg_ggd_flevoland_valpreventie_almere"],
            },
            {
                "party_or_role": "Gemeente Almere",
                "indicated_role": "genoemd in afspraken rond gemeentelijk domein voor matig valrisico",
                "authority": "regional_implementation_source",
                "validation_status": "role_signal_needs_owner_and_controller_validation",
                "source_ids": ["reg_ggd_flevoland_valpreventie_almere_ketendocument_2026"],
                "claim_ids": [
                    "clm__reg_ggd_flevoland_valpreventie_almere_ketendocument_2026_governance_and_finance_002"
                ],
            },
            {
                "party_or_role": "Paramedisch Platform Almere",
                "indicated_role": "genoemd bij afspraken voor valpreventieve beweeginterventies bij matig valrisico",
                "authority": "regional_implementation_source",
                "validation_status": "party_signal_not_full_contract_confirmation",
                "source_ids": ["reg_ggd_flevoland_valpreventie_almere_ketendocument_2026"],
                "claim_ids": [
                    "clm__reg_ggd_flevoland_valpreventie_almere_ketendocument_2026_governance_and_finance_002"
                ],
            },
            {
                "party_or_role": "EELA",
                "indicated_role": (
                    "ROS die volgens het ketendocument samenwerking tussen zorglijnen, sociaal domein, "
                    "overheden, verzekeraars en bedrijfsleven in Almere en Amsterdam helpt versterken"
                ),
                "authority": "regional_implementation_source",
                "validation_status": "party_signal_scope_and_task_need_validation",
                "source_ids": ["reg_ggd_flevoland_valpreventie_almere_ketendocument_2026"],
                "claim_ids": ["clm__reg_ggd_flevoland_valpreventie_almere_ketendocument_2026_municipal_translation_002"],
            },
            {
                "party_or_role": "centrale coördinator valpreventie",
                "indicated_role": "verzamelt aanmeldingen binnen Almere en houdt wachtlijsten per gebied/woonkern bij",
                "authority": "regional_implementation_source",
                "validation_status": "role_signal_identity_mandate_and_current_status_unconfirmed",
                "source_ids": ["reg_ggd_flevoland_valpreventie_almere_ketendocument_2026"],
                "claim_ids": ["clm__reg_ggd_flevoland_valpreventie_almere_ketendocument_2026_municipal_translation_003"],
            },
        ],
        "finance_and_resource_signals": [
            {
                "signal_id": "valpreventie_moderate_risk_municipal_arrangements",
                "statement": (
                    "Het ketendocument noemt gemeentelijke regelingen en afspraken tussen Gemeente Almere "
                    "en het Paramedisch Platform Almere voor valpreventieve beweeginterventies bij matig valrisico."
                ),
                "authority": "regional_implementation_source",
                "validation_status": "finance_signal_requires_controller_validation",
                "source_ids": ["reg_ggd_flevoland_valpreventie_almere_ketendocument_2026"],
                "claim_ids": [
                    "clm__reg_ggd_flevoland_valpreventie_almere_ketendocument_2026_governance_and_finance_002"
                ],
            },
            {
                "signal_id": "valpreventie_accessibility_finance_signal",
                "statement": (
                    "Het ketendocument legt een verband tussen de financieringsstructuur en deelname "
                    "zonder financiële drempels; dit is geen bewijs van structurele borging."
                ),
                "authority": "regional_implementation_source",
                "validation_status": "finance_context_not_structural_funding_confirmation",
                "source_ids": ["reg_ggd_flevoland_valpreventie_almere_ketendocument_2026"],
                "claim_ids": [
                    "clm__reg_ggd_flevoland_valpreventie_almere_ketendocument_2026_governance_and_finance_003"
                ],
            },
        ],
        "monitoring_and_learning_signals": [
            {
                "signal_id": "valpreventie_monitoring_registration",
                "statement": "Het ketendocument bevat onderdelen over monitoring, registratie en kwaliteit.",
                "authority": "regional_implementation_source",
                "validation_status": "monitoring_signal_owner_and_use_unconfirmed",
                "source_ids": ["reg_ggd_flevoland_valpreventie_almere_ketendocument_2026"],
                "claim_ids": [
                    "clm__reg_ggd_flevoland_valpreventie_almere_ketendocument_2026_monitoring_and_evaluation_001"
                ],
            },
            {
                "signal_id": "valpreventie_excel_monitoring_template",
                "statement": "Het ketendocument noemt een Excel-sjabloon voor monitoring en registratie.",
                "authority": "regional_implementation_source",
                "validation_status": "instrument_signal_not_validated_reporting_arrangement",
                "source_ids": ["reg_ggd_flevoland_valpreventie_almere_ketendocument_2026"],
                "claim_ids": [
                    "clm__reg_ggd_flevoland_valpreventie_almere_ketendocument_2026_monitoring_and_evaluation_003"
                ],
            },
        ],
    },
    "ketenaanpak_overgewicht_obesitas_volwassenen": {
        "implementation_progress_signals": [
            {
                "signal_id": "adult_overweight_public_baseline",
                "statement": (
                    "GGD Flevoland geeft voor Almere publieke indicatoren voor matig overgewicht, "
                    "obesitas en voldoen aan de beweegrichtlijn bij volwassenen."
                ),
                "authority": "public_table_book_source",
                "validation_status": "source_backed_population_signal_not_service_capacity",
                "source_ids": ["reg_ggd_flevoland_2024_volwassenen_gemeenten"],
            },
            {
                "signal_id": "adult_overweight_operational_direction",
                "statement": (
                    "De landelijke D5-richting vraagt om samenhang tussen centrale zorgcoördinatie, "
                    "beweegaanbod, gezondheidsvaardigheden/leefstijl, individuele ondersteuning en GLI."
                ),
                "authority": "national_operational_requirement",
                "validation_status": "target_design_direction_local_capacity_unconfirmed",
                "source_ids": ["nat_azwa_opdracht_werkagenda_d5_2026", "nat_azwa_format_werkagenda_d5_2026"],
            },
            {
                "signal_id": "adult_overweight_fgw_support",
                "statement": (
                    "Het Almere GALA-plan noemt Flevoland Gezond en Wel als preventiecoalitie die "
                    "regionale ketenaanpakken ondersteunt, waaronder de gecombineerde leefstijlinterventie "
                    "voor volwassenen."
                ),
                "authority": "municipal_policy_source",
                "validation_status": "regional_support_signal_not_local_delivery_confirmation",
                "source_ids": ["mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak"],
                "claim_ids": ["clm__mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak_d5_001"],
            },
        ],
        "party_and_role_signals": [
            {
                "party_or_role": "Flevoland Gezond en Wel",
                "indicated_role": "preventiecoalitie die regionale ketenaanpakken ondersteunt",
                "authority": "municipal_policy_source",
                "validation_status": "support_signal_task_scope_needs_validation",
                "source_ids": ["mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak"],
                "claim_ids": ["clm__mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak_d5_001"],
            },
            {
                "party_or_role": "gemeente, zorgverzekeraar, eerstelijn, leefstijlcoaches, beweegaanbieders en sociaal domein",
                "indicated_role": "actoren die volgens de D5-richting nodig zijn voor de aanpak",
                "authority": "operational_requirements_layer",
                "validation_status": "actor_hint_not_local_role_confirmation",
                "source_ids": ["nat_azwa_opdracht_werkagenda_d5_2026", "nat_azwa_format_werkagenda_d5_2026"],
            },
        ],
        "finance_and_resource_signals": [
            {
                "signal_id": "adult_overweight_finance_mix_hint",
                "statement": (
                    "De beschikbare D5-richting wijst op een financieringsmix met Zvw, gemeentelijke "
                    "AZWA/SPUK-lijnen en gescheiden behandeling van bestaande GALA-middelen."
                ),
                "authority": "operational_requirements_layer",
                "validation_status": "finance_stream_hint_controller_validation_required",
                "source_ids": ["nat_vws_brief_azwa_d5_d6_financieringsinstrument_2026"],
            },
            {
                "signal_id": "adult_overweight_budget_table_signal",
                "statement": (
                    "De Almere gezondheidsbeleidsinformatie bevat een begrotingsregel voor aanpak "
                    "overgewicht en obesitas; scope, jaarschijf en inzet voor de werkagenda moeten "
                    "voor gebruik worden bevestigd."
                ),
                "authority": "municipal_policy_source",
                "validation_status": "low_authority_budget_signal_needs_controller_validation",
                "source_ids": ["mun_almere_2024_2026_visie_gezondheidsbeleid_beleidstekst"],
                "claim_ids": ["clm__mun_almere_2024_2026_visie_gezondheidsbeleid_beleidstekst_d5_002"],
            },
        ],
        "monitoring_and_learning_signals": [
            {
                "signal_id": "adult_overweight_ggd_indicators",
                "statement": (
                    "De GGD-indicatoren kunnen dienen als huidige informatie voor de opgave, maar "
                    "niet als monitoringafspraak voor de ketenaanpak."
                ),
                "authority": "public_table_book_source",
                "validation_status": "baseline_signal_not_monitoring_owner_confirmation",
                "source_ids": ["reg_ggd_flevoland_2024_volwassenen_gemeenten"],
            }
        ],
    },
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def index_by(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {str(item[key]): item for item in items if key in item}


def unique_strings(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


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
            "organisation": "Gemeente Almere as mandaatgemeente for IZA/AZWA-regio Flevoland, with preferente zorgverzekeraar and regional partners",
            "role": "municipal financing/coordination node and regional workagenda preparation; not the province and not proof of sole regional ownership",
            "source_id": "nat_zorgakkoorden_werkagenda_handvatten_2026",
        },
        "regional_coordination_entities": [
            {
                "organisation": "Verbindende Coalitie Zorgzaam Flevoland",
                "role": "regional steering/forum candidate for IZA-opgaven; decision authority and relation to colleges still need validation",
                "source_ids": [
                    "reg_noordoostpolder_iza_status_memo_2024",
                    "reg_provincie_flevoland_verbindende_coalitie_2024",
                ],
            },
            {
                "organisation": "Netwerkbureau Zorgzaam Flevoland",
                "role": "regional support bureau for overview, coherence, monitoring, learning and connection; host, reporting line and continuity still need validation",
                "source_ids": [
                    "reg_noordoostpolder_iza_status_memo_2024",
                    "reg_zonmw_zorgzaam_flevoland_project",
                    "reg_proscoop_zorgzaam_flevoland_netwerkbureau_2024",
                ],
            },
        ],
        "scale_guardrail": (
            "Almere always means the municipality. Flevoland can mean province, IZA/AZWA-regio, GGD-regio, "
            "zorgkantoor/ROAZ context or broader regional wording; write the intended scale explicitly."
        ),
        "primary_municipality_delivery_target": {
            "date": MUNICIPAL_DELIVERY_TARGET_DATE,
            "description": (
                "Main municipality-facing target date for Almere to deliver structured input to "
                "the regional workagenda process."
            ),
            "why_it_matters": (
                "The regional coordinator needs time after municipal delivery to consolidate local "
                "input before the formal regional adoption deadline."
            ),
            "status": "planning_assumption",
            "source_backing": "internal_planning_or_user_supplied; not national formal deadline",
            "must_surface_in_municipality_outputs": True,
        },
        "formal_workagenda_deadline": {
            "date": REGIONAL_ADOPTION_DEADLINE,
            "description": "Regional workagenda adopted by colleges",
            "status": "source_backed",
            "source_id": "nat_zorgakkoorden_werkagenda_handvatten_2026",
            "primary_audience": "regional coordinator and college adoption process",
        },
        "almere_internal_submission_target": {
            "date": MUNICIPAL_DELIVERY_TARGET_DATE,
            "description": "Target date for Almere to send structured input to the regional workagenda process",
            "status": "planning_assumption",
            "source_backing": "internal_planning_or_user_supplied; not national formal deadline",
        },
        "final_workagenda_format_context": {
            "source": FORMAT_SOURCE_REF,
            "format_status": "actual_format_for_final_regional_workagenda_input",
            "format_levels": [
                "regional_prevention_infrastructure",
                "leefgebied",
                "component_current_state_target_state_gap_project_plan",
            ],
            "almere_input_role": (
                "Almere can prepare component-level and local contribution input for this format, "
                "but the final regional workagenda is consolidated by the regional process."
            ),
            "status_boundary": (
                "A field may contain source-backed or likely/indicated input for the 15 September "
                "municipal handoff while still being unavailable as confirmed regional workagenda text."
            ),
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


def source_refs_for(
    row: dict[str, Any],
    operational_requirement: dict[str, Any] | None,
    capacity_item: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    refs = [NATIONAL_SOURCE_REF]
    if row["target_id"] == "valpreventie":
        refs.extend(VALPREVENTIE_SOURCE_REFS)
    if row["target_id"] == "ketenaanpak_overgewicht_obesitas_volwassenen":
        refs.extend(
            [
                {
                    "source_id": "reg_ggd_flevoland_2024_volwassenen_gemeenten",
                    "title": "GGD Flevoland Tabellenboek volwassenen 2024 - gemeenten",
                    "use_for": ["current information", "overweight and movement indicators"],
                    "authority": "public_table_book_source",
                    "confidence": "medium",
                },
                {
                    "source_id": "mun_almere_2024_2026_brede_spuk_gala_plan_van_aanpak",
                    "title": "Almere Brede SPUK / GALA plan van aanpak 2024-2026",
                    "use_for": ["regional prevention-chain support signal"],
                    "authority": "municipal_policy_source",
                    "confidence": "medium",
                },
            ]
        )

    source_ids = []
    if operational_requirement:
        source_ids.extend(operational_requirement.get("source_document_ids", []))
    if capacity_item:
        for indicator in capacity_item.get("public_indicators", []):
            if indicator.get("source_document_id"):
                source_ids.append(indicator["source_document_id"])

    for source_id in source_ids:
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
        "data/extracted/local_source_strengthening_almere.json",
        "data/extracted/municipal/almere_d6_responsibility_register.json",
        "data/raw/national/nat_azwa_format_werkagenda_d5_2026.docx",
        "data/site/source_view_models/format-werkagenda-azwa.json",
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


def build_workagenda_delivery_requirements(
    row: dict[str, Any],
    operational_requirement: dict[str, Any] | None,
) -> dict[str, Any]:
    if not operational_requirement:
        return {
            "status": "requirements_not_found_for_component",
            "required_sections": WORKAGENDA_REQUIRED_SECTIONS,
            "component_requirement_summary": {},
            "minimum_municipal_input_by_2026_09_15": [
                "safe component classification",
                "current information that can be shared without overclaiming",
                "main decisions or validations still needed",
            ],
        }

    # These are requirements and directional hints from generated source-backed
    # layers, not evidence that Almere has already made the local choices.
    return {
        "status": "requirements_available",
        "required_sections": WORKAGENDA_REQUIRED_SECTIONS,
        "component_requirement_summary": {
            "population_or_target_group": operational_requirement.get("population_or_target_group"),
            "coverage_or_capacity_direction": operational_requirement.get("coverage_or_capacity_direction"),
            "scale_hint": operational_requirement.get("scale_hint"),
            "related_component_ids": operational_requirement.get("related_target_ids", []),
            "almere_concept_status": operational_requirement.get("almere_concept_status"),
        },
        "source_document_ids": operational_requirement.get("source_document_ids", []),
        "source_claim_ids": operational_requirement.get("source_claim_ids", []),
        "minimum_municipal_input_by_2026_09_15": [
            "current local status: structureel, projectmatig, deels ingericht or still unclear",
            "known route, partners and current implementation signals",
            "validated or explicitly unvalidated owner and coordinator",
            "validated or explicitly unvalidated finance route",
            "main monitoring signal and owner if known",
            "decision or phasing question for the regional coordinator",
        ],
        "review_questions_from_requirement_layer": operational_requirement.get("review_questions", []),
    }


def actor_hints_from_requirement(operational_requirement: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not operational_requirement:
        return []
    return [
        {
            "party_or_role": actor,
            "indicated_role": "actor hint from the D5 operational requirement layer",
            "authority": "operational_requirements_layer",
            "validation_status": "actor_hint_not_local_role_confirmation",
            "source_ids": operational_requirement.get("source_document_ids", []),
        }
        for actor in operational_requirement.get("actor_hints", [])
    ]


def finance_hints_from_requirement(operational_requirement: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not operational_requirement:
        return []
    return [
        {
            "signal_id": f"finance_stream_hint_{index:02d}",
            "statement": stream,
            "authority": "operational_requirements_layer",
            "validation_status": "finance_stream_hint_not_controller_confirmation",
            "source_ids": operational_requirement.get("source_document_ids", []),
        }
        for index, stream in enumerate(operational_requirement.get("finance_stream_hints", []), start=1)
    ]


def indicators_as_monitoring_signals(capacity_item: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not capacity_item:
        return []
    signals: list[dict[str, Any]] = []
    for indicator in capacity_item.get("public_indicators", []):
        label = indicator.get("label")
        value = indicator.get("value")
        unit = indicator.get("unit", "")
        signals.append(
            {
                "signal_id": f"public_indicator_{indicator.get('indicator_id', len(signals) + 1)}",
                "statement": f"{label}: {value}{unit}",
                "authority": "public_indicator_source",
                "validation_status": "baseline_indicator_not_local_monitoring_arrangement",
                "source_ids": [indicator.get("source_document_id")] if indicator.get("source_document_id") else [],
            }
        )
    return signals


def build_available_information_for_workagenda(
    row: dict[str, Any],
    operational_requirement: dict[str, Any] | None,
    capacity_item: dict[str, Any] | None,
    source_need: dict[str, Any] | None,
) -> dict[str, Any]:
    component_id = row["target_id"]
    curated = CURATED_COMPONENT_ENRICHMENT.get(component_id, {})
    capacity_evidence = capacity_item.get("public_evidence", []) if capacity_item else []
    public_indicators = capacity_item.get("public_indicators", []) if capacity_item else []
    current_info = unique_strings([*row.get("public_evidence", []), *capacity_evidence])
    local_fill_fields = unique_strings(
        [
            *row.get("local_fill_fields", []),
            *(capacity_item.get("local_fill_fields", []) if capacity_item else []),
        ]
    )

    implementation_progress = curated.get("implementation_progress_signals", [])
    party_signals = [
        *actor_hints_from_requirement(operational_requirement),
        *curated.get("party_and_role_signals", []),
    ]
    finance_signals = [
        *finance_hints_from_requirement(operational_requirement),
        *curated.get("finance_and_resource_signals", []),
    ]
    monitoring_signals = [
        *indicators_as_monitoring_signals(capacity_item),
        *curated.get("monitoring_and_learning_signals", []),
    ]

    if implementation_progress:
        summary = (
            "There is already usable current information and implementation movement, but it must be "
            "kept separate from confirmed local decisions."
        )
    elif current_info or public_indicators:
        summary = (
            "There is current information for first regional orientation, but local implementation, "
            "ownership, finance and monitoring still need confirmation."
        )
    else:
        summary = "Only limited current information is available in the generated source-backed layers."

    return {
        "summary": summary,
        "source_backed_current_information": current_info,
        "public_indicators": public_indicators,
        "operational_direction": {
            "population_or_target_group": operational_requirement.get("population_or_target_group")
            if operational_requirement
            else None,
            "coverage_or_capacity_direction": operational_requirement.get("coverage_or_capacity_direction")
            if operational_requirement
            else None,
            "scale_hint": operational_requirement.get("scale_hint") if operational_requirement else None,
            "related_component_ids": operational_requirement.get("related_target_ids", [])
            if operational_requirement
            else [],
        },
        "implementation_progress_signals": implementation_progress,
        "party_and_role_signals": party_signals,
        "finance_and_resource_signals": finance_signals,
        "monitoring_and_learning_signals": monitoring_signals,
        "local_information_still_needed": local_fill_fields,
        "decisions_still_needed": row.get("decision_needed", []),
        "source_strengthening_candidates": {
            "candidate_source_ids": source_need.get("candidate_source_ids", []) if source_need else [],
            "still_needs_local_decision": source_need.get("still_needs_local_decision") if source_need else None,
            "note": source_need.get("note") if source_need else None,
        },
        "authority_boundary": (
            "Use source-backed and low-authority signals for first contact and 15 September input preparation; "
            "do not upgrade them to confirmed ownership, capacity, finance, monitoring or final workagenda text "
            "without local validation."
        ),
    }


def format_status_detail(status_id: str) -> dict[str, Any]:
    for item in FORMAT_INFORMATION_STATUS_MODEL:
        if item["status_id"] == status_id:
            return item
    return {
        "status_id": status_id,
        "meaning": "Status not defined in the format information status model.",
        "may_use_for_concept": False,
        "may_use_as_confirmed_workagenda_text": False,
    }


def compact_list(values: list[str], limit: int = 4) -> str:
    cleaned = [value for value in values if value]
    if not cleaned:
        return ""
    selected = cleaned[:limit]
    suffix = "" if len(cleaned) <= limit else f" Plus {len(cleaned) - limit} aanvullende signalen."
    return " ".join(selected) + suffix


def public_indicator_summary(capacity_item: dict[str, Any] | None) -> str:
    if not capacity_item:
        return ""
    indicators = []
    for indicator in capacity_item.get("public_indicators", [])[:5]:
        label = indicator.get("label")
        value = indicator.get("value")
        unit = indicator.get("unit", "")
        if label and value is not None:
            indicators.append(f"{label}: {value}{unit}")
    return "; ".join(indicators)


def signal_summary(signals: list[dict[str, Any]], key: str = "statement", limit: int = 3) -> str:
    return compact_list([str(signal.get(key, "")) for signal in signals], limit=limit)


def format_field(
    field_definition: dict[str, Any],
    draft_input: str,
    status_id: str,
    evidence_refs: list[str],
    validation_or_decision_needed: list[str],
    notes: str = "",
) -> dict[str, Any]:
    status = format_status_detail(status_id)
    return {
        "field_id": field_definition["field_id"],
        "label": field_definition["label"],
        "source_stage_label": field_definition.get("source_stage_label"),
        "project_vocabulary_group": field_definition.get("project_vocabulary_group"),
        "format_question": field_definition["format_question"],
        "draft_input_for_15_september": draft_input,
        "information_status": status_id,
        "status_meaning": status["meaning"],
        "may_use_for_15_september_concept": status["may_use_for_concept"],
        "may_use_as_confirmed_workagenda_text": status["may_use_as_confirmed_workagenda_text"],
        "evidence_refs": unique_strings(evidence_refs),
        "validation_or_decision_needed": validation_or_decision_needed,
        "notes": notes,
    }


def build_leefgebied_fields(
    row: dict[str, Any],
    operational_requirement: dict[str, Any] | None,
    available_information: dict[str, Any],
) -> dict[str, Any]:
    actor_hint_text = ", ".join(
        signal.get("party_or_role", "")
        for signal in available_information.get("party_and_role_signals", [])[:6]
        if signal.get("party_or_role")
    )
    operational_direction = available_information.get("operational_direction", {})
    health_input = compact_list(row.get("public_evidence", []), limit=3)
    if not health_input:
        health_input = "No component-specific health-goal input is available yet for this leefgebied."
    scope_input = operational_direction.get("scale_hint") or "Scope and coherence need to be confirmed for this leefgebied."
    roles_input = (
        f"Relevant actor signals for first contact: {actor_hint_text}."
        if actor_hint_text
        else "Organisation and roles still need to be mapped for this leefgebied."
    )
    return {
        "health_goals": format_field(
            LEEFGEBIED_FORMAT_FIELDS[0],
            health_input,
            "source_backed_current_information" if row.get("public_evidence") else "validation_needed",
            row.get("public_evidence", []),
            ["Translate component evidence into regional leefgebied goals and validate regionally."],
        ),
        "scope_and_coherence": format_field(
            LEEFGEBIED_FORMAT_FIELDS[1],
            scope_input,
            "likely_or_indicated" if operational_requirement else "validation_needed",
            operational_requirement.get("source_document_ids", []) if operational_requirement else [],
            ["Confirm scope, coherence with other leefgebieden and any D6 prerequisites."],
        ),
        "organisation_and_roles": format_field(
            LEEFGEBIED_FORMAT_FIELDS[2],
            roles_input,
            "likely_or_indicated" if actor_hint_text else "validation_needed",
            [
                source_id
                for signal in available_information.get("party_and_role_signals", [])
                for source_id in signal.get("source_ids", [])
            ],
            ["Confirm owner, coordinator, uitvoeringscapaciteit and financier roles for the leefgebied."],
        ),
    }


def build_milestone_rows(row: dict[str, Any]) -> list[dict[str, Any]]:
    local_deadline = row.get("deadline")
    rows = [
        {
            "period": "Q2-Q3 2026",
            "activities": [
                "Prepare Almere concept input for the actual workagenda format.",
                "Resolve the priority validation questions needed for first handoff.",
            ],
            "responsible": "Gemeente Almere policy owner and relevant validation actors; owner still to confirm",
            "partial_result": "Concept input with explicit unresolved fields.",
            "information_status": "planning_assumption",
        },
        {
            "period": "around 2026-09-15",
            "activities": [
                "Deliver structured Almere input to the regional workagenda process.",
            ],
            "responsible": "Gemeente Almere",
            "partial_result": "Municipal input available for regional consolidation.",
            "information_status": "planning_assumption",
        },
        {
            "period": "toward 2026-11-15",
            "activities": [
                "Regional process consolidates municipal and partner input.",
                "Move toward college adoption of the regional workagenda.",
            ],
            "responsible": "Regional workagenda process",
            "partial_result": "Regional workagenda adoption route.",
            "information_status": "source_backed_current_information",
        },
    ]
    if local_deadline:
        rows.insert(
            0,
            {
                "period": local_deadline,
                "activities": ["Component-level local action deadline from the current steering layer."],
                "responsible": str(row.get("action_owner", "owner still to confirm")),
                "partial_result": "Local action or validation step.",
                "information_status": "planning_assumption",
            },
        )
    return rows


def build_component_format_fields(
    row: dict[str, Any],
    operational_requirement: dict[str, Any] | None,
    capacity_item: dict[str, Any] | None,
    available_information: dict[str, Any],
) -> dict[str, Any]:
    current_info = available_information.get("source_backed_current_information", [])
    indicators = public_indicator_summary(capacity_item)
    implementation = signal_summary(available_information.get("implementation_progress_signals", []))
    party_signals = signal_summary(available_information.get("party_and_role_signals", []), key="party_or_role")
    finance_signals = signal_summary(available_information.get("finance_and_resource_signals", []))
    monitoring_signals = signal_summary(available_information.get("monitoring_and_learning_signals", []))
    local_needs = available_information.get("local_information_still_needed", [])
    decisions = available_information.get("decisions_still_needed", [])
    source_docs = operational_requirement.get("source_document_ids", []) if operational_requirement else []
    source_claims = operational_requirement.get("source_claim_ids", []) if operational_requirement else []

    urgency_input = compact_list(current_info, limit=3)
    if indicators:
        urgency_input = f"{urgency_input} Indicatoren: {indicators}".strip()
    situation_input = implementation or compact_list(row.get("public_evidence", []), limit=3)
    ambition_input = (
        operational_requirement.get("coverage_or_capacity_direction")
        if operational_requirement
        else "Ambition for regionally covering offer is not available in the current layer."
    )
    design_input = (
        f"Scale direction: {operational_requirement.get('scale_hint')}. Actor signals: {party_signals}."
        if operational_requirement
        else "Design choices and actor roles still need to be prepared."
    )
    project_objectives_input = (
        "SMART project objectives are not yet confirmed. Use current gaps and validation outcomes to turn "
        "priority, capacity, ownership and phasing into SMART agreements."
    )
    financial_input = finance_signals or "No validated financial plan is available yet."
    monitoring_input = monitoring_signals or "No validated monitoring arrangement is available yet."
    milestone_input = (
        "Use the milestone rows to separate Almere's 15 September municipal delivery from the later 15 November "
        "regional adoption process."
    )

    return {
        "current_state": {
            "urgency": format_field(
                COMPONENT_FORMAT_FIELDS[0],
                urgency_input or "Urgency input not available yet.",
                "source_backed_current_information" if urgency_input else "not_available_yet",
                [*row.get("public_evidence", []), *(indicator.get("source_document_id", "") for indicator in (capacity_item or {}).get("public_indicators", []))],
                ["Validate regional interpretation and priority for final workagenda wording."],
            ),
            "current_situation": format_field(
                COMPONENT_FORMAT_FIELDS[1],
                situation_input or "Current implementation situation not available yet.",
                "likely_or_indicated" if implementation else "validation_needed",
                [
                    source_id
                    for signal in available_information.get("implementation_progress_signals", [])
                    for source_id in signal.get("source_ids", [])
                ],
                local_needs or ["Confirm local status, coverage, capacity and constraints."],
            ),
        },
        "target_state": {
            "ambition": format_field(
                COMPONENT_FORMAT_FIELDS[2],
                ambition_input,
                "local_decision_needed",
                [*source_docs, *source_claims],
                ["Confirm what Almere and the region treat as regionally covering offer and phasing toward 2030."],
                "National direction can guide the concept, but local/regional ambition still needs decision or validation.",
            ),
            "design_choices": format_field(
                COMPONENT_FORMAT_FIELDS[3],
                design_input,
                "likely_or_indicated" if party_signals else "validation_needed",
                [
                    source_id
                    for signal in available_information.get("party_and_role_signals", [])
                    for source_id in signal.get("source_ids", [])
                ],
                [
                    "Confirm explicit design choices, owner/coordinator/executor roles and choices still open.",
                    "Confirm D6 dependency status before final workagenda text.",
                ],
            ),
        },
        "gap_project_plan": {
            "project_objectives": format_field(
                COMPONENT_FORMAT_FIELDS[4],
                project_objectives_input,
                "local_decision_needed",
                [],
                decisions or ["Decide priorities, phasing and SMART project agreements."],
            ),
            "financial_plan": format_field(
                COMPONENT_FORMAT_FIELDS[5],
                financial_input,
                "finance_controller_validation_needed",
                [
                    source_id
                    for signal in available_information.get("finance_and_resource_signals", [])
                    for source_id in signal.get("source_ids", [])
                ],
                ["Validate funding route, continuity, controller check and double-counting guardrails."],
            ),
            "monitoring": format_field(
                COMPONENT_FORMAT_FIELDS[6],
                monitoring_input,
                "validation_needed",
                [
                    source_id
                    for signal in available_information.get("monitoring_and_learning_signals", [])
                    for source_id in signal.get("source_ids", [])
                ],
                ["Confirm monitoring owner, indicators, reporting rhythm and learning-cycle use."],
            ),
            "milestone_planning": {
                **format_field(
                    COMPONENT_FORMAT_FIELDS[7],
                    milestone_input,
                    "planning_assumption",
                    [FORMAT_SOURCE_REF["source_id"], "nat_zorgakkoorden_werkagenda_handvatten_2026"],
                    ["Confirm component owner, activity planning, quarterly milestones and responsible actors."],
                ),
                "milestone_rows": build_milestone_rows(row),
            },
        },
    }


def build_rpi_alignment() -> dict[str, Any]:
    return {
        "format_fields": [
            {
                **field,
                "almere_input_role": (
                    "Almere can provide local signals and validation input, but the regional process must "
                    "consolidate this into the final RPI section."
                ),
                "information_status": "validation_needed",
            }
            for field in REGIONAL_PREVENTION_INFRASTRUCTURE_FORMAT_FIELDS
        ],
        "local_contribution_needed_by_2026_09_15": [
            "local signals for health goals and priority groups",
            "local finance/controller notes relevant to regional funding agreements",
            "local owner/coordinator/executor signals",
            "local monitoring indicators or data-owner signals",
            "known D6 dependencies and unresolved regional infrastructure questions",
        ],
        "boundary": "The RPI is a regional format section; this generated object only prepares Almere contribution fields.",
    }


def build_format_aligned_workagenda_input(
    row: dict[str, Any],
    operational_requirement: dict[str, Any] | None,
    capacity_item: dict[str, Any] | None,
    available_information: dict[str, Any],
) -> dict[str, Any]:
    component_id = row["target_id"]
    context = FORMAT_COMPONENT_CONTEXT.get(
        component_id,
        {
            "format_item_id": "unknown",
            "format_item_title": row.get("title"),
            "leefgebied": "unknown",
            "component_kind_in_format": row.get("category"),
            "format_match_status": "not_mapped",
        },
    )
    component_fields = build_component_format_fields(row, operational_requirement, capacity_item, available_information)
    confirmed_field_count = sum(
        1
        for group in component_fields.values()
        for value in group.values()
        if isinstance(value, dict) and value.get("information_status") == "confirmed_decision"
    )
    return {
        "format_source": FORMAT_SOURCE_REF,
        "format_alignment_status": "mapped_to_actual_vng_workagenda_format",
        "format_component_context": context,
        "information_status_model": FORMAT_INFORMATION_STATUS_MODEL,
        "regional_prevention_infrastructure_alignment": build_rpi_alignment(),
        "leefgebied_context": {
            "leefgebied": context.get("leefgebied"),
            "format_fields": build_leefgebied_fields(row, operational_requirement, available_information),
            "boundary": "Leefgebied fields are regional consolidation fields; Almere input is a contribution, not the final regional answer.",
        },
        "component_format_fields": component_fields,
        "readiness_summary": {
            "can_populate_format_as_concept": concept_handoff_ready(row),
            "can_populate_format_as_confirmed": bool(row.get("ready_for_workagenda_drafting")),
            "confirmed_field_count": confirmed_field_count,
            "status": "concept_fields_available_with_explicit_gaps"
            if concept_handoff_ready(row)
            else "insufficient_input_for_format",
            "main_not_confirmed_reasons": unresolved_reasons(row),
        },
        "handoff_boundary": (
            "This section makes the Almere object compatible with the actual workagenda format. "
            "It is still an Almere concept-input model and must not be treated as the final regional workagenda."
        ),
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
    operational_requirement: dict[str, Any] | None,
    capacity_item: dict[str, Any] | None,
    source_need: dict[str, Any] | None,
) -> dict[str, Any]:
    component_id = row["target_id"]
    ready = concept_handoff_ready(row)
    confirmed = bool(row.get("ready_for_workagenda_drafting"))
    ticket_ids = tickets_by_component.get(component_id, [])
    gap_summary = build_gap_summary(row)
    main_gaps = gap_summary["main_gaps"]
    available_information = build_available_information_for_workagenda(
        row,
        operational_requirement,
        capacity_item,
        source_need,
    )
    current_information = available_information["source_backed_current_information"]

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
        # This is deliberately repeated at object level so municipality-facing
        # outputs surface the 15 September delivery target before the regional
        # 15 November adoption deadline.
        "municipality_delivery_to_region": {
            "target_date": MUNICIPAL_DELIVERY_TARGET_DATE,
            "date_role": "primary_municipality_delivery_target",
            "description": (
                "Main target date for Almere to deliver structured concept input for this component "
                "to the regional workagenda process."
            ),
            "status": "planning_assumption",
            "why_before_regional_deadline": (
                "Regional coordination needs time to consolidate municipal input before the "
                f"{REGIONAL_ADOPTION_DEADLINE} formal adoption deadline."
            ),
            "must_surface_in_municipality_outputs": True,
        },
        "local_action_deadline": {
            "date": row.get("deadline"),
            "status": "status_matrix_local_action_deadline" if row.get("deadline") else "not_provided",
            "source": "data/workagenda/d5_status_matrix.json?deadline",
        },
        "almere_submission": {
            "submission_status": "concept_input" if ready else "not_ready_for_handoff",
            "target_delivery_to_region_date": MUNICIPAL_DELIVERY_TARGET_DATE,
            "target_delivery_to_region_note": (
                "For Almere and other municipalities, this is the main delivery target for input to "
                "the regional process; 15 November is the later regional adoption deadline."
            ),
            "concept_handoff_ready": ready,
            "confirmed_position_ready": confirmed,
            "recommended_submission_type": "confirmed_position"
            if confirmed
            else "concept_with_validation_gaps",
            "reason_not_confirmed": [] if confirmed else unresolved_reasons(row),
        },
        "almere_policy_input": build_policy_input(row),
        "current_state": {
            "known_from_public_sources": current_information,
            "known_or_indicated_local_elements": VALPREVENTIE_LOCAL_ELEMENTS
            if component_id == "valpreventie"
            else [],
            "unknown_or_unconfirmed": row.get("local_fill_fields", []),
        },
        "target_state_for_regional_workagenda": build_target_state(row),
        "workagenda_delivery_requirements": build_workagenda_delivery_requirements(
            row,
            operational_requirement,
        ),
        "available_information_for_workagenda": available_information,
        "format_aligned_workagenda_input": build_format_aligned_workagenda_input(
            row,
            operational_requirement,
            capacity_item,
            available_information,
        ),
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
            "source_refs": source_refs_for(row, operational_requirement, capacity_item),
            "public_evidence": row.get("public_evidence", []),
            "public_indicators": capacity_item.get("public_indicators", []) if capacity_item else [],
            "source_claim_ids": unique_strings(
                [
                    *(operational_requirement.get("source_claim_ids", []) if operational_requirement else []),
                    *[
                        claim_id
                        for group in CURATED_COMPONENT_ENRICHMENT.get(component_id, {}).values()
                        for signal in group
                        for claim_id in signal.get("claim_ids", [])
                    ],
                ]
            ),
            "evidence_limitations": [
                "Generated data layers are not public sources.",
                "Public-source signals do not equal confirmed local policy, finance, ownership or capacity.",
                (
                    "The 2026-09-15 Almere submission target is the main municipality-facing delivery "
                    "target for sending input to the region, but remains a planning assumption rather "
                    "than the national formal deadline."
                ),
                (
                    "The 2026-11-15 date is the regional college-adoption deadline; it should not be "
                    "presented as the main municipality delivery date."
                ),
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
        "enriched_information_object_count": sum(
            1
            for item in objects
            if item["available_information_for_workagenda"]["source_backed_current_information"]
            or item["available_information_for_workagenda"]["implementation_progress_signals"]
            or item["available_information_for_workagenda"]["public_indicators"]
        ),
        "implementation_progress_signal_count": sum(
            len(item["available_information_for_workagenda"]["implementation_progress_signals"])
            for item in objects
        ),
        "party_and_role_signal_count": sum(
            len(item["available_information_for_workagenda"]["party_and_role_signals"]) for item in objects
        ),
        "format_aligned_object_count": sum(
            1 for item in objects if item.get("format_aligned_workagenda_input")
        ),
        "format_confirmed_field_count": sum(
            item["format_aligned_workagenda_input"]["readiness_summary"]["confirmed_field_count"]
            for item in objects
            if item.get("format_aligned_workagenda_input")
        ),
        "format_source_id": FORMAT_SOURCE_REF["source_id"],
        "primary_municipality_delivery_target": MUNICIPAL_DELIVERY_TARGET_DATE,
        "municipality_delivery_to_region_target": MUNICIPAL_DELIVERY_TARGET_DATE,
        "almere_internal_submission_target": MUNICIPAL_DELIVERY_TARGET_DATE,
        "formal_workagenda_deadline": REGIONAL_ADOPTION_DEADLINE,
        "date_priority_note": (
            "Municipality-facing outputs should surface 2026-09-15 as the main delivery target for "
            "Almere input to the region. 2026-11-15 is the later regional adoption deadline."
        ),
        "status_note": (
            "Objects support concept handoff with visible gaps; they do not make any component a confirmed "
            "Almere position unless confirmed_position_ready is true."
        ),
    }


def build_layer() -> dict[str, Any]:
    matrix = load_json(STATUS_MATRIX)
    tickets = load_json(VALIDATION_TICKETS)
    operational_requirements = load_json(OPERATIONAL_REQUIREMENTS)
    nulmeting_capacity = load_json(NULMETING_CAPACITY)
    local_source_strengthening = load_json(LOCAL_SOURCE_STRENGTHENING)
    ticket_lookup = {item["ticket_id"]: item for item in tickets["tickets"]}
    tickets_by_component = tickets["tickets_by_component"]
    operational_by_target = index_by(operational_requirements.get("targets", []), "target_id")
    capacity_by_target = index_by(nulmeting_capacity.get("targets", []), "target_id")
    source_need_by_target = index_by(local_source_strengthening.get("target_source_needs", []), "target_id")
    objects = [
        build_object(
            row,
            tickets_by_component,
            ticket_lookup,
            operational_by_target.get(row["target_id"]),
            capacity_by_target.get(row["target_id"]),
            source_need_by_target.get(row["target_id"]),
        )
        for row in matrix["rows"]
    ]
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
