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
        self.assertEqual(self.layer["format_field_check"]["scope"], "format_aligned_workagenda_input")

    def test_output_contains_one_object_per_d5_status_matrix_row(self) -> None:
        matrix_ids = [row["target_id"] for row in self.matrix["rows"]]
        output_ids = [item["component_id"] for item in self.layer["objects"]]

        self.assertEqual(output_ids, matrix_ids)
        self.assertEqual(self.layer["summary"]["object_count"], len(matrix_ids))
        self.assertEqual(self.layer["summary"]["confirmed_position_ready_count"], 0)
        self.assertGreaterEqual(self.layer["summary"]["enriched_information_object_count"], len(matrix_ids))
        self.assertGreater(self.layer["summary"]["implementation_progress_signal_count"], 0)
        self.assertEqual(self.layer["summary"]["format_aligned_object_count"], len(matrix_ids))
        self.assertEqual(self.layer["summary"]["format_confirmed_field_count"], 0)
        self.assertEqual(self.layer["summary"]["format_source_id"], "nat_azwa_format_werkagenda_d5_2026")
        self.assertEqual(
            self.layer["format_field_check"]["field_status_counts"]["source_backed_current_information"],
            77,
        )
        self.assertEqual(
            self.layer["format_field_check"]["deep_research_recommendation"][
                "confirmed_d5_component_decision_records_seen"
            ],
            0,
        )
        self.assertEqual(self.layer["summary"]["primary_municipality_delivery_target"], "2026-09-15")
        self.assertIn("main delivery target", self.layer["summary"]["date_priority_note"])

    def test_valpreventie_acceptance_shape(self) -> None:
        objects = {item["component_id"]: item for item in self.layer["objects"]}
        valpreventie = objects["valpreventie"]

        self.assertEqual(valpreventie["component_id"], "valpreventie")
        self.assertEqual(
            valpreventie["municipality_delivery_to_region"]["target_date"],
            "2026-09-15",
        )
        self.assertTrue(
            valpreventie["municipality_delivery_to_region"]["must_surface_in_municipality_outputs"]
        )
        self.assertEqual(
            valpreventie["almere_submission"]["target_delivery_to_region_date"],
            "2026-09-15",
        )
        self.assertTrue(valpreventie["almere_submission"]["concept_handoff_ready"])
        self.assertFalse(valpreventie["almere_submission"]["confirmed_position_ready"])
        self.assertIn("workagenda_delivery_requirements", valpreventie)
        self.assertIn("available_information_for_workagenda", valpreventie)
        self.assertEqual(
            len(valpreventie["workagenda_delivery_requirements"]["required_sections"]),
            8,
        )
        implementation_signals = valpreventie["available_information_for_workagenda"][
            "implementation_progress_signals"
        ]
        self.assertTrue(any("cursus" in signal["statement"] for signal in implementation_signals))
        party_signals = valpreventie["available_information_for_workagenda"]["party_and_role_signals"]
        self.assertTrue(any("Paramedisch Platform Almere" in signal["party_or_role"] for signal in party_signals))
        self.assertTrue(valpreventie["evidence_package"]["public_evidence"])
        self.assertTrue(valpreventie["evidence_package"]["public_indicators"])
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

    def test_valpreventie_maps_to_actual_workagenda_format(self) -> None:
        objects = {item["component_id"]: item for item in self.layer["objects"]}
        valpreventie = objects["valpreventie"]

        format_input = valpreventie["format_aligned_workagenda_input"]
        self.assertEqual(
            format_input["format_source"]["source_id"],
            "nat_azwa_format_werkagenda_d5_2026",
        )
        self.assertEqual(format_input["format_component_context"]["format_item_id"], "5a")
        self.assertEqual(
            format_input["format_component_context"]["leefgebied"],
            "Vitaal ouder worden/ouderen",
        )
        self.assertTrue(format_input["readiness_summary"]["can_populate_format_as_concept"])
        self.assertFalse(format_input["readiness_summary"]["can_populate_format_as_confirmed"])

        rpi_fields = {
            field["field_id"]: field
            for field in format_input["regional_prevention_infrastructure_alignment"]["format_fields"]
        }
        self.assertEqual(
            rpi_fields["rpi_explanation"]["information_status"],
            "source_backed_current_information",
        )
        self.assertIn("mandaatgemeente", rpi_fields["rpi_explanation"]["draft_input_for_15_september"])
        self.assertEqual(
            rpi_fields["financial_resources"]["information_status"],
            "finance_controller_validation_needed",
        )
        self.assertEqual(
            rpi_fields["regional_health_goals"]["information_status"],
            "validation_needed",
        )

        component_fields = format_input["component_format_fields"]
        self.assertEqual(
            component_fields["current_state"]["urgency"]["information_status"],
            "source_backed_current_information",
        )
        self.assertEqual(
            component_fields["current_state"]["current_situation"]["information_status"],
            "likely_or_indicated",
        )
        self.assertEqual(
            component_fields["gap_project_plan"]["financial_plan"]["information_status"],
            "finance_controller_validation_needed",
        )
        self.assertGreaterEqual(
            len(component_fields["gap_project_plan"]["milestone_planning"]["milestone_rows"]),
            3,
        )

        statuses = {item["status_id"] for item in format_input["information_status_model"]}
        self.assertIn("confirmed_decision", statuses)
        self.assertIn("likely_or_indicated", statuses)
        self.assertIn("local_decision_needed", statuses)

    def test_adult_overweight_has_current_information_and_party_signals(self) -> None:
        objects = {item["component_id"]: item for item in self.layer["objects"]}
        adult_overweight = objects["ketenaanpak_overgewicht_obesitas_volwassenen"]

        available = adult_overweight["available_information_for_workagenda"]
        self.assertGreaterEqual(len(available["public_indicators"]), 3)
        self.assertTrue(
            any("Flevoland Gezond en Wel" in signal["statement"] for signal in available["implementation_progress_signals"])
        )
        self.assertTrue(
            any("GLI" in signal["statement"] for signal in available["implementation_progress_signals"])
        )
        self.assertTrue(available["finance_and_resource_signals"])
        format_context = adult_overweight["format_aligned_workagenda_input"]["format_component_context"]
        self.assertEqual(format_context["format_item_id"], "4a")
        self.assertEqual(format_context["leefgebied"], "Leefstijl")

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

        self.assertIn("Current sprint: Sprint 33.P9", text)
        self.assertIn("format_aligned_workagenda_input", text)
        self.assertIn("format_field_check", text)
        self.assertIn("This layer is a preparation and handoff model.", text)
        self.assertIn("not proof that unresolved local items have been decided", text)


if __name__ == "__main__":
    unittest.main()
