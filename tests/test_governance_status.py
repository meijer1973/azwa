from __future__ import annotations

import unittest

from src.build_claims_top5 import governance_status_for


class GovernanceStatusTests(unittest.TestCase):
    def test_decision_role_detects_council_decision(self) -> None:
        status = governance_status_for(
            "De gemeenteraad heeft het geamendeerde raadsvoorstel vastgesteld.",
            "mun_almere_2026_stevige_lokale_teams_besluitenlijst",
            "municipal_policy",
            "direct_extraction",
            "municipal.role_allocation",
            "governance_requirement",
        )

        self.assertEqual(status["status"], "decision_role")
        self.assertIn("gemeenteraad", status["actor_signals"])

    def test_coordination_role_stays_separate_from_execution(self) -> None:
        status = governance_status_for(
            "Partijen werken onder regie van de mandaatgemeente aan regionale afstemming.",
            "nat_azwa_opdracht_werkagenda_d5_2026",
            "assignment",
            "direct_extraction",
            "governance.regional_coordination",
            "governance_arrangement",
        )

        self.assertEqual(status["status"], "coordination_role")
        self.assertIn("mandaatgemeente", status["actor_signals"])

    def test_governance_gap_needs_verification(self) -> None:
        status = governance_status_for(
            "De bronbasis laat nog geen expliciete eigenaar of besluitroute voor lokale financiering zien.",
            "mun_almere_pga_transformatieplan",
            "implementation_plan",
            "contextual_relevance",
            "governance.local_coalition",
            "governance_arrangement",
        )

        self.assertEqual(status["status"], "governance_gap")
        self.assertTrue(status["needs_verification"])

    def test_vague_region_only_is_marked(self) -> None:
        status = governance_status_for(
            "De regio werkt aan verdere uitvoering van de afspraken.",
            "reg_flevoland_2023_regioplan_iza",
            "regional_plan",
            "direct_extraction",
            "governance.regional_coordination",
            "governance_arrangement",
        )

        self.assertTrue(status["vague_region_only"])
        self.assertTrue(status["needs_verification"])

    def test_non_governance_claim_stays_not_governance(self) -> None:
        status = governance_status_for(
            "De publicatie noemt een lokale impacthorizon voor 2029.",
            "mun_almere_pga_transformatieplan",
            "implementation_plan",
            "direct_extraction",
            "timeline.almere_2029",
            "timeline_commitment",
        )

        self.assertEqual(status["status"], "not_governance")


if __name__ == "__main__":
    unittest.main()
