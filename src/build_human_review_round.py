from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "config" / "data_quality_perspectives.json"
REVIEW_QUEUE_PATH = REPO_ROOT / "data" / "extracted" / "review_queue.json"
CLAIMS_MASTER_PATH = REPO_ROOT / "data" / "extracted" / "claims" / "claims_master.jsonl"
MONTHLY_AUDIT_PATH = REPO_ROOT / "data" / "extracted" / "monthly_source_audit.json"
OUTPUT_JSON_PATH = REPO_ROOT / "data" / "extracted" / "human_review_round.json"
OUTPUT_MD_PATH = REPO_ROOT / "docs" / "review" / "phase31.3-human-review-round.md"


REASON_PERSPECTIVE_FALLBACKS = {
    "authority_unclear": ["norm"],
    "lower_authority_norm_signal": ["norm"],
    "expected_time_not_deadline": ["time"],
    "local_planning_context_not_policy_deadline": ["time"],
    "finance_context_needs_verification": ["money"],
    "local_funding_gap": ["money"],
    "actor_context_needs_role_split": ["governance"],
    "governance_gap": ["governance"],
    "vague_region_actor": ["governance"],
    "municipality_relevance_inferred": ["locality"],
    "national_claim_local_relevance": ["locality"],
    "local_adoption_gap": ["locality"],
    "regional_split_context": ["locality"],
    "execution_capacity_need": ["execution"],
    "execution_context_needs_action_split": ["execution"],
    "execution_decision_question": ["execution"],
    "execution_dependency": ["execution"],
    "execution_review_task": ["execution"],
    "execution_sequencing_need": ["execution"],
}


PERSPECTIVE_REVIEW_QUESTIONS = {
    "norm": [
        "Welke bronhouder of bronsoort moet expliciet worden genoemd voordat deze normtaal veilig is?",
        "Is dit bindend, een afspraak, een verwachting, guidance of alleen context?",
    ],
    "time": [
        "Is dit een formele deadline, een verwacht moment, een publicatiedatum of lokale planningscontext?",
        "Mag deze datum in publieke tekst als termijn worden gebruikt, of alleen als indicatieve planning?",
    ],
    "money": [
        "Welke financieringsroute, budgetperiode of verantwoordingsregel volgt direct uit de bron?",
        "Welke lokale middelenmix, dekking of dubbeltelling blijft een finance/controller-vraag?",
    ],
    "governance": [
        "Noemt de bron besluitvorming, coordinatie, uitvoering, eigenaarschap, goedkeuring of alleen een actor?",
        "Welke actorrol moet expliciet door een mens worden bevestigd voordat de tekst sterker mag worden?",
    ],
    "locality": [
        "Is de claim expliciet Almere, expliciet Flevoland, algemeen landelijk of alleen lokaal relevant door interpretatie?",
        "Welke lokale bron of stakeholdervalidatie is nodig voordat dit als Almeerse keuze kan worden geschreven?",
    ],
    "execution": [
        "Is dit een feitelijke uitvoeringsactiviteit, een mogelijke opvolgactie, een afhankelijkheid of een reviewtaak?",
        "Welke actie, volgorde, capaciteit of eigenaar mag niet worden ingevuld zonder lokale bevestiging?",
    ],
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_claims() -> dict[str, dict[str, Any]]:
    claims: dict[str, dict[str, Any]] = {}
    for line in CLAIMS_MASTER_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        claim = json.loads(line)
        claims[claim["claim_id"]] = claim
    return claims


def perspective_ids_for_topic(topic: str | None, perspective_config: dict[str, Any]) -> set[str]:
    if not topic:
        return set()
    perspective_ids: set[str] = set()
    for perspective in perspective_config["perspectives"]:
        perspective_id = perspective["perspective_id"]
        if any(topic.startswith(prefix) for prefix in perspective.get("topic_prefixes", [])):
            perspective_ids.add(perspective_id)
        if topic in perspective.get("topic_ids", []):
            perspective_ids.add(perspective_id)
    return perspective_ids


def perspective_ids_for_claim(claim: dict[str, Any], perspective_config: dict[str, Any]) -> set[str]:
    perspective_ids = perspective_ids_for_topic(claim.get("topic"), perspective_config)
    jurisdiction_level = claim.get("jurisdiction_level")
    for perspective in perspective_config["perspectives"]:
        if jurisdiction_level in perspective.get("jurisdiction_level_hints", []):
            perspective_ids.add(perspective["perspective_id"])
    return perspective_ids


def sample_claim_ids(review_item: dict[str, Any]) -> list[str]:
    return list((review_item.get("related_ids") or {}).get("sample_claim_ids") or [])


def derive_item_perspectives(
    review_item: dict[str, Any],
    claim_index: dict[str, dict[str, Any]],
    perspective_config: dict[str, Any],
) -> list[str]:
    perspective_ids = perspective_ids_for_topic(review_item.get("topic"), perspective_config)
    for claim_id in sample_claim_ids(review_item):
        claim = claim_index.get(claim_id)
        if claim:
            perspective_ids.update(perspective_ids_for_claim(claim, perspective_config))
    perspective_ids.update(REASON_PERSPECTIVE_FALLBACKS.get(review_item.get("reason_code"), []))
    return sorted(perspective_ids)


def item_record(review_item: dict[str, Any], perspective_ids: list[str]) -> dict[str, Any]:
    return {
        "review_item_id": review_item.get("review_item_id"),
        "severity": review_item.get("severity"),
        "reason_code": review_item.get("reason_code"),
        "document_id": review_item.get("document_id"),
        "topic": review_item.get("topic"),
        "summary": review_item.get("summary"),
        "recommended_action": review_item.get("recommended_action"),
        "sample_claim_ids": sample_claim_ids(review_item),
        "source_paths": review_item.get("source_paths") or [],
        "perspective_ids": perspective_ids,
    }


def build_review_round(as_of: date) -> dict[str, Any]:
    perspective_config = load_json(CONFIG_PATH)
    review_queue = load_json(REVIEW_QUEUE_PATH)
    claim_index = load_claims()
    monthly_audit = load_json(MONTHLY_AUDIT_PATH) if MONTHLY_AUDIT_PATH.exists() else None
    perspective_titles = {item["perspective_id"]: item["title"] for item in perspective_config["perspectives"]}

    records: list[dict[str, Any]] = []
    by_perspective: dict[str, list[dict[str, Any]]] = defaultdict(list)
    unassigned: list[dict[str, Any]] = []

    for review_item in review_queue.get("items", []):
        perspective_ids = derive_item_perspectives(review_item, claim_index, perspective_config)
        record = item_record(review_item, perspective_ids)
        records.append(record)
        if perspective_ids:
            for perspective_id in perspective_ids:
                by_perspective[perspective_id].append(record)
        else:
            unassigned.append(record)

    perspective_sections = []
    for perspective_id in ["norm", "time", "money", "governance", "locality", "execution"]:
        items = by_perspective.get(perspective_id, [])
        reason_counts = Counter(item["reason_code"] for item in items)
        severity_counts = Counter(item["severity"] for item in items)
        documents = Counter(item["document_id"] for item in items if item.get("document_id"))
        perspective_sections.append(
            {
                "perspective_id": perspective_id,
                "title": perspective_titles.get(perspective_id, perspective_id),
                "review_item_count": len(items),
                "severity_counts": dict(severity_counts),
                "top_reason_codes": dict(reason_counts.most_common(8)),
                "top_documents": dict(documents.most_common(6)),
                "review_questions": PERSPECTIVE_REVIEW_QUESTIONS[perspective_id],
                "sample_items": items[:8],
            }
        )

    monthly_summary = None
    if monthly_audit:
        monthly_summary = {
            "generated_on": monthly_audit["generated_on"],
            "watchlist_count": monthly_audit["summary"]["watchlist_count"],
            "pending_replacement_count": monthly_audit["summary"]["pending_replacement_count"],
            "pending_timeline_item_count": monthly_audit["summary"]["pending_timeline_item_count"],
            "live_link_issue_count": monthly_audit["summary"]["live_link_issue_count"],
            "live_link_review_count": monthly_audit["summary"]["live_link_review_count"],
            "boundary": monthly_audit["source_boundary"],
        }

    return {
        "review_round_id": "phase31_3_human_review_round",
        "generated_on": as_of.isoformat(),
        "current_sprint": "Sprint 31.3 - Reviewronde met menselijke beoordelaars",
        "source_paths": [
            "data/extracted/review_queue.json",
            "data/extracted/data_quality_audit.json",
            "data/extracted/monthly_source_audit.json",
            "docs/human-review-guidance.md",
        ],
        "summary": {
            "review_item_count": len(records),
            "unassigned_item_count": len(unassigned),
            "blocking_count": review_queue.get("summary", {}).get("blocking", 0),
            "warning_count": review_queue.get("summary", {}).get("warning", 0),
            "review_count": review_queue.get("summary", {}).get("review", 0),
            "reason_counts_by_code": review_queue.get("summary", {}).get("issue_counts_by_reason", {}),
        },
        "perspectives": perspective_sections,
        "unassigned_sample_items": unassigned[:8],
        "monthly_source_audit_summary": monthly_summary,
        "decision_recording_rule": "Reviewer decisions must be recorded as human review decisions or validation records. They do not become source claims unless backed by a canonical source or explicit validation evidence.",
        "d6_guardrail": "Do not mark D6 responsibility-register rows as settled during Sprint 31.3. Sprint 25.6 remains parked until stakeholder validation records, local/internal documents, finance/controller confirmation, or an explicit policy decision exist.",
    }


def render_markdown(review_round: dict[str, Any]) -> str:
    summary = review_round["summary"]
    lines = [
        "# Sprint 31.3 Human Review Round",
        "",
        "## Summary",
        f"Current sprint: {review_round['current_sprint']}.",
        f"Generated on: {review_round['generated_on']}.",
        f"Review items: {summary['review_item_count']}.",
        f"Warnings: {summary['warning_count']}.",
        f"Review-level items: {summary['review_count']}.",
        f"Unassigned items: {summary['unassigned_item_count']}.",
        "",
        "This pack is for human reviewers. It does not settle policy, D6 ownership, funding, timing, or execution questions by itself.",
        "",
        "## How To Use This Pack",
        "- Reviewers should answer the questions for their perspective and cite the source, validation record, or decision basis they used.",
        "- Treat lower-authority, local-adoption, funding, governance and execution signals as review prompts until confirmed.",
        "- Record reviewer decisions separately from source claims. Do not rewrite the claim layer to match a judgement unless the judgement has source or validation evidence.",
        f"- D6 guardrail: {review_round['d6_guardrail']}",
        "",
        "## Monthly Source Audit Carry-In",
        "",
    ]
    monthly = review_round.get("monthly_source_audit_summary")
    if monthly:
        lines.extend(
            [
                f"- Audit generated on: {monthly['generated_on']}.",
                f"- Watchlist rows: {monthly['watchlist_count']}.",
                f"- Pending replacements: {monthly['pending_replacement_count']}.",
                f"- Pending timeline items: {monthly['pending_timeline_item_count']}.",
                f"- Live link issues: {monthly['live_link_issue_count']}.",
                f"- Live link review items: {monthly['live_link_review_count']}.",
                f"- Boundary: {monthly['boundary']}",
                "",
            ]
        )
    else:
        lines.extend(["- No monthly source audit available.", ""])

    lines.extend(
        [
            "## Perspective Review Lists",
            "",
        ]
    )
    for perspective in review_round["perspectives"]:
        lines.extend(
            [
                f"### {perspective['title']}",
                "",
                f"Review items: {perspective['review_item_count']}.",
                "",
                "Reviewer questions:",
            ]
        )
        for question in perspective["review_questions"]:
            lines.append(f"- {question}")
        lines.extend(["", "Top reason codes:"])
        if perspective["top_reason_codes"]:
            for reason, count in perspective["top_reason_codes"].items():
                lines.append(f"- `{reason}`: {count}")
        else:
            lines.append("- None.")
        lines.extend(["", "Sample items:"])
        if perspective["sample_items"]:
            for item in perspective["sample_items"][:5]:
                lines.append(
                    f"- `{item['review_item_id']}` / `{item['reason_code']}`: {item['summary']} Action: {item['recommended_action']}"
                )
        else:
            lines.append("- None.")
        lines.append("")

    lines.extend(
        [
            "## Decision Recording Rule",
            review_round["decision_recording_rule"],
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", default=date.today().isoformat())
    args = parser.parse_args()

    review_round = build_review_round(date.fromisoformat(args.as_of))
    write_json(OUTPUT_JSON_PATH, review_round)
    OUTPUT_MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD_PATH.write_text(render_markdown(review_round), encoding="utf-8")
    print(f"Wrote {OUTPUT_JSON_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {OUTPUT_MD_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
