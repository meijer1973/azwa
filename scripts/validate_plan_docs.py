from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = [
    ROOT / "docs" / "rapporten" / "plan-van-aanpak-v1.md",
    ROOT / "docs" / "rapporten" / "plan-van-aanpak-v2.md",
]
REPORT_DIR = ROOT / "docs" / "rapporten"
SITE_PATH = ROOT / "data" / "site" / "site_almere_view.json"
CURRENT_PATH = ROOT / "data" / "extracted" / "municipal" / "almere_current_view.json"
QC_PATH = ROOT / "data" / "extracted" / "qc_report.json"

HEADINGS = [
    "## Inleiding en aanleiding",
    "## Probleemanalyse en lokale opgave",
    "## Ambitie en Doelstellingen",
    "## Scope en afbakening",
    "## Samenwerking en governance (rollen en betrokkenen, besluitvorming)",
    "## Aanpak en strategie",
    "## Actielijnen, werkpakketten",
    "## Personele inzet",
    "## Concrete acties en planning",
    "## Middelen en Financien Meicirculaire",
    "## Risico's en beheersmaatregelen en randvoorwaarden",
    "## Monitoring en evaluatie",
    "## Communicatie en participatie",
    "## Besluitvorming en vervolgstappen",
    "## Verantwoording",
    "## Bijlagen",
]

REGIONAL_RISK_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("de regio", re.compile(r"\bde regio\b", re.IGNORECASE)),
    ("regionale structuur", re.compile(r"\bregionale structuur\b", re.IGNORECASE)),
    ("Flevolandse structuur", re.compile(r"\bFlevolandse structuur\b", re.IGNORECASE)),
    ("mandaatgemeente", re.compile(r"\bmandaatgemeente\b", re.IGNORECASE)),
    ("zorgkantoor", re.compile(r"\bzorgkantoor\w*\b", re.IGNORECASE)),
    ("GGD-regio", re.compile(r"\bGGD-regio\b", re.IGNORECASE)),
    ("IZA-regio", re.compile(r"\bIZA-regio\b", re.IGNORECASE)),
    ("GGD Flevoland", re.compile(r"\bGGD Flevoland\b", re.IGNORECASE)),
]

REGIONAL_CLARIFIERS = [
    "IZA/AZWA-regio",
    "IZA-regio",
    "AZWA-regio",
    "GGD-regio",
    "zorgkantoorregio",
    "ROAZ",
    "subregio",
    "subregionale",
    "provincie",
    "formeel",
    "formele",
    "praktisch",
    "praktische",
    "coordinatie",
    "uitvoering",
    "middelen",
    "verantwoording",
    "review",
    "te bepalen",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def regional_ambiguity_warnings(paths: list[Path]) -> list[str]:
    warnings: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for label, pattern in REGIONAL_RISK_PATTERNS:
            for match in pattern.finditer(text):
                idx = match.start()
                window = text[max(0, idx - 180) : min(len(text), idx + 240)]
                if not any(clarifier.lower() in window.lower() for clarifier in REGIONAL_CLARIFIERS):
                    line_no = text.count("\n", 0, idx) + 1
                    warnings.append(
                        f"{path.name}:{line_no}: regionale term '{label}' mist nabije duiding van schaal, rol of reviewstatus"
                    )
    return warnings


def main() -> int:
    site = load_json(SITE_PATH)
    current = load_json(CURRENT_PATH)
    qc = load_json(QC_PATH)

    gap_titles = [item["title"] for item in site["local_gaps"]]
    as_of_date = current["as_of_date"]
    blocking = qc["summary"]["blocking"]
    warnings = qc["summary"]["warning"]
    reviews = qc["summary"]["review"]

    common_fragments = [
        f"Peildatum: {as_of_date}.",
        "Datatoets 22 april 2026",
        f"{blocking} blocking issues",
        f"{warnings} warnings",
        f"{reviews} reviewpunten",
        "2027-2028",
        "2028",
        "2030",
    ] + gap_titles

    missing: list[str] = []
    warnings: list[str] = []

    for doc_path in DOCS:
        if not doc_path.exists():
            missing.append(f"{doc_path}: file ontbreekt")
            continue
        text = doc_path.read_text(encoding="utf-8")
        for heading in HEADINGS:
            if heading not in text:
                missing.append(f"{doc_path.name}: mist kopje '{heading}'")
        for fragment in common_fragments:
            if fragment not in text:
                missing.append(f"{doc_path.name}: mist fragment '{fragment}'")

    report_docs = [
        path
        for path in sorted(REPORT_DIR.glob("*.md"))
        if path.name != "schrijfrichtlijn-plan-van-aanpak.md"
    ]
    warnings.extend(regional_ambiguity_warnings(report_docs))

    if missing:
        print("VALIDATION FAILED")
        for item in missing:
            print(f"- {item}")
        if warnings:
            print("REGIONAL AMBIGUITY WARNINGS")
            for item in warnings:
                print(f"- {item}")
        return 1

    print("VALIDATION OK")
    for doc_path in DOCS:
        print(f"- {doc_path.relative_to(ROOT)}")
    if warnings:
        print("REGIONAL AMBIGUITY WARNINGS")
        for item in warnings:
            print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
