from __future__ import annotations

import json
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "data" / "raw" / "manifest.json"
OUTPUT_PATH = REPO_ROOT / "data" / "extracted" / "document_inventory.json"


ANNOTATIONS = {
    "nat_azwa_2025_definitief": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": True,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Definitive national agreement text and the main normative source for AZWA-wide D5/D6 extraction.",
    },
    "nat_azwa_2025_onderhandelaarsakkoord": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": True,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Substantive predecessor agreement that is useful for tracing pre-final wording and commitments.",
    },
    "nat_azwa_2026_cw31_kader_d5_d6": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": True,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "The most targeted D5/D6 framework document in the corpus, including finance and evaluation framing.",
    },
    "reg_flevoland_2023_regioplan_iza": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": True,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Regional IZA implementation plan with strong governance, monitoring, and Almere relevance.",
    },
    "mun_almere_pga_transformatieplan": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Core local implementation source for Almere, but not itself a D5/D6 source document.",
    },
    "nat_azwa_2026_cw31_kamerbrief": {
        "source_classification": "derivative",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": False,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Transmittal letter for the CW 3.1 annexes; useful for status and official framing rather than detailed extraction.",
    },
    "nat_azwa_2026_voortgang_kamerbrief": {
        "source_classification": "derivative",
        "curation_bucket": "canonical",
        "contains_d5": True,
        "contains_d6": True,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Progress letter with important implementation, monitoring, and regionalization details for D5/D6 rollout.",
    },
    "nat_azwa_2025_aanbiedingsbrief": {
        "source_classification": "derivative",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Short offering letter that confirms signature status and gives limited interpretive context.",
    },
    "nat_iza_2022_integraal_zorgakkoord": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": True,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Upstream national agreement that provides the main pre-AZWA governance and monitoring context.",
    },
    "nat_gala_2023_gezond_en_actief_leven": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": True,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Upstream public-health and municipal implementation agreement relevant to prevention and social-basis context.",
    },
    "mun_almere_pga_seo_businesscase_2024": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": True,
        "contains_financing_logic": True,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Commissioned research and business-case report that can support local claim and impact interpretation.",
    },
    "reg_flevoland_2023_regiobeeld": {
        "source_classification": "primary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": True,
        "contains_financing_logic": False,
        "contains_governance_logic": False,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Regional baseline evidence report for needs, pressures, and context rather than normative policy content.",
    },
    "nat_vng_azwa_faq_middelen": {
        "source_classification": "supporting_commentary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": True,
        "contains_governance_logic": False,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Practical VNG funding explainer; useful for implementation context but weaker than the underlying agreements.",
    },
    "nat_vng_azwa_faq_uitvoeringscapaciteit": {
        "source_classification": "supporting_commentary",
        "curation_bucket": "canonical",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Practical VNG implementation-capacity explainer with municipal relevance but low normative weight.",
    },
    "mun_almere_2024_2034_maatschappelijke_agenda": {
        "source_classification": "derivative",
        "curation_bucket": "context",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Agendawijzer summary page that points to underlying municipal documents rather than replacing them.",
    },
    "mun_almere_2024_2026_visie_gezondheidsbeleid": {
        "source_classification": "derivative",
        "curation_bucket": "context",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": True,
        "contains_municipal_implications": True,
        "inventory_notes": "Agendawijzer summary page with useful local policy signals but not the full policy text.",
    },
    "mun_almere_sociaal_domein_informatiepagina": {
        "source_classification": "supporting_commentary",
        "curation_bucket": "context",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": True,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "General orientation page that links the local policy landscape but is not itself a source of detailed claims.",
    },
    "mun_almere_sociale_staat_gateway": {
        "source_classification": "supporting_commentary",
        "curation_bucket": "context",
        "contains_d5": False,
        "contains_d6": False,
        "contains_structured_tables": False,
        "contains_financing_logic": False,
        "contains_governance_logic": False,
        "contains_monitoring_evaluation_logic": False,
        "contains_municipal_implications": True,
        "inventory_notes": "Gateway page that should eventually be replaced by the linked underlying reports.",
    },
}


def priority_label(priority_rank: int) -> str:
    if priority_rank <= 5:
        return "critical"
    if priority_rank <= 8:
        return "high"
    if priority_rank <= 12:
        return "medium"
    return "low"


def validate_annotations(document_ids: set[str]) -> None:
    annotation_ids = set(ANNOTATIONS)
    missing = sorted(document_ids - annotation_ids)
    unexpected = sorted(annotation_ids - document_ids)
    if missing or unexpected:
        parts = []
        if missing:
            parts.append(f"missing annotations for: {', '.join(missing)}")
        if unexpected:
            parts.append(f"unexpected annotation ids: {', '.join(unexpected)}")
        raise ValueError("; ".join(parts))


def build_inventory() -> dict:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    document_ids = {entry["document_id"] for entry in manifest}
    validate_annotations(document_ids)

    documents = []
    for entry in manifest:
        annotation = ANNOTATIONS[entry["document_id"]]
        source_format = Path(entry["file_path"]).suffix.lower().lstrip(".")
        traceability_mode = "page_based" if source_format == "pdf" else "section_chunk_based"
        documents.append(
            {
                "document_id": entry["document_id"],
                "source_number": entry["source_number"],
                "title": entry["title"],
                "short_title": entry["short_title"],
                "publisher": entry["publisher"],
                "publication_date": entry["publication_date"],
                "document_type": entry["document_type"],
                "jurisdiction_level": entry["jurisdiction_level"],
                "status": entry["status"],
                "source_url": entry["source_url"],
                "file_path": entry["file_path"],
                "source_format": source_format,
                "traceability_mode": traceability_mode,
                "source_classification": annotation["source_classification"],
                "curation_bucket": annotation["curation_bucket"],
                "contains_d5": annotation["contains_d5"],
                "contains_d6": annotation["contains_d6"],
                "contains_structured_tables": annotation["contains_structured_tables"],
                "contains_financing_logic": annotation["contains_financing_logic"],
                "contains_governance_logic": annotation["contains_governance_logic"],
                "contains_monitoring_evaluation_logic": annotation["contains_monitoring_evaluation_logic"],
                "contains_municipal_implications": annotation["contains_municipal_implications"],
                "priority_rank": entry["priority_rank"],
                "extraction_priority": priority_label(entry["priority_rank"]),
                "inventory_notes": annotation["inventory_notes"],
            }
        )

    documents.sort(key=lambda item: (item["priority_rank"], item["document_id"]))

    summary = {
        "document_count": len(documents),
        "priority_counts": {
            "critical": sum(1 for item in documents if item["extraction_priority"] == "critical"),
            "high": sum(1 for item in documents if item["extraction_priority"] == "high"),
            "medium": sum(1 for item in documents if item["extraction_priority"] == "medium"),
            "low": sum(1 for item in documents if item["extraction_priority"] == "low"),
        },
        "source_classification_counts": {
            "primary": sum(1 for item in documents if item["source_classification"] == "primary"),
            "derivative": sum(1 for item in documents if item["source_classification"] == "derivative"),
            "supporting_commentary": sum(
                1 for item in documents if item["source_classification"] == "supporting_commentary"
            ),
        },
        "topic_signal_counts": {
            "contains_d5": sum(1 for item in documents if item["contains_d5"]),
            "contains_d6": sum(1 for item in documents if item["contains_d6"]),
            "contains_structured_tables": sum(1 for item in documents if item["contains_structured_tables"]),
            "contains_financing_logic": sum(1 for item in documents if item["contains_financing_logic"]),
            "contains_governance_logic": sum(1 for item in documents if item["contains_governance_logic"]),
            "contains_monitoring_evaluation_logic": sum(
                1 for item in documents if item["contains_monitoring_evaluation_logic"]
            ),
            "contains_municipal_implications": sum(
                1 for item in documents if item["contains_municipal_implications"]
            ),
        },
    }

    return {
        "inventory_version": 1,
        "generated_on": date.today().isoformat(),
        "source_manifest": MANIFEST_PATH.relative_to(REPO_ROOT).as_posix(),
        "documents": documents,
        "summary": summary,
    }


def main() -> None:
    inventory = build_inventory()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"Prepared inventory for {inventory['summary']['document_count']} documents")


if __name__ == "__main__":
    main()
