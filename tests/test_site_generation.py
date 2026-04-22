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
DECISION_DIR = REPO_ROOT / "data" / "site" / "decision_view_models"
ACTION_DIR = REPO_ROOT / "data" / "site" / "action_view_models"
DIST_DIR = REPO_ROOT / "dist"
INDEX_PATH = DIST_DIR / "index.html"
ALMERE_PAGE_PATH = DIST_DIR / "almere" / "index.html"
DECISIONS_PAGE_PATH = DIST_DIR / "decisions" / "index.html"
ACTIONS_PAGE_PATH = DIST_DIR / "actions" / "index.html"
DASHBOARD_PAGE_PATH = DIST_DIR / "dashboard" / "index.html"
SEARCH_INDEX_PATH = DIST_DIR / "search-index.json"


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
        self.assertGreater(len(list(DECISION_DIR.glob("*.json"))), 0)
        self.assertGreater(len(list(ACTION_DIR.glob("*.json"))), 0)

    def test_rendered_pages_exist(self) -> None:
        for path in [
            INDEX_PATH,
            ALMERE_PAGE_PATH,
            DECISIONS_PAGE_PATH,
            ACTIONS_PAGE_PATH,
            DASHBOARD_PAGE_PATH,
            SEARCH_INDEX_PATH,
        ]:
            self.assertTrue(path.exists(), f"Missing rendered output: {path}")

    def test_home_page_contains_careful_public_wording(self) -> None:
        html = INDEX_PATH.read_text(encoding="utf-8")
        self.assertIn("AZWA D5/D6 - Almere", html)
        self.assertIn("Bestuurlijk overzicht", html)
        self.assertIn("mogelijke besluitvragen", html)
        self.assertIn("mogelijke opvolgacties", html)
        self.assertIn('href="almere/index.html"', html)
        self.assertIn('href="decisions/index.html"', html)

    def test_decisions_page_contains_explicit_notice(self) -> None:
        html = DECISIONS_PAGE_PATH.read_text(encoding="utf-8")
        self.assertIn("mogelijke besluitvragen", html)
        self.assertIn("geen vastgestelde gemeentelijke besluiten", html)

    def test_search_index_covers_overviews_and_detail_pages(self) -> None:
        search_index = load_json(SEARCH_INDEX_PATH)
        titles = {entry["title"] for entry in search_index}
        page_types = {entry["page_type"] for entry in search_index}
        self.assertTrue({"Start", "Almere", "Besluitvragen", "Opvolgacties", "Dashboard"}.issubset(titles))
        self.assertIn("decision", page_types)
        self.assertIn("action", page_types)


if __name__ == "__main__":
    unittest.main()
