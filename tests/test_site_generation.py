from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HOME_VIEW_PATH = REPO_ROOT / "data" / "site" / "site_home_view.json"
ALMERE_VIEW_PATH = REPO_ROOT / "data" / "site" / "site_almere_view.json"
DASHBOARD_VIEW_PATH = REPO_ROOT / "data" / "site" / "dashboard_view.json"
TIMELINE_VIEW_PATH = REPO_ROOT / "data" / "site" / "site_timeline_view.json"
THEMES_VIEW_PATH = REPO_ROOT / "data" / "site" / "site_themes_view.json"
REFERENCE_VIEW_PATH = REPO_ROOT / "data" / "site" / "site_reference_view.json"
SOURCES_VIEW_PATH = REPO_ROOT / "data" / "site" / "site_sources_view.json"
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
SEARCH_INDEX_PATH = DIST_DIR / "search-index.json"
SITE_BUILD_PATH = DIST_DIR / "site-build.json"
DEPLOY_WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "deploy-pages.yml"


def load_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


class SiteGenerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run([sys.executable, "src/build_site_view_models.py"], cwd=REPO_ROOT, check=True)
        subprocess.run([sys.executable, "src/render_site.py"], cwd=REPO_ROOT, check=True)

    def test_site_view_model_outputs_exist(self) -> None:
        self.assertTrue(HOME_VIEW_PATH.exists())
        self.assertTrue(ALMERE_VIEW_PATH.exists())
        self.assertTrue(DASHBOARD_VIEW_PATH.exists())
        self.assertTrue(TIMELINE_VIEW_PATH.exists())
        self.assertTrue(THEMES_VIEW_PATH.exists())
        self.assertTrue(REFERENCE_VIEW_PATH.exists())
        self.assertTrue(SOURCES_VIEW_PATH.exists())
        self.assertGreater(len(list(DECISION_DIR.glob("*.json"))), 0)
        self.assertGreater(len(list(ACTION_DIR.glob("*.json"))), 0)
        self.assertGreater(len(list(THEME_DIR.glob("*.json"))), 0)
        self.assertGreater(len(list(REFERENCE_TOPIC_DIR.glob("*.json"))), 0)
        self.assertGreater(len(list(SOURCE_VIEW_DIR.glob("*.json"))), 0)

    def test_rendered_pages_exist(self) -> None:
        for path in [
            INDEX_PATH,
            ALMERE_PAGE_PATH,
            DECISIONS_PAGE_PATH,
            ACTIONS_PAGE_PATH,
            DASHBOARD_PAGE_PATH,
            TIMELINE_PAGE_PATH,
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
        self.assertIn('href="decisions/index.html?theme=', html)
        self.assertIn('href="actions/index.html?theme=', html)
        self.assertIn('href="themes/index.html"', html)
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
        self.assertIn('#menselijke-duiding">Menselijke duiding nodig:', html)

        detail_pages = list(DECISION_DIR.glob("*.json"))
        self.assertTrue(detail_pages)
        detail_html = (DIST_DIR / "decisions" / "mogelijke-besluitvraag-regiemodel-voor-d6-en-lokale-teams" / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="menselijke-duiding"', detail_html)
        self.assertIn("Bronnen die extra duiding vragen", detail_html)
        self.assertIn("Aanbevolen vervolgstap", detail_html)

    def test_logical_clickability_regression(self) -> None:
        home_html = INDEX_PATH.read_text(encoding="utf-8")
        themes_html = THEMES_PAGE_PATH.read_text(encoding="utf-8")
        reference_html = REFERENCE_PAGE_PATH.read_text(encoding="utf-8")
        sources_html = SOURCES_PAGE_PATH.read_text(encoding="utf-8")

        self.assertIn('href="almere/index.html#menselijke-duiding"', home_html)
        self.assertIn('href="decisions/index.html?theme=governance-en-regie"', home_html)
        self.assertIn('href="actions/index.html?theme=governance-en-regie"', home_html)
        self.assertIn('class="card card--link" href="themes/index.html"', home_html)

        self.assertIn('href="../decisions/index.html?theme=governance-en-regie"', themes_html)
        self.assertIn('href="../actions/index.html?theme=governance-en-regie"', themes_html)

        self.assertIn('href="topics/index.html"', reference_html)
        self.assertIn('href="topics/d5-definition/index.html"', reference_html)
        self.assertIn('class="card card--link" href="topics/d5-definition/index.html"', reference_html)

        self.assertIn('href="azwa-definitief/index.html"', sources_html)
        self.assertIn('class="card card--link" href="azwa-definitief/index.html"', sources_html)

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
        self.assertIn("2026-04-09", html)
        self.assertIn("begin 2027", html)

    def test_deploy_workflow_runs_tests_before_build(self) -> None:
        workflow = DEPLOY_WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn('python -m unittest discover -s tests -p "test_*.py"', workflow)
        self.assertIn("python src/run_pipeline.py --stage phase13_site_render", workflow)

    def test_search_index_covers_overviews_and_detail_pages(self) -> None:
        search_index = load_json(SEARCH_INDEX_PATH)
        titles = {entry["title"] for entry in search_index}
        page_types = {entry["page_type"] for entry in search_index}
        self.assertTrue({"Start", "Almere", "Besluitvragen", "Opvolgacties", "Dashboard", "Thema's", "Referentie", "Bronnen"}.issubset(titles))
        self.assertIn("decision", page_types)
        self.assertIn("action", page_types)
        self.assertIn("theme", page_types)
        self.assertIn("reference_topic", page_types)
        self.assertIn("source", page_types)


if __name__ == "__main__":
    unittest.main()
