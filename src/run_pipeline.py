from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PIPELINE_CONFIG_PATH = REPO_ROOT / "config" / "pipeline_graph.json"
LOG_DIR = REPO_ROOT / "data" / "logs" / "pipeline_runs"


def load_config() -> dict:
    return json.loads(PIPELINE_CONFIG_PATH.read_text(encoding="utf-8"))


def stage_maps(config: dict) -> tuple[list[dict], dict[str, dict]]:
    stages = config["stages"]
    stage_map = {stage["stage_id"]: stage for stage in stages}
    return stages, stage_map


def validate_graph(stages: list[dict], stage_map: dict[str, dict]) -> None:
    for stage in stages:
        for dependency in stage.get("depends_on", []):
            if dependency not in stage_map:
                raise ValueError(f"Unknown dependency '{dependency}' in stage {stage['stage_id']}")

        if stage["kind"] == "script":
            script = REPO_ROOT / stage["script"]
            if not script.exists():
                raise FileNotFoundError(f"Missing pipeline script: {script}")

    outputs_seen: set[str] = set()
    for stage in stages:
        for output in stage.get("outputs", []):
            if output in outputs_seen:
                raise ValueError(f"Duplicate output path in pipeline graph: {output}")
            outputs_seen.add(output)


def topo_sort(stages: list[dict], stage_map: dict[str, dict]) -> list[str]:
    position = {stage["stage_id"]: index for index, stage in enumerate(stages)}
    indegree: dict[str, int] = {stage["stage_id"]: 0 for stage in stages}
    children: dict[str, list[str]] = defaultdict(list)

    for stage in stages:
        stage_id = stage["stage_id"]
        for dependency in stage.get("depends_on", []):
            indegree[stage_id] += 1
            children[dependency].append(stage_id)

    ready = sorted([stage_id for stage_id, degree in indegree.items() if degree == 0], key=position.get)
    ordered: list[str] = []

    while ready:
        stage_id = ready.pop(0)
        ordered.append(stage_id)
        for child in sorted(children[stage_id], key=position.get):
            indegree[child] -= 1
            if indegree[child] == 0 and child not in ready:
                ready.append(child)
        ready.sort(key=position.get)

    if len(ordered) != len(stages):
        raise ValueError("Pipeline graph contains a cycle")
    return ordered


def expand_path_spec(path_spec: str) -> list[Path]:
    if any(char in path_spec for char in "*?[]"):
        matches = [path for path in REPO_ROOT.glob(path_spec) if path.exists()]
        return sorted(matches)

    path = REPO_ROOT / path_spec
    if not path.exists():
        return []
    return [path]


def file_candidates(path: Path) -> list[Path]:
    if path.is_file():
        return [] if path.name == ".gitkeep" else [path]

    descendants = [
        child
        for child in path.rglob("*")
        if child.is_file() and child.name != ".gitkeep" and "__pycache__" not in child.parts
    ]
    return sorted(descendants)


def latest_mtime(path_specs: list[str]) -> float:
    mtimes: list[float] = []
    for path_spec in path_specs:
        for path in expand_path_spec(path_spec):
            candidates = file_candidates(path) if path.is_dir() else [path]
            if not candidates and path.is_dir():
                mtimes.append(path.stat().st_mtime)
                continue
            for candidate in candidates:
                mtimes.append(candidate.stat().st_mtime)
    return max(mtimes) if mtimes else 0.0


def output_paths_exist(path_specs: list[str]) -> bool:
    for path_spec in path_specs:
        matches = expand_path_spec(path_spec)
        if not matches:
            return False
        for path in matches:
            if path.is_file():
                continue
            if not file_candidates(path):
                return False
    return True


def oldest_output_mtime(path_specs: list[str]) -> float:
    mtimes: list[float] = []
    for path_spec in path_specs:
        for path in expand_path_spec(path_spec):
            candidates = file_candidates(path) if path.is_dir() else [path]
            if not candidates and path.is_dir():
                mtimes.append(path.stat().st_mtime)
                continue
            for candidate in candidates:
                mtimes.append(candidate.stat().st_mtime)
    return min(mtimes) if mtimes else 0.0


def ancestors(stage_id: str, stage_map: dict[str, dict]) -> set[str]:
    collected: set[str] = set()
    stack = list(stage_map[stage_id].get("depends_on", []))
    while stack:
        dependency = stack.pop()
        if dependency in collected:
            continue
        collected.add(dependency)
        stack.extend(stage_map[dependency].get("depends_on", []))
    return collected


def descendants(stage_id: str, stages: list[dict]) -> set[str]:
    children: dict[str, list[str]] = defaultdict(list)
    for stage in stages:
        for dependency in stage.get("depends_on", []):
            children[dependency].append(stage["stage_id"])

    collected: set[str] = set()
    stack = list(children[stage_id])
    while stack:
        child = stack.pop()
        if child in collected:
            continue
        collected.add(child)
        stack.extend(children[child])
    return collected


def dirty_reason(stage: dict, stage_outputs: list[str]) -> tuple[bool, str]:
    if stage["kind"] == "asset":
        if output_paths_exist(stage_outputs):
            return False, "asset_present"
        return True, "asset_missing"

    if not output_paths_exist(stage_outputs):
        return True, "outputs_missing"

    dependency_outputs = []
    for dependency in stage.get("depends_on", []):
        dependency_outputs.extend(stage_outputs_by_id[dependency])

    latest_input = latest_mtime(stage.get("inputs", []) + dependency_outputs)
    oldest_output = oldest_output_mtime(stage_outputs)
    if latest_input > oldest_output:
        return True, "upstream_newer_than_outputs"
    return False, "up_to_date"


def run_stage(stage: dict) -> None:
    subprocess.run(
        [sys.executable, stage["script"]],
        cwd=REPO_ROOT,
        check=True,
    )


def write_run_log(log_payload: dict) -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_path = LOG_DIR / f"{timestamp}_pipeline.json"
    log_path.write_text(json.dumps(log_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    latest_path = LOG_DIR / "latest.json"
    latest_path.write_text(json.dumps(log_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return log_path


def parse_args(default_target: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run or inspect the AZWA extraction pipeline.")
    parser.add_argument("--list", action="store_true", help="List the configured stages and exit.")
    parser.add_argument("--all", action="store_true", help="Evaluate the full configured pipeline.")
    parser.add_argument("--stage", help="Evaluate a single stage and its prerequisites.")
    parser.add_argument("--from-stage", dest="from_stage", help="Evaluate a stage, its prerequisites, and all downstream stages.")
    parser.add_argument("--target", default=default_target, help="Fallback target stage when no explicit scope is provided.")
    parser.add_argument("--force", action="store_true", help="Run selected script stages even if they look up to date.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would run without executing scripts.")
    return parser.parse_args()


def selected_stage_ids(args: argparse.Namespace, ordered_stage_ids: list[str], stage_map: dict[str, dict], stages: list[dict]) -> set[str]:
    if args.all:
        return set(ordered_stage_ids)

    if args.stage:
        return ancestors(args.stage, stage_map) | {args.stage}

    if args.from_stage:
        return ancestors(args.from_stage, stage_map) | {args.from_stage} | descendants(args.from_stage, stages)

    target = args.target
    return ancestors(target, stage_map) | {target}


if __name__ == "__main__":
    config = load_config()
    stages, stage_map = stage_maps(config)
    validate_graph(stages, stage_map)
    ordered_stage_ids = topo_sort(stages, stage_map)

    args = parse_args(config["default_target"])

    if args.list:
        for stage_id in ordered_stage_ids:
            stage = stage_map[stage_id]
            print(f"{stage_id} [{stage['kind']}]")
            print(f"  {stage['description']}")
        raise SystemExit(0)

    unknown_stage = next(
        (
            stage_id
            for stage_id in [args.stage, args.from_stage, args.target]
            if stage_id and stage_id not in stage_map
        ),
        None,
    )
    if unknown_stage:
        raise SystemExit(f"Unknown stage id: {unknown_stage}")

    selected_ids = selected_stage_ids(args, ordered_stage_ids, stage_map, stages)
    stage_outputs_by_id = {stage["stage_id"]: stage.get("outputs", []) for stage in stages}

    run_records: list[dict] = []

    for stage_id in ordered_stage_ids:
        if stage_id not in selected_ids:
            continue

        stage = stage_map[stage_id]
        outputs = stage.get("outputs", [])
        dirty, reason = dirty_reason(stage, outputs)

        record = {
            "stage_id": stage_id,
            "kind": stage["kind"],
            "description": stage["description"],
            "dirty": dirty,
            "reason": reason,
            "action": "skip",
        }

        if stage["kind"] == "asset":
            if dirty:
                raise SystemExit(f"Required asset stage '{stage_id}' is missing one or more outputs.")
            print(f"[asset] {stage_id}: present")
            run_records.append(record)
            continue

        if args.force or dirty:
            record["action"] = "run"
            print(f"[run] {stage_id}: {reason}")
            if not args.dry_run:
                run_stage(stage)
        else:
            print(f"[skip] {stage_id}: up to date")

        run_records.append(record)

    log_payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "dry_run": args.dry_run,
        "force": args.force,
        "selected_stage_ids": [stage_id for stage_id in ordered_stage_ids if stage_id in selected_ids],
        "records": run_records,
    }
    log_path = write_run_log(log_payload)
    print(f"Log written to {log_path.relative_to(REPO_ROOT).as_posix()}")
