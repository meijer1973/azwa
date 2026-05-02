from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
STUURMODEL_PATH = REPO_ROOT / "data" / "workagenda" / "d5_stuurmodel.json"
STATUS_MATRIX_PATH = REPO_ROOT / "data" / "workagenda" / "d5_status_matrix.json"
STATUS_MATRIX_DOC_PATH = REPO_ROOT / "docs" / "workagenda-d5-statusmatrix.md"


class WorkagendaD5StatusMatrixTests(unittest.TestCase):
    def test_status_matrix_matches_stuurmodel_scope(self) -> None:
        stuurmodel = json.loads(STUURMODEL_PATH.read_text(encoding="utf-8"))
        matrix = json.loads(STATUS_MATRIX_PATH.read_text(encoding="utf-8"))

        stuurmodel_ids = [target["target_id"] for target in stuurmodel["d5_scope"]]
        matrix_ids = [row["target_id"] for row in matrix["rows"]]

        self.assertEqual(matrix_ids, stuurmodel_ids)
        self.assertEqual(matrix["summary"]["target_count"], 11)
        self.assertEqual(matrix["summary"]["required_target_count"], 9)

    def test_every_field_status_uses_contract_code(self) -> None:
        stuurmodel = json.loads(STUURMODEL_PATH.read_text(encoding="utf-8"))
        matrix = json.loads(STATUS_MATRIX_PATH.read_text(encoding="utf-8"))
        valid_codes = {item["code"] for item in stuurmodel["delivery_status_values"]}

        for row in matrix["rows"]:
            self.assertFalse(row["ready_for_workagenda_drafting"])
            for cell in row["field_statuses"].values():
                self.assertIn(cell["status_code"], valid_codes)

    def test_required_rows_expose_delivery_blockers(self) -> None:
        matrix = json.loads(STATUS_MATRIX_PATH.read_text(encoding="utf-8"))
        required_rows = [row for row in matrix["rows"] if row["required_in_workagenda"]]

        self.assertEqual(len(required_rows), 9)
        for row in required_rows:
            self.assertIn(row["risk"], {"geel", "rood"})
            self.assertEqual(row["finance_status"], "controllercheck_nodig")
            self.assertEqual(row["governance_status"], "eigenaar_onbekend")
            self.assertEqual(row["decision_status"], "besluit_nodig")
            self.assertTrue(row["d6_dependency_hints"])

    def test_optional_rows_stay_out_of_required_workagenda_until_scope_choice(self) -> None:
        matrix = json.loads(STATUS_MATRIX_PATH.read_text(encoding="utf-8"))
        optional_rows = [row for row in matrix["rows"] if not row["required_in_workagenda"]]

        self.assertEqual(len(optional_rows), 2)
        for row in optional_rows:
            self.assertEqual(row["risk"], "grijs")
            self.assertIn("optional/conditional", row["next_action"])
            self.assertTrue(all(cell["status_code"] == "I" for cell in row["field_statuses"].values()))

    def test_human_statusmatrix_names_sprint_and_guardrail(self) -> None:
        text = STATUS_MATRIX_DOC_PATH.read_text(encoding="utf-8")

        self.assertIn("Current sprint: Sprint 32.1", text)
        self.assertIn("No row is ready for drafting yet", text)
        self.assertIn("Do not turn yellow or red rows into final workagenda text", text)


if __name__ == "__main__":
    unittest.main()
