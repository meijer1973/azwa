from src.build_precontact_agent_plan import build_plan


def test_precontact_agent_plan_has_expected_agents():
    plan = build_plan()
    agent_ids = {agent["agent_id"] for agent in plan["agents"]}

    assert plan["dispatch_status"] == "prepared_not_sent"
    assert agent_ids == {
        "p3_evidence_prefill_audit",
        "p3_d5_source_update_watchlist",
        "p3_d5_d6_dependency_mapping",
        "p3_policymaker_readability",
        "p3_finance_risk_precheck",
    }


def test_precontact_agent_plan_blocks_stakeholder_contact_and_settlement():
    plan = build_plan()
    guardrails = " ".join(plan["guardrails"]).lower()

    assert "do not contact policymakers" in guardrails
    assert "do not settle d5 or d6 ownership" in guardrails

    for agent in plan["agents"]:
        assert agent["dispatch_status"] == "prepared_not_sent"
        prompt = agent["prompt"].lower()
        assert "do not contact policymakers" in prompt
        assert "must not resolve" in prompt


def test_precontact_agent_prompts_have_structured_deliverables():
    plan = build_plan()

    for agent in plan["agents"]:
        assert agent["deliverable_fields"]
        assert "Deliver a concise table with these fields:" in agent["prompt"]
        for field in agent["deliverable_fields"]:
            assert f"`{field}`" in agent["prompt"]
