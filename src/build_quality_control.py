from __future__ import annotations

import json
from collections import Counter
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = REPO_ROOT / "data" / "extracted" / "document_inventory.json"
DOCUMENTS_DIR = REPO_ROOT / "data" / "extracted" / "documents"
CLAIMS_DIR = REPO_ROOT / "data" / "extracted" / "claims"
MUNICIPAL_DIR = REPO_ROOT / "data" / "extracted" / "municipal"
TABLES_DIR = REPO_ROOT / "data" / "intermediate" / "tables"
SITE_DIR = REPO_ROOT / "data" / "site"

CLAIMS_MASTER_PATH = CLAIMS_DIR / "claims_master.jsonl"
CONFLICT_REGISTER_PATH = CLAIMS_DIR / "conflict_register.json"
CURRENT_INTERPRETATION_PATH = CLAIMS_DIR / "current_interpretation.json"
D5_D6_MASTER_PATH = CLAIMS_DIR / "d5_d6_master.json"
ALMERE_CURRENT_VIEW_PATH = MUNICIPAL_DIR / "almere_current_view.json"
ALMERE_D6_RESPONSIBILITY_PATH = MUNICIPAL_DIR / "almere_d6_responsibility_register.json"
ALMERE_D6_RESPONSIBILITY_SCHEMA_PATH = REPO_ROOT / "data" / "schemas" / "almere_d6_responsibility_register.schema.json"
D6_DECISION_STATUSES = {"settled", "proposed", "inferred", "unknown", "review_needed"}
LOCAL_AUTHORITY_SOURCE_PREFIXES = ("mun_almere_", "reg_ggd_flevoland_")

QC_REPORT_PATH = REPO_ROOT / "data" / "extracted" / "qc_report.json"
REVIEW_QUEUE_PATH = REPO_ROOT / "data" / "extracted" / "review_queue.json"

QC_RUN_ID = "phase11_quality_control_v1"
TODAY = date.today().isoformat()

REQUIRED_DOCUMENT_METADATA_FIELDS = [
    "document_id",
    "title",
    "publisher",
    "publication_date",
    "document_type",
    "jurisdiction_level",
    "status",
    "source_url",
    "file_path",
    "source_classification",
    "curation_bucket",
]

REQUIRED_DOCUMENT_SCOPE_FIELDS = [
    "contains_d5",
    "contains_d6",
    "contains_structured_table",
    "contains_financial_framework",
    "contains_monitoring_framework",
    "contains_municipal_implications",
    "extraction_priority",
    "traceability_mode",
]

SEVERITY_ORDER = {"blocking": 0, "warning": 1, "review": 2}
NAVIGATION_PATTERNS = (
    "Ga terug naar de overzichtspagina",
    "Laatst bewerkt op:",
    "Raadsnummer:",
    "/page/",
)
ENCODING_PATTERNS = ("Ã", "â", "Â")

ACCEPTED_NORMATIVE_STATUSES = {
    "binding",
    "agreement",
    "expectation",
    "guidance",
    "lower_authority_signal",
    "contextual",
}

ACCEPTED_TIME_STATUSES = {
    "formal_deadline",
    "expected_moment",
    "review_or_update_moment",
    "budget_calendar_moment",
    "implementation_horizon",
    "local_planning_context",
    "source_dated_moment",
    "publication_or_context_date",
    "undated_context",
}

ACCEPTED_MONEY_STATUSES = {
    "funding_route",
    "application_condition",
    "budget_window",
    "allocation_mechanism",
    "spending_scope",
    "accountability_rule",
    "local_funding_gap",
    "double_counting_risk",
    "finance_context",
    "not_financial",
}

ACCEPTED_GOVERNANCE_STATUSES = {
    "decision_role",
    "coordination_role",
    "application_role",
    "execution_role",
    "accountability_role",
    "approval_role",
    "review_role",
    "governance_gap",
    "actor_context",
    "not_governance",
}

ACCEPTED_LOCALITY_STATUSES = {
    "explicit_almere",
    "explicit_flevoland",
    "regional_split_context",
    "national_general",
    "national_with_local_relevance",
    "inferred_local_relevance",
    "local_adoption_gap",
    "municipal_context",
    "no_locality_signal",
}

ACCEPTED_EXECUTION_STATUSES = {
    "operational_requirement",
    "implementation_activity",
    "decision_question",
    "dependency",
    "sequencing_need",
    "capacity_need",
    "review_task",
    "execution_context",
    "not_execution",
}


def load_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def relative_path(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def empty_value(value: object) -> bool:
    return value is None or value == "" or value == []


def sort_and_number_issues(issues: list[dict]) -> list[dict]:
    issues.sort(
        key=lambda item: (
            SEVERITY_ORDER[item["severity"]],
            item["check_id"],
            item.get("document_id") or "",
            item.get("topic") or "",
            item["reason_code"],
            item["summary"],
        )
    )
    numbered: list[dict] = []
    for index, issue in enumerate(issues, start=1):
        numbered_issue = dict(issue)
        numbered_issue["review_item_id"] = f"rvw_{index:03d}"
        numbered.append(numbered_issue)
    return numbered


def add_issue(
    issues: list[dict],
    seen: set[str],
    *,
    check_id: str,
    severity: str,
    reason_code: str,
    summary: str,
    recommended_action: str,
    document_id: str | None = None,
    topic: str | None = None,
    source_paths: list[str] | None = None,
    related_ids: dict | None = None,
    evidence: dict | None = None,
) -> None:
    source_paths = source_paths or []
    related_ids = related_ids or {}
    evidence = evidence or {}
    dedupe_key = json.dumps(
        {
            "check_id": check_id,
            "severity": severity,
            "reason_code": reason_code,
            "summary": summary,
            "document_id": document_id,
            "topic": topic,
            "source_paths": source_paths,
            "related_ids": related_ids,
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    if dedupe_key in seen:
        return
    seen.add(dedupe_key)
    issues.append(
        {
            "status": "open",
            "severity": severity,
            "check_id": check_id,
            "reason_code": reason_code,
            "summary": summary,
            "recommended_action": recommended_action,
            "document_id": document_id,
            "topic": topic,
            "source_paths": source_paths,
            "related_ids": related_ids,
            "evidence": evidence,
        }
    )


def statement_records(document_payload: dict) -> list[dict]:
    records: list[dict] = []
    for field_name, entry in document_payload["document_level_summary"].items():
        if not entry:
            continue
        records.append(
            {
                "container_type": "document_level_summary",
                "container_name": field_name,
                "statement_id": entry["statement_id"],
                "statement": entry["statement"],
                "statement_type": entry["statement_type"],
                "evidence": entry.get("evidence", []),
            }
        )

    for field_name, block in document_payload["structured_content"].items():
        for item in block.get("items", []):
            records.append(
                {
                    "container_type": "structured_content",
                    "container_name": field_name,
                    "statement_id": item["statement_id"],
                    "statement": item["statement"],
                    "statement_type": item["statement_type"],
                    "evidence": item.get("evidence", []),
                }
            )

    return records


def suspicious_claims(claims: list[dict]) -> list[dict]:
    flagged: list[dict] = []
    for claim in claims:
        statement = claim["statement"]
        if any(pattern in statement for pattern in ENCODING_PATTERNS):
            flagged.append(claim)
            continue
        if any(pattern in statement for pattern in NAVIGATION_PATTERNS):
            flagged.append(claim)
            continue
        if statement.startswith("**["):
            flagged.append(claim)
            continue
        if len(statement) > 450 and statement.count(";") >= 4:
            flagged.append(claim)
    return flagged


def review_reason_counts(items: list[dict]) -> dict[str, int]:
    counts = Counter(item["reason_code"] for item in items)
    return dict(sorted(counts.items()))


def severity_counts(items: list[dict]) -> dict[str, int]:
    return {
        "blocking": sum(1 for item in items if item["severity"] == "blocking"),
        "warning": sum(1 for item in items if item["severity"] == "warning"),
        "review": sum(1 for item in items if item["severity"] == "review"),
    }


def check_status(issues: list[dict], check_id: str) -> str:
    relevant = [item for item in issues if item["check_id"] == check_id]
    if any(item["severity"] == "blocking" for item in relevant):
        return "fail"
    if relevant:
        return "warn"
    return "pass"


def check_document_payloads(
    inventory_documents: list[dict],
    issues: list[dict],
    seen: set[str],
) -> tuple[dict[str, dict], dict[str, dict]]:
    document_map: dict[str, dict] = {}
    claim_file_map: dict[str, dict] = {}

    for inventory_entry in inventory_documents:
        document_id = inventory_entry["document_id"]
        document_path = DOCUMENTS_DIR / f"{document_id}.json"
        claim_path = CLAIMS_DIR / f"{document_id}.json"
        table_path = TABLES_DIR / f"{document_id}.json"

        if not document_path.exists():
            add_issue(
                issues,
                seen,
                check_id="document_payload_integrity",
                severity="blocking",
                reason_code="missing_document_extraction",
                summary=f"Document extraction JSON is missing for {document_id}.",
                recommended_action="Rerun Phase 3 for this document before trusting downstream outputs.",
                document_id=document_id,
                source_paths=[relative_path(document_path)],
            )
            continue

        if not claim_path.exists():
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="blocking",
                reason_code="missing_claim_file",
                summary=f"Claim extraction JSON is missing for {document_id}.",
                recommended_action="Rerun Phase 4 for this document before using the master claim set.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
            )
        else:
            claim_file_map[document_id] = load_json(claim_path)

        document_payload = load_json(document_path)
        document_map[document_id] = document_payload

        if document_payload.get("document_id") != document_id:
            add_issue(
                issues,
                seen,
                check_id="document_payload_integrity",
                severity="blocking",
                reason_code="document_id_mismatch",
                summary=f"Document extraction payload for {document_id} carries a mismatched document_id.",
                recommended_action="Regenerate the document extraction so the payload ID matches the file path and manifest.",
                document_id=document_id,
                source_paths=[relative_path(document_path)],
                related_ids={"payload_document_id": document_payload.get("document_id")},
            )

        metadata = document_payload.get("metadata", {})
        for field_name in REQUIRED_DOCUMENT_METADATA_FIELDS:
            if field_name not in metadata:
                add_issue(
                    issues,
                    seen,
                    check_id="document_payload_integrity",
                    severity="blocking",
                    reason_code="missing_metadata_field",
                    summary=f"Document extraction for {document_id} is missing metadata field '{field_name}'.",
                    recommended_action="Regenerate the document extraction with the required metadata fields present.",
                    document_id=document_id,
                    source_paths=[relative_path(document_path)],
                    related_ids={"missing_field": field_name},
                )

        scope = document_payload.get("extraction_scope", {})
        for field_name in REQUIRED_DOCUMENT_SCOPE_FIELDS:
            if field_name not in scope:
                add_issue(
                    issues,
                    seen,
                    check_id="document_payload_integrity",
                    severity="blocking",
                    reason_code="missing_scope_field",
                    summary=f"Document extraction for {document_id} is missing extraction_scope field '{field_name}'.",
                    recommended_action="Regenerate the document extraction with the full extraction_scope object.",
                    document_id=document_id,
                    source_paths=[relative_path(document_path)],
                    related_ids={"missing_field": field_name},
                )

        records = statement_records(document_payload)
        traceability_mode = scope.get("traceability_mode", inventory_entry["traceability_mode"])
        table_rows = load_json(table_path) if table_path.exists() else []
        known_table_ids = {row["table_id"] for row in table_rows}
        referenced_table_ids: set[str] = set()

        if inventory_entry["contains_structured_tables"] and not table_rows:
            add_issue(
                issues,
                seen,
                check_id="document_payload_integrity",
                severity="warning",
                reason_code="table_extraction_missing",
                summary=f"{document_id} is marked as table-bearing in the inventory, but no table candidates were extracted.",
                recommended_action="Inspect the structural extraction for this document and improve table capture before relying on table-dependent logic.",
                document_id=document_id,
                source_paths=[relative_path(table_path)],
            )

        for record in records:
            evidence_list = record.get("evidence", [])
            if not evidence_list:
                add_issue(
                    issues,
                    seen,
                    check_id="document_payload_integrity",
                    severity="blocking",
                    reason_code="missing_evidence",
                    summary=f"{document_id} statement {record['statement_id']} has no evidence block.",
                    recommended_action="Regenerate the document extraction so every extracted statement carries source evidence.",
                    document_id=document_id,
                    source_paths=[relative_path(document_path)],
                    related_ids={"statement_id": record["statement_id"]},
                )
                continue

            for evidence in evidence_list:
                if empty_value(evidence.get("evidence_quote")):
                    add_issue(
                        issues,
                        seen,
                        check_id="document_payload_integrity",
                        severity="blocking",
                        reason_code="missing_evidence_quote",
                        summary=f"{document_id} statement {record['statement_id']} has an evidence entry without evidence_quote.",
                        recommended_action="Regenerate the extraction and ensure every evidence entry includes the source excerpt.",
                        document_id=document_id,
                        source_paths=[relative_path(document_path)],
                        related_ids={"statement_id": record["statement_id"]},
                    )

                if traceability_mode == "page_based" and evidence.get("page") is None:
                    add_issue(
                        issues,
                        seen,
                        check_id="document_payload_integrity",
                        severity="blocking",
                        reason_code="missing_page_reference",
                        summary=f"{document_id} statement {record['statement_id']} is page-based but has no page reference.",
                        recommended_action="Fix the structural extraction so page-based evidence always preserves page numbers.",
                        document_id=document_id,
                        source_paths=[relative_path(document_path)],
                        related_ids={"statement_id": record["statement_id"]},
                    )

                if traceability_mode == "section_chunk_based" and empty_value(evidence.get("section")):
                    add_issue(
                        issues,
                        seen,
                        check_id="document_payload_integrity",
                        severity="blocking",
                        reason_code="missing_section_reference",
                        summary=f"{document_id} statement {record['statement_id']} is section-based but has no section reference.",
                        recommended_action="Fix the HTML extraction so section-chunk evidence always retains the source section path.",
                        document_id=document_id,
                        source_paths=[relative_path(document_path)],
                        related_ids={"statement_id": record["statement_id"]},
                    )

                table_id = evidence.get("table_id")
                if table_id:
                    referenced_table_ids.add(table_id)
                    if table_id not in known_table_ids:
                        add_issue(
                            issues,
                            seen,
                            check_id="document_payload_integrity",
                            severity="blocking",
                            reason_code="unknown_table_reference",
                            summary=f"{document_id} statement {record['statement_id']} references unknown table_id {table_id}.",
                            recommended_action="Regenerate the table extraction or fix the document extraction so table references point to existing table entries.",
                            document_id=document_id,
                            source_paths=[relative_path(document_path), relative_path(table_path)],
                            related_ids={"statement_id": record["statement_id"], "table_id": table_id},
                        )

        if inventory_entry["contains_d5"] and not document_payload["structured_content"]["d5"]["items"]:
            add_issue(
                issues,
                seen,
                check_id="document_payload_integrity",
                severity="warning",
                reason_code="missing_d5_content",
                summary=f"{document_id} is expected to contain D5 material, but the extraction produced no D5 items.",
                recommended_action="Review the source and improve the D5 extraction rules for this document.",
                document_id=document_id,
                source_paths=[relative_path(document_path)],
            )

        if inventory_entry["contains_d6"] and not document_payload["structured_content"]["d6"]["items"]:
            add_issue(
                issues,
                seen,
                check_id="document_payload_integrity",
                severity="warning",
                reason_code="missing_d6_content",
                summary=f"{document_id} is expected to contain D6 material, but the extraction produced no D6 items.",
                recommended_action="Review the source and improve the D6 extraction rules for this document.",
                document_id=document_id,
                source_paths=[relative_path(document_path)],
            )

        if inventory_entry["contains_structured_tables"] and table_rows and not referenced_table_ids:
            add_issue(
                issues,
                seen,
                check_id="document_payload_integrity",
                severity="review",
                reason_code="table_content_not_promoted",
                summary=f"{document_id} has extracted tables, but no document statements currently retain table_id evidence.",
                recommended_action="Promote the relevant table rows into the document extraction so downstream claims can cite the D5/D6 matrix or financing tables explicitly.",
                document_id=document_id,
                source_paths=[relative_path(document_path), relative_path(table_path)],
                evidence={"table_count": len(table_rows)},
            )

    return document_map, claim_file_map


def check_claim_payloads(
    inventory_documents: list[dict],
    claim_file_map: dict[str, dict],
    issues: list[dict],
    seen: set[str],
) -> list[dict]:
    all_per_document_claims: list[dict] = []

    for inventory_entry in inventory_documents:
        document_id = inventory_entry["document_id"]
        claim_path = CLAIMS_DIR / f"{document_id}.json"
        claim_payload = claim_file_map.get(document_id)
        if claim_payload is None:
            continue

        claims = claim_payload.get("claims", [])
        if claim_payload.get("claim_count") != len(claims):
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="blocking",
                reason_code="claim_count_mismatch",
                summary=f"{document_id} claim_count does not match the number of claim objects.",
                recommended_action="Regenerate the claim file so the count metadata matches the actual claim list.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={
                    "claim_count": claim_payload.get("claim_count"),
                    "actual_count": len(claims),
                },
            )

        contextual_claims = [claim for claim in claims if claim["source_statement_type"] == "contextual_relevance"]
        review_claims = [claim for claim in claims if claim["human_review_status"] == "needs_human_review"]
        noisy_claims = suspicious_claims(claims)
        missing_norm_status = [
            claim
            for claim in claims
            if (claim.get("normative_status") or {}).get("status") not in ACCEPTED_NORMATIVE_STATUSES
        ]
        missing_time_status = [
            claim
            for claim in claims
            if (claim.get("time_status") or {}).get("status") not in ACCEPTED_TIME_STATUSES
        ]
        missing_money_status = [
            claim
            for claim in claims
            if (claim.get("money_status") or {}).get("status") not in ACCEPTED_MONEY_STATUSES
        ]
        missing_governance_status = [
            claim
            for claim in claims
            if (claim.get("governance_status") or {}).get("status") not in ACCEPTED_GOVERNANCE_STATUSES
        ]
        missing_locality_status = [
            claim
            for claim in claims
            if (claim.get("locality_status") or {}).get("status") not in ACCEPTED_LOCALITY_STATUSES
        ]
        missing_execution_status = [
            claim
            for claim in claims
            if (claim.get("execution_status") or {}).get("status") not in ACCEPTED_EXECUTION_STATUSES
        ]
        lower_authority_norm_claims = [
            claim
            for claim in claims
            if (claim.get("normative_status") or {}).get("status") == "lower_authority_signal"
        ]
        expected_time_claims = [
            claim
            for claim in claims
            if (claim.get("time_status") or {}).get("status") == "expected_moment"
        ]
        local_planning_time_claims = [
            claim
            for claim in claims
            if (claim.get("time_status") or {}).get("status") == "local_planning_context"
        ]
        local_funding_gap_claims = [
            claim
            for claim in claims
            if (claim.get("money_status") or {}).get("status") == "local_funding_gap"
        ]
        double_counting_claims = [
            claim
            for claim in claims
            if (claim.get("money_status") or {}).get("status") == "double_counting_risk"
        ]
        finance_context_claims = [
            claim
            for claim in claims
            if (claim.get("money_status") or {}).get("status") == "finance_context"
        ]
        governance_gap_claims = [
            claim
            for claim in claims
            if (claim.get("governance_status") or {}).get("status") == "governance_gap"
        ]
        actor_context_claims = [
            claim
            for claim in claims
            if (claim.get("governance_status") or {}).get("status") == "actor_context"
        ]
        vague_region_claims = [
            claim
            for claim in claims
            if (claim.get("governance_status") or {}).get("vague_region_only")
        ]
        national_local_relevance_claims = [
            claim
            for claim in claims
            if (claim.get("locality_status") or {}).get("status") == "national_with_local_relevance"
        ]
        inferred_local_claims = [
            claim
            for claim in claims
            if (claim.get("locality_status") or {}).get("status") == "inferred_local_relevance"
        ]
        local_adoption_gap_claims = [
            claim
            for claim in claims
            if (claim.get("locality_status") or {}).get("status") == "local_adoption_gap"
        ]
        regional_split_claims = [
            claim
            for claim in claims
            if (claim.get("locality_status") or {}).get("status") == "regional_split_context"
        ]
        execution_decision_claims = [
            claim
            for claim in claims
            if (claim.get("execution_status") or {}).get("status") == "decision_question"
        ]
        execution_dependency_claims = [
            claim
            for claim in claims
            if (claim.get("execution_status") or {}).get("status") == "dependency"
        ]
        execution_capacity_claims = [
            claim
            for claim in claims
            if (claim.get("execution_status") or {}).get("status") == "capacity_need"
        ]
        execution_sequencing_claims = [
            claim
            for claim in claims
            if (claim.get("execution_status") or {}).get("status") == "sequencing_need"
        ]
        execution_review_claims = [
            claim
            for claim in claims
            if (claim.get("execution_status") or {}).get("status") == "review_task"
        ]
        execution_context_claims = [
            claim
            for claim in claims
            if (claim.get("execution_status") or {}).get("status") == "execution_context"
        ]

        if missing_norm_status:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="blocking",
                reason_code="missing_or_invalid_normative_status",
                summary=f"{document_id} contains claim(s) without a valid Sprint 27.1 normative_status.",
                recommended_action="Regenerate claims with the norm-strength classifier before using the claim stream.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in missing_norm_status[:5]]},
            )

        if missing_time_status:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="blocking",
                reason_code="missing_or_invalid_time_status",
                summary=f"{document_id} contains claim(s) without a valid Sprint 27.2 time_status.",
                recommended_action="Regenerate claims with the time-status classifier before using timeline or planning outputs.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in missing_time_status[:5]]},
            )

        if missing_money_status:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="blocking",
                reason_code="missing_or_invalid_money_status",
                summary=f"{document_id} contains claim(s) without a valid Sprint 27.3 money_status.",
                recommended_action="Regenerate claims with the money-status classifier before using finance outputs.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in missing_money_status[:5]]},
            )

        if missing_governance_status:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="blocking",
                reason_code="missing_or_invalid_governance_status",
                summary=f"{document_id} contains claim(s) without a valid Sprint 27.4 governance_status.",
                recommended_action="Regenerate claims with the governance-status classifier before using role, decision, or accountability outputs.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in missing_governance_status[:5]]},
            )

        if missing_locality_status:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="blocking",
                reason_code="missing_or_invalid_locality_status",
                summary=f"{document_id} contains claim(s) without a valid Sprint 27.5 locality_status.",
                recommended_action="Regenerate claims with the locality-status classifier before using local or regional outputs.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in missing_locality_status[:5]]},
            )

        if missing_execution_status:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="blocking",
                reason_code="missing_or_invalid_execution_status",
                summary=f"{document_id} contains claim(s) without a valid Sprint 27.6 execution_status.",
                recommended_action="Regenerate claims with the execution-status classifier before using action, dependency, or implementation outputs.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in missing_execution_status[:5]]},
            )

        if contextual_claims:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="review",
                reason_code="municipality_relevance_inferred",
                summary=f"{document_id} contains {len(contextual_claims)} contextual claim(s) where municipal relevance is inferred rather than explicitly stated.",
                recommended_action="Review these claims before treating them as firm municipal obligations or implementation facts.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={
                    "sample_claim_ids": [claim["claim_id"] for claim in contextual_claims[:5]],
                    "topic_count": len({claim["topic"] for claim in contextual_claims}),
                },
            )

        if review_claims and any(claim["instrument_type"] in {"faq", "commentary"} for claim in review_claims):
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="review",
                reason_code="authority_unclear",
                summary=f"{document_id} contributes lower-authority claims that still require human review.",
                recommended_action="Keep these claims as contextual support only until a stronger primary source confirms or replaces them.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={
                    "review_claim_count": len(review_claims),
                    "sample_claim_ids": [claim["claim_id"] for claim in review_claims[:5]],
                },
            )

        if lower_authority_norm_claims:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="review",
                reason_code="lower_authority_norm_signal",
                summary=f"{document_id} contains {len(lower_authority_norm_claims)} lower-authority norm signal claim(s).",
                recommended_action="Attribute these passages explicitly and do not present them as binding without a stronger source.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in lower_authority_norm_claims[:5]]},
            )

        if expected_time_claims:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="review",
                reason_code="expected_time_not_deadline",
                summary=f"{document_id} contains {len(expected_time_claims)} expected or indicative time claim(s).",
                recommended_action="Keep these as expected moments unless a stronger source establishes a formal deadline.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in expected_time_claims[:5]]},
            )

        if local_planning_time_claims:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="review",
                reason_code="local_planning_context_not_policy_deadline",
                summary=f"{document_id} contains {len(local_planning_time_claims)} local planning context claim(s).",
                recommended_action="Use these as local governance context and do not present them as substantive D5/D6 deadlines.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in local_planning_time_claims[:5]]},
            )

        if local_funding_gap_claims:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="review",
                reason_code="local_funding_gap",
                summary=f"{document_id} contains {len(local_funding_gap_claims)} local funding gap claim(s).",
                recommended_action="Keep these as local validation or decision points; do not fill local budget, owner, or allocation by inference.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in local_funding_gap_claims[:5]]},
            )

        if double_counting_claims:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="review",
                reason_code="double_counting_risk",
                summary=f"{document_id} contains {len(double_counting_claims)} double-counting or funding-line separation claim(s).",
                recommended_action="Keep AZWA-D5, AZWA-D6, GALA/SPUK, PGA/IZA, municipal regular budget and Zvw/insurer lines separate unless a source connects them.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in double_counting_claims[:5]]},
            )

        if finance_context_claims:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="review",
                reason_code="finance_context_needs_verification",
                summary=f"{document_id} contains {len(finance_context_claims)} finance-context claim(s) without a more specific money status.",
                recommended_action="Review these before treating them as a funding route, condition, budget window, spending rule, or accountability rule.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in finance_context_claims[:5]]},
            )

        if governance_gap_claims:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="review",
                reason_code="governance_gap",
                summary=f"{document_id} contains {len(governance_gap_claims)} governance gap claim(s).",
                recommended_action="Keep these as validation or decision points; do not fill mandate, owner, or role by inference.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in governance_gap_claims[:5]]},
            )

        if actor_context_claims:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="review",
                reason_code="actor_context_needs_role_split",
                summary=f"{document_id} contains {len(actor_context_claims)} actor-context claim(s) without a more specific governance role.",
                recommended_action="Review these before treating an actor mention as decision-making, coordination, execution, approval, application, accountability or monitoring responsibility.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in actor_context_claims[:5]]},
            )

        if vague_region_claims:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="review",
                reason_code="vague_region_actor",
                summary=f"{document_id} contains {len(vague_region_claims)} claim(s) where 'regio' is the only detected actor signal.",
                recommended_action="Clarify whether the source means IZA/AZWA-regio, GGD-regio, zorgkantoorregio, ROAZ/subregio, province, mandaatgemeente, or practical execution structure before using this as a role claim.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in vague_region_claims[:5]]},
            )

        if national_local_relevance_claims:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="review",
                reason_code="national_claim_local_relevance",
                summary=f"{document_id} contains {len(national_local_relevance_claims)} national claim(s) with local relevance.",
                recommended_action="Frame these as national lines relevant to Almere; do not present them as local adoption without local evidence.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in national_local_relevance_claims[:5]]},
            )

        if inferred_local_claims:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="review",
                reason_code="inferred_local_relevance",
                summary=f"{document_id} contains {len(inferred_local_claims)} claim(s) where local relevance is inferred.",
                recommended_action="Verify local adoption or explicit local documentation before using these as Almere facts.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in inferred_local_claims[:5]]},
            )

        if local_adoption_gap_claims:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="review",
                reason_code="local_adoption_gap",
                summary=f"{document_id} contains {len(local_adoption_gap_claims)} local adoption or documentation gap claim(s).",
                recommended_action="Keep these visible as local validation or decision questions; do not resolve them by inference.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in local_adoption_gap_claims[:5]]},
            )

        if regional_split_claims:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="review",
                reason_code="regional_split_context",
                summary=f"{document_id} contains {len(regional_split_claims)} regional split context claim(s).",
                recommended_action="Name the relevant regional scale before drawing conclusions for Almere.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in regional_split_claims[:5]]},
            )

        if execution_decision_claims:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="review",
                reason_code="execution_decision_question",
                summary=f"{document_id} contains {len(execution_decision_claims)} execution decision-question claim(s).",
                recommended_action="Keep these as possible decision questions; do not present them as decided actions.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in execution_decision_claims[:5]]},
            )

        if execution_dependency_claims:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="review",
                reason_code="execution_dependency",
                summary=f"{document_id} contains {len(execution_dependency_claims)} execution dependency claim(s).",
                recommended_action="Name the dependency and keep it open unless a source shows it has been resolved.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in execution_dependency_claims[:5]]},
            )

        if execution_capacity_claims:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="review",
                reason_code="execution_capacity_need",
                summary=f"{document_id} contains {len(execution_capacity_claims)} execution capacity claim(s).",
                recommended_action="Use these as capacity questions; do not infer staffing, fte, or ownership.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in execution_capacity_claims[:5]]},
            )

        if execution_sequencing_claims:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="review",
                reason_code="execution_sequencing_need",
                summary=f"{document_id} contains {len(execution_sequencing_claims)} execution sequencing claim(s).",
                recommended_action="Treat these as sequencing or phasing signals; do not turn them into a hard local implementation plan without source evidence.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in execution_sequencing_claims[:5]]},
            )

        if execution_review_claims:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="review",
                reason_code="execution_review_task",
                summary=f"{document_id} contains {len(execution_review_claims)} execution review or monitoring claim(s).",
                recommended_action="Keep these as review, monitoring, or validation tasks; do not present them as settled implementation choices.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in execution_review_claims[:5]]},
            )

        if execution_context_claims:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="review",
                reason_code="execution_context_needs_action_split",
                summary=f"{document_id} contains {len(execution_context_claims)} execution-context claim(s) without a more specific execution status.",
                recommended_action="Review these before turning context into an action, dependency, owner, sequence, or capacity need.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in execution_context_claims[:5]]},
            )

        if noisy_claims:
            add_issue(
                issues,
                seen,
                check_id="claim_payload_integrity",
                severity="review",
                reason_code="extraction_noise_detected",
                summary=f"{document_id} contains {len(noisy_claims)} suspicious claim statement(s) with navigation text, encoding noise, or over-concatenated list content.",
                recommended_action="Manually review these claims and tighten the extraction filters before promoting them to briefings or dashboards.",
                document_id=document_id,
                source_paths=[relative_path(claim_path)],
                related_ids={"sample_claim_ids": [claim["claim_id"] for claim in noisy_claims[:5]]},
                evidence={"sample_statements": [claim["statement"] for claim in noisy_claims[:2]]},
            )

        all_per_document_claims.extend(claims)

    return all_per_document_claims


def check_master_claim_integrity(
    per_document_claims: list[dict],
    issues: list[dict],
    seen: set[str],
) -> dict[str, dict]:
    master_claims = load_jsonl(CLAIMS_MASTER_PATH)
    master_ids = [claim["claim_id"] for claim in master_claims]
    duplicate_ids = [claim_id for claim_id, count in Counter(master_ids).items() if count > 1]

    if duplicate_ids:
        add_issue(
            issues,
            seen,
            check_id="claim_master_integrity",
            severity="blocking",
            reason_code="duplicate_claim_ids",
            summary=f"The master claim stream contains duplicate claim_id values ({len(duplicate_ids)} duplicates).",
            recommended_action="Fix the claim generator so claim_ids are unique before using the master stream for interpretation.",
            source_paths=[relative_path(CLAIMS_MASTER_PATH)],
            related_ids={"duplicate_claim_ids": duplicate_ids[:10]},
        )

    per_document_ids = [claim["claim_id"] for claim in per_document_claims]
    if Counter(per_document_ids) != Counter(master_ids):
        missing_from_master = sorted(set(per_document_ids) - set(master_ids))
        missing_from_documents = sorted(set(master_ids) - set(per_document_ids))
        add_issue(
            issues,
            seen,
            check_id="claim_master_integrity",
            severity="blocking",
            reason_code="master_claim_stream_mismatch",
            summary="The aggregated claim stream does not match the union of the per-document claim files.",
            recommended_action="Regenerate the aggregated claim stream after rerunning the per-document claim extraction step.",
            source_paths=[relative_path(CLAIMS_MASTER_PATH)],
            related_ids={
                "missing_from_master": missing_from_master[:10],
                "missing_from_documents": missing_from_documents[:10],
            },
        )

    claim_map = {claim["claim_id"]: claim for claim in master_claims}
    for claim in master_claims:
        for relation in claim.get("relations", []):
            target_claim_id = relation["target_claim_id"]
            if target_claim_id not in claim_map:
                add_issue(
                    issues,
                    seen,
                    check_id="claim_master_integrity",
                    severity="blocking",
                    reason_code="missing_relation_target",
                    summary=f"Claim {claim['claim_id']} references missing relation target {target_claim_id}.",
                    recommended_action="Fix or remove broken relation references before trusting the conflict layer.",
                    source_paths=[relative_path(CLAIMS_MASTER_PATH)],
                    related_ids={"claim_id": claim["claim_id"], "target_claim_id": target_claim_id},
                )

    return claim_map


def check_interpretation_and_views(
    claim_map: dict[str, dict],
    issues: list[dict],
    seen: set[str],
) -> tuple[dict, dict, dict]:
    conflict_register = load_json(CONFLICT_REGISTER_PATH)
    current_interpretation = load_json(CURRENT_INTERPRETATION_PATH)
    d5_d6_master = load_json(D5_D6_MASTER_PATH)
    almere_view = load_json(ALMERE_CURRENT_VIEW_PATH)

    interpretation_topics = {entry["topic"]: entry for entry in current_interpretation["topics"]}
    unresolved_topics = {
        entry["topic"]
        for entry in conflict_register["conflicts"]
        if entry["resolution_status"] != "resolved"
    }

    for entry in current_interpretation["topics"]:
        current_ids = set(entry["current_claim_ids"])
        superseded_ids = set(entry["superseded_claim_ids"])
        historical_ids = set(entry["historical_claim_ids"])
        conflicted_ids = set(entry["conflicted_claim_ids"])

        for claim_id in current_ids | superseded_ids | historical_ids | conflicted_ids:
            if claim_id not in claim_map:
                add_issue(
                    issues,
                    seen,
                    check_id="interpretation_integrity",
                    severity="blocking",
                    reason_code="unknown_interpretation_claim",
                    summary=f"Current interpretation topic {entry['topic']} references unknown claim_id {claim_id}.",
                    recommended_action="Regenerate the interpretation layer after reconciling the master claim stream.",
                    source_paths=[relative_path(CURRENT_INTERPRETATION_PATH)],
                    topic=entry["topic"],
                    related_ids={"claim_id": claim_id},
                )

        overlap_with_superseded = sorted(current_ids & superseded_ids)
        if overlap_with_superseded:
            add_issue(
                issues,
                seen,
                check_id="interpretation_integrity",
                severity="blocking",
                reason_code="claim_active_and_superseded",
                summary=f"Interpretation topic {entry['topic']} marks the same claim as both current and superseded.",
                recommended_action="Fix the precedence logic so a claim cannot remain active once superseded.",
                source_paths=[relative_path(CURRENT_INTERPRETATION_PATH)],
                topic=entry["topic"],
                related_ids={"claim_ids": overlap_with_superseded},
            )

        overlap_with_historical = sorted(current_ids & historical_ids)
        if overlap_with_historical:
            add_issue(
                issues,
                seen,
                check_id="interpretation_integrity",
                severity="blocking",
                reason_code="claim_active_and_historical",
                summary=f"Interpretation topic {entry['topic']} marks the same claim as both current and historical.",
                recommended_action="Fix the interpretation layer so historical claims are preserved separately from active ones.",
                source_paths=[relative_path(CURRENT_INTERPRETATION_PATH)],
                topic=entry["topic"],
                related_ids={"claim_ids": overlap_with_historical},
            )

    for conflict in conflict_register["conflicts"]:
        for claim_id in (
            conflict["claim_ids"]
            + conflict.get("winning_claim_ids", [])
            + conflict.get("superseded_claim_ids", [])
        ):
            if claim_id not in claim_map:
                add_issue(
                    issues,
                    seen,
                    check_id="interpretation_integrity",
                    severity="blocking",
                    reason_code="unknown_conflict_claim",
                    summary=f"Conflict register entry {conflict['conflict_id']} references unknown claim_id {claim_id}.",
                    recommended_action="Regenerate the conflict register after reconciling the claim master stream.",
                    source_paths=[relative_path(CONFLICT_REGISTER_PATH)],
                    topic=conflict["topic"],
                    related_ids={"claim_id": claim_id, "conflict_id": conflict["conflict_id"]},
                )

        if (
            conflict["resolution_status"] == "resolved"
            and conflict["recommended_resolution_rule"] == "equal_authority_and_date_stays_unresolved"
        ):
            add_issue(
                issues,
                seen,
                check_id="interpretation_integrity",
                severity="blocking",
                reason_code="resolved_conflict_uses_unresolved_rule",
                summary=f"Conflict {conflict['conflict_id']} is marked resolved even though the recommended rule says it should stay unresolved.",
                recommended_action="Fix the conflict classification logic so unresolved precedence ties are surfaced for review.",
                source_paths=[relative_path(CONFLICT_REGISTER_PATH)],
                topic=conflict["topic"],
                related_ids={"conflict_id": conflict["conflict_id"]},
            )

        if conflict["resolution_status"] != "resolved":
            add_issue(
                issues,
                seen,
                check_id="interpretation_integrity",
                severity="review",
                reason_code="unresolved_conflict",
                summary=f"Conflict {conflict['conflict_id']} for topic {conflict['topic']} still needs human review.",
                recommended_action="Resolve or annotate this topic before using it as settled policy guidance for Almere.",
                topic=conflict["topic"],
                source_paths=[relative_path(CONFLICT_REGISTER_PATH), relative_path(CURRENT_INTERPRETATION_PATH)],
                related_ids={
                    "conflict_id": conflict["conflict_id"],
                    "claim_ids": conflict["claim_ids"][:10],
                },
            )

    master_unresolved_topics = {entry["topic"] for entry in d5_d6_master["unresolved_conflicts"]}
    almere_unresolved_topics = {entry["topic"] for entry in almere_view["unresolved_conflicts"]}

    missing_from_master = sorted(unresolved_topics - master_unresolved_topics)
    if missing_from_master:
        add_issue(
            issues,
            seen,
            check_id="view_integrity",
            severity="blocking",
            reason_code="master_view_missing_unresolved_conflicts",
            summary="The D5/D6 master view is missing unresolved conflicts that exist in the conflict register.",
            recommended_action="Regenerate the master view after updating the conflict register handling.",
            source_paths=[relative_path(D5_D6_MASTER_PATH), relative_path(CONFLICT_REGISTER_PATH)],
            related_ids={"topics": missing_from_master},
        )

    missing_from_almere = sorted(unresolved_topics - almere_unresolved_topics)
    if missing_from_almere:
        add_issue(
            issues,
            seen,
            check_id="view_integrity",
            severity="blocking",
            reason_code="almere_view_missing_unresolved_conflicts",
            summary="The Almere current view is missing unresolved conflicts that exist in the conflict register.",
            recommended_action="Regenerate the Almere view after updating the conflict register handling.",
            source_paths=[relative_path(ALMERE_CURRENT_VIEW_PATH), relative_path(CONFLICT_REGISTER_PATH)],
            related_ids={"topics": missing_from_almere},
        )

    if empty_value(almere_view.get("as_of_date")):
        add_issue(
            issues,
            seen,
            check_id="view_integrity",
            severity="blocking",
            reason_code="almere_view_missing_as_of_date",
            summary="Almere current view is missing as_of_date.",
            recommended_action="Regenerate the municipal view so the computed snapshot remains temporally explicit.",
            source_paths=[relative_path(ALMERE_CURRENT_VIEW_PATH)],
        )

    return conflict_register, current_interpretation, almere_view


def check_almere_d6_responsibility_register(issues: list[dict], seen: set[str]) -> None:
    source_paths = [
        relative_path(ALMERE_D6_RESPONSIBILITY_PATH),
        relative_path(ALMERE_D6_RESPONSIBILITY_SCHEMA_PATH),
    ]
    if not ALMERE_D6_RESPONSIBILITY_PATH.exists():
        add_issue(
            issues,
            seen,
            check_id="d6_responsibility_register",
            severity="blocking",
            reason_code="register_missing",
            summary="The Almere D6 responsibility register is missing.",
            recommended_action="Generate data/extracted/municipal/almere_d6_responsibility_register.json before using D6 outputs.",
            source_paths=source_paths,
        )
        return

    if not ALMERE_D6_RESPONSIBILITY_SCHEMA_PATH.exists():
        add_issue(
            issues,
            seen,
            check_id="d6_responsibility_register",
            severity="blocking",
            reason_code="schema_missing",
            summary="The Almere D6 responsibility register schema is missing.",
            recommended_action="Add data/schemas/almere_d6_responsibility_register.schema.json and keep it aligned with the generated register.",
            source_paths=source_paths,
        )

    register = load_json(ALMERE_D6_RESPONSIBILITY_PATH)
    components = register.get("components", [])
    if len(components) < 12:
        add_issue(
            issues,
            seen,
            check_id="d6_responsibility_register",
            severity="blocking",
            reason_code="too_few_components",
            summary="The Almere D6 responsibility register has fewer than the required twelve start components.",
            recommended_action="Add rows for all required D6 components before proceeding to report or work-agenda drafting.",
            source_paths=source_paths,
            evidence={"component_count": len(components)},
        )

    required_fields = [
        "d6_component",
        "existing_almere_provision",
        "required_upgrade",
        "owner",
        "executor_or_executors",
        "cooperation_partners",
        "scale",
        "funding_source",
        "decision_status",
        "evidence_source",
        "confidence",
        "open_issue",
        "needs_human_review",
    ]
    for component in components:
        component_id = component.get("component_id") or component.get("d6_component") or "unknown_component"
        missing_fields = [field for field in required_fields if field not in component]
        if missing_fields:
            add_issue(
                issues,
                seen,
                check_id="d6_responsibility_register",
                severity="blocking",
                reason_code="required_fields_missing",
                summary=f"D6 responsibility row '{component_id}' is missing required fields.",
                recommended_action="Regenerate the register with the schema-compatible D6 responsibility fields.",
                source_paths=source_paths,
                related_ids={"component_id": component_id},
                evidence={"missing_fields": missing_fields},
            )

        decision_status = component.get("decision_status")
        if decision_status not in D6_DECISION_STATUSES:
            add_issue(
                issues,
                seen,
                check_id="d6_responsibility_register",
                severity="blocking",
                reason_code="invalid_decision_status",
                summary=f"D6 responsibility row '{component_id}' has an unsupported decision_status.",
                recommended_action="Use only settled, proposed, inferred, unknown, or review_needed.",
                source_paths=source_paths,
                related_ids={"component_id": component_id},
                evidence={"decision_status": decision_status},
            )

        evidence_sources = component.get("evidence_source") or component.get("evidence_sources") or []
        if empty_value(evidence_sources):
            add_issue(
                issues,
                seen,
                check_id="d6_responsibility_register",
                severity="blocking",
                reason_code="evidence_missing",
                summary=f"D6 responsibility row '{component_id}' has no evidence source.",
                recommended_action="Add at least one source-backed evidence reference or mark the row as incomplete before use.",
                source_paths=source_paths,
                related_ids={"component_id": component_id},
            )

        site_evidence = [source for source in evidence_sources if str(source).startswith("data/site/")]
        if site_evidence:
            add_issue(
                issues,
                seen,
                check_id="d6_responsibility_register",
                severity="blocking",
                reason_code="site_file_used_as_register_evidence",
                summary=f"D6 responsibility row '{component_id}' uses a site file as evidence.",
                recommended_action="Use raw, extracted, curated, or canonical source references for D6 responsibility rows; site files are orientation only.",
                source_paths=source_paths,
                related_ids={"component_id": component_id},
                evidence={"site_evidence": site_evidence},
            )

        if decision_status == "settled":
            evidence = component.get("evidence") or []
            local_authority_evidence = [
                item
                for item in evidence
                if str(item.get("source_id", "")).startswith(LOCAL_AUTHORITY_SOURCE_PREFIXES)
                and item.get("repository_status") == "ingested_formal_corpus"
            ]
            if not local_authority_evidence:
                add_issue(
                    issues,
                    seen,
                    check_id="d6_responsibility_register",
                    severity="blocking",
                    reason_code="settled_without_local_authority_evidence",
                    summary=f"D6 responsibility row '{component_id}' is settled without local-authority evidence.",
                    recommended_action="Only mark D6 rows settled when backed by an ingested formal local or regional authority source.",
                    source_paths=source_paths,
                    related_ids={"component_id": component_id},
                )

        if empty_value(component.get("owner")) and empty_value(component.get("open_issue")):
            add_issue(
                issues,
                seen,
                check_id="d6_responsibility_register",
                severity="blocking",
                reason_code="owner_unknown_without_open_issue",
                summary=f"D6 responsibility row '{component_id}' has no owner and no open issue.",
                recommended_action="Explain exactly which owner/responsibility decision remains open.",
                source_paths=source_paths,
                related_ids={"component_id": component_id},
            )

    d6_site_files = [
        SITE_DIR / "theme_view_models" / "basisinfrastructuur-d6.json",
        SITE_DIR / "reference_topic_view_models" / "d6-local-teams.json",
        SITE_DIR / "reference_topic_view_models" / "d6-regional-coordination.json",
        SITE_DIR / "site_almere_view.json",
    ]
    rough_markers = (
        "rough_claim",
        "bullet_or_heading_fragment",
        "fragment_too_short",
        "long_raw_excerpt",
        "unverified_extraction_length",
    )
    rough_public_files = []
    for path in d6_site_files:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if any(marker in text for marker in rough_markers):
            rough_public_files.append(relative_path(path))

    if rough_public_files:
        add_issue(
            issues,
            seen,
            check_id="d6_responsibility_register",
            severity="blocking",
            reason_code="rough_d6_claims_in_site_output",
            summary="D6 site output contains rough-claim markers.",
            recommended_action="Correct, quarantine, or explicitly exclude rough D6 claims before public or bestuurlijke use.",
            source_paths=rough_public_files,
        )


def build_report(
    issues: list[dict],
    inventory_documents: list[dict],
    claim_map: dict[str, dict],
    current_interpretation: dict,
) -> dict:
    checks = []
    for check_id, description in [
        ("document_payload_integrity", "Document extraction metadata, evidence, page/section traceability, and table references."),
        ("claim_payload_integrity", "Per-document claim outputs, review-heavy contextual claims, and suspicious extraction noise."),
        ("claim_master_integrity", "Aggregated claim stream uniqueness, completeness, and relation integrity."),
        ("interpretation_integrity", "Conflict register and current interpretation consistency."),
        ("view_integrity", "D5/D6 master and Almere current view alignment with unresolved conflicts and as_of_date."),
        ("d6_responsibility_register", "Almere D6 responsibility register schema fields, evidence, decision status, and source-layer safety."),
    ]:
        check_items = [item for item in issues if item["check_id"] == check_id]
        checks.append(
            {
                "check_id": check_id,
                "description": description,
                "status": check_status(issues, check_id),
                "issue_count": len(check_items),
                "blocking_issue_count": sum(1 for item in check_items if item["severity"] == "blocking"),
                "warning_issue_count": sum(1 for item in check_items if item["severity"] == "warning"),
                "review_issue_count": sum(1 for item in check_items if item["severity"] == "review"),
            }
        )

    summary = severity_counts(issues)
    summary.update(
        {
            "review_queue_item_count": len(issues),
            "document_count": len(inventory_documents),
            "master_claim_count": len(claim_map),
            "interpretation_topic_count": current_interpretation["topic_count"],
            "issue_counts_by_reason": review_reason_counts(issues),
        }
    )

    return {
        "qc_run_id": QC_RUN_ID,
        "generated_on": TODAY,
        "as_of_date": current_interpretation["as_of_date"],
        "summary": summary,
        "checks": checks,
    }


def build_review_queue_payload(issues: list[dict]) -> dict:
    return {
        "review_run_id": QC_RUN_ID,
        "generated_on": TODAY,
        "summary": {
            **severity_counts(issues),
            "item_count": len(issues),
            "issue_counts_by_reason": review_reason_counts(issues),
        },
        "items": issues,
    }


def main() -> None:
    inventory_payload = load_json(INVENTORY_PATH)
    inventory_documents = inventory_payload["documents"]
    issues: list[dict] = []
    seen: set[str] = set()

    _document_map, claim_file_map = check_document_payloads(inventory_documents, issues, seen)
    per_document_claims = check_claim_payloads(inventory_documents, claim_file_map, issues, seen)
    claim_map = check_master_claim_integrity(per_document_claims, issues, seen)
    _conflict_register, current_interpretation, _almere_view = check_interpretation_and_views(
        claim_map,
        issues,
        seen,
    )
    check_almere_d6_responsibility_register(issues, seen)

    numbered_issues = sort_and_number_issues(issues)
    qc_report = build_report(numbered_issues, inventory_documents, claim_map, current_interpretation)
    review_queue = build_review_queue_payload(numbered_issues)

    QC_REPORT_PATH.write_text(json.dumps(qc_report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REVIEW_QUEUE_PATH.write_text(json.dumps(review_queue, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Wrote {relative_path(QC_REPORT_PATH)}")
    print(f"Wrote {relative_path(REVIEW_QUEUE_PATH)}")
    print(
        "QC summary: "
        f"{qc_report['summary']['blocking']} blocking, "
        f"{qc_report['summary']['warning']} warning, "
        f"{qc_report['summary']['review']} review item(s)"
    )


if __name__ == "__main__":
    main()
