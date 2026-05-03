# Roadmap Version Log

## Summary
Current roadmap version: `v2026.05.03-5`.

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
| `v2026.05.03-5` | 2026-05-03 | Closed Sprint 33.P2 and moved the active task to Sprint 33.P3 targeted pre-contact agents. | `docs/data-quality-roadmap.md` | Added `data/workagenda/validation_workbook_prefill_audit.json`, `docs/review/validation-workbook-prefill-audit.md`, and `src/build_validation_workbook_prefill_audit.py`. |
| `v2026.05.03-4` | 2026-05-03 | Closed Sprint 33.P1 at repository-map level and moved the active task to Sprint 33.P2 prefill audit/current working views. | `docs/data-quality-roadmap.md` | Added `data/workagenda/validation_workbook_traceability_map.json`, `docs/review/validation-workbook-traceability-audit.md`, and `src/build_validation_workbook_traceability.py`. |
| `v2026.05.03-3` | 2026-05-03 | Reframed the active roadmap around pre-contact validation-readiness, with Sprint 33.P0-P7 before policymaker contact and V1-V4 after send-readiness. | `docs/data-quality-roadmap.md` | Added `docs/review/validation-instrument-register.md` and brought the D5/D6 Excel workbooks under tracked baseline control. |
| `v2026.05.03-2` | 2026-05-03 | Changed the top roadmap ledger into an active task ledger and moved completed sprint history out of the top roadmap flow. | `docs/data-quality-roadmap.md` | Completed sprint history now lives in `docs/roadmap/completed-sprint-ledger.md`. |
| `v2026.05.03` | 2026-05-03 | Merged the workagenda-delivery roadmap into the canonical roadmap and introduced roadmap versioning. | `docs/data-quality-roadmap.md` | Archived prior standalone workagenda roadmap as `docs/roadmap/archive/workagenda-delivery-roadmap-v2026.05.02.md`; `docs/workagenda-delivery-roadmap.md` is now a redirect. |
