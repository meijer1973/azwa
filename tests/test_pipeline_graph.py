from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PIPELINE_CONFIG_PATH = REPO_ROOT / "config" / "pipeline_graph.json"


class PipelineGraphTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = json.loads(PIPELINE_CONFIG_PATH.read_text(encoding="utf-8"))
        self.stages = self.payload["stages"]
        self.stage_map = {stage["stage_id"]: stage for stage in self.stages}

    def test_stage_ids_are_unique(self) -> None:
        self.assertEqual(len(self.stage_map), len(self.stages))

    def test_dependencies_exist(self) -> None:
        for stage in self.stages:
            for dependency in stage.get("depends_on", []):
                self.assertIn(dependency, self.stage_map)

    def test_script_stages_have_existing_scripts(self) -> None:
        for stage in self.stages:
            if stage["kind"] != "script":
                continue
            script_path = REPO_ROOT / stage["script"]
            self.assertTrue(script_path.exists(), f"Missing script for stage {stage['stage_id']}: {script_path}")

    def test_output_paths_are_unique(self) -> None:
        seen: set[str] = set()
        for stage in self.stages:
            for output in stage.get("outputs", []):
                self.assertNotIn(output, seen, f"Duplicate output path: {output}")
                seen.add(output)

    def test_prompt_stage_outputs_exist(self) -> None:
        prompt_stage = self.stage_map["phase9_prompt_assets"]
        for output in prompt_stage["outputs"]:
            self.assertTrue((REPO_ROOT / output).exists(), f"Missing prompt asset: {output}")


if __name__ == "__main__":
    unittest.main()
