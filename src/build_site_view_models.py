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
MASTER_VIEW_PATH = CLAIMS_DIR / "d5_d6_master.json"
CURRENT_INTERPRETATION_PATH = CLAIMS_DIR / "current_interpretation.json"
CLAIMS_MASTER_PATH = CLAIMS_DIR / "claims_master.jsonl"
INVENTORY_PATH = EXTRACTED_DIR / "document_inventory.json"
REVIEW_QUEUE_PATH = EXTRACTED_DIR / "review_queue.json"
SITE_TAXONOMY_PATH = REPO_ROOT / "config" / "site_taxonomy.json"

DOCUMENTS_DIR = EXTRACTED_DIR / "documents"

HOME_VIEW_PATH = SITE_DIR / "site_home_view.json"
ALMERE_SITE_VIEW_PATH = SITE_DIR / "site_almere_view.json"
DASHBOARD_VIEW_PATH = SITE_DIR / "dashboard_view.json"
SITE_MANIFEST_PATH = SITE_DIR / "site_manifest.json"
DECISION_DIR = SITE_DIR / "decision_view_models"
ACTION_DIR = SITE_DIR / "action_view_models"

SITE_RUN_ID = "phase12_site_views_v1"
TODAY = date.today().isoformat()


TOPIC_LABELS = {
    "d5.definition": "D5-definitie",
    "d5.basisfunctionaliteiten_onderbouwd": "onderbouwde D5-basisfunctionaliteiten",
    "d5.regional_workagenda": "regionale/lokale D5-werkagenda",
    "d5.cross_domain_collaboration": "domeinoverstijgende samenwerking",
    "d5.mentale_gezondheidsnetwerken": "mentale gezondheidsnetwerken",
    "d5.health_first_shift": "verschuiving naar gezondheid en veerkracht",
    "d6.basisinfrastructuur": "D6-basisinfrastructuur",
    "d6.local_teams": "stevige lokale teams en wijkverbanden",
    "d6.digital_and_operational_infrastructure": "digitale en operationele infrastructuur",
    "finance.d5_d6.funding_instrument": "bekostigingsroute D5/D6",
    "finance.d5_d6.municipal_funding": "gemeentelijke middelen D5/D6",
    "finance.local_alignment_goal": "lokale financiele aansluiting",
    "governance.regional_coordination": "regionale coordinatie",
    "monitoring.framework": "monitoringskader",
    "monitoring.local_learning": "lokaal leren en bijsturen",
    "monitoring.update_2028": "actualisatiecyclus 2028",
    "municipal.role_allocation": "rolverdeling en regie",
    "municipal.implementation_translation": "lokale vertaling in openbare stukken",
    "municipal.almere_initiatives": "Almeerse initiatieven",
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


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: Path, payload: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


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


def theme_definitions() -> list[dict]:
    return load_json(SITE_TAXONOMY_PATH)["themes"]


def navigation_items() -> list[dict]:
    return load_json(SITE_TAXONOMY_PATH)["navigation"]


def site_meta() -> dict:
    return load_json(SITE_TAXONOMY_PATH)["site"]


def topic_label(topic: str) -> str:
    return TOPIC_LABELS.get(topic, topic)


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


def authority_note(claim: dict) -> str | None:
    instrument_type = claim.get("instrument_type")
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
                "jurisdiction_level": document["jurisdiction_level"],
                "authority_note": authority_note(claim),
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
        claim_ids = dedupe(
            choice["supporting_claim_ids"]
            + [claim_id for gap in gap_entries for claim_id in gap["supporting_claim_ids"]]
            + [claim_id for dependency in dependency_entries for claim_id in dependency["supporting_claim_ids"]]
        )
        document_refs = document_refs_from_claim_ids(claim_ids, claims, documents)
        topics = dedupe(choice["based_on_topics"] + [topic for gap in gap_entries for topic in gap["based_on_topics"]])
        linked_theme_ids = dedupe(blueprint["theme_ids"] + theme_ids_for_topics(topics, themes))
        options = option_set(blueprint["decision_id"])
        review_note = review_note_for_topics(topics, uncertainty_by_topic, conflict_by_topic)

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
            "supporting_evidence": evidence_entries(claim_ids, claims, documents),
            "supporting_claim_ids": claim_ids,
            "review_note": review_note,
            "scope_note": "Dit is een machine-gegenereerde mogelijke besluitvraag op basis van de huidige openbare bronbasis; geen vastgestelde gemeentelijke beslissing.",
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
            source_item = gaps[blueprint["source_id"]]
            source_claim_ids = list(source_item["supporting_claim_ids"])
            current_status_detail = GAP_LABELS[blueprint["source_id"]]["summary"]
        else:
            source_item = dependencies[blueprint["source_id"]]
            source_claim_ids = list(source_item["supporting_claim_ids"])
            current_status_detail = DEPENDENCY_LABELS[blueprint["source_id"]]["summary"]

        dependency_entries = [dependencies[dep_id] for dep_id in blueprint["dependency_ids"] if dep_id in dependencies]
        claim_ids = dedupe(
            source_claim_ids
            + [claim_id for dependency in dependency_entries for claim_id in dependency["supporting_claim_ids"]]
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
                "page_url": "/themes/",
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
                "source_url": metadata["source_url"],
            }
        )
    entries.sort(key=lambda item: (item["publication_date"], item["title"]), reverse=True)
    return entries[:5]


def timeline_entries(master_view: dict) -> list[dict]:
    return [
        {
            "date_label": "begin 2027",
            "title": "Tussentijds evaluatiemoment",
            "summary": "In de landelijke bronbasis staat een tussentijds evaluatiemoment voorzien waarmee afspraken kunnen worden aangescherpt of bijgesteld.",
            "linked_domain": "D5 en D6",
        },
        {
            "date_label": "voor 1 juli 2027",
            "title": "Besluitvorming richting 2028",
            "summary": "Voor de verdere koers richting 2028 is bestuurlijke besluitvorming voorzien op basis van monitoring en voortgang.",
            "linked_domain": "D5 en D6",
        },
        {
            "date_label": "2028",
            "title": "Actualisatie van basisfunctionaliteiten",
            "summary": "De bronbasis verwijst naar een actualisatie op basis van monitoring en evaluatie in 2028.",
            "linked_domain": "D5",
        },
        {
            "date_label": "2030",
            "title": "Landelijke dekking van bekende basisfunctionaliteiten",
            "summary": "De landelijke inzet werkt toe naar bredere dekking van de bekende basisfunctionaliteiten vanaf 2030.",
            "linked_domain": "D5",
        },
    ]


def build_home_view(
    almere_view: dict,
    decision_models: list[dict],
    action_models: list[dict],
    themes: list[dict],
    review_queue: dict,
    document_payloads: dict[str, dict],
    documents: dict[str, dict],
) -> dict:
    implementation_status_blocks = [
        {
            "title": "Landelijke basis zichtbaar",
            "metric": len([item for item in almere_view["applicable_d5_items"] + almere_view["applicable_d6_items"] if item["scope"] in {"national", "mixed"}]),
            "summary": "De landelijke basis voor D5 en D6 is in de bronbasis herkenbaar aanwezig.",
        },
        {
            "title": "Lokale aanknopingspunten zichtbaar",
            "metric": len(almere_view["relevant_municipal_documents"]),
            "summary": "Er zijn lokale Almere-documenten zichtbaar, maar niet alle landelijke verwachtingen zijn daarin expliciet overgenomen.",
        },
        {
            "title": "Open uitwerkingsvragen",
            "metric": len(almere_view["local_gaps"]),
            "summary": "De huidige bronbasis laat meerdere punten zien waar lokale explicitering of bestuurlijke keuze nog niet zichtbaar is.",
        },
        {
            "title": "Menselijke duiding nodig",
            "metric": review_queue["summary"]["review"],
            "summary": "Een deel van de bronbasis vraagt nog om menselijke duiding over autoriteit, lokale overname of begripsafbakening.",
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
            "page_url": "/almere/#onzekerheden",
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

    return {
        "view_run_id": SITE_RUN_ID,
        "generated_on": TODAY,
        "as_of_date": almere_view["as_of_date"],
        "title": "Start",
        "executive_summary": executive_summary,
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
        "near_term_timeline": timeline_entries(load_json(MASTER_VIEW_PATH)),
        "featured_themes": build_featured_themes(decision_models, action_models, themes),
        "recent_changes": build_recent_changes(document_payloads, documents),
        "supporting_navigation": [item for item in navigation_items() if item["priority"] == "secondary"],
    }


def build_expected_responsibilities(almere_view: dict) -> list[dict]:
    responsibilities: list[dict] = []
    for item in almere_view["applicable_d5_items"][:3]:
        responsibilities.append(
            {
                "topic": item["topic"],
                "title": topic_label(item["topic"]),
                "summary": "Landelijke basis aanwezig; lokale vertaling en bestuurlijke explicitering blijven voor Almere relevant.",
            }
        )
    for item in almere_view["applicable_d6_items"][:3]:
        responsibilities.append(
            {
                "topic": item["topic"],
                "title": topic_label(item["topic"]),
                "summary": "Landelijke of gemengde basis aanwezig; lokale structuur, regie en aansluiting op regionale infrastructuur vragen om bestuurlijke aandacht.",
            }
        )
    return responsibilities


def build_current_local_state(almere_view: dict) -> list[dict]:
    state: list[dict] = []
    for document in almere_view["relevant_municipal_documents"][:5]:
        state.append(
            {
                "document_id": document["document_id"],
                "title": document["title"],
                "summary": f"In dit document zijn aanknopingspunten zichtbaar voor: {', '.join(topic_label(topic) for topic in document['relevant_topics'][:3])}.",
            }
        )
    return state


def build_almere_site_view(
    almere_view: dict,
    decision_models: list[dict],
    action_models: list[dict],
    claims: dict[str, dict],
    documents: dict[str, dict],
) -> dict:
    evidence_claim_ids = []
    for decision in decision_models[:3]:
        evidence_claim_ids.extend(decision["supporting_claim_ids"][:3])
    for action in action_models[:3]:
        evidence_claim_ids.extend(action["supporting_claim_ids"][:3])

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
                "linked_page_url": "/almere/#onzekerheden",
            }
        )

    return {
        "view_run_id": SITE_RUN_ID,
        "generated_on": TODAY,
        "as_of_date": almere_view["as_of_date"],
        "rows": rows,
    }


def build_site_manifest(decisions: list[dict], actions: list[dict]) -> dict:
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
    return {
        "site_run_id": SITE_RUN_ID,
        "generated_on": TODAY,
        "pages": pages,
        "navigation": navigation_items(),
    }


def main() -> None:
    almere_view = load_json(ALMERE_VIEW_PATH)
    review_queue = load_json(REVIEW_QUEUE_PATH)
    claims = claim_map()
    documents = document_map()
    document_payloads = document_payload_map()
    themes = theme_definitions()

    decision_models = build_decision_models(almere_view, claims, documents, themes)
    action_models = build_action_models(almere_view, claims, documents, decision_models)
    home_view = build_home_view(
        almere_view,
        decision_models,
        action_models,
        themes,
        review_queue,
        document_payloads,
        documents,
    )
    almere_site_view = build_almere_site_view(almere_view, decision_models, action_models, claims, documents)
    dashboard_view = build_dashboard_view(almere_view, decision_models, action_models)
    site_manifest = build_site_manifest(decision_models, action_models)

    write_json(HOME_VIEW_PATH, home_view)
    write_json(ALMERE_SITE_VIEW_PATH, almere_site_view)
    write_json(DASHBOARD_VIEW_PATH, dashboard_view)
    write_json(SITE_MANIFEST_PATH, site_manifest)

    DECISION_DIR.mkdir(parents=True, exist_ok=True)
    ACTION_DIR.mkdir(parents=True, exist_ok=True)
    for model in decision_models:
        write_json(DECISION_DIR / f"{model['decision_id']}.json", model)
    for model in action_models:
        write_json(ACTION_DIR / f"{model['action_id']}.json", model)

    print(f"Wrote {HOME_VIEW_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"Wrote {ALMERE_SITE_VIEW_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"Wrote {DASHBOARD_VIEW_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"Wrote {SITE_MANIFEST_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"Wrote {len(decision_models)} decision view models and {len(action_models)} action view models")


if __name__ == "__main__":
    main()
