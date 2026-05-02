from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
STUURMODEL_PATH = REPO_ROOT / "data" / "workagenda" / "d5_stuurmodel.json"
STUURMODEL_DOC_PATH = REPO_ROOT / "docs" / "workagenda-d5-stuurmodel.md"


class WorkagendaD5StuurmodelTests(unittest.TestCase):
    def test_status_contract_has_expected_codes(self) -> None:
        model = json.loads(STUURMODEL_PATH.read_text(encoding="utf-8"))
        codes = [item["code"] for item in model["delivery_status_values"]]
        self.assertEqual(codes, list("ABCDEFGHIJ"))
        self.assertEqual(len({item["status"] for item in model["delivery_status_values"]}), 10)

    def test_d5_scope_matches_delivery_contract(self) -> None:
        model = json.loads(STUURMODEL_PATH.read_text(encoding="utf-8"))
        target_ids = {target["target_id"] for target in model["d5_scope"]}

        self.assertEqual(len(model["d5_scope"]), 11)
        self.assertEqual(sum(1 for target in model["d5_scope"] if target["required_in_workagenda"]), 9)
        self.assertIn("laagdrempelige_steunpunten", target_ids)
        self.assertIn("sociaal_verwijzen", target_ids)
        self.assertIn("mentale_gezondheidsnetwerken", target_ids)
        self.assertIn("ontwikkelagenda_1_nieuw_beproeven", target_ids)
        self.assertIn("ontwikkelagenda_2_overige_initiatieven", target_ids)

    def test_stuurmodel_defers_later_delivery_files(self) -> None:
        model = json.loads(STUURMODEL_PATH.read_text(encoding="utf-8"))
        planned_files = set(model["planned_files"])

        self.assertIn("data/workagenda/d5_status_matrix.json", planned_files)
        self.assertIn("data/workagenda/d5_validation_tickets.json", planned_files)
        self.assertIn("data/workagenda/d5_finance_matrix.json", planned_files)
        self.assertIn("data/workagenda/d5_d6_dependency_map.json", planned_files)
        self.assertIn("data/workagenda/d5_dashboard_view.json", planned_files)

    def test_human_stuurmodel_names_current_sprint_and_guardrails(self) -> None:
        text = STUURMODEL_DOC_PATH.read_text(encoding="utf-8")

        self.assertIn("Current sprint: Sprint 32.0", text)
        self.assertIn("This stuurmodel is not a local decision", text)
        self.assertIn("Do not start workagenda drafting", text)


if __name__ == "__main__":
    unittest.main()
