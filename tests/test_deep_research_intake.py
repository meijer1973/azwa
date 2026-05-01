from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HEALTHY_SCHOOL_REPORT_PATH = REPO_ROOT / "docs" / "dr" / "Healthy school.md"
DIGITAL_INFRA_REPORT_PATH = REPO_ROOT / "docs" / "dr" / "Digital and operational infrastructure.md"
INFORMAL_SUPPORT_REPORT_PATH = REPO_ROOT / "docs" / "dr" / "Informal support.md"
PGA_ZORGZAAM_FLEVER_REPORT_PATH = REPO_ROOT / "docs" / "dr" / "Zorgzaam Flevoland, and Flever interface.md"
SAMEN_STERKER_REPORT_PATH = REPO_ROOT / "docs" / "dr" / "Samen Sterker in de Wijk in Almere.md"
AUTHORITY_ADOPTION_REPORT_PATH = (
    REPO_ROOT / "docs" / "dr" / "Stronger official sources for Almere authority and adoption items.md"
)
SETTLEMENT_AUDIT_REPORT_PATH = REPO_ROOT / "docs" / "dr" / "Almere D6 Settlement Evidence Audit.md"
STAND_VAN_ZAKEN_REPORT_PATH = (
    REPO_ROOT / "docs" / "dr" / "Stable public source check for “Stand van zaken Gezondheidsbeleid (IZA en GALA)”.md"
)
CONSTRAINED_ANSWER_DESIGN_REPORT_PATH = (
    REPO_ROOT / "docs" / "dr" / "Constrained answer design for the Almere D6 open-question set.md"
)
MANIFEST_PATH = REPO_ROOT / "data" / "raw" / "manifest.json"
SOURCE_INTAKE_CANDIDATES_PATH = REPO_ROOT / "data" / "raw" / "source_intake_candidates.json"
INVENTORY_PATH = REPO_ROOT / "data" / "extracted" / "document_inventory.json"
REGISTER_PATH = REPO_ROOT / "data" / "extracted" / "municipal" / "almere_d6_responsibility_register.json"
TRIAGE_PATH = REPO_ROOT / "data" / "extracted" / "review_triage_deep_research_offload.json"
OPEN_QUESTIONS_PATH = REPO_ROOT / "docs" / "review" / "almere_d6_open_questions.md"
VALIDATION_MATRIX_PATH = REPO_ROOT / "docs" / "review" / "almere_d6_validation_ticket_matrix.md"
CONSTRAINED_ANSWER_DESIGN_INTAKE_PATH = (
    REPO_ROOT / "docs" / "source-intake" / "phase31.5-constrained-answer-design-intake.md"
)

HEALTHY_SCHOOL_SOURCE_IDS = {
    "mun_almere_gezonde_scholen",
    "mun_almere_gezond_in_almere",
    "reg_ggd_flevoland_gezonde_school",
    "reg_ggd_flevoland_ketenaanpak_gezond_gewicht_almere",
    "mun_almere_lea_2024_2028",
}

DIGITAL_OPERATIONAL_SOURCE_IDS = {
    "nat_zorgakkoorden_pga_20_miljoen_2024",
    "mun_almere_pga_regionaal_transferpunt",
    "reg_flevoziekenhuis_rtp_flevoland_2025",
    "reg_rtp_flevoland_home",
    "mun_almere_pga_rso_data_infrastructuur",
    "reg_flevoziekenhuis_thuismonitoring",
    "reg_ggd_flevoland_kadernota_2027",
    "reg_woonzorg_flevoland_beleidsplan_2026",
    "reg_npz_almere_pilot_viewer_acp",
    "reg_npz_almere_evaluatie_viewer_pzp_acp_2025",
    "nat_palliaweb_digitale_initiatieven_pzp",
    "reg_npz_almere_jaarplan_2025",
}

INFORMAL_SUPPORT_SOURCE_IDS = {
    "mun_almere_welzijnskader_2020",
    "mun_almere_subsidie_buurtontmoeting",
    "mun_almere_nadere_regels_buurtontmoeting",
    "mun_almere_wijkbudget",
    "mun_almere_ondersteuning_mantelzorg",
    "mun_almere_mantelzorgwaardering",
    "mun_almere_sociaal_domein_aanbod_jeugd_gezin",
    "mun_almere_sociale_veerkracht_almeerders",
    "mun_deschoor_buurtkamers",
    "mun_deschoor_initiatievenbureau",
    "mun_deschoor_buurtkracht",
    "mun_deschoor_opbouwwerk_almere",
    "mun_vmca_meerjarenvisie_2022_2025",
    "mun_humanitas_almere",
    "mun_almere_almeers_preventieakkoord",
    "mun_almere_wijkteams_ontmoeting",
}

PGA_ZORGZAAM_FLEVER_SOURCE_IDS = {
    "reg_ggd_flevoland_kadernota_2025",
    "reg_flever_zorgzaam_flevoland_project",
    "reg_flever_meerjarenplan_2025_2028",
    "reg_flever_inwoners_onderdeel_pga",
}

SAMEN_STERKER_SOURCE_IDS = {
    "reg_almere_zorglandschap_wmo",
    "reg_zorglandschap_wmo_uitvoeringsprogramma_2022",
    "reg_zorglandschap_wmo_monitor_2025",
    "reg_zonmw_samen_sterker_uitvoeringsplan",
    "reg_zonmw_samen_sterker_startsubsidie",
    "mun_almere_pga_samen_sterker_wijk",
    "mun_almere_subsidieregister_2023",
    "mun_almere_evaluatie_schakelteams_2021",
    "reg_samen_sterker_in_de_wijk_home",
}

SETTLEMENT_AUDIT_SOURCE_IDS = {
    "mun_almere_subsidieregister_2024",
    "mun_almere_subsidieregister_2025",
    "mun_almere_mentale_gezondheid",
    "reg_ggd_flevoland_voortgang_gala_regio_2023",
    "nat_zorgakkoorden_werkagenda_handvatten_2026",
}


def load_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


class DeepResearchIntakeTests(unittest.TestCase):
    def test_deep_research_report_is_not_manifest_source(self) -> None:
        self.assertTrue(HEALTHY_SCHOOL_REPORT_PATH.exists())
        self.assertTrue(DIGITAL_INFRA_REPORT_PATH.exists())
        self.assertTrue(INFORMAL_SUPPORT_REPORT_PATH.exists())
        self.assertTrue(PGA_ZORGZAAM_FLEVER_REPORT_PATH.exists())
        self.assertTrue(SAMEN_STERKER_REPORT_PATH.exists())
        self.assertTrue(AUTHORITY_ADOPTION_REPORT_PATH.exists())
        self.assertTrue(SETTLEMENT_AUDIT_REPORT_PATH.exists())
        self.assertTrue(STAND_VAN_ZAKEN_REPORT_PATH.exists())
        self.assertTrue(CONSTRAINED_ANSWER_DESIGN_REPORT_PATH.exists())
        manifest = load_json(MANIFEST_PATH)
        self.assertFalse(any(entry["file_path"] == "docs/dr/Healthy school.md" for entry in manifest))
        self.assertFalse(
            any(entry["file_path"] == "docs/dr/Digital and operational infrastructure.md" for entry in manifest)
        )
        self.assertFalse(any(entry["file_path"] == "docs/dr/Informal support.md" for entry in manifest))
        self.assertFalse(
            any(entry["file_path"] == "docs/dr/Zorgzaam Flevoland, and Flever interface.md" for entry in manifest)
        )
        self.assertFalse(
            any(entry["file_path"] == "docs/dr/Samen Sterker in de Wijk in Almere.md" for entry in manifest)
        )
        self.assertFalse(
            any(
                entry["file_path"] == "docs/dr/Stronger official sources for Almere authority and adoption items.md"
                for entry in manifest
            )
        )
        self.assertFalse(
            any(entry["file_path"] == "docs/dr/Almere D6 Settlement Evidence Audit.md" for entry in manifest)
        )
        self.assertFalse(
            any(
                entry["file_path"]
                == "docs/dr/Stable public source check for “Stand van zaken Gezondheidsbeleid (IZA en GALA)”.md"
                for entry in manifest
            )
        )
        self.assertFalse(
            any(
                entry["file_path"] == "docs/dr/Constrained answer design for the Almere D6 open-question set.md"
                for entry in manifest
            )
        )

    def test_healthy_school_sources_are_ingested(self) -> None:
        manifest = load_json(MANIFEST_PATH)
        manifest_ids = {entry["document_id"] for entry in manifest}
        self.assertTrue(HEALTHY_SCHOOL_SOURCE_IDS.issubset(manifest_ids))

        inventory = load_json(INVENTORY_PATH)
        inventory_ids = {entry["document_id"] for entry in inventory["documents"]}
        self.assertTrue(HEALTHY_SCHOOL_SOURCE_IDS.issubset(inventory_ids))

    def test_digital_operational_sources_are_ingested(self) -> None:
        manifest = load_json(MANIFEST_PATH)
        manifest_ids = {entry["document_id"] for entry in manifest}
        self.assertTrue(DIGITAL_OPERATIONAL_SOURCE_IDS.issubset(manifest_ids))

        inventory = load_json(INVENTORY_PATH)
        inventory_ids = {entry["document_id"] for entry in inventory["documents"]}
        self.assertTrue(DIGITAL_OPERATIONAL_SOURCE_IDS.issubset(inventory_ids))

    def test_informal_support_sources_are_ingested(self) -> None:
        manifest = load_json(MANIFEST_PATH)
        manifest_ids = {entry["document_id"] for entry in manifest}
        self.assertTrue(INFORMAL_SUPPORT_SOURCE_IDS.issubset(manifest_ids))

        inventory = load_json(INVENTORY_PATH)
        inventory_ids = {entry["document_id"] for entry in inventory["documents"]}
        self.assertTrue(INFORMAL_SUPPORT_SOURCE_IDS.issubset(inventory_ids))

    def test_pga_zorgzaam_flever_sources_are_ingested(self) -> None:
        manifest = load_json(MANIFEST_PATH)
        manifest_ids = {entry["document_id"] for entry in manifest}
        self.assertTrue(PGA_ZORGZAAM_FLEVER_SOURCE_IDS.issubset(manifest_ids))

        inventory = load_json(INVENTORY_PATH)
        inventory_ids = {entry["document_id"] for entry in inventory["documents"]}
        self.assertTrue(PGA_ZORGZAAM_FLEVER_SOURCE_IDS.issubset(inventory_ids))

    def test_samen_sterker_sources_are_ingested(self) -> None:
        manifest = load_json(MANIFEST_PATH)
        manifest_ids = {entry["document_id"] for entry in manifest}
        self.assertTrue(SAMEN_STERKER_SOURCE_IDS.issubset(manifest_ids))

        inventory = load_json(INVENTORY_PATH)
        inventory_ids = {entry["document_id"] for entry in inventory["documents"]}
        self.assertTrue(SAMEN_STERKER_SOURCE_IDS.issubset(inventory_ids))

    def test_settlement_audit_sources_are_ingested(self) -> None:
        manifest = load_json(MANIFEST_PATH)
        manifest_ids = {entry["document_id"] for entry in manifest}
        self.assertTrue(SETTLEMENT_AUDIT_SOURCE_IDS.issubset(manifest_ids))

        inventory = load_json(INVENTORY_PATH)
        inventory_ids = {entry["document_id"] for entry in inventory["documents"]}
        self.assertTrue(SETTLEMENT_AUDIT_SOURCE_IDS.issubset(inventory_ids))

    def test_healthy_school_findings_reach_d6_register(self) -> None:
        register = load_json(REGISTER_PATH)
        row = next(
            component
            for component in register["components"]
            if component["component_id"] == "gezonde_school_mentale_gezonde_school"
        )
        evidence_sources = set(row["evidence_source"])
        self.assertTrue(HEALTHY_SCHOOL_SOURCE_IDS.issubset(evidence_sources))
        self.assertIsNotNone(row["existing_almere_provision"])
        self.assertNotEqual(row["decision_status"], "settled")
        self.assertTrue(row["needs_human_review"])

    def test_digital_operational_findings_reach_d6_register(self) -> None:
        register = load_json(REGISTER_PATH)
        row = next(
            component
            for component in register["components"]
            if component["component_id"] == "digital_operational_infrastructure"
        )
        evidence_sources = set(row["evidence_source"])
        self.assertTrue(DIGITAL_OPERATIONAL_SOURCE_IDS.issubset(evidence_sources))
        self.assertIsNotNone(row["existing_almere_provision"])
        self.assertEqual(row["decision_status"], "inferred")
        self.assertNotEqual(row["decision_status"], "settled")
        self.assertTrue(row["needs_human_review"])

    def test_informal_support_findings_reach_d6_register(self) -> None:
        register = load_json(REGISTER_PATH)
        inloop_row = next(
            component
            for component in register["components"]
            if component["component_id"] == "inloopvoorzieningen_sociaal_en_gezond"
        )
        informal_row = next(
            component
            for component in register["components"]
            if component["component_id"] == "citizen_initiatives_informal_support"
        )

        inloop_evidence = set(inloop_row["evidence_source"])
        informal_evidence = set(informal_row["evidence_source"])
        self.assertTrue(
            {
                "mun_almere_subsidie_buurtontmoeting",
                "mun_almere_nadere_regels_buurtontmoeting",
                "mun_deschoor_buurtkamers",
                "mun_almere_wijkteams_ontmoeting",
            }.issubset(inloop_evidence)
        )
        self.assertTrue(
            {
                "mun_almere_wijkbudget",
                "mun_almere_ondersteuning_mantelzorg",
                "mun_deschoor_buurtkracht",
                "mun_vmca_meerjarenvisie_2022_2025",
                "mun_humanitas_almere",
            }.issubset(informal_evidence)
        )
        self.assertEqual(inloop_row["decision_status"], "inferred")
        self.assertEqual(informal_row["decision_status"], "inferred")
        self.assertNotEqual(inloop_row["decision_status"], "settled")
        self.assertNotEqual(informal_row["decision_status"], "settled")
        self.assertTrue(inloop_row["needs_human_review"])
        self.assertTrue(informal_row["needs_human_review"])

    def test_pga_zorgzaam_flever_findings_reach_d6_register(self) -> None:
        register = load_json(REGISTER_PATH)
        row = next(
            component
            for component in register["components"]
            if component["component_id"] == "pga_zorgzaam_flevoland_interface"
        )
        evidence_sources = set(row["evidence_source"])
        self.assertTrue(PGA_ZORGZAAM_FLEVER_SOURCE_IDS.issubset(evidence_sources))
        self.assertIn("PGA as local transformation programme", row["existing_almere_provision"])
        self.assertEqual(row["decision_status"], "inferred")
        self.assertNotEqual(row["decision_status"], "settled")
        self.assertTrue(row["needs_human_review"])

    def test_samen_sterker_findings_reach_d6_register(self) -> None:
        register = load_json(REGISTER_PATH)
        row = next(
            component
            for component in register["components"]
            if component["component_id"] == "samen_sterker_wijk_mental_health"
        )
        evidence_sources = set(row["evidence_source"])
        self.assertTrue(SAMEN_STERKER_SOURCE_IDS.issubset(evidence_sources))
        self.assertIn("Zorglandschap Wmo", row["existing_almere_provision"])
        self.assertEqual(row["decision_status"], "inferred")
        self.assertNotEqual(row["decision_status"], "settled")
        self.assertTrue(row["needs_human_review"])

    def test_settlement_audit_keeps_d6_rows_unsettled(self) -> None:
        register = load_json(REGISTER_PATH)
        triage = load_json(TRIAGE_PATH)

        self.assertEqual(register["summary"]["settled_count"], 0)
        self.assertEqual(register["summary"]["component_count"], 12)
        self.assertEqual(triage["summary"]["d6_rows_requiring_human_validation"], 12)
        self.assertEqual(triage["summary"]["d6_rows_with_named_public_search_gap"], 0)

        funding_row = next(
            component
            for component in register["components"]
            if component["component_id"] == "funding_budget_alignment"
        )
        self.assertTrue(SETTLEMENT_AUDIT_SOURCE_IDS.intersection(funding_row["evidence_source"]))
        self.assertNotEqual(funding_row["decision_status"], "settled")
        self.assertTrue(funding_row["needs_human_review"])

    def test_stand_van_zaken_candidate_waits_for_full_text(self) -> None:
        candidates = load_json(SOURCE_INTAKE_CANDIDATES_PATH)
        candidate = next(
            item
            for item in candidates["candidate_sources"]
            if item["proposed_document_id"] == "mun_almere_stand_van_zaken_gezondheidsbeleid_iza_gala_2025"
        )
        self.assertEqual(candidate["ingestion_status"], "pending_full_text")
        self.assertIn("documentwijzer", candidate["source_url"])
        self.assertIn("full text", candidate["ingestion_note"])

        manifest = load_json(MANIFEST_PATH)
        manifest_ids = {entry["document_id"] for entry in manifest}
        self.assertNotIn("mun_almere_stand_van_zaken_gezondheidsbeleid_iza_gala_2025", manifest_ids)

        open_questions = OPEN_QUESTIONS_PATH.read_text(encoding="utf-8")
        self.assertIn("Stable Documentwijzer landing URL found", open_questions)
        self.assertIn("underlying raadsbrief text/PDF is still needed", open_questions)

    def test_constrained_answer_design_is_plain_language_handoff(self) -> None:
        self.assertTrue(CONSTRAINED_ANSWER_DESIGN_INTAKE_PATH.exists())
        matrix = VALIDATION_MATRIX_PATH.read_text(encoding="utf-8")

        self.assertIn("Which description best fits this component?", matrix)
        self.assertIn("Stakeholder Packets", matrix)
        self.assertIn("Simple Decision Rules", matrix)
        self.assertIn("The current working view is that this component may be relevant to D6", matrix)

        lower_matrix = matrix.lower()
        for internal_term in [
            "repository",
            "register",
            "prefill",
            "source intake",
            "top-layer",
            "case b",
            "case c",
            "d6 row",
            "`settled`",
            "`inferred`",
        ]:
            self.assertNotIn(internal_term, lower_matrix)


if __name__ == "__main__":
    unittest.main()
