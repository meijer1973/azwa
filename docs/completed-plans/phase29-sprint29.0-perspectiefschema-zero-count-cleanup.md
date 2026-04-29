# Phase 29 Sprint 29.0 - Perspectiefschema zero-count cleanup

## Summary

Current sprint at completion: Sprint 29.0. This sprint cleaned the active perspective contract before Sprint 29.1 starts using perspective status fields more heavily in timeline text.

The audit now reports no `zero_count_statuses` for Norm, Time, Money, Governance, Locality or Execution, and no `zero_count_actor_signals` for Governance.

## Completed Work

- Removed unused active money statuses:
  - `spending_scope`
  - `double_counting_risk`
- Removed unused active locality statuses:
  - `inferred_local_relevance`
  - `municipal_context`
  - `no_locality_signal`
- Removed unused active governance actor signal:
  - `fondsbeheerder`
- Kept source-text concepts such as funding-line separation and fondsbeheerder references available in prose, source interpretation, and D6 review materials where they are source-backed, but no longer advertises them as produced claim-status enum values.
- Updated classifier logic, schema enums, perspective config, QC accepted status sets, audit expected actor signals, research-agent guidance, checklist guidance, and tests.
- Regenerated claims, audit, QC/review queue, site view models, rendered site, and internal dashboard.

## Files To Check

- `src/build_claims_top5.py`
- `config/data_quality_perspectives.json`
- `data/schemas/claim.schema.json`
- `src/build_quality_control.py`
- `src/build_data_quality_audit.py`
- `data/extracted/data_quality_audit.json`
- `RESEARCH_AGENT_MAP.md`
- `docs/data-quality-checklist.md`
- `docs/data-quality-roadmap.md`
- `tests/test_data_quality_audit.py`
- `tests/test_money_status.py`
- `tests/test_governance_status.py`
- `tests/test_locality_status.py`

## Verification

- `python src/build_claims_top5.py`
- `python src/build_data_quality_audit.py`
- `python src/build_quality_control.py`
- `python src/build_site_view_models.py`
- `python src/render_site.py`
- `python src/build_internal_review_dashboard.py`
- `python -m pytest`

## Notes For Later Sprints

- Sprint 29.1 may treat `zero_count_statuses` as an active audit guardrail rather than a known backlog item.
- Do not reintroduce a status enum until the classifier can produce it from current source-backed claim text or the sprint explicitly accepts it as a temporary planned-but-empty contract.
