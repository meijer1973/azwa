from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACEABILITY_PATH = ROOT / "data" / "workagenda" / "validation_workbook_traceability_map.json"
PREFILL_AUDIT_PATH = ROOT / "data" / "workagenda" / "validation_workbook_prefill_audit.json"
OUTPUT_JSON_PATH = ROOT / "data" / "workagenda" / "precontact_stakeholder_packets.json"
OUTPUT_DOC_PATH = ROOT / "docs" / "review" / "precontact-stakeholder-packets.md"
OUTPUT_PACKET_DIR = ROOT / "data" / "workagenda" / "precontact_packets"


PACKET_DEFINITIONS: dict[str, dict[str, str]] = {
    "kernteam_werkagenda": {
        "label": "Kernteam werkagenda",
        "purpose": "Integratie, voortgangsbewaking en controle op alle pakketten.",
        "instruction": "Gebruik dit pakket voor interne sturing; stuur het niet als volledig validatiepakket naar externe stakeholders.",
        "contact_owner": "Kernteam werkagenda",
        "escalation_route": "Projectlead werkagenda",
    },
    "gemeente_almere_sociaal_domein": {
        "label": "Gemeente Almere beleid / sociaal domein",
        "purpose": "Lokale status, eigenaarschap, mandaat, prioritering, D6-relatie en veilige formulering.",
        "instruction": "Bevestig of corrigeer alleen onderdelen die onder gemeentelijk beleid, sociaal domein of lokale besluitvorming vallen.",
        "contact_owner": "Gemeente Almere beleidscontact",
        "escalation_route": "Projectlead werkagenda / beleidsowner",
    },
    "gemeente_almere_sociaal_domein_d5": {
        "label": "Gemeente Almere sociaal domein - D5 lokale invulling",
        "purpose": "D5 lokale status, aanbod, eigenaarschap, prioritering en veilige werkagenda-input.",
        "instruction": "Beantwoord alleen D5-invulling die onder gemeentelijk beleid of sociaal domein valt; verwijs finance-, Zvw- of regionale vragen door.",
        "contact_owner": "Gemeente Almere beleidscontact",
        "escalation_route": "Projectlead werkagenda / beleidsowner",
    },
    "gemeente_almere_sociaal_domein_sturing": {
        "label": "Gemeente Almere sociaal domein - sturing en afhankelijkheden",
        "purpose": "Governance, D5-D6-afhankelijkheden, optionele ontwikkelagenda en bestuurlijke sturing.",
        "instruction": "Gebruik dit pakket voor sturings- en besluitvoorbereiding; markeer punten die een apart besluit of andere eigenaar nodig hebben.",
        "contact_owner": "Gemeente Almere beleidscontact",
        "escalation_route": "Projectlead werkagenda / beleidsowner",
    },
    "gemeente_almere_sociaal_domein_d6": {
        "label": "Gemeente Almere sociaal domein - D6 validatie",
        "purpose": "D6-classificatie, lokale eigenaar, mandaat, veilige formulering en sociaal-domeinrelatie.",
        "instruction": "Bevestig of corrigeer D6-relatie en lokale rol; laat financiering of formele settlement staan als aparte evidence- of besluitvraag.",
        "contact_owner": "Gemeente Almere beleidscontact",
        "escalation_route": "Projectlead werkagenda / D6 beleidsowner",
    },
    "finance_controller": {
        "label": "Finance/controller",
        "purpose": "Financieringslijn, structureel/projectmatig karakter, dubbeltelling en controllerstatus.",
        "instruction": "Vul geen beleidsinhoud in; beperk antwoorden tot financiering, dekking, dubbeltelling, begrotingsregel en controllerbevestiging.",
        "contact_owner": "Finance/controller contact",
        "escalation_route": "Finance lead / projectlead werkagenda",
    },
    "ggd_jgz": {
        "label": "GGD/JGZ",
        "purpose": "JGZ/GGD-taaksplit, publieke gezondheid, preventie, monitoring, Kansrijke Start, NNZ, valpreventie en overgewicht kinderen.",
        "instruction": "Beantwoord taak-, schaal-, uitvoerings- en monitoringvragen; markeer gemeentelijke of financevragen als niet mijn domein.",
        "contact_owner": "GGD/JGZ contact",
        "escalation_route": "GGD/JGZ lead / projectlead werkagenda",
    },
    "zorgverzekeraar_zvw": {
        "label": "Zorgverzekeraar/Zvw",
        "purpose": "Zvw-rol, inkoop, contractering, GLI, CZV, MGN en inzet van zorgprofessionals.",
        "instruction": "Bevestig alleen Zvw-/verzekeraarsrollen, contractering, inkoop en zorgprofessionele inzet.",
        "contact_owner": "Zorgverzekeraar/Zvw contact",
        "escalation_route": "Regionale governance / projectlead werkagenda",
    },
    "welzijn_sociale_basis": {
        "label": "Welzijn en sociale basis",
        "purpose": "Laagdrempelige steunpunten, sociaal verwijzen, brugfunctie, informele steun en lokale uitvoering.",
        "instruction": "Bevestig bestaand aanbod, dekking, uitvoerders, routes en bewijsstukken; markeer besluit- of financevragen als niet mijn domein.",
        "contact_owner": "Welzijn/sociale-basis contact",
        "escalation_route": "Gemeente Almere sociaal domein",
    },
    "sociale_basis_partners": {
        "label": "Sociale-basis partners",
        "purpose": "Inloopvoorzieningen, informele steun, vrijwilligerswerk, mantelzorg en burgerinitiatieven.",
        "instruction": "Bevestig alleen concrete voorzieningen, mechanismen, partners, schaal en bewijs.",
        "contact_owner": "Sociale-basis partnercontact",
        "escalation_route": "Gemeente Almere sociaal domein",
    },
    "ggz_mgn_partners": {
        "label": "GGZ/MGN partners",
        "purpose": "Mentale gezondheidsnetwerken, verkennend gesprek, transfermechanisme, LSP-relatie en continuïteit.",
        "instruction": "Bevestig MGN-functies, uitvoeringsmodel, schaal en continuïteit; verwijs financiering door waar nodig.",
        "contact_owner": "GGZ/MGN contact",
        "escalation_route": "Regionale governance / projectlead werkagenda",
    },
    "vsv_geboortezorg_jgz": {
        "label": "VSV / geboortezorg / JGZ",
        "purpose": "Kansrijke Start, integrale gezinspoli, Nu Niet Zwanger en geboortezorgafspraken.",
        "instruction": "Bevestig coalitie, afspraken, uitvoering, privacy/casuïstiek en bewijsstukken binnen geboortezorg/JGZ-scope.",
        "contact_owner": "VSV/geboortezorg/JGZ contact",
        "escalation_route": "GGD/JGZ lead / projectlead werkagenda",
    },
    "regionale_governance": {
        "label": "Regionale governance",
        "purpose": "Regionale rolverdeling, governance, monitoring, D5/D6-samenhang en werkagenda-route.",
        "instruction": "Bevestig alleen regionale proces-, governance- en afstemmingsrollen; markeer lokale uitvoering of financevragen als niet mijn domein.",
        "contact_owner": "Regionale governance contact",
        "escalation_route": "Mandaatgemeente / projectlead werkagenda",
    },
    "ict_data_privacy": {
        "label": "ICT / data / privacy",
        "purpose": "Operationele eigenaar, data-/privacyverantwoordelijkheid, monitoring, dashboards en digitale infrastructuur.",
        "instruction": "Beantwoord alleen data-, privacy-, security-, dashboard- en operationele systeemverantwoordelijkheid.",
        "contact_owner": "ICT/data/privacy contact",
        "escalation_route": "ICT/privacy lead / projectlead werkagenda",
    },
    "d6_validation_owner": {
        "label": "D6 validatie-owner",
        "purpose": "D5-D6-afhankelijkheden en D6-randvoorwaarden bewaken.",
        "instruction": "Gebruik dit pakket om D6-afhankelijkheden te controleren; markeer formele D6-settlement als stakeholder-/beleidsbesluit.",
        "contact_owner": "D6 validation owner",
        "escalation_route": "Projectlead werkagenda / D6 beleidsowner",
    },
    "wijkteams_slt_leads": {
        "label": "Wijkteams / SLT-leads",
        "purpose": "Mandaat, dekking, uitvoeringsmodel en relatie tussen Wijkteams en Stevige Lokale Teams.",
        "instruction": "Bevestig operationele en governancevragen rond wijkteams en SLT; verwijs budgetvragen door naar finance/controller.",
        "contact_owner": "Wijkteams/SLT lead",
        "escalation_route": "Gemeente Almere sociaal domein",
    },
    "onderwijs_partners": {
        "label": "Onderwijs partners",
        "purpose": "Gezonde School, schoolwelzijn en onderwijsgerelateerde preventie.",
        "instruction": "Bevestig alleen school-/onderwijspraktijk, betrokken partners, schaal en bewijsstukken.",
        "contact_owner": "Onderwijscontact",
        "escalation_route": "Gemeente Almere / GGD/JGZ",
    },
    "wijkgerichte_ggz_welzijnspartners": {
        "label": "Wijkgerichte GGZ-/welzijnspartners",
        "purpose": "Samen Sterker in de Wijk, wijkgerichte mentale-gezondheidsinfrastructuur, schaal en continuïteit.",
        "instruction": "Bevestig actuele status, schaal, partners en bewijs; laat D6-classificatie en financiering expliciet als validatievraag staan.",
        "contact_owner": "Wijkgerichte GGZ-/welzijnscontact",
        "escalation_route": "Gemeente Almere / GGZ-MGN lead",
    },
    "pga_zorgzaam_flever_regionale_governance": {
        "label": "PGA / Zorgzaam / Flever / regionale governance",
        "purpose": "Actor-rolscheiding, lokaal/regionaal programma, participatieondersteuning en governance-interface.",
        "instruction": "Bevestig rol en schaal per actor; behandel eigenaarschap, mandaat en financiering als aparte validatie- of besluitvraag.",
        "contact_owner": "PGA/Zorgzaam/Flever contact",
        "escalation_route": "Regionale governance / projectlead werkagenda",
    },
}


def routed_packet_id(packet_id: str, row: dict[str, Any]) -> str:
    if packet_id != "gemeente_almere_sociaal_domein":
        return packet_id
    if row["domain"] == "D6":
        return "gemeente_almere_sociaal_domein_d6"
    if row["sheet"] in {"D6 afhankelijkheden", "Optionele ontwikkelagenda", "Overzicht D5"}:
        return "gemeente_almere_sociaal_domein_sturing"
    return "gemeente_almere_sociaal_domein_d5"


CSV_FIELDS = [
    "vraag_id",
    "domain",
    "workbook_id",
    "sheet",
    "sheet_row",
    "component_id",
    "question_text",
    "antwoordtype",
    "repo_update_effect",
    "bewijstype_verplicht",
    "validatiestatus_default",
    "deadline",
    "stakeholderpakket",
    "answer",
    "evidence_type",
    "evidence_reference",
    "correction_or_note",
    "not_my_domain_reroute",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def slugify(value: str) -> str:
    return value.lower().replace("/", "_").replace(" ", "_")


def packet_definition(packet_id: str) -> dict[str, str]:
    if packet_id in PACKET_DEFINITIONS:
        return PACKET_DEFINITIONS[packet_id]
    return {
        "label": packet_id.replace("_", " ").title(),
        "purpose": "Targeted validation questions for this stakeholder group.",
        "instruction": "Bevestig of corrigeer alleen wat binnen uw domein valt; gebruik niet mijn domein voor andere vragen.",
        "contact_owner": "To be assigned",
        "escalation_route": "Projectlead werkagenda",
    }


def cleanup_lookup(prefill_audit: dict[str, Any]) -> dict[tuple[str, str], list[str]]:
    out: dict[tuple[str, str], list[str]] = {}
    for workbook in prefill_audit["workbooks"]:
        for sheet in workbook["sheets"]:
            recommendations = sheet.get("recommendations") or []
            if recommendations:
                out[(workbook["workbook_id"], sheet["sheet"])] = recommendations
    return out


def collect_rows(traceability: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for workbook in traceability["workbooks"]:
        for sheet in workbook["sheets"]:
            for row in sheet["rows"]:
                rows.append(
                    {
                        "domain": workbook["validation_domain"],
                        "workbook_id": workbook["workbook_id"],
                        "workbook_path": workbook["path"],
                        "sheet": sheet["sheet"],
                        "sheet_row": row["sheet_row"],
                        "vraag_id": row["vraag_id"],
                        "component_id": row["component_id"],
                        "question_text": row["question_text"],
                        "stakeholderpakket": row["stakeholderpakket"],
                        "antwoordtype": row["antwoordtype"],
                        "validatiestatus_default": row["validatiestatus_default"],
                        "bewijstype_verplicht": row["bewijstype_verplicht"],
                        "repo_update_effect": row["repo_update_effect"],
                        "deadline": row["deadline"],
                    }
                )
    return rows


def write_packet_csv(packet_id: str, rows: list[dict[str, Any]]) -> str:
    OUTPUT_PACKET_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_PACKET_DIR / f"{slugify(packet_id)}.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    **row,
                    "stakeholderpakket": packet_id,
                    "answer": "",
                    "evidence_type": "",
                    "evidence_reference": "",
                    "correction_or_note": "",
                    "not_my_domain_reroute": "",
                }
            )
    return str(path.relative_to(ROOT)).replace("\\", "/")


def build_packets() -> dict[str, Any]:
    traceability = load_json(TRACEABILITY_PATH)
    prefill_audit = load_json(PREFILL_AUDIT_PATH)
    cleanup_by_sheet = cleanup_lookup(prefill_audit)
    all_rows = collect_rows(traceability)

    packet_rows: dict[str, list[dict[str, Any]]] = {}
    for row in all_rows:
        for packet_id in row["stakeholderpakket"]:
            routed_id = routed_packet_id(packet_id, row)
            packet_rows.setdefault(routed_id, []).append(row)

    # Clear only CSVs generated by this builder.
    if OUTPUT_PACKET_DIR.exists():
        for existing in OUTPUT_PACKET_DIR.glob("*.csv"):
            existing.unlink()

    packets: list[dict[str, Any]] = []
    for packet_id in sorted(packet_rows):
        definition = packet_definition(packet_id)
        rows = sorted(packet_rows[packet_id], key=lambda item: (item["domain"], item["sheet"], item["sheet_row"]))
        csv_path = write_packet_csv(packet_id, rows)
        cleanup_items = []
        seen_cleanup = set()
        for row in rows:
            key = (row["workbook_id"], row["sheet"])
            for recommendation in cleanup_by_sheet.get(key, []):
                cleanup_key = (row["workbook_id"], row["sheet"], recommendation)
                if cleanup_key in seen_cleanup:
                    continue
                seen_cleanup.add(cleanup_key)
                cleanup_items.append(
                    {
                        "workbook_id": row["workbook_id"],
                        "sheet": row["sheet"],
                        "recommendation": recommendation,
                    }
                )
        packets.append(
            {
                "packet_id": packet_id,
                "label": definition["label"],
                "dispatch_status": "prepared_not_sent",
                "purpose": definition["purpose"],
                "instruction": definition["instruction"],
                "contact_owner": definition["contact_owner"],
                "escalation_route": definition["escalation_route"],
                "expected_response_timing": "to_be_set_after_p7_send_readiness_gate",
                "csv_path": csv_path,
                "row_count": len(rows),
                "d5_row_count": sum(1 for row in rows if row["domain"] == "D5"),
                "d6_row_count": sum(1 for row in rows if row["domain"] == "D6"),
                "sheet_count": len({(row["workbook_id"], row["sheet"]) for row in rows}),
                "evidence_required_count": sum(1 for row in rows if row["bewijstype_verplicht"]),
                "cleanup_before_send": cleanup_items,
                "rows": rows,
            }
        )

    return {
        "generated_on": date.today().isoformat(),
        "current_sprint": "Sprint 33.P4 - Pre-contact validation-readiness: build stakeholder packets",
        "dispatch_status": "prepared_not_sent",
        "purpose": "Filtered D5/D6 pre-contact validation packet index and CSV send set.",
        "guardrails": [
            "Prepared packets are not sent and are not stakeholder validation records.",
            "Do not contact policymakers before the P7 send-readiness gate.",
            "Keep vraag_id values in every outgoing packet and returned answer.",
            "Human answers must be processed through validation logs, finance matrices, decision registers, dependency maps or source intake as appropriate.",
            "Do not fill unanswered fields by repository inference.",
        ],
        "source_inputs": [
            str(TRACEABILITY_PATH.relative_to(ROOT)).replace("\\", "/"),
            str(PREFILL_AUDIT_PATH.relative_to(ROOT)).replace("\\", "/"),
            "data/workagenda/precontact_agent_plan.json",
        ],
        "packet_count": len(packets),
        "total_packet_rows": sum(packet["row_count"] for packet in packets),
        "unique_vraag_ids": len({row["vraag_id"] for packet in packets for row in packet["rows"]}),
        "packets": packets,
    }


def render_markdown(packet_index: dict[str, Any]) -> str:
    lines = [
        "# Pre-contact Stakeholder Packets",
        "",
        "## Summary",
        "Current sprint: Sprint 33.P4 - Pre-contact validation-readiness: build stakeholder packets.",
        "",
        f"Generated on: {packet_index['generated_on']}.",
        "",
        "This file indexes filtered D5/D6 validation packet drafts. They are prepared, not sent. They are not stakeholder validation records.",
        "",
        "## Guardrails",
        "",
    ]
    lines.extend(f"- {item}" for item in packet_index["guardrails"])
    lines.extend(
        [
            "",
            "## Packet Overview",
            "",
            "| Packet | Rows | D5 | D6 | CSV | Cleanup before send |",
            "| --- | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for packet in packet_index["packets"]:
        cleanup_count = len(packet["cleanup_before_send"])
        cleanup_text = "none" if cleanup_count == 0 else f"{cleanup_count} item(s)"
        lines.append(
            f"| {packet['label']} (`{packet['packet_id']}`) | {packet['row_count']} | {packet['d5_row_count']} | {packet['d6_row_count']} | `{packet['csv_path']}` | {cleanup_text} |"
        )

    lines.extend(["", "## Packet Details", ""])
    for packet in packet_index["packets"]:
        lines.extend(
            [
                f"### {packet['label']}",
                "",
                f"Packet ID: `{packet['packet_id']}`",
                "",
                f"Status: `{packet['dispatch_status']}`",
                "",
                f"Purpose: {packet['purpose']}",
                "",
                f"Instruction: {packet['instruction']}",
                "",
                f"CSV: `{packet['csv_path']}`",
                "",
                f"Contact owner: {packet['contact_owner']}",
                "",
                f"Escalation route: {packet['escalation_route']}",
                "",
                f"Rows: {packet['row_count']} ({packet['d5_row_count']} D5, {packet['d6_row_count']} D6)",
                "",
            ]
        )
        if packet["cleanup_before_send"]:
            lines.extend(["Cleanup before send:", ""])
            for item in packet["cleanup_before_send"]:
                lines.append(
                    f"- `{item['workbook_id']}` / `{item['sheet']}`: {item['recommendation']}"
                )
            lines.append("")
        else:
            lines.extend(["Cleanup before send: none flagged by the prefill audit.", ""])

        sample_rows = packet["rows"][:8]
        lines.extend(["Sample questions:", "", "| Vraag ID | Domain | Sheet | Question |", "| --- | --- | --- | --- |"])
        for row in sample_rows:
            question = str(row["question_text"]).replace("|", "\\|")
            if len(question) > 120:
                question = question[:117] + "..."
            lines.append(f"| `{row['vraag_id']}` | {row['domain']} | {row['sheet']} | {question} |")
        if len(packet["rows"]) > len(sample_rows):
            lines.append(f"| ... | ... | ... | {len(packet['rows']) - len(sample_rows)} more row(s) in CSV |")
        lines.append("")

    lines.extend(
        [
            "## Required Before Sending",
            "",
            "- Resolve or consciously route cleanup items from `validation-workbook-prefill-audit.md`.",
            "- Confirm that packet CSVs preserve `vraag_id`, evidence fields and `not_my_domain_reroute`.",
            "- Decide whether packet CSVs are the send format or whether they should be converted into filtered Excel tabs.",
            "- Run the internal dry run in Sprint 33.P5 before any stakeholder contact.",
            "- Keep all packet statuses as `prepared_not_sent` until the P7 send-readiness gate passes.",
            "",
            "## Next Step",
            "",
            "Sprint 33.P5 should run an internal dry run with selected reviewers against these packet drafts: one D5 tab, one D6 tab, one finance row, one evidence field and one `niet mijn domein` case.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    packet_index = build_packets()
    OUTPUT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON_PATH.write_text(
        json.dumps(packet_index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    OUTPUT_DOC_PATH.write_text(render_markdown(packet_index), encoding="utf-8")
    print(f"Wrote {OUTPUT_JSON_PATH.relative_to(ROOT)}")
    print(f"Wrote {OUTPUT_DOC_PATH.relative_to(ROOT)}")
    print(f"Wrote {len(packet_index['packets'])} CSV packet(s) to {OUTPUT_PACKET_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
