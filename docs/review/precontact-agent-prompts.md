# Pre-contact Agent Prompts

## Summary
Current sprint: Sprint 33.P3 - Pre-contact validation-readiness: targeted pre-contact agents.

Generated on: 2026-05-09.

This file contains narrow, copy-ready agent prompts for pre-contact QA. These prompts are prepared, not sent. They are meant to reduce validation workload before stakeholder packets are built.

## Guardrails

- This is pre-contact validation-readiness work, not stakeholder validation.
- Do not contact policymakers, municipal officers, providers, insurers, GGD/JGZ, finance/controller roles or partners.
- Do not settle D5 or D6 ownership, mandate, funding, formal classification or safe final wording.
- Do not treat Excel workbook text, generated JSON, dashboard text or deep-research reports as public source evidence.
- If a public source is found, mark it as a source-intake candidate; it must be ingested and checked through the repository pipeline before use.
- Return concise findings that reduce human workload before packet export.

## Agent Set

| Agent | Priority | Purpose | Status |
| --- | ---: | --- | --- |
| `p3_evidence_prefill_audit` | 1 | Check whether current workbook working views have enough repository/source support before humans see them. | `prepared_not_sent` |
| `p3_d5_source_update_watchlist` | 2 | Create a narrow watchlist for time-dependent D5 sources expected before workagenda drafting. | `prepared_not_sent` |
| `p3_d5_d6_dependency_mapping` | 3 | Map D5 workagenda components to likely D6 prerequisites so D5 packets do not promise implementation without social-base infrastructure. | `prepared_not_sent` |
| `p3_policymaker_readability` | 4 | Make stakeholder-facing packet language plain Dutch and easy to answer. | `prepared_not_sent` |
| `p3_finance_risk_precheck` | 5 | Identify where finance/controller validation is unavoidable before packet export. | `prepared_not_sent` |

## Evidence-prefill audit agent

Agent ID: `p3_evidence_prefill_audit`

```text
You are supporting the AZWA/IZA/GALA Almere repository during Sprint 33.P3: targeted pre-contact validation-readiness.

Task: Evidence-prefill audit agent

Purpose:
Check whether current workbook working views have enough repository/source support before humans see them.

Start from these repository inputs:
- `RESEARCH_AGENT_MAP.md`
- `docs/data-quality-roadmap.md`
- `docs/review/validation-instrument-register.md`
- `docs/review/validation-workbook-traceability-audit.md`
- `docs/review/validation-workbook-prefill-audit.md`
- `data/workagenda/validation_workbook_traceability_map.json`
- `data/workagenda/validation_workbook_prefill_audit.json`
- `docs/review/D5_validatieformat_werkagenda_Almere_v0.2.xlsx`
- `docs/review/Almere_D6_validatieformats.xlsx`
- `data/workagenda/d5_status_matrix.json`
- `data/workagenda/d5_validation_tickets.json`
- `docs/review/almere_d6_deep_research_learnings.md`
- `docs/review/almere_d6_open_questions.md`
- `docs/review/almere_d6_validation_ticket_matrix.md`

Focus only on:
- D5 tabs with missing current working view: Financiering, Governance rollen, Monitoring cyclus, D6 afhankelijkheden.
- Any row whose current working view is weak, overly broad, or not clearly source-backed.
- D6 tabs where safe wording depends on public evidence versus validation.

You may resolve:
- Evidence-strength grading.
- Source-intake candidate identification.
- Safer pre-contact wording suggestions.

You must not resolve:
- Formal D5/D6 decisions.
- Local ownership or mandate.
- Funding allocation.
- Stakeholder validation status.

Guardrails:
- This is pre-contact validation-readiness work, not stakeholder validation.
- Do not contact policymakers, municipal officers, providers, insurers, GGD/JGZ, finance/controller roles or partners.
- Do not settle D5 or D6 ownership, mandate, funding, formal classification or safe final wording.
- Do not treat Excel workbook text, generated JSON, dashboard text or deep-research reports as public source evidence.
- If a public source is found, mark it as a source-intake candidate; it must be ingested and checked through the repository pipeline before use.
- Return concise findings that reduce human workload before packet export.

Deliver a concise table with these fields:
- `workbook`
- `sheet`
- `vraag_id_or_component`
- `current_working_view`
- `evidence_strength`
- `missing_source`
- `source_candidate`
- `human_validation_still_needed`
- `safe_dutch_wording`
- `packet_change_recommendation`

Also include:
- clear conclusions;
- evidence used;
- important uncertainties or conflicts;
- practical implications for packet export.
```

## D5 source-update watchlist agent

Agent ID: `p3_d5_source_update_watchlist`

```text
You are supporting the AZWA/IZA/GALA Almere repository during Sprint 33.P3: targeted pre-contact validation-readiness.

Task: D5 source-update watchlist agent

Purpose:
Create a narrow watchlist for time-dependent D5 sources expected before workagenda drafting.

Start from these repository inputs:
- `RESEARCH_AGENT_MAP.md`
- `docs/data-quality-roadmap.md`
- `docs/review/validation-instrument-register.md`
- `docs/review/validation-workbook-traceability-audit.md`
- `docs/review/validation-workbook-prefill-audit.md`
- `data/workagenda/validation_workbook_traceability_map.json`
- `data/workagenda/validation_workbook_prefill_audit.json`
- `docs/review/D5_validatieformat_werkagenda_Almere_v0.2.xlsx`
- `docs/review/Almere_D6_validatieformats.xlsx`
- `config/monthly_source_audit.json`
- `data/extracted/monthly_source_audit.json`
- `docs/internal/monthly-source-audit-2026-04-30.md`
- `data/site/timeline_register.json`

Focus only on:
- D5 handreikingen expected end May.
- Handreiking Regionale Preventie Infrastructuur.
- Regioscan and rode-dradenanalyse.
- Ontwikkelagenda process for beproevende regio's.
- Finance updates for AZWA/D5, doorbraakmiddelen, Zvw and social-domain funding.

You may resolve:
- Expected-source watchlist entries.
- Workbook tabs affected by each expected source.
- Action after source appears.

You must not resolve:
- Using expected sources as if they already exist.
- Filling local workagenda answers from watchlist entries.

Guardrails:
- This is pre-contact validation-readiness work, not stakeholder validation.
- Do not contact policymakers, municipal officers, providers, insurers, GGD/JGZ, finance/controller roles or partners.
- Do not settle D5 or D6 ownership, mandate, funding, formal classification or safe final wording.
- Do not treat Excel workbook text, generated JSON, dashboard text or deep-research reports as public source evidence.
- If a public source is found, mark it as a source-intake candidate; it must be ingested and checked through the repository pipeline before use.
- Return concise findings that reduce human workload before packet export.

Deliver a concise table with these fields:
- `source`
- `expected_timing`
- `relevance`
- `workbook_tabs_affected`
- `trigger_for_action`
- `action_after_source_appears`
- `current_status`

Also include:
- clear conclusions;
- evidence used;
- important uncertainties or conflicts;
- practical implications for packet export.
```

## D5-D6 dependency mapping agent

Agent ID: `p3_d5_d6_dependency_mapping`

```text
You are supporting the AZWA/IZA/GALA Almere repository during Sprint 33.P3: targeted pre-contact validation-readiness.

Task: D5-D6 dependency mapping agent

Purpose:
Map D5 workagenda components to likely D6 prerequisites so D5 packets do not promise implementation without social-base infrastructure.

Start from these repository inputs:
- `RESEARCH_AGENT_MAP.md`
- `docs/data-quality-roadmap.md`
- `docs/review/validation-instrument-register.md`
- `docs/review/validation-workbook-traceability-audit.md`
- `docs/review/validation-workbook-prefill-audit.md`
- `data/workagenda/validation_workbook_traceability_map.json`
- `data/workagenda/validation_workbook_prefill_audit.json`
- `docs/review/D5_validatieformat_werkagenda_Almere_v0.2.xlsx`
- `docs/review/Almere_D6_validatieformats.xlsx`
- `data/workagenda/d5_status_matrix.json`
- `data/workagenda/d5_validation_tickets.json`
- `data/extracted/municipal/almere_d6_responsibility_register.json`
- `docs/review/almere_d6_validation_ticket_matrix.md`
- `docs/review/almere_d6_open_questions.md`

Focus only on:
- D5 rows where D6 dependency is possible or unknown.
- Dependencies around inloopvoorzieningen, wijkteams, JGZ/GGD, Samen Sterker, monitoring, digital infrastructure and informal support.
- Questions that should be asked together in stakeholder packets.

You may resolve:
- Likely dependency mapping.
- Dependency validation question wording.
- Risk labels for D5 items blocked by unresolved D6 infrastructure.

You must not resolve:
- Whether a D6 component is formally settled.
- Which organization owns or funds the D6 component.

Guardrails:
- This is pre-contact validation-readiness work, not stakeholder validation.
- Do not contact policymakers, municipal officers, providers, insurers, GGD/JGZ, finance/controller roles or partners.
- Do not settle D5 or D6 ownership, mandate, funding, formal classification or safe final wording.
- Do not treat Excel workbook text, generated JSON, dashboard text or deep-research reports as public source evidence.
- If a public source is found, mark it as a source-intake candidate; it must be ingested and checked through the repository pipeline before use.
- Return concise findings that reduce human workload before packet export.

Deliver a concise table with these fields:
- `d5_component`
- `likely_d6_dependency`
- `dependency_status`
- `affected_vraag_ids`
- `validation_question`
- `risk_if_unresolved`
- `recommended_packet`

Also include:
- clear conclusions;
- evidence used;
- important uncertainties or conflicts;
- practical implications for packet export.
```

## Policymaker readability agent

Agent ID: `p3_policymaker_readability`

```text
You are supporting the AZWA/IZA/GALA Almere repository during Sprint 33.P3: targeted pre-contact validation-readiness.

Task: Policymaker readability agent

Purpose:
Make stakeholder-facing packet language plain Dutch and easy to answer.

Start from these repository inputs:
- `RESEARCH_AGENT_MAP.md`
- `docs/data-quality-roadmap.md`
- `docs/review/validation-instrument-register.md`
- `docs/review/validation-workbook-traceability-audit.md`
- `docs/review/validation-workbook-prefill-audit.md`
- `data/workagenda/validation_workbook_traceability_map.json`
- `data/workagenda/validation_workbook_prefill_audit.json`
- `docs/review/D5_validatieformat_werkagenda_Almere_v0.2.xlsx`
- `docs/review/Almere_D6_validatieformats.xlsx`

Focus only on:
- Language flags in validation_workbook_prefill_audit.json.
- D6 terms such as evidence and social-base.
- Broad prompts in Gezonde School and Samen Sterker.
- Any internal terms: repository, register, prefill, inferred, source intake, top layer, pipeline, JSON, claim layer.

You may resolve:
- Replacement wording.
- Question simplification.
- Packet instructions.

You must not resolve:
- Substantive policy answer choices beyond making the existing choices readable.
- Final workagenda wording approval.

Guardrails:
- This is pre-contact validation-readiness work, not stakeholder validation.
- Do not contact policymakers, municipal officers, providers, insurers, GGD/JGZ, finance/controller roles or partners.
- Do not settle D5 or D6 ownership, mandate, funding, formal classification or safe final wording.
- Do not treat Excel workbook text, generated JSON, dashboard text or deep-research reports as public source evidence.
- If a public source is found, mark it as a source-intake candidate; it must be ingested and checked through the repository pipeline before use.
- Return concise findings that reduce human workload before packet export.

Deliver a concise table with these fields:
- `workbook`
- `sheet`
- `vraag_id_or_location`
- `issue_type`
- `current_text`
- `recommended_replacement`
- `priority`
- `reason`

Also include:
- clear conclusions;
- evidence used;
- important uncertainties or conflicts;
- practical implications for packet export.
```

## Finance-risk precheck agent

Agent ID: `p3_finance_risk_precheck`

```text
You are supporting the AZWA/IZA/GALA Almere repository during Sprint 33.P3: targeted pre-contact validation-readiness.

Task: Finance-risk precheck agent

Purpose:
Identify where finance/controller validation is unavoidable before packet export.

Start from these repository inputs:
- `RESEARCH_AGENT_MAP.md`
- `docs/data-quality-roadmap.md`
- `docs/review/validation-instrument-register.md`
- `docs/review/validation-workbook-traceability-audit.md`
- `docs/review/validation-workbook-prefill-audit.md`
- `data/workagenda/validation_workbook_traceability_map.json`
- `data/workagenda/validation_workbook_prefill_audit.json`
- `docs/review/D5_validatieformat_werkagenda_Almere_v0.2.xlsx`
- `docs/review/Almere_D6_validatieformats.xlsx`
- `data/workagenda/d5_status_matrix.json`
- `docs/review/almere_d6_validation_ticket_matrix.md`
- `docs/review/validation-workbook-prefill-audit.md`

Focus only on:
- D5 finance workbook tab.
- D6 financing and budget-demarcation tab.
- Rows with mixed funding, unknown funding, project continuity or double-counting risk.
- Separation of AZWA-D5, AZWA-D6, SPUK/GALA, PGA/IZA, regular municipal funding, GGD contribution/plustaak and Zvw/insurer funding.

You may resolve:
- Finance questions to ask controllers.
- Double-counting risk preclassification.
- Urgency for finance packet routing.

You must not resolve:
- Actual funding allocation.
- Controller confirmation.
- Insurer/Zvw commitment.

Guardrails:
- This is pre-contact validation-readiness work, not stakeholder validation.
- Do not contact policymakers, municipal officers, providers, insurers, GGD/JGZ, finance/controller roles or partners.
- Do not settle D5 or D6 ownership, mandate, funding, formal classification or safe final wording.
- Do not treat Excel workbook text, generated JSON, dashboard text or deep-research reports as public source evidence.
- If a public source is found, mark it as a source-intake candidate; it must be ingested and checked through the repository pipeline before use.
- Return concise findings that reduce human workload before packet export.

Deliver a concise table with these fields:
- `component`
- `possible_funding_lines`
- `double_counting_risk`
- `controller_question`
- `zvw_or_insurer_question`
- `urgency`
- `evidence_needed`

Also include:
- clear conclusions;
- evidence used;
- important uncertainties or conflicts;
- practical implications for packet export.
```

## Next Step

Use results in Sprint 33.P4 to build filtered stakeholder packets; do not contact policymakers before the P7 send-readiness gate.
