from __future__ import annotations

import unittest
from datetime import date

import src.build_human_review_round as human_review


class HumanReviewRoundTests(unittest.TestCase):
    def test_review_round_summarizes_current_queue(self) -> None:
        review_round = human_review.build_review_round(date(2026, 4, 30))
        summary = review_round["summary"]

        self.assertEqual(review_round["current_sprint"], "Sprint 31.3 - Reviewronde met menselijke beoordelaars")
        self.assertEqual(summary["review_item_count"], 387)
        self.assertEqual(summary["blocking_count"], 0)
        self.assertEqual(summary["warning_count"], 6)
        self.assertEqual(summary["review_count"], 381)
        self.assertEqual({item["perspective_id"] for item in review_round["perspectives"]}, {"norm", "time", "money", "governance", "locality", "execution"})

    def test_review_round_keeps_boundaries_visible(self) -> None:
        review_round = human_review.build_review_round(date(2026, 4, 30))

        self.assertIn("do not become source claims", review_round["decision_recording_rule"])
        self.assertIn("Do not mark D6 responsibility-register rows as settled", review_round["d6_guardrail"])
        self.assertIn("not public evidence", review_round["monthly_source_audit_summary"]["boundary"])

    def test_markdown_pack_is_human_readable(self) -> None:
        review_round = human_review.build_review_round(date(2026, 4, 30))
        note = human_review.render_markdown(review_round)

        self.assertIn("Current sprint: Sprint 31.3", note)
        self.assertIn("How To Use This Pack", note)
        self.assertIn("Perspective Review Lists", note)
        self.assertIn("Monthly Source Audit Carry-In", note)
        self.assertIn("Decision Recording Rule", note)


if __name__ == "__main__":
    unittest.main()
