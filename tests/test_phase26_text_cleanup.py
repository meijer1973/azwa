from __future__ import annotations

import unittest

from src.build_document_extractions import clean_candidate_statement, is_hard_noise_candidate, is_noise_candidate
from src.build_claims_top5 import (
    apply_claim_dedup,
    has_invalid_sentence_start,
    should_reject_for_sentence_boundary,
)
from src.build_structural_extractions import (
    is_structural_noise_line,
    repair_mojibake,
    voting_records_from_text,
)


class Phase26TextCleanupTests(unittest.TestCase):
    def test_structural_filters_remove_toc_drupal_and_voting_lines(self) -> None:
        self.assertTrue(is_structural_noise_line("1.3 Totstandkoming van de keuzes van Almere voor 2024-2026 6"))
        self.assertTrue(is_structural_noise_line("[###### GGD Flevoland 2023-07-07](/article/ggd-flevoland)"))
        self.assertTrue(is_structural_noise_line("Het amendement is met 21 stemmen voor en 19 stemmen tegen aangenomen."))

    def test_mojibake_repair_handles_common_pdf_artifacts(self) -> None:
        repaired, counts = repair_mojibake("Zie â€œAnalyseâ€ en verwijder\x07 controle.")

        self.assertEqual(repaired, "Zie “Analyse” en verwijder controle.")
        self.assertTrue(counts)

    def test_document_candidate_filter_removes_letterhead_and_voting_noise(self) -> None:
        self.assertTrue(
            is_hard_noise_candidate(
                "Correspondentie uitsluitend richten aan het retouradres met vermelding van de datum en het kenmerk. "
                "Deze tabelrij bevat ook een jaartal 2026, maar blijft letterhead-ruis."
            )
        )
        self.assertTrue(
            is_noise_candidate(
                "Correspondentie uitsluitend richten aan het retouradres met vermelding van de datum en het kenmerk. "
                "Geachte voorzitter, in deze brief informeer ik de Kamer over het akkoord."
            )
        )
        self.assertTrue(
            is_noise_candidate(
                "Randvoorwaarden Stevige Lokale Teams. Het amendement is met 21 stemmen voor en 19 stemmen tegen aangenomen."
            )
        )

    def test_candidate_cleaning_preserves_substantive_bullet_text(self) -> None:
        text = "- 50 miljoen euro extra voor gemeenten, aanvullend op de bestaande SPUK IZA en de Brede SPUK GALA."

        self.assertEqual(
            clean_candidate_statement(text),
            "50 miljoen euro extra voor gemeenten, aanvullend op de bestaande SPUK IZA en de Brede SPUK GALA.",
        )

    def test_sentence_boundary_gate_rejects_mid_sentence_start(self) -> None:
        reject, reasons = should_reject_for_sentence_boundary(
            "ingang van 1 januari 2024 gelden de ketenaanpakken."
        )

        self.assertTrue(reject)
        self.assertIn("lowercase_mid_sentence_start", reasons)
        self.assertFalse(has_invalid_sentence_start("De ketenaanpakken gelden vanaf 2024."))

    def test_claim_dedup_keeps_longest_duplicate_opening(self) -> None:
        base_claim = {
            "source_document_id": "doc",
            "topic": "d5.example",
            "subtopic": "same",
            "statement": (
                "Dezelfde opening wordt hier gebruikt in een langere claim met genoeg woorden om de eerste "
                "tweehonderd tekens volledig identiek te maken voor de dedup-test, zodat alleen de langste "
                "variant overblijft in de claimlaag en de korte variant superseded wordt."
            ),
        }
        claims_by_document = {
            "doc": [
                {**base_claim, "claim_id": "clm__short"},
                {
                    **base_claim,
                    "claim_id": "clm__long",
                    "statement": (
                        base_claim["statement"]
                        + " Extra context wint omdat deze claim dezelfde opening heeft maar meer inhoud bevat."
                    ),
                },
            ]
        }
        filtered, log = apply_claim_dedup(claims_by_document)

        self.assertEqual([claim["claim_id"] for claim in filtered["doc"]], ["clm__long"])
        self.assertEqual(log["superseded_claim_count"], 1)

    def test_voting_records_are_preserved_outside_claim_input(self) -> None:
        entry = {"document_id": "mun_almere_test", "file_path": "data/raw/test.html", "source_url": "https://example.test"}
        records = voting_records_from_text(
            entry,
            "De motie is met 8 stemmen voor en 32 stemmen tegen verworpen.\nGeen stemuitslag op deze regel.",
        )

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["record_type"], "voting_result")


if __name__ == "__main__":
    unittest.main()
