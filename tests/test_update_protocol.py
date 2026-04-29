from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

import src.validate_update_protocol as update_protocol


REPO_ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_DOC_PATH = REPO_ROOT / "docs" / "updateprotocol.md"
CHECK_NOTE_PATH = REPO_ROOT / "docs" / "internal" / "update-protocol-check-2026-04-29.md"


class UpdateProtocolTests(unittest.TestCase):
    def test_update_protocol_document_exists_and_names_required_workflow(self) -> None:
        text = PROTOCOL_DOC_PATH.read_text(encoding="utf-8")
        self.assertIn("Current sprint: Sprint 31.1", text)
        self.assertIn("config/site_updates.json", text)
        self.assertIn("python src/validate_update_protocol.py", text)
        self.assertIn("Old Claims", text)
        self.assertIn("Commit and push", text)

    def test_site_updates_follow_protocol(self) -> None:
        result = update_protocol.validate_updates()
        self.assertEqual(result["update_count"], 3)
        self.assertEqual(result["issue_count"], 0)

    def test_validator_writes_internal_check_note(self) -> None:
        subprocess.run([sys.executable, "src/validate_update_protocol.py"], cwd=REPO_ROOT, check=True)
        text = CHECK_NOTE_PATH.read_text(encoding="utf-8")
        self.assertIn("Current sprint: Sprint 31.1", text)
        self.assertIn("Updates checked: 3", text)
        self.assertIn("Blocking update-protocol issues found: 0", text)


if __name__ == "__main__":
    unittest.main()
