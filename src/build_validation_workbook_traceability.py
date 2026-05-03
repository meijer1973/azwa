from __future__ import annotations

import json
import re
import zipfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "data" / "workagenda" / "validation_workbook_traceability_map.json"

NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "pkgrel": "http://schemas.openxmlformats.org/package/2006/relationships",
}


@dataclass(frozen=True)
class SheetConfig:
    component_id: str
    id_prefix: str
    stakeholder_packages: list[str]
    answer_type: str
    repo_update_effect: str
    deadline: str


@dataclass(frozen=True)
class WorkbookConfig:
    workbook_id: str
    path: Path
    version: str
    validation_domain: str
    sheets: dict[str, SheetConfig]


WORKBOOKS = [
    WorkbookConfig(
        workbook_id="d5_validation_workbook",
        path=ROOT / "docs" / "review" / "D5_validatieformat_werkagenda_Almere_v0.1.xlsx",
        version="v0.1",
        validation_domain="D5",
        sheets={
            "Overzicht D5": SheetConfig(
                "d5_overview",
                "D5-OVZ",
                ["kernteam_werkagenda"],
                "status_overview",
                "status_matrix_update",
                "pre_contact_send_readiness",
            ),
            "Laagdremp. steunpunten": SheetConfig(
                "laagdrempelige_steunpunten",
                "D5-LSP",
                ["gemeente_almere_sociaal_domein", "welzijn_sociale_basis"],
                "dropdown_plus_evidence",
                "validation_log_or_decision_ticket",
                "pre_contact_send_readiness",
            ),
            "Sociaal verwijzen": SheetConfig(
                "sociaal_verwijzen",
                "D5-SV",
                ["gemeente_almere_sociaal_domein", "welzijn_sociale_basis", "zorgverzekeraar_zvw"],
                "dropdown_plus_evidence",
                "validation_log_or_finance_ticket",
                "pre_contact_send_readiness",
            ),
            "Mentale gezondheid": SheetConfig(
                "mentale_gezondheidsnetwerken",
                "D5-MGN",
                ["ggz_mgn_partners", "zorgverzekeraar_zvw", "gemeente_almere_sociaal_domein"],
                "dropdown_plus_evidence",
                "validation_log_or_decision_ticket",
                "pre_contact_send_readiness",
            ),
            "Valpreventie": SheetConfig(
                "valpreventie",
                "D5-VAL",
                ["ggd_jgz", "gemeente_almere_sociaal_domein", "zorgverzekeraar_zvw"],
                "dropdown_plus_evidence",
                "validation_log_or_finance_ticket",
                "pre_contact_send_readiness",
            ),
            "Overgewicht volwassenen": SheetConfig(
                "overgewicht_volwassenen",
                "D5-OVW",
                ["zorgverzekeraar_zvw", "gemeente_almere_sociaal_domein", "finance_controller"],
                "dropdown_plus_evidence",
                "validation_log_or_finance_ticket",
                "pre_contact_send_readiness",
            ),
            "Kansrijke Start": SheetConfig(
                "kansrijke_start",
                "D5-KS",
                ["ggd_jgz", "vsv_geboortezorg_jgz", "gemeente_almere_sociaal_domein"],
                "dropdown_plus_evidence",
                "validation_log_or_decision_ticket",
                "pre_contact_send_readiness",
            ),
            "Integrale gezinspoli": SheetConfig(
                "integrale_gezinspoli",
                "D5-IGP",
                ["vsv_geboortezorg_jgz", "ggd_jgz", "zorgverzekeraar_zvw"],
                "dropdown_plus_evidence",
                "validation_log_or_decision_ticket",
                "pre_contact_send_readiness",
            ),
            "Nu Niet Zwanger": SheetConfig(
                "nu_niet_zwanger",
                "D5-NNZ",
                ["ggd_jgz", "gemeente_almere_sociaal_domein", "finance_controller"],
                "dropdown_plus_evidence",
                "validation_log_or_finance_ticket",
                "pre_contact_send_readiness",
            ),
            "Overgewicht kinderen": SheetConfig(
                "overgewicht_kinderen",
                "D5-OK",
                ["ggd_jgz", "zorgverzekeraar_zvw", "gemeente_almere_sociaal_domein"],
                "dropdown_plus_evidence",
                "validation_log_or_finance_ticket",
                "pre_contact_send_readiness",
            ),
            "Optionele ontwikkelagenda": SheetConfig(
                "optionele_ontwikkelagenda",
                "D5-OPT",
                ["kernteam_werkagenda", "gemeente_almere_sociaal_domein"],
                "dropdown_plus_evidence",
                "decision_ticket_or_status_matrix_update",
                "pre_contact_send_readiness",
            ),
            "Financiering": SheetConfig(
                "d5_financiering",
                "D5-FIN",
                ["finance_controller", "zorgverzekeraar_zvw"],
                "finance_matrix",
                "finance_matrix_update",
                "pre_contact_send_readiness",
            ),
            "Governance rollen": SheetConfig(
                "d5_governance_rollen",
                "D5-GOV",
                ["gemeente_almere_sociaal_domein", "regionale_governance"],
                "role_matrix",
                "decision_register_or_validation_log",
                "pre_contact_send_readiness",
            ),
            "Monitoring cyclus": SheetConfig(
                "d5_monitoring_cyclus",
                "D5-MON",
                ["ggd_jgz", "ict_data_privacy", "regionale_governance"],
                "monitoring_matrix",
                "validation_log_or_ict_privacy_ticket",
                "pre_contact_send_readiness",
            ),
            "D6 afhankelijkheden": SheetConfig(
                "d5_d6_afhankelijkheden",
                "D5-D6DEP",
                ["gemeente_almere_sociaal_domein", "d6_validation_owner"],
                "dependency_matrix",
                "d5_d6_dependency_map_update",
                "pre_contact_send_readiness",
            ),
        },
    ),
    WorkbookConfig(
        workbook_id="d6_validation_workbook",
        path=ROOT / "docs" / "review" / "Almere_D6_validatieformats.xlsx",
        version="current_imported_baseline",
        validation_domain="D6",
        sheets={
            "Inloopvoorzieningen": SheetConfig(
                "inloopvoorzieningen_sociaal_en_gezond",
                "D6-INLOOP",
                ["gemeente_almere_sociaal_domein", "sociale_basis_partners", "finance_controller"],
                "component_inventory",
                "d6_validation_log_or_decision_ticket",
                "pre_contact_send_readiness",
            ),
            "Wijkteams": SheetConfig(
                "wijkteams_almere",
                "D6-WIJK",
                ["gemeente_almere_sociaal_domein", "wijkteams_slt_leads"],
                "classification_choice",
                "d6_validation_log_or_register_update",
                "pre_contact_send_readiness",
            ),
            "SLT": SheetConfig(
                "stevige_lokale_teams",
                "D6-SLT",
                ["gemeente_almere_sociaal_domein", "wijkteams_slt_leads", "finance_controller"],
                "mandate_interpretation",
                "d6_validation_log_or_decision_ticket",
                "pre_contact_send_readiness",
            ),
            "JGZ Almere": SheetConfig(
                "jgz_almere",
                "D6-JGZ",
                ["ggd_jgz", "gemeente_almere_sociaal_domein"],
                "role_split_matrix",
                "d6_validation_log_or_register_update",
                "pre_contact_send_readiness",
            ),
            "GGD Flevoland": SheetConfig(
                "ggd_flevoland_coordinatie",
                "D6-GGD",
                ["ggd_jgz", "gemeente_almere_sociaal_domein", "regionale_governance"],
                "task_split_matrix",
                "d6_validation_log_or_register_update",
                "pre_contact_send_readiness",
            ),
            "Gezonde School": SheetConfig(
                "gezonde_school_mentale_gezonde_school",
                "D6-GS",
                ["ggd_jgz", "gemeente_almere_sociaal_domein", "onderwijs_partners"],
                "classification_choice",
                "d6_validation_log_or_decision_ticket",
                "pre_contact_send_readiness",
            ),
            "Monitoring": SheetConfig(
                "kennis_advies_monitoring_dashboards",
                "D6-MON",
                ["ggd_jgz", "ict_data_privacy", "regionale_governance"],
                "monitoring_matrix",
                "d6_validation_log_or_ict_privacy_ticket",
                "pre_contact_send_readiness",
            ),
            "Samen Sterker": SheetConfig(
                "samen_sterker_in_de_wijk",
                "D6-SSW",
                ["wijkgerichte_ggz_welzijnspartners", "gemeente_almere_sociaal_domein", "finance_controller"],
                "classification_choice",
                "d6_validation_log_or_decision_ticket",
                "pre_contact_send_readiness",
            ),
            "PGA-Zorgzaam-Flever": SheetConfig(
                "pga_zorgzaam_flever_interface",
                "D6-PZF",
                ["pga_zorgzaam_flever_regionale_governance", "gemeente_almere_sociaal_domein"],
                "actor_role_matrix",
                "d6_validation_log_or_decision_ticket",
                "pre_contact_send_readiness",
            ),
            "Digitaal-operationeel": SheetConfig(
                "digitale_en_operationele_infrastructuur",
                "D6-DIG",
                ["ict_data_privacy", "pga_zorgzaam_flever_regionale_governance", "finance_controller"],
                "subcomponent_inventory",
                "d6_validation_log_or_ict_privacy_ticket",
                "pre_contact_send_readiness",
            ),
            "Informele steun": SheetConfig(
                "burgerinitiatieven_informele_steun",
                "D6-INF",
                ["sociale_basis_partners", "gemeente_almere_sociaal_domein"],
                "actor_mechanism_inventory",
                "d6_validation_log_or_register_update",
                "pre_contact_send_readiness",
            ),
            "Financiering": SheetConfig(
                "d6_financiering_budgetafbakening",
                "D6-FIN",
                ["finance_controller", "gemeente_almere_sociaal_domein", "regionale_governance"],
                "finance_matrix",
                "d6_finance_matrix_or_decision_ticket",
                "pre_contact_send_readiness",
            ),
        },
    ),
]


REQUIRED_TRACEABILITY_FIELDS = [
    "vraag_id",
    "component_id",
    "stakeholderpakket",
    "antwoordtype",
    "validatiestatus",
    "bewijstype_verplicht",
    "repo_update_effect",
    "deadline",
]


def normalize(value: str) -> str:
    cleaned = value.strip().lower()
    cleaned = cleaned.replace("/", " ")
    cleaned = cleaned.replace("-", " ")
    return re.sub(r"\s+", " ", cleaned)


def column_index(cell_ref: str) -> int:
    match = re.match(r"([A-Z]+)", cell_ref)
    if not match:
        raise ValueError(f"Invalid cell reference: {cell_ref}")
    out = 0
    for char in match.group(1):
        out = out * 26 + (ord(char) - 64)
    return out


def read_shared_strings(archive: zipfile.ZipFile) -> list[str]:
    try:
        root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    values: list[str] = []
    for shared_string in root.findall("main:si", NS):
        values.append("".join(text.text or "" for text in shared_string.findall(".//main:t", NS)))
    return values


def cell_value(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    value = cell.find("main:v", NS)
    if cell_type == "s" and value is not None:
        return shared_strings[int(value.text or "0")]
    if cell_type == "inlineStr":
        return "".join(text.text or "" for text in cell.findall(".//main:t", NS))
    return value.text if value is not None else ""


def normalize_target(target: str) -> str:
    target = target.lstrip("/")
    if target.startswith("xl/"):
        return target
    return "xl/" + target


def workbook_sheets(archive: zipfile.ZipFile) -> dict[str, str]:
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    rel_by_id = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels.findall("pkgrel:Relationship", NS)
    }
    sheets: dict[str, str] = {}
    for sheet in workbook.findall("main:sheets/main:sheet", NS):
        rel_id = sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]
        sheets[sheet.attrib["name"]] = normalize_target(rel_by_id[rel_id])
    return sheets


def read_sheet_rows(
    archive: zipfile.ZipFile, sheet_path: str, shared_strings: list[str]
) -> list[dict[str, object]]:
    root = ET.fromstring(archive.read(sheet_path))
    rows: list[dict[str, object]] = []
    for row in root.findall("main:sheetData/main:row", NS):
        values: dict[int, str] = {}
        for cell in row.findall("main:c", NS):
            ref = cell.attrib.get("r")
            if not ref:
                continue
            value = cell_value(cell, shared_strings)
            if value != "":
                values[column_index(ref)] = value
        if values:
            rows.append({"row_number": int(row.attrib.get("r", "0")), "values": values})
    return rows


def find_header_row(rows: list[dict[str, object]]) -> dict[str, object] | None:
    header_markers = {
        "d5 onderdeel",
        "vraag te valideren aspect",
        "vraag",
        "functiecluster",
        "taakcluster",
        "monitor dashboard rapport",
        "actor",
        "subcomponent",
        "actor of mechanisme",
        "faciliteit of mechanisme",
        "component",
        "organisatie actor",
        "d5 onderdeel thema",
    }
    for row in rows:
        values = row["values"]
        assert isinstance(values, dict)
        normalized = {normalize(value) for value in values.values()}
        if normalized & header_markers:
            return row
    return None


def header_lookup(header_row: dict[str, object] | None) -> dict[int, str]:
    if not header_row:
        return {}
    values = header_row["values"]
    assert isinstance(values, dict)
    return {idx: value for idx, value in values.items()}


def field_coverage(headers: dict[int, str], sheet_summary: str) -> dict[str, bool]:
    normalized_headers = [normalize(value) for value in headers.values()]
    summary_present = "huidige werkhypothese" in sheet_summary.lower()
    return {
        "vraag_id": any(value in {"vraag id", "vraag_id"} for value in normalized_headers),
        "component_id": any(value in {"component id", "component_id"} for value in normalized_headers),
        "stakeholderpakket": any("stakeholderpakket" in value for value in normalized_headers),
        "antwoordtype": any(value in {"antwoordtype", "type vraag"} for value in normalized_headers),
        "validatiestatus": any("validatiestatus" in value for value in normalized_headers),
        "bewijstype_verplicht": any("bewijstype verplicht" in value for value in normalized_headers),
        "repo_update_effect": any(value in {"repo update effect", "repo_update_effect"} for value in normalized_headers),
        "deadline": any("deadline" in value for value in normalized_headers),
        "evidence_reference": any("bewijs" in value for value in normalized_headers),
        "current_working_view": any("huidige werkhypothese" in value for value in normalized_headers)
        or summary_present,
    }


def row_text(values: dict[int, str], headers: dict[int, str]) -> str:
    normalized_to_index = {normalize(header): idx for idx, header in headers.items()}
    for candidate in (
        "vraag te valideren aspect",
        "vraag",
        "d5 onderdeel",
        "component",
        "functiecluster",
        "taakcluster",
        "monitor dashboard rapport",
        "actor",
        "subcomponent",
        "actor of mechanisme",
        "faciliteit of mechanisme",
        "organisatie actor",
        "d5 onderdeel thema",
        "beslispunt",
        "onderdeel",
    ):
        idx = normalized_to_index.get(candidate)
        if idx is not None and values.get(idx):
            if candidate in {"vraag", "onderdeel", "beslispunt"}:
                first = values.get(1)
                if first and first != values[idx]:
                    return f"{first}: {values[idx]}"
            return values[idx]
    return values.get(1, "")


def sheet_summary(rows: list[dict[str, object]], header_row: dict[str, object] | None) -> str:
    header_number = int(header_row["row_number"]) if header_row else 9999
    summary_parts: list[str] = []
    for row in rows:
        if int(row["row_number"]) >= header_number:
            continue
        values = row["values"]
        assert isinstance(values, dict)
        for value in values.values():
            if "Huidige werkhypothese" in value:
                summary_parts.append(value)
                break
        if summary_parts:
            break
    return "\n".join(summary_parts)


def validation_rows(
    rows: list[dict[str, object]],
    header_row: dict[str, object] | None,
    headers: dict[int, str],
    config: SheetConfig,
) -> list[dict[str, object]]:
    if not header_row:
        return []
    header_number = int(header_row["row_number"])
    out: list[dict[str, object]] = []
    sequence = 1
    for row in rows:
        row_number = int(row["row_number"])
        if row_number <= header_number:
            continue
        values = row["values"]
        assert isinstance(values, dict)
        if not values.get(1):
            continue
        question_id = f"{config.id_prefix}-{sequence:03d}"
        out.append(
            {
                "vraag_id": question_id,
                "component_id": config.component_id,
                "sheet_row": row_number,
                "question_text": row_text(values, headers),
                "stakeholderpakket": config.stakeholder_packages,
                "antwoordtype": config.answer_type,
                "validatiestatus_default": "nog_niet_gevraagd",
                "bewijstype_verplicht": True,
                "repo_update_effect": config.repo_update_effect,
                "deadline": config.deadline,
            }
        )
        sequence += 1
    return out


def build_map() -> dict[str, object]:
    workbooks: list[dict[str, object]] = []
    all_question_ids: list[str] = []
    for workbook_config in WORKBOOKS:
        with zipfile.ZipFile(workbook_config.path) as archive:
            shared_strings = read_shared_strings(archive)
            sheets = workbook_sheets(archive)
            sheet_entries: list[dict[str, object]] = []
            for sheet_name, sheet_config in workbook_config.sheets.items():
                rows = read_sheet_rows(archive, sheets[sheet_name], shared_strings)
                header_row = find_header_row(rows)
                headers = header_lookup(header_row)
                summary = sheet_summary(rows, header_row)
                mapped_rows = validation_rows(rows, header_row, headers, sheet_config)
                all_question_ids.extend(row["vraag_id"] for row in mapped_rows)
                coverage = field_coverage(headers, summary)
                missing = [
                    field
                    for field in REQUIRED_TRACEABILITY_FIELDS
                    if not coverage.get(field, False)
                ]
                sheet_entries.append(
                    {
                        "sheet": sheet_name,
                        "component_id": sheet_config.component_id,
                        "id_prefix": sheet_config.id_prefix,
                        "stakeholderpakket": sheet_config.stakeholder_packages,
                        "header_row": header_row["row_number"] if header_row else None,
                        "headers": list(headers.values()),
                        "required_field_coverage": coverage,
                        "missing_required_fields_in_workbook": missing,
                        "mapped_validation_row_count": len(mapped_rows),
                        "rows": mapped_rows,
                    }
                )
        workbooks.append(
            {
                "workbook_id": workbook_config.workbook_id,
                "path": str(workbook_config.path.relative_to(ROOT)).replace("\\", "/"),
                "version": workbook_config.version,
                "validation_domain": workbook_config.validation_domain,
                "sheets": sheet_entries,
            }
        )
    return {
        "generated_on": date.today().isoformat(),
        "current_sprint": "Sprint 33.P1 - Pre-contact validation-readiness: add IDs, routing and traceability",
        "purpose": "Repository-side traceability map for D5/D6 Excel validation workbooks before stakeholder contact.",
        "required_traceability_fields": REQUIRED_TRACEABILITY_FIELDS,
        "guardrail": "The Excel workbooks and this map are validation instruments, not source evidence or validation results.",
        "question_id_uniqueness": {
            "total_ids": len(all_question_ids),
            "unique_ids": len(set(all_question_ids)),
            "duplicates": sorted({item for item in all_question_ids if all_question_ids.count(item) > 1}),
        },
        "workbooks": workbooks,
    }


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(build_map(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
