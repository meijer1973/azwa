# Sprint 31.2 - Maandelijkse bronaudit

## Summary
Sprint 31.2 is completed. The current sprint is Sprint 31.3 - Reviewronde met menselijke beoordelaars. Sprint 25.6 remains parked until stakeholder validation records, local/internal documents, finance/controller confirmation, or an explicit policy decision exist.

## What Changed
- Added `config/monthly_source_audit.json` as the monthly watchlist for expected public sources.
- Added `src/build_monthly_source_audit.py` to build the monthly audit from the watchlist, raw manifest and source-intake candidates.
- Added `data/extracted/monthly_source_audit.json` as the machine-readable audit output.
- Added `docs/internal/monthly-source-audit-2026-04-30.md` as the human-readable internal audit note.
- Added `tests/test_monthly_source_audit.py`.

## Audit Result
The 30 April 2026 audit keeps six expected source groups on watch:

- 2026 gemeentefonds circulaires: mei, september and december.
- AZWA handreikingen basisfunctionaliteiten.
- Nieuwe AZWA-SPUK voor gemeenten 2027-2029.
- Geintegreerde IZA/AZWA-monitor 2026.

All six watchlist rows are `not_due_yet` for 30 April 2026. The audit also preserves one pending replacement source, `nat_vng_iza_azwa_wegwijzer_2026`, and three pending timeline items that still require source intake before they can become evidence-backed timeline facts.

## Source Boundary
Watchlist items, expected publications and pending intake candidates are not public evidence. They may only become claims, timeline facts or public-facing text after source intake, manifest registration and pipeline processing.

## Link Checks
The live audit found the VNG wegwijzer candidate URL still returning 404. It also records redirect behavior that needs manual review separately from dead-link issues, so redirect handling is not overread as source disappearance.

## Verification
Verification for this sprint should include:

```powershell
python src/build_monthly_source_audit.py --as-of 2026-04-30 --live
python -m pytest tests/test_monthly_source_audit.py
python -m pytest
```
