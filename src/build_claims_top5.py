from __future__ import annotations

import json
import re
import unicodedata
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCUMENT_DIR = REPO_ROOT / "data" / "extracted" / "documents"
INVENTORY_PATH = REPO_ROOT / "data" / "extracted" / "document_inventory.json"
AUTHORITY_RULES_PATH = REPO_ROOT / "config" / "authority_rules.json"
CLAIM_SCHEMA_PATH = REPO_ROOT / "data" / "schemas" / "claim.schema.json"
OUTPUT_DIR = REPO_ROOT / "data" / "extracted" / "claims"
SENTENCE_VALIDATOR_REJECTS_PATH = OUTPUT_DIR / "sentence_validator_rejects.json"
DEDUP_LOG_PATH = OUTPUT_DIR / "dedup_log.json"

CLAIM_EXTRACTION_RUN_ID = "phase4_all_docs_claims_v3"
RELATION_SEED_DOCUMENT_IDS = [
    "nat_azwa_2025_definitief",
    "nat_azwa_2025_onderhandelaarsakkoord",
    "nat_azwa_2026_cw31_kader_d5_d6",
    "reg_flevoland_2023_regioplan_iza",
    "mun_almere_pga_transformatieplan",
]
SENTENCE_START_WHITELIST = {"de", "het", "een", "dat", "dit", "deze", "die", "in", "met", "voor", "van", "op", "om", "bij"}
FIRST_WORD_PATTERN = re.compile(r"^[\"'“”‘’(\[]*([A-Za-zÀ-ÖØ-öø-ÿ]+)")
SENTENCE_END_PATTERN = re.compile(r'(?:[.!?…»”"]|\.\.\.)$')
LOWER_AUTHORITY_INSTRUMENTS = {"faq", "commentary", "regional_plan", "implementation_plan", "municipal_policy"}
PRACTICAL_GUIDANCE_INSTRUMENTS = {"faq", "commentary", "template", "process_note"}
NORM_SIGNAL_TERMS = (
    "moet",
    "moeten",
    "vereist",
    "verplicht",
    "voorwaarde",
    "voorwaarden",
    "dient",
    "dienen",
    "uiterlijk",
    "afgesproken",
    "spreken af",
    "vastgesteld",
    "verantwoorden",
    "aanleveren",
)
AGREEMENT_SIGNAL_TERMS = ("afgesproken", "spreken af", "partijen spreken", "akkoord", "afspraken")
EXPECTATION_SIGNAL_TERMS = ("verwacht", "beoogd", "doel", "werkt toe", "streven", "richting", "uiterlijk")
GUIDANCE_SIGNAL_TERMS = ("handreiking", "format", "toelichting", "faq", "kan", "kunnen", "advies", "praktisch")
DEADLINE_SIGNAL_TERMS = (
    "uiterlijk",
    "deadline",
    "aanvraagdeadline",
    "voor 1 juli",
    "voor 15 november",
    "voor 31 maart",
    "15 juli",
    "aanleveren",
    "verantwoorden",
    "gereed moet zijn",
)
EXPECTED_TIME_SIGNAL_TERMS = (
    "verwacht",
    "naar verwachting",
    "planning",
    "in de praktijk",
    "medio",
    "voorjaar",
    "najaar",
)
REVIEW_TIME_SIGNAL_TERMS = (
    "evaluatie",
    "tussentijds",
    "mid-term",
    "mtr",
    "herijk",
    "herijken",
    "actualisatie",
    "bijstelling",
)
BUDGET_TIME_SIGNAL_TERMS = (
    "begroting",
    "gemeentefonds",
    "circulaire",
    "meicirculaire",
    "septembercirculaire",
    "decembercirculaire",
    "spuk",
    "subsidie",
    "middelen",
    "financiering",
    "verantwoording",
)
LOCAL_PLANNING_SIGNAL_TERMS = (
    "gemeenteraad",
    "politieke markt",
    "vergaderschema",
    "besluitvorming",
    "benoeming",
    "afscheid raad",
    "verkiezingen",
)
IMPLEMENTATION_HORIZON_TERMS = (
    "2030",
    "2028",
    "2029",
    "dekking",
    "uitrol",
    "gereed",
    "implementatie",
    "horizon",
)
FUNDING_ROUTE_TERMS = (
    "spuk",
    "specifieke uitkering",
    "gemeentefonds",
    "fondsbeheerder",
    "vng",
    "zorgverzekeraar",
    "zvw",
    "bekostigingsroute",
    "financieringsroute",
    "uitkering",
)
APPLICATION_CONDITION_TERMS = (
    "aanvraag",
    "aanvragen",
    "voorwaarde",
    "voorwaarden",
    "randvoorwaardelijk",
    "vereist",
    "moet worden aangevraagd",
    "penvoerder",
)
BUDGET_WINDOW_TERMS = (
    "2026",
    "2027",
    "2028",
    "2029",
    "2030",
    "2031",
    "meerjarig",
    "startpakket",
    "budget",
    "budgettair",
    "begroting",
    "middelen",
    "macrokader",
)
ALLOCATION_MECHANISM_TERMS = (
    "verdeeld",
    "verdeling",
    "verdeelsleutel",
    "allocatie",
    "toegekend",
    "toekenning",
    "uitkeren",
    "uitkering",
    "beschikbaar gesteld",
)
FINANCE_CONTEXT_TERMS = (
    "besteding",
    "bestedingsruimte",
    "mag worden besteed",
    "inzet van middelen",
    "middelen inzetten",
    "cofinanciering",
    "eigen bijdrage",
)
ACCOUNTABILITY_RULE_TERMS = (
    "verantwoording",
    "verantwoorden",
    "aanleveren",
    "rapportage",
    "siSa",
    "controle",
    "monitoring",
)
LOCAL_FUNDING_GAP_TERMS = (
    "lokale verdeling",
    "lokaal budget",
    "budgetverdeling",
    "niet expliciet",
    "geen expliciete",
    "nog geen",
    "niet zichtbaar",
    "lokale keuze",
    "onbekend",
)
GOVERNANCE_ACTOR_TERMS = {
    "ministerie": ("ministerie", "vws", "minister"),
    "vng": ("vng",),
    "mandaatgemeente": ("mandaatgemeente", "mandaathouder"),
    "regio": ("regio", "regionaal", "regionale"),
    "gemeente": ("gemeente", "gemeenten", "gemeentelijk"),
    "gemeenteraad": ("gemeenteraad", "raad", "raadsbesluit", "besluitenlijst"),
    "college": ("college", "college van b&w", "college van burgemeester"),
    "zorgverzekeraar": ("zorgverzekeraar", "zorgverzekeraars", "zn", "zvw"),
    "uitvoeringspartner": ("aanbieder", "aanbieders", "uitvoerder", "uitvoerders", "partner", "partners"),
}
DECISION_ROLE_TERMS = (
    "besluit",
    "besluiten",
    "besluitvorming",
    "vastgesteld",
    "vaststellen",
    "instemmen",
    "aangenomen",
    "amendement",
)
COORDINATION_ROLE_TERMS = (
    "coordineert",
    "coordinatie",
    "coordineren",
    "regie",
    "regisseur",
    "onder regie",
    "afstemming",
    "samenwerking",
)
APPLICATION_ROLE_TERMS = (
    "aanvraag",
    "aanvragen",
    "penvoerder",
    "indienen",
    "aanleveren",
)
EXECUTION_ROLE_TERMS = (
    "uitvoering",
    "uitvoeren",
    "organiseren",
    "implementatie",
    "realiseren",
    "leveren",
    "inzet",
)
ACCOUNTABILITY_ROLE_TERMS = (
    "verantwoording",
    "verantwoorden",
    "aanspreekbaar",
    "eigenaar",
    "eigenaarschap",
    "verantwoordelijk",
    "verantwoordelijkheid",
)
APPROVAL_ROLE_TERMS = (
    "goedkeuren",
    "goedkeuring",
    "akkoord",
    "instemming",
    "vaststelling",
)
REVIEW_ROLE_TERMS = (
    "toets",
    "toetsen",
    "review",
    "evaluatie",
    "monitoring",
    "controle",
)
GOVERNANCE_GAP_TERMS = (
    "onduidelijk",
    "niet expliciet",
    "geen expliciete",
    "nog geen",
    "moet worden verduidelijkt",
)
ALMERE_TERMS = ("almere", "almeerse", "gemeente almere", "raad van almere")
FLEVOLAND_TERMS = ("flevoland", "flevolandse", "ggd flevoland", "zorgzaam flevoland")
REGIONAL_SPLIT_TERMS = {
    "IZA/AZWA-regio": ("iza-regio", "azwa-regio", "regioplan", "werkagenda", "mandaatgemeente"),
    "GGD-regio": ("ggd-regio", "ggd flevoland", "jgz almere", "publieke gezondheid"),
    "zorgkantoorregio": ("zorgkantoor", "zorgkantoorregio"),
    "ROAZ/subregio": ("roaz", "subregio", "noord-veluwe", "zeewolde"),
    "provincie": ("provincie", "provinciaal"),
    "gemeentelijk": ("gemeente", "gemeenten", "gemeenteraad", "college"),
}
LOCAL_ADOPTION_GAP_TERMS = (
    "lokale overname",
    "lokale uitwerking",
    "lokaal vastgelegd",
    "niet expliciet",
    "geen expliciete",
    "nog geen",
    "niet zichtbaar",
)
EXECUTION_OPERATIONAL_REQUIREMENT_TERMS = (
    "moet worden georganiseerd",
    "moeten worden georganiseerd",
    "organiseren",
    "inrichten",
    "uitwerken",
    "ontwikkelen",
    "versterken",
    "voorbereiden",
)
EXECUTION_ACTIVITY_TERMS = (
    "uitvoering",
    "uitvoeren",
    "implementatie",
    "realisatie",
    "realiseren",
    "gestart",
    "loopt",
    "lopende",
    "in gang",
    "pilot",
    "project",
    "programma",
)
EXECUTION_DECISION_TERMS = (
    "besluitvraag",
    "keuze",
    "besluit nodig",
    "moet besluiten",
    "besluitvorming",
    "vaststellen",
    "prioriteren",
)
EXECUTION_DEPENDENCY_TERMS = (
    "afhankelijk",
    "voorwaarde",
    "randvoorwaarde",
    "vereist",
    "nodig",
    "mits",
    "alleen als",
    "aansluiting",
)
EXECUTION_SEQUENCING_TERMS = (
    "fasering",
    "fase",
    "volgorde",
    "stap",
    "eerst",
    "daarna",
    "planning",
    "mijlpaal",
    "start",
    "voorbereiding",
)
EXECUTION_CAPACITY_TERMS = (
    "capaciteit",
    "uitvoeringscapaciteit",
    "fte",
    "personeel",
    "bemensing",
    "arbeidsmarkt",
)
EXECUTION_REVIEW_TERMS = (
    "review",
    "toets",
    "toetsen",
    "valideren",
    "validatie",
    "monitoring",
    "evaluatie",
    "leren",
    "dashboard",
)


def normalize_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip().lower()
    text = unicodedata.normalize("NFKD", text)
    return text.encode("ascii", "ignore").decode("ascii")


def normalized_statement_prefix(statement: str, max_chars: int = 200) -> str:
    return re.sub(r"\s+", " ", statement).strip().lower()[:max_chars]


def first_word(text: str) -> str | None:
    match = FIRST_WORD_PATTERN.search(text.strip())
    return match.group(1) if match else None


def has_invalid_sentence_start(statement: str) -> bool:
    word = first_word(statement)
    if not word:
        return False
    return word[0].islower() and word.lower() not in SENTENCE_START_WHITELIST


def has_invalid_sentence_end(statement: str) -> bool:
    compact = statement.strip()
    return bool(compact) and SENTENCE_END_PATTERN.search(compact) is None


def should_reject_for_sentence_boundary(statement: str) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if has_invalid_sentence_start(statement):
        reasons.append("lowercase_mid_sentence_start")
    if has_invalid_sentence_end(statement):
        reasons.append("missing_sentence_terminal")

    if "lowercase_mid_sentence_start" in reasons:
        return True, reasons

    if "missing_sentence_terminal" in reasons:
        normalized = normalize_text(statement)
        heading_like = len(statement) < 140 or normalized.startswith(
            (
                "datum ",
                "de voorzitter van de tweede kamer",
                "regionale eerstelijnssamenwerkingsverbanden",
                "pagina ",
            )
        )
        section_heading = bool(re.match(r"^\d+(?:\.\d+)*\s+[A-ZÀ-ÖØ-Þ]", statement.strip()))
        if heading_like or section_heading:
            return True, reasons

    return False, reasons


def contains_any(normalized_text: str, *terms: str) -> bool:
    return any(normalize_text(term) in normalized_text for term in terms)


def contains_term(normalized_text: str, term: str) -> bool:
    normalized_term = normalize_text(term)
    return bool(re.search(rf"(?<!\w){re.escape(normalized_term)}(?!\w)", normalized_text))


def normative_status_for(
    statement: str,
    instrument_type: str,
    instrument_profile: dict,
    source_statement_type: str,
    topic: str,
) -> dict:
    normalized = normalize_text(statement)
    has_norm_signal = contains_any(normalized, *NORM_SIGNAL_TERMS)
    has_agreement_signal = contains_any(normalized, *AGREEMENT_SIGNAL_TERMS)
    has_expectation_signal = contains_any(normalized, *EXPECTATION_SIGNAL_TERMS)
    has_guidance_signal = contains_any(normalized, *GUIDANCE_SIGNAL_TERMS)
    can_bind = bool(instrument_profile.get("can_create_binding_obligation"))
    is_norm_topic = topic.startswith(("d5.", "d6.", "finance.", "governance."))

    if instrument_type == "agreement" or has_agreement_signal and instrument_type in {"framework", "kamerbrief"}:
        status = "agreement"
        label = "Afspraak of akkoordtekst"
        guardrail = "Formuleer als afspraak tussen akkoordpartijen; niet automatisch als wettelijke plicht voor Almere."
    elif can_bind and has_norm_signal:
        status = "binding"
        label = "Bindend of formeel verplichtend"
        guardrail = "Mag sterk worden geformuleerd, maar alleen dicht bij de bronpassage."
    elif instrument_type in LOWER_AUTHORITY_INSTRUMENTS and (has_norm_signal or is_norm_topic):
        status = "lower_authority_signal"
        label = "Lagere-autoriteitssignaal"
        guardrail = "Altijd expliciet toeschrijven aan de bron; niet als harde norm presenteren zonder sterkere bron."
    elif instrument_type in PRACTICAL_GUIDANCE_INSTRUMENTS or has_guidance_signal:
        status = "guidance"
        label = "Toelichting of praktische guidance"
        guardrail = "Formuleer als toelichting, format, advies of handreiking."
    elif has_expectation_signal or is_norm_topic and source_statement_type == "direct_extraction":
        status = "expectation"
        label = "Verwachting of richtinggevende norm"
        guardrail = "Formuleer als verwachting, richting of uitwerkingskader; vermijd verplichtende taal."
    else:
        status = "contextual"
        label = "Contextueel signaal"
        guardrail = "Gebruik als context of bronaanwijzing, niet als norm."

    return {
        "status": status,
        "label": label,
        "source_authority": instrument_type,
        "has_normative_language": has_norm_signal,
        "public_wording_guardrail": guardrail,
        "needs_attribution": status in {"lower_authority_signal", "guidance"} or source_statement_type == "contextual_relevance",
    }


def time_signal_for(statement: str) -> str:
    normalized = normalize_text(statement)
    if re.search(r"\b\d{4}-\d{2}-\d{2}\b", statement):
        return "exact_date"
    if re.search(r"\b\d{1,2}\s+(januari|februari|maart|april|mei|juni|juli|augustus|september|oktober|november|december)\s+\d{4}\b", normalized):
        return "exact_date"
    if re.search(r"\bq[1-4]\s+\d{4}\b", normalized):
        return "quarter"
    if re.search(r"\b(voorjaar|najaar|begin|medio|eind)\s+20\d{2}\b", normalized):
        return "period"
    if re.search(r"\b20\d{2}\s*[-/]\s*20\d{2}\b", normalized):
        return "period"
    if re.search(r"\b20\d{2}\b", normalized):
        return "year"
    if contains_any(normalized, "mei", "september", "december"):
        return "month_or_cycle"
    return "none"


def time_status_for(
    statement: str,
    document_id: str,
    instrument_type: str,
    source_statement_type: str,
    topic: str,
    claim_type: str,
) -> dict:
    normalized = normalize_text(statement)
    date_signal = time_signal_for(statement)
    is_time_topic = topic.startswith(("timeline.", "monitoring."))
    is_local_calendar = document_id == "mun_almere_raad_vergaderschema_2026" or topic == "timeline.local_governance_calendar"
    has_deadline_signal = contains_any(normalized, *DEADLINE_SIGNAL_TERMS)
    has_expected_signal = contains_any(normalized, *EXPECTED_TIME_SIGNAL_TERMS)
    has_review_signal = contains_any(normalized, *REVIEW_TIME_SIGNAL_TERMS)
    has_budget_signal = contains_any(normalized, *BUDGET_TIME_SIGNAL_TERMS)
    has_local_planning_signal = contains_any(normalized, *LOCAL_PLANNING_SIGNAL_TERMS)
    has_implementation_horizon = contains_any(normalized, *IMPLEMENTATION_HORIZON_TERMS)

    if has_deadline_signal:
        status = "formal_deadline"
        label = "Formele of harde termijn"
        guardrail = "Formuleer als deadline alleen wanneer de bronpassage zelf de uiterste termijn draagt."
    elif has_review_signal or topic.startswith("monitoring."):
        status = "review_or_update_moment"
        label = "Evaluatie-, herijkings- of actualisatiemoment"
        guardrail = "Formuleer als review- of updatecyclus; niet automatisch als lokaal besluitmoment."
    elif has_budget_signal or topic.startswith("finance."):
        status = "budget_calendar_moment"
        label = "Begrotings- of financieringsmoment"
        guardrail = "Koppel aan de financiele bronroute; maak geen lokale budgetkeuze zonder lokale bron."
    elif is_local_calendar or has_local_planning_signal:
        status = "local_planning_context"
        label = "Lokale planningscontext"
        guardrail = "Gebruik als lokale bestuurlijke context; niet als landelijke of inhoudelijke D5/D6-deadline."
    elif has_expected_signal or date_signal in {"quarter", "month_or_cycle", "period"}:
        status = "expected_moment"
        label = "Verwacht of indicatief moment"
        guardrail = "Formuleer als verwacht, indicatief of bronafhankelijk moment; niet als harde deadline."
    elif has_implementation_horizon and (is_time_topic or claim_type in {"timeline_commitment", "implementation_requirement"}):
        status = "implementation_horizon"
        label = "Implementatiehorizon"
        guardrail = "Formuleer als horizon of fasering; vermijd precieze lokale planning zonder lokale bron."
    elif date_signal != "none" and is_time_topic:
        status = "source_dated_moment"
        label = "Bronverankerd tijdmoment"
        guardrail = "Gebruik als bronverankerd tijdmoment en controleer de bronpassage voor precieze formulering."
    elif date_signal != "none":
        status = "publication_or_context_date"
        label = "Publicatie- of contextdatum"
        guardrail = "Gebruik als bron- of contextdatum; niet als beleidsdeadline."
    else:
        status = "undated_context"
        label = "Geen zelfstandig tijdmoment"
        guardrail = "Niet op de tijdlijn plaatsen zonder aanvullende tijdbron."

    return {
        "status": status,
        "label": label,
        "date_signal": date_signal,
        "source_temporal_anchor": "explicit_text_signal" if date_signal != "none" or is_time_topic else "publication_context",
        "public_wording_guardrail": guardrail,
        "needs_review": status in {"expected_moment", "local_planning_context"} or source_statement_type == "contextual_relevance",
    }


def money_status_for(
    statement: str,
    document_id: str,
    instrument_type: str,
    source_statement_type: str,
    topic: str,
    claim_type: str,
) -> dict:
    normalized = normalize_text(statement)
    is_finance_topic = topic.startswith("finance.") or topic == "governance_and_finance.other"
    has_funding_route = contains_any(normalized, *FUNDING_ROUTE_TERMS)
    has_application_condition = contains_any(normalized, *APPLICATION_CONDITION_TERMS)
    has_budget_window = contains_any(normalized, *BUDGET_WINDOW_TERMS)
    has_allocation = contains_any(normalized, *ALLOCATION_MECHANISM_TERMS)
    has_finance_context = contains_any(normalized, *FINANCE_CONTEXT_TERMS)
    has_accountability = contains_any(normalized, *ACCOUNTABILITY_RULE_TERMS)
    has_local_gap = contains_any(normalized, *LOCAL_FUNDING_GAP_TERMS)
    mentions_money = is_finance_topic or any(
        (
            has_funding_route,
            has_application_condition,
            has_budget_window,
            has_allocation,
            has_finance_context,
            has_accountability,
            has_local_gap,
        )
    )

    if has_local_gap and mentions_money:
        status = "local_funding_gap"
        label = "Lokale financieringslacune"
        guardrail = "Formuleer als lokaal invul- of besluitpunt; vul geen budget of eigenaar in zonder lokale bron."
    elif has_accountability:
        status = "accountability_rule"
        label = "Verantwoordings- of rapportageregel"
        guardrail = "Koppel aan de bronroute en verantwoordingsplicht; maak er geen bestedingsruimte van."
    elif has_application_condition:
        status = "application_condition"
        label = "Aanvraagvoorwaarde of randvoorwaarde"
        guardrail = "Formuleer als aanvraag- of procesvoorwaarde; controleer of de bron formeel of praktisch is."
    elif has_allocation:
        status = "allocation_mechanism"
        label = "Verdeel- of toekenningsmechanisme"
        guardrail = "Beschrijf alleen het verdeelmechanisme dat de bron noemt; geen lokale verdeling afleiden."
    elif has_funding_route:
        status = "funding_route"
        label = "Financieringsroute"
        guardrail = "Beschrijf de route en betrokken partijen; niet automatisch als lokaal beschikbaar budget formuleren."
    elif has_budget_window and mentions_money and not has_finance_context:
        status = "budget_window"
        label = "Budgetvenster of financieel tijdvak"
        guardrail = "Gebruik als budgetvenster; maak geen claim over lokale besteding zonder lokale bron."
    elif mentions_money:
        status = "finance_context"
        label = "Financiele context"
        guardrail = "Gebruik als context; controleer sterkere bronnen voordat hier een financieringsregel van wordt gemaakt."
    else:
        status = "not_financial"
        label = "Geen zelfstandige financiele claim"
        guardrail = "Niet gebruiken als financieringsregel."

    return {
        "status": status,
        "label": label,
        "financial_signal": mentions_money,
        "source_finance_anchor": "explicit_finance_signal" if mentions_money else "none",
        "public_wording_guardrail": guardrail,
        "needs_verification": status in {"local_funding_gap", "finance_context"}
        or source_statement_type == "contextual_relevance",
    }


def actor_signals_for(normalized_statement: str) -> list[str]:
    signals = [
        actor
        for actor, terms in GOVERNANCE_ACTOR_TERMS.items()
        if any(contains_term(normalized_statement, term) for term in terms)
    ]
    return unique_preserving_order(signals)


def governance_status_for(
    statement: str,
    document_id: str,
    instrument_type: str,
    source_statement_type: str,
    topic: str,
    claim_type: str,
) -> dict:
    normalized = normalize_text(statement)
    actor_signals = actor_signals_for(normalized)
    is_governance_topic = topic.startswith("governance.") or topic in {
        "governance_and_finance.other",
        "municipal.role_allocation",
    }
    has_decision = contains_any(normalized, *DECISION_ROLE_TERMS)
    has_coordination = contains_any(normalized, *COORDINATION_ROLE_TERMS)
    has_application = contains_any(normalized, *APPLICATION_ROLE_TERMS)
    has_execution = contains_any(normalized, *EXECUTION_ROLE_TERMS)
    has_accountability = contains_any(normalized, *ACCOUNTABILITY_ROLE_TERMS)
    has_approval = contains_any(normalized, *APPROVAL_ROLE_TERMS)
    has_review = contains_any(normalized, *REVIEW_ROLE_TERMS)
    has_gap = contains_any(normalized, *GOVERNANCE_GAP_TERMS)
    has_governance_signal = is_governance_topic or bool(actor_signals) or any(
        (
            has_decision,
            has_coordination,
            has_application,
            has_execution,
            has_accountability,
            has_approval,
            has_review,
            has_gap,
        )
    )

    if has_gap and has_governance_signal:
        status = "governance_gap"
        label = "Governance- of rolverdelingsgat"
        guardrail = "Formuleer als validatie- of besluitvraag; vul actor, mandaat of eigenaar niet in zonder bron."
    elif has_decision:
        status = "decision_role"
        label = "Besluitvormende rol"
        guardrail = "Splits besluitvorming van coordinatie en uitvoering; noem de beslissende actor alleen als de bron dat draagt."
    elif has_approval:
        status = "approval_role"
        label = "Goedkeurings- of vaststellingsrol"
        guardrail = "Gebruik als goedkeurings- of vaststellingsrol; niet automatisch als uitvoeringsverantwoordelijkheid."
    elif has_application:
        status = "application_role"
        label = "Aanvraag- of indieningsrol"
        guardrail = "Gebruik als aanvraag- of penvoerdersrol; niet automatisch als inhoudelijke eigenaar."
    elif has_accountability:
        status = "accountability_role"
        label = "Verantwoordings- of eigenaarschapsrol"
        guardrail = "Maak duidelijk of het gaat om eigenaarschap, aanspreekbaarheid of verantwoording."
    elif has_coordination:
        status = "coordination_role"
        label = "Coordinatie- of regierol"
        guardrail = "Gebruik als coordinatie/regie; niet vermengen met besluitvorming of uitvoering."
    elif has_execution:
        status = "execution_role"
        label = "Uitvoeringsrol"
        guardrail = "Gebruik als uitvoeringsrol; noem geen opdrachtgever of eigenaar tenzij de bron dat zegt."
    elif has_review:
        status = "review_role"
        label = "Review-, monitorings- of toetsrol"
        guardrail = "Gebruik als toetsing, monitoring of evaluatie; niet als besluitvorming."
    elif has_governance_signal:
        status = "actor_context"
        label = "Actor- of governancecontext"
        guardrail = "Gebruik als context; specificeer rol alleen wanneer de bron die rol benoemt."
    else:
        status = "not_governance"
        label = "Geen zelfstandige governanceclaim"
        guardrail = "Niet gebruiken als rol- of besluitclaim."

    vague_region_only = actor_signals == ["regio"]

    return {
        "status": status,
        "label": label,
        "actor_signals": actor_signals,
        "source_governance_anchor": "explicit_governance_signal" if has_governance_signal else "none",
        "public_wording_guardrail": guardrail,
        "needs_verification": status in {"governance_gap", "actor_context"} or vague_region_only
        or source_statement_type == "contextual_relevance",
        "vague_region_only": vague_region_only,
    }


def regional_split_signals_for(normalized_statement: str) -> list[str]:
    signals = [
        split
        for split, terms in REGIONAL_SPLIT_TERMS.items()
        if any(normalize_text(term) in normalized_statement for term in terms)
    ]
    return unique_preserving_order(signals)


def locality_status_for(
    statement: str,
    document_id: str,
    jurisdiction_level: str,
    source_statement_type: str,
    topic: str,
) -> dict:
    normalized = normalize_text(statement)
    explicit_almere = contains_any(normalized, *ALMERE_TERMS) or document_id.startswith("mun_almere_")
    explicit_flevoland = contains_any(normalized, *FLEVOLAND_TERMS) or document_id.startswith("reg_flevoland_") or document_id.startswith("reg_ggd_flevoland_")
    regional_splits = regional_split_signals_for(normalized)
    substantive_regional_splits = [split for split in regional_splits if split != "gemeentelijk"]
    national_source = document_id.startswith("nat_") or jurisdiction_level == "national"
    municipal_source = document_id.startswith("mun_") or jurisdiction_level == "municipal"
    regional_source = document_id.startswith("reg_") or jurisdiction_level == "regional"
    has_adoption_gap = contains_any(normalized, *LOCAL_ADOPTION_GAP_TERMS)
    is_locality_topic = topic.startswith("municipal.") or topic.startswith("governance.local")
    inferred_local = source_statement_type == "contextual_relevance" or (
        national_source and ("Almere" in applies_to_for(document_id) or is_locality_topic)
    )

    if has_adoption_gap and (explicit_almere or explicit_flevoland or is_locality_topic or inferred_local):
        status = "local_adoption_gap"
        label = "Lokale adoptie- of documentatiegap"
        scope = "Almere/Flevoland validation"
        guardrail = "Formuleer als lokale adoptie- of documentatiegap; niet als lokaal vastgesteld beleid."
    elif explicit_almere:
        status = "explicit_almere"
        label = "Expliciet Almeers"
        scope = "Almere"
        guardrail = "Mag als Almeerse bronlijn worden gebruikt, maar alleen voor wat de bron zelf zegt."
    elif explicit_flevoland:
        status = "explicit_flevoland"
        label = "Expliciet Flevolands"
        scope = "Flevoland"
        guardrail = "Formuleer als Flevolandse of GGD/Flevolandse bronlijn; niet automatisch als Almeerse keuze."
    elif substantive_regional_splits or regional_source:
        status = "regional_split_context"
        label = "Regionale split-context"
        scope = "regional split"
        guardrail = "Benoem welke regionale schaal bedoeld is; gebruik niet alleen 'de regio'."
    elif national_source and inferred_local:
        status = "national_with_local_relevance"
        label = "Landelijk met lokale relevantie"
        scope = "national to local"
        guardrail = "Formuleer als landelijke lijn met relevantie voor Almere; niet als lokale vaststelling."
    elif national_source:
        status = "national_general"
        label = "Algemeen landelijk"
        scope = "Netherlands"
        guardrail = "Gebruik als landelijke context; lokale toepassing vraagt aparte bron of interpretatie."
    else:
        status = "national_general"
        label = "Algemene broncontext"
        scope = "general"
        guardrail = "Gebruik als algemene context; lokale toepassing vraagt aparte bron of interpretatie."

    return {
        "status": status,
        "label": label,
        "locality_scope": scope,
        "regional_split_signals": regional_splits,
        "explicit_location_signals": {
            "almere": explicit_almere,
            "flevoland": explicit_flevoland,
        },
        "public_wording_guardrail": guardrail,
        "needs_verification": status in {
            "local_adoption_gap",
            "national_with_local_relevance",
            "regional_split_context",
        },
    }


def execution_need_signals_for(normalized_statement: str) -> list[str]:
    signals: list[str] = []
    if contains_any(normalized_statement, *EXECUTION_OPERATIONAL_REQUIREMENT_TERMS):
        signals.append("operational_requirement")
    if contains_any(normalized_statement, *EXECUTION_ACTIVITY_TERMS):
        signals.append("implementation_activity")
    if contains_any(normalized_statement, *EXECUTION_DECISION_TERMS):
        signals.append("decision_question")
    if contains_any(normalized_statement, *EXECUTION_DEPENDENCY_TERMS):
        signals.append("dependency")
    if contains_any(normalized_statement, *EXECUTION_SEQUENCING_TERMS):
        signals.append("sequencing")
    if contains_any(normalized_statement, *EXECUTION_CAPACITY_TERMS):
        signals.append("capacity")
    if contains_any(normalized_statement, *EXECUTION_REVIEW_TERMS):
        signals.append("review")
    return unique_preserving_order(signals)


def execution_status_for(
    statement: str,
    document_id: str,
    source_statement_type: str,
    topic: str,
    claim_type: str,
) -> dict:
    normalized = normalize_text(statement)
    need_signals = execution_need_signals_for(normalized)
    is_execution_topic = topic.startswith(("d5.", "d6.", "municipal.", "monitoring.")) or topic in {
        "timeline.d5_d6_implementation",
        "timeline.implementation_status",
        "timeline.rollout_2030",
        "timeline.almere_2029",
    }
    has_explicit_execution_signal = bool(need_signals)
    has_execution_signal = has_explicit_execution_signal or is_execution_topic or claim_type == "implementation_requirement"

    if "decision_question" in need_signals:
        status = "decision_question"
        label = "Uitvoering vraagt besluit of keuze"
        guardrail = "Formuleer als besluit- of keuzevraag; schrijf niet dat uitvoering al besloten is."
    elif "dependency" in need_signals:
        status = "dependency"
        label = "Uitvoering heeft afhankelijkheid of randvoorwaarde"
        guardrail = "Benoem de afhankelijkheid; los haar niet op zonder bron of validatie."
    elif "capacity" in need_signals:
        status = "capacity_need"
        label = "Uitvoering vraagt capaciteit of bemensing"
        guardrail = "Formuleer als capaciteitsvraag; vul geen fte, team of eigenaar in zonder bron."
    elif "sequencing" in need_signals:
        status = "sequencing_need"
        label = "Uitvoering vraagt fasering of volgorde"
        guardrail = "Formuleer als fasering of volgordevraag; maak er geen harde planning van zonder bron."
    elif "review" in need_signals:
        status = "review_task"
        label = "Uitvoering vraagt review, monitoring of validatie"
        guardrail = "Formuleer als review-, monitorings- of validatietaak; niet als besluit of uitvoeringseigenaarschap."
    elif "implementation_activity" in need_signals:
        status = "implementation_activity"
        label = "Uitvoeringsactiviteit zichtbaar"
        guardrail = "Beschrijf alleen de activiteit die de bron noemt; voeg geen eigenaar, bereik of vervolgplanning toe."
    elif "operational_requirement" in need_signals or claim_type == "implementation_requirement":
        status = "operational_requirement"
        label = "Operationele vereiste of inrichting"
        guardrail = "Formuleer als wat moet worden ingericht of voorbereid; niet als lokaal al uitgevoerde actie."
    elif has_execution_signal:
        status = "execution_context"
        label = "Uitvoeringscontext"
        guardrail = "Gebruik als uitvoeringscontext; maak er geen actie, eigenaar of planning van zonder sterker bewijs."
    else:
        status = "not_execution"
        label = "Geen zelfstandige uitvoeringsclaim"
        guardrail = "Niet gebruiken als actie- of implementatieclaim."

    return {
        "status": status,
        "label": label,
        "execution_need_signals": need_signals,
        "source_execution_anchor": "explicit_execution_signal" if has_explicit_execution_signal else (
            "topic_context" if has_execution_signal else "none"
        ),
        "public_wording_guardrail": guardrail,
        "needs_verification": status
        in {
            "decision_question",
            "dependency",
            "capacity_need",
            "sequencing_need",
            "review_task",
            "execution_context",
        }
        or source_statement_type == "contextual_relevance",
    }


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


def load_document_ids() -> list[str]:
    payload = load_json(INVENTORY_PATH)
    return [
        item["document_id"]
        for item in payload["documents"]
        if (DOCUMENT_DIR / f"{item['document_id']}.json").exists()
    ]


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


def validity_status_for(metadata: dict, source_statement_type: str) -> str:
    document_id = metadata["document_id"]
    if document_id == "nat_azwa_2025_onderhandelaarsakkoord":
        return "historical"
    if metadata["jurisdiction_level"] in {"regional", "municipal"}:
        return "contextual_active"
    if source_statement_type == "contextual_relevance":
        return "contextual_active"
    if metadata["source_classification"] == "supporting_commentary":
        return "contextual_active"
    if metadata["status"] == "reference":
        return "historical"
    return "active"


def confidence_for(jurisdiction_level: str, source_statement_type: str, topic: str, instrument_type: str) -> float:
    if source_statement_type == "contextual_relevance":
        base = 0.68
    elif instrument_type == "faq":
        base = 0.52
    elif instrument_type == "commentary":
        base = 0.56
    elif instrument_type == "implementation_plan":
        base = 0.78
    elif instrument_type == "regional_plan":
        base = 0.82
    elif instrument_type == "kamerbrief":
        base = 0.88
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


def human_review_status_for(source_statement_type: str, topic: str, instrument_type: str) -> str:
    if source_statement_type == "contextual_relevance" or topic.endswith(".other") or instrument_type in {"faq", "commentary"}:
        return "needs_human_review"
    return "seeded_from_document_extraction"


def classify_d5(document_id: str, statement: str) -> tuple[str, str, str]:
    normalized = normalize_text(statement)

    if document_id in {"mun_almere_pga_transformatieplan", "mun_almere_pga_seo_businesscase_2024"}:
        if contains_any(
            normalized,
            "health first",
            "right help in the right place",
            "minder nadruk op ziekte en meer op gezondheid",
            "gezondheid voorop",
            "positieve gezondheid",
            "veerkracht, gezondheid en zelfredzaamheid",
        ):
            return "d5.health_first_shift", "prevention_first", "local_strategy"
        if contains_any(
            normalized,
            "samen sterker in de wijk",
            "mentale klachten",
            "verkennend gesprek",
            "mentale gezondheidscentra",
        ):
            return "d5.mentale_gezondheidsnetwerken", "almere_neighbourhood_model", "contextual_implementation_signal"
        return "d5.cross_domain_collaboration", "almere_neighbourhood_collaboration", "contextual_implementation_signal"

    if document_id == "reg_flevoland_2023_regioplan_iza":
        if contains_any(normalized, "ecosysteem mentale gezondheid", "samen sterker in de wijk"):
            return "d5.mentale_gezondheidsnetwerken", "flevoland_neighbourhood_model", "contextual_implementation_signal"
        return "d5.cross_domain_collaboration", "regional_domain_overstijgende_samenwerking", "contextual_implementation_signal"

    if contains_any(
        normalized,
        "five life domains",
        "five leefgebieden",
        "organized around five life domains",
        "vijf leefgebieden",
        "kansrijk opgroeien",
        "gezonde leefstijl",
        "vitaal ouder worden",
        "gezondheidsachterstanden",
    ) and contains_any(normalized, "basisfunctionaliteit", "basisfunctionaliteiten"):
        return "d5.definition", "five_leefgebieden", "definition"

    if contains_any(
        normalized,
        "sociaal verwijzen",
        "valpreventie",
        "welzijn op recept",
        "kansrijke start",
        "aanpak overgewicht",
        "gecombineerde leefstijlinterventie",
    ):
        if contains_any(normalized, "ontwikkelagenda", "doorontwikkeld tot een basisfunctionaliteit"):
            return "d5.ontwikkelagenda", "underbouwd_and_development_split", "development_commitment"
        return "d5.basisfunctionaliteiten_onderbouwd", "sociaal_verwijzen_and_valpreventie", "implementation_commitment"

    if contains_any(
        normalized,
        "workagenda",
        "workagendas",
        "gereedschapskist",
        "werkagenda",
        "regioscan",
        "landelijke handreikingen",
        "regioplan",
    ):
        return "d5.regional_workagenda", "regional_translation", "implementation_requirement"

    if contains_any(
        normalized,
        "regional monitor",
        "content update",
        "structural financing conditions",
        "integrale monitor",
        "doorontwikkeling van de monitoring",
    ):
        return "d5.implementation_enablers", "funding_monitoring_update_cycle", "implementation_commitment"

    if contains_any(
        normalized,
        "mentale gezondheidsnetwerken",
        "verkennend gesprek",
        "mentale gezondheidscentra",
        "mentale klachten",
    ):
        return "d5.mentale_gezondheidsnetwerken", "mental_health_networks", "implementation_commitment"

    if contains_any(
        normalized,
        "goal",
        "equal access",
        "gelijkwaardiger toegankelijk",
        "verbinding tussen het medisch en sociaal domein",
        "samenwerking sociaal domein",
        "domeinoverstijgend",
        "beweging naar de voorkant",
        "passende zorg op de juiste plek",
        "sociale basis",
    ):
        if contains_any(normalized, "gezondheid voorop", "preventie", "positieve gezondheid"):
            return "d5.health_first_shift", "prevention_first", "definition"
        return "d5.cross_domain_collaboration", "care_social_cooperation_goal", "definition"

    if contains_any(normalized, "gezonde leefstijl", "gezondheidsachterstanden", "mentale gezondheid"):
        return "d5.definition", "care_social_cooperation_goal", "definition"

    return "d5.other", "uncategorized", "implementation_requirement"


def classify_d6(document_id: str, statement: str) -> tuple[str, str, str]:
    normalized = normalize_text(statement)

    if contains_any(
        normalized,
        "rtp",
        "regionaal transferpunt",
        "rso",
        "data infrastructure",
        "data-infrastructuur",
        "digitale infrastructuur",
        "digital infrastructure",
        "digitale gegevensuitwisselingsorganisatie",
        "information picture",
        "actueel informatiebeeld",
        "monitoring@home",
        "digitale lotgenotengroepen",
        "e-health",
    ):
        return "d6.digital_and_operational_infrastructure", "data_and_transfer_infrastructure", "implementation_condition"

    if contains_any(
        normalized,
        "inloopvoorzieningen",
        "basisinfrastructuur",
        "basis in wijk",
        "basisvoorzieningen in wijken en buurten",
        "sociale infrastructuur",
        "lokale sociale basis",
        "laagdrempelige steunpunten",
        "dekkend netwerk van laagdrempelige steunpunten",
    ):
        if contains_any(normalized, "goal", "framed", "gaat over", "vereist"):
            return "d6.basisinfrastructuur", "wijk_en_regio_basis", "definition"
        return "d6.basisinfrastructuur", "wijk_en_regio_basis", "implementation_requirement"

    if contains_any(
        normalized,
        "local teams",
        "hechte wijkverbanden",
        "lokale teams",
        "stevige lokale teams",
        "sociaal wijkteam",
        "wijkverbanden",
    ):
        return "d6.local_teams", "wijkverbanden", "implementation_requirement"

    if contains_any(
        normalized,
        "ggd",
        "regional structure",
        "regionale infrastructuur",
        "regionale preventie-infrastructuur",
        "regiobeeld",
        "regioplan",
    ):
        return "d6.regional_coordination", "ggd_and_regional_coordination", "implementation_requirement"

    return "d6.other", "uncategorized", "implementation_requirement"


def classify_governance_and_finance(document_id: str, statement: str) -> tuple[str, str, str]:
    normalized = normalize_text(statement)

    if contains_any(
        normalized,
        "financieringsvorm",
        "financiele-verhoudingswet",
        "fund managers",
        "brede spuk",
        "spuk iza",
        "specifieke uitkering",
        "spuk",
    ):
        return "finance.d5_d6.funding_instrument", "municipal_channel", "funding_channel"

    if contains_any(normalized, "doorbraakmiddelen"):
        return "finance.d5_d6.municipal_funding", "doorbraakmiddelen", "funding_commitment"

    if contains_any(normalized, "start package", "startpakket"):
        return "finance.d5_d6.municipal_funding", "startpakket_2027_2028", "funding_commitment"

    if contains_any(
        normalized,
        "spuk gala",
        "spuk iza",
        "transformatiemiddelen",
        "transformatiegelden",
        "concrete budgets",
        "middelen beschikbaar",
        "middelen worden verstrekt",
    ):
        return "finance.regional_funding_path", "spuk_and_transformation_funding", "funding_path"

    if contains_any(
        normalized,
        "multi-year funding horizon",
        "financial framework already runs through 2028",
        "phased financing horizon",
        "sectoral growth",
        "budgetary agreements leading",
        "financieel arrangement",
        "budgettaire afspraken",
    ):
        return "finance.azwa_macro_framework", "multi_year_horizon", "financial_framework"

    if contains_any(normalized, "businesscase", "besparing", "netto besparingen", "structurele besparingen"):
        return "finance.local_alignment_goal", "businesscase_and_accessibility", "local_goal"

    if contains_any(normalized, "verbindende coalitie", "workgroups", "expert team", "mandaathouder", "mandaatstructuur"):
        return "governance.regional_coordination", "flevoland_transformation_governance", "governance_arrangement"

    if contains_any(
        normalized,
        "broad local coalition",
        "broad local coalition of almere municipality",
        "zorg- en welzijnsorganisaties in almere en de gemeente",
        "brede samenwerking tussen",
    ):
        return "governance.local_coalition", "almere_transformation_coalition", "governance_arrangement"

    if contains_any(normalized, "bestuurlijke afspraak", "bestuurlijke afspraken", "bestuurlijk overleg", "motie"):
        return "governance.national_coordination", "bestuurlijke_afspraken", "governance_arrangement"

    if contains_any(normalized, "future balance", "better aligned", "betere balans", "passend aanbod", "toegankelijkheid"):
        return "finance.local_alignment_goal", "almere_balance", "local_goal"

    return "governance_and_finance.other", "uncategorized", "governance_arrangement"


def classify_timeline(document_id: str, statement: str) -> tuple[str, str, str]:
    normalized = normalize_text(statement)

    if document_id == "mun_almere_raad_vergaderschema_2026" and contains_any(
        normalized,
        "politieke markt",
        "gemeenteraadsverkiezingen",
        "benoeming raad",
        "afscheid raad",
        "besluitvorming",
    ):
        return "timeline.local_governance_calendar", "almere_council_milestones", "local_calendar_milestone"

    if contains_any(
        normalized,
        "q4 2025",
        "q1 2026",
        "q2 2026",
        "q3 2026",
        "voorjaar",
        "landelijke handreikingen",
        "eerste kwartaal",
        "tweede kwartaal",
        "derde kwartaal",
        "vierde kwartaal",
    ):
        return "timeline.d5_d6_implementation", "national_milestones", "timeline_commitment"

    if "2030" in normalized:
        return "timeline.rollout_2030", "landelijke_dekking", "timeline_commitment"

    if contains_any(
        normalized,
        "2026 to 2031",
        "2026 through 2031",
        "phased financing horizon",
        "tot en met 2026",
        "na 2026",
        "tot en met 2028",
    ):
        return "timeline.d5_d6_financing_horizon", "funding_window_2026_2031", "timeline_commitment"

    if "2029" in normalized:
        return "timeline.almere_2029", "local_impact_horizon", "timeline_commitment"

    if contains_any(
        normalized,
        "first and second quarter of 2024",
        "end of the second quarter",
        "definite transformatieagenda",
        "herijken",
        "vijfjaarlijks",
    ):
        return "timeline.flevoland_transformatieagenda", "q2_2024", "timeline_commitment"

    if contains_any(normalized, "ongoing implementation status", "transformation rather than a standalone project", "uitvoering in gang"):
        return "timeline.implementation_status", "ongoing_transformation", "status_assessment"

    return "timeline.other", "uncategorized", "timeline_commitment"


def classify_monitoring(document_id: str, statement: str) -> tuple[str, str, str]:
    normalized = normalize_text(statement)

    if contains_any(normalized, "impact goals", "reach by 2029", "impact in 2029", "kritische prestatie-indicatoren", "kpi"):
        return "monitoring.local_goal_tracking", "almere_2029_goals", "monitoring_commitment"

    if contains_any(normalized, "mid-term review", "mtr", "tussentijds evaluatiemoment"):
        return "monitoring.mid_term_review", "mtr_2027", "monitoring_commitment"

    if contains_any(normalized, "updated in 2028", "updated in 2028 based on monitoring and evaluation", "in 2028 te herijken"):
        return "monitoring.update_2028", "content_refresh", "monitoring_commitment"

    if contains_any(
        normalized,
        "three levels",
        "process-output-outcome",
        "process, output, and outcome",
        "proces, beweging",
        "doelgroepen",
        "monitoren van doelen en effecten",
    ):
        return "monitoring.framework", "process_output_outcome", "monitoring_framework"

    if contains_any(normalized, "mechanism and implementation will be monitored", "regioscan", "geintegreerde monitor"):
        return "monitoring.d5_operational_monitoring", "implementation_adjustment", "monitoring_commitment"

    if contains_any(normalized, "dashboard", "2024 monitoringsplan", "venster op de regionale samenwerking", "interactief dashboard"):
        return "monitoring.regional_monitoring_plan", "dashboard_and_existing_data", "monitoring_framework"

    if contains_any(normalized, "samen leren", "monitoring and learning", "lerende evaluaties", "monitoringsysteem"):
        return "monitoring.local_learning", "almere_learning_cycle", "monitoring_framework"

    if contains_any(
        normalized,
        "iza-based azwa monitoring",
        "broader iza-based azwa monitoring and evaluation framework",
        "aansluiting bij de azwa-afspraken",
    ):
        return "monitoring.framework", "iza_linkage", "monitoring_framework"

    return "monitoring.other", "uncategorized", "monitoring_commitment"


def classify_municipal_translation(document_id: str, statement: str) -> tuple[str, str, str]:
    normalized = normalize_text(statement)

    if document_id in {"mun_almere_pga_transformatieplan", "mun_almere_pga_seo_businesscase_2024"}:
        if contains_any(
            normalized,
            "voorzorgcirkels",
            "welzijn op recept",
            "leefstijlloket",
            "kansrijke omgeving",
            "samen sterker in de wijk",
            "monitoring@home",
            "rtp almere",
        ):
            return "municipal.almere_initiatives", "named_local_initiatives", "local_implementation"
        return "municipal.almere_context", "local_pressure_profile", "local_context"

    if contains_any(normalized, "roles and responsibilities", "rolverdeling", "mandaathouder", "aanspreekbaar"):
        return "municipal.role_allocation", "implementation_responsibility", "governance_requirement"

    if contains_any(
        normalized,
        "local teams",
        "neighbourhood-level voorzieningen",
        "lokale teams",
        "wijkteams",
        "lokale inzet",
        "regionale en lokale inzet",
    ):
        return "municipal.local_structure", "d6_local_delivery", "implementation_requirement"

    if contains_any(
        normalized,
        "local tailoring",
        "local needs",
        "lokale plannen",
        "regioplan",
        "gemeenten",
        "gemeenteraad",
        "almere",
        "zorgverzekeraars en gemeenten",
    ):
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


def build_claim(
    item: dict,
    document_payload: dict,
    section_name: str,
    instrument_type: str,
    authority_weight: float,
    instrument_profile: dict,
) -> dict:
    statement = item["statement"]
    topic, subtopic, claim_type = classify_claim(document_payload["document_id"], section_name, statement)
    metadata = document_payload["metadata"]
    source_statement_type = item.get("statement_type", "direct_extraction")
    return {
        "claim_id": claim_id_for(item["statement_id"]),
        "topic": topic,
        "subtopic": subtopic,
        "claim_type": claim_type,
        "normative_status": normative_status_for(
            statement, instrument_type, instrument_profile, source_statement_type, topic
        ),
        "time_status": time_status_for(
            statement, document_payload["document_id"], instrument_type, source_statement_type, topic, claim_type
        ),
        "money_status": money_status_for(
            statement, document_payload["document_id"], instrument_type, source_statement_type, topic, claim_type
        ),
        "governance_status": governance_status_for(
            statement, document_payload["document_id"], instrument_type, source_statement_type, topic, claim_type
        ),
        "locality_status": locality_status_for(
            statement, document_payload["document_id"], metadata["jurisdiction_level"], source_statement_type, topic
        ),
        "execution_status": execution_status_for(
            statement, document_payload["document_id"], source_statement_type, topic, claim_type
        ),
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
        "validity_status": validity_status_for(metadata, source_statement_type),
        "applies_to": applies_to_for(document_payload["document_id"]),
        "confidence": confidence_for(metadata["jurisdiction_level"], source_statement_type, topic, instrument_type),
        "human_review_status": human_review_status_for(source_statement_type, topic, instrument_type),
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
            claims.append(
                build_claim(
                    item,
                    document_payload,
                    section_name,
                    instrument_type,
                    authority_weight,
                    instrument_profiles[instrument_type],
                )
            )
    return claims


def apply_sentence_boundary_gate(claims_by_document: dict[str, list[dict]]) -> tuple[dict[str, list[dict]], dict]:
    filtered: dict[str, list[dict]] = {}
    rejected: list[dict] = []
    reviewed: list[dict] = []

    for document_id, claims in claims_by_document.items():
        kept_claims: list[dict] = []
        for claim in claims:
            reject, reasons = should_reject_for_sentence_boundary(claim["statement"])
            if reject:
                rejected.append(
                    {
                        "claim_id": claim["claim_id"],
                        "source_document_id": claim["source_document_id"],
                        "topic": claim["topic"],
                        "subtopic": claim["subtopic"],
                        "reasons": reasons,
                        "statement": claim["statement"],
                        "source_statement_ids": claim["source_location"]["source_statement_ids"],
                    }
                )
                continue
            if reasons:
                reviewed.append(
                    {
                        "claim_id": claim["claim_id"],
                        "source_document_id": claim["source_document_id"],
                        "topic": claim["topic"],
                        "subtopic": claim["subtopic"],
                        "reasons": reasons,
                        "statement": claim["statement"],
                        "source_statement_ids": claim["source_location"]["source_statement_ids"],
                    }
                )
            kept_claims.append(claim)
        filtered[document_id] = kept_claims

    log = {
        "generated_on": date.today().isoformat(),
        "run_id": f"{CLAIM_EXTRACTION_RUN_ID}_sentence_boundary_gate",
        "policy": {
            "rejected": [
                "Claims starting with a lowercase word outside the standard Dutch article/preposition whitelist.",
                "Short or heading-like claims missing terminal sentence punctuation.",
            ],
            "review_only": [
                "Longer claims missing terminal sentence punctuation are retained but logged for later cleanup.",
            ],
        },
        "input_claim_count": sum(len(claims) for claims in claims_by_document.values()),
        "kept_claim_count": sum(len(claims) for claims in filtered.values()),
        "rejected_claim_count": len(rejected),
        "review_only_count": len(reviewed),
        "rejected_claims": rejected,
        "review_only_claims": reviewed,
    }
    return filtered, log


def apply_claim_dedup(claims_by_document: dict[str, list[dict]]) -> tuple[dict[str, list[dict]], dict]:
    groups: dict[tuple[str, str, str, str], list[dict]] = {}
    for claims in claims_by_document.values():
        for claim in claims:
            key = (
                claim["source_document_id"],
                claim["topic"],
                claim["subtopic"],
                normalized_statement_prefix(claim["statement"]),
            )
            groups.setdefault(key, []).append(claim)

    winner_ids: set[str] = set()
    loser_ids: set[str] = set()
    entries: list[dict] = []

    for key, group_claims in groups.items():
        if len(group_claims) == 1:
            winner_ids.add(group_claims[0]["claim_id"])
            continue
        ranked = sorted(group_claims, key=lambda claim: (-len(claim["statement"]), claim["claim_id"]))
        winner = ranked[0]
        losers = ranked[1:]
        winner_ids.add(winner["claim_id"])
        loser_ids.update(claim["claim_id"] for claim in losers)
        entries.append(
            {
                "source_document_id": key[0],
                "topic": key[1],
                "subtopic": key[2],
                "normalized_prefix": key[3],
                "winning_claim_id": winner["claim_id"],
                "winning_statement_length": len(winner["statement"]),
                "superseded_claims": [
                    {
                        "claim_id": claim["claim_id"],
                        "statement_length": len(claim["statement"]),
                        "statement": claim["statement"],
                    }
                    for claim in losers
                ],
            }
        )

    filtered: dict[str, list[dict]] = {}
    for document_id, claims in claims_by_document.items():
        filtered[document_id] = [claim for claim in claims if claim["claim_id"] not in loser_ids]

    log = {
        "generated_on": date.today().isoformat(),
        "run_id": f"{CLAIM_EXTRACTION_RUN_ID}_dedup",
        "grouping": ["source_document_id", "topic", "subtopic", "first_200_normalized_statement_chars"],
        "input_claim_count": sum(len(claims) for claims in claims_by_document.values()),
        "kept_claim_count": sum(len(claims) for claims in filtered.values()),
        "dedup_group_count": len(entries),
        "superseded_claim_count": len(loser_ids),
        "entries": entries,
    }
    return filtered, log


def prune_missing_relation_targets(claims_by_document: dict[str, list[dict]]) -> None:
    claim_ids = {claim["claim_id"] for claims in claims_by_document.values() for claim in claims}
    for claims in claims_by_document.values():
        for claim in claims:
            claim["relations"] = [
                relation
                for relation in claim["relations"]
                if relation["target_claim_id"] in claim_ids
            ]


def validate_claims(claims: list[dict], allowed_relation_types: set[str]) -> None:
    required_fields = {
        "claim_id",
        "topic",
        "subtopic",
        "claim_type",
        "normative_status",
        "time_status",
        "money_status",
        "governance_status",
        "locality_status",
        "execution_status",
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


def write_outputs(document_ids: list[str], claims_by_document: dict[str, list[dict]], source_runs: dict[str, str]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    master_path = OUTPUT_DIR / "claims_master.jsonl"
    with master_path.open("w", encoding="utf-8") as handle:
        for document_id in document_ids:
            for claim in claims_by_document[document_id]:
                handle.write(json.dumps(claim, ensure_ascii=False) + "\n")

    for document_id in document_ids:
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


def write_claim_quality_logs(sentence_log: dict, dedup_log: dict) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SENTENCE_VALIDATOR_REJECTS_PATH.write_text(
        json.dumps(sentence_log, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    DEDUP_LOG_PATH.write_text(
        json.dumps(dedup_log, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {SENTENCE_VALIDATOR_REJECTS_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"Wrote {DEDUP_LOG_PATH.relative_to(REPO_ROOT).as_posix()}")


def main() -> None:
    authority_map, instrument_profiles = load_authority_model()
    allowed_relation_types = load_allowed_relation_types()
    relations_by_claim_id = relation_specs()
    document_ids = load_document_ids()

    claims_by_document: dict[str, list[dict]] = {}
    source_runs: dict[str, str] = {}

    for document_id in document_ids:
        document_payload = load_document(document_id)
        source_runs[document_id] = document_payload["extraction_run_id"]
        document_claims = build_document_claims(document_id, authority_map, instrument_profiles)
        for claim in document_claims:
            claim["relations"] = relations_by_claim_id.get(claim["claim_id"], [])
        claims_by_document[document_id] = document_claims

    claims_by_document, sentence_log = apply_sentence_boundary_gate(claims_by_document)
    claims_by_document, dedup_log = apply_claim_dedup(claims_by_document)
    prune_missing_relation_targets(claims_by_document)

    all_claims = [claim for document_id in document_ids for claim in claims_by_document[document_id]]
    validate_claims(all_claims, allowed_relation_types)
    write_outputs(document_ids, claims_by_document, source_runs)
    write_claim_quality_logs(sentence_log, dedup_log)


if __name__ == "__main__":
    main()
