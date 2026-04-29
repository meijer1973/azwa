from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
EXTRACTED_DIR = DATA_DIR / "extracted"
SITE_DIR = DATA_DIR / "site"
CLAIMS_DIR = EXTRACTED_DIR / "claims"
MUNICIPAL_DIR = EXTRACTED_DIR / "municipal"

ALMERE_VIEW_PATH = MUNICIPAL_DIR / "almere_current_view.json"
CLAIMS_MASTER_PATH = CLAIMS_DIR / "claims_master.jsonl"
CURRENT_INTERPRETATION_PATH = CLAIMS_DIR / "current_interpretation.json"
INVENTORY_PATH = EXTRACTED_DIR / "document_inventory.json"
REVIEW_QUEUE_PATH = EXTRACTED_DIR / "review_queue.json"
SITE_TAXONOMY_PATH = REPO_ROOT / "config" / "site_taxonomy.json"
SITE_UPDATES_CONFIG_PATH = REPO_ROOT / "config" / "site_updates.json"
DATA_QUALITY_PERSPECTIVES_PATH = REPO_ROOT / "config" / "data_quality_perspectives.json"

DOCUMENTS_DIR = EXTRACTED_DIR / "documents"

HOME_VIEW_PATH = SITE_DIR / "site_home_view.json"
ALMERE_SITE_VIEW_PATH = SITE_DIR / "site_almere_view.json"
DASHBOARD_VIEW_PATH = SITE_DIR / "dashboard_view.json"
TIMELINE_REGISTER_PATH = SITE_DIR / "timeline_register.json"
TIMELINE_VIEW_PATH = SITE_DIR / "site_timeline_view.json"
THEMES_VIEW_PATH = SITE_DIR / "site_themes_view.json"
REFERENCE_VIEW_PATH = SITE_DIR / "site_reference_view.json"
SOURCES_VIEW_PATH = SITE_DIR / "site_sources_view.json"
SITE_UPDATES_VIEW_PATH = SITE_DIR / "site_updates_view.json"
SITE_MANIFEST_PATH = SITE_DIR / "site_manifest.json"
DECISION_DIR = SITE_DIR / "decision_view_models"
ACTION_DIR = SITE_DIR / "action_view_models"
THEME_DIR = SITE_DIR / "theme_view_models"
REFERENCE_TOPIC_DIR = SITE_DIR / "reference_topic_view_models"
SOURCE_VIEW_DIR = SITE_DIR / "source_view_models"
TIMELINE_CURATION_PATH = REPO_ROOT / "config" / "timeline_curation.json"

SITE_RUN_ID = "phase16_site_views_v1"
TODAY = date.today().isoformat()


TOPIC_LABELS = {
    "d5.definition": "D5-definitie",
    "d5.basisfunctionaliteiten_onderbouwd": "onderbouwde D5-basisfunctionaliteiten",
    "d5.implementation_enablers": "randvoorwaarden voor D5-uitvoering",
    "d5.ontwikkelagenda": "D5-ontwikkelagenda",
    "d5.other": "overige D5-lijn",
    "d5.regional_workagenda": "regionale/lokale D5-werkagenda",
    "d5.cross_domain_collaboration": "domeinoverstijgende samenwerking",
    "d5.mentale_gezondheidsnetwerken": "mentale gezondheidsnetwerken",
    "d5.health_first_shift": "verschuiving naar gezondheid en veerkracht",
    "d6.basisinfrastructuur": "D6-basisinfrastructuur",
    "d6.local_teams": "stevige lokale teams en wijkverbanden",
    "d6.digital_and_operational_infrastructure": "digitale en operationele infrastructuur",
    "d6.regional_coordination": "regionale coördinatie voor D6",
    "d6.other": "overige D6-lijn",
    "finance.azwa_macro_framework": "macrokader voor AZWA-financiering",
    "finance.d5_d6.funding_instrument": "bekostigingsroute D5/D6",
    "finance.d5_d6.municipal_funding": "gemeentelijke middelen D5/D6",
    "finance.local_alignment_goal": "lokale financiele aansluiting",
    "finance.regional_funding_path": "regionale financieringsroute",
    "governance.local_coalition": "lokale coalitie en samenwerking",
    "governance.national_coordination": "landelijke coordinatie",
    "governance.regional_coordination": "regionale coordinatie",
    "governance_and_finance.other": "overige governance- en financieringslijn",
    "monitoring.d5_operational_monitoring": "operationele D5-monitoring",
    "monitoring.framework": "monitoringskader",
    "monitoring.local_learning": "lokaal leren en bijsturen",
    "monitoring.local_goal_tracking": "lokale doelvolging",
    "monitoring.mid_term_review": "tussentijdse evaluatie",
    "monitoring.other": "overige monitoringslijn",
    "monitoring.regional_monitoring_plan": "regionaal monitoringsplan",
    "monitoring.update_2028": "actualisatiecyclus 2028",
    "municipal.almere_context": "Almeerse context",
    "municipal.role_allocation": "rolverdeling en regie",
    "municipal.implementation_translation": "lokale vertaling in openbare stukken",
    "municipal.almere_initiatives": "Almeerse initiatieven",
    "municipal.local_structure": "lokale structuur",
    "timeline.d5_d6_financing_horizon": "financieringshorizon D5/D6",
    "timeline.d5_d6_implementation": "implementatielijn D5/D6",
    "timeline.flevoland_transformatieagenda": "Flevolandse transformatieagenda",
    "timeline.implementation_status": "implementatiestatus",
    "timeline.local_governance_calendar": "lokale bestuurlijke kalender",
    "timeline.other": "overige tijdlijnmomenten",
    "timeline.rollout_2030": "landelijke dekking richting 2030",
    "timeline.almere_2029": "lokale horizon Positief Gezond Almere",
}

GAP_LABELS = {
    "gap_almere_d5_workagenda_mapping": {
        "title": "Lokale vertaling van D5 nog niet expliciet vastgelegd",
        "summary": (
            "In de huidige openbare Almere-documenten is nog niet expliciet zichtbaar hoe het landelijke "
            "D5-kader wordt vertaald naar doelgroepen, volgorde en interventiekeuze."
        ),
    },
    "gap_almere_d6_local_structure": {
        "title": "Lokale D6-structuur nog niet expliciet beschreven",
        "summary": (
            "De bronbasis laat nog niet expliciet zien hoe Almere de landelijke eis rond stevige lokale teams "
            "en hechte wijkverbanden bestuurlijk en organisatorisch invult."
        ),
    },
    "gap_almere_funding_choices": {
        "title": "Lokale verdeling van middelen nog niet expliciet zichtbaar",
        "summary": (
            "De landelijke bekostigingsroute is zichtbaar, maar de huidige bronbasis laat nog geen expliciete "
            "Almeerse keuze zien over verdeling van middelen, eigenaarschap en prioritering."
        ),
    },
    "gap_almere_monitoring_alignment": {
        "title": "Lokale monitoring nog niet expliciet gekoppeld aan regionale en landelijke cyclus",
        "summary": (
            "De huidige bronbasis laat nog geen expliciete Almeerse uitwerking zien van de koppeling tussen "
            "lokale monitoring, de Flevolandse monitoringsaanpak en de landelijke actualisatiecyclus."
        ),
    },
}

DEPENDENCY_LABELS = {
    "dep_regional_digital_infrastructure": {
        "title": "Regionale digitale infrastructuur in Flevoland",
        "summary": (
            "Almere is voor een deel afhankelijk van de regionale digitale infrastructuur, de "
            "gegevensuitwisselingsorganisatie en de gezamenlijke informatiearchitectuur in Flevoland."
        ),
        "next_step": "Regionale afstemming over architectuur, gegevensuitwisseling en lokale aansluiting concretiseren.",
    },
    "dep_national_funding_channel": {
        "title": "Landelijke keuze voor bekostigingsroute en inzet van middelen",
        "summary": (
            "De uiteindelijke route voor inzet en verstrekking van D5/D6-middelen is afhankelijk van landelijke "
            "afspraken tussen VNG, fondsbeheerders en VWS."
        ),
        "next_step": "Volgen en verwerken van landelijke uitwerking van de bekostigingsroute en startpakketten.",
    },
    "dep_regional_role_allocation": {
        "title": "Regionale rolverdeling en coordinatie",
        "summary": (
            "Voor Almere blijft de verdeling van rollen tussen gemeente, sociaal domein, zorgpartijen en "
            "de Flevolandse governance-structuur mede bepalend voor de uitvoerbaarheid."
        ),
        "next_step": "Bestuurlijke en ambtelijke rolverdeling regionaal expliciteren.",
    },
    "dep_national_update_cycle": {
        "title": "Landelijke D5/D6- en monitoringscyclus",
        "summary": (
            "De lokale fasering in Almere moet rekening houden met landelijke governance-afspraken, "
            "de tussentijdse evaluatie en de actualisatiecyclus richting 2028."
        ),
        "next_step": "Lokale planning koppelen aan landelijke evaluatie- en besluitmomenten.",
    },
}

DECISION_STATUS_LABELS = {
    "open": "open besluitvraag",
    "partly_resolved": "gedeeltelijk ingevuld",
    "blocked": "geblokkeerd door afhankelijkheid",
    "awaiting_clarification": "wacht op verduidelijking",
}

ACTION_STATUS_LABELS = {
    "not_started": "nog niet gestart",
    "in_preparation": "in voorbereiding",
    "blocked": "geblokkeerd door afhankelijkheid",
    "underway": "lopende uitwerking zichtbaar",
}

REVIEW_REASON_LABELS = {
    "authority_unclear": "lagere autoriteit vraagt menselijke duiding",
    "municipality_relevance_inferred": "lokale overname is nog niet expliciet zichtbaar",
    "unresolved_conflict": "begrips- of interpretatieduiding nodig",
}

DECISION_BLUEPRINTS = [
    {
        "decision_id": "dec_d5_prioritering",
        "choice_id": "choice_d5_prioritization",
        "gap_ids": ["gap_almere_d5_workagenda_mapping"],
        "dependency_ids": ["dep_national_update_cycle"],
        "theme_ids": ["basisfunctionaliteiten-d5", "governance-en-regie"],
        "linked_domain": "D5",
        "status": "partly_resolved",
        "title": "Mogelijke besluitvraag: prioritering van D5-interventies in Almere",
        "decision_question": "Welke D5-interventies worden in Almere als eerste expliciet uitgewerkt, voor welke doelgroepen en via welk lokaal of regionaal spoor?",
        "matter": "Zonder expliciete prioritering blijft onduidelijk welke D5-onderdelen bestuurlijk voorrang krijgen en hoe lokale en regionale inzet op elkaar aansluiten.",
        "non_decision": "Zonder expliciete keuze blijft de lokale vertaling van D5 versnipperd en lastiger bestuurlijk uitlegbaar.",
    },
    {
        "decision_id": "dec_d6_regiemodel",
        "choice_id": "choice_d6_governance_model",
        "gap_ids": ["gap_almere_d6_local_structure"],
        "dependency_ids": ["dep_regional_role_allocation"],
        "theme_ids": ["basisinfrastructuur-d6", "governance-en-regie"],
        "linked_domain": "D6",
        "status": "awaiting_clarification",
        "title": "Mogelijke besluitvraag: regiemodel voor D6 en lokale teams",
        "decision_question": "Hoe wil Almere eigenaarschap, regie en verantwoording organiseren rond D6, stevige lokale teams en hechte wijkverbanden?",
        "matter": "De term lokale teams komt in meerdere contexten voor; bestuurlijke duiding is nodig om uitvoering, regie en aanspreekbaarheid helder te maken.",
        "non_decision": "Zonder bestuurlijke afbakening blijft onduidelijk welke lokale structuur als uitvoeringsbasis voor D6 geldt.",
    },
    {
        "decision_id": "dec_budget_verdeling",
        "choice_id": "choice_budget_distribution",
        "gap_ids": ["gap_almere_funding_choices"],
        "dependency_ids": ["dep_national_funding_channel"],
        "theme_ids": ["financiering", "basisfunctionaliteiten-d5", "basisinfrastructuur-d6"],
        "linked_domain": "beide",
        "status": "blocked",
        "title": "Mogelijke besluitvraag: verdeling van beschikbare middelen over D5 en D6",
        "decision_question": "Hoe wil Almere beschikbare D5/D6-gerelateerde middelen verdelen tussen directe interventies, randvoorwaardelijke infrastructuur en bredere preventieve inzet?",
        "matter": "De inzet van middelen bepaalt welke onderdelen van D5 en D6 bestuurlijk en uitvoerend als eerste zichtbaar worden.",
        "non_decision": "Zonder financiele richting blijft lastig aantoonbaar hoe landelijke en regionale middelen lokaal worden vertaald.",
    },
    {
        "decision_id": "dec_monitoring_arrangement",
        "choice_id": "choice_monitoring_package",
        "gap_ids": ["gap_almere_monitoring_alignment"],
        "dependency_ids": ["dep_national_update_cycle", "dep_regional_role_allocation"],
        "theme_ids": ["monitoring-en-leren", "governance-en-regie"],
        "linked_domain": "beide",
        "status": "open",
        "title": "Mogelijke besluitvraag: monitoringsarrangement voor Almere",
        "decision_question": "Welke monitoringsset en welk bestuurlijk ritme wil Almere gebruiken om lokale uitvoering te koppelen aan Flevoland en landelijke D5/D6-cycli?",
        "matter": "Zonder expliciete monitoringskeuze blijft lastig te volgen hoe lokale voortgang, regionale afstemming en landelijke actualisatie op elkaar aansluiten.",
        "non_decision": "Zonder expliciet monitoringsarrangement blijft bestuurlijk overzicht beperkt en wordt bijsturing lastiger.",
    },
]

ACTION_BLUEPRINTS = [
    {
        "action_id": "act_d5_werkagenda_expliciteren",
        "kind": "gap",
        "source_id": "gap_almere_d5_workagenda_mapping",
        "linked_decision_ids": ["dec_d5_prioritering"],
        "dependency_ids": ["dep_national_update_cycle"],
        "theme_ids": ["basisfunctionaliteiten-d5", "governance-en-regie"],
        "linked_domain": "D5",
        "status": "in_preparation",
        "title": "Mogelijke opvolgactie: D5-vertaling voor Almere expliciteren",
        "action_statement": "Werk expliciet uit hoe de landelijke D5-basisfunctionaliteiten in Almere worden vertaald naar doelgroepen, interventies en lokale of regionale werksporen.",
        "intended_outcome": "Een expliciete lokale vertaling van D5 in openbare beleids- of uitvoeringsstukken.",
        "consequence": "Zonder explicitering blijft de lokale vertaling van D5 impliciet en moeilijk bestuurlijk te volgen.",
    },
    {
        "action_id": "act_d6_lokale_structuur_verduidelijken",
        "kind": "gap",
        "source_id": "gap_almere_d6_local_structure",
        "linked_decision_ids": ["dec_d6_regiemodel"],
        "dependency_ids": ["dep_regional_role_allocation"],
        "theme_ids": ["basisinfrastructuur-d6", "governance-en-regie"],
        "linked_domain": "D6",
        "status": "in_preparation",
        "title": "Mogelijke opvolgactie: lokale D6-structuur bestuurlijk verduidelijken",
        "action_statement": "Breng bestuurlijk en organisatorisch in kaart hoe Almere lokale teams, wijkverbanden en regie rond D6 expliciet wil positioneren.",
        "intended_outcome": "Een expliciete beschrijving van de lokale D6-structuur en de bestuurlijke rolverdeling.",
        "consequence": "Zonder expliciete beschrijving blijft onduidelijk welke lokale structuur als D6-basis geldt.",
    },
    {
        "action_id": "act_middelen_en_eigenaarschap_vastleggen",
        "kind": "gap",
        "source_id": "gap_almere_funding_choices",
        "linked_decision_ids": ["dec_budget_verdeling"],
        "dependency_ids": ["dep_national_funding_channel"],
        "theme_ids": ["financiering", "governance-en-regie"],
        "linked_domain": "beide",
        "status": "blocked",
        "title": "Mogelijke opvolgactie: inzet van middelen en eigenaarschap vastleggen",
        "action_statement": "Leg vast hoe Almere beschikbare middelen wil inzetten, wie bestuurlijk trekker is en hoe die inzet aansluit op landelijke en regionale bekostigingsroutes.",
        "intended_outcome": "Een bestuurlijk uitlegbare koppeling tussen middelen, eigenaarschap en lokale uitvoeringsrichting.",
        "consequence": "Zonder vastlegging blijft financiele doorvertaling voor Almere beperkt zichtbaar.",
    },
    {
        "action_id": "act_monitoring_afstemmen",
        "kind": "gap",
        "source_id": "gap_almere_monitoring_alignment",
        "linked_decision_ids": ["dec_monitoring_arrangement"],
        "dependency_ids": ["dep_national_update_cycle", "dep_regional_role_allocation"],
        "theme_ids": ["monitoring-en-leren", "governance-en-regie"],
        "linked_domain": "beide",
        "status": "in_preparation",
        "title": "Mogelijke opvolgactie: monitoringsaanpak voor Almere afstemmen",
        "action_statement": "Werk uit hoe lokale monitoring, het Flevolandse monitoringsspoor en landelijke evaluatiemomenten bestuurlijk met elkaar verbonden worden.",
        "intended_outcome": "Een bestuurlijk bruikbare monitorings- en leerstructuur voor Almere.",
        "consequence": "Zonder afstemming blijven lokale voortgang en regionale/landelijke vergelijkbaarheid beperkt.",
    },
    {
        "action_id": "act_regionale_digitale_aansluiting",
        "kind": "dependency",
        "source_id": "dep_regional_digital_infrastructure",
        "linked_decision_ids": [],
        "dependency_ids": ["dep_regional_digital_infrastructure"],
        "theme_ids": ["basisinfrastructuur-d6", "governance-en-regie"],
        "linked_domain": "D6",
        "status": "blocked",
        "title": "Mogelijke opvolgactie: regionale digitale aansluiting concretiseren",
        "action_statement": "Breng in kaart hoe Almere aansluit op de Flevolandse digitale infrastructuur, gegevensuitwisseling en informatiearchitectuur die voor D6 randvoorwaardelijk zijn.",
        "intended_outcome": "Duidelijkheid over regionale randvoorwaarden en lokale aansluitstappen.",
        "consequence": "Zonder concretisering blijft onduidelijk welke regionale infrastructuur beschikbaar is voor lokale uitvoering.",
    },
]

TIMELINE_DOCUMENT_SPECS = [
    {
        "document_id": "nat_iza_2022_integraal_zorgakkoord",
        "summary": "IZA legt het regionale samenwerkingsspoor vast waar latere D5/D6-uitwerking voor gemeenten en regio's op voortbouwt.",
        "linked_domain": "D5 en D6",
        "relation_type": "legt basis",
        "consequence_for_almere": "Maakt zichtbaar dat Almere zich in regionale en lokale uitwerking moet verhouden tot het bredere IZA-spoor.",
    },
    {
        "document_id": "nat_gala_2023_gezond_en_actief_leven",
        "summary": "GALA verbindt landelijke gezondheidsdoelen aan regionale en lokale uitvoering, waaronder ketenaanpakken die later ook in D5 terugkomen.",
        "linked_domain": "D5 en D6",
        "relation_type": "verbreedt",
        "consequence_for_almere": "Onderstreept dat landelijke doelen rond gezondheid en preventie lokaal herkenbaar gemaakt moeten worden.",
    },
    {
        "document_id": "nat_azwa_2025_definitief",
        "summary": "Het definitieve AZWA brengt D5 en D6 expliciet in de landelijke bestuurlijke lijn, inclusief werkagenda's, governance en evaluatiemomenten.",
        "linked_domain": "D5 en D6",
        "relation_type": "stelt vast",
        "consequence_for_almere": "Vanaf dit moment is er een duidelijke nationale basis waar Almere zich bestuurlijk toe moet verhouden.",
    },
    {
        "document_id": "nat_azwa_2025_aanbiedingsbrief",
        "summary": "De aanbiedingsbrief plaatst het akkoord formeel in het parlementaire en bestuurlijke vervolgspoor.",
        "linked_domain": "D5 en D6",
        "relation_type": "formaliseert",
        "consequence_for_almere": "Markeert dat de landelijke afspraken niet alleen inhoudelijk maar ook bestuurlijk worden doorgezet.",
    },
    {
        "document_id": "nat_azwa_2026_cw31_kader_d5_d6",
        "summary": "CW 3.1 werkt de ordening van basisfunctionaliteiten en basisinfrastructuur verder uit en maakt de D5/D6-kaders concreter.",
        "linked_domain": "D5 en D6",
        "relation_type": "werkt uit",
        "consequence_for_almere": "Geeft Almere en Flevoland een concreter referentiekader voor lokale en regionale vertaling.",
    },
    {
        "document_id": "nat_azwa_2026_voortgang_kamerbrief",
        "summary": "De voortgangsbrief beschrijft de implementatiestand en scherpt het bestuurlijke beeld rond D5, D6 en monitoring verder aan.",
        "linked_domain": "D5 en D6",
        "relation_type": "verduidelijkt",
        "consequence_for_almere": "Geeft richting aan welke onderdelen voor Almere bestuurlijk nog explicitering vragen.",
    },
]

TIMELINE_REFERENCE_SPECS = [
    {
        "entry_key": "d5_landelijk_kader_q4_2025",
        "date_label": "Q4 2025",
        "sort_key": "2025-12-31",
        "date_granularity": "quarter",
        "title": "Landelijk D5-kader vaststellen in BO IZA/AZWA",
        "summary": "In de akkoordtekst staat dat het landelijk D5-kader uiterlijk in Q4 2025 wordt vastgesteld en daarna periodiek wordt herijkt.",
        "linked_domain": "D5",
        "relation_type": "besluitmoment",
        "entry_type": "toekomstige beleidsstap",
        "consequence_for_almere": "Bepaalt welk landelijk referentiekader Almere gebruikt voor lokale en regionale vertaling van D5.",
        "claim_ids": [
            "clm__nat_azwa_2025_definitief_timeline_and_status_001"
        ],
        "topic_keys": [
            "timeline.d5_d6_implementation"
        ],
        "timeline_note": "Expliciete tijdverwijzing in de nationale akkoordtekst.",
    },
    {
        "entry_key": "d5_governance_q1_2026",
        "date_label": "Q1 2026",
        "sort_key": "2026-03-31",
        "date_granularity": "quarter",
        "title": "Governance voor beheer van de gereedschapskist uitwerken",
        "summary": "In de akkoordtekst staat dat VNG, ZN en VWS uiterlijk in Q1 2026 de governance voor beheer van de gereedschapskist en verdere uitwerking uitwerken.",
        "linked_domain": "D5",
        "relation_type": "uitwerking",
        "entry_type": "beleidsuitwerking",
        "consequence_for_almere": "Geeft meer duidelijkheid over de landelijke werkwijze waarmee Almere D5-onderdelen bestuurlijk moet volgen en vertalen.",
        "claim_ids": [
            "clm__nat_azwa_2025_definitief_timeline_and_status_001"
        ],
        "topic_keys": [
            "timeline.d5_d6_implementation"
        ],
        "timeline_note": "Expliciete tijdverwijzing in de nationale akkoordtekst.",
    },
    {
        "entry_key": "d6_regie_q1_2026",
        "date_label": "Q1 2026",
        "sort_key": "2026-03-31",
        "date_granularity": "quarter",
        "title": "Regionale afspraken over D6-structuur en regie bij ketenaanpakken",
        "summary": "In de akkoordtekst staat dat uiterlijk in Q1 2026 afspraken worden gemaakt over regionale structuurversterking, regie en aansluiting van stevige lokale teams.",
        "linked_domain": "D6",
        "relation_type": "uitwerking",
        "entry_type": "beleidsuitwerking",
        "consequence_for_almere": "Raakt direct aan de vraag hoe Almere lokale teams, wijkverbanden en bestuurlijke regie publiek en bestuurlijk positioneert.",
        "claim_ids": [
            "clm__nat_azwa_2025_definitief_d6_002"
        ],
        "topic_keys": [
            "d6.local_teams",
            "timeline.rollout_2030"
        ],
        "timeline_note": "Expliciete tijdverwijzing in de nationale akkoordtekst.",
    },
    {
        "entry_key": "mid_term_review_begin_2027",
        "date_label": "begin 2027",
        "sort_key": "2027-01-01",
        "date_granularity": "period",
        "title": "Tussentijdse evaluatie van IZA/AZWA",
        "summary": "De huidige interpretatielaag houdt vast aan een tussentijds evaluatiemoment begin 2027 waarin afspraken, middeleninzet en bestuurlijke accenten kunnen worden aangescherpt.",
        "linked_domain": "D5 en D6",
        "relation_type": "evaluatie",
        "entry_type": "toekomstig evaluatiemoment",
        "consequence_for_almere": "Kan leiden tot bijstelling van afspraken en vraagt dus dat Almere uiterlijk dan een navolgbaar lokaal beeld heeft van voortgang en keuzes.",
        "claim_ids": [
            "clm__nat_azwa_2025_definitief_monitoring_and_evaluation_002",
            "clm__nat_azwa_2026_voortgang_kamerbrief_monitoring_and_evaluation_001"
        ],
        "topic_keys": [
            "monitoring.mid_term_review"
        ],
        "timeline_note": "Huidige lijn uit de interpretatielaag, gebaseerd op twee nationale bronnen.",
    },
    {
        "entry_key": "decision_2028_before_july_2027",
        "date_label": "voor 1 juli 2027",
        "sort_key": "2027-07-01",
        "date_granularity": "deadline",
        "title": "Bestuurlijke besluitvorming over koers richting 2028",
        "summary": "De huidige interpretatielaag houdt vast aan besluitvorming voor 1 juli 2027 over 2028, inclusief mogelijke aanpassingen van afspraken of middeleninzet.",
        "linked_domain": "D5 en D6",
        "relation_type": "besluitmoment",
        "entry_type": "toekomstig besluitmoment",
        "consequence_for_almere": "Dit is een logisch ijkpunt waarop Almere de eigen lijn naast landelijke keuzes moet leggen en waar nodig lokale besluitvorming voorbereidt.",
        "claim_ids": [
            "clm__nat_azwa_2025_definitief_monitoring_and_evaluation_002"
        ],
        "topic_keys": [
            "monitoring.mid_term_review"
        ],
        "timeline_note": "Expliciete deadline in de nationale akkoordtekst.",
    },
    {
        "entry_key": "startpakket_2027_2028",
        "date_label": "2027-2028",
        "sort_key": "2027-07-02",
        "date_granularity": "period",
        "title": "Startpakket sociaal domein en evaluatieperiode",
        "summary": "De huidige interpretatielaag houdt vast aan een tweejarig startpakket voor 2027-2028 om maatregelen uit te werken en te evalueren, met een route naar structurele financiering.",
        "linked_domain": "D5 en D6",
        "relation_type": "financieringsvenster",
        "entry_type": "toekomstige financieringsstap",
        "consequence_for_almere": "Maakt zichtbaar dat lokale keuzes over inzet, eigenaarschap en verantwoording tijdig voorbereid moeten zijn voordat het financieringsvenster opent.",
        "claim_ids": [
            "clm__nat_azwa_2025_definitief_governance_and_finance_002"
        ],
        "topic_keys": [
            "finance.d5_d6.municipal_funding"
        ],
        "timeline_note": "Expliciete meerjarige verwijzing in de nationale akkoordtekst.",
    },
    {
        "entry_key": "update_2028",
        "date_label": "2028",
        "sort_key": "2028-01-01",
        "date_granularity": "year",
        "title": "Actualisatie van basisfunctionaliteiten",
        "summary": "De huidige interpretatielaag houdt vast aan een actualisatie van de basisfunctionaliteiten in 2028 op basis van monitoring en evaluatie.",
        "linked_domain": "D5",
        "relation_type": "actualisatie",
        "entry_type": "toekomstige beleidsstap",
        "consequence_for_almere": "Nieuwe landelijke duiding kan lokale prioritering, publieke verantwoording en de keuze van interventies opnieuw raken.",
        "claim_ids": [
            "clm__nat_azwa_2026_cw31_kader_d5_d6_monitoring_and_evaluation_001"
        ],
        "topic_keys": [
            "monitoring.update_2028"
        ],
        "timeline_note": "Huidige lijn uit CW 3.1 en de interpretatielaag.",
    },
    {
        "entry_key": "d6_q4_2028_local_teams",
        "date_label": "Q4 2028",
        "sort_key": "2028-10-01",
        "date_granularity": "quarter",
        "title": "Aansluiting van lokale teams in hechte wijkverbanden overal gereed",
        "summary": "De nationale akkoordtekst zegt dat de aansluiting van stevige lokale teams in hechte wijkverbanden uiterlijk in Q4 2028 overal gereed moet zijn.",
        "linked_domain": "D6",
        "relation_type": "implementatiehorizon",
        "entry_type": "toekomstige uitvoeringshorizon",
        "consequence_for_almere": "Legt een duidelijke landelijke eindhorizon onder de lokale vraag hoe Almere D6-structuur en wijkverbanden bestuurlijk en publiek zichtbaar maakt.",
        "claim_ids": [
            "clm__nat_azwa_2025_definitief_timeline_and_status_002"
        ],
        "topic_keys": [
            "timeline.rollout_2030",
            "d6.local_teams"
        ],
        "timeline_note": "Expliciete horizon in de nationale akkoordtekst.",
    },
    {
        "entry_key": "almere_impact_2029",
        "date_label": "2029",
        "sort_key": "2029-01-01",
        "date_granularity": "year",
        "title": "Lokale impacthorizon Positief Gezond Almere",
        "summary": "Het lokale transformatieplan koppelt leren en monitoring aan concrete impactdoelen die Almere in 2029 wil bereiken.",
        "linked_domain": "D5 en D6",
        "relation_type": "lokale horizon",
        "entry_type": "lokale uitvoeringshorizon",
        "consequence_for_almere": "Maakt zichtbaar dat Almere naast landelijke termijnen ook een eigen lokale resultaatshorizon heeft waar keuzes en monitoring op moeten aansluiten.",
        "claim_ids": [
            "clm__mun_almere_pga_transformatieplan_timeline_and_status_001",
            "clm__mun_almere_pga_transformatieplan_monitoring_and_evaluation_002"
        ],
        "topic_keys": [
            "timeline.almere_2029",
            "monitoring.local_goal_tracking"
        ],
        "timeline_note": "Lokale horizon uit het transformatieplan; nuttig voor bestuurlijke planning maar geen landelijke norm.",
    },
    {
        "entry_key": "rollout_2030",
        "date_label": "2030",
        "sort_key": "2030-01-01",
        "date_granularity": "year",
        "title": "Landelijke dekking van bekende basisfunctionaliteiten",
        "summary": "De huidige interpretatielaag houdt vast aan de landelijke horizon om met de bekende basisfunctionaliteiten naar dekking in 2030 toe te werken.",
        "linked_domain": "D5",
        "relation_type": "landelijke horizon",
        "entry_type": "toekomstige uitvoeringshorizon",
        "consequence_for_almere": "Geeft de langste horizon voor lokale en regionale uitwerking en maakt zichtbaar dat huidige keuzes onderdeel zijn van een meerjarige landelijke route.",
        "claim_ids": [
            "clm__nat_azwa_2025_definitief_timeline_and_status_002",
            "clm__nat_azwa_2026_voortgang_kamerbrief_timeline_and_status_002"
        ],
        "topic_keys": [
            "timeline.rollout_2030"
        ],
        "timeline_note": "Huidige lijn uit nationale bronnen en de interpretatielaag.",
    },
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: Path, payload: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def clear_generated_json_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    for item in path.glob("*.json"):
        item.unlink()


def slugify(value: str) -> str:
    collapsed = "".join(char.lower() if char.isalnum() else "-" for char in value)
    while "--" in collapsed:
        collapsed = collapsed.replace("--", "-")
    return collapsed.strip("-")


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def claim_map() -> dict[str, dict]:
    return {claim["claim_id"]: claim for claim in load_jsonl(CLAIMS_MASTER_PATH)}


def document_map() -> dict[str, dict]:
    inventory = load_json(INVENTORY_PATH)
    return {entry["document_id"]: entry for entry in inventory["documents"]}


def document_payload_map() -> dict[str, dict]:
    payloads: dict[str, dict] = {}
    for path in DOCUMENTS_DIR.glob("*.json"):
        payload = load_json(path)
        payloads[payload["document_id"]] = payload
    return payloads


def current_interpretation_topics() -> list[dict]:
    return load_json(CURRENT_INTERPRETATION_PATH)["topics"]


def current_topic_lookup(entries: list[dict]) -> dict[str, dict]:
    return {entry["topic"]: entry for entry in entries}


def theme_definitions() -> list[dict]:
    return load_json(SITE_TAXONOMY_PATH)["themes"]


def navigation_items() -> list[dict]:
    return load_json(SITE_TAXONOMY_PATH)["navigation"]


def site_meta() -> dict:
    return load_json(SITE_TAXONOMY_PATH)["site"]


def site_updates_config() -> dict:
    return load_json(SITE_UPDATES_CONFIG_PATH)


def data_quality_config() -> dict:
    return load_json(DATA_QUALITY_PERSPECTIVES_PATH)


def data_quality_perspectives() -> list[dict]:
    return data_quality_config()["perspectives"]


def data_quality_classification(classification_id: str) -> dict:
    for item in data_quality_config()["classifications"]:
        if item["classification_id"] == classification_id:
            return item
    raise KeyError(f"Unknown data quality classification: {classification_id}")


def timeline_curation() -> dict:
    return load_json(TIMELINE_CURATION_PATH)


def humanize_identifier(value: str) -> str:
    cleaned = value.replace(".", " ").replace("_", " ").replace("-", " ").strip()
    if not cleaned:
        return value
    return cleaned[0].upper() + cleaned[1:]


def topic_label(topic: str) -> str:
    return TOPIC_LABELS.get(topic, humanize_identifier(topic))


def topic_slug(topic: str) -> str:
    return slugify(topic.replace(".", "-"))


def topic_page_url(topic: str) -> str:
    return f"/reference/topics/{topic_slug(topic)}/"


def theme_page_url(theme_id: str) -> str:
    return f"/themes/{theme_id}/"


def source_page_url(document: dict) -> str:
    short_title = document.get("short_title") or document["title"]
    return f"/sources/{slugify(short_title)}/"


def perspective_ids_for_context(
    *,
    topic_ids: list[str] | None = None,
    theme_ids: list[str] | None = None,
    page_type: str | None = None,
    jurisdiction_level: str | None = None,
) -> list[str]:
    topic_ids = topic_ids or []
    theme_ids = theme_ids or []
    matched: list[str] = []
    for perspective in data_quality_perspectives():
        perspective_id = perspective["perspective_id"]
        if page_type and page_type in perspective.get("page_type_defaults", []):
            matched.append(perspective_id)
            continue
        if jurisdiction_level and jurisdiction_level in perspective.get("jurisdiction_level_hints", []):
            matched.append(perspective_id)
            continue
        if any(topic in perspective.get("topic_ids", []) for topic in topic_ids):
            matched.append(perspective_id)
            continue
        if any(
            topic.startswith(prefix)
            for topic in topic_ids
            for prefix in perspective.get("topic_prefixes", [])
        ):
            matched.append(perspective_id)
            continue
        if any(theme_id in perspective.get("theme_ids", []) for theme_id in theme_ids):
            matched.append(perspective_id)
            continue
    return dedupe(matched)


def quality_perspective_refs(perspective_ids: list[str]) -> list[dict]:
    lookup = {item["perspective_id"]: item for item in data_quality_perspectives()}
    return [
        {
            "perspective_id": perspective_id,
            "title": lookup[perspective_id]["title"],
            "question": lookup[perspective_id]["question"],
        }
        for perspective_id in perspective_ids
        if perspective_id in lookup
    ]


def quality_classification_ref(classification_id: str) -> dict:
    item = data_quality_classification(classification_id)
    return {
        "classification_id": item["classification_id"],
        "label": item["label"],
        "description": item["description"],
    }


def domain_for_topic(topic: str) -> str:
    if topic.startswith("d5."):
        return "D5"
    if topic.startswith("d6."):
        return "D6"
    if topic.startswith(("finance.", "governance.", "monitoring.", "timeline.", "municipal.")):
        return "D5 en D6"
    return "overig"


def status_label_for_topic(entry: dict) -> str:
    if entry["current_claim_ids"] and not entry["needs_human_review"]:
        return "huidige lijn zonder extra review"
    if entry["current_claim_ids"] and entry["needs_human_review"]:
        return "huidige lijn met menselijke duiding"
    if entry["historical_claim_ids"]:
        return "historische of verdrongen lijn"
    return "geen actuele lijn geselecteerd"


def confidence_label(score: float) -> str:
    if score >= 0.85:
        return "hoog"
    if score >= 0.6:
        return "middel"
    return "voorzichtig"


def source_classification_label(document: dict) -> str:
    mapping = {
        "primary": "primaire bron",
        "derivative": "afgeleide bron",
        "commentary": "toelichtende bron",
        "supporting_commentary": "toelichtende bron",
    }
    value = document.get("source_classification", "bron")
    return mapping.get(value, humanize_identifier(value).lower())


def document_type_label(document_type: str) -> str:
    mapping = {
        "agreement": "akkoord",
        "framework": "kader",
        "kamerbrief": "kamerbrief",
        "ministerial_letter": "ministeriële brief",
        "assignment": "opdracht",
        "template": "format",
        "process_note": "toelichting",
        "regulation": "regeling",
        "regional_plan": "regionaal plan",
        "regional_report": "regionaal rapport",
        "implementation_plan": "uitvoeringsplan",
        "research_report": "onderzoeksrapport",
        "program_page": "programmapagina",
        "topic_page": "onderwerppagina",
        "subsidy_page": "subsidiepagina",
        "government_info_page": "overheidsinformatiepagina",
        "sector_commentary_page": "sectorale duidingspagina",
        "members_letter": "ledenbrief",
        "municipal_policy_summary": "gemeentelijke beleidssamenvatting",
        "municipal_info_page": "gemeentelijke informatiepagina",
        "municipal_schedule_page": "gemeentelijk vergaderschema",
        "municipal_gateway_page": "gemeentelijke verwijspagina",
        "faq": "FAQ",
    }
    return mapping.get(document_type, humanize_identifier(document_type).lower())


def section_statement(section: dict) -> str | None:
    items = section.get("items") or []
    if items:
        return items[0]["statement"]
    relevance_note = section.get("relevance_note")
    if relevance_note:
        return relevance_note
    return None


def theme_ids_for_topics(topics: list[str], themes: list[dict]) -> list[str]:
    matched: list[str] = []
    for theme in themes:
        topic_ids = theme.get("topic_ids", [])
        topic_prefixes = theme.get("topic_prefixes", [])
        if any(topic in topic_ids for topic in topics):
            matched.append(theme["theme_id"])
            continue
        if any(topic.startswith(prefix) for topic in topics for prefix in topic_prefixes):
            matched.append(theme["theme_id"])
    return dedupe(matched)


def theme_lookup(themes: list[dict]) -> dict[str, dict]:
    return {theme["theme_id"]: theme for theme in themes}


def authority_note(claim: dict, document: dict | None = None) -> str | None:
    norm_status = claim.get("normative_status") or {}
    if norm_status.get("status") == "binding":
        return "Normstatus: formeel verplichtend of bindend volgens de broncategorie; blijf dicht bij de bronpassage."
    if norm_status.get("status") == "agreement":
        return "Normstatus: afspraak of akkoordtekst; niet automatisch als wettelijke plicht voor Almere formuleren."
    if norm_status.get("status") == "expectation":
        return "Normstatus: richtinggevende verwachting of uitwerkingskader; vermijd harde verplichtingstaal."
    if norm_status.get("status") == "lower_authority_signal":
        return "Normstatus: lagere-autoriteitssignaal; expliciet toeschrijven en niet als harde norm presenteren."
    if norm_status.get("status") == "guidance":
        return "Normstatus: toelichting, format, advies of praktische guidance."
    instrument_type = claim.get("instrument_type")
    document_type = document.get("document_type") if document else None
    publisher = document.get("publisher") if document else None
    if document_type == "municipal_schedule_page":
        return "Officiële lokale planning uit het vergaderschema van de Raad van Almere; relevant als lokaal bestuurlijk moment, niet als landelijke norm."
    if document_type == "sector_commentary_page":
        publisher_label = publisher or "deze sectorale duidingsbron"
        return f"Lagere autoriteit: deze passage is afkomstig uit een sectorale duidingspagina van {publisher_label}."
    if instrument_type == "faq":
        return "Lagere autoriteit: deze passage is afkomstig uit een VNG-FAQ."
    if instrument_type == "commentary":
        return "Lagere autoriteit: deze passage is afkomstig uit een toelichtende of samenvattende bron."
    if claim.get("source_statement_type") == "contextual_relevance":
        return "Relevantie voor Almere is afgeleid; expliciete lokale overname is niet altijd zichtbaar in de verzamelde openbare Almere-documenten."
    return None


def evidence_entries(claim_ids: list[str], claims: dict[str, dict], documents: dict[str, dict], limit: int = 6) -> list[dict]:
    entries: list[dict] = []
    for claim_id in claim_ids:
        claim = claims.get(claim_id)
        if claim is None:
            continue
        document = documents[claim["source_document_id"]]
        entries.append(
            {
                "claim_id": claim_id,
                "statement": claim["statement"],
                "topic": claim["topic"],
                "topic_label": topic_label(claim["topic"]),
                "document_id": document["document_id"],
                "document_title": document["title"],
                "publisher": document["publisher"],
                "publication_date": document["publication_date"],
                "source_url": document["source_url"],
                "page_url": source_page_url(document),
                "jurisdiction_level": document["jurisdiction_level"],
                "authority_note": authority_note(claim, document),
                "normative_status": claim.get("normative_status"),
                "time_status": claim.get("time_status"),
                "money_status": claim.get("money_status"),
                "governance_status": claim.get("governance_status"),
                "locality_status": claim.get("locality_status"),
                "needs_human_review": claim.get("human_review_status") == "needs_human_review",
            }
        )

    entries.sort(
        key=lambda item: (
            item["needs_human_review"],
            item["publication_date"] or "",
            item["document_title"],
        ),
        reverse=False,
    )
    return entries[:limit]


def document_refs_from_claim_ids(claim_ids: list[str], claims: dict[str, dict], documents: dict[str, dict]) -> list[dict]:
    by_id: dict[str, dict] = {}
    for claim_id in claim_ids:
        claim = claims.get(claim_id)
        if claim is None:
            continue
        document = documents[claim["source_document_id"]]
        if document["document_id"] in by_id:
            by_id[document["document_id"]]["topics"].append(topic_label(claim["topic"]))
            continue
        by_id[document["document_id"]] = {
            "document_id": document["document_id"],
            "title": document["title"],
            "publisher": document["publisher"],
            "publication_date": document["publication_date"],
            "document_type": document["document_type"],
            "jurisdiction_level": document["jurisdiction_level"],
            "status": document["status"],
            "source_url": document["source_url"],
            "page_url": source_page_url(document),
            "topics": [topic_label(claim["topic"])],
        }

    refs = list(by_id.values())
    for ref in refs:
        ref["topics"] = dedupe(ref["topics"])
    refs.sort(key=lambda item: (item["publication_date"] or "", item["title"]), reverse=True)
    return refs


def join_titles(document_refs: list[dict], max_items: int = 3) -> str:
    titles = [ref["title"] for ref in document_refs[:max_items]]
    if not titles:
        return "de huidige bronbasis"
    if len(titles) == 1:
        return titles[0]
    if len(titles) == 2:
        return f"{titles[0]} en {titles[1]}"
    return f"{', '.join(titles[:-1])} en {titles[-1]}"


def timeline_anchor(seed: str) -> str:
    return f"tijdlijn-{slugify(seed)}"


def timeline_year(sort_key: str) -> str:
    return sort_key[:4]


def timeline_temporal_status(sort_key: str, as_of_date: str = TODAY) -> str:
    if sort_key < as_of_date:
        return "verstreken referentie"
    if sort_key[:4] == as_of_date[:4]:
        return "komende stap"
    return "toekomstige referentie"


def timeline_time_status(entry_type: str, date_granularity: str, relation_type: str, temporal_status: str) -> dict:
    normalized_relation = relation_type.lower()
    if "deadline" in normalized_relation or "uiterste" in normalized_relation:
        status = "formal_deadline"
        label = "Formele of harde termijn"
        guardrail = "Gebruik als deadline alleen voor zover de bronbasis deze termijn expliciet draagt."
    elif "evaluatie" in normalized_relation or entry_type == "toekomstig evaluatiemoment":
        status = "review_or_update_moment"
        label = "Evaluatie-, herijkings- of actualisatiemoment"
        guardrail = "Gebruik als review- of bijsturingsmoment, niet automatisch als lokale besluitdatum."
    elif "financier" in normalized_relation or entry_type == "toekomstige financieringsstap":
        status = "budget_calendar_moment"
        label = "Begrotings- of financieringsmoment"
        guardrail = "Koppel aan de financiele bronroute; maak geen lokale budgetkeuze zonder lokale bron."
    elif entry_type in {"toekomstige uitvoeringshorizon", "lokale uitvoeringshorizon"}:
        status = "implementation_horizon"
        label = "Implementatiehorizon"
        guardrail = "Gebruik als horizon of fasering; vermijd precieze lokale planning zonder lokale bron."
    elif "lokaal" in normalized_relation or entry_type == "beleidsuitwerking" and date_granularity == "date":
        status = "local_planning_context"
        label = "Lokale planningscontext"
        guardrail = "Gebruik als lokale bestuurlijke context; niet als landelijke of inhoudelijke D5/D6-deadline."
    elif temporal_status == "verstreken referentie" and entry_type == "bronmoment":
        status = "publication_or_context_date"
        label = "Publicatie- of contextdatum"
        guardrail = "Gebruik als bron- of contextdatum; niet als beleidsdeadline."
    elif date_granularity in {"quarter", "month", "period"}:
        status = "expected_moment"
        label = "Verwacht of indicatief moment"
        guardrail = "Formuleer als verwacht, indicatief of bronafhankelijk moment; niet als harde deadline."
    else:
        status = "source_dated_moment"
        label = "Bronverankerd tijdmoment"
        guardrail = "Gebruik als bronverankerd tijdmoment en controleer de bronpassage voor precieze formulering."

    return {
        "status": status,
        "label": label,
        "date_granularity": date_granularity,
        "public_wording_guardrail": guardrail,
        "needs_review": status in {"expected_moment", "local_planning_context"},
    }


def timeline_entry_type_label(value: str) -> str:
    labels = {
        "bronmoment": "brondocument",
        "toekomstige beleidsstap": "beleidsstap",
        "beleidsuitwerking": "beleidsuitwerking",
        "toekomstig evaluatiemoment": "evaluatiemoment",
        "toekomstig besluitmoment": "besluitmoment",
        "toekomstige financieringsstap": "financieringsstap",
        "toekomstige uitvoeringshorizon": "uitvoeringshorizon",
        "lokale uitvoeringshorizon": "lokale horizon",
    }
    return labels.get(value, value)


def timeline_document_ref(document: dict, topics: list[str] | None = None) -> dict:
    return {
        "document_id": document["document_id"],
        "title": document["title"],
        "publisher": document["publisher"],
        "publication_date": document["publication_date"],
        "document_type": document["document_type"],
        "jurisdiction_level": document["jurisdiction_level"],
        "status": document["status"],
        "source_url": document["source_url"],
        "page_url": source_page_url(document),
        "topics": topics or [],
    }


def timeline_source_ref(source: dict) -> dict:
    return {
        "title": source["title"],
        "publisher": source["publisher"],
        "publication_date": source.get("publication_date"),
        "document_type": source.get("document_type", "reference"),
        "jurisdiction_level": source.get("jurisdiction_level", "national"),
        "status": source.get("status", "reference"),
        "source_url": source["source_url"],
        "topics": source.get("topics", []),
        **({"page_url": source["page_url"]} if source.get("page_url") else {}),
    }


def topics_for_claim_ids(claim_ids: list[str], claims: dict[str, dict]) -> list[str]:
    return dedupe([claims[claim_id]["topic"] for claim_id in claim_ids if claim_id in claims])


def source_notes_for_claim_ids(claim_ids: list[str], claims: dict[str, dict], documents: dict[str, dict]) -> list[str]:
    notes = []
    for claim_id in claim_ids:
        claim = claims.get(claim_id)
        if claim is None:
            continue
        note = authority_note(claim, documents.get(claim["source_document_id"]))
        if note:
            notes.append(note)
    return dedupe(notes)


def source_basis_for_claim_ids(claim_ids: list[str], claims: dict[str, dict], documents: dict[str, dict]) -> list[dict]:
    return document_refs_from_claim_ids(claim_ids, claims, documents)


def timeline_counts_as_future(entry: dict) -> bool:
    return entry["temporal_status"] in {"komende stap", "toekomstige referentie"}


def related_timeline_models(
    models: list[dict],
    claim_ids: list[str],
    topic_keys: list[str],
    claims: dict[str, dict],
    id_key: str,
) -> list[dict]:
    claim_set = set(claim_ids)
    topic_set = set(topic_keys)
    related: list[dict] = []
    for model in models:
        model_claim_ids = [claim_id for claim_id in model.get("supporting_claim_ids", []) if claim_id in claims]
        model_topics = set(topics_for_claim_ids(model_claim_ids, claims))
        if claim_set.intersection(model_claim_ids) or topic_set.intersection(model_topics):
            related.append(
                {
                    id_key: model[id_key],
                    "title": model["title"],
                    "status": model["status"],
                    "page_url": model["page_url"],
                }
            )
    related.sort(key=lambda item: item["title"])
    return related


def timeline_models_by_ids(models: list[dict], ids: list[str], id_key: str) -> list[dict]:
    lookup = {model[id_key]: model for model in models}
    related = []
    for item_id in ids:
        model = lookup.get(item_id)
        if model is None:
            continue
        related.append(
            {
                id_key: model[id_key],
                "title": model["title"],
                "status": model["status"],
                "page_url": model["page_url"],
            }
        )
    return related


def document_timeline_entry_from_spec(spec: dict, documents: dict[str, dict]) -> dict:
    document = documents[spec["document_id"]]
    entry_id = timeline_anchor(f"{document['publication_date']}-{document['document_id']}")
    temporal_status = timeline_temporal_status(document["publication_date"])
    time_status = timeline_time_status("bronmoment", "date", spec["relation_type"], temporal_status)
    return {
        "entry_key": document["document_id"],
        "entry_id": entry_id,
        "year": timeline_year(document["publication_date"]),
        "date_label": document["publication_date"],
        "date_granularity": "date",
        "sort_key": document["publication_date"],
        "temporal_status": temporal_status,
        "time_status": time_status,
        "title": document["title"],
        "summary": spec["summary"],
        "linked_domain": spec["linked_domain"],
        "relation_type": spec["relation_type"],
        "entry_type": "bronmoment",
        "entry_type_label": timeline_entry_type_label("bronmoment"),
        "consequence_for_almere": spec["consequence_for_almere"],
        "timeline_note": "Bronmoment in de beleidslijn.",
        "needs_human_review": False,
        "source_basis": [timeline_document_ref(document)],
        "source_notes": [],
        "linked_decisions": [],
        "linked_actions": [],
        "page_url": f"/timeline/#{entry_id}",
    }


def reference_timeline_entry_from_spec(
    spec: dict,
    claims: dict[str, dict],
    documents: dict[str, dict],
    current_topics: dict[str, dict],
    decision_models: list[dict],
    action_models: list[dict],
) -> dict:
    claim_ids = [claim_id for claim_id in spec["claim_ids"] if claim_id in claims]
    topic_keys = dedupe(spec.get("topic_keys", []) + topics_for_claim_ids(claim_ids, claims))
    needs_human_review = spec.get("force_human_review", False) or any(
        current_topics.get(topic, {}).get("needs_human_review") for topic in topic_keys
    )
    entry_id = timeline_anchor(f"{spec['sort_key']}-{spec['entry_key']}")
    temporal_status = timeline_temporal_status(spec["sort_key"])
    time_status = timeline_time_status(spec["entry_type"], spec["date_granularity"], spec["relation_type"], temporal_status)
    return {
        "entry_key": spec["entry_key"],
        "entry_id": entry_id,
        "year": timeline_year(spec["sort_key"]),
        "date_label": spec["date_label"],
        "date_granularity": spec["date_granularity"],
        "sort_key": spec["sort_key"],
        "temporal_status": temporal_status,
        "time_status": time_status,
        "title": spec["title"],
        "summary": spec["summary"],
        "linked_domain": spec["linked_domain"],
        "relation_type": spec["relation_type"],
        "entry_type": spec["entry_type"],
        "entry_type_label": timeline_entry_type_label(spec["entry_type"]),
        "consequence_for_almere": spec["consequence_for_almere"],
        "timeline_note": spec["timeline_note"],
        "needs_human_review": needs_human_review,
        "supporting_claim_ids": claim_ids,
        "topic_keys": topic_keys,
        "source_basis": source_basis_for_claim_ids(claim_ids, claims, documents),
        "source_notes": source_notes_for_claim_ids(claim_ids, claims, documents),
        "linked_decisions": related_timeline_models(decision_models, claim_ids, topic_keys, claims, "decision_id"),
        "linked_actions": related_timeline_models(action_models, claim_ids, topic_keys, claims, "action_id"),
        "page_url": f"/timeline/#{entry_id}",
    }


def external_timeline_entry_from_spec(
    spec: dict,
    decision_models: list[dict],
    action_models: list[dict],
) -> dict:
    entry_id = timeline_anchor(f"{spec['sort_key']}-{spec['entry_key']}")
    temporal_status = timeline_temporal_status(spec["sort_key"])
    time_status = timeline_time_status(spec["entry_type"], spec["date_granularity"], spec["relation_type"], temporal_status)
    return {
        "entry_key": spec["entry_key"],
        "entry_id": entry_id,
        "year": timeline_year(spec["sort_key"]),
        "date_label": spec["date_label"],
        "date_granularity": spec["date_granularity"],
        "sort_key": spec["sort_key"],
        "temporal_status": temporal_status,
        "time_status": time_status,
        "title": spec["title"],
        "summary": spec["summary"],
        "linked_domain": spec["linked_domain"],
        "relation_type": spec["relation_type"],
        "entry_type": spec["entry_type"],
        "entry_type_label": timeline_entry_type_label(spec["entry_type"]),
        "consequence_for_almere": spec["consequence_for_almere"],
        "timeline_note": spec["timeline_note"],
        "needs_human_review": spec.get("needs_human_review", False),
        "topic_keys": spec.get("topic_keys", []),
        "source_basis": [timeline_source_ref(item) for item in spec.get("source_basis", [])],
        "source_notes": spec.get("source_notes", []),
        "linked_decisions": timeline_models_by_ids(
            decision_models,
            spec.get("linked_decision_ids", []),
            "decision_id",
        ),
        "linked_actions": timeline_models_by_ids(
            action_models,
            spec.get("linked_action_ids", []),
            "action_id",
        ),
        "page_url": f"/timeline/#{entry_id}",
    }


def ordered_timeline_years(years: list[str], current_year: str) -> list[str]:
    future_years = sorted((year for year in years if year > current_year))
    past_years = sorted((year for year in years if year < current_year), reverse=True)
    ordered: list[str] = []
    if current_year in years:
        ordered.append(current_year)
    ordered.extend(future_years)
    ordered.extend(past_years)
    return ordered


def ordered_timeline_entries(entries: list[dict], as_of_date: str) -> list[dict]:
    return sorted(entries, key=lambda entry: (entry["sort_key"], entry["title"]))


def review_summary_for_reason(reason_code: str) -> str:
    mapping = {
        "authority_unclear": "Brondocumenten met lagere autoriteit vragen expliciete bronduiding in menselijke samenvattingen.",
        "municipality_relevance_inferred": "Er is een landelijk of regionaal spoor zichtbaar, maar in openbare Almere-documenten is lokale overname nog niet expliciet vastgelegd.",
        "unresolved_conflict": "Begrippen of lokale vertalingen worden in meerdere contexten gebruikt en vragen bestuurlijke of beleidsmatige duiding.",
    }
    return mapping.get(reason_code, "Menselijke duiding is nodig voordat dit punt als bestuurlijk uitgewerkte lijn kan worden gepresenteerd.")


def choice_map(almere_view: dict) -> dict[str, dict]:
    return {item["choice_id"]: item for item in almere_view["items_requiring_political_choice"]}


def gap_map(almere_view: dict) -> dict[str, dict]:
    return {item["gap_id"]: item for item in almere_view["local_gaps"]}


def dependency_map(almere_view: dict) -> dict[str, dict]:
    return {item["dependency_id"]: item for item in almere_view["local_dependencies"]}


def conflict_map(almere_view: dict) -> dict[str, dict]:
    return {item["topic"]: item for item in almere_view["unresolved_conflicts"]}


def uncertain_map(almere_view: dict) -> dict[str, dict]:
    return {item["topic"]: item for item in almere_view["uncertain_items"]}


def linked_domain_label(value: str) -> str:
    if value == "D5":
        return "D5"
    if value == "D6":
        return "D6"
    return "D5 en D6"


def review_note_for_topics(topics: list[str], uncertainty_by_topic: dict[str, dict], conflict_by_topic: dict[str, dict]) -> str | None:
    relevant_uncertain = [uncertainty_by_topic[topic] for topic in topics if topic in uncertainty_by_topic]
    relevant_conflicts = [conflict_by_topic[topic] for topic in topics if topic in conflict_by_topic]
    if relevant_conflicts:
        return "Menselijke duiding nodig: de betrokken begrippen of lokale vertalingen worden in meerdere contexten gebruikt."
    if relevant_uncertain:
        return "Menselijke duiding nodig: een deel van de relevante bronbasis bestaat uit lagere autoriteit of afgeleide lokale relevantie."
    return None


def review_details_for_topics(
    topics: list[str],
    supporting_evidence: list[dict],
    uncertainty_by_topic: dict[str, dict],
    conflict_by_topic: dict[str, dict],
) -> dict | None:
    note = review_note_for_topics(topics, uncertainty_by_topic, conflict_by_topic)
    if note is None:
        return None

    issue_items: list[dict] = []
    for topic in topics:
        if topic in conflict_by_topic:
            conflict = conflict_by_topic[topic]
            issue_items.append(
                {
                    "topic": topic,
                    "topic_label": topic_label(topic),
                    "reason_label": review_reason_label("unresolved_conflict"),
                    "summary": conflict_note(conflict),
                    "recommended_action": conflict_resolution_label(conflict["recommended_resolution_rule"]),
                }
            )
        elif topic in uncertainty_by_topic:
            issue_items.append(
                {
                    "topic": topic,
                    "topic_label": topic_label(topic),
                    "reason_label": "lagere autoriteit of afgeleide lokale relevantie",
                    "summary": (
                        "Rond dit onderwerp bevat de huidige bronbasis naast de landelijke basis ook bronnen met lagere autoriteit "
                        "of passages waarvan de relevantie voor Almere vooral uit context is afgeleid."
                    ),
                    "recommended_action": (
                        "Maak in bestuurlijke duiding expliciet welke bron de landelijke basis vormt en waar Almere publieke "
                        "overname nog niet expliciet heeft vastgelegd."
                    ),
                }
            )

    source_signals: list[dict] = []
    seen_sources: set[str] = set()
    for evidence in supporting_evidence:
        if not (evidence.get("authority_note") or evidence.get("needs_human_review")):
            continue
        if evidence["document_id"] in seen_sources:
            continue
        seen_sources.add(evidence["document_id"])
        source_signals.append(
            {
                "document_title": evidence["document_title"],
                "publisher": evidence["publisher"],
                "publication_date": evidence["publication_date"],
                "topic_label": evidence["topic_label"],
                "summary": evidence.get("authority_note")
                or "Menselijke duiding nodig voordat deze passage als expliciete lokale vastlegging kan worden gepresenteerd.",
            }
        )

    return {
        "note": note,
        "section_url": "#menselijke-duiding",
        "issues": issue_items,
        "source_signals": source_signals,
    }


def conflict_resolution_label(rule: str) -> str:
    mapping = {
        "municipal_documents_cannot_override_national_obligations": "Lokale documenten kunnen de landelijke basis niet wijzigen; duiding van de lokale vertaling is nodig.",
        "guidance_may_clarify_but_not_override_stronger_norm": "Uitwerking kan verduidelijken, maar wijzigt geen bron met hogere autoriteit.",
    }
    return mapping.get(rule, "Menselijke duiding nodig om de verhouding tussen bronnen en lokale vertaling expliciet te maken.")


def conflict_note(conflict: dict) -> str:
    if conflict["conflict_type"] == "localization_overlap":
        return (
            "De landelijke basis blijft leidend, terwijl regionale of lokale vertalingen daarnaast blijven bestaan. "
            "Menselijke duiding is nodig om te bepalen hoe Almere dit bestuurlijk en publiek moet formuleren."
        )
    if conflict["conflict_type"] == "implementation_layering":
        return (
            "De beschikbare bronnen lijken eerder verschillende uitvoeringslagen te beschrijven dan een harde tegenspraak. "
            "Menselijke duiding is nodig om de lagen en definities expliciet te maken."
        )
    return "Er blijft menselijke duiding nodig om te bepalen hoe deze bronrelatie voor Almere moet worden geïnterpreteerd."


def review_reason_label(reason_code: str) -> str:
    return REVIEW_REASON_LABELS.get(reason_code, reason_code.replace("_", " "))


def scope_label(scope: str) -> str:
    labels = {
        "national": "landelijke basis",
        "mixed": "landelijke basis met regionale of lokale uitwerking",
        "regional": "regionale basis",
        "municipal": "lokale basis",
    }
    return labels.get(scope, scope)


def status_group_for_decision(status: str) -> str:
    mapping = {
        "open": "open_decisions",
        "partly_resolved": "partly_resolved",
        "blocked": "blocked",
        "awaiting_clarification": "awaiting_clarification",
    }
    return mapping[status]


def status_group_for_action(status: str) -> str:
    mapping = {
        "not_started": "not_started",
        "in_preparation": "in_preparation",
        "blocked": "blocked",
        "underway": "underway",
    }
    return mapping[status]


def option_set(decision_id: str) -> list[dict]:
    if decision_id == "dec_d5_prioritering":
        return [
            {
                "option_id": "opt_local_explicitering",
                "title": "Lokale prioritering expliciet vastleggen",
                "type": "afgeleide optie",
                "summary": "Leg in een bestuurlijk of beleidsmatig spoor vast welke D5-interventies voor Almere eerst worden uitgewerkt.",
            },
            {
                "option_id": "opt_regionale_aansluiting",
                "title": "Eerst regionaal uitwerken, daarna lokaal preciseren",
                "type": "afgeleide optie",
                "summary": "Sluit primair aan op regionale uitwerking en concretiseer pas daarna de lokale vertaling.",
            },
            {
                "option_id": "opt_huidige_lijn",
                "title": "Huidige impliciete lijn handhaven",
                "type": "afgeleide optie",
                "summary": "Werk voorlopig door via bestaande initiatieven zonder expliciete lokale prioritering in openbare stukken.",
            },
        ]
    if decision_id == "dec_d6_regiemodel":
        return [
            {
                "option_id": "opt_explicit_local_model",
                "title": "Expliciet lokaal regiemodel vastleggen",
                "type": "afgeleide optie",
                "summary": "Leg expliciet vast hoe lokale teams, wijkverbanden en regie bestuurlijk zijn georganiseerd.",
            },
            {
                "option_id": "opt_regional_alignment_first",
                "title": "Eerst regionale afbakening, daarna lokale vastlegging",
                "type": "afgeleide optie",
                "summary": "Gebruik eerst regionale rolverdeling en governance-afspraken als kader voor lokale concretisering.",
            },
            {
                "option_id": "opt_functional_description",
                "title": "Alleen functionele beschrijving opnemen",
                "type": "afgeleide optie",
                "summary": "Beperk lokale vastlegging voorlopig tot functies, taken en samenwerkingsafspraken zonder volledig regiemodel.",
            },
        ]
    if decision_id == "dec_budget_verdeling":
        return [
            {
                "option_id": "opt_interventions_first",
                "title": "Eerst directe interventies financieren",
                "type": "afgeleide optie",
                "summary": "Geef prioriteit aan interventies die direct zichtbaar zijn voor inwoners en professionals.",
            },
            {
                "option_id": "opt_infrastructure_first",
                "title": "Eerst randvoorwaardelijke infrastructuur financieren",
                "type": "afgeleide optie",
                "summary": "Leg het accent eerst op regie, gegevensuitwisseling, lokale teams en andere uitvoeringsvoorwaarden.",
            },
            {
                "option_id": "opt_balanced_portfolio",
                "title": "Gespreide inzet over interventies en infrastructuur",
                "type": "afgeleide optie",
                "summary": "Verdeel middelen over directe interventies, infrastructuur en preventieve doorontwikkeling.",
            },
        ]
    return [
        {
            "option_id": "opt_local_dashboard",
            "title": "Eigen lokale monitoringsset opstellen",
            "type": "afgeleide optie",
            "summary": "Ontwikkel een eigen lokale set van indicatoren en bestuurlijke momenten voor Almere.",
        },
        {
            "option_id": "opt_regional_alignment",
            "title": "Primair aansluiten op Flevoland",
            "type": "afgeleide optie",
            "summary": "Laat de lokale monitoringsaanpak primair aansluiten op de regionale Flevolandse aanpak.",
        },
        {
            "option_id": "opt_hybrid_model",
            "title": "Hybride model met lokale en regionale component",
            "type": "afgeleide optie",
            "summary": "Combineer lokale bestuurlijke indicatoren met regionale en landelijke comparabiliteit.",
        },
    ]


def option_comparison(options: list[dict], status: str) -> list[dict]:
    comparison: list[dict] = []
    for option in options:
        if "local" in option["option_id"] or "expliciet" in option["title"].lower():
            bestuurlijke_duidelijkheid = "hoger"
            afhankelijkheid = "lager"
        elif "regional" in option["option_id"] or "regio" in option["title"].lower():
            bestuurlijke_duidelijkheid = "middel"
            afhankelijkheid = "hoger"
        else:
            bestuurlijke_duidelijkheid = "middel"
            afhankelijkheid = "middel"
        comparison.append(
            {
                "option_id": option["option_id"],
                "bestuurlijke_duidelijkheid": bestuurlijke_duidelijkheid,
                "afhankelijkheid_van_anderen": afhankelijkheid,
                "huidige_statuscontext": DECISION_STATUS_LABELS[status],
            }
        )
    return comparison


def proposed_sequence(action_id: str) -> list[str]:
    sequences = {
        "act_d5_werkagenda_expliciteren": [
            "Bundel bestaande landelijke, regionale en lokale D5-aanknopingspunten in een overzicht.",
            "Maak zichtbaar voor welke doelgroepen Almere expliciet wil prioriteren.",
            "Verwerk de gekozen richting in een bestuurlijk of beleidsmatig document dat openbaar navolgbaar is.",
        ],
        "act_d6_lokale_structuur_verduidelijken": [
            "Breng in kaart welke lokale teams, wijkverbanden en regielijnen nu in Almere zichtbaar zijn.",
            "Toets waar terminologie en beleidsdefinitie nog niet samenvallen.",
            "Leg bestuurlijk vast welke lokale structuur als uitvoeringsbasis voor D6 geldt.",
        ],
        "act_middelen_en_eigenaarschap_vastleggen": [
            "Werk uit welke landelijke en regionale middelen voor Almere relevant zijn.",
            "Maak expliciet wie bestuurlijk eigenaar is van verdeling, verantwoording en aansluiting op doelen.",
            "Verwerk de financiele richting in een navolgbare lokale uitwerkingsstap.",
        ],
        "act_monitoring_afstemmen": [
            "Bepaal welke lokale indicatoren bestuurlijk relevant zijn voor Almere.",
            "Koppel die indicatoren aan het Flevolandse monitoringsspoor en landelijke evaluatiemomenten.",
            "Leg ritme, verantwoordingsmomenten en dashboardlogica bestuurlijk vast.",
        ],
        "act_regionale_digitale_aansluiting": [
            "Maak zichtbaar welke regionale digitale bouwstenen nu al worden ontwikkeld.",
            "Bepaal welke lokale aansluiting Almere nodig heeft voor gegevensuitwisseling en operationele sturing.",
            "Verwerk die aansluiting in een bestuurlijk navolgbare uitvoeringslijn.",
        ],
    }
    return sequences[action_id]


def current_working_direction(blueprint: dict, document_refs: list[dict]) -> str:
    if blueprint["decision_id"] == "dec_d5_prioritering":
        return (
            f"In de huidige bronbasis zijn al lokale aanknopingspunten zichtbaar in {join_titles(document_refs)}, "
            "maar een expliciete Almeerse prioritering van D5 naar doelgroep en interventiekeuze is nog niet zichtbaar."
        )
    if blueprint["decision_id"] == "dec_d6_regiemodel":
        return (
            f"De huidige bronbasis bevat verwijzingen naar lokale teams en regie in {join_titles(document_refs)}, "
            "maar nog geen expliciete bestuurlijke afbakening van wat in Almere precies als D6-structuur geldt."
        )
    if blueprint["decision_id"] == "dec_budget_verdeling":
        return (
            f"De bronbasis laat mogelijke middelen- en uitvoeringssporen zien in {join_titles(document_refs)}, "
            "maar nog geen expliciete Almeerse keuze voor verdeling en eigenaarschap."
        )
    return (
        f"In {join_titles(document_refs)} zijn aanknopingspunten voor monitoring en leren zichtbaar, "
        "maar nog geen expliciete bestuurlijke keuze voor één Almeers monitoringsarrangement."
    )


def why_decision_required(blueprint: dict, gap_entries: list[dict], dependency_entries: list[dict]) -> str:
    gap_part = (
        GAP_LABELS[gap_entries[0]["gap_id"]]["summary"]
        if gap_entries
        else "De lokale uitwerking is nog niet expliciet zichtbaar."
    )
    if blueprint["status"] == "blocked" and dependency_entries:
        dependency_part = DEPENDENCY_LABELS[dependency_entries[0]["dependency_id"]]["summary"]
        return f"{gap_part} Daarnaast is dit punt mede afhankelijk van: {dependency_part}"
    return gap_part


def next_formal_step_for_decision(status: str) -> str:
    if status == "blocked":
        return "Eerst verduidelijken welke landelijke of regionale afhankelijkheid bepalend is, daarna lokale keuze expliciteren."
    if status == "awaiting_clarification":
        return "Eerst bestuurlijke begripsduiding en rolafbakening expliciteren."
    if status == "partly_resolved":
        return "Bepalen of en hoe de huidige lijn expliciet in lokale openbare stukken wordt vastgelegd."
    return "Bepalen of een bestuurlijke opdracht of expliciete lokale uitwerking nodig is."


def next_milestone(decision_id: str) -> str:
    milestones = {
        "dec_d5_prioritering": "Lokale of regionale werkagenda expliciet gekoppeld aan D5.",
        "dec_d6_regiemodel": "Bestuurlijke afbakening van lokale teams, wijkverbanden en regie.",
        "dec_budget_verdeling": "Navolgbare keuze over middelenverdeling en eigenaarschap.",
        "dec_monitoring_arrangement": "Expliciete monitoringsset en bestuurlijk ritme voor Almere.",
    }
    return milestones[decision_id]


def consequences_for_action(action: dict, dependency_entries: list[dict]) -> str:
    if dependency_entries:
        dependency_part = DEPENDENCY_LABELS[dependency_entries[0]["dependency_id"]]["summary"]
        return f"{action['consequence']} Daarbij blijft de afhankelijkheid bestaan van: {dependency_part}"
    return action["consequence"]


def owner_label(action: dict) -> str:
    if action["action_id"] in {"act_d5_werkagenda_expliciteren", "act_d6_lokale_structuur_verduidelijken"}:
        return "Nog niet expliciet benoemd in de bronbasis; gemeentelijke regie ligt voor de hand."
    if action["action_id"] == "act_regionale_digitale_aansluiting":
        return "Nog niet expliciet benoemd in de bronbasis; regionale en gemeentelijke afstemming lijkt nodig."
    return "Nog niet expliciet benoemd in de bronbasis; bestuurlijk en ambtelijk eigenaarschap moet nog worden verduidelijkt."


def milestone_for_action(action_id: str) -> str:
    mapping = {
        "act_d5_werkagenda_expliciteren": "Expliciete lokale D5-vertaling in openbare stukken.",
        "act_d6_lokale_structuur_verduidelijken": "Expliciet lokaal D6-structuur- en regiebeeld.",
        "act_middelen_en_eigenaarschap_vastleggen": "Navolgbare koppeling tussen middelen, eigenaarschap en inzet.",
        "act_monitoring_afstemmen": "Afgestemde lokale monitoringsstructuur.",
        "act_regionale_digitale_aansluiting": "Concreet aansluitbeeld tussen Almere en Flevolandse digitale infrastructuur.",
    }
    return mapping[action_id]


def build_decision_models(
    almere_view: dict,
    claims: dict[str, dict],
    documents: dict[str, dict],
    themes: list[dict],
) -> list[dict]:
    choices = choice_map(almere_view)
    gaps = gap_map(almere_view)
    dependencies = dependency_map(almere_view)
    uncertainty_by_topic = uncertain_map(almere_view)
    conflict_by_topic = conflict_map(almere_view)

    models: list[dict] = []
    for blueprint in DECISION_BLUEPRINTS:
        choice = choices[blueprint["choice_id"]]
        gap_entries = [gaps[gap_id] for gap_id in blueprint["gap_ids"] if gap_id in gaps]
        dependency_entries = [dependencies[dep_id] for dep_id in blueprint["dependency_ids"] if dep_id in dependencies]
        claim_ids = [
            claim_id
            for claim_id in dedupe(
                choice["supporting_claim_ids"]
                + [claim_id for gap in gap_entries for claim_id in gap["supporting_claim_ids"]]
                + [claim_id for dependency in dependency_entries for claim_id in dependency["supporting_claim_ids"]]
            )
            if claim_id in claims
        ]
        document_refs = document_refs_from_claim_ids(claim_ids, claims, documents)
        topics = dedupe(choice["based_on_topics"] + [topic for gap in gap_entries for topic in gap["based_on_topics"]])
        linked_theme_ids = dedupe(blueprint["theme_ids"] + theme_ids_for_topics(topics, themes))
        options = option_set(blueprint["decision_id"])
        all_supporting_evidence = evidence_entries(claim_ids, claims, documents, limit=max(len(claim_ids), 12))
        supporting_evidence = all_supporting_evidence[:6]
        review_note = review_note_for_topics(topics, uncertainty_by_topic, conflict_by_topic)
        review_details = review_details_for_topics(topics, all_supporting_evidence, uncertainty_by_topic, conflict_by_topic)
        perspective_ids = perspective_ids_for_context(
            topic_ids=topics,
            theme_ids=linked_theme_ids,
            page_type="decision",
        )

        model = {
            "decision_id": blueprint["decision_id"],
            "slug": slugify(blueprint["title"]),
            "page_url": f"/decisions/{slugify(blueprint['title'])}/",
            "title": blueprint["title"],
            "status": DECISION_STATUS_LABELS[blueprint["status"]],
            "status_group": status_group_for_decision(blueprint["status"]),
            "as_of_date": almere_view["as_of_date"],
            "responsible_level": "gemeentelijk / bestuurlijke afweging",
            "linked_domain": blueprint["linked_domain"],
            "linked_domain_label": linked_domain_label(blueprint["linked_domain"]),
            "linked_theme_ids": linked_theme_ids,
            "decision_question": blueprint["decision_question"],
            "why_decision_required": why_decision_required(blueprint, gap_entries, dependency_entries),
            "current_working_direction": current_working_direction(blueprint, document_refs),
            "why_it_matters_for_leadership": blueprint["matter"],
            "policy_basis": document_refs[:6],
            "current_situation_almere": {
                "summary": GAP_LABELS[blueprint["gap_ids"][0]]["summary"] if blueprint["gap_ids"] else "Geen lokale samenvatting beschikbaar.",
                "supporting_documents": [ref["title"] for ref in document_refs if ref["jurisdiction_level"] == "municipal"][:4],
            },
            "options": options,
            "option_comparison": option_comparison(options, blueprint["status"]),
            "consequences_of_non_decision": blueprint["non_decision"],
            "dependencies": [
                {
                    "dependency_id": dep_id,
                    "title": DEPENDENCY_LABELS[dep_id]["title"],
                    "summary": DEPENDENCY_LABELS[dep_id]["summary"],
                }
                for dep_id in blueprint["dependency_ids"]
            ],
            "next_formal_step": next_formal_step_for_decision(blueprint["status"]),
            "next_milestone": next_milestone(blueprint["decision_id"]),
            "supporting_evidence": supporting_evidence,
            "supporting_claim_ids": claim_ids,
            "review_note": review_note,
            "review_details": review_details,
            "scope_note": "Dit is een machine-gegenereerde mogelijke besluitvraag op basis van de huidige openbare bronbasis; geen vastgestelde gemeentelijke beslissing.",
            "content_classification": quality_classification_ref("human_choice_question"),
            "perspective_ids": perspective_ids,
            "quality_perspectives": quality_perspective_refs(perspective_ids),
        }
        models.append(model)

    return models


def build_action_models(
    almere_view: dict,
    claims: dict[str, dict],
    documents: dict[str, dict],
    decision_models: list[dict],
) -> list[dict]:
    gaps = gap_map(almere_view)
    dependencies = dependency_map(almere_view)
    decision_map = {item["decision_id"]: item for item in decision_models}

    models: list[dict] = []
    for blueprint in ACTION_BLUEPRINTS:
        if blueprint["kind"] == "gap":
            source_item = gaps.get(blueprint["source_id"])
            if source_item is None:
                continue
            source_claim_ids = list(source_item["supporting_claim_ids"])
            current_status_detail = GAP_LABELS[blueprint["source_id"]]["summary"]
        else:
            source_item = dependencies.get(blueprint["source_id"])
            if source_item is None:
                continue
            source_claim_ids = list(source_item["supporting_claim_ids"])
            current_status_detail = DEPENDENCY_LABELS[blueprint["source_id"]]["summary"]

        dependency_entries = [dependencies[dep_id] for dep_id in blueprint["dependency_ids"] if dep_id in dependencies]
        claim_ids = [
            claim_id
            for claim_id in dedupe(
                source_claim_ids
                + [claim_id for dependency in dependency_entries for claim_id in dependency["supporting_claim_ids"]]
            )
            if claim_id in claims
        ]
        topics = topics_for_claim_ids(claim_ids, claims)
        perspective_ids = perspective_ids_for_context(
            topic_ids=topics,
            theme_ids=blueprint["theme_ids"],
            page_type="action",
        )
        model = {
            "action_id": blueprint["action_id"],
            "slug": slugify(blueprint["title"]),
            "page_url": f"/actions/{slugify(blueprint['title'])}/",
            "title": blueprint["title"],
            "status": ACTION_STATUS_LABELS[blueprint["status"]],
            "status_group": status_group_for_action(blueprint["status"]),
            "as_of_date": almere_view["as_of_date"],
            "owner": owner_label(blueprint),
            "linked_domain": blueprint["linked_domain"],
            "linked_domain_label": linked_domain_label(blueprint["linked_domain"]),
            "linked_decision_ids": blueprint["linked_decision_ids"],
            "linked_decision_titles": [decision_map[decision_id]["title"] for decision_id in blueprint["linked_decision_ids"]],
            "linked_theme_ids": blueprint["theme_ids"],
            "action_statement": blueprint["action_statement"],
            "why_leadership_action_required": current_status_detail,
            "intended_outcome": blueprint["intended_outcome"],
            "current_status_detail": current_status_detail,
            "participants": [
                "Gemeente Almere",
                "Regionale partners in Flevoland" if any(dep["dependency_id"] == "dep_regional_role_allocation" for dep in dependency_entries) else "Regionale of landelijke partners waar relevant",
            ],
            "dependencies": [
                {
                    "dependency_id": dep["dependency_id"],
                    "title": DEPENDENCY_LABELS[dep["dependency_id"]]["title"],
                    "summary": DEPENDENCY_LABELS[dep["dependency_id"]]["summary"],
                }
                for dep in dependency_entries
            ],
            "proposed_sequence": proposed_sequence(blueprint["action_id"]),
            "expected_deliverable": milestone_for_action(blueprint["action_id"]),
            "timing_and_milestones": [
                {
                    "label": "eerstvolgende bestuurlijk relevante stap",
                    "value": milestone_for_action(blueprint["action_id"]),
                }
            ],
            "next_milestone": milestone_for_action(blueprint["action_id"]),
            "consequences_if_not_followed_up": consequences_for_action(blueprint, dependency_entries),
            "supporting_evidence": evidence_entries(claim_ids, claims, documents),
            "supporting_claim_ids": claim_ids,
            "scope_note": "Dit is een machine-gegenereerde mogelijke opvolgactie op basis van de huidige openbare bronbasis; geen vastgestelde gemeentelijke opdracht.",
            "content_classification": quality_classification_ref("human_choice_question"),
            "perspective_ids": perspective_ids,
            "quality_perspectives": quality_perspective_refs(perspective_ids),
        }
        models.append(model)
    return models


def build_featured_themes(decisions: list[dict], actions: list[dict], themes: list[dict]) -> list[dict]:
    counter: Counter[str] = Counter()
    for model in decisions + actions:
        counter.update(model["linked_theme_ids"])
    theme_map = theme_lookup(themes)
    featured: list[dict] = []
    for theme_id, count in counter.most_common(4):
        theme = theme_map[theme_id]
        linked_decision_count = sum(1 for item in decisions if theme_id in item["linked_theme_ids"])
        linked_action_count = sum(1 for item in actions if theme_id in item["linked_theme_ids"])
        featured.append(
            {
                "theme_id": theme_id,
                "title": theme["title"],
                "summary": theme["summary"],
                "linked_decision_count": linked_decision_count,
                "linked_action_count": linked_action_count,
                "page_url": theme_page_url(theme_id),
                "decision_page_url": f"/decisions/?theme={theme_id}",
                "action_page_url": f"/actions/?theme={theme_id}",
            }
        )
    return featured


def build_recent_changes(document_payloads: dict[str, dict], documents: dict[str, dict]) -> list[dict]:
    entries: list[dict] = []
    for document_id, metadata in documents.items():
        publication_date = metadata["publication_date"]
        if not publication_date:
            continue
        payload = document_payloads.get(document_id)
        summary = None
        if payload:
            summary_entry = payload.get("document_level_summary", {}).get("implementation_relevance_for_municipality")
            if summary_entry:
                summary = summary_entry["statement"]
        entries.append(
            {
                "document_id": document_id,
                "title": metadata["title"],
                "publication_date": publication_date,
                "document_type": metadata["document_type"],
                "summary": summary or "Toegevoegd of bijgewerkt in de huidige bronbasis.",
                "page_url": source_page_url(metadata),
                "source_url": metadata["source_url"],
            }
        )
    entries.sort(key=lambda item: (item["publication_date"], item["title"]), reverse=True)
    return entries[:5]


def format_metric_delta(before: int, after: int) -> str:
    delta = after - before
    if delta > 0:
        return f"+{delta}"
    if delta < 0:
        return str(delta)
    return "0"


def build_site_updates_view(documents: dict[str, dict], timeline_register: dict, claims: dict[str, dict]) -> dict:
    update_specs = site_updates_config().get("updates", [])
    timeline_lookup = {
        entry["entry_key"]: entry
        for entry in timeline_register["entries"]
        if entry.get("entry_key")
    }

    updates: list[dict] = []
    ordered_specs = [
        spec
        for _, spec in sorted(
            enumerate(update_specs),
            key=lambda item: (item[1]["published_on"], -item[0]),
            reverse=True,
        )
    ]
    for spec in ordered_specs:
        update_page_url = f"/updates/#{spec['update_id']}"
        claims_page_url = f"/updates/claims/{spec['update_id']}/"
        section_urls = {
            "samenvatting": f"/updates/#{spec['update_id']}-samenvatting",
            "wijzigingen": f"/updates/#{spec['update_id']}-wijzigingen",
            "claims": claims_page_url,
            "tijdlijn": f"/updates/#{spec['update_id']}-tijdlijn",
            "bronnen": f"/updates/#{spec['update_id']}-bronnen",
        }
        metrics = []
        for item in spec.get("metrics", []):
            label = item["label"].lower()
            if "bronnen" in label:
                metric_page_url = section_urls["bronnen"]
            elif label == "claims":
                metric_page_url = section_urls["claims"]
            else:
                metric_page_url = section_urls["tijdlijn"]
            metrics.append(
                {
                    "label": item["label"],
                    "before": item["before"],
                    "after": item["after"],
                    "delta": item["after"] - item["before"],
                    "delta_label": format_metric_delta(item["before"], item["after"]),
                    "page_url": metric_page_url,
                }
            )

        affected_sources = []
        for document_id in spec.get("affected_document_ids", []):
            document = documents.get(document_id)
            if document is None:
                continue
            affected_sources.append(
                {
                    "document_id": document_id,
                    "title": document["title"],
                    "publisher": document["publisher"],
                    "publication_date": document["publication_date"],
                    "page_url": source_page_url(document),
                }
            )

        affected_claims_by_source = []
        for document_id in spec.get("affected_document_ids", []):
            document = documents.get(document_id)
            if document is None:
                continue
            source_claims = [
                claim for claim in claims.values() if claim["source_document_id"] == document_id
            ]
            source_claims.sort(key=lambda claim: (claim.get("topic", ""), claim.get("claim_id", "")))
            affected_claims_by_source.append(
                {
                    "document_id": document_id,
                    "title": document["title"],
                    "publisher": document["publisher"],
                    "publication_date": document["publication_date"],
                    "page_url": source_page_url(document),
                    "claim_count": len(source_claims),
                    "claims": [
                        {
                            "claim_id": claim["claim_id"],
                            "topic": claim["topic"],
                            "topic_label": topic_label(claim["topic"]),
                            "statement": claim["statement"],
                            "validity_status": claim.get("validity_status", ""),
                            "normative_status": claim.get("normative_status"),
                            "time_status": claim.get("time_status"),
                            "money_status": claim.get("money_status"),
                            "governance_status": claim.get("governance_status"),
                            "locality_status": claim.get("locality_status"),
                            "page_labels": [
                                str(page)
                                for page in claim.get("source_location", {}).get("pages", [])
                                if page is not None
                            ],
                            "section_labels": [
                                section
                                for section in claim.get("source_location", {}).get("sections", [])
                                if section
                            ],
                        }
                        for claim in source_claims
                    ],
                }
            )

        highlighted_timeline_entries = []
        for entry_key in spec.get("highlighted_timeline_entry_keys", []):
            entry = timeline_lookup.get(entry_key)
            if entry is None:
                continue
            highlighted_timeline_entries.append(
                {
                    "entry_key": entry["entry_key"],
                    "date_label": entry["date_label"],
                    "title": entry["title"],
                    "summary": entry["summary"],
                    "page_url": entry["page_url"],
                }
            )

        source_reference = None
        if spec.get("source_reference"):
            source_reference = timeline_source_ref(
                {
                    **spec["source_reference"],
                    "title": spec["source_reference"].get("title", spec["source_reference"].get("label", "")),
                }
            )

        updates.append(
            {
                "update_id": spec["update_id"],
                "page_url": update_page_url,
                "claims_page_url": claims_page_url,
                "published_on": spec["published_on"],
                "title": spec["title"],
                "summary": spec["summary"],
                "source_reference": source_reference,
                "human_summary": spec.get("human_summary", {}),
                "key_points": spec.get("key_points", []),
                "section_urls": section_urls,
                "change_highlights": spec.get("change_highlights", []),
                "metrics": metrics,
                "affected_pages": spec.get("affected_pages", []),
                "affected_sources": affected_sources,
                "affected_claims_by_source": affected_claims_by_source,
                "affected_claim_count": sum(item["claim_count"] for item in affected_claims_by_source),
                "highlighted_timeline_entries": highlighted_timeline_entries,
            }
        )

    return {
        "view_run_id": SITE_RUN_ID,
        "generated_on": TODAY,
        "as_of_date": TODAY,
        "title": "Updates",
        "updates": updates,
        "latest_update": updates[0] if updates else None,
    }


def build_timeline_register(
    documents: dict[str, dict],
    claims: dict[str, dict],
    current_topics: list[dict],
    decision_models: list[dict],
    action_models: list[dict],
) -> dict:
    current_topic_map = current_topic_lookup(current_topics)
    curation = timeline_curation()
    entries = [
        document_timeline_entry_from_spec(spec, documents)
        for spec in curation["document_entries"]
    ]
    entries.extend(
        reference_timeline_entry_from_spec(spec, claims, documents, current_topic_map, decision_models, action_models)
        for spec in curation["claim_entries"]
    )
    entries.extend(
        external_timeline_entry_from_spec(spec, decision_models, action_models)
        for spec in curation.get("supplemental_entries", [])
    )
    entries.sort(key=lambda item: (item["sort_key"], item["title"]))

    year_counts: dict[str, dict[str, int]] = defaultdict(lambda: {"entries": 0, "future": 0, "documents": 0})
    for entry in entries:
        year_counts[entry["year"]]["entries"] += 1
        if entry["entry_type"] == "bronmoment":
            year_counts[entry["year"]]["documents"] += 1
        if timeline_counts_as_future(entry):
            year_counts[entry["year"]]["future"] += 1

    years = [
        {
            "year": year,
            "entry_count": year_counts[year]["entries"],
            "future_count": year_counts[year]["future"],
            "document_count": year_counts[year]["documents"],
            "page_url": f"/timeline/#jaar-{year}",
        }
        for year in sorted(year_counts.keys())
    ]

    return {
        "register_run_id": SITE_RUN_ID,
        "generated_on": TODAY,
        "as_of_date": TODAY,
        "default_open_year": TODAY[:4],
        "entries": entries,
        "years": years,
    }


def build_timeline_view(timeline_register: dict) -> dict:
    grouped_entries: dict[str, list[dict]] = defaultdict(list)
    for entry in timeline_register["entries"]:
        grouped_entries[entry["year"]].append(entry)

    year_groups = []
    for year in ordered_timeline_years(list(grouped_entries.keys()), timeline_register["default_open_year"]):
        entries = ordered_timeline_entries(grouped_entries[year], timeline_register["as_of_date"])
        year_groups.append(
            {
                "year": year,
                "anchor_id": f"jaar-{year}",
                "default_open": year == timeline_register["default_open_year"],
                "entry_count": len(entries),
                "future_count": sum(1 for entry in entries if timeline_counts_as_future(entry)),
                "document_count": sum(1 for entry in entries if entry["entry_type"] == "bronmoment"),
                "entries": entries,
            }
        )

    return {
        "view_run_id": SITE_RUN_ID,
        "generated_on": timeline_register["generated_on"],
        "as_of_date": timeline_register["as_of_date"],
        "title": "Tijdlijn",
        "default_open_year": timeline_register["default_open_year"],
        "year_summaries": timeline_register["years"],
        "year_groups": year_groups,
        "entries": timeline_register["entries"],
    }


def build_home_view(
    almere_view: dict,
    decision_models: list[dict],
    action_models: list[dict],
    themes: list[dict],
    review_queue: dict,
    document_payloads: dict[str, dict],
    documents: dict[str, dict],
    timeline_register: dict,
    site_updates_view: dict,
) -> dict:
    implementation_status_blocks = [
        {
            "title": "Landelijke basis zichtbaar",
            "metric": len([item for item in almere_view["applicable_d5_items"] + almere_view["applicable_d6_items"] if item["scope"] in {"national", "mixed"}]),
            "summary": "De landelijke basis voor D5 en D6 is in de bronbasis herkenbaar aanwezig.",
            "page_url": "/almere/#landelijke-basis-zichtbaar",
        },
        {
            "title": "Lokale aanknopingspunten zichtbaar",
            "metric": len(almere_view["relevant_municipal_documents"]),
            "summary": "Er zijn lokale Almere-documenten zichtbaar, maar niet alle landelijke verwachtingen zijn daarin expliciet overgenomen.",
            "page_url": "/almere/#wat-al-in-beeld-is",
        },
        {
            "title": "Open uitwerkingsvragen",
            "metric": len(almere_view["local_gaps"]),
            "summary": "De huidige bronbasis laat meerdere punten zien waar lokale explicitering of bestuurlijke keuze nog niet zichtbaar is.",
            "page_url": "/almere/#lokale-hiaten",
        },
        {
            "title": "Menselijke duiding nodig",
            "metric": review_queue["summary"]["review"],
            "summary": "Een deel van de bronbasis vraagt nog om menselijke duiding over autoriteit, lokale overname of begripsafbakening.",
            "page_url": "/almere/#menselijke-duiding",
        },
    ]

    key_risks = [
        {
            "title": "Lokale overname nog niet expliciet zichtbaar",
            "summary": "Voor meerdere nationale of regionale doelen is in de huidige openbare Almere-documenten nog niet expliciet zichtbaar hoe lokale overname plaatsvindt.",
            "linked_domain": "D5 en D6",
            "page_url": "/almere/#lokale-hiaten",
        },
        {
            "title": "Begripsduiding rond lokale teams",
            "summary": "De term lokale teams wordt in verschillende contexten gebruikt; menselijke duiding blijft nodig om beleidsdefinitie en publieke formulering te scheiden.",
            "linked_domain": "D6",
            "page_url": "/almere/#review-unresolved-conflict",
        },
        {
            "title": "Bekostigingsroute en lokale verdeling nog niet volledig uitgewerkt",
            "summary": "Landelijke en regionale financieringssporen zijn zichtbaar, maar de lokale verdeling en het eigenaarschap zijn nog niet expliciet vastgelegd.",
            "linked_domain": "D5 en D6",
            "page_url": "/actions/",
        },
    ]

    executive_summary = (
        f"De huidige bronbasis laat voor Almere {len(decision_models)} mogelijke besluitvragen en "
        f"{len(action_models)} mogelijke opvolgacties zien. De meeste open punten zitten in lokale "
        "concretisering van D5 en D6, regie en governance, financiering en monitoring. "
        "De landelijke basis is zichtbaar, maar een deel van de lokale doorvertaling is in openbare Almere-documenten nog niet expliciet."
    )
    past_entries = [entry for entry in timeline_register["entries"] if entry["sort_key"] < TODAY]
    future_entries = [entry for entry in timeline_register["entries"] if entry["sort_key"] >= TODAY]
    near_term_timeline = past_entries[-2:] + future_entries[:4]

    return {
        "view_run_id": SITE_RUN_ID,
        "generated_on": TODAY,
        "as_of_date": almere_view["as_of_date"],
        "title": "Start",
        "executive_summary": executive_summary,
        "latest_update": site_updates_view.get("latest_update"),
        "top_decisions": decision_models[:3],
        "top_actions": action_models[:3],
        "implementation_status_blocks": implementation_status_blocks,
        "key_risks": key_risks,
        "key_dependencies": [
            {
                "dependency_id": item["dependency_id"],
                "title": DEPENDENCY_LABELS[item["dependency_id"]]["title"],
                "summary": DEPENDENCY_LABELS[item["dependency_id"]]["summary"],
                "linked_domain": "D5 en D6",
                "page_url": "/almere/#externe-afhankelijkheden",
            }
            for item in almere_view["local_dependencies"][:3]
        ],
        "near_term_timeline": near_term_timeline,
        "featured_themes": build_featured_themes(decision_models, action_models, themes),
        "recent_changes": build_recent_changes(document_payloads, documents),
        "supporting_navigation": [item for item in navigation_items() if item["priority"] == "secondary"],
    }


def build_expected_responsibilities(almere_view: dict) -> list[dict]:
    responsibilities: list[dict] = []
    for item in almere_view["applicable_d5_items"] + almere_view["applicable_d6_items"]:
        if item["scope"] not in {"national", "mixed"}:
            continue
        source_titles = [document["title"] for document in item["source_documents"][:3]]
        if item["scope"] == "national":
            summary = f"Landelijke basis zichtbaar via {join_titles([{'title': title} for title in source_titles])}."
        else:
            summary = (
                f"Landelijke basis zichtbaar, met aanvullende regionale of lokale uitwerking via "
                f"{join_titles([{'title': title} for title in source_titles])}."
            )
        responsibilities.append(
            {
                "topic": item["topic"],
                "title": topic_label(item["topic"]),
                "summary": summary,
                "scope_label": scope_label(item["scope"]),
                "needs_human_review": item["needs_human_review"],
            }
        )
    return responsibilities


def build_current_local_state(almere_view: dict) -> list[dict]:
    state: list[dict] = []
    for document in almere_view["relevant_municipal_documents"]:
        state.append(
            {
                "document_id": document["document_id"],
                "title": document["title"],
                "summary": f"In dit document zijn aanknopingspunten zichtbaar voor: {', '.join(topic_label(topic) for topic in document['relevant_topics'][:3])}.",
            }
        )
    return state


def build_review_items(review_queue: dict, documents: dict[str, dict]) -> tuple[list[dict], list[dict], list[dict]]:
    items: list[dict] = []
    reason_counts: Counter[str] = Counter()
    for review_item in review_queue["items"]:
        reason_code = review_item["reason_code"]
        reason_counts[reason_code] += 1

        document_id = review_item.get("document_id")
        document = documents.get(document_id) if document_id else None
        document_title = document["title"] if document else (document_id or "onbekende bron")
        publisher = document["publisher"] if document else "onbekende uitgever"
        topic = review_item.get("topic")
        reason_anchor = f"review-{reason_code.replace('_', '-')}"

        if reason_code == "authority_unclear":
            summary = f"{publisher} stelt dit in {document_title}; deze bron heeft lagere autoriteit en vraagt daarom expliciete bronduiding."
            recommended_action = "Gebruik dit voorlopig als context en benoem de bron expliciet, tenzij een sterkere bron dezelfde lijn bevestigt."
        elif reason_code == "municipality_relevance_inferred":
            summary = (
                f"In {document_title} is een landelijke of regionale lijn zichtbaar, maar in openbaar beschikbare "
                "Almere-documenten is nog niet expliciet vastgelegd dat Almere deze lijn lokaal heeft overgenomen."
            )
            recommended_action = "Beoordeel of Almere deze lijn bestuurlijk of beleidsmatig expliciet wil overnemen in openbare stukken."
        else:
            topic_part = topic_label(topic) if topic else "deze bronrelatie"
            summary = f"Voor {topic_part} is nog menselijke duiding nodig omdat begrippen, definities of lokale vertalingen in meerdere contexten worden gebruikt."
            recommended_action = "Maak expliciet welke beleidsdefinitie wordt bedoeld en hoe de landelijke basis zich verhoudt tot de lokale of regionale vertaling."

        items.append(
            {
                "review_item_id": review_item["review_item_id"],
                "reason_code": reason_code,
                "reason_anchor": reason_anchor,
                "reason_label": review_reason_label(reason_code),
                "document_id": document_id,
                "document_title": document_title,
                "topic": topic,
                "topic_label": topic_label(topic) if topic else None,
                "summary": summary,
                "recommended_action": recommended_action,
            }
        )

    reason_order = ["authority_unclear", "municipality_relevance_inferred", "unresolved_conflict"]
    reason_summary = [
        {
            "reason_code": reason_code,
            "reason_label": review_reason_label(reason_code),
            "metric": count,
            "summary": review_summary_for_reason(reason_code),
            "page_url": f"/almere/#review-{reason_code.replace('_', '-')}",
        }
        for reason_code in reason_order
        for count in [reason_counts.get(reason_code, 0)]
        if count
    ]
    reason_groups = [
        {
            "reason_code": reason["reason_code"],
            "reason_label": reason["reason_label"],
            "anchor_id": f"review-{reason['reason_code'].replace('_', '-')}",
            "summary": review_summary_for_reason(reason["reason_code"]),
            "items": [item for item in items if item["reason_code"] == reason["reason_code"]],
        }
        for reason in reason_summary
    ]
    return items, reason_summary, reason_groups


def build_almere_site_view(
    almere_view: dict,
    decision_models: list[dict],
    action_models: list[dict],
    review_queue: dict,
    claims: dict[str, dict],
    documents: dict[str, dict],
) -> dict:
    evidence_claim_ids = []
    for decision in decision_models[:3]:
        evidence_claim_ids.extend(decision["supporting_claim_ids"][:3])
    for action in action_models[:3]:
        evidence_claim_ids.extend(action["supporting_claim_ids"][:3])
    review_items, review_reason_summary, review_groups = build_review_items(review_queue, documents)

    return {
        "view_run_id": SITE_RUN_ID,
        "generated_on": TODAY,
        "as_of_date": almere_view["as_of_date"],
        "title": "Almere",
        "current_picture": (
            "De huidige bronbasis laat voor Almere een herkenbare landelijke basis voor D5 en D6 zien, "
            "maar de lokale vertaling is niet op alle punten expliciet zichtbaar in openbare gemeentelijke stukken."
        ),
        "expected_municipal_responsibilities": build_expected_responsibilities(almere_view),
        "current_local_state": build_current_local_state(almere_view),
        "local_gaps": [
            {
                "gap_id": gap["gap_id"],
                "title": GAP_LABELS[gap["gap_id"]]["title"],
                "summary": GAP_LABELS[gap["gap_id"]]["summary"],
            }
            for gap in almere_view["local_gaps"]
        ],
        "leadership_requirements": [decision["title"] for decision in decision_models] + [action["title"] for action in action_models[:2]],
        "current_decisions": decision_models,
        "current_actions": action_models,
        "review_reason_summary": review_reason_summary,
        "review_items": review_items,
        "review_groups": review_groups,
        "external_dependencies": [
            {
                "dependency_id": dependency["dependency_id"],
                "title": DEPENDENCY_LABELS[dependency["dependency_id"]]["title"],
                "summary": DEPENDENCY_LABELS[dependency["dependency_id"]]["summary"],
                "next_step": DEPENDENCY_LABELS[dependency["dependency_id"]]["next_step"],
            }
            for dependency in almere_view["local_dependencies"]
        ],
        "evidence_refs": evidence_entries(dedupe(evidence_claim_ids), claims, documents),
    }


def build_dashboard_view(
    almere_view: dict,
    decision_models: list[dict],
    action_models: list[dict],
) -> dict:
    rows: list[dict] = []
    for decision in decision_models:
        rows.append(
            {
                "issue_id": decision["decision_id"],
                "issue_type": "decision",
                "title": decision["title"],
                "linked_domain": decision["linked_domain_label"],
                "status": decision["status"],
                "owner": decision["responsible_level"],
                "next_milestone": decision["next_milestone"],
                "dependencies": ", ".join(dep["title"] for dep in decision["dependencies"]) or "geen expliciete afhankelijkheid",
                "consequences_of_non_follow_up": decision["consequences_of_non_decision"],
                "linked_theme_ids": decision["linked_theme_ids"],
                "linked_page_url": decision["page_url"],
            }
        )
    for action in action_models:
        rows.append(
            {
                "issue_id": action["action_id"],
                "issue_type": "action",
                "title": action["title"],
                "linked_domain": action["linked_domain_label"],
                "status": action["status"],
                "owner": action["owner"],
                "next_milestone": action["next_milestone"],
                "dependencies": ", ".join(dep["title"] for dep in action["dependencies"]) or "geen expliciete afhankelijkheid",
                "consequences_of_non_follow_up": action["consequences_if_not_followed_up"],
                "linked_theme_ids": action["linked_theme_ids"],
                "linked_page_url": action["page_url"],
            }
        )
    for dependency in almere_view["local_dependencies"]:
        rows.append(
            {
                "issue_id": dependency["dependency_id"],
                "issue_type": "dependency",
                "title": DEPENDENCY_LABELS[dependency["dependency_id"]]["title"],
                "linked_domain": "D5 en D6",
                "status": "externe afhankelijkheid",
                "owner": "extern / gedeeld",
                "next_milestone": DEPENDENCY_LABELS[dependency["dependency_id"]]["next_step"],
                "dependencies": "n.v.t.",
                "consequences_of_non_follow_up": DEPENDENCY_LABELS[dependency["dependency_id"]]["summary"],
                "linked_theme_ids": [],
                "linked_page_url": "/almere/#externe-afhankelijkheden",
            }
        )
    for conflict in almere_view["unresolved_conflicts"]:
        rows.append(
            {
                "issue_id": conflict["conflict_id"],
                "issue_type": "risk",
                "title": f"Menselijke duiding nodig: {topic_label(conflict['topic'])}",
                "linked_domain": "D5 en D6" if conflict["topic"].startswith(("d5.", "d6.")) else "governance en monitoring",
                "status": "wacht op duiding",
                "owner": "menselijke beoordeling nodig",
                "next_milestone": "Begripsduiding of bestuurlijke interpretatie expliciteren",
                "dependencies": conflict_resolution_label(conflict["recommended_resolution_rule"]),
                "consequences_of_non_follow_up": conflict_note(conflict),
                "linked_theme_ids": [],
                "linked_page_url": "/almere/#review-unresolved-conflict",
            }
        )

    return {
        "view_run_id": SITE_RUN_ID,
        "generated_on": TODAY,
        "as_of_date": almere_view["as_of_date"],
        "rows": rows,
    }


def build_theme_models(
    themes: list[dict],
    current_topics: list[dict],
    almere_view: dict,
    decision_models: list[dict],
    action_models: list[dict],
    claims: dict[str, dict],
    documents: dict[str, dict],
) -> list[dict]:
    theme_topics: defaultdict[str, list[dict]] = defaultdict(list)
    for topic_entry in current_topics:
        for theme_id in theme_ids_for_topics([topic_entry["topic"]], themes):
            theme_topics[theme_id].append(topic_entry)

    theme_models: list[dict] = []
    for theme in themes:
        theme_id = theme["theme_id"]
        linked_decisions = [decision for decision in decision_models if theme_id in decision["linked_theme_ids"]]
        linked_actions = [action for action in action_models if theme_id in action["linked_theme_ids"]]
        topic_entries = sorted(theme_topics.get(theme_id, []), key=lambda item: topic_label(item["topic"]))
        claim_ids = dedupe(
            [claim_id for entry in topic_entries for claim_id in entry["current_claim_ids"] + entry["historical_claim_ids"]]
        )
        source_basis = [
            {
                **ref,
                "page_url": source_page_url(documents[ref["document_id"]]),
            }
            for ref in document_refs_from_claim_ids(claim_ids, claims, documents)
        ]

        relevant_items = []
        for item in almere_view["applicable_d5_items"] + almere_view["applicable_d6_items"]:
            if theme_id not in theme_ids_for_topics([item["topic"]], themes):
                continue
            relevant_items.append(
                {
                    "topic": item["topic"],
                    "title": topic_label(item["topic"]),
                    "scope_label": scope_label(item["scope"]),
                    "needs_human_review": item["needs_human_review"],
                }
            )

        current_interpretation = [
            {
                "topic": entry["topic"],
                "title": topic_label(entry["topic"]),
                "status": status_label_for_topic(entry),
                "confidence_label": confidence_label(entry["confidence"]),
                "needs_human_review": entry["needs_human_review"],
                "page_url": topic_page_url(entry["topic"]),
            }
            for entry in topic_entries
        ]

        almere_implications = []
        for gap in almere_view["local_gaps"]:
            if theme_id in theme_ids_for_topics(gap["based_on_topics"], themes):
                almere_implications.append(
                    {
                        "title": GAP_LABELS[gap["gap_id"]]["title"],
                        "summary": GAP_LABELS[gap["gap_id"]]["summary"],
                        "page_url": "/almere/#lokale-hiaten",
                    }
                )
        for uncertain in almere_view["uncertain_items"]:
            if theme_id in theme_ids_for_topics([uncertain["topic"]], themes):
                almere_implications.append(
                    {
                        "title": f"Menselijke duiding bij {topic_label(uncertain['topic'])}",
                        "summary": "De huidige interpretatielaag markeert dit onderwerp voor extra menselijke duiding.",
                        "page_url": "/almere/#menselijke-duiding",
                    }
                )
        almere_implications = almere_implications[:6]

        dependencies = []
        seen_dependency_ids: set[str] = set()
        for model in linked_decisions + linked_actions:
            for dependency in model["dependencies"]:
                if dependency["dependency_id"] in seen_dependency_ids:
                    continue
                seen_dependency_ids.add(dependency["dependency_id"])
                dependencies.append(
                    {
                        "title": dependency["title"],
                        "summary": dependency["summary"],
                        "page_url": "/almere/#externe-afhankelijkheden",
                    }
                )

        related_reference_topics = [
            {
                "topic": entry["topic"],
                "title": topic_label(entry["topic"]),
                "status": status_label_for_topic(entry),
                "page_url": topic_page_url(entry["topic"]),
            }
            for entry in topic_entries
        ]
        theme_topic_ids = [entry["topic"] for entry in topic_entries]
        perspective_ids = perspective_ids_for_context(
            topic_ids=theme_topic_ids,
            theme_ids=[theme_id],
        )

        theme_models.append(
            {
                "theme_id": theme_id,
                "title": theme["title"],
                "summary": theme["summary"],
                "page_url": theme_page_url(theme_id),
                "linked_decision_count": len(linked_decisions),
                "linked_action_count": len(linked_actions),
                "linked_decisions": [
                    {"title": item["title"], "status": item["status"], "page_url": item["page_url"]}
                    for item in linked_decisions
                ],
                "linked_actions": [
                    {"title": item["title"], "status": item["status"], "page_url": item["page_url"]}
                    for item in linked_actions
                ],
                "relevant_d5_d6_items": relevant_items,
                "current_interpretation": current_interpretation,
                "almere_implications": almere_implications,
                "dependencies": dependencies,
                "source_basis": source_basis[:8],
                "related_reference_topics": related_reference_topics,
                "content_classification": quality_classification_ref("interpretation"),
                "perspective_ids": perspective_ids,
                "quality_perspectives": quality_perspective_refs(perspective_ids),
            }
        )

    return theme_models


def build_themes_view(theme_models: list[dict]) -> dict:
    return {
        "view_run_id": SITE_RUN_ID,
        "generated_on": TODAY,
        "as_of_date": TODAY,
        "title": "Thema's",
        "themes": theme_models,
    }


def build_reference_topic_models(
    current_topics: list[dict],
    themes: list[dict],
    decision_models: list[dict],
    action_models: list[dict],
    claims: dict[str, dict],
    documents: dict[str, dict],
) -> list[dict]:
    topic_models: list[dict] = []
    for entry in sorted(current_topics, key=lambda item: topic_label(item["topic"])):
        claim_ids = dedupe(entry["current_claim_ids"] + entry["historical_claim_ids"])
        linked_theme_ids = theme_ids_for_topics([entry["topic"]], themes)
        linked_decisions = [
            decision
            for decision in decision_models
            if set(decision["supporting_claim_ids"]) & set(claim_ids)
            or any(theme_id in decision["linked_theme_ids"] for theme_id in linked_theme_ids)
        ]
        linked_actions = [
            action
            for action in action_models
            if set(action["supporting_claim_ids"]) & set(claim_ids)
            or any(theme_id in action["linked_theme_ids"] for theme_id in linked_theme_ids)
        ]
        source_basis = [
            {
                **ref,
                "page_url": source_page_url(documents[ref["document_id"]]),
            }
            for ref in document_refs_from_claim_ids(claim_ids, claims, documents)
        ]
        related_topics = []
        for candidate in current_topics:
            if candidate["topic"] == entry["topic"]:
                continue
            if not set(theme_ids_for_topics([candidate["topic"]], themes)) & set(linked_theme_ids):
                continue
            related_topics.append(
                {
                    "topic": candidate["topic"],
                    "title": topic_label(candidate["topic"]),
                    "page_url": topic_page_url(candidate["topic"]),
                }
            )

        definition = (
            f"Voor {topic_label(entry['topic'])} zijn {len(entry['current_claim_ids'])} actuele claim(s) "
            f"en {len(entry['historical_claim_ids'])} historische claim(s) beschikbaar in de huidige referentielaag."
        )
        perspective_ids = perspective_ids_for_context(topic_ids=[entry["topic"]])
        topic_models.append(
            {
                "topic_id": entry["topic"],
                "slug": topic_slug(entry["topic"]),
                "page_url": topic_page_url(entry["topic"]),
                "title": topic_label(entry["topic"]),
                "definition": definition,
                "status": status_label_for_topic(entry),
                "linked_domain": domain_for_topic(entry["topic"]),
                "linked_theme_ids": linked_theme_ids,
                "linked_themes": [
                    {
                        "theme_id": theme_id,
                        "title": theme_lookup(themes)[theme_id]["title"],
                        "page_url": theme_page_url(theme_id),
                    }
                    for theme_id in linked_theme_ids
                ],
                "linked_decisions": [
                    {"title": item["title"], "status": item["status"], "page_url": item["page_url"]}
                    for item in linked_decisions[:6]
                ],
                "linked_actions": [
                    {"title": item["title"], "status": item["status"], "page_url": item["page_url"]}
                    for item in linked_actions[:6]
                ],
                "source_basis": source_basis[:8],
                "timeline_notes": [
                    {
                        "date_label": ref["publication_date"] or "datum onbekend",
                        "title": ref["title"],
                        "status": ref["status"],
                        "page_url": ref["page_url"],
                    }
                    for ref in source_basis[:6]
                ],
                "related_topics": related_topics[:6],
                "current_claim_count": len(entry["current_claim_ids"]),
                "historical_claim_count": len(entry["historical_claim_ids"]),
                "needs_human_review": entry["needs_human_review"],
                "confidence_label": confidence_label(entry["confidence"]),
                "content_classification": quality_classification_ref("interpretation"),
                "perspective_ids": perspective_ids,
                "quality_perspectives": quality_perspective_refs(perspective_ids),
            }
        )
    return topic_models


def build_reference_view(reference_topics: list[dict], source_models: list[dict]) -> dict:
    grouped_topics: defaultdict[str, list[dict]] = defaultdict(list)
    for topic in reference_topics:
        grouped_topics[topic["linked_domain"]].append(topic)

    publishers: Counter[str] = Counter(source["metadata"]["publisher"] for source in source_models)
    return {
        "view_run_id": SITE_RUN_ID,
        "generated_on": TODAY,
        "as_of_date": TODAY,
        "title": "Referentie",
        "topic_count": len(reference_topics),
        "domain_groups": {
            domain: topics
            for domain, topics in sorted(grouped_topics.items())
        },
        "publishers": [
            {"publisher": publisher, "document_count": count}
            for publisher, count in publishers.most_common(6)
        ],
        "featured_topics": reference_topics[:8],
    }


def source_summary(document: dict, payload: dict | None) -> str:
    if payload is None:
        return "Deze bron is opgenomen in de corpusinventaris, maar heeft nog geen nadere sitesamenvatting gekregen."
    scope = payload["extraction_scope"]
    if scope["contains_d5"] and scope["contains_d6"]:
        return "Deze bron bevat expliciete informatie over zowel D5 als D6 en wordt in de huidige site gebruikt voor bestuurlijke duiding en traceerbaarheid."
    if scope["contains_d5"]:
        return "Deze bron draagt vooral bij aan de D5-lijn en de vertaling daarvan naar uitvoering en bestuurlijke duiding."
    if scope["contains_d6"]:
        return "Deze bron draagt vooral bij aan de D6-lijn en de randvoorwaarden voor uitvoering."
    if scope["contains_municipal_implications"]:
        return "Deze bron bevat vooral context of lokale vertaling die relevant is voor Almere, zonder zelf de landelijke D5/D6-basistekst te zijn."
    return "Deze bron biedt aanvullende context binnen de huidige bronbasis."


def source_contribution(document: dict) -> str:
    if document["jurisdiction_level"] == "national" and document["status"] == "current":
        return "Deze bron draagt bij aan de actuele landelijke bestuurlijke lijn."
    if document["jurisdiction_level"] == "regional":
        return "Deze bron laat zien hoe landelijke lijnen regionaal in Flevoland worden vertaald."
    if document["jurisdiction_level"] == "municipal":
        return "Deze bron laat zien welke lokale vertaling of context in Almere openbaar zichtbaar is."
    return "Deze bron geeft aanvullende bestuurlijke context voor de huidige corpuslijn."


def relevance_note_for_section(section: dict, label: str) -> str:
    if section.get("explicit_reference_present"):
        return f"Bevat expliciete {label}-passages in de huidige extractie."
    items = section.get("items") or []
    if items:
        return f"Bevat vooral contextuele of afgeleide signalen die aan {label} raken."
    return f"Geen duidelijke {label}-passages in de huidige extractie."


def build_source_view_models(
    documents: dict[str, dict],
    document_payloads: dict[str, dict],
    claims: dict[str, dict],
    decision_models: list[dict],
    action_models: list[dict],
    themes: list[dict],
) -> list[dict]:
    claims_by_document: defaultdict[str, list[dict]] = defaultdict(list)
    for claim in claims.values():
        claims_by_document[claim["source_document_id"]].append(claim)

    source_models: list[dict] = []
    for document in sorted(documents.values(), key=lambda item: (item["publication_date"] or "", item["title"]), reverse=True):
        payload = document_payloads.get(document["document_id"])
        document_claims = claims_by_document.get(document["document_id"], [])
        claim_ids = [claim["claim_id"] for claim in document_claims]
        topic_counts = Counter(claim["topic"] for claim in document_claims)
        theme_ids = dedupe(
            theme_id
            for claim in document_claims
            for theme_id in theme_ids_for_topics([claim["topic"]], themes)
        )
        linked_decisions = [
            {"title": item["title"], "status": item["status"], "page_url": item["page_url"]}
            for item in decision_models
            if set(item["supporting_claim_ids"]) & set(claim_ids)
        ]
        linked_actions = [
            {"title": item["title"], "status": item["status"], "page_url": item["page_url"]}
            for item in action_models
            if set(item["supporting_claim_ids"]) & set(claim_ids)
        ]

        extraction_scope = payload["extraction_scope"] if payload else {}
        d5_section = (payload or {}).get("structured_content", {}).get("d5", {})
        d6_section = (payload or {}).get("structured_content", {}).get("d6", {})
        perspective_ids = perspective_ids_for_context(
            topic_ids=list(topic_counts.keys()),
            theme_ids=list(theme_ids),
            page_type="source",
            jurisdiction_level=document["jurisdiction_level"],
        )

        source_models.append(
            {
                "source_id": document["document_id"],
                "slug": slugify(document.get("short_title") or document["title"]),
                "page_url": source_page_url(document),
                "metadata": {
                    **document,
                    "document_type_label": document_type_label(document["document_type"]),
                    "source_classification_label": source_classification_label(document),
                },
                "summary": source_summary(document, payload),
                "what_changed_or_added": source_contribution(document),
                "d5_relevance": relevance_note_for_section(d5_section, "D5"),
                "d6_relevance": relevance_note_for_section(d6_section, "D6"),
                "linked_claims": [
                    {
                        "topic": topic,
                        "title": topic_label(topic),
                        "claim_count": count,
                        "page_url": topic_page_url(topic),
                    }
                    for topic, count in topic_counts.most_common(8)
                ],
                "linked_decisions": linked_decisions,
                "linked_actions": linked_actions,
                "linked_themes": [
                    {
                        "theme_id": theme_id,
                        "title": theme_lookup(themes)[theme_id]["title"],
                        "page_url": theme_page_url(theme_id),
                    }
                    for theme_id in theme_ids
                ],
                "related_sources": [],
                "structured_signals": {
                    "contains_structured_table": extraction_scope.get("contains_structured_table", False),
                    "d5_item_count": len(d5_section.get("items", [])),
                    "d6_item_count": len(d6_section.get("items", [])),
                    "governance_item_count": len((payload or {}).get("structured_content", {}).get("governance_and_finance", {}).get("items", [])),
                    "timeline_item_count": len((payload or {}).get("structured_content", {}).get("timeline_and_status", {}).get("items", [])),
                },
                "content_classification": quality_classification_ref("source_fact"),
                "perspective_ids": perspective_ids,
                "quality_perspectives": quality_perspective_refs(perspective_ids),
            }
        )

    theme_sets = {model["source_id"]: {item["theme_id"] for item in model["linked_themes"]} for model in source_models}
    for model in source_models:
        overlaps = []
        for candidate in source_models:
            if candidate["source_id"] == model["source_id"]:
                continue
            overlap_count = len(theme_sets[model["source_id"]] & theme_sets[candidate["source_id"]])
            if overlap_count == 0 and candidate["metadata"]["publisher"] != model["metadata"]["publisher"]:
                continue
            overlaps.append((overlap_count, candidate["metadata"]["publication_date"] or "", candidate))
        overlaps.sort(key=lambda item: (item[0], item[1], item[2]["metadata"]["title"]), reverse=True)
        model["related_sources"] = [
            {
                "title": candidate["metadata"]["title"],
                "page_url": candidate["page_url"],
            }
            for _, _, candidate in overlaps[:5]
        ]

    return source_models


def build_sources_view(source_models: list[dict]) -> dict:
    return {
        "view_run_id": SITE_RUN_ID,
        "generated_on": TODAY,
        "as_of_date": TODAY,
        "title": "Bronnen",
        "sources": source_models,
    }


def build_site_manifest(
    decisions: list[dict],
    actions: list[dict],
    themes: list[dict],
    reference_topics: list[dict],
    sources: list[dict],
    updates_view: dict,
) -> dict:
    pages = [
        {
            "page_type": "home",
            "title": "Start",
            "url": "/",
        },
        {
            "page_type": "almere",
            "title": "Almere",
            "url": "/almere/",
        },
        {
            "page_type": "decisions",
            "title": "Besluitvragen",
            "url": "/decisions/",
        },
        {
            "page_type": "actions",
            "title": "Opvolgacties",
            "url": "/actions/",
        },
        {
            "page_type": "dashboard",
            "title": "Dashboard",
            "url": "/dashboard/",
        },
        {
            "page_type": "timeline",
            "title": "Tijdlijn",
            "url": "/timeline/",
        },
        {
            "page_type": "updates",
            "title": "Updates",
            "url": "/updates/",
        },
        {
            "page_type": "themes",
            "title": "Thema's",
            "url": "/themes/",
        },
        {
            "page_type": "reference",
            "title": "Referentie",
            "url": "/reference/",
        },
        {
            "page_type": "reference_topics",
            "title": "Onderwerpen",
            "url": "/reference/topics/",
        },
        {
            "page_type": "sources",
            "title": "Bronnen",
            "url": "/sources/",
        },
    ]
    pages.extend(
        {
            "page_type": "decision_detail",
            "title": item["title"],
            "url": item["page_url"],
        }
        for item in decisions
    )
    pages.extend(
        {
            "page_type": "action_detail",
            "title": item["title"],
            "url": item["page_url"],
        }
        for item in actions
    )
    pages.extend(
        {
            "page_type": "theme_detail",
            "title": item["title"],
            "url": item["page_url"],
        }
        for item in themes
    )
    pages.extend(
        {
            "page_type": "reference_topic_detail",
            "title": item["title"],
            "url": item["page_url"],
        }
        for item in reference_topics
    )
    pages.extend(
        {
            "page_type": "source_detail",
            "title": item["metadata"]["title"],
            "url": item["page_url"],
        }
        for item in sources
    )
    pages.extend(
        {
            "page_type": "update_note",
            "title": item["title"],
            "url": item["page_url"],
        }
        for item in updates_view.get("updates", [])
    )
    pages.extend(
        {
            "page_type": "update_claims",
            "title": f'Claimlijst: {item["title"]}',
            "url": item["claims_page_url"],
        }
        for item in updates_view.get("updates", [])
    )
    return {
        "site_run_id": SITE_RUN_ID,
        "generated_on": TODAY,
        "pages": pages,
        "navigation": navigation_items(),
    }


def main() -> None:
    almere_view = load_json(ALMERE_VIEW_PATH)
    current_topics = current_interpretation_topics()
    review_queue = load_json(REVIEW_QUEUE_PATH)
    claims = claim_map()
    documents = document_map()
    document_payloads = document_payload_map()
    themes = theme_definitions()

    decision_models = build_decision_models(almere_view, claims, documents, themes)
    action_models = build_action_models(almere_view, claims, documents, decision_models)
    timeline_register = build_timeline_register(documents, claims, current_topics, decision_models, action_models)
    site_updates_view = build_site_updates_view(documents, timeline_register, claims)
    theme_models = build_theme_models(themes, current_topics, almere_view, decision_models, action_models, claims, documents)
    source_models = build_source_view_models(documents, document_payloads, claims, decision_models, action_models, themes)
    reference_topic_models = build_reference_topic_models(current_topics, themes, decision_models, action_models, claims, documents)
    home_view = build_home_view(
        almere_view,
        decision_models,
        action_models,
        themes,
        review_queue,
        document_payloads,
        documents,
        timeline_register,
        site_updates_view,
    )
    almere_site_view = build_almere_site_view(almere_view, decision_models, action_models, review_queue, claims, documents)
    dashboard_view = build_dashboard_view(almere_view, decision_models, action_models)
    timeline_view = build_timeline_view(timeline_register)
    themes_view = build_themes_view(theme_models)
    reference_view = build_reference_view(reference_topic_models, source_models)
    sources_view = build_sources_view(source_models)
    site_manifest = build_site_manifest(decision_models, action_models, theme_models, reference_topic_models, source_models, site_updates_view)

    write_json(HOME_VIEW_PATH, home_view)
    write_json(ALMERE_SITE_VIEW_PATH, almere_site_view)
    write_json(DASHBOARD_VIEW_PATH, dashboard_view)
    write_json(TIMELINE_REGISTER_PATH, timeline_register)
    write_json(TIMELINE_VIEW_PATH, timeline_view)
    write_json(THEMES_VIEW_PATH, themes_view)
    write_json(REFERENCE_VIEW_PATH, reference_view)
    write_json(SOURCES_VIEW_PATH, sources_view)
    write_json(SITE_UPDATES_VIEW_PATH, site_updates_view)
    write_json(SITE_MANIFEST_PATH, site_manifest)

    for generated_dir in [DECISION_DIR, ACTION_DIR, THEME_DIR, REFERENCE_TOPIC_DIR, SOURCE_VIEW_DIR]:
        clear_generated_json_dir(generated_dir)
    for model in decision_models:
        write_json(DECISION_DIR / f"{model['decision_id']}.json", model)
    for model in action_models:
        write_json(ACTION_DIR / f"{model['action_id']}.json", model)
    for model in theme_models:
        write_json(THEME_DIR / f"{model['theme_id']}.json", model)
    for model in reference_topic_models:
        write_json(REFERENCE_TOPIC_DIR / f"{model['slug']}.json", model)
    for model in source_models:
        write_json(SOURCE_VIEW_DIR / f"{model['slug']}.json", model)

    print(f"Wrote {HOME_VIEW_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"Wrote {ALMERE_SITE_VIEW_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"Wrote {DASHBOARD_VIEW_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"Wrote {TIMELINE_REGISTER_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"Wrote {TIMELINE_VIEW_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"Wrote {THEMES_VIEW_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"Wrote {REFERENCE_VIEW_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"Wrote {SOURCES_VIEW_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"Wrote {SITE_UPDATES_VIEW_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"Wrote {SITE_MANIFEST_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(
        f"Wrote {len(decision_models)} decision view models, {len(action_models)} action view models, "
        f"{len(theme_models)} theme view models, {len(reference_topic_models)} reference topic view models, "
        f"and {len(source_models)} source view models"
    )


if __name__ == "__main__":
    main()
