from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

import src.audit_report_grounding as report_audit


REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT_NOTE_PATH = REPO_ROOT / "docs" / "internal" / "report-grounding-audit-2026-04-29.md"


class ReportGroundingTests(unittest.TestCase):
    def test_current_public_reports_have_no_blocking_grounding_issues(self) -> None:
        audit = report_audit.build_audit()
        self.assertEqual(audit["report_count"], 2)
        self.assertEqual(audit["issue_count"], 0)
        checked_paths = {report["path"] for report in audit["reports"]}
        self.assertEqual(
            checked_paths,
            {
                "docs/rapporten/plan-van-aanpak-v3.md",
                "docs/rapporten/bestuurlijke-planning-azwa-almere-2026.md",
            },
        )

    def test_superseded_v2_is_not_public_candidate(self) -> None:
        manifest = report_audit.load_manifest()
        report = next(item for item in manifest["reports"] if item["path"] == "docs/rapporten/plan-van-aanpak-v2.md")
        self.assertFalse(report["public_facing_candidate"])
        self.assertEqual(report["status"], "superseded_do_not_use_publicly")

    def test_audit_script_writes_internal_note(self) -> None:
        subprocess.run([sys.executable, "src/audit_report_grounding.py"], cwd=REPO_ROOT, check=True)
        text = AUDIT_NOTE_PATH.read_text(encoding="utf-8")
        self.assertIn("Current sprint: Sprint 30.3", text)
        self.assertIn("Blocking report-grounding issues found: 0", text)
        self.assertIn("Superseded Drafts", text)


if __name__ == "__main__":
    unittest.main()
