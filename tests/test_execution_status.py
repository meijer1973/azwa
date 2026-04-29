from __future__ import annotations

import unittest

from src.build_claims_top5 import execution_status_for


class ExecutionStatusTests(unittest.TestCase):
    def test_operational_requirement_detects_what_must_be_organized(self) -> None:
        status = execution_status_for(
            "Gemeenten moeten de basisfunctionaliteiten lokaal uitwerken en organiseren.",
            "nat_azwa_2025_definitief",
            "direct_extraction",
            "d5.local_translation",
            "implementation_requirement",
        )

        self.assertEqual(status["status"], "operational_requirement")
        self.assertIn("operational_requirement", status["execution_need_signals"])

    def test_decision_question_is_not_treated_as_decided_action(self) -> None:
        status = execution_status_for(
            "De bronbasis laat een besluitvraag zien over prioritering van lokale uitvoering.",
            "mun_almere_pga_transformatieplan",
            "contextual_relevance",
            "municipal.implementation_translation",
            "implementation_requirement",
        )

        self.assertEqual(status["status"], "decision_question")
        self.assertTrue(status["needs_verification"])

    def test_dependency_detects_execution_dependency(self) -> None:
        status = execution_status_for(
            "De lokale uitvoering is afhankelijk van regionale digitale aansluiting.",
            "reg_flevoland_2023_regioplan_iza",
            "direct_extraction",
            "d6.regional_infrastructure",
            "implementation_requirement",
        )

        self.assertEqual(status["status"], "dependency")
        self.assertIn("dependency", status["execution_need_signals"])

    def test_capacity_need_detects_staffing_question(self) -> None:
        status = execution_status_for(
            "De vervolgstap vraagt uitvoeringscapaciteit en fte voor de voorbereiding.",
            "nat_vng_azwa_faq_uitvoeringscapaciteit",
            "direct_extraction",
            "municipal.implementation_translation",
            "implementation_requirement",
        )

        self.assertEqual(status["status"], "capacity_need")

    def test_non_execution_claim_stays_not_execution(self) -> None:
        status = execution_status_for(
            "Het document is gepubliceerd in maart 2026.",
            "nat_azwa_2026_cw31_kamerbrief",
            "direct_extraction",
            "timeline.other",
            "timeline_commitment",
        )

        self.assertEqual(status["status"], "not_execution")


if __name__ == "__main__":
    unittest.main()
