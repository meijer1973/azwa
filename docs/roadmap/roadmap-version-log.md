# Roadmap Version Log

## Summary
Current roadmap version: `v2026.05.09-6`.

The active roadmap is `docs/data-quality-roadmap.md`. This log records material roadmap changes so the project does not split into multiple competing roadmap documents.

## Versioning Rules

- Use date-based versions: `vYYYY.MM.DD`.
- If more than one roadmap change happens on the same day, append a suffix: `vYYYY.MM.DD-2`.
- Increment the version when sprint status, phase scope, gate rules, canonical file routing, or delivery sequence changes.
- Archive replaced standalone roadmap files or major prior snapshots under `docs/roadmap/archive/`.
- Keep redirect files short and explicit.

## Versions

| Version | Date | Change | Active roadmap | Archive / notes |
| --- | --- | --- | --- | --- |
| `v2026.05.09-6` | 2026-05-09 | Switched active D5 validation workbook routing from `v0.5` to versioned `v0.6`. | `docs/data-quality-roadmap.md` | Current D5 workbook is `docs/review/D5_validatieformat_werkagenda_Almere_v0.6.xlsx`; dedicated D5 `Financiering` and `Governance rollen` tabs are removed, while finance/governance questions remain in component rows where relevant. |
| `v2026.05.09-5` | 2026-05-09 | Switched active D5 validation workbook routing from `v0.4` to versioned `v0.5`. | `docs/data-quality-roadmap.md` | Current D5 workbook is `docs/review/D5_validatieformat_werkagenda_Almere_v0.5.xlsx`; `Bewijssoort` is renamed to `Brontype` and `Bewijs / verwijzing` / `Bewijs/verwijzing` to `bron`. |
| `v2026.05.09-4` | 2026-05-09 | Switched active D5 validation workbook routing from `v0.3` to repaired version `v0.4`. | `docs/data-quality-roadmap.md` | Current D5 workbook is `docs/review/D5_validatieformat_werkagenda_Almere_v0.4.xlsx`; `v0.3` is superseded because its Excel table metadata caused repair prompts. |
| `v2026.05.09-3` | 2026-05-09 | Switched active D5 validation workbook routing from `v0.2` to versioned `v0.3`. | `docs/data-quality-roadmap.md` | Current D5 workbook is `docs/review/D5_validatieformat_werkagenda_Almere_v0.3.xlsx`; `v0.2` remains preserved as prior version. |
| `v2026.05.09-2` | 2026-05-09 | Switched active D5 validation workbook routing from `v0.1` to versioned `v0.2` and preserved `v0.1` as the baseline. | `docs/data-quality-roadmap.md` | Current D5 workbook is `docs/review/D5_validatieformat_werkagenda_Almere_v0.2.xlsx`; workbook edits must create a new version instead of overwriting prior versions. |
| `v2026.05.09` | 2026-05-09 | Closed Sprint 33.P6 repository/workflow integration and marked Sprint 33.P7 blocked pending P5 human dry run. | `docs/data-quality-roadmap.md` | Added `data/workagenda/precontact_response_workflow.json`, `docs/review/precontact-response-workflow.md`, and `src/build_precontact_response_workflow.py`; no answers imported and no stakeholder contact authorized. |
| `v2026.05.03-8` | 2026-05-03 | Prepared Sprint 33.P5 internal dry-run cases and moved repository-side active work to Sprint 33.P6 workflow integration. | `docs/data-quality-roadmap.md` | Added `data/workagenda/precontact_internal_dry_run.json`, `docs/review/precontact-internal-dry-run.md`, and `src/build_precontact_internal_dry_run.py`; P5 human reviewer execution remains a P7 blocker, not a P6 blocker. |
| `v2026.05.03-7` | 2026-05-03 | Closed Sprint 33.P4 and moved the active task to Sprint 33.P5 internal dry run. | `docs/data-quality-roadmap.md` | Added `data/workagenda/precontact_stakeholder_packets.json`, `docs/review/precontact-stakeholder-packets.md`, `data/workagenda/precontact_packets/*.csv`, and `src/build_precontact_stakeholder_packets.py`; packet drafts are prepared, not sent. |
| `v2026.05.03-6` | 2026-05-03 | Closed Sprint 33.P3 and moved the active task to Sprint 33.P4 stakeholder packet building. | `docs/data-quality-roadmap.md` | Added `data/workagenda/precontact_agent_plan.json`, `docs/review/precontact-agent-prompts.md`, and `src/build_precontact_agent_plan.py`; prompts are prepared, not sent. |
| `v2026.05.03-5` | 2026-05-03 | Closed Sprint 33.P2 and moved the active task to Sprint 33.P3 targeted pre-contact agents. | `docs/data-quality-roadmap.md` | Added `data/workagenda/validation_workbook_prefill_audit.json`, `docs/review/validation-workbook-prefill-audit.md`, and `src/build_validation_workbook_prefill_audit.py`. |
| `v2026.05.03-4` | 2026-05-03 | Closed Sprint 33.P1 at repository-map level and moved the active task to Sprint 33.P2 prefill audit/current working views. | `docs/data-quality-roadmap.md` | Added `data/workagenda/validation_workbook_traceability_map.json`, `docs/review/validation-workbook-traceability-audit.md`, and `src/build_validation_workbook_traceability.py`. |
| `v2026.05.03-3` | 2026-05-03 | Reframed the active roadmap around pre-contact validation-readiness, with Sprint 33.P0-P7 before policymaker contact and V1-V4 after send-readiness. | `docs/data-quality-roadmap.md` | Added `docs/review/validation-instrument-register.md` and brought the D5/D6 Excel workbooks under tracked baseline control. |
| `v2026.05.03-2` | 2026-05-03 | Changed the top roadmap ledger into an active task ledger and moved completed sprint history out of the top roadmap flow. | `docs/data-quality-roadmap.md` | Completed sprint history now lives in `docs/roadmap/completed-sprint-ledger.md`. |
| `v2026.05.03` | 2026-05-03 | Merged the workagenda-delivery roadmap into the canonical roadmap and introduced roadmap versioning. | `docs/data-quality-roadmap.md` | Archived prior standalone workagenda roadmap as `docs/roadmap/archive/workagenda-delivery-roadmap-v2026.05.02.md`; `docs/workagenda-delivery-roadmap.md` is now a redirect. |
