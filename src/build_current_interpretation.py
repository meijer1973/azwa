from __future__ import annotations

import json
from collections import defaultdict
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CLAIMS_MASTER_PATH = REPO_ROOT / "data" / "extracted" / "claims" / "claims_master.jsonl"
RESOLUTION_RULES_PATH = REPO_ROOT / "config" / "claim_resolution_rules.json"
OUTPUT_DIR = REPO_ROOT / "data" / "extracted" / "claims"

INTERPRETATION_RUN_ID = "phase6_current_interpretation_v1"
TODAY = date.today().isoformat()
SUPERCESSION_RELATIONS = {"supersedes", "partially_supersedes", "expires", "postpones"}
LAYERING_RELATIONS = {"clarifies", "implements", "derives_from", "depends_on", "narrows", "broadens", "repeats"}


def load_claims() -> list[dict]:
    lines = CLAIMS_MASTER_PATH.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def load_rule_ids() -> dict[str, str]:
    payload = json.loads(RESOLUTION_RULES_PATH.read_text(encoding="utf-8"))
    return {rule["rule_id"]: rule["rule_id"] for rule in payload["rules"]}


def parse_iso(value: str | None) -> tuple[int, int, int]:
    if not value:
        return (0, 0, 0)
    year, month, day = value.split("-")
    return (int(year), int(month), int(day))


def sort_claims(claims: list[dict]) -> list[dict]:
    return sorted(
        claims,
        key=lambda claim: (
            claim["authority_weight"],
            parse_iso(claim["effective_from"]),
            parse_iso(claim["publication_date"]),
            claim["claim_id"],
        ),
        reverse=True,
    )


def impact_on_almere(topic: str) -> str:
    if topic.startswith("d5."):
        return "Affects which D5 functions and collaboration patterns Almere should treat as current."
    if topic.startswith("d6."):
        return "Affects which D6 infrastructure elements Almere should prioritize or localize."
    if topic.startswith("finance."):
        return "Affects Almere's funding assumptions, municipal channel, or implementation budget expectations."
    if topic.startswith("monitoring."):
        return "Affects the monitoring and evaluation cycle Almere should align with."
    if topic.startswith("timeline."):
        return "Affects planning milestones and sequencing relevant to Almere."
    if topic.startswith("governance."):
        return "Affects coordination and responsibility-setting relevant to Almere."
    if topic.startswith("municipal."):
        return "Affects how national and regional claims are translated into Almere's local implementation."
    return "Affects how Almere should interpret the current policy picture."


def pairwise_precedence_rule(winner: dict, loser: dict, rule_ids: dict[str, str]) -> str:
    if winner["authority_weight"] > loser["authority_weight"]:
        return rule_ids["higher_authority_beats_lower_authority"]
    if parse_iso(winner["effective_from"]) > parse_iso(loser["effective_from"]):
        return rule_ids["later_effective_date_beats_earlier_when_authority_equal"]
    return rule_ids["equal_authority_and_date_stays_unresolved"]


def relation_index(claims: list[dict]) -> tuple[dict[str, list[dict]], dict[str, list[dict]]]:
    by_source: dict[str, list[dict]] = defaultdict(list)
    by_target: dict[str, list[dict]] = defaultdict(list)
    for claim in claims:
        for relation in claim["relations"]:
            relation_record = {
                "source_claim_id": claim["claim_id"],
                "type": relation["type"],
                "target_claim_id": relation["target_claim_id"],
                "note": relation.get("note"),
            }
            by_source[claim["claim_id"]].append(relation_record)
            by_target[relation["target_claim_id"]].append(relation_record)
    return by_source, by_target


def build_superseded_set(
    topic_claims: list[dict],
    topic_claim_ids: set[str],
    relations_by_source: dict[str, list[dict]],
    rule_ids: dict[str, str],
) -> tuple[set[str], list[str]]:
    superseded_ids: set[str] = set()
    rule_applications: list[str] = []
    current_by_id = {claim["claim_id"]: claim for claim in topic_claims}
    sorted_claims = sort_claims(topic_claims)

    for claim in topic_claims:
        for relation in relations_by_source.get(claim["claim_id"], []):
            if relation["type"] in SUPERCESSION_RELATIONS and relation["target_claim_id"] in topic_claim_ids:
                superseded_ids.add(relation["target_claim_id"])
                target_claim = current_by_id[relation["target_claim_id"]]
                rule_applications.append(pairwise_precedence_rule(claim, target_claim, rule_ids))

    non_historical = [claim for claim in sorted_claims if claim["validity_status"] != "historical"]
    if not non_historical:
        return superseded_ids, dedupe(rule_applications)

    top_current = non_historical[0]
    for claim in topic_claims:
        if claim["validity_status"] != "historical":
            continue
        if claim["claim_id"] in superseded_ids:
            continue
        precedence_rule = pairwise_precedence_rule(top_current, claim, rule_ids)
        if precedence_rule != rule_ids["equal_authority_and_date_stays_unresolved"]:
            superseded_ids.add(claim["claim_id"])
            rule_applications.append(precedence_rule)

    return superseded_ids, dedupe(rule_applications)


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def build_conflict_entry(
    topic: str,
    topic_claims: list[dict],
    current_claims: list[dict],
    superseded_ids: set[str],
    same_topic_relations: list[dict],
    rule_ids: dict[str, str],
) -> dict | None:
    if len(topic_claims) <= 1:
        return None

    has_supersession = any(relation["type"] in SUPERCESSION_RELATIONS for relation in same_topic_relations)
    has_historical = any(claim["validity_status"] == "historical" for claim in topic_claims)
    jurisdictions = {claim["jurisdiction_level"] for claim in current_claims}
    has_local_layer = "national" in jurisdictions and ("regional" in jurisdictions or "municipal" in jurisdictions)
    has_layering_relation = any(relation["type"] in LAYERING_RELATIONS for relation in same_topic_relations)

    if has_supersession:
        conflict_type = "supersession"
        resolution_status = "resolved"
        recommended_rule = rule_ids["later_effective_date_beats_earlier_when_authority_equal"]
    elif has_historical and current_claims:
        conflict_type = "precedence_overlap"
        resolution_status = "resolved"
        top_current = sort_claims(current_claims)[0]
        historical_claims = [claim for claim in topic_claims if claim["validity_status"] == "historical"]
        recommended_rule = pairwise_precedence_rule(top_current, historical_claims[0], rule_ids)
    elif has_local_layer:
        conflict_type = "localization_overlap"
        resolution_status = "parallel_claims"
        recommended_rule = rule_ids["municipal_documents_cannot_override_national_obligations"]
    elif has_layering_relation:
        conflict_type = "implementation_layering"
        resolution_status = "parallel_claims"
        recommended_rule = rule_ids["guidance_may_clarify_but_not_override_stronger_norm"]
    else:
        return None

    needs_human_review = any(
        claim["human_review_status"] == "needs_human_review" for claim in current_claims
    ) and resolution_status != "resolved"
    notes = build_conflict_note(topic, current_claims, superseded_ids, has_local_layer, has_layering_relation)

    return {
        "conflict_id": f"conflict__{topic.replace('.', '__')}",
        "topic": topic,
        "claim_ids": [claim["claim_id"] for claim in sort_claims(topic_claims)],
        "conflict_type": conflict_type,
        "resolution_status": resolution_status,
        "recommended_resolution_rule": recommended_rule,
        "impact_on_almere": impact_on_almere(topic),
        "winning_claim_ids": [claim["claim_id"] for claim in sort_claims(current_claims)],
        "superseded_claim_ids": sorted(superseded_ids),
        "needs_human_review": needs_human_review,
        "notes": notes,
    }


def build_conflict_note(
    topic: str,
    current_claims: list[dict],
    superseded_ids: set[str],
    has_local_layer: bool,
    has_layering_relation: bool,
) -> str:
    if superseded_ids:
        return (
            f"Current interpretation retains {len(current_claims)} non-superseded claim(s) for {topic} "
            f"and preserves {len(superseded_ids)} earlier claim(s) as history."
        )
    if has_local_layer:
        return (
            f"Current interpretation keeps the higher-authority national baseline and also preserves lower-authority "
            f"regional or municipal localization claims for Almere."
        )
    if has_layering_relation:
        return "Current interpretation treats the topic as layered rather than contradictory."
    return "Current interpretation preserves multiple compatible claims for this topic."


def summarize_topic(
    topic: str,
    current_claims: list[dict],
    historical_claims: list[dict],
    superseded_ids: set[str],
    same_topic_relations: list[dict],
    needs_human_review: bool,
) -> str:
    if not current_claims:
        return (
            f"No active current claim was selected for {topic}; "
            f"{len(historical_claims)} historical claim(s) remain preserved for traceability."
        )

    sorted_current = sort_claims(current_claims)
    primary = sorted_current[0]
    jurisdictions = {claim["jurisdiction_level"] for claim in current_claims}
    has_local_layer = "national" in jurisdictions and ("regional" in jurisdictions or "municipal" in jurisdictions)
    has_layering_relation = any(relation["type"] in LAYERING_RELATIONS for relation in same_topic_relations)

    if len(current_claims) == 1:
        prefix = ""
        if superseded_ids:
            prefix = "Current view prefers this claim over earlier preserved wording. "
        elif needs_human_review:
            prefix = "Current view is provisional because it rests on contextual or local evidence. "
        return prefix + primary["statement"]

    if has_local_layer:
        return (
            f"Current view combines {len(current_claims)} compatible claims. The national claim set is the operative "
            f"baseline, while regional or municipal claims localize implementation for Almere."
        )

    if has_layering_relation:
        return (
            f"Current view combines {len(current_claims)} compatible claims led by {primary['source_document_id']}. "
            f"Lower-authority claims clarify or implement the baseline rather than replacing it."
        )

    return (
        f"Current view combines {len(current_claims)} compatible claims for {topic}, led by "
        f"{primary['source_document_id']}: {primary['statement']}"
    )


def interpretation_confidence(current_claims: list[dict], needs_human_review: bool) -> float:
    if not current_claims:
        return 0.2
    base = sum(claim["confidence"] for claim in current_claims) / len(current_claims)
    if len(current_claims) > 1:
        base -= 0.03
    if needs_human_review:
        base -= 0.08
    return round(max(0.2, min(base, 0.98)), 2)


def main() -> None:
    claims = load_claims()
    rule_ids = load_rule_ids()
    relations_by_source, _relations_by_target = relation_index(claims)
    claims_by_topic: dict[str, list[dict]] = defaultdict(list)

    for claim in claims:
        claims_by_topic[claim["topic"]].append(claim)

    source_runs = dedupe([claim["claim_extraction_run_id"] for claim in claims])
    conflict_entries: list[dict] = []
    interpretation_entries: list[dict] = []

    for topic in sorted(claims_by_topic):
        topic_claims = claims_by_topic[topic]
        topic_claim_ids = {claim["claim_id"] for claim in topic_claims}
        same_topic_relations = [
            relation
            for claim in topic_claims
            for relation in relations_by_source.get(claim["claim_id"], [])
            if relation["target_claim_id"] in topic_claim_ids
        ]

        superseded_ids, _rule_applications = build_superseded_set(
            topic_claims,
            topic_claim_ids,
            relations_by_source,
            rule_ids,
        )

        current_claims = [
            claim
            for claim in topic_claims
            if claim["claim_id"] not in superseded_ids and claim["validity_status"] != "historical"
        ]
        current_claims = sort_claims(current_claims)
        historical_claims = sort_claims([claim for claim in topic_claims if claim["validity_status"] == "historical"])
        conflicted_claim_ids: list[str] = []

        needs_human_review = any(
            claim["human_review_status"] == "needs_human_review" for claim in current_claims
        )

        conflict_entry = build_conflict_entry(
            topic,
            topic_claims,
            current_claims,
            superseded_ids,
            same_topic_relations,
            rule_ids,
        )
        if conflict_entry:
            conflict_entries.append(conflict_entry)
            if conflict_entry["resolution_status"] == "needs_human_review":
                conflicted_claim_ids = conflict_entry["claim_ids"]
                needs_human_review = True

        interpretation_entries.append(
            {
                "topic": topic,
                "as_of_date": TODAY,
                "current_claim_ids": [claim["claim_id"] for claim in current_claims],
                "historical_claim_ids": [claim["claim_id"] for claim in historical_claims],
                "superseded_claim_ids": sorted(superseded_ids),
                "conflicted_claim_ids": conflicted_claim_ids,
                "interpretation_summary": summarize_topic(
                    topic,
                    current_claims,
                    historical_claims,
                    superseded_ids,
                    same_topic_relations,
                    needs_human_review,
                ),
                "confidence": interpretation_confidence(current_claims, needs_human_review),
                "needs_human_review": needs_human_review,
            }
        )

    conflict_payload = {
        "interpretation_run_id": INTERPRETATION_RUN_ID,
        "generated_on": TODAY,
        "as_of_date": TODAY,
        "source_claim_extraction_runs": source_runs,
        "conflict_count": len(conflict_entries),
        "conflicts": conflict_entries,
    }

    interpretation_payload = {
        "interpretation_run_id": INTERPRETATION_RUN_ID,
        "generated_on": TODAY,
        "as_of_date": TODAY,
        "source_claim_extraction_runs": source_runs,
        "topic_count": len(interpretation_entries),
        "topics": interpretation_entries,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    conflict_path = OUTPUT_DIR / "conflict_register.json"
    interpretation_path = OUTPUT_DIR / "current_interpretation.json"
    conflict_path.write_text(json.dumps(conflict_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    interpretation_path.write_text(
        json.dumps(interpretation_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {conflict_path.relative_to(REPO_ROOT).as_posix()}")
    print(f"Wrote {interpretation_path.relative_to(REPO_ROOT).as_posix()}")


if __name__ == "__main__":
    main()
