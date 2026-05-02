from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKAGENDA_DIR = REPO_ROOT / "data" / "workagenda"
PACKET_DIR = WORKAGENDA_DIR / "validation_packets"
DOCS_DIR = REPO_ROOT / "docs"

TICKETS_PATH = WORKAGENDA_DIR / "d5_validation_tickets.json"
OUTPUT_JSON_PATH = WORKAGENDA_DIR / "d5_validation_packets.json"
OUTPUT_MD_PATH = DOCS_DIR / "workagenda-d5-validation-format.md"


PACKET_RULES = [
    (
        "finance_controller",
        "finance_controller",
        "Finance/controller en zorgverzekeraar",
        "Funding line, structural/project status, double-counting risk and insurer/Zvw confirmation.",
    ),
    (
        "d6_dependency",
        "d6_dependency",
        "D6-afhankelijkheden",
        "D6 preconditions needed for D5 execution.",
    ),
    (
        "decision_phasing",
        "decision_phasing",
        "Besluitvorming en fasering",
        "Decision owner, phasing toward 2027-2030 and governance escalation.",
    ),
    (
        "zorgverzekeraar",
        "component_packet_contains",
        "Zorgverzekeraar / Zvw",
        "Zvw, contracting, insurer role and care-professional funding questions.",
    ),
    (
        "jgz_ggd",
        "component_packet_contains",
        "JGZ / GGD Flevoland",
        "JGZ, GGD, prevention, monitoring and public-health role validation.",
    ),
    (
        "gemeente_sociaal_domein",
        "fallback_policy",
        "Gemeente Almere beleid en sociaal domein",
        "Local status, capacity, ownership, local coverage and social-domain implementation.",
    ),
]


CSV_COLUMNS = [
    "ticket_id",
    "component",
    "ticket_type",
    "current_working_view",
    "question",
    "choice_sets",
    "answer",
    "correction_or_note",
    "evidence_type",
    "evidence_path_or_document",
    "evidence_gate",
    "default_if_no_evidence",
    "status_matrix_effect",
    "escalation_trigger",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower())
    return slug.strip("_")


def packet_for_ticket(ticket: dict[str, Any]) -> str:
    ticket_type = ticket["ticket_type"]
    packet = ticket["stakeholder_packet"].lower()
    if ticket_type in {"finance_controller", "d6_dependency", "decision_phasing"}:
        return ticket_type
    if "zorgverzekeraar" in packet:
        return "zorgverzekeraar"
    if "jgz" in packet or "ggd" in packet:
        return "jgz_ggd"
    return "gemeente_sociaal_domein"


def packet_metadata(packet_id: str) -> dict[str, str]:
    for rule_id, _rule_type, title, purpose in PACKET_RULES:
        if rule_id == packet_id:
            return {"packet_id": packet_id, "title": title, "purpose": purpose}
    return {"packet_id": packet_id, "title": packet_id, "purpose": "Validation packet."}


def build_packets() -> dict[str, Any]:
    ticket_set = load_json(TICKETS_PATH)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for ticket in ticket_set["tickets"]:
        grouped[packet_for_ticket(ticket)].append(ticket)

    packet_rows = []
    for packet_id in sorted(grouped):
        metadata = packet_metadata(packet_id)
        tickets = grouped[packet_id]
        packet_rows.append(
            {
                **metadata,
                "ticket_count": len(tickets),
                "ticket_ids": [ticket["ticket_id"] for ticket in tickets],
                "component_count": len({ticket["target_id"] for ticket in tickets}),
                "ticket_type_counts": dict(sorted(Counter(ticket["ticket_type"] for ticket in tickets).items())),
                "csv_path": f"data/workagenda/validation_packets/{slugify(metadata['title'])}.csv",
            }
        )

    return {
        "packet_set_id": "workagenda_d5_validation_packets_v1",
        "generated_on": date.today().isoformat(),
        "sprint": "32.2 D5-validatie voorbereiden",
        "status": "stakeholder_packet_format",
        "purpose": "Stakeholder packet layer derived from constrained D5 validation tickets. These packet CSVs can be opened as spreadsheet forms or converted to Excel/form tooling.",
        "source_layers": ["data/workagenda/d5_validation_tickets.json"],
        "guardrails": [
            "Packets are validation forms, not completed validation records.",
            "Blank answer fields mean unresolved; do not fill them by inference.",
            "Evidence path or document reference is required before using answers to change statusmatrix fields.",
        ],
        "csv_columns": CSV_COLUMNS,
        "summary": {
            "packet_count": len(packet_rows),
            "ticket_count": sum(packet["ticket_count"] for packet in packet_rows),
            "component_count": len({ticket["target_id"] for ticket in ticket_set["tickets"]}),
        },
        "packets": packet_rows,
    }


def write_packet_csvs(ticket_set: dict[str, Any], packet_set: dict[str, Any]) -> None:
    PACKET_DIR.mkdir(parents=True, exist_ok=True)
    ticket_by_id = {ticket["ticket_id"]: ticket for ticket in ticket_set["tickets"]}
    for packet in packet_set["packets"]:
        csv_path = REPO_ROOT / packet["csv_path"]
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
            writer.writeheader()
            for ticket_id in packet["ticket_ids"]:
                ticket = ticket_by_id[ticket_id]
                writer.writerow(
                    {
                        "ticket_id": ticket["ticket_id"],
                        "component": ticket["component"],
                        "ticket_type": ticket["ticket_type"],
                        "current_working_view": ticket["current_working_view"],
                        "question": ticket["question"],
                        "choice_sets": "; ".join(ticket["choice_sets"]),
                        "answer": "",
                        "correction_or_note": "",
                        "evidence_type": "",
                        "evidence_path_or_document": "",
                        "evidence_gate": ticket["evidence_gate"],
                        "default_if_no_evidence": ticket["default_if_no_evidence"],
                        "status_matrix_effect": ticket["status_matrix_effect"],
                        "escalation_trigger": ticket["escalation_trigger"],
                    }
                )


def render_markdown(packet_set: dict[str, Any]) -> str:
    lines = [
        "# Werkagenda D5 validation format",
        "",
        "## Summary",
        "Current sprint: Sprint 32.2 - D5-validatie voorbereiden.",
        "",
        "This is the practical handoff format for D5 validation. It groups the constrained ticket set into stakeholder packets and writes CSV forms that can be opened as spreadsheets or converted into Excel/form tooling.",
        "",
        "Machine-readable packet index: `data/workagenda/d5_validation_packets.json`.",
        "",
        "## How To Use",
        "",
        "Send only the relevant packet to each stakeholder group. Ask them to fill `answer`, add a short correction if needed, choose or name the evidence type, and provide an evidence path or document reference. Blank answers remain unresolved.",
        "",
        "## Packet Overview",
        "",
        "| Packet | Purpose | Tickets | CSV form |",
        "| --- | --- | ---: | --- |",
    ]
    for packet in packet_set["packets"]:
        lines.append(
            f"| {packet['title']} | {packet['purpose']} | {packet['ticket_count']} | `{packet['csv_path']}` |"
        )

    lines.extend(
        [
            "",
            "## Completion Rule",
            "",
            "Sprint 32.2 is repository-side complete when these packet forms exist, remain constrained, and keep evidence gates visible. Sprint 32.3 remains blocked until completed stakeholder answers or explicit policy decisions are available.",
            "",
            "## Guardrails",
            "",
            "- These packet forms are not validation results.",
            "- Do not fill blank answers from repository inference.",
            "- Do not use finance, governance or D6 dependency answers unless evidence is recorded.",
            "- Keep unresolved answers as validation, finance, decision or dependency tickets.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    ticket_set = load_json(TICKETS_PATH)
    packet_set = build_packets()
    write_packet_csvs(ticket_set, packet_set)
    OUTPUT_JSON_PATH.write_text(json.dumps(packet_set, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUTPUT_MD_PATH.write_text(render_markdown(packet_set), encoding="utf-8")


if __name__ == "__main__":
    main()
