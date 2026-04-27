from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTER_PATH = REPO_ROOT / "data" / "extracted" / "municipal" / "almere_d6_responsibility_register.json"
SCHEMA_PATH = REPO_ROOT / "data" / "schemas" / "almere_d6_responsibility_register.schema.json"

REQUIRED_FIELDS = {
    "d6_component",
    "existing_almere_provision",
    "required_upgrade",
    "owner",
    "executor_or_executors",
    "cooperation_partners",
    "scale",
    "funding_source",
    "decision_status",
    "evidence_source",
    "confidence",
    "open_issue",
    "needs_human_review",
}
ALLOWED_STATUSES = {"settled", "proposed", "inferred", "unknown", "review_needed"}
LOCAL_AUTHORITY_SOURCE_PREFIXES = ("mun_almere_", "reg_ggd_flevoland_")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class AlmereD6ResponsibilityRegisterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.register = load_json(REGISTER_PATH)
        self.schema = load_json(SCHEMA_PATH)

    def test_register_and_schema_exist(self) -> None:
        self.assertTrue(REGISTER_PATH.exists())
        self.assertTrue(SCHEMA_PATH.exists())
        self.assertEqual(self.schema["title"], "Almere D6 Responsibility Register")

    def test_required_start_components_are_present(self) -> None:
        components = self.register["components"]
        self.assertGreaterEqual(len(components), 12)
        component_ids = {component["component_id"] for component in components}
        self.assertIn("wijkteams_almere", component_ids)
        self.assertIn("stevige_lokale_teams", component_ids)
        self.assertIn("funding_budget_alignment", component_ids)

    def test_rows_have_required_fields_and_evidence(self) -> None:
        for component in self.register["components"]:
            with self.subTest(component=component["component_id"]):
                self.assertTrue(REQUIRED_FIELDS.issubset(component.keys()))
                self.assertIn(component["decision_status"], ALLOWED_STATUSES)
                self.assertTrue(component["evidence_source"])
                self.assertFalse(any(source.startswith("data/site/") for source in component["evidence_source"]))

    def test_settled_rows_require_local_authority_evidence(self) -> None:
        for component in self.register["components"]:
            if component["decision_status"] != "settled":
                continue
            evidence = component.get("evidence", [])
            self.assertTrue(
                any(
                    item.get("repository_status") == "ingested_formal_corpus"
                    and item.get("source_id", "").startswith(LOCAL_AUTHORITY_SOURCE_PREFIXES)
                    for item in evidence
                ),
                component["component_id"],
            )


if __name__ == "__main__":
    unittest.main()
