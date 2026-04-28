from __future__ import annotations

import unittest

from src.build_claims_top5 import time_status_for


class TimeStatusTests(unittest.TestCase):
    def test_deadline_signal_becomes_formal_deadline(self) -> None:
        status = time_status_for(
            "De specifieke uitkering wordt uiterlijk op 31 maart 2027 aangevraagd.",
            "nat_wetten_spuk_transformatiemiddelen_regeling",
            "regulation",
            "direct_extraction",
            "timeline.other",
            "timeline_commitment",
        )

        self.assertEqual(status["status"], "formal_deadline")
        self.assertEqual(status["date_signal"], "exact_date")

    def test_expected_quarter_is_not_deadline(self) -> None:
        status = time_status_for(
            "Het aanvullende regioplan is naar verwachting in Q3 2026 gereed.",
            "nat_vng_ledenbrief_onderhandelaarsakkoord_azwa_2025",
            "members_letter",
            "direct_extraction",
            "timeline.d5_d6_implementation",
            "timeline_commitment",
        )

        self.assertEqual(status["status"], "expected_moment")
        self.assertTrue(status["needs_review"])

    def test_local_governance_calendar_stays_context(self) -> None:
        status = time_status_for(
            "Het vergaderschema noemt de benoeming van de raad op 1 april 2026.",
            "mun_almere_raad_vergaderschema_2026",
            "municipal_policy",
            "direct_extraction",
            "timeline.local_governance_calendar",
            "local_calendar_milestone",
        )

        self.assertEqual(status["status"], "local_planning_context")
        self.assertIn("lokale bestuurlijke context", status["public_wording_guardrail"])

    def test_undated_claim_stays_undated_context(self) -> None:
        status = time_status_for(
            "Almere noemt samenwerking met lokale partners in de wijk.",
            "mun_almere_pga_transformatieplan",
            "implementation_plan",
            "contextual_relevance",
            "municipal.local_structure",
            "implementation_requirement",
        )

        self.assertEqual(status["status"], "undated_context")
        self.assertTrue(status["needs_review"])


if __name__ == "__main__":
    unittest.main()
