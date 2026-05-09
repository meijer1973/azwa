from src.build_precontact_response_workflow import build_workflow


def test_precontact_response_workflow_defines_no_answer_import_state():
    workflow = build_workflow()

    assert workflow["status"] == "repository_workflow_defined_no_answers_imported"
    assert workflow["human_validation_status"] == "no_stakeholder_answers_yet"
    assert workflow["ready_for_p7"] is False
    assert "P5 human internal dry run is pending." in workflow["p7_blockers"]


def test_precontact_response_workflow_covers_all_packet_routes():
    workflow = build_workflow()

    assert workflow["unknown_routes"] == []
    routes = {route["repo_update_effect"] for route in workflow["route_coverage"]}
    defined_routes = {route["repo_update_effect"] for route in workflow["route_definitions"]}
    assert routes == defined_routes
    assert len(routes) == 12


def test_precontact_response_workflow_preserves_return_contract():
    workflow = build_workflow()

    required = set(workflow["return_contract"]["required_fields"])
    assert {
        "vraag_id",
        "stakeholderpakket",
        "answer",
        "evidence_type",
        "evidence_reference",
        "not_my_domain_reroute",
    }.issubset(required)
    assert "do not merge answers by question text" in workflow["return_contract"]["identity_rule"]
    assert "source intake first" in workflow["return_contract"]["source_rule"]


def test_precontact_response_workflow_has_expected_targets_and_gates():
    workflow = build_workflow()

    target_ids = {target["target_id"] for target in workflow["target_artifacts"]}
    assert {
        "d5_validation_log",
        "d6_validation_log",
        "d5_finance_matrix",
        "d6_finance_matrix",
        "d5_decision_register",
        "d6_decision_register",
        "d5_d6_dependency_map",
        "source_update_log",
        "ict_privacy_register",
    }.issubset(target_ids)

    gates = {gate["gate"] for gate in workflow["quality_gates"]}
    assert {
        "no_silent_source_claims",
        "no_settled_without_evidence",
        "weak_confirmation_stays_open",
        "conflicts_escalate",
        "not_my_domain_reroutes",
    } == gates


def test_precontact_response_workflow_answer_outcomes_do_not_overclaim():
    workflow = build_workflow()

    outcome_rules = {rule["outcome"]: rule for rule in workflow["answer_outcome_rules"]}
    assert outcome_rules["confirmed_with_evidence"]["may_update_status"] is True
    for outcome, rule in outcome_rules.items():
        if outcome != "confirmed_with_evidence":
            assert rule["may_update_status"] is False
