from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DR_REPORT_PATH = REPO_ROOT / "docs" / "dr" / "Healthy school.md"
MANIFEST_PATH = REPO_ROOT / "data" / "raw" / "manifest.json"
INVENTORY_PATH = REPO_ROOT / "data" / "extracted" / "document_inventory.json"
REGISTER_PATH = REPO_ROOT / "data" / "extracted" / "municipal" / "almere_d6_responsibility_register.json"

HEALTHY_SCHOOL_SOURCE_IDS = {
    "mun_almere_gezonde_scholen",
    "mun_almere_gezond_in_almere",
    "reg_ggd_flevoland_gezonde_school",
    "reg_ggd_flevoland_ketenaanpak_gezond_gewicht_almere",
    "mun_almere_lea_2024_2028",
}


def load_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


class DeepResearchIntakeTests(unittest.TestCase):
    def test_deep_research_report_is_not_manifest_source(self) -> None:
        self.assertTrue(DR_REPORT_PATH.exists())
        manifest = load_json(MANIFEST_PATH)
        self.assertFalse(any(entry["file_path"] == "docs/dr/Healthy school.md" for entry in manifest))

    def test_healthy_school_sources_are_ingested(self) -> None:
        manifest = load_json(MANIFEST_PATH)
        manifest_ids = {entry["document_id"] for entry in manifest}
        self.assertTrue(HEALTHY_SCHOOL_SOURCE_IDS.issubset(manifest_ids))

        inventory = load_json(INVENTORY_PATH)
        inventory_ids = {entry["document_id"] for entry in inventory["documents"]}
        self.assertTrue(HEALTHY_SCHOOL_SOURCE_IDS.issubset(inventory_ids))

    def test_healthy_school_findings_reach_d6_register(self) -> None:
        register = load_json(REGISTER_PATH)
        row = next(
            component
            for component in register["components"]
            if component["component_id"] == "gezonde_school_mentale_gezonde_school"
        )
        evidence_sources = set(row["evidence_source"])
        self.assertTrue(HEALTHY_SCHOOL_SOURCE_IDS.issubset(evidence_sources))
        self.assertIsNotNone(row["existing_almere_provision"])
        self.assertNotEqual(row["decision_status"], "settled")
        self.assertTrue(row["needs_human_review"])


if __name__ == "__main__":
    unittest.main()
