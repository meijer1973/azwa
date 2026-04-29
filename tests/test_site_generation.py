from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HOME_VIEW_PATH = REPO_ROOT / "data" / "site" / "site_home_view.json"
ALMERE_VIEW_PATH = REPO_ROOT / "data" / "site" / "site_almere_view.json"
DASHBOARD_VIEW_PATH = REPO_ROOT / "data" / "site" / "dashboard_view.json"
TIMELINE_REGISTER_PATH = REPO_ROOT / "data" / "site" / "timeline_register.json"
TIMELINE_VIEW_PATH = REPO_ROOT / "data" / "site" / "site_timeline_view.json"
TIMELINE_CURATION_PATH = REPO_ROOT / "config" / "timeline_curation.json"
CLAIMS_MASTER_PATH = REPO_ROOT / "data" / "extracted" / "claims" / "claims_master.jsonl"
THEMES_VIEW_PATH = REPO_ROOT / "data" / "site" / "site_themes_view.json"
REFERENCE_VIEW_PATH = REPO_ROOT / "data" / "site" / "site_reference_view.json"
SOURCES_VIEW_PATH = REPO_ROOT / "data" / "site" / "site_sources_view.json"
UPDATES_VIEW_PATH = REPO_ROOT / "data" / "site" / "site_updates_view.json"
SITE_MANIFEST_PATH = REPO_ROOT / "data" / "site" / "site_manifest.json"
DATA_QUALITY_AUDIT_PATH = REPO_ROOT / "data" / "extracted" / "data_quality_audit.json"
DATA_QUALITY_CONFIG_PATH = REPO_ROOT / "config" / "data_quality_perspectives.json"
SOURCE_INTAKE_CANDIDATES_PATH = REPO_ROOT / "data" / "raw" / "source_intake_candidates.json"
DECISION_DIR = REPO_ROOT / "data" / "site" / "decision_view_models"
ACTION_DIR = REPO_ROOT / "data" / "site" / "action_view_models"
THEME_DIR = REPO_ROOT / "data" / "site" / "theme_view_models"
REFERENCE_TOPIC_DIR = REPO_ROOT / "data" / "site" / "reference_topic_view_models"
SOURCE_VIEW_DIR = REPO_ROOT / "data" / "site" / "source_view_models"
DIST_DIR = REPO_ROOT / "dist"
INDEX_PATH = DIST_DIR / "index.html"
ALMERE_PAGE_PATH = DIST_DIR / "almere" / "index.html"
DECISIONS_PAGE_PATH = DIST_DIR / "decisions" / "index.html"
ACTIONS_PAGE_PATH = DIST_DIR / "actions" / "index.html"
DASHBOARD_PAGE_PATH = DIST_DIR / "dashboard" / "index.html"
TIMELINE_PAGE_PATH = DIST_DIR / "timeline" / "index.html"
THEMES_PAGE_PATH = DIST_DIR / "themes" / "index.html"
REFERENCE_PAGE_PATH = DIST_DIR / "reference" / "index.html"
REFERENCE_TOPICS_PAGE_PATH = DIST_DIR / "reference" / "topics" / "index.html"
SOURCES_PAGE_PATH = DIST_DIR / "sources" / "index.html"
UPDATES_PAGE_PATH = DIST_DIR / "updates" / "index.html"
LATEST_UPDATE_ID = "upd_d6_almere_gate_remediation_intake_2026_04_27"
LATEST_UPDATE_CLAIMS_PAGE_PATH = DIST_DIR / "updates" / "claims" / LATEST_UPDATE_ID / "index.html"
VNG_FINANCING_UPDATE_ID = "upd_vng_financiering_2026_04_23"
VNG_FINANCING_UPDATE_CLAIMS_PAGE_PATH = DIST_DIR / "updates" / "claims" / VNG_FINANCING_UPDATE_ID / "index.html"
SEARCH_INDEX_PATH = DIST_DIR / "search-index.json"
SITE_BUILD_PATH = DIST_DIR / "site-build.json"
DEPLOY_WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "deploy-pages.yml"


def load_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def load_claim_ids() -> set[str]:
    return {json.loads(line)["claim_id"] for line in CLAIMS_MASTER_PATH.read_text(encoding="utf-8").splitlines()}


class SiteGenerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run([sys.executable, "src/build_site_view_models.py"], cwd=REPO_ROOT, check=True)
        subprocess.run([sys.executable, "src/build_data_quality_audit.py"], cwd=REPO_ROOT, check=True)
        subprocess.run([sys.executable, "src/render_site.py"], cwd=REPO_ROOT, check=True)

    def test_site_view_model_outputs_exist(self) -> None:
        self.assertTrue(HOME_VIEW_PATH.exists())
        self.assertTrue(ALMERE_VIEW_PATH.exists())
        self.assertTrue(DASHBOARD_VIEW_PATH.exists())
        self.assertTrue(TIMELINE_REGISTER_PATH.exists())
        self.assertTrue(SOURCE_INTAKE_CANDIDATES_PATH.exists())
        self.assertTrue(TIMELINE_VIEW_PATH.exists())
        self.assertTrue(THEMES_VIEW_PATH.exists())
        self.assertTrue(REFERENCE_VIEW_PATH.exists())
        self.assertTrue(SOURCES_VIEW_PATH.exists())
        self.assertTrue(UPDATES_VIEW_PATH.exists())
        self.assertTrue(DATA_QUALITY_AUDIT_PATH.exists())
        self.assertGreater(len(list(DECISION_DIR.glob("*.json"))), 0)
        self.assertGreater(len(list(ACTION_DIR.glob("*.json"))), 0)
        self.assertGreater(len(list(THEME_DIR.glob("*.json"))), 0)
        self.assertGreater(len(list(REFERENCE_TOPIC_DIR.glob("*.json"))), 0)
        self.assertGreater(len(list(SOURCE_VIEW_DIR.glob("*.json"))), 0)
        self.assertTrue(DATA_QUALITY_CONFIG_PATH.exists())

    def test_data_quality_taxonomy_is_saved_in_expected_locations(self) -> None:
        config = load_json(DATA_QUALITY_CONFIG_PATH)
        checklist = (REPO_ROOT / "docs" / "data-quality-checklist.md").read_text(encoding="utf-8")

        perspective_ids = {item["perspective_id"] for item in config["perspectives"]}
        classification_ids = {item["classification_id"] for item in config["classifications"]}

        self.assertEqual(
            perspective_ids,
            {"norm", "time", "money", "governance", "locality", "execution"},
        )
        self.assertEqual(
            classification_ids,
            {"source_fact", "interpretation", "local_gap", "human_choice_question"},
        )
        self.assertIn("config/data_quality_perspectives.json", checklist)
        self.assertIn("data/site/*.json", checklist)

    def test_data_quality_audit_surfaces_broad_topics_and_rough_claims(self) -> None:
        audit = load_json(DATA_QUALITY_AUDIT_PATH)

        broad_topics = {item["topic"] for item in audit["topic_bucket_audit"]["broad_rest_topics"]}
        rough_issue_counts = audit["rough_publication_claims"]["issue_counts"]
        rough_claim_ids = {item["claim_id"] for item in audit["rough_publication_claims"]["claims"]}
        site_risk_paths = {item["path"] for item in audit["site_text_risks"]["files"]}

        self.assertEqual(audit["audit_run_id"], "phase24_data_quality_audit_v1")
        self.assertIn("timeline.other", broad_topics)
        self.assertIn("monitoring.other", broad_topics)
        self.assertIn("governance_and_finance.other", broad_topics)
        self.assertIn("d5.other", broad_topics)
        self.assertIn("d6.other", broad_topics)
        self.assertGreater(rough_issue_counts["english_summary"], 0)
        self.assertGreater(rough_issue_counts["unverified_extraction_length"], 0)
        self.assertEqual(rough_issue_counts.get("raw_letterhead", 0), 0)
        self.assertNotIn("clm__nat_azwa_2026_cw31_kamerbrief_d5_002", rough_claim_ids)
        self.assertIn("data/site/decision_view_models/dec_d5_prioritering.json", site_risk_paths)
        self.assertIn("data/site/site_home_view.json", site_risk_paths)

    def test_data_quality_audit_tracks_unmapped_topics(self) -> None:
        audit = load_json(DATA_QUALITY_AUDIT_PATH)
        topic_mapping_gaps = {item["topic"] for item in audit["perspective_coverage"]["claims"]["topic_mapping_gaps"]}
        self.assertIn("governance_and_finance.other", topic_mapping_gaps)
        self.assertGreaterEqual(audit["summary"]["claims_without_perspectives"], 1)

    def test_site_view_models_carry_quality_perspectives(self) -> None:
        decision = load_json(DECISION_DIR / "dec_d5_prioritering.json")
        action = load_json(ACTION_DIR / "act_middelen_en_eigenaarschap_vastleggen.json")
        theme = load_json(THEME_DIR / "financiering.json")
        reference_topic = load_json(REFERENCE_TOPIC_DIR / "finance-d5-d6-funding-instrument.json")
        source = load_json(SOURCE_VIEW_DIR / "vws-brief-d5-d6-financieringsinstrument.json")

        self.assertEqual(decision["content_classification"]["classification_id"], "human_choice_question")
        self.assertIn("execution", decision["perspective_ids"])
        self.assertIn("governance", decision["perspective_ids"])

        self.assertEqual(action["content_classification"]["classification_id"], "human_choice_question")
        self.assertIn("money", action["perspective_ids"])
        self.assertIn("execution", action["perspective_ids"])

        self.assertEqual(theme["content_classification"]["classification_id"], "interpretation")
        self.assertIn("money", theme["perspective_ids"])

        self.assertEqual(reference_topic["content_classification"]["classification_id"], "interpretation")
        self.assertIn("money", reference_topic["perspective_ids"])

        self.assertEqual(source["content_classification"]["classification_id"], "source_fact")
        self.assertIn("money", source["perspective_ids"])
        self.assertTrue(source["quality_perspectives"])

    def test_rendered_pages_exist(self) -> None:
        for path in [
            INDEX_PATH,
            ALMERE_PAGE_PATH,
            DECISIONS_PAGE_PATH,
            ACTIONS_PAGE_PATH,
            DASHBOARD_PAGE_PATH,
            TIMELINE_PAGE_PATH,
            UPDATES_PAGE_PATH,
            LATEST_UPDATE_CLAIMS_PAGE_PATH,
            VNG_FINANCING_UPDATE_CLAIMS_PAGE_PATH,
            THEMES_PAGE_PATH,
            REFERENCE_PAGE_PATH,
            REFERENCE_TOPICS_PAGE_PATH,
            SOURCES_PAGE_PATH,
            SEARCH_INDEX_PATH,
            SITE_BUILD_PATH,
        ]:
            self.assertTrue(path.exists(), f"Missing rendered output: {path}")
        self.assertTrue((DIST_DIR / "themes" / "governance-en-regie" / "index.html").exists())
        self.assertTrue((DIST_DIR / "reference" / "topics" / "d6-local-teams" / "index.html").exists())
        self.assertTrue((DIST_DIR / "sources" / "azwa-definitief" / "index.html").exists())

    def test_home_page_contains_careful_public_wording(self) -> None:
        html = INDEX_PATH.read_text(encoding="utf-8")
        self.assertIn("AZWA D5/D6 - Almere", html)
        self.assertIn("Bestuurlijk overzicht", html)
        self.assertIn("mogelijke besluitvragen", html)
        self.assertIn("mogelijke opvolgacties", html)
        self.assertIn('href="almere/index.html"', html)
        self.assertIn('href="decisions/index.html"', html)
        self.assertIn('href="almere/index.html#landelijke-basis-zichtbaar"', html)
        self.assertIn('href="almere/index.html#menselijke-duiding"', html)
        self.assertIn('href="timeline/index.html#', html)
        self.assertIn(f'href="updates/index.html#{LATEST_UPDATE_ID}-bronnen"', html)
        self.assertIn(f'href="updates/claims/{LATEST_UPDATE_ID}/index.html"', html)
        self.assertIn(f'href="updates/index.html#{LATEST_UPDATE_ID}-tijdlijn"', html)
        self.assertIn('href="decisions/index.html?theme=', html)
        self.assertIn('href="actions/index.html?theme=', html)
        self.assertIn('href="themes/index.html"', html)
        self.assertIn("Nieuwste bronnen", html)
        self.assertIn('href="reference/index.html"', html)
        self.assertIn('href="sources/index.html"', html)

    def test_decisions_page_contains_explicit_notice(self) -> None:
        html = DECISIONS_PAGE_PATH.read_text(encoding="utf-8")
        self.assertIn("mogelijke besluitvragen", html)
        self.assertIn("geen vastgestelde gemeentelijke besluiten", html)
        self.assertIn('id="issue-filter-status"', html)
        self.assertIn('data-issue-card="decision"', html)

    def test_almere_page_contains_review_section(self) -> None:
        html = ALMERE_PAGE_PATH.read_text(encoding="utf-8")
        self.assertIn('id="menselijke-duiding"', html)
        self.assertIn("Menselijke duiding en reviewpunten", html)
        self.assertIn("lagere autoriteit vraagt menselijke duiding", html)
        self.assertIn('href="index.html#review-authority-unclear"', html)
        self.assertIn('id="review-unresolved-conflict"', html)

    def test_decision_cards_link_review_tags_to_detail_sections(self) -> None:
        html = INDEX_PATH.read_text(encoding="utf-8")
        self.assertIn('/onderbouwing/index.html#menselijke-duiding">Menselijke duiding nodig:', html)

        detail_pages = list(DECISION_DIR.glob("*.json"))
        self.assertTrue(detail_pages)
        detail_path = DIST_DIR / "decisions" / "mogelijke-besluitvraag-regiemodel-voor-d6-en-lokale-teams" / "index.html"
        evidence_path = detail_path.parent / "onderbouwing" / "index.html"
        detail_html = detail_path.read_text(encoding="utf-8")
        evidence_html = evidence_path.read_text(encoding="utf-8")

        self.assertIn('id="onderbouwing"', detail_html)
        self.assertIn("Onderbouwing en drill-down", detail_html)
        self.assertIn('href="onderbouwing/index.html#bronbasis"', detail_html)
        self.assertIn('href="onderbouwing/index.html#menselijke-duiding"', detail_html)
        self.assertIn("Bekijk volledige beleidsbasis", detail_html)
        self.assertNotIn("Bronnen die extra duiding vragen", detail_html)

        self.assertIn('id="menselijke-duiding"', evidence_html)
        self.assertIn('id="bronbasis"', evidence_html)
        self.assertIn("Terug naar hoofdtekst", evidence_html)
        self.assertIn("Bronnen die extra duiding vragen", evidence_html)
        self.assertIn("Aanbevolen vervolgstap", evidence_html)
        self.assertIn("Bronhouder: Zorgzaam Flevoland / Flever", evidence_html)
        self.assertIn("Bronstatus: Lagere-autoriteitssignaal", evidence_html)
        self.assertIn("Veilige formulering: Altijd expliciet toeschrijven", evidence_html)

    def test_logical_clickability_regression(self) -> None:
        home_html = INDEX_PATH.read_text(encoding="utf-8")
        themes_html = THEMES_PAGE_PATH.read_text(encoding="utf-8")
        reference_html = REFERENCE_PAGE_PATH.read_text(encoding="utf-8")
        sources_html = SOURCES_PAGE_PATH.read_text(encoding="utf-8")
        updates_html = UPDATES_PAGE_PATH.read_text(encoding="utf-8")

        self.assertIn('href="almere/index.html#menselijke-duiding"', home_html)
        self.assertIn(f'href="updates/index.html#{LATEST_UPDATE_ID}-bronnen"', home_html)
        self.assertIn(f'href="updates/claims/{LATEST_UPDATE_ID}/index.html"', home_html)
        self.assertIn(f'href="updates/index.html#{LATEST_UPDATE_ID}-tijdlijn"', home_html)
        self.assertIn('href="decisions/index.html?theme=governance-en-regie"', home_html)
        self.assertIn('href="actions/index.html?theme=governance-en-regie"', home_html)
        self.assertIn('class="card card--link" href="themes/index.html"', home_html)
        self.assertIn('class="card card--link" href="updates/index.html"', home_html)

        self.assertIn('href="../decisions/index.html?theme=governance-en-regie"', themes_html)
        self.assertIn('href="../actions/index.html?theme=governance-en-regie"', themes_html)

        self.assertIn('href="topics/index.html"', reference_html)
        self.assertIn('href="topics/d5-definition/index.html"', reference_html)
        self.assertIn('class="card card--link" href="topics/d5-definition/index.html"', reference_html)

        self.assertIn('href="azwa-definitief/index.html"', sources_html)
        self.assertIn('class="card card--link" href="azwa-definitief/index.html"', sources_html)

        self.assertIn(f'class="summary-box summary-box--link" href="index.html#{LATEST_UPDATE_ID}-bronnen"', updates_html)
        self.assertIn(f'class="summary-box summary-box--link" href="claims/{LATEST_UPDATE_ID}/index.html"', updates_html)
        self.assertIn(f'class="summary-box summary-box--link" href="index.html#{LATEST_UPDATE_ID}-tijdlijn"', updates_html)
        self.assertIn(f'id="{LATEST_UPDATE_ID}-wijziging-1"', updates_html)
        self.assertIn("Meer duiding", updates_html)

    def test_traceability_pages_link_internally(self) -> None:
        theme_html = (DIST_DIR / "themes" / "governance-en-regie" / "index.html").read_text(encoding="utf-8")
        topic_html = (DIST_DIR / "reference" / "topics" / "d6-local-teams" / "index.html").read_text(encoding="utf-8")
        source_html = (DIST_DIR / "sources" / "azwa-definitief" / "index.html").read_text(encoding="utf-8")

        self.assertIn('../../sources/', theme_html)
        self.assertIn('../../reference/topics/', theme_html)
        self.assertIn('../../../sources/', topic_html)
        self.assertIn('../../themes/', source_html)
        self.assertIn('../../decisions/', source_html)

    def test_timeline_page_starts_before_2027(self) -> None:
        html = TIMELINE_PAGE_PATH.read_text(encoding="utf-8")
        self.assertIn("2025-08-31", html)
        self.assertIn("2025-10-09", html)
        self.assertIn("2025-11-13", html)
        self.assertIn("2026-04-01", html)
        self.assertIn("2026-04-09", html)
        self.assertIn("23 april 2026, 12.00-13.00 uur", html)
        self.assertIn("26 mei 2026", html)
        self.assertIn("2026-05-31", html)
        self.assertIn("begin 2027", html)
        self.assertIn("2027-03-31", html)
        self.assertIn("2027-07-15", html)
        self.assertIn('class="timeline-year"', html)
        self.assertIn('id="jaar-2026" open', html)
        self.assertIn('id="jaar-2027"', html)
        self.assertIn('class="timeline-entry"', html)
        self.assertIn("Meer informatie", html)
        self.assertIn("../sources/azwa-definitief/index.html", html)
        self.assertIn("../sources/regeling-spuk-transformatiemiddelen/index.html", html)
        self.assertIn("../actions/mogelijke-opvolgactie-monitoringsaanpak-voor-almere-afstemmen/index.html", html)
        self.assertLess(html.index('id="jaar-2026" open'), html.index('id="jaar-2027"'))
        self.assertLess(html.index('id="jaar-2027"'), html.index('id="jaar-2025"'))
        self.assertLess(
            html.index("2026-03-10"),
            html.index("2026-03-31"),
        )
        self.assertLess(
            html.index("2026-03-31"),
            html.index("2026-04-01"),
        )
        self.assertLess(
            html.index("2026-04-01"),
            html.index("2026-04-09"),
        )
        self.assertLess(
            html.index("2026-04-09"),
            html.index("23 april 2026, 12.00-13.00 uur"),
        )
        self.assertLess(
            html.index("23 april 2026, 12.00-13.00 uur"),
            html.index("26 mei 2026"),
        )
        self.assertLess(
            html.index("26 mei 2026"),
            html.index("2026-05-31"),
        )
        self.assertLess(
            html.index("begin 2027"),
            html.index("2027-03-31"),
        )
        self.assertLess(
            html.index("2027-03-31"),
            html.index("2027-07-01"),
        )
        self.assertLess(
            html.index("2027-07-01"),
            html.index("2027-07-15"),
        )

    def test_timeline_register_contains_future_references(self) -> None:
        register = load_json(TIMELINE_REGISTER_PATH)
        titles = {entry["title"] for entry in register["entries"]}
        years = {year["year"] for year in register["years"]}
        self.assertIn("2026", years)
        self.assertIn("2027", years)
        self.assertIn("2030", years)
        self.assertIn("Meicirculaire gemeentefonds 2026 verwacht", titles)
        self.assertIn("Aanvraagdeadline SPUK transformatiemiddelen voor gemeenten", titles)
        self.assertIn("Uiterste verantwoording over uitgevoerde activiteiten in kalenderjaar 2026", titles)
        self.assertIn("Programmabegroting 2026 aangeboden aan de gemeenteraad", titles)
        self.assertIn("Gemeenteraadsverkiezingen 2026 in Almere", titles)
        self.assertIn("Benoeming van de raad 2026-2030", titles)
        self.assertIn("VWS en VNG-webinar over AZWA-middelen en regionale werkagenda", titles)
        self.assertIn("Landelijke thematafel Medisch-Sociaal en Preventie", titles)
        self.assertIn("VNG-ledenbrief noemt aanvullend regioplan gereed in Q3 2026", titles)
        self.assertIn("Tussentijdse evaluatie van IZA/AZWA", titles)
        self.assertIn("Startpakket sociaal domein en evaluatieperiode", titles)
        self.assertIn("Lokale impacthorizon Positief Gezond Almere", titles)

    def test_timeline_entries_carry_policy_metadata(self) -> None:
        register = load_json(TIMELINE_REGISTER_PATH)
        for entry in register["entries"]:
            self.assertIn("moment_type", entry)
            self.assertIn("source_status", entry)
            self.assertIn("authority", entry)
            self.assertIn("actor_summary", entry)
            self.assertIn("primary_perspective", entry)
            self.assertIn("timeline_policy_note", entry)
            self.assertIn(entry["primary_perspective"]["perspective_id"], {"time", "money", "governance", "execution"})
            self.assertTrue(entry["consequence_for_almere"])

        by_title = {entry["title"]: entry for entry in register["entries"]}
        self.assertEqual(
            by_title["Aanvraagdeadline SPUK transformatiemiddelen voor gemeenten"]["primary_perspective"]["perspective_id"],
            "money",
        )
        self.assertEqual(
            by_title["Gemeenteraadsverkiezingen 2026 in Almere"]["primary_perspective"]["perspective_id"],
            "governance",
        )

    def test_timeline_curation_claim_ids_resolve(self) -> None:
        curation = load_json(TIMELINE_CURATION_PATH)
        claim_ids = load_claim_ids()
        missing = []
        for entry in curation["claim_entries"]:
            for claim_id in entry.get("claim_ids", []):
                if claim_id not in claim_ids:
                    missing.append((entry["entry_key"], claim_id))

        self.assertEqual(missing, [])

    def test_timeline_page_renders_policy_metadata(self) -> None:
        html = TIMELINE_PAGE_PATH.read_text(encoding="utf-8")
        self.assertIn("Type moment", html)
        self.assertIn("Primair perspectief", html)
        self.assertIn("Bronstatus", html)
        self.assertIn("Autoriteit", html)
        self.assertIn("Actor", html)
        self.assertIn("Veilige tijdlijnlezing", html)

    def test_updates_page_contains_current_change_log(self) -> None:
        updates_view = load_json(UPDATES_VIEW_PATH)
        html = UPDATES_PAGE_PATH.read_text(encoding="utf-8")

        self.assertEqual(updates_view["latest_update"]["update_id"], LATEST_UPDATE_ID)
        self.assertIn("D6-verantwoordelijkheidsbronnen Almere aangevuld", html)
        self.assertIn("Kort samengevat", html)
        self.assertIn("Zes extra publieke bronnen zijn toegevoegd", html)
        self.assertIn('../sources/slt-geamendeerd-raadsvoorstel/index.html', html)
        self.assertIn("598", html)
        self.assertIn("Bekijk volledige controlelijst", html)
        self.assertIn("Wat is er veranderd", html)
        self.assertIn("Meer duiding", html)
        self.assertIn("Documentwijzer/Notubiz-stukken bij Stevige Lokale Teams zijn toegevoegd", html)
        self.assertIn("Samenwerkingsprojecten/Samen Sterker in de Wijk", html)
        self.assertIn("Tijdlijn", html)
        self.assertIn(f'claims/{LATEST_UPDATE_ID}/index.html', html)
        self.assertIn(f'id="{VNG_FINANCING_UPDATE_ID}"', html)
        self.assertNotIn("clm__nat_vng_ledenbrief_azwa_financiering_2026_d5_001", html)

    def test_update_human_summaries_avoid_pipeline_language(self) -> None:
        updates_view = load_json(UPDATES_VIEW_PATH)
        forbidden_pattern = re.compile(
            r"dataset|claim\s*laag|bron\s*laag|pijplijn|pipeline|data/raw|manifest|"
            r"view\s*model|site-viewmodels|review_needed|source-backed|ingest(?:ed|ie|en|ion)?|"
            r"\bjson\b|\bqc\b|machine-gegenereerd",
            re.IGNORECASE,
        )
        dutch_markers = {
            "aan",
            "als",
            "bij",
            "dat",
            "de",
            "deze",
            "die",
            "een",
            "en",
            "het",
            "in",
            "is",
            "met",
            "niet",
            "ook",
            "openbare",
            "over",
            "voor",
            "van",
            "zijn",
        }

        for update in updates_view["updates"]:
            summary = update["human_summary"]
            for field_name in ["intro", "what_happened", "what_changed", "why_it_matters"]:
                self.assertIn(field_name, summary)
                value = summary[field_name]
                self.assertIsInstance(value, str)
                self.assertGreaterEqual(len(value), 80, f"{update['update_id']} {field_name} is too short")
                normalized_words = set(re.findall(r"[a-zA-ZÀ-ÿ]+", value.lower()))
                self.assertGreaterEqual(
                    len(normalized_words & dutch_markers),
                    3,
                    f"{update['update_id']} {field_name} does not look like Dutch prose",
                )
                self.assertIsNone(
                    forbidden_pattern.search(value),
                    f"technical jargon found in {update['update_id']} {field_name}",
                )

    def test_update_claims_detail_page_contains_full_claim_list(self) -> None:
        html = VNG_FINANCING_UPDATE_CLAIMS_PAGE_PATH.read_text(encoding="utf-8")
        self.assertIn("Hoe deze controlelijst te lezen", html)
        self.assertIn("Waarom sommige fragmenten onvolledige zinnen lijken", html)
        self.assertIn("Alle betrokken bronfragmenten (64)", html)
        self.assertIn("14 claims", html)
        self.assertIn("13 claims", html)
        self.assertIn("10 claims", html)
        self.assertIn("clm__nat_vng_ledenbrief_azwa_financiering_2026_d5_001", html)
        self.assertIn("brongetrouwe", html)

    def test_update_claims_detail_explicitly_attributes_lower_authority_fragments(self) -> None:
        html = LATEST_UPDATE_CLAIMS_PAGE_PATH.read_text(encoding="utf-8")
        self.assertIn("Bronhouder: Raad van Almere", html)
        self.assertIn("Soort bron: lokaal beleids- of raadsstuk", html)
        self.assertIn("Veilige formulering: Altijd expliciet toeschrijven", html)
        self.assertIn("Volgens Raad van Almere:", html)

    def test_timeline_register_is_chronological_within_each_year(self) -> None:
        register = load_json(TIMELINE_REGISTER_PATH)
        year_to_sort_keys = {}
        for entry in register["entries"]:
            year_to_sort_keys.setdefault(entry["year"], []).append(entry["sort_key"])

        for year, sort_keys in year_to_sort_keys.items():
            self.assertEqual(sort_keys, sorted(sort_keys), f"Tijdlijn voor {year} is niet chronologisch gesorteerd.")

    def test_site_manifest_has_no_fallback_topic_titles_for_d6(self) -> None:
        manifest = load_json(SITE_MANIFEST_PATH)
        titles = {page["title"] for page in manifest["pages"]}
        self.assertNotIn("D6 other", titles)
        self.assertNotIn("D6 regional coordination", titles)
        self.assertIn("Updates", titles)
        self.assertIn("Controlelijst: VNG-financieringsset van 22 april 2026 verwerkt", titles)
        self.assertIn("Onderbouwing: Mogelijke besluitvraag: regiemodel voor D6 en lokale teams", titles)
        self.assertIn("Onderbouwing: Mogelijke opvolgactie: monitoringsaanpak voor Almere afstemmen", titles)
        self.assertIn("overige D6-lijn", titles)
        self.assertIn("regionale coördinatie voor D6", titles)

    def test_source_intake_candidates_capture_pipeline_first_timeline_work(self) -> None:
        intake = load_json(SOURCE_INTAKE_CANDIDATES_PATH)
        titles = {entry["title"] for entry in intake["candidate_sources"]}
        statuses = {entry["proposed_document_id"]: entry["ingestion_status"] for entry in intake["candidate_sources"]}
        subjects = {entry["subject"] for entry in intake["candidate_timeline_items"]}
        self.assertIn("Specifieke uitkering transformatiemiddelen IZA & AZWA 2024-2028", titles)
        self.assertIn("Gemeentefonds", titles)
        self.assertIn("Vergaderschema Raad van Almere", titles)
        self.assertIn("Gezond en actief leven", titles)
        self.assertIn("Ledenbrief onderhandelaarsakkoord AZWA", titles)
        self.assertIn("Aanvulling regioplan", subjects)
        self.assertIn("Gemeentelijke begrotingscyclus Almere", subjects)
        self.assertEqual(statuses["nat_dusi_spuk_transformatiemiddelen_2024_2028"], "ingested")
        self.assertEqual(statuses["nat_bzk_gemeentefonds_cyclus"], "ingested")
        self.assertEqual(statuses["mun_almere_raad_vergaderschema_2026"], "ingested")
        self.assertEqual(statuses["nat_vng_gezond_en_actief_leven_2026"], "ingested")
        self.assertEqual(statuses["nat_vng_ledenbrief_onderhandelaarsakkoord_azwa_2025"], "ingested")
        self.assertEqual(statuses["nat_vng_iza_azwa_wegwijzer_2026"], "pending_replacement")

    def test_site_js_reveals_hash_targets_inside_details(self) -> None:
        script = (DIST_DIR / "assets" / "site.js").read_text(encoding="utf-8")
        self.assertIn("function revealHashTarget()", script)
        self.assertIn('current.tagName === "DETAILS"', script)

    def test_deploy_workflow_runs_tests_before_build(self) -> None:
        workflow = DEPLOY_WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn('python -m unittest discover -s tests -p "test_*.py"', workflow)
        self.assertIn("python src/build_site_view_models.py", workflow)
        self.assertIn("python src/render_site.py", workflow)

    def test_search_index_covers_overviews_and_detail_pages(self) -> None:
        search_index = load_json(SEARCH_INDEX_PATH)
        titles = {entry["title"] for entry in search_index}
        page_types = {entry["page_type"] for entry in search_index}
        self.assertTrue({"Start", "Almere", "Besluitvragen", "Opvolgacties", "Dashboard", "Thema's", "Updates", "Referentie", "Bronnen"}.issubset(titles))
        self.assertIn("decision", page_types)
        self.assertIn("action", page_types)
        self.assertIn("theme", page_types)
        self.assertIn("updates", page_types)
        self.assertIn("update", page_types)
        self.assertIn("update_claims", page_types)
        self.assertIn("decision_evidence", page_types)
        self.assertIn("action_evidence", page_types)
        self.assertIn("reference_topic", page_types)
        self.assertIn("source", page_types)

    def test_search_index_contains_update_claims_page(self) -> None:
        search_index = load_json(SEARCH_INDEX_PATH)
        entry = next(
            item
            for item in search_index
            if item["page_type"] == "update_claims"
            and item["url"] == f"updates/claims/{LATEST_UPDATE_ID}/index.html"
        )
        self.assertIn("Controlelijst:", entry["title"])


if __name__ == "__main__":
    unittest.main()
