from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = [
    ROOT / "docs" / "rapporten" / "plan-van-aanpak-v1.md",
    ROOT / "docs" / "rapporten" / "plan-van-aanpak-v2.md",
]
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


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


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

    if missing:
        print("VALIDATION FAILED")
        for item in missing:
            print(f"- {item}")
        return 1

    print("VALIDATION OK")
    for doc_path in DOCS:
        print(f"- {doc_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
