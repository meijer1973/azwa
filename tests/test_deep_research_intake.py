from __future__ import annotations

import json
import re
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
OPERATIONAL_REPORT_PATH = REPO_ROOT / "docs" / "dr" / "azwa operational.md"
REGIONAL_GOVERNANCE_REPORT_PATH = REPO_ROOT / "docs" / "dr" / "Regional governance.md"
MANIFEST_PATH = REPO_ROOT / "data" / "raw" / "manifest.json"
SOURCE_INTAKE_CANDIDATES_PATH = REPO_ROOT / "data" / "raw" / "source_intake_candidates.json"
INVENTORY_PATH = REPO_ROOT / "data" / "extracted" / "document_inventory.json"
REGISTER_PATH = REPO_ROOT / "data" / "extracted" / "municipal" / "almere_d6_responsibility_register.json"
REGIONAL_ROLES_PATH = REPO_ROOT / "data" / "curated" / "regional_roles_and_splits_almere_flevoland.json"
D6_GOVERNANCE_PATH = REPO_ROOT / "data" / "extracted" / "d6_governance_collaboration.json"
REGIONAL_WORKAGENDA_INPUT_PATH = REPO_ROOT / "data" / "workagenda" / "almere_regional_workagenda_input_objects.json"
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

OPERATIONAL_SOURCE_IDS = {
    "reg_ggd_flevoland_valpreventie_almere_ketendocument_2026",
    "reg_ggd_flevoland_valpreventie_lelystad_2025",
    "reg_amstellandzorg_welzijn_op_recept_procesflow_2024",
    "reg_ros_friesland_zorgpad_vroegsignalering_zwangeren_2024",
    "reg_samen_nijmegen_protocol_kwetsbare_zwangere_2024",
    "nat_kind_naar_gezonder_gewicht_monitoring_matrix_2023",
    "nat_leidraad_consultatiefunctie_ggz_sociaal_domein_2024",
    "nat_pharos_brugfuncties_huisartsenzorg_sociaal_domein_2025",
}

REGIONAL_GOVERNANCE_SOURCE_IDS = {
    "reg_noordoostpolder_iza_status_memo_2024",
    "reg_provincie_flevoland_verbindende_coalitie_2024",
    "reg_zonmw_zorgzaam_flevoland_project",
    "nat_dusi_spuk_iza_2023_2026",
    "nat_vws_spuk_iza_brede_spuk_mandaatgemeente_2025",
    "reg_centrumregeling_sociaal_domein_flevoland",
    "reg_proscoop_zorgzaam_flevoland_netwerkbureau_2024",
    "reg_ggd_flevoland_bestuursrapportage_aug_2024",
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
        self.assertTrue(OPERATIONAL_REPORT_PATH.exists())
        self.assertTrue(REGIONAL_GOVERNANCE_REPORT_PATH.exists())
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
        self.assertFalse(any(entry["file_path"] == "docs/dr/azwa operational.md" for entry in manifest))
        self.assertFalse(any(entry["file_path"] == "docs/dr/Regional governance.md" for entry in manifest))

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

    def test_operational_sources_are_ingested(self) -> None:
        manifest = load_json(MANIFEST_PATH)
        manifest_ids = {entry["document_id"] for entry in manifest}
        self.assertTrue(OPERATIONAL_SOURCE_IDS.issubset(manifest_ids))

        inventory = load_json(INVENTORY_PATH)
        inventory_ids = {entry["document_id"] for entry in inventory["documents"]}
        self.assertTrue(OPERATIONAL_SOURCE_IDS.issubset(inventory_ids))

    def test_regional_governance_sources_are_ingested(self) -> None:
        manifest = load_json(MANIFEST_PATH)
        manifest_ids = {entry["document_id"] for entry in manifest}
        self.assertTrue(REGIONAL_GOVERNANCE_SOURCE_IDS.issubset(manifest_ids))

        inventory = load_json(INVENTORY_PATH)
        inventory_ids = {entry["document_id"] for entry in inventory["documents"]}
        self.assertTrue(REGIONAL_GOVERNANCE_SOURCE_IDS.issubset(inventory_ids))

    def test_operational_findings_reach_top_layers(self) -> None:
        claims_path = REPO_ROOT / "data" / "extracted" / "claims" / "claims_master.jsonl"
        source_ids_with_claims = set()
        operational_claim_count = 0
        for line in claims_path.read_text(encoding="utf-8").splitlines():
            claim = json.loads(line)
            if claim.get("source_document_id") in OPERATIONAL_SOURCE_IDS:
                source_ids_with_claims.add(claim["source_document_id"])
                operational_claim_count += 1

        self.assertEqual(source_ids_with_claims, OPERATIONAL_SOURCE_IDS)
        self.assertGreaterEqual(operational_claim_count, 90)

        sources_view = load_json(REPO_ROOT / "data" / "site" / "site_sources_view.json")
        source_view_ids = {source["metadata"]["document_id"] for source in sources_view["sources"]}
        self.assertTrue(OPERATIONAL_SOURCE_IDS.issubset(source_view_ids))

        operational_layer = (REPO_ROOT / "data" / "extracted" / "workagenda_d5_operational_requirements.json").read_text(
            encoding="utf-8"
        )
        self.assertIn("valpreventie", operational_layer.lower())
        self.assertIn("welzijn op recept", operational_layer.lower())
        self.assertIn("brugfunctie", operational_layer.lower())

    def test_regional_governance_findings_reach_top_layers(self) -> None:
        claims_path = REPO_ROOT / "data" / "extracted" / "claims" / "claims_master.jsonl"
        source_ids_with_claims = set()
        for line in claims_path.read_text(encoding="utf-8").splitlines():
            claim = json.loads(line)
            if claim.get("source_document_id") in REGIONAL_GOVERNANCE_SOURCE_IDS:
                source_ids_with_claims.add(claim["source_document_id"])

        self.assertTrue(REGIONAL_GOVERNANCE_SOURCE_IDS.issubset(source_ids_with_claims))

        sources_view = load_json(REPO_ROOT / "data" / "site" / "site_sources_view.json")
        source_view_ids = {source["metadata"]["document_id"] for source in sources_view["sources"]}
        self.assertTrue(REGIONAL_GOVERNANCE_SOURCE_IDS.issubset(source_view_ids))

        d6_layer_text = D6_GOVERNANCE_PATH.read_text(encoding="utf-8")
        self.assertIn("Verbindende Coalitie Zorgzaam Flevoland", d6_layer_text)
        self.assertIn("Netwerkbureau Zorgzaam Flevoland", d6_layer_text)
        self.assertIn("Gemeente Almere", d6_layer_text)
        self.assertIn("IZA/AZWA-regio Flevoland", d6_layer_text)

        regional_input_text = REGIONAL_WORKAGENDA_INPUT_PATH.read_text(encoding="utf-8")
        self.assertIn("Verbindende Coalitie Zorgzaam Flevoland", regional_input_text)
        self.assertIn("Netwerkbureau Zorgzaam Flevoland", regional_input_text)
        self.assertIn("not the province", regional_input_text)

    def test_regional_roles_keep_flevoland_almere_separate(self) -> None:
        roles = load_json(REGIONAL_ROLES_PATH)
        role_ids = {role["role_id"] for role in roles["regional_roles"]}
        split_ids = {split["split_id"] for split in roles["regional_splits"]}

        self.assertIn("iza_flevoland_formal_mandaatgemeente_almere", role_ids)
        self.assertIn("verbindende_coalitie_zorgzaam_flevoland", role_ids)
        self.assertIn("netwerkbureau_zorgzaam_flevoland", role_ids)
        self.assertIn("province_flevoland_distinct_public_body", role_ids)
        self.assertIn("spuk_annex_flevoland_almere", split_ids)
        self.assertNotIn("Flevoland - Almere", roles["editorial_rule"])
        self.assertIn("combined Flevoland-and-Almere label", roles["editorial_rule"])

        almere_role = next(
            role
            for role in roles["regional_roles"]
            if role["role_id"] == "iza_flevoland_formal_mandaatgemeente_almere"
        )
        self.assertIn("Flevoland en Almere vormen samen een actor.", almere_role["does_not_mean"])

    def test_active_data_does_not_use_combined_flevoland_almere_labels(self) -> None:
        pattern = re.compile("Flevoland\\s*(?:-|\u2013|/)\\s*Almere|Almere\\s*/\\s*Flevoland")
        active_data_roots = [
            REPO_ROOT / "data" / "curated",
            REPO_ROOT / "data" / "extracted",
            REPO_ROOT / "data" / "site",
            REPO_ROOT / "data" / "workagenda",
        ]
        hits = []
        for root in active_data_roots:
            for path in root.rglob("*"):
                if path.is_file() and path.suffix.lower() in {".json", ".jsonl", ".csv"}:
                    text = path.read_text(encoding="utf-8", errors="ignore")
                    if pattern.search(text):
                        hits.append(path.relative_to(REPO_ROOT).as_posix())
        self.assertEqual([], hits)

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
