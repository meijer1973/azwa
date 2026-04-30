# Sprint 31.4 - Review triage and deep-research offload

## Summary
Sprint 31.4 is completed. The current next sprint is not yet selected. Sprint 25.6 remains parked until stakeholder validation records, local/internal documents, finance/controller confirmation, or an explicit policy decision exist.

## What Changed
- Added `src/build_review_triage.py` to route review work into human-only, deep-research, mixed and pipeline-cleanup buckets.
- Added `data/extracted/review_triage_deep_research_offload.json` as the machine-readable triage layer.
- Added `docs/review/phase31.4-review-triage-deep-research-offload.md` as the human-readable triage note.
- Added `docs/review/phase31.4-deep-research-agent-prompts.md` with ready-to-send deep research prompts.
- Added the new review-triage docs to the internal dashboard.
- Added `tests/test_review_triage.py`.

## Triage Result
The current review queue has 387 items:

- 199 `deep_research_candidate` items.
- 120 `mixed_public_search_then_human` items.
- 58 `human_only` items.
- 10 `pipeline_or_extraction_cleanup` items.

This means not every review item should go directly to human policy reviewers. Public-source research can reduce part of the workload before stakeholder validation.

## Deep Research Assignments
Six assignments are prepared:

1. Gezonde School / mentale gezonde school Almere.
2. Digital and operational infrastructure for D6 Almere/Flevoland.
3. Burgerinitiatieven, informele steun and social-base access.
4. PGA / Zorgzaam Flevoland / Flever interface.
5. Samen Sterker in de Wijk source strengthening.
6. Stronger public source hunt for review-queue authority/adoption items.

## Guardrail
Deep research can add public sources, source candidates, stronger authority evidence, replacement sources or explicit local-adoption evidence. It cannot settle D6 classification, ownership, mandate, funding, safe work-agenda wording or register status.

## Verification
Verification for this sprint should include:

```powershell
python src/build_review_triage.py --as-of 2026-04-30
python src/build_internal_review_dashboard.py
python -m pytest tests/test_review_triage.py
python -m pytest
```
