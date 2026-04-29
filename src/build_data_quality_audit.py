from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO_ROOT / "config"
DATA_DIR = REPO_ROOT / "data"
EXTRACTED_DIR = DATA_DIR / "extracted"
SITE_DIR = DATA_DIR / "site"
CLAIMS_MASTER_PATH = EXTRACTED_DIR / "claims" / "claims_master.jsonl"
CURRENT_INTERPRETATION_PATH = EXTRACTED_DIR / "claims" / "current_interpretation.json"
REVIEW_QUEUE_PATH = EXTRACTED_DIR / "review_queue.json"
PERSPECTIVES_PATH = CONFIG_DIR / "data_quality_perspectives.json"
AUDIT_OUTPUT_PATH = EXTRACTED_DIR / "data_quality_audit.json"

AUDIT_RUN_ID = "phase24_data_quality_audit_v1"
TODAY = date.today().isoformat()

ROUGH_TEXT_PATTERNS = {
    "raw_letterhead": (
        "Correspondentie uitsluitend richten",
        "Geachte voorzitter",
        "retouradres",
    ),
    "encoding_noise": (
        "â",
        "Ã",
        "\ufffd",
    ),
}

ENGLISH_STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "that",
    "this",
    "must",
    "should",
    "current",
    "view",
    "local",
    "regional",
    "people",
    "support",
    "care",
}

DUTCH_STOPWORDS = {
    "de",
    "het",
    "en",
    "voor",
    "met",
    "van",
    "dat",
    "deze",
    "moet",
    "lokale",
    "regionale",
    "gemeente",
    "zorg",
    "ondersteuning",
}

ISSUE_WEIGHTS = {
    "raw_letterhead": 5,
    "encoding_noise": 4,
    "english_summary": 3,
    "bullet_or_heading_fragment": 2,
    "fragment_too_short": 2,
    "unverified_extraction_length": 1,
}

LOWERCASE_START_WHITELIST = {
    "e-health",
    "ehealth",
    "i-sociaal",
    "i-standaarden",
}

TERMINAL_PUNCTUATION = (".", "!", "?", '"', "'", "”", "’", "»")

COLUMN_MERGE_PATTERNS = (
    re.compile(r"\b\d{4}\s+\d{4}\s+\d{4}\b"),
    re.compile(r"\b(?:eur|€)\s?\d[\d.,]*\s+\d[\d.,]*\s+\d[\d.,]*", re.IGNORECASE),
    re.compile(r"\b(?:ja|nee|n\.v\.t\.|onbekend)\s+(?:ja|nee|n\.v\.t\.|onbekend)\b", re.IGNORECASE),
)

SITE_VIEW_MODEL_GROUPS = {
    "decision_view_models": "decision_detail",
    "action_view_models": "action_detail",
    "theme_view_models": "theme_detail",
    "reference_topic_view_models": "reference_topic_detail",
    "source_view_models": "source_detail",
}

KNOWN_GOVERNANCE_ACTOR_SIGNALS = [
    "ministerie",
    "vng",
    "mandaatgemeente",
    "regio",
    "gemeente",
    "gemeenteraad",
    "college",
    "zorgverzekeraar",
    "uitvoeringspartner",
]


def load_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def load_claims() -> list[dict]:
    claims: list[dict] = []
    for line in CLAIMS_MASTER_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            claims.append(json.loads(line))
    return claims


def load_perspective_config() -> dict:
    return load_json(PERSPECTIVES_PATH)


def perspective_ids_for_claim(claim: dict, perspective_config: dict) -> list[str]:
    topic = claim.get("topic") or ""
    jurisdiction_level = claim.get("jurisdiction_level")
    perspective_ids: list[str] = []

    for perspective in perspective_config["perspectives"]:
        perspective_id = perspective["perspective_id"]
        topic_prefixes = perspective.get("topic_prefixes", [])
        topic_ids = perspective.get("topic_ids", [])
        jurisdiction_hints = perspective.get("jurisdiction_level_hints", [])

        if any(topic.startswith(prefix) for prefix in topic_prefixes):
            perspective_ids.append(perspective_id)
            continue
        if topic in topic_ids:
            perspective_ids.append(perspective_id)
            continue
        if jurisdiction_level in jurisdiction_hints:
            perspective_ids.append(perspective_id)

    return sorted(set(perspective_ids))


def normalize_words(text: str) -> list[str]:
    return re.findall(r"[A-Za-zÀ-ÿ']+", text.lower())


def looks_english(text: str) -> bool:
    words = normalize_words(text)
    if len(words) < 8:
        return False

    english_hits = sum(1 for word in words if word in ENGLISH_STOPWORDS)
    dutch_hits = sum(1 for word in words if word in DUTCH_STOPWORDS)
    starts_english = bool(re.match(r"^(The|This|Current|Regional|A\s|For\s)", text))
    return starts_english or (english_hits >= 4 and english_hits > dutch_hits * 1.5)


def first_word(text: str) -> str:
    match = re.search(r"[^\W\d_][^\W\d_'-]*", text, flags=re.UNICODE)
    return match.group(0) if match else ""


def starts_lowercase_outside_whitelist(text: str) -> bool:
    word = first_word(text)
    if not word:
        return False
    return word[0].islower() and word.lower() not in LOWERCASE_START_WHITELIST


def lacks_terminal_punctuation(text: str) -> bool:
    return not text.rstrip().endswith(TERMINAL_PUNCTUATION)


def has_column_merge_fingerprint(text: str) -> bool:
    return any(pattern.search(text) for pattern in COLUMN_MERGE_PATTERNS)


def has_unverified_extraction_length(text: str) -> bool:
    stripped = text.strip()
    if len(stripped) <= 240:
        return False
    return (
        starts_lowercase_outside_whitelist(stripped)
        or lacks_terminal_punctuation(stripped)
        or has_column_merge_fingerprint(stripped)
    )


def detect_rough_issues(text: str) -> list[str]:
    issues: list[str] = []
    stripped = text.strip()

    for issue_code, patterns in ROUGH_TEXT_PATTERNS.items():
        if any(pattern in stripped for pattern in patterns):
            issues.append(issue_code)

    if looks_english(stripped):
        issues.append("english_summary")
    if stripped.startswith(("•", "-", "1.", "2.", "3.")):
        issues.append("bullet_or_heading_fragment")
    if len(normalize_words(stripped)) < 8:
        issues.append("fragment_too_short")
    if has_unverified_extraction_length(stripped):
        issues.append("unverified_extraction_length")

    return sorted(set(issues))


def claim_excerpt(text: str, limit: int = 400) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."


def page_group_for_file(path: Path) -> str:
    parts = path.parts
    for directory_name, group_name in SITE_VIEW_MODEL_GROUPS.items():
        if directory_name in parts:
            return group_name
    return path.stem


def walk_claim_refs(node: object) -> list[dict]:
    matches: list[dict] = []
    if isinstance(node, dict):
        if "claim_id" in node and "statement" in node:
            matches.append(node)
        for value in node.values():
            matches.extend(walk_claim_refs(value))
    elif isinstance(node, list):
        for item in node:
            matches.extend(walk_claim_refs(item))
    return matches


def site_json_files() -> list[Path]:
    return sorted(
        path
        for path in SITE_DIR.rglob("*.json")
        if path.is_file()
    )


def build_perspective_coverage(claims: list[dict], perspective_config: dict) -> tuple[dict, dict[str, list[str]]]:
    claims_by_perspective: defaultdict[str, set[str]] = defaultdict(set)
    topics_by_perspective: defaultdict[str, set[str]] = defaultdict(set)
    claim_perspectives: dict[str, list[str]] = {}
    claims_by_topic: Counter[str] = Counter()
    sample_claim_ids_by_topic: defaultdict[str, list[str]] = defaultdict(list)
    claims_without_perspectives_count_by_topic: Counter[str] = Counter()
    claims_without_perspectives_by_topic: defaultdict[str, list[str]] = defaultdict(list)

    for claim in claims:
        claim_id = claim["claim_id"]
        topic = claim["topic"]
        perspective_ids = perspective_ids_for_claim(claim, perspective_config)
        claim_perspectives[claim_id] = perspective_ids
        claims_by_topic[topic] += 1
        if len(sample_claim_ids_by_topic[topic]) < 5:
            sample_claim_ids_by_topic[topic].append(claim_id)
        if not perspective_ids:
            claims_without_perspectives_count_by_topic[topic] += 1
            if len(claims_without_perspectives_by_topic[topic]) < 5:
                claims_without_perspectives_by_topic[topic].append(claim_id)

        for perspective_id in perspective_ids:
            claims_by_perspective[perspective_id].add(claim_id)
            topics_by_perspective[perspective_id].add(topic)

    perspective_summaries = []
    perspective_lookup = {item["perspective_id"]: item for item in perspective_config["perspectives"]}
    for perspective in perspective_config["perspectives"]:
        perspective_id = perspective["perspective_id"]
        perspective_summaries.append(
            {
                "perspective_id": perspective_id,
                "title": perspective["title"],
                "claim_count": len(claims_by_perspective[perspective_id]),
                "topic_count": len(topics_by_perspective[perspective_id]),
                "sample_topics": sorted(topics_by_perspective[perspective_id])[:8],
            }
        )

    unmapped_topics = [
        {
            "topic": topic,
            "claim_count": count,
            "sample_claim_ids": sample_claim_ids_by_topic[topic],
        }
        for topic, count in sorted(claims_by_topic.items(), key=lambda item: (-item[1], item[0]))
        if not any(topic in topics_by_perspective[p["perspective_id"]] for p in perspective_config["perspectives"])
    ]

    topic_mapping_gaps = [
        {
            "topic": topic,
            "claim_without_perspective_count": claims_without_perspectives_count_by_topic[topic],
            "sample_claim_ids": claim_ids,
        }
        for topic, claim_ids in sorted(
            claims_without_perspectives_by_topic.items(),
            key=lambda item: (-claims_without_perspectives_count_by_topic[item[0]], item[0]),
        )
    ]

    return {
        "claims_by_perspective": perspective_summaries,
        "claims_with_perspectives": sum(1 for values in claim_perspectives.values() if values),
        "claims_without_perspectives": sum(1 for values in claim_perspectives.values() if not values),
        "unmapped_topics": unmapped_topics,
        "topic_mapping_gaps": topic_mapping_gaps,
    }, claim_perspectives


def build_normative_status_audit(claims: list[dict], claim_perspectives: dict[str, list[str]]) -> dict:
    status_counts: Counter[str] = Counter()
    norm_perspective_counts: Counter[str] = Counter()
    attribution_needed: list[dict] = []

    for claim in claims:
        status_payload = claim.get("normative_status") or {}
        status = status_payload.get("status", "missing")
        status_counts[status] += 1
        if "norm" in claim_perspectives.get(claim["claim_id"], []):
            norm_perspective_counts[status] += 1
        if status_payload.get("needs_attribution") and len(attribution_needed) < 25:
            attribution_needed.append(
                {
                    "claim_id": claim["claim_id"],
                    "source_document_id": claim["source_document_id"],
                    "topic": claim["topic"],
                    "normative_status": status,
                    "source_authority": status_payload.get("source_authority"),
                    "statement_excerpt": claim_excerpt(claim["statement"], limit=220),
                    "public_wording_guardrail": status_payload.get("public_wording_guardrail"),
                }
            )

    return {
        "description": "Sprint 27.1 norm-strength split for binding text, agreement text, expectations, guidance, lower-authority signals, and contextual material.",
        "status_counts": dict(sorted(status_counts.items())),
        "norm_perspective_status_counts": dict(sorted(norm_perspective_counts.items())),
        "attribution_needed_sample": attribution_needed,
    }


def build_time_status_audit(claims: list[dict], claim_perspectives: dict[str, list[str]]) -> dict:
    status_counts: Counter[str] = Counter()
    time_perspective_counts: Counter[str] = Counter()
    date_signal_counts: Counter[str] = Counter()
    review_sample: list[dict] = []

    for claim in claims:
        status_payload = claim.get("time_status") or {}
        status = status_payload.get("status", "missing")
        status_counts[status] += 1
        date_signal_counts[status_payload.get("date_signal", "missing")] += 1
        if "time" in claim_perspectives.get(claim["claim_id"], []):
            time_perspective_counts[status] += 1
        if status_payload.get("needs_review") and len(review_sample) < 25:
            review_sample.append(
                {
                    "claim_id": claim["claim_id"],
                    "source_document_id": claim["source_document_id"],
                    "topic": claim["topic"],
                    "time_status": status,
                    "date_signal": status_payload.get("date_signal"),
                    "statement_excerpt": claim_excerpt(claim["statement"], limit=220),
                    "public_wording_guardrail": status_payload.get("public_wording_guardrail"),
                }
            )

    return {
        "description": "Sprint 27.2 time split for formal deadlines, expected moments, review/update cycles, budget-calendar moments, implementation horizons, local planning context, source-dated moments, publication/context dates, and undated context.",
        "status_counts": dict(sorted(status_counts.items())),
        "time_perspective_status_counts": dict(sorted(time_perspective_counts.items())),
        "date_signal_counts": dict(sorted(date_signal_counts.items())),
        "review_needed_sample": review_sample,
    }


def build_money_status_audit(claims: list[dict], claim_perspectives: dict[str, list[str]]) -> dict:
    status_counts: Counter[str] = Counter()
    money_perspective_counts: Counter[str] = Counter()
    verification_sample: list[dict] = []

    for claim in claims:
        status_payload = claim.get("money_status") or {}
        status = status_payload.get("status", "missing")
        status_counts[status] += 1
        if "money" in claim_perspectives.get(claim["claim_id"], []):
            money_perspective_counts[status] += 1
        if status_payload.get("needs_verification") and len(verification_sample) < 25:
            verification_sample.append(
                {
                    "claim_id": claim["claim_id"],
                    "source_document_id": claim["source_document_id"],
                    "topic": claim["topic"],
                    "money_status": status,
                    "statement_excerpt": claim_excerpt(claim["statement"], limit=220),
                    "public_wording_guardrail": status_payload.get("public_wording_guardrail"),
                }
            )

    return {
        "description": "Sprint 27.3 money split for funding routes, application conditions, budget windows, allocation mechanisms, spending scope, accountability rules, local funding gaps, double-counting risks, finance context, and non-financial material.",
        "status_counts": dict(sorted(status_counts.items())),
        "money_perspective_status_counts": dict(sorted(money_perspective_counts.items())),
        "verification_needed_sample": verification_sample,
    }


def build_governance_status_audit(claims: list[dict], claim_perspectives: dict[str, list[str]]) -> dict:
    status_counts: Counter[str] = Counter()
    governance_perspective_counts: Counter[str] = Counter()
    actor_signal_counts: Counter[str] = Counter()
    verification_sample: list[dict] = []

    for claim in claims:
        status_payload = claim.get("governance_status") or {}
        status = status_payload.get("status", "missing")
        status_counts[status] += 1
        actor_signal_counts.update(status_payload.get("actor_signals", []))
        if "governance" in claim_perspectives.get(claim["claim_id"], []):
            governance_perspective_counts[status] += 1
        if status_payload.get("needs_verification") and len(verification_sample) < 25:
            verification_sample.append(
                {
                    "claim_id": claim["claim_id"],
                    "source_document_id": claim["source_document_id"],
                    "topic": claim["topic"],
                    "governance_status": status,
                    "actor_signals": status_payload.get("actor_signals", []),
                    "vague_region_only": status_payload.get("vague_region_only", False),
                    "statement_excerpt": claim_excerpt(claim["statement"], limit=220),
                    "public_wording_guardrail": status_payload.get("public_wording_guardrail"),
                }
            )

    return {
        "description": "Sprint 27.4 governance split for decision, coordination, application, execution, accountability, approval, review, governance gaps, actor context, and non-governance material.",
        "status_counts": dict(sorted(status_counts.items())),
        "governance_perspective_status_counts": dict(sorted(governance_perspective_counts.items())),
        "actor_signal_counts": dict(sorted(actor_signal_counts.items())),
        "zero_count_actor_signals": [
            actor for actor in KNOWN_GOVERNANCE_ACTOR_SIGNALS if actor_signal_counts.get(actor, 0) == 0
        ],
        "verification_needed_sample": verification_sample,
    }


def build_locality_status_audit(claims: list[dict], claim_perspectives: dict[str, list[str]]) -> dict:
    status_counts: Counter[str] = Counter()
    locality_perspective_counts: Counter[str] = Counter()
    regional_split_counts: Counter[str] = Counter()
    verification_sample: list[dict] = []

    for claim in claims:
        status_payload = claim.get("locality_status") or {}
        status = status_payload.get("status", "missing")
        status_counts[status] += 1
        regional_split_counts.update(status_payload.get("regional_split_signals", []))
        if "locality" in claim_perspectives.get(claim["claim_id"], []):
            locality_perspective_counts[status] += 1
        if status_payload.get("needs_verification") and len(verification_sample) < 25:
            verification_sample.append(
                {
                    "claim_id": claim["claim_id"],
                    "source_document_id": claim["source_document_id"],
                    "topic": claim["topic"],
                    "locality_status": status,
                    "locality_scope": status_payload.get("locality_scope"),
                    "regional_split_signals": status_payload.get("regional_split_signals", []),
                    "explicit_location_signals": status_payload.get("explicit_location_signals", {}),
                    "statement_excerpt": claim_excerpt(claim["statement"], limit=220),
                    "public_wording_guardrail": status_payload.get("public_wording_guardrail"),
                }
            )

    return {
        "description": "Sprint 27.5 locality split for explicit Almere, explicit Flevoland, regional split context, national general, national with local relevance, inferred local relevance, local adoption gaps, municipal context, and no locality signal.",
        "status_counts": dict(sorted(status_counts.items())),
        "locality_perspective_status_counts": dict(sorted(locality_perspective_counts.items())),
        "regional_split_counts": dict(sorted(regional_split_counts.items())),
        "verification_needed_sample": verification_sample,
    }


def perspective_status_values(perspective_config: dict, perspective_id: str, field_name: str) -> list[str]:
    for perspective in perspective_config["perspectives"]:
        if perspective["perspective_id"] == perspective_id:
            return [item["status"] for item in perspective.get(field_name, [])]
    return []


def add_zero_count_statuses(audit_payload: dict, expected_statuses: list[str]) -> dict:
    status_counts = audit_payload.get("status_counts", {})
    enriched = dict(audit_payload)
    enriched["zero_count_statuses"] = [status for status in expected_statuses if status_counts.get(status, 0) == 0]
    return enriched


def build_execution_status_audit(claims: list[dict], claim_perspectives: dict[str, list[str]]) -> dict:
    status_counts: Counter[str] = Counter()
    execution_perspective_counts: Counter[str] = Counter()
    need_signal_counts: Counter[str] = Counter()
    verification_sample: list[dict] = []

    for claim in claims:
        status_payload = claim.get("execution_status") or {}
        status = status_payload.get("status", "missing")
        status_counts[status] += 1
        need_signal_counts.update(status_payload.get("execution_need_signals", []))
        if "execution" in claim_perspectives.get(claim["claim_id"], []):
            execution_perspective_counts[status] += 1
        if status_payload.get("needs_verification") and len(verification_sample) < 25:
            verification_sample.append(
                {
                    "claim_id": claim["claim_id"],
                    "source_document_id": claim["source_document_id"],
                    "topic": claim["topic"],
                    "execution_status": status,
                    "execution_need_signals": status_payload.get("execution_need_signals", []),
                    "source_execution_anchor": status_payload.get("source_execution_anchor"),
                    "statement_excerpt": claim_excerpt(claim["statement"], limit=220),
                    "public_wording_guardrail": status_payload.get("public_wording_guardrail"),
                }
            )

    return {
        "description": "Sprint 27.6 execution split for operational requirements, implementation activity, decision questions, dependencies, sequencing needs, capacity needs, review tasks, execution context, and non-execution material.",
        "status_counts": dict(sorted(status_counts.items())),
        "execution_perspective_status_counts": dict(sorted(execution_perspective_counts.items())),
        "execution_need_signal_counts": dict(sorted(need_signal_counts.items())),
        "verification_needed_sample": verification_sample,
    }


def build_view_model_coverage() -> dict:
    coverage: dict[str, dict] = {}
    for directory_name, group_name in SITE_VIEW_MODEL_GROUPS.items():
        directory = SITE_DIR / directory_name
        files = sorted(directory.glob("*.json"))
        labeled = 0
        perspective_counter: Counter[str] = Counter()
        classifications: Counter[str] = Counter()

        for path in files:
            payload = load_json(path)
            perspective_ids = payload.get("perspective_ids", [])
            if perspective_ids:
                labeled += 1
                perspective_counter.update(perspective_ids)
            classification = (payload.get("content_classification") or {}).get("classification_id")
            if classification:
                classifications[classification] += 1

        coverage[group_name] = {
            "file_count": len(files),
            "labeled_file_count": labeled,
            "unlabeled_file_count": len(files) - labeled,
            "perspective_counts": dict(perspective_counter),
            "classification_counts": dict(classifications),
        }

    return coverage


def build_broad_topic_bucket_audit(current_interpretation: dict, claims_by_id: dict[str, dict], claim_perspectives: dict[str, list[str]]) -> dict:
    broad_rest_topics = []
    high_volume_topics = []

    for topic_entry in current_interpretation["topics"]:
        topic = topic_entry["topic"]
        current_claim_ids = topic_entry.get("current_claim_ids", [])
        historical_claim_ids = topic_entry.get("historical_claim_ids", [])

        if topic.endswith(".other"):
            broad_rest_topics.append(
                {
                    "topic": topic,
                    "current_claim_count": len(current_claim_ids),
                    "historical_claim_count": len(historical_claim_ids),
                    "needs_human_review": topic_entry["needs_human_review"],
                    "confidence": topic_entry["confidence"],
                    "perspective_ids": sorted(
                        {
                            perspective_id
                            for claim_id in current_claim_ids
                            for perspective_id in claim_perspectives.get(claim_id, [])
                        }
                    ),
                    "sample_documents": sorted(
                        {
                            claims_by_id[claim_id]["source_document_id"]
                            for claim_id in current_claim_ids[:10]
                            if claim_id in claims_by_id
                        }
                    ),
                    "sample_claim_ids": current_claim_ids[:8],
                    "interpretation_summary": topic_entry["interpretation_summary"],
                }
            )

        if len(current_claim_ids) >= 20:
            high_volume_topics.append(
                {
                    "topic": topic,
                    "current_claim_count": len(current_claim_ids),
                    "historical_claim_count": len(historical_claim_ids),
                    "needs_human_review": topic_entry["needs_human_review"],
                    "confidence": topic_entry["confidence"],
                    "sample_claim_ids": current_claim_ids[:8],
                    "interpretation_summary": topic_entry["interpretation_summary"],
                }
            )

    broad_rest_topics.sort(key=lambda item: (-item["current_claim_count"], item["topic"]))
    high_volume_topics.sort(key=lambda item: (-item["current_claim_count"], item["topic"]))

    return {
        "broad_rest_topics": broad_rest_topics,
        "high_volume_topics": high_volume_topics[:10],
    }


def build_rough_claim_audit(claims: list[dict], claim_perspectives: dict[str, list[str]]) -> tuple[dict, set[str]]:
    issue_counts: Counter[str] = Counter()
    rough_claims = []
    rough_claim_ids: set[str] = set()

    for claim in claims:
        issues = detect_rough_issues(claim["statement"])
        if not issues:
            continue

        rough_claim_ids.add(claim["claim_id"])
        issue_counts.update(issues)
        rough_claims.append(
            {
                "claim_id": claim["claim_id"],
                "topic": claim["topic"],
                "document_id": claim["source_document_id"],
                "jurisdiction_level": claim["jurisdiction_level"],
                "perspective_ids": claim_perspectives.get(claim["claim_id"], []),
                "issue_codes": issues,
                "statement_excerpt": claim_excerpt(claim["statement"]),
            }
        )

    rough_claims.sort(
        key=lambda item: (
            -sum(ISSUE_WEIGHTS[issue] for issue in item["issue_codes"]),
            item["document_id"],
            item["claim_id"],
        )
    )

    return {
        "criteria": {
            "raw_letterhead": "Claim contains letterhead or formal header text instead of substantive policy content.",
            "encoding_noise": "Claim contains visibly broken encoding characters.",
            "english_summary": "Claim text is in English or reads like an English summarization rather than Dutch source-grounded text.",
            "bullet_or_heading_fragment": "Claim starts like a bullet, heading, or list fragment.",
            "fragment_too_short": "Claim is too short to stand well on its own for publication.",
            "unverified_extraction_length": (
                "Claim is long and also has a suspicious extraction signal: lowercase fragment start, "
                "missing terminal punctuation, or table/column merge fingerprint."
            ),
        },
        "issue_counts": dict(issue_counts),
        "claim_count": len(rough_claims),
        "claims": rough_claims,
    }, rough_claim_ids


def build_site_text_risk_audit(rough_claim_ids: set[str], rough_claim_lookup: dict[str, dict]) -> dict:
    files = []
    page_group_counter: Counter[str] = Counter()

    for path in site_json_files():
        payload = load_json(path)
        claim_refs = walk_claim_refs(payload)

        matched_claims = []
        seen_claim_ids: set[str] = set()
        for claim_ref in claim_refs:
            claim_id = claim_ref["claim_id"]
            if claim_id not in rough_claim_ids or claim_id in seen_claim_ids:
                continue
            seen_claim_ids.add(claim_id)
            matched_claims.append(
                {
                    "claim_id": claim_id,
                    "issue_codes": rough_claim_lookup[claim_id]["issue_codes"],
                    "statement_excerpt": rough_claim_lookup[claim_id]["statement_excerpt"],
                }
            )

        if not matched_claims:
            continue

        page_group = page_group_for_file(path.relative_to(SITE_DIR))
        page_group_counter[page_group] += len(matched_claims)
        files.append(
            {
                "path": path.relative_to(REPO_ROOT).as_posix(),
                "page_group": page_group,
                "rough_claim_count": len(matched_claims),
                "sample_claims": matched_claims[:8],
            }
        )

    files.sort(key=lambda item: (-item["rough_claim_count"], item["path"]))
    return {
        "file_count": len(files),
        "page_group_counts": dict(sorted(page_group_counter.items())),
        "files": files,
    }


def build_next_cleanup_targets(
    broad_topics: dict,
    rough_claim_audit: dict,
    site_text_risks: dict,
    review_queue: dict,
) -> list[dict]:
    targets = [
        {
            "target_id": "split_broad_rest_topics",
            "title": "Split broad *.other topic buckets before deeper text cleanup",
            "reason": "The audit still finds broad rest categories that mix multiple policy lines into one topic.",
            "related_topics": [item["topic"] for item in broad_topics["broad_rest_topics"][:5]],
            "related_review_reasons": ["unresolved_conflict"],
            "suggested_sprint": "27.x",
        },
        {
            "target_id": "clean_rough_claim_text",
            "title": "Clean publication-facing claim text before broader site prose work",
            "reason": "The audit finds claims with English summaries, letterhead fragments, encoding noise, or overly raw extraction blocks.",
            "related_topics": [item["topic"] for item in rough_claim_audit["claims"][:5]],
            "related_review_reasons": ["authority_unclear", "municipality_relevance_inferred"],
            "suggested_sprint": "26.2",
        },
        {
            "target_id": "remove_rough_claims_from_site_drilldowns",
            "title": "Reduce rough claim leakage into site drill-downs",
            "reason": "Site data already contains rough supporting evidence in detail and overview models.",
            "related_topics": [],
            "related_review_reasons": list(review_queue["summary"]["issue_counts_by_reason"].keys()),
            "suggested_sprint": "28.3",
        },
    ]

    if site_text_risks["files"]:
        targets[2]["related_files"] = [item["path"] for item in site_text_risks["files"][:6]]

    return targets


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    perspective_config = load_perspective_config()
    claims = load_claims()
    claims_by_id = {claim["claim_id"]: claim for claim in claims}
    current_interpretation = load_json(CURRENT_INTERPRETATION_PATH)
    review_queue = load_json(REVIEW_QUEUE_PATH)

    perspective_coverage, claim_perspectives = build_perspective_coverage(claims, perspective_config)
    normative_status_audit = add_zero_count_statuses(
        build_normative_status_audit(claims, claim_perspectives),
        perspective_status_values(perspective_config, "norm", "normative_status_values"),
    )
    time_status_audit = add_zero_count_statuses(
        build_time_status_audit(claims, claim_perspectives),
        perspective_status_values(perspective_config, "time", "time_status_values"),
    )
    money_status_audit = add_zero_count_statuses(
        build_money_status_audit(claims, claim_perspectives),
        perspective_status_values(perspective_config, "money", "money_status_values"),
    )
    governance_status_audit = add_zero_count_statuses(
        build_governance_status_audit(claims, claim_perspectives),
        perspective_status_values(perspective_config, "governance", "governance_status_values"),
    )
    locality_status_audit = add_zero_count_statuses(
        build_locality_status_audit(claims, claim_perspectives),
        perspective_status_values(perspective_config, "locality", "locality_status_values"),
    )
    execution_status_audit = add_zero_count_statuses(
        build_execution_status_audit(claims, claim_perspectives),
        perspective_status_values(perspective_config, "execution", "execution_status_values"),
    )
    view_model_coverage = build_view_model_coverage()
    broad_topics = build_broad_topic_bucket_audit(current_interpretation, claims_by_id, claim_perspectives)
    rough_claim_audit, rough_claim_ids = build_rough_claim_audit(claims, claim_perspectives)
    rough_claim_lookup = {item["claim_id"]: item for item in rough_claim_audit["claims"]}
    site_text_risks = build_site_text_risk_audit(rough_claim_ids, rough_claim_lookup)
    next_cleanup_targets = build_next_cleanup_targets(
        broad_topics,
        rough_claim_audit,
        site_text_risks,
        review_queue,
    )

    payload = {
        "audit_run_id": AUDIT_RUN_ID,
        "generated_on": TODAY,
        "storage": {
            "canonical_output": AUDIT_OUTPUT_PATH.relative_to(REPO_ROOT).as_posix(),
            "sprint_note": "docs/completed-plans/phase24-sprint24.2-audit.md",
        },
        "summary": {
            "claim_count": len(claims),
            "topic_count": len(current_interpretation["topics"]),
            "claims_with_perspectives": perspective_coverage["claims_with_perspectives"],
            "claims_without_perspectives": perspective_coverage["claims_without_perspectives"],
            "broad_rest_topic_count": len(broad_topics["broad_rest_topics"]),
            "high_volume_topic_count": len(broad_topics["high_volume_topics"]),
            "rough_claim_count": rough_claim_audit["claim_count"],
            "site_files_with_rough_claims": site_text_risks["file_count"],
            "open_review_items": review_queue["summary"]["review"],
        },
        "perspective_coverage": {
            "claims": perspective_coverage,
            "site_view_models": view_model_coverage,
        },
        "normative_status_audit": normative_status_audit,
        "time_status_audit": time_status_audit,
        "money_status_audit": money_status_audit,
        "governance_status_audit": governance_status_audit,
        "locality_status_audit": locality_status_audit,
        "execution_status_audit": execution_status_audit,
        "topic_bucket_audit": broad_topics,
        "rough_publication_claims": rough_claim_audit,
        "site_text_risks": site_text_risks,
        "next_cleanup_targets": next_cleanup_targets,
    }

    write_json(AUDIT_OUTPUT_PATH, payload)
    print(f"Wrote {AUDIT_OUTPUT_PATH.relative_to(REPO_ROOT).as_posix()}")


if __name__ == "__main__":
    main()
