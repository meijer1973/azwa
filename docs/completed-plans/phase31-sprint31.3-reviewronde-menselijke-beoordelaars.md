# Sprint 31.3 - Reviewronde met menselijke beoordelaars

## Summary
Sprint 31.3 is completed. The current next sprint is not yet selected in this note. Sprint 25.6 remains parked until stakeholder validation records, local/internal documents, finance/controller confirmation, or an explicit policy decision exist.

## What Changed
- Added `src/build_human_review_round.py` to turn the review queue, perspective config and monthly source audit into a human-review package.
- Added `data/extracted/human_review_round.json` as the machine-readable review-round layer.
- Added `docs/review/phase31.3-human-review-round.md` as the human-readable reviewer pack.
- Added the reviewer pack to the internal review dashboard.
- Added `tests/test_human_review_round.py`.

## Review Posture
The review pack is not a policy decision layer. It helps reviewers distinguish:

- source authority and attribution questions;
- expected moments versus deadlines;
- funding and controller-validation questions;
- actor mentions versus confirmed governance roles;
- national/regional relevance versus explicit Almere adoption;
- possible execution actions versus settled implementation.

## D6 Guardrail
Sprint 31.3 does not harden the D6 responsibility register. No D6 row should become `settled` until Sprint 25.6 is unparked through stakeholder validation records, local/internal documents, finance/controller confirmation, or an explicit policy decision.

## Verification
Verification for this sprint should include:

```powershell
python src/build_human_review_round.py --as-of 2026-04-30
python src/build_internal_review_dashboard.py
python -m pytest tests/test_human_review_round.py
python -m pytest
```
