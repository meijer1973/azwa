from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
STATUS_MATRIX_PATH = REPO_ROOT / "data" / "workagenda" / "d5_status_matrix.json"
OUTPUT_PATH = REPO_ROOT / "data" / "workagenda" / "almere_regional_workagenda_input_objects.json"
SCHEMA_PATH = REPO_ROOT / "data" / "schemas" / "almere_regional_workagenda_input.schema.json"
DOC_PATH = REPO_ROOT / "docs" / "workagenda-almere-regional-input-model.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def nested_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        keys = set(value)
        for item in value.values():
            keys.update(nested_keys(item))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(nested_keys(item))
        return keys
    return set()


class AlmereRegionalWorkagendaInputTests(unittest.TestCase):
    def setUp(self) -> None:
        self.matrix = load_json(STATUS_MATRIX_PATH)
        self.layer = load_json(OUTPUT_PATH)

    def test_layer_schema_doc_and_output_exist(self) -> None:
        self.assertTrue(OUTPUT_PATH.exists())
        self.assertTrue(SCHEMA_PATH.exists())
        self.assertTrue(DOC_PATH.exists())
        self.assertEqual(self.layer["schema_id"], "ALMERE-REGIONAL-WORKAGENDA-INPUT-V1")
        self.assertEqual(self.layer["status"], "generated_concept_layer")

    def test_output_contains_one_object_per_d5_status_matrix_row(self) -> None:
        matrix_ids = [row["target_id"] for row in self.matrix["rows"]]
        output_ids = [item["component_id"] for item in self.layer["objects"]]

        self.assertEqual(output_ids, matrix_ids)
        self.assertEqual(self.layer["summary"]["object_count"], len(matrix_ids))
        self.assertEqual(self.layer["summary"]["confirmed_position_ready_count"], 0)

    def test_valpreventie_acceptance_shape(self) -> None:
        objects = {item["component_id"]: item for item in self.layer["objects"]}
        valpreventie = objects["valpreventie"]

        self.assertEqual(valpreventie["component_id"], "valpreventie")
        self.assertTrue(valpreventie["almere_submission"]["concept_handoff_ready"])
        self.assertFalse(valpreventie["almere_submission"]["confirmed_position_ready"])
        self.assertTrue(valpreventie["evidence_package"]["public_evidence"])
        self.assertEqual(
            valpreventie["validation_needed_before_or_after_submission"]["validation_ticket_ids"],
            [
                "valpreventie__local_status_capacity",
                "valpreventie__governance_roles",
                "valpreventie__finance_controller",
                "valpreventie__d6_dependency",
                "valpreventie__decision_phasing",
            ],
        )

        gap_fields = {gap["field"] for gap in valpreventie["gap_summary"]["main_gaps"]}
        self.assertIn("governance", gap_fields)
        self.assertIn("finance", gap_fields)
        self.assertIn("capacity", gap_fields)
        self.assertIn("monitoring", gap_fields)
        self.assertIn("d6_dependency", gap_fields)
        self.assertIn("bestaande uitvoeringsroute", valpreventie["handoff_to_region"]["recommended_wording"])

    def test_priority_questions_are_limited_and_traceable(self) -> None:
        for item in self.layer["objects"]:
            questions = item["validation_needed_before_or_after_submission"]["priority_questions"]
            self.assertLessEqual(len(questions), 5)
            for question in questions:
                self.assertTrue(question["source_ticket_id"])
                self.assertTrue(question["question"])
                self.assertTrue(question["evidence_required"])

    def test_disallowed_german_terms_are_not_used_as_keys(self) -> None:
        keys = nested_keys(self.layer)
        self.assertFalse({"ist", "soll", "ist_soll_gap"}.intersection(keys))

    def test_doc_names_sprint_and_boundary(self) -> None:
        text = DOC_PATH.read_text(encoding="utf-8")

        self.assertIn("Current sprint: Sprint 33.P7", text)
        self.assertIn("This layer is a preparation and handoff model.", text)
        self.assertIn("not proof that unresolved local items have been decided", text)


if __name__ == "__main__":
    unittest.main()
