from __future__ import annotations

import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKAGENDA_DIR = REPO_ROOT / "data" / "workagenda"
DOCS_DIR = REPO_ROOT / "docs"

STUURMODEL_PATH = WORKAGENDA_DIR / "d5_stuurmodel.json"
OPERATIONAL_REQUIREMENTS_PATH = REPO_ROOT / "data" / "extracted" / "workagenda_d5_operational_requirements.json"
NULMETING_PATH = REPO_ROOT / "data" / "extracted" / "workagenda_nulmeting_capacity.json"

OUTPUT_JSON_PATH = WORKAGENDA_DIR / "d5_status_matrix.json"
OUTPUT_MD_PATH = DOCS_DIR / "workagenda-d5-statusmatrix.md"


D6_DEPENDENCY_HINTS = {
    "laagdrempelige_steunpunten": [
        "inloopvoorzieningen_sociaal_en_gezond",
        "burgerinitiatieven_informele_steun",
        "wijkteams_almere",
    ],
    "sociaal_verwijzen": [
        "wijkteams_almere",
        "inloopvoorzieningen_sociaal_en_gezond",
        "digitale_operationele_infrastructuur",
    ],
    "mentale_gezondheidsnetwerken": [
        "samen_sterker_in_de_wijk",
        "pga_zorgzaam_flevoland_interface",
        "kennis_advies_monitoring_dashboards",
    ],
    "valpreventie": [
        "ggd_flevoland_coordinatie",
        "kennis_advies_monitoring_dashboards",
        "burgerinitiatieven_informele_steun",
    ],
    "ketenaanpak_overgewicht_obesitas_volwassenen": [
        "sociaal_verwijzen_d6_interface",
        "inloopvoorzieningen_sociaal_en_gezond",
        "burgerinitiatieven_informele_steun",
    ],
    "kansrijke_start": [
        "jgz_almere",
        "ggd_flevoland_coordinatie",
        "stevige_lokale_teams",
        "burgerinitiatieven_informele_steun",
    ],
    "integrale_gezinspoli": [
        "jgz_almere",
        "stevige_lokale_teams",
        "digitale_operationele_infrastructuur",
    ],
    "nu_niet_zwanger": [
        "ggd_flevoland_coordinatie",
        "digitale_operationele_infrastructuur",
    ],
    "ketenaanpak_overgewicht_obesitas_kinderen": [
        "jgz_almere",
        "gezonde_school_mentale_gezonde_school",
        "ggd_flevoland_coordinatie",
    ],
}


ACTION_OWNERS = {
    "laagdrempelige_steunpunten": "Gemeente Almere sociaal domein; sociale-basis partners; finance/controller",
    "sociaal_verwijzen": "Gemeente Almere sociaal domein; eerstelijn/welzijn; zorgverzekeraar; finance/controller",
    "mentale_gezondheidsnetwerken": "GGZ/MGN governance; Gemeente Almere; zorgverzekeraar; sociaal domein",
    "valpreventie": "Gemeente Almere preventie; GGD/JGZ; beweegaanbieders; finance/controller",
    "ketenaanpak_overgewicht_obesitas_volwassenen": "Gemeente Almere preventie; zorgverzekeraar; leefstijl/beweegaanbieders",
    "kansrijke_start": "Gemeente Almere; JGZ/GGD; geboortezorg/VSV; finance/controller",
    "integrale_gezinspoli": "Gemeente Almere; VSV/geboortezorg; Flevoziekenhuis; zorgverzekeraar",
    "nu_niet_zwanger": "GGD/JGZ; Gemeente Almere; regionale governance; finance/controller",
    "ketenaanpak_overgewicht_obesitas_kinderen": "Gemeente Almere; JGZ/GGD; onderwijs/scholen; zorgverzekeraar",
    "ontwikkelagenda_1_nieuw_beproeven": "IZA/AZWA governance; Gemeente Almere; zorgverzekeraar",
    "ontwikkelagenda_2_overige_initiatieven": "IZA/AZWA governance; Gemeente Almere",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def status_cell(code: str, reason: str, evidence: list[str] | None = None, blockers: list[str] | None = None) -> dict[str, Any]:
    return {
        "status_code": code,
        "reason": reason,
        "evidence": evidence or [],
        "blockers": blockers or [],
    }


def public_foundation_for(target: dict[str, Any]) -> str:
    evidence = target.get("public_evidence", [])
    indicators = target.get("public_indicators", [])
    calculations = target.get("indicative_calculations", [])
    joined_evidence = " ".join(evidence).lower()

    weak_markers = [
        "geen almeerse capaciteit",
        "nog niet in de corpuslaag gevonden",
        "nog invulveld",
        "alleen vullen wanneer",
        "alleen opnemen als",
    ]
    if any(marker in joined_evidence for marker in weak_markers):
        return "zwak"
    if len(evidence) >= 2 and (indicators or calculations):
        return "sterk"
    if evidence:
        return "deels"
    return "geen"


def risk_for(required: bool, public_foundation: str, local_fill_count: int, indicators: list[Any], calculations: list[Any]) -> str:
    if not required:
        return "grijs"
    if public_foundation in {"geen", "zwak"} and not indicators and not calculations:
        return "rood"
    if local_fill_count >= 6 and public_foundation == "zwak":
        return "rood"
    return "geel"


def field_statuses_for(
    target_id: str,
    required: bool,
    public_foundation: str,
    nulmeting_target: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    evidence = nulmeting_target.get("public_evidence", [])
    indicators = nulmeting_target.get("public_indicators", [])
    calculations = nulmeting_target.get("indicative_calculations", [])
    decision_needed = nulmeting_target.get("decision_needed", [])

    if not required:
        optional_reason = "Scope choice is optional or conditional before workagenda fields should be filled."
        return {
            "huidige_situatie": status_cell("I", optional_reason, evidence),
            "gewenste_situatie": status_cell("I", optional_reason),
            "ingroeipad_2030": status_cell("I", optional_reason),
            "aantallen_capaciteit": status_cell("I", optional_reason),
            "financiering": status_cell("I", optional_reason),
            "verantwoordelijkheid_governance": status_cell("I", optional_reason),
            "monitoring_lerende_cyclus": status_cell("I", optional_reason),
            "mijlpalen": status_cell("I", optional_reason),
            "d6_afhankelijkheden": status_cell("I", optional_reason),
            "open_besluiten_risicos": status_cell("I", optional_reason),
        }

    current_code = "B" if public_foundation in {"sterk", "deels"} else "C"
    capacity_code = "B" if indicators or calculations else "C"
    return {
        "huidige_situatie": status_cell(
            current_code,
            "Public sources support a working view, but local status and coverage still need validation."
            if current_code == "B"
            else "Public sources do not yet fill the local current-state field strongly enough.",
            evidence,
            nulmeting_target.get("local_fill_fields", []),
        ),
        "gewenste_situatie": status_cell(
            "B",
            "National workagenda sources describe the target direction, but Almere/Flevoland must validate the local design.",
        ),
        "ingroeipad_2030": status_cell(
            "D",
            "Prioritisation and phasing toward 2030 need a local or regional decision.",
            blockers=["prioritering_2027_2030"],
        ),
        "aantallen_capaciteit": status_cell(
            capacity_code,
            "Indicators or indicative calculations exist, but capacity needs validation."
            if capacity_code == "B"
            else "No sufficient public Almere capacity basis is present yet.",
            evidence,
            nulmeting_target.get("local_fill_fields", []),
        ),
        "financiering": status_cell(
            "E",
            "Funding line, structural/project status and double-counting must be checked by finance/controller.",
            blockers=["budget"],
        ),
        "verantwoordelijkheid_governance": status_cell(
            "C",
            "Owner, coordinator, executor and mandate must be locally validated.",
            blockers=["lokale_eigenaar", "formele_besluitstatus"],
        ),
        "monitoring_lerende_cyclus": status_cell(
            "G",
            "Monitoring arrangement, data/reporting owner and learning-cycle accountability need confirmation.",
            blockers=["monitoringafspraak"],
        ),
        "mijlpalen": status_cell(
            "B",
            "National milestone structure exists, but local sequencing and action dates need validation.",
        ),
        "d6_afhankelijkheden": status_cell(
            "C",
            "D6 prerequisites must be mapped explicitly before drafting.",
            evidence=D6_DEPENDENCY_HINTS.get(target_id, []),
        ),
        "open_besluiten_risicos": status_cell(
            "D",
            "Open decisions remain and must become validation, finance or decision tickets.",
            blockers=decision_needed,
        ),
    }


def matrix_row(
    scope_target: dict[str, Any],
    operational_target: dict[str, Any],
    nulmeting_target: dict[str, Any],
) -> dict[str, Any]:
    target_id = scope_target["target_id"]
    required = bool(scope_target["required_in_workagenda"])
    foundation = public_foundation_for(nulmeting_target)
    indicators = nulmeting_target.get("public_indicators", [])
    calculations = nulmeting_target.get("indicative_calculations", [])
    local_fill_count = int(nulmeting_target.get("local_fill_count", 0))
    risk = risk_for(required, foundation, local_fill_count, indicators, calculations)
    field_statuses = field_statuses_for(target_id, required, foundation, nulmeting_target)
    field_code_counts = Counter(cell["status_code"] for cell in field_statuses.values())

    return {
        "target_id": target_id,
        "title": scope_target["title"],
        "category": scope_target["category"],
        "required_in_workagenda": required,
        "status_in_azwa": operational_target.get("workagenda_status", scope_target["category"]),
        "public_foundation": foundation,
        "local_validation_status": "niet_gestart" if required else "scopekeuze_nodig",
        "decision_status": "besluit_nodig" if required else "scopekeuze_nodig",
        "finance_status": "controllercheck_nodig" if required else "niet_van_toepassing_tot_scopekeuze",
        "capacity_status": "indicatief" if indicators or calculations else "onbekend",
        "governance_status": "eigenaar_onbekend" if required else "niet_van_toepassing_tot_scopekeuze",
        "monitoring_status": "concept" if indicators else "onbekend",
        "d6_dependency_status": "mogelijk" if target_id in D6_DEPENDENCY_HINTS else "onbekend",
        "risk": risk,
        "ready_for_workagenda_drafting": False,
        "field_statuses": field_statuses,
        "field_code_counts": dict(sorted(field_code_counts.items())),
        "public_evidence": nulmeting_target.get("public_evidence", []),
        "public_indicator_count": len(indicators),
        "indicative_calculation_count": len(calculations),
        "local_fill_fields": nulmeting_target.get("local_fill_fields", []),
        "decision_needed": nulmeting_target.get("decision_needed", []),
        "d6_dependency_hints": D6_DEPENDENCY_HINTS.get(target_id, []),
        "next_action": next_action_for(required, target_id, operational_target, foundation),
        "action_owner": ACTION_OWNERS.get(target_id, "Nog te bepalen"),
        "deadline": "2026-05-31" if required else "2026-06-15",
        "evidence": {
            "operational_requirement_source_ids": operational_target.get("source_document_ids", []),
            "nulmeting_source_layer": "data/extracted/workagenda_nulmeting_capacity.json",
            "stuurmodel_source_layer": "data/workagenda/d5_stuurmodel.json",
        },
    }


def next_action_for(required: bool, target_id: str, operational_target: dict[str, Any], public_foundation: str) -> str:
    if not required:
        return "Decide whether this optional/conditional item belongs in the Almere/Flevoland workagenda scope."
    questions = operational_target.get("review_questions", [])
    if questions:
        return f"Prepare constrained validation ticket: {questions[0]}"
    if public_foundation in {"geen", "zwak"}:
        return "Prepare targeted source/validation ticket for missing local current-state evidence."
    return "Prepare constrained validation ticket for local status, owner, finance and D6 dependency."


def build_matrix() -> dict[str, Any]:
    stuurmodel = load_json(STUURMODEL_PATH)
    operational = load_json(OPERATIONAL_REQUIREMENTS_PATH)
    nulmeting = load_json(NULMETING_PATH)

    operational_by_id = {target["target_id"]: target for target in operational.get("targets", [])}
    nulmeting_by_id = {target["target_id"]: target for target in nulmeting.get("targets", [])}

    rows = [
        matrix_row(
            scope_target,
            operational_by_id.get(scope_target["target_id"], {}),
            nulmeting_by_id.get(scope_target["target_id"], {}),
        )
        for scope_target in stuurmodel["d5_scope"]
    ]

    risk_counts = Counter(row["risk"] for row in rows)
    field_code_counts: Counter[str] = Counter()
    for row in rows:
        field_code_counts.update(row["field_code_counts"])

    return {
        "matrix_id": "workagenda_d5_status_matrix_v1",
        "generated_on": date.today().isoformat(),
        "sprint": "32.1 D5-statusmatrix bouwen",
        "status": "initial_delivery_matrix",
        "purpose": "Central delivery-status matrix showing, per D5 component and workagenda field, what public sources can prefill and what still needs validation, finance/controller confirmation, decisions or D6 dependency mapping.",
        "source_layers": [
            "data/workagenda/d5_stuurmodel.json",
            "data/extracted/workagenda_d5_operational_requirements.json",
            "data/extracted/workagenda_nulmeting_capacity.json",
            "data/extracted/municipal/almere_d6_responsibility_register.json",
        ],
        "guardrails": [
            "This matrix is a steering aid, not a workagenda draft or local decision.",
            "No row is ready for workagenda drafting until validation, finance/controller status, governance and D6 dependencies are resolved or explicitly escalated.",
            "Public-source working views must remain separate from local validation and finance/controller confirmation.",
        ],
        "summary": {
            "target_count": len(rows),
            "required_target_count": sum(1 for row in rows if row["required_in_workagenda"]),
            "ready_for_workagenda_drafting_count": sum(1 for row in rows if row["ready_for_workagenda_drafting"]),
            "risk_counts": dict(sorted(risk_counts.items())),
            "field_status_code_counts": dict(sorted(field_code_counts.items())),
        },
        "status_model": stuurmodel["delivery_status_values"],
        "rows": rows,
    }


def render_markdown(matrix: dict[str, Any]) -> str:
    rows = matrix["rows"]
    lines = [
        "# Werkagenda D5 statusmatrix v1",
        "",
        "## Summary",
        "Current sprint: Sprint 32.1 - D5-statusmatrix bouwen.",
        "",
        "This is the first central D5 delivery-status matrix. It does not draft the workagenda and it does not validate local choices. It translates the existing D5 workagenda requirements and public-source nulmeting into red/yellow/gray steering rows.",
        "",
        f"Machine-readable version: `data/workagenda/d5_status_matrix.json`.",
        "",
        "## Current Steering Summary",
        "",
        f"- D5 components tracked: {matrix['summary']['target_count']}.",
        f"- Required components: {matrix['summary']['required_target_count']}.",
        f"- Ready for workagenda drafting: {matrix['summary']['ready_for_workagenda_drafting_count']}.",
        f"- Risk counts: {json.dumps(matrix['summary']['risk_counts'], ensure_ascii=False)}.",
        "",
        "No row is ready for drafting yet. The next sprint should turn these rows into constrained validation tickets and formats.",
        "",
        "## Matrix",
        "",
        "| D5 component | Required | Public foundation | Risk | Main blocker | Next action |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for row in rows:
        blockers = main_blockers_for(row)
        lines.append(
            "| {title} | {required} | {foundation} | {risk} | {blockers} | {action} |".format(
                title=row["title"],
                required="Yes" if row["required_in_workagenda"] else "Conditional",
                foundation=row["public_foundation"],
                risk=row["risk"],
                blockers=", ".join(blockers),
                action=row["next_action"],
            )
        )

    lines.extend(
        [
            "",
            "## Field Status Meaning",
            "",
            "The machine-readable matrix scores each component on these fields:",
            "",
            "- `huidige_situatie`",
            "- `gewenste_situatie`",
            "- `ingroeipad_2030`",
            "- `aantallen_capaciteit`",
            "- `financiering`",
            "- `verantwoordelijkheid_governance`",
            "- `monitoring_lerende_cyclus`",
            "- `mijlpalen`",
            "- `d6_afhankelijkheden`",
            "- `open_besluiten_risicos`",
            "",
            "Status codes come from `data/workagenda/d5_stuurmodel.json`: A source-answered, B source-suggested but validation needed, C local validation needed, D decision needed, E finance/controller needed, F insurer/Zvw confirmation needed, G ICT/privacy/data confirmation needed, H awaiting national guidance, I optional/not applicable, J unknown.",
            "",
            "## Guardrails",
            "",
            "- Treat the matrix as a steering layer only.",
            "- Do not turn yellow or red rows into final workagenda text.",
            "- Do not use finance or governance wording as confirmed until validation evidence exists.",
            "- Keep D6 prerequisites visible as dependencies.",
            "",
        ]
    )
    return "\n".join(lines)


def main_blockers_for(row: dict[str, Any]) -> list[str]:
    if not row["required_in_workagenda"]:
        return ["scope choice"]
    blockers = []
    if row["finance_status"] == "controllercheck_nodig":
        blockers.append("finance")
    if row["governance_status"] == "eigenaar_onbekend":
        blockers.append("owner")
    if row["decision_status"] == "besluit_nodig":
        blockers.append("decision")
    if row["d6_dependency_status"] in {"mogelijk", "onbekend"}:
        blockers.append("D6 dependency")
    return blockers


def main() -> None:
    matrix = build_matrix()
    WORKAGENDA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON_PATH.write_text(json.dumps(matrix, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUTPUT_MD_PATH.write_text(render_markdown(matrix), encoding="utf-8")


if __name__ == "__main__":
    main()
