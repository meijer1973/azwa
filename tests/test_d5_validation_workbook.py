from __future__ import annotations

import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "docs" / "review" / "D5_validatieformat_werkagenda_Almere_v0.2.xlsx"

NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pkgrel": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def _normalise_target(target: str) -> str:
    target = target.lstrip("/")
    return target if target.startswith("xl/") else f"xl/{target}"


def _col_to_num(col: str) -> int:
    value = 0
    for char in col:
        value = value * 26 + ord(char) - 64
    return value


def _cell_ref(cell_ref: str) -> tuple[int, int]:
    match = re.match(r"([A-Z]+)(\d+)$", cell_ref)
    if not match:
        raise ValueError(cell_ref)
    return int(match.group(2)), _col_to_num(match.group(1))


def _sheet_targets(archive: zipfile.ZipFile) -> dict[str, str]:
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    rid_to_target = {
        rel.attrib["Id"]: _normalise_target(rel.attrib["Target"])
        for rel in rels.findall("pkgrel:Relationship", NS)
    }
    targets: dict[str, str] = {}
    for sheet in workbook.findall("main:sheets/main:sheet", NS):
        rid = sheet.attrib[
            "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
        ]
        targets[sheet.attrib["name"]] = rid_to_target[rid]
    return targets


def _shared_strings(archive: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    return [
        "".join(text.text or "" for text in item.findall(".//main:t", NS))
        for item in root.findall("main:si", NS)
    ]


def _cell_value(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        return "".join(text.text or "" for text in cell.findall(".//main:t", NS))
    value = cell.find("main:v", NS)
    if value is None:
        return ""
    raw = value.text or ""
    if cell_type == "s":
        return shared_strings[int(raw)]
    return raw


def _keuzelijst_values(
    archive: zipfile.ZipFile, targets: dict[str, str], column_number: int
) -> list[str]:
    shared_strings = _shared_strings(archive)
    root = ET.fromstring(archive.read(targets["Keuzelijsten"]))
    values: list[str] = []
    for cell in root.findall(".//main:sheetData/main:row/main:c", NS):
        _row, col = _cell_ref(cell.attrib["r"])
        if col == column_number:
            values.append(_cell_value(cell, shared_strings))
    return values


def _validations(archive: zipfile.ZipFile, sheet_target: str) -> dict[str, str]:
    root = ET.fromstring(archive.read(sheet_target))
    data_validations = root.find("main:dataValidations", NS)
    if data_validations is None:
        return {}
    formulas: dict[str, str] = {}
    for validation in data_validations.findall("main:dataValidation", NS):
        formula = validation.find("main:formula1", NS)
        formulas[validation.attrib["sqref"]] = formula.text if formula is not None else ""
    return formulas


def test_d5_validation_workbook_has_owner_and_routing_dropdowns() -> None:
    with zipfile.ZipFile(WORKBOOK) as archive:
        assert archive.testzip() is None
        targets = _sheet_targets(archive)

        owner_values = _keuzelijst_values(archive, targets, column_number=22)
        stakeholder_values = _keuzelijst_values(archive, targets, column_number=23)
        overleg_values = _keuzelijst_values(archive, targets, column_number=24)
        bijsturing_values = _keuzelijst_values(archive, targets, column_number=25)

        assert owner_values[0] == "EigenaarPartij"
        assert "Gemeente Almere" in owner_values
        assert "Gemengd, splitsing nodig" in owner_values
        assert "Anders, toelichten" in owner_values

        assert stakeholder_values[0] == "Stakeholdergroep"
        assert "Finance/controller" in stakeholder_values
        assert "Meerdere partijen; splitsing nodig" in stakeholder_values

        assert overleg_values[0] == "Overlegcyclus"
        assert "Aansluiten bij bestaande overlegtafel" in overleg_values

        assert bijsturing_values[0] == "Bijsturingsafspraak"
        assert "Nog af te spreken" in bijsturing_values

        owner_formula = "Keuzelijsten!$V$2:$V$20"
        stakeholder_formula = "Keuzelijsten!$W$2:$W$16"
        overleg_formula = "Keuzelijsten!$X$2:$X$12"
        bijsturing_formula = "Keuzelijsten!$Y$2:$Y$9"

        component_sheets = [
            "Laagdremp. steunpunten",
            "Sociaal verwijzen",
            "Mentale gezondheid",
            "Valpreventie",
            "Overgewicht volwassenen",
            "Kansrijke Start",
            "Integrale gezinspoli",
            "Nu Niet Zwanger",
            "Overgewicht kinderen",
            "Optionele ontwikkelagenda",
        ]
        for sheet_name in component_sheets:
            validations = _validations(archive, targets[sheet_name])
            assert validations["F5:F50"] == owner_formula
            assert validations["P5:P50"] == owner_formula

        expected_validations = {
            "Overzicht D5": {"N11:N100": owner_formula},
            "Governance rollen": {"B5:B120": owner_formula},
            "Monitoring cyclus": {
                "E5:E80": owner_formula,
                "F5:F80": overleg_formula,
                "I5:I80": bijsturing_formula,
            },
            "D6 afhankelijkheden": {
                "F5:F80": stakeholder_formula,
                "L5:L80": owner_formula,
            },
            "Validatielog": {
                "C5:C100": stakeholder_formula,
                "N5:N100": owner_formula,
            },
            "Bronnen wijzigingen": {"G5:G80": owner_formula},
        }
        for sheet_name, expected in expected_validations.items():
            validations = _validations(archive, targets[sheet_name])
            for range_ref, formula in expected.items():
                assert validations[range_ref] == formula
