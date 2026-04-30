from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
REVIEW_QUEUE_PATH = REPO_ROOT / "data" / "extracted" / "review_queue.json"
HUMAN_REVIEW_ROUND_PATH = REPO_ROOT / "data" / "extracted" / "human_review_round.json"
ALMERE_D6_REGISTER_PATH = REPO_ROOT / "data" / "extracted" / "municipal" / "almere_d6_responsibility_register.json"
OUTPUT_JSON_PATH = REPO_ROOT / "data" / "extracted" / "review_triage_deep_research_offload.json"
OUTPUT_MD_PATH = REPO_ROOT / "docs" / "review" / "phase31.4-review-triage-deep-research-offload.md"
PROMPT_OUTPUT_PATH = REPO_ROOT / "docs" / "review" / "phase31.4-deep-research-agent-prompts.md"


BUCKET_RULES = {
    "human_only": {
        "reason_codes": {
            "execution_capacity_need",
            "execution_decision_question",
            "execution_review_task",
            "governance_gap",
            "local_funding_gap",
        },
        "description": "Requires policy judgement, stakeholder validation, finance/controller confirmation, or local mandate clarification.",
    },
    "deep_research_candidate": {
        "reason_codes": {
            "authority_unclear",
            "expected_time_not_deadline",
            "finance_context_needs_verification",
            "local_adoption_gap",
            "local_planning_context_not_policy_deadline",
            "lower_authority_norm_signal",
            "municipality_relevance_inferred",
            "national_claim_local_relevance",
            "regional_split_context",
            "unresolved_conflict",
            "vague_region_actor",
        },
        "description": "May be reducible by a careful public-source search for stronger sources, clearer dates, actor scope, or explicit local adoption.",
    },
    "mixed_public_search_then_human": {
        "reason_codes": {
            "actor_context_needs_role_split",
            "execution_context_needs_action_split",
            "execution_dependency",
            "execution_sequencing_need",
        },
        "description": "Public search may clarify the source basis, but final role, action, sequencing or responsibility language may still need human validation.",
    },
    "pipeline_or_extraction_cleanup": {
        "reason_codes": {
            "extraction_noise_detected",
            "missing_d5_content",
            "missing_d6_content",
            "table_content_not_promoted",
        },
        "description": "Mostly repository/pipeline cleanup rather than policy review.",
    },
}


DEEP_RESEARCH_ASSIGNMENTS = [
    {
        "assignment_id": "dr_gezonde_school_almere",
        "title": "Gezonde School / mentale gezonde school Almere",
        "d6_rows": ["Gezonde School / mentale gezonde school", "JGZ Almere"],
        "question": "Find public Almere, GGD/JGZ, school-board or programme sources that show whether and how Gezonde School or mental-health school prevention is implemented in Almere, who coordinates it, and whether it is linked to D6, JGZ or SLT.",
        "likely_sources": ["Gemeente Almere", "GGD Flevoland", "JGZ Almere", "school-board pages", "Gezonde School programme pages"],
        "may_resolve": ["public-source gap", "implementation evidence", "candidate owner/executor evidence"],
        "must_not_resolve": ["formal D6 classification", "funding allocation", "mandate without local validation"],
    },
    {
        "assignment_id": "dr_digitale_operationele_infrastructuur",
        "title": "Digital and operational infrastructure for D6 Almere/Flevoland",
        "d6_rows": ["Digitale en operationele infrastructuur", "Kennis & Advies / monitoring / dashboards"],
        "question": "Find public sources for RTP Almere, RSO, Monitoring@home, shared information picture, regional data infrastructure or digital cooperation that are relevant to D5/D6 execution in Almere/Flevoland.",
        "likely_sources": ["Gemeente Almere", "Zorgzaam Flevoland", "Flever", "GGD Flevoland", "regional digital/data partnerships", "IZA/AZWA regional pages"],
        "may_resolve": ["named-source gap", "actor/context evidence", "scope evidence"],
        "must_not_resolve": ["D6 ownership", "budget split", "formal governance role"],
    },
    {
        "assignment_id": "dr_burgerinitiatieven_informele_steun",
        "title": "Burgerinitiatieven, informele steun and social-base access",
        "d6_rows": ["Burgerinitiatieven en informele steun", "Inloopvoorzieningen sociaal en gezond"],
        "question": "Find public Almere sources that identify social-base partners, volunteer support, citizen initiatives, informal care, walk-in/access points or inloopvoorzieningen relevant to D6 basisinfrastructuur.",
        "likely_sources": ["Gemeente Almere", "De Schoor", "VMCA", "MEE Samen", "wijkteams pages", "social-base programme pages"],
        "may_resolve": ["local inventory candidates", "public-source evidence", "partner mapping"],
        "must_not_resolve": ["formal D6 classification", "assigned responsibility", "confirmed funding"],
    },
    {
        "assignment_id": "dr_pga_zorgzaam_flever_interface",
        "title": "PGA / Zorgzaam Flevoland / Flever interface",
        "d6_rows": ["Positief Gezond Almere / Zorgzaam Flevoland-interface", "Financiering en budgetafbakening"],
        "question": "Find public sources that clarify the relation between Positief Gezond Almere, Zorgzaam Flevoland, Flever, IZA/AZWA work-agenda governance, transformation funding and D5/D6 execution.",
        "likely_sources": ["Positief Gezond Almere", "Zorgzaam Flevoland", "Flever", "ZonMw", "Gemeente Almere", "regional governance pages"],
        "may_resolve": ["programme-role evidence", "public funding context", "interface terminology"],
        "must_not_resolve": ["component-level budget allocation", "formal D6 governance vehicle", "controller validation"],
    },
    {
        "assignment_id": "dr_samen_sterker_wijk",
        "title": "Samen Sterker in de Wijk source strengthening",
        "d6_rows": ["Samen Sterker in de Wijk / mentale-gezondheidswijkinfrastructuur"],
        "question": "Find public sources beyond the current Almere page that describe Samen Sterker in de Wijk governance, project status, partners, funding, evaluation, or relation to mental-health neighbourhood infrastructure.",
        "likely_sources": ["Gemeente Almere", "Zorgplatform Flevoland", "GGZ Centraal", "Kwintes", "Triade", "Amethist", "Leger des Heils", "GGD Flevoland"],
        "may_resolve": ["project evidence", "partner evidence", "public implementation context"],
        "must_not_resolve": ["formal D6 status", "owner/coordinator without validation", "funding assignment"],
    },
    {
        "assignment_id": "dr_stronger_authority_sources",
        "title": "Stronger public source hunt for review-queue authority/adoption items",
        "d6_rows": [],
        "question": "For high-volume review reasons such as authority_unclear, lower_authority_norm_signal, municipality_relevance_inferred and national_claim_local_relevance, search whether stronger public sources exist in the corpus domains or official publisher sites.",
        "likely_sources": ["Rijksoverheid", "VNG", "Zorgakkoorden", "DUS-I", "wetten.nl", "Gemeente Almere", "GGD Flevoland"],
        "may_resolve": ["authority hierarchy", "public-source replacement", "explicit local adoption evidence"],
        "must_not_resolve": ["human policy judgement", "non-public decision status", "local validation"],
    },
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def bucket_for_reason(reason_code: str | None) -> str:
    for bucket_id, rule in BUCKET_RULES.items():
        if reason_code in rule["reason_codes"]:
            return bucket_id
    return "human_only"


def sample_claim_ids(item: dict[str, Any]) -> list[str]:
    return list((item.get("related_ids") or {}).get("sample_claim_ids") or [])


def build_review_triage(as_of: date) -> dict[str, Any]:
    review_queue = load_json(REVIEW_QUEUE_PATH)
    human_review_round = load_json(HUMAN_REVIEW_ROUND_PATH)
    d6_register = load_json(ALMERE_D6_REGISTER_PATH)

    bucket_counts: Counter[str] = Counter()
    reason_counts_by_bucket: dict[str, Counter[str]] = defaultdict(Counter)
    samples_by_bucket: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for item in review_queue.get("items", []):
        reason_code = item.get("reason_code")
        bucket_id = bucket_for_reason(reason_code)
        bucket_counts[bucket_id] += 1
        reason_counts_by_bucket[bucket_id][reason_code] += 1
        if len(samples_by_bucket[bucket_id]) < 8:
            samples_by_bucket[bucket_id].append(
                {
                    "review_item_id": item.get("review_item_id"),
                    "reason_code": reason_code,
                    "document_id": item.get("document_id"),
                    "summary": item.get("summary"),
                    "recommended_action": item.get("recommended_action"),
                    "sample_claim_ids": sample_claim_ids(item),
                }
            )

    d6_components = d6_register.get("components", [])
    human_only_d6_rows = [
        component["component_label"]
        for component in d6_components
        if component.get("decision_status") in {"review_needed", "unknown"}
        or component.get("funding_source") == ["unknown_needs_decision"]
        or component.get("needs_human_review")
    ]
    public_gap_rows = [
        component["component_label"]
        for component in d6_components
        if "public-source gap" in component.get("open_issue", "")
        or component["component_id"] in {
            "gezonde_school_mentale_gezonde_school",
            "digital_operational_infrastructure",
            "citizen_initiatives_informal_support",
        }
    ]

    return {
        "triage_id": "phase31_4_review_triage_deep_research_offload",
        "generated_on": as_of.isoformat(),
        "current_sprint": "Sprint 31.4 - Review triage and deep-research offload",
        "inputs": [
            "data/extracted/review_queue.json",
            "data/extracted/human_review_round.json",
            "data/extracted/municipal/almere_d6_responsibility_register.json",
            "docs/review/*.md",
        ],
        "summary": {
            "review_queue_items": len(review_queue.get("items", [])),
            "human_review_round_items": human_review_round["summary"]["review_item_count"],
            "bucket_counts": dict(bucket_counts),
            "deep_research_assignment_count": len(DEEP_RESEARCH_ASSIGNMENTS),
            "d6_rows_requiring_human_validation": len(set(human_only_d6_rows)),
            "d6_rows_with_named_public_search_gap": len(set(public_gap_rows)),
        },
        "bucket_definitions": {
            bucket_id: {
                "description": rule["description"],
                "reason_codes": sorted(rule["reason_codes"]),
                "item_count": bucket_counts.get(bucket_id, 0),
                "top_reason_codes": dict(reason_counts_by_bucket[bucket_id].most_common()),
                "sample_items": samples_by_bucket[bucket_id],
            }
            for bucket_id, rule in BUCKET_RULES.items()
        },
        "human_only_d6_rows": sorted(set(human_only_d6_rows)),
        "public_search_gap_d6_rows": sorted(set(public_gap_rows)),
        "deep_research_assignments": DEEP_RESEARCH_ASSIGNMENTS,
        "routing_rule": "Send only public-source gaps, authority/source hierarchy checks, explicit local adoption searches and source-replacement searches to deep research agents. Keep ownership, mandate, funding, D6 classification and settled-status decisions with human stakeholders or policy owners.",
        "d6_guardrail": "No D6 responsibility-register row may move to settled from a deep research result alone. A deep research result can add source candidates or reduce public-source gaps; formal classification, ownership, mandate and funding still need validation evidence.",
    }


def render_markdown(triage: dict[str, Any]) -> str:
    summary = triage["summary"]
    lines = [
        "# Sprint 31.4 Review Triage And Deep-Research Offload",
        "",
        "## Summary",
        f"Current sprint: {triage['current_sprint']}.",
        f"Generated on: {triage['generated_on']}.",
        f"Review queue items triaged: {summary['review_queue_items']}.",
        f"Deep-research assignments prepared: {summary['deep_research_assignment_count']}.",
        f"D6 rows still requiring human validation: {summary['d6_rows_requiring_human_validation']}.",
        f"D6 rows with named public-search gaps: {summary['d6_rows_with_named_public_search_gap']}.",
        "",
        triage["routing_rule"],
        "",
        "## Triage Buckets",
        "",
        "| Bucket | Item count | What it means | Top reason codes |",
        "| --- | ---: | --- | --- |",
    ]
    for bucket_id, bucket in triage["bucket_definitions"].items():
        top_reasons = ", ".join(f"`{reason}` ({count})" for reason, count in list(bucket["top_reason_codes"].items())[:5])
        lines.append(f"| `{bucket_id}` | {bucket['item_count']} | {bucket['description']} | {top_reasons} |")

    lines.extend(
        [
            "",
            "## Human-Only D6 Rows",
            "",
            "These rows still need policy-owner, stakeholder, finance/controller or internal-document validation. Do not send them to deep research as if public search can settle them.",
            "",
        ]
    )
    for row in triage["human_only_d6_rows"]:
        lines.append(f"- {row}")

    lines.extend(
        [
            "",
            "## D6 Rows With Public-Search Gaps",
            "",
            "Deep research may look for additional public sources for these rows, but it may not settle classification, owner, mandate or funding.",
            "",
        ]
    )
    for row in triage["public_search_gap_d6_rows"]:
        lines.append(f"- {row}")

    lines.extend(
        [
            "",
            "## Deep-Research Assignments",
            "",
            "| Assignment | D6 rows | Search question | May resolve | Must not resolve |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for assignment in triage["deep_research_assignments"]:
        rows = ", ".join(assignment["d6_rows"]) if assignment["d6_rows"] else "Cross-cutting review queue"
        may_resolve = ", ".join(assignment["may_resolve"])
        must_not = ", ".join(assignment["must_not_resolve"])
        lines.append(f"| `{assignment['assignment_id']}` {assignment['title']} | {rows} | {assignment['question']} | {may_resolve} | {must_not} |")

    lines.extend(
        [
            "",
            "## D6 Guardrail",
            triage["d6_guardrail"],
            "",
        ]
    )
    return "\n".join(lines)


def render_prompts(triage: dict[str, Any]) -> str:
    lines = [
        "# Sprint 31.4 Deep Research Agent Prompts",
        "",
        "## Summary",
        "Current sprint: Sprint 31.4 - Review triage and deep-research offload.",
        "",
        "Use these prompts for public-source deep research only. Agents may find and assess public sources, source gaps, authority hierarchy and conflicts. They may not decide local ownership, D6 classification, mandate, funding allocation, or settled status.",
        "",
    ]
    for assignment in triage["deep_research_assignments"]:
        lines.extend(
            [
                f"## {assignment['assignment_id']} - {assignment['title']}",
                "",
                "You are researching the AZWA/IZA/GALA policy corpus for the Almere case.",
                "",
                "Start from this repository map:",
                "",
                "https://github.com/meijer1973/azwa/blob/main/RESEARCH_AGENT_MAP.md",
                "",
                "Use repository derived data layers for orientation, but verify important factual claims against canonical source markdown/PDFs and public source URLs.",
                "",
                "Research question:",
                "",
                f"{assignment['question']}",
                "",
                f"Relevant D6 rows: {', '.join(assignment['d6_rows']) if assignment['d6_rows'] else 'cross-cutting review queue authority/adoption items'}.",
                f"Likely source types or publishers: {', '.join(assignment['likely_sources'])}.",
                f"May resolve: {', '.join(assignment['may_resolve'])}.",
                f"Must not resolve: {', '.join(assignment['must_not_resolve'])}.",
                "",
                "Deliver:",
                "",
                "- Clear conclusions.",
                "- Public sources found, with URLs and publication/source-holder details.",
                "- Whether each source is already present in `data/raw/manifest.json` or should be added.",
                "- What public sources prove, suggest, and do not prove.",
                "- Important uncertainties, conflicts, dead links or replacement sources.",
                "- Practical implications for Almere.",
                "- Explicit statement of which questions still require stakeholder validation, internal/local documents, finance/controller confirmation or policy decision.",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", default=date.today().isoformat())
    args = parser.parse_args()

    triage = build_review_triage(date.fromisoformat(args.as_of))
    write_json(OUTPUT_JSON_PATH, triage)
    OUTPUT_MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD_PATH.write_text(render_markdown(triage), encoding="utf-8")
    PROMPT_OUTPUT_PATH.write_text(render_prompts(triage), encoding="utf-8")
    print(f"Wrote {OUTPUT_JSON_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {OUTPUT_MD_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PROMPT_OUTPUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
