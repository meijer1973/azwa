from __future__ import annotations

import unittest

from src.build_data_quality_audit import claim_excerpt, detect_rough_issues


class DataQualityAuditTests(unittest.TestCase):
    def test_long_complete_statement_is_not_length_only_rough(self) -> None:
        statement = (
            "Deze claim beschrijft een beleidsmatige samenhang met voldoende context, een duidelijke "
            "zinsopbouw en een normale afsluiting. "
            "De tekst is bewust langer dan de lengte waarop ruwe extracties vroeger automatisch werden "
            "gemarkeerd, maar bevat geen tabelspoor, afgebroken begin of ontbrekende slotpunctuatie."
        )

        self.assertGreater(len(statement), 240)
        self.assertNotIn("unverified_extraction_length", detect_rough_issues(statement))

    def test_long_lowercase_fragment_is_flagged(self) -> None:
        statement = (
            "waarbij lokale partijen, regionale partners en uitvoerders samen werken aan een lange "
            "afgebroken bronpassage die wel veel woorden bevat maar niet als zelfstandige claim begint "
            "en daardoor door menselijke review moet worden bekeken voordat de tekst publiek gebruikt "
            "wordt in een dashboard of beleidsmatige samenvatting"
        )

        self.assertGreater(len(statement), 240)
        self.assertIn("unverified_extraction_length", detect_rough_issues(statement))

    def test_long_table_merge_fingerprint_is_flagged(self) -> None:
        statement = (
            "Deze bronpassage bevat een tabelspoor met jaren 2026 2027 2028 en meerdere kolommen die "
            "mogelijk in een lopende tekst zijn samengevoegd. "
            "De rest van de zin is lang genoeg om de detectie op extractielengte te activeren, zodat de "
            "audit dit niet als publicatieklare claim behandelt zonder extra controle."
        )

        self.assertGreater(len(statement), 240)
        self.assertIn("unverified_extraction_length", detect_rough_issues(statement))

    def test_claim_excerpt_uses_wider_review_window(self) -> None:
        statement = " ".join(["woord"] * 90)
        excerpt = claim_excerpt(statement)

        self.assertEqual(len(excerpt), 400)
        self.assertTrue(excerpt.endswith("..."))


if __name__ == "__main__":
    unittest.main()
