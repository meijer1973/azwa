from __future__ import annotations

import unittest
from datetime import date

import src.build_review_triage as review_triage


class ReviewTriageTests(unittest.TestCase):
    def test_review_triage_routes_current_review_queue(self) -> None:
        triage = review_triage.build_review_triage(date(2026, 4, 30))
        summary = triage["summary"]

        self.assertEqual(triage["current_sprint"], "Sprint 31.4 - Review triage and deep-research offload")
        self.assertEqual(summary["review_queue_items"], 387)
        self.assertEqual(summary["human_review_round_items"], 387)
        self.assertEqual(summary["deep_research_assignment_count"], 6)
        self.assertEqual(
            summary["bucket_counts"],
            {
                "pipeline_or_extraction_cleanup": 10,
                "mixed_public_search_then_human": 120,
                "human_only": 58,
                "deep_research_candidate": 199,
            },
        )

    def test_deep_research_does_not_settle_d6_rows(self) -> None:
        triage = review_triage.build_review_triage(date(2026, 4, 30))

        self.assertEqual(triage["summary"]["d6_rows_requiring_human_validation"], 12)
        self.assertEqual(triage["summary"]["d6_rows_with_named_public_search_gap"], 3)
        self.assertIn("No D6 responsibility-register row may move to settled", triage["d6_guardrail"])
        for assignment in triage["deep_research_assignments"]:
            self.assertTrue(assignment["may_resolve"])
            self.assertTrue(assignment["must_not_resolve"])

    def test_markdown_and_prompts_are_ready_for_agents(self) -> None:
        triage = review_triage.build_review_triage(date(2026, 4, 30))
        note = review_triage.render_markdown(triage)
        prompts = review_triage.render_prompts(triage)

        self.assertIn("Triage Buckets", note)
        self.assertIn("Deep-Research Assignments", note)
        self.assertIn("dr_gezonde_school_almere", prompts)
        self.assertIn("dr_digitale_operationele_infrastructuur", prompts)
        self.assertIn("Must not resolve", prompts)


if __name__ == "__main__":
    unittest.main()
