from __future__ import annotations

import unittest

from src.build_claims_top5 import locality_status_for


class LocalityStatusTests(unittest.TestCase):
    def test_municipal_almere_source_is_explicit_almere(self) -> None:
        status = locality_status_for(
            "De gemeente Almere werkt aan lokale samenwerking.",
            "mun_almere_pga_transformatieplan",
            "municipal",
            "direct_extraction",
            "municipal.almere_context",
        )

        self.assertEqual(status["status"], "explicit_almere")
        self.assertEqual(status["locality_scope"], "Almere")

    def test_flevoland_source_is_explicit_flevoland(self) -> None:
        status = locality_status_for(
            "GGD Flevoland beschrijft regionale monitoring.",
            "reg_ggd_flevoland_begroting_2026",
            "regional",
            "direct_extraction",
            "monitoring.regional_monitoring_plan",
        )

        self.assertEqual(status["status"], "explicit_flevoland")
        self.assertIn("GGD-regio", status["regional_split_signals"])

    def test_national_claim_with_local_relevance_is_not_local_adoption(self) -> None:
        status = locality_status_for(
            "Gemeenten werken de basisfunctionaliteiten uit.",
            "nat_azwa_2025_definitief",
            "national",
            "direct_extraction",
            "municipal.implementation_translation",
        )

        self.assertEqual(status["status"], "national_with_local_relevance")
        self.assertTrue(status["needs_verification"])

    def test_local_adoption_gap_is_visible(self) -> None:
        status = locality_status_for(
            "De lokale uitwerking is nog geen expliciete Almeerse keuze in openbare stukken.",
            "nat_azwa_2025_definitief",
            "national",
            "contextual_relevance",
            "municipal.implementation_translation",
        )

        self.assertEqual(status["status"], "local_adoption_gap")

    def test_national_general_stays_national(self) -> None:
        status = locality_status_for(
            "Het akkoord beschrijft landelijke afspraken tussen partijen.",
            "nat_azwa_2025_definitief",
            "national",
            "direct_extraction",
            "d5.definition",
        )

        self.assertEqual(status["status"], "national_general")

    def test_unmatched_source_uses_general_context_not_dead_enum(self) -> None:
        status = locality_status_for(
            "Algemene samenwerking zonder lokale plaatsnaam.",
            "external_unknown",
            "other",
            "direct_extraction",
            "d5.definition",
        )

        self.assertEqual(status["status"], "national_general")
        self.assertEqual(status["locality_scope"], "general")


if __name__ == "__main__":
    unittest.main()
