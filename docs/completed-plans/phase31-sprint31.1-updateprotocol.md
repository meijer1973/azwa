# Sprint 31.1 - Updateprotocol

## Summary
Sprint 31.1 is completed. The current sprint is Sprint 31.2 - Maandelijkse bronaudit. Sprint 25.6 remains parked until stakeholder validation records, local/internal documents, finance/controller confirmation, or an explicit policy decision exist.

## What Changed
- Added `docs/updateprotocol.md` as the workflow for source-intake and public update history.
- Added `src/validate_update_protocol.py` to validate `config/site_updates.json`.
- Added `docs/internal/update-protocol-check-2026-04-29.md` as the internal protocol check output.
- Added `tests/test_update_protocol.py`.

## Protocol Boundary
The protocol does not require a public update for every internal refactor. It requires an update when source intake or source correction changes public source interpretation, source pages, claims, timeline entries, review status, report-readiness or public pages.

## Old Claims
Old claims remain part of the corpus history. New claims can add, clarify, narrow or contradict older claims, but meaning changes must be described in `human_summary.what_changed` and, where relevant, in `change_highlights`.

## Verification
Verification for this sprint should include:

```powershell
python src/validate_update_protocol.py
python -m pytest tests/test_update_protocol.py
python -m pytest
```
