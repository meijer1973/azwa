from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
CLAIMS_MASTER_PATH = REPO_ROOT / "data" / "extracted" / "claims" / "claims_master.jsonl"
SCAN_ROOTS = [
    REPO_ROOT / "data" / "extracted",
    REPO_ROOT / "data" / "site",
]
REFERENCE_LOG_EXCLUDES = {
    REPO_ROOT / "data" / "extracted" / "claims" / "sentence_validator_rejects.json",
    REPO_ROOT / "data" / "extracted" / "claims" / "dedup_log.json",
}


def load_master_claim_ids() -> set[str]:
    claim_ids: set[str] = set()
    for line in CLAIMS_MASTER_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        claim_ids.add(json.loads(line)["claim_id"])
    return claim_ids


def walk_claim_references(node: Any, path: str = "$") -> list[tuple[str, str]]:
    references: list[tuple[str, str]] = []
    if isinstance(node, dict):
        for key, value in node.items():
            child_path = f"{path}.{key}"
            if "claim_id" in key:
                if isinstance(value, str) and value.startswith("clm__"):
                    references.append((child_path, value))
                elif isinstance(value, list):
                    for index, item in enumerate(value):
                        if isinstance(item, str) and item.startswith("clm__"):
                            references.append((f"{child_path}[{index}]", item))
            references.extend(walk_claim_references(value, child_path))
    elif isinstance(node, list):
        for index, item in enumerate(node):
            references.extend(walk_claim_references(item, f"{path}[{index}]"))
    return references


def verify() -> list[dict]:
    master_claim_ids = load_master_claim_ids()
    missing: list[dict] = []
    for root in SCAN_ROOTS:
        for path in sorted(root.rglob("*.json")):
            resolved = path.resolve()
            if resolved in {item.resolve() for item in REFERENCE_LOG_EXCLUDES}:
                continue
            payload = json.loads(path.read_text(encoding="utf-8"))
            for location, claim_id in walk_claim_references(payload):
                if claim_id not in master_claim_ids:
                    missing.append(
                        {
                            "path": path.relative_to(REPO_ROOT).as_posix(),
                            "location": location,
                            "claim_id": claim_id,
                        }
                    )
    return missing


def main() -> None:
    missing = verify()
    if missing:
        print(f"Found {len(missing)} unresolved claim_id reference(s).")
        for item in missing[:50]:
            print(f"- {item['path']} {item['location']}: {item['claim_id']}")
        if len(missing) > 50:
            print(f"... and {len(missing) - 50} more")
        sys.exit(1)
    print("All claim_id references in data/extracted and data/site resolve to claims_master.jsonl.")


if __name__ == "__main__":
    main()
