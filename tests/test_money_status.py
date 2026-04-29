from __future__ import annotations

import unittest

from src.build_claims_top5 import money_status_for


class MoneyStatusTests(unittest.TestCase):
    def test_spuk_route_becomes_funding_route(self) -> None:
        status = money_status_for(
            "Gemeenten ontvangen vanaf 2027 via een nieuwe SPUK middelen voor D5 en D6.",
            "nat_vws_brief_azwa_d5_d6_financieringsinstrument_2026",
            "ministerial_letter",
            "direct_extraction",
            "finance.d5_d6.funding_instrument",
            "finance_arrangement",
        )

        self.assertEqual(status["status"], "funding_route")
        self.assertTrue(status["financial_signal"])

    def test_application_condition_wins_over_general_route(self) -> None:
        status = money_status_for(
            "Vaststelling van de regionale werkagenda is randvoorwaardelijk voor uitkering van middelen.",
            "nat_vng_ledenbrief_azwa_financiering_2026",
            "members_letter",
            "direct_extraction",
            "finance.d5_d6.funding_instrument",
            "finance_arrangement",
        )

        self.assertEqual(status["status"], "application_condition")

    def test_double_counting_risk_needs_verification(self) -> None:
        status = money_status_for(
            "Houd GALA/SPUK, PGA/IZA-transformatiemiddelen en AZWA-D5/SPUK middelen apart om dubbeltelling te voorkomen.",
            "nat_vws_brief_azwa_d5_d6_financieringsinstrument_2026",
            "ministerial_letter",
            "direct_extraction",
            "finance.d5_d6.municipal_funding",
            "finance_arrangement",
        )

        self.assertEqual(status["status"], "double_counting_risk")
        self.assertTrue(status["needs_verification"])

    def test_local_funding_gap_is_searchable(self) -> None:
        status = money_status_for(
            "De bronbasis laat mogelijke middelen zien, maar nog geen expliciete Almeerse keuze voor verdeling en eigenaarschap.",
            "mun_almere_pga_transformatieplan",
            "implementation_plan",
            "contextual_relevance",
            "finance.local_alignment_goal",
            "local_goal",
        )

        self.assertEqual(status["status"], "local_funding_gap")
        self.assertTrue(status["needs_verification"])

    def test_non_financial_claim_stays_not_financial(self) -> None:
        status = money_status_for(
            "Almere noemt samenwerking met lokale partners in de wijk.",
            "mun_almere_pga_transformatieplan",
            "implementation_plan",
            "contextual_relevance",
            "municipal.local_structure",
            "implementation_requirement",
        )

        self.assertEqual(status["status"], "not_financial")


if __name__ == "__main__":
    unittest.main()
