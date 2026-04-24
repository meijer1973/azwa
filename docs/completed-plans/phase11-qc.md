# Phase 11 Quality Control

Phase 11 adds a dedicated quality-control and review-queue layer on top of the extraction pipeline.

## Outputs

- `data/extracted/qc_report.json`
- `data/extracted/review_queue.json`
- `src/build_quality_control.py`

## What It Checks

- document extraction presence and metadata completeness
- evidence traceability for page-based and section-based sources
- table reference integrity and table-promotion gaps
- per-document claim count integrity
- aggregated claim-stream uniqueness and relation targets
- current-interpretation consistency
- unresolved conflict surfacing in the master and Almere views
- review-heavy contextual claims and suspicious extraction noise

## Severity Model

- `blocking`: structural integrity failure that should stop trust in downstream outputs
- `warning`: important extraction gap that does not invalidate the full corpus
- `review`: human judgment needed before using the affected output as settled policy guidance

## Design Notes

- The QC stage is intentionally strict on structural integrity and intentionally tolerant on contextual municipal pages.
- Review-heavy sources are surfaced to `review_queue.json` instead of being silently discarded.
- The interpretation layer was also tightened so equal-authority, equal-date precedence ties now stay unresolved and enter review instead of being marked resolved.
