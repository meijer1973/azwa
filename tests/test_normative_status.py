from __future__ import annotations

import unittest

from src.build_claims_top5 import normative_status_for


class NormativeStatusTests(unittest.TestCase):
    def test_binding_requires_binding_instrument_and_norm_language(self) -> None:
        status = normative_status_for(
            "Gemeenten moeten de aanvraag uiterlijk indienen.",
            "regulation",
            {"can_create_binding_obligation": True},
            "direct_extraction",
            "finance.d5_d6.funding_instrument",
        )

        self.assertEqual(status["status"], "binding")
        self.assertFalse(status["needs_attribution"])

    def test_agreement_is_not_treated_as_legal_binding(self) -> None:
        status = normative_status_for(
            "Partijen spreken af dat de basisfunctionaliteiten worden doorontwikkeld.",
            "agreement",
            {"can_create_binding_obligation": True},
            "direct_extraction",
            "d5.regional_workagenda",
        )

        self.assertEqual(status["status"], "agreement")
        self.assertIn("niet automatisch", status["public_wording_guardrail"])

    def test_lower_authority_norm_signal_needs_attribution(self) -> None:
        status = normative_status_for(
            "De VNG FAQ vermeldt dat gemeenten deze middelen moeten verantwoorden.",
            "faq",
            {"can_create_binding_obligation": False},
            "direct_extraction",
            "finance.d5_d6.funding_instrument",
        )

        self.assertEqual(status["status"], "lower_authority_signal")
        self.assertTrue(status["needs_attribution"])

    def test_contextual_claim_without_norm_signal_stays_contextual(self) -> None:
        status = normative_status_for(
            "Almere noemt samenwerking met lokale partners in de wijk.",
            "municipal_policy",
            {"can_create_binding_obligation": False},
            "contextual_relevance",
            "municipal.local_structure",
        )

        self.assertEqual(status["status"], "contextual")
        self.assertTrue(status["needs_attribution"])


if __name__ == "__main__":
    unittest.main()
