from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKAGENDA_DIR = REPO_ROOT / "data" / "workagenda"
DOCS_DIR = REPO_ROOT / "docs"

STATUS_MATRIX_PATH = WORKAGENDA_DIR / "d5_status_matrix.json"
OUTPUT_JSON_PATH = WORKAGENDA_DIR / "d5_validation_tickets.json"
OUTPUT_MD_PATH = DOCS_DIR / "workagenda-d5-validation-tickets.md"


STANDARD_CHOICES = {
    "local_status": [
        "Bestaat al en is structureel",
        "Bestaat als project/pilot",
        "Bestaat deels",
        "In voorbereiding",
        "Niet aanwezig",
        "Onbekend",
        "Anders, toelichten",
    ],
    "coverage": [
        "Regionaal dekkend",
        "Almere-dekkend",
        "Deels dekkend",
        "Wijk- of locatiegebonden",
        "Alleen pilotgebied",
        "Onbekend",
        "Anders, toelichten",
    ],
    "role": [
        "Opdrachtgever/eigenaar",
        "Coordinator",
        "Uitvoerder",
        "Partner",
        "Financier",
        "Adviseur/monitoring",
        "Geen formele rol",
        "Onbekend",
        "Anders, toelichten",
    ],
    "finance": [
        "Gemeentelijke middelen",
        "AZWA-D5",
        "Doorbraakmiddelen sociaal domein",
        "SPUK/GALA",
        "Zvw/zorgverzekeraar",
        "Reguliere organisatiebekostiging",
        "Projectsubsidie",
        "Gemengd, uitsplitsing nodig",
        "Geen financiering besloten",
        "Onbekend",
        "Anders, toelichten",
    ],
    "continuity": [
        "Structureel geborgd",
        "Tijdelijk/projectmatig",
        "Deels structureel, deels tijdelijk",
        "Continuiteitsbesluit nodig",
        "Onbekend",
        "Anders, toelichten",
    ],
    "d6_dependency": [
        "Niet nodig",
        "Mogelijke afhankelijkheid",
        "Bevestigde afhankelijkheid",
        "Kritieke blokkade",
        "Nog te valideren",
        "Onbekend",
        "Anders, toelichten",
    ],
    "scope_choice": [
        "Opnemen in werkagenda",
        "Niet opnemen",
        "Alleen volgen als ontwikkelagenda-optie",
        "Wachten op landelijke handreiking",
        "Besluit nodig",
        "Onbekend",
        "Anders, toelichten",
    ],
    "evidence": [
        "Formeel besluit",
        "Begrotingsregel of controllerbevestiging",
        "Uitvoeringsplan",
        "Samenwerkingsafspraak",
        "Contract/inkoopafspraak",
        "Stakeholderbevestiging",
        "Publieke bron",
        "Geen bewijs beschikbaar",
        "Anders, toelichten",
    ],
}


PACKET_BY_TARGET = {
    "laagdrempelige_steunpunten": "Gemeente Almere sociaal domein / welzijn en sociale basis",
    "sociaal_verwijzen": "Gemeente Almere sociaal domein / eerstelijn / welzijn",
    "mentale_gezondheidsnetwerken": "GGZ/MGN / zorgverzekeraar / sociaal domein",
    "valpreventie": "Gemeente Almere preventie / GGD / beweegaanbieders",
    "ketenaanpak_overgewicht_obesitas_volwassenen": "Gemeente Almere preventie / zorgverzekeraar / leefstijlpartners",
    "kansrijke_start": "Gemeente Almere / JGZ-GGD / geboortezorg-VSV",
    "integrale_gezinspoli": "Gemeente Almere / VSV-geboortezorg / Flevoziekenhuis / zorgverzekeraar",
    "nu_niet_zwanger": "GGD-JGZ / Gemeente Almere / regionale governance",
    "ketenaanpak_overgewicht_obesitas_kinderen": "Gemeente Almere / JGZ-GGD / onderwijs / zorgverzekeraar",
    "ontwikkelagenda_1_nieuw_beproeven": "IZA/AZWA governance / Gemeente Almere / zorgverzekeraar",
    "ontwikkelagenda_2_overige_initiatieven": "IZA/AZWA governance / Gemeente Almere",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def current_working_view(row: dict[str, Any]) -> str:
    evidence = row.get("public_evidence", [])
    if evidence:
        return " ".join(evidence)
    if not row.get("required_in_workagenda"):
        return "This item is optional or conditional until the region chooses to include it."
    return "Public sources identify this as a D5 workagenda target, but filling for gemeente Almere and, where relevant, IZA/AZWA-regio Flevoland still needs validation."


def ticket(
    row: dict[str, Any],
    ticket_type: str,
    question: str,
    choice_sets: list[str],
    evidence_gate: str,
    default_if_no_evidence: str,
    status_matrix_effect: str,
    escalation_trigger: str,
    packet: str | None = None,
) -> dict[str, Any]:
    ticket_id = f"{row['target_id']}__{ticket_type}"
    return {
        "ticket_id": ticket_id,
        "target_id": row["target_id"],
        "component": row["title"],
        "ticket_type": ticket_type,
        "stakeholder_packet": packet or PACKET_BY_TARGET.get(row["target_id"], "Nog te bepalen"),
        "current_working_view": current_working_view(row),
        "question": question,
        "choice_sets": choice_sets,
        "answer_options": {name: STANDARD_CHOICES[name] for name in choice_sets},
        "evidence_options": STANDARD_CHOICES["evidence"],
        "evidence_gate": evidence_gate,
        "default_if_no_evidence": default_if_no_evidence,
        "status_matrix_effect": status_matrix_effect,
        "escalation_trigger": escalation_trigger,
        "source_status": {
            "public_foundation": row["public_foundation"],
            "risk": row["risk"],
            "public_indicator_count": row["public_indicator_count"],
            "indicative_calculation_count": row["indicative_calculation_count"],
        },
    }


def tickets_for_required_row(row: dict[str, Any]) -> list[dict[str, Any]]:
    component = row["title"]
    owner_packet = PACKET_BY_TARGET.get(row["target_id"], "Nog te bepalen")
    return [
        ticket(
            row,
            "local_status_capacity",
            f"Wat is de actuele lokale invulling, dekking en capaciteit voor {component}?",
            ["local_status", "coverage", "continuity"],
            "Uitvoeringsplan, samenwerkingsafspraak, publieke bron plus stakeholderbevestiging, of validatie door verantwoordelijke organisatie.",
            "Keep current and capacity fields as validation-needed; do not draft as confirmed.",
            "May move huidige_situatie/aantallen_capaciteit from validation-needed to confirmed concept if evidence is complete.",
            "Capacity unknown, coverage conflict, or no accountable respondent.",
            owner_packet,
        ),
        ticket(
            row,
            "governance_roles",
            f"Wie is eigenaar, coordinator, uitvoerder en partner voor {component}?",
            ["role"],
            "Mandaat, samenwerkingsafspraak, uitvoeringsplan of expliciete stakeholderbevestiging.",
            "Keep governance as owner unknown/local validation needed.",
            "May update governance fields only for roles supported by evidence.",
            "No owner, conflicting owners, unclear mandate or unclear relation between local and regional scale.",
            owner_packet,
        ),
        ticket(
            row,
            "finance_controller",
            f"Welke financiering geldt voor {component}, en is die structureel, tijdelijk of gemengd?",
            ["finance", "continuity"],
            "Begrotingsregel, controllerbevestiging, verzekeraar/Zvw-bevestiging, contract/inkoopafspraak of formeel financieringsbesluit.",
            "Keep finance as controllercheck needed; do not write as funded.",
            "May move finance status from controllercheck needed to concept/confirmed only when funding line and continuity are evidenced.",
            "No funding line, double-counting risk, insurer role unclear or structural/project status unknown.",
            "Finance/controller / zorgverzekeraar waar relevant",
        ),
        ticket(
            row,
            "d6_dependency",
            f"Welke D6-infrastructuur is randvoorwaardelijk voor {component}?",
            ["d6_dependency"],
            "Validatierecord of expliciete afhankelijkheid in werkagenda-, uitvoerings-, governance- of D6-verantwoordelijkheidsbron.",
            "Keep D6 dependency as possible/needs validation.",
            "May mark dependency as confirmed, blocked, not needed or split by subdependency.",
            "D6 dependency is critical, unresolved, or conflicts with D6 responsibility overview.",
            "Gemeente Almere / D6 policy owner / relevant D6 partners",
        ),
        ticket(
            row,
            "decision_phasing",
            f"Welk besluit of welke fasering is nodig om {component} richting 2027-2030 op te nemen?",
            ["continuity"],
            "Besluitrecord, governancebesluit, planningsbevestiging of goedgekeurde faseringsnotitie.",
            "Keep decision/phasing as decision needed.",
            "May convert open decision into resolved decision, explicit risk or later milestone.",
            "No decision owner, no deadline before September 2026, or bestuurlijke wording risk.",
            "IZA/AZWA governance / Gemeente Almere / betrokken besluitnemer",
        ),
    ]


def tickets_for_optional_row(row: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        ticket(
            row,
            "scope_choice",
            f"Moet {row['title']} in de werkagenda voor gemeente Almere en, waar relevant, de IZA/AZWA-regio Flevoland worden opgenomen?",
            ["scope_choice"],
            "Explicit scope decision, governance confirmation or later national guidance.",
            "Keep item optional/not applicable and do not include in required workagenda text.",
            "May activate a normal validation-ticket set if the region chooses to include it.",
            "No scope owner, conflicting regional preference, or national guidance changes requirement.",
        )
    ]


def build_tickets() -> dict[str, Any]:
    matrix = load_json(STATUS_MATRIX_PATH)
    tickets: list[dict[str, Any]] = []
    for row in matrix["rows"]:
        if row["required_in_workagenda"]:
            tickets.extend(tickets_for_required_row(row))
        else:
            tickets.extend(tickets_for_optional_row(row))

    ticket_type_counts = Counter(ticket["ticket_type"] for ticket in tickets)
    packet_counts = Counter(ticket["stakeholder_packet"] for ticket in tickets)
    by_component = defaultdict(list)
    for ticket_item in tickets:
        by_component[ticket_item["target_id"]].append(ticket_item["ticket_id"])

    return {
        "ticket_set_id": "workagenda_d5_validation_tickets_v1",
        "generated_on": date.today().isoformat(),
        "sprint": "32.2 D5-validatie voorbereiden",
        "status": "initial_validation_ticket_set",
        "purpose": "Constrained validation tickets for D5 workagenda components. Stakeholders should confirm, correct, choose an option and provide evidence instead of doing open-ended research.",
        "source_layers": [
            "data/workagenda/d5_status_matrix.json",
            "data/workagenda/d5_stuurmodel.json",
            "data/extracted/workagenda_d5_operational_requirements.json",
            "data/extracted/workagenda_nulmeting_capacity.json",
        ],
        "guardrails": [
            "Tickets are validation prompts, not source claims.",
            "Do not fill stakeholder answers by repository inference.",
            "No D5 component becomes drafting-ready without evidence for local status, governance, finance, decision/phasing and D6 dependency handling.",
            "Finance and insurer/Zvw answers require finance/controller, contract, budget or insurer evidence.",
        ],
        "standard_choice_sets": STANDARD_CHOICES,
        "summary": {
            "ticket_count": len(tickets),
            "component_count": len(by_component),
            "ticket_type_counts": dict(sorted(ticket_type_counts.items())),
            "stakeholder_packet_counts": dict(sorted(packet_counts.items())),
        },
        "tickets_by_component": {key: value for key, value in sorted(by_component.items())},
        "tickets": tickets,
    }


def render_markdown(ticket_set: dict[str, Any]) -> str:
    lines = [
        "# Werkagenda D5 validation tickets v1",
        "",
        "## Summary",
        "Current sprint: Sprint 32.2 - D5-validatie voorbereiden.",
        "",
        "This file is the human-readable validation format for the D5 workagenda track. It does not validate the workagenda. It turns the statusmatrix into constrained tickets that stakeholders can answer by choosing, correcting and attaching evidence.",
        "",
        "Machine-readable version: `data/workagenda/d5_validation_tickets.json`.",
        "",
        "## How To Use",
        "",
        "Use the current working view as context only. For each ticket, choose the closest answer option, add a short correction if needed, and provide an evidence path or name the document/person/role that can provide it. If evidence is missing, keep the field unresolved.",
        "",
        "## Summary Counts",
        "",
        f"- Tickets: {ticket_set['summary']['ticket_count']}.",
        f"- Components: {ticket_set['summary']['component_count']}.",
        f"- Ticket types: {json.dumps(ticket_set['summary']['ticket_type_counts'], ensure_ascii=False)}.",
        "",
        "## Stakeholder Packets",
        "",
        "| Packet | Ticket count |",
        "| --- | ---: |",
    ]
    for packet, count in ticket_set["summary"]["stakeholder_packet_counts"].items():
        lines.append(f"| {packet} | {count} |")

    lines.extend(
        [
            "",
            "## Ticket Matrix",
            "",
            "| Component | Ticket type | Stakeholder packet | Question | Evidence gate |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for ticket_item in ticket_set["tickets"]:
        lines.append(
            "| {component} | `{ticket_type}` | {packet} | {question} | {gate} |".format(
                component=ticket_item["component"],
                ticket_type=ticket_item["ticket_type"],
                packet=ticket_item["stakeholder_packet"],
                question=ticket_item["question"],
                gate=ticket_item["evidence_gate"],
            )
        )

    lines.extend(
        [
            "",
            "## Standard Choice Sets",
            "",
        ]
    )
    for choice_set, options in ticket_set["standard_choice_sets"].items():
        lines.append(f"### {choice_set}")
        lines.append("")
        for option in options:
            lines.append(f"- {option}")
        lines.append("")

    lines.extend(
        [
            "## Guardrails",
            "",
            "- Tickets are validation prompts, not source claims.",
            "- Do not fill stakeholder answers by inference from repository data.",
            "- Keep finance/controller and insurer/Zvw confirmation separate from public-source hints.",
            "- Keep D6 dependencies visible as dependencies until validated or explicitly escalated.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    ticket_set = build_tickets()
    WORKAGENDA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON_PATH.write_text(json.dumps(ticket_set, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUTPUT_MD_PATH.write_text(render_markdown(ticket_set), encoding="utf-8")


if __name__ == "__main__":
    main()
