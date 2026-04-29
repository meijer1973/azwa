# Sprint 30.3 - Beleidsdocumenten en rapporten

## Summary
Sprint 30.3 is completed. The current sprint is Sprint 31.1 - Updateprotocol. Sprint 25.6 remains parked until stakeholder validation records, local/internal documents, finance/controller confirmation, or an explicit policy decision exist.

## What Changed
- Added `docs/rapporten/report-status.json` to distinguish current public-review report candidates from superseded drafts and internal guidance.
- Added `src/audit_report_grounding.py` to check current public-review report candidates for:
  - internal datalayer language;
  - exact FTE claims;
  - appendix lists that require real attached files;
  - final-sounding internal planning language.
- Added `docs/internal/report-grounding-audit-2026-04-29.md` as the internal report-control note.
- Added `tests/test_report_grounding.py` so the report grounding boundary is tested.
- Marked `docs/rapporten/plan-van-aanpak-v2.md` as a superseded concept that should not be used as public-facing or bestuurlijke text.

## Source Boundary
This sprint did not make new policy choices. It only clarified which report drafts are current candidates and added controls to prevent internal repository/model language or unsupported exact planning/capacity claims from entering public-facing report text.

## Current Report Candidates
- `docs/rapporten/plan-van-aanpak-v3.md`
- `docs/rapporten/bestuurlijke-planning-azwa-almere-2026.md`

## Superseded Drafts
- `docs/rapporten/plan-van-aanpak-v1.md`
- `docs/rapporten/plan-van-aanpak-v2.md`

## Verification
Verification for this sprint should include:

```powershell
python src/audit_report_grounding.py
python -m pytest tests/test_report_grounding.py
python -m pytest
```
