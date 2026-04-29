from __future__ import annotations

import unittest
from datetime import date

import src.build_monthly_source_audit as monthly_audit


class MonthlySourceAuditTests(unittest.TestCase):
    def test_april_audit_keeps_expected_sources_on_watchlist(self) -> None:
        audit = monthly_audit.build_audit(date(2026, 4, 30), live=False)
        summary = audit["summary"]

        self.assertEqual(summary["watchlist_count"], 6)
        self.assertEqual(summary["candidate_source_count"], 16)
        self.assertEqual(summary["pending_timeline_item_count"], 3)
        self.assertEqual(summary["pending_replacement_count"], 1)
        self.assertEqual(summary["watch_status_counts"], {"not_due_yet": 6})
        self.assertFalse(audit["live_link_check"])

    def test_pending_replacement_and_timeline_items_remain_separate_from_evidence(self) -> None:
        audit = monthly_audit.build_audit(date(2026, 4, 30), live=False)
        pending_replacements = {item["proposed_document_id"] for item in audit["pending_replacements"]}
        pending_timeline_statuses = {item["status"] for item in audit["pending_timeline_items"]}

        self.assertEqual(pending_replacements, {"nat_vng_iza_azwa_wegwijzer_2026"})
        self.assertEqual(pending_timeline_statuses, {"pending_source_ingestion"})
        self.assertIn("not public evidence", audit["source_boundary"])

    def test_markdown_note_is_human_readable_and_names_current_sprint(self) -> None:
        audit = monthly_audit.build_audit(date(2026, 4, 30), live=False)
        note = monthly_audit.render_markdown(audit)

        self.assertIn("Current sprint: Sprint 31.2", note)
        self.assertIn("Expected Source Watchlist", note)
        self.assertIn("Pending Replacements", note)
        self.assertIn("Pending Timeline Items", note)
        self.assertIn("Link Review Items", note)
        self.assertIn("Do not turn watchlist or pending items into claims", note)


if __name__ == "__main__":
    unittest.main()
