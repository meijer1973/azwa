from src.build_precontact_internal_dry_run import build_dry_run


def test_precontact_internal_dry_run_is_repository_checked_but_human_pending():
    dry_run = build_dry_run()

    assert dry_run["repository_check_status"] == "completed"
    assert dry_run["human_dry_run_status"] == "pending_internal_reviewers"
    assert "Blocks P7" in dry_run["gate_effect"]
    assert "does not block P6" in dry_run["gate_effect"]


def test_precontact_internal_dry_run_has_required_case_coverage():
    dry_run = build_dry_run()

    case_types = {case["case_type"] for case in dry_run["cases"]}
    assert {
        "d5_tab_answerability",
        "d6_tab_answerability",
        "finance_row",
        "evidence_field",
        "not_my_domain_reroute",
    }.issubset(case_types)


def test_precontact_internal_dry_run_cases_keep_traceability_and_csv_fields():
    dry_run = build_dry_run()

    for case in dry_run["cases"]:
        assert case["packet_id"]
        assert case["vraag_id"]
        assert case["workbook_path"].endswith(".xlsx")
        assert case["human_entry_surface"] == "excel_workbook"
        assert case["repository_traceability_surface"] == "csv_packet_reference"
        assert case["sheet"]
        assert case["question_text"]
        assert case["repo_update_effect"]
        assert case["bewijstype_verplicht"] is True
        assert not case["missing_required_csv_fields"]


def test_precontact_internal_dry_run_automated_checks_pass():
    dry_run = build_dry_run()

    assert dry_run["automated_checks"]
    assert {check["status"] for check in dry_run["automated_checks"]} == {"pass"}
