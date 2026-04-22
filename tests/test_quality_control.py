from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
QC_REPORT_PATH = REPO_ROOT / "data" / "extracted" / "qc_report.json"
REVIEW_QUEUE_PATH = REPO_ROOT / "data" / "extracted" / "review_queue.json"
CONFLICT_REGISTER_PATH = REPO_ROOT / "data" / "extracted" / "claims" / "conflict_register.json"
D5_D6_MASTER_PATH = REPO_ROOT / "data" / "extracted" / "claims" / "d5_d6_master.json"
ALMERE_VIEW_PATH = REPO_ROOT / "data" / "extracted" / "municipal" / "almere_current_view.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class QualityControlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.qc_report = load_json(QC_REPORT_PATH)
        self.review_queue = load_json(REVIEW_QUEUE_PATH)
        self.conflict_register = load_json(CONFLICT_REGISTER_PATH)
        self.master_view = load_json(D5_D6_MASTER_PATH)
        self.almere_view = load_json(ALMERE_VIEW_PATH)

    def test_qc_outputs_exist(self) -> None:
        self.assertTrue(QC_REPORT_PATH.exists())
        self.assertTrue(REVIEW_QUEUE_PATH.exists())

    def test_review_queue_summary_matches_items(self) -> None:
        items = self.review_queue["items"]
        summary = self.review_queue["summary"]
        self.assertEqual(summary["item_count"], len(items))
        self.assertEqual(summary["blocking"], sum(1 for item in items if item["severity"] == "blocking"))
        self.assertEqual(summary["warning"], sum(1 for item in items if item["severity"] == "warning"))
        self.assertEqual(summary["review"], sum(1 for item in items if item["severity"] == "review"))

    def test_qc_report_has_no_blocking_issues(self) -> None:
        self.assertEqual(self.qc_report["summary"]["blocking"], 0)

    def test_unresolved_conflicts_propagate_to_views(self) -> None:
        unresolved_topics = {
            entry["topic"]
            for entry in self.conflict_register["conflicts"]
            if entry["resolution_status"] != "resolved"
        }
        master_topics = {entry["topic"] for entry in self.master_view["unresolved_conflicts"]}
        almere_topics = {entry["topic"] for entry in self.almere_view["unresolved_conflicts"]}
        self.assertTrue(unresolved_topics.issubset(master_topics))
        self.assertTrue(unresolved_topics.issubset(almere_topics))


if __name__ == "__main__":
    unittest.main()
