from src.build_validation_workbook_prefill_audit import build_audit


def test_prefill_audit_covers_traceable_workbook_rows():
    audit = build_audit()

    assert audit["summary"]["sheet_count"] >= 20
    assert audit["summary"]["mapped_validation_row_count"] >= 180


def test_prefill_audit_keeps_evidence_fields_visible():
    audit = build_audit()

    assert audit["summary"]["sheets_missing_evidence_field"] == []


def test_prefill_audit_reports_targeted_cleanup_not_blank_workbooks():
    audit = build_audit()

    assert len(audit["summary"]["sheets_missing_current_working_view"]) < audit["summary"]["sheet_count"]
    assert len(audit["summary"]["sheets_missing_assessment_field"]) == 0
    assert audit["summary"]["sheets_with_language_flags"]
