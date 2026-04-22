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

CLAIMS_MASTER_PATH = CLAIMS_DIR / "claims_master.jsonl"
CONFLICT_REGISTER_PATH = CLAIMS_DIR / "conflict_register.json"
CURRENT_INTERPRETATION_PATH = CLAIMS_DIR / "current_interpretation.json"
D5_D6_MASTER_PATH = CLAIMS_DIR / "d5_d6_master.json"
ALMERE_CURRENT_VIEW_PATH = MUNICIPAL_DIR / "almere_current_view.json"

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
