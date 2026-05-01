# Review Folder Guide

## Summary
Current sprint: Sprint 31.5 - Deep-research bronintake en top-layer verificatie.

This folder contains human-review and validation materials. Use this guide first when deciding which review document is current, which one is generated, and which one is archived.

## Current D6 Validation Handoff

These files are current. They are for policy validation and may be used without reading the full repository.

| File | Use |
| --- | --- |
| `almere_d6_deep_research_learnings.md` | Clear summary of what Sprint 31.5 deep-research intake added to the public-source picture. |
| `almere_d6_open_questions.md` | Clear list of what remains unknown and what must be asked of stakeholders, finance/controller roles or internal document owners. |
| `almere_d6_validation_pack.md` | Main D6 validation pack. Start here for the complete current picture. |
| `almere_d6_public_source_boundary.md` | Explains what public sources prove, suggest, and cannot settle for each D6 row. |
| `almere_d6_safe_wording.md` | Safe and unsafe wording for later work-agenda drafting. |
| `almere_d6_decision_needed.md` | Human decision list for unresolved D6 classification, ownership, scale and funding questions. |
| `almere_d6_funding_gap_table.md` | Finance validation table; keeps known funding, unknown funding and double-counting risk separate. |
| `almere_d6_stakeholder_information_request.md` | Request pack for policy/stakeholder validation. |
| `almere_d6_stakeholder_validation_log.md` | Log template for validation sessions and written responses. |

No D6 responsibility-register row may move to `settled` from these documents alone. Settlement requires traceable stakeholder validation, a local decision, or another authoritative source that directly answers classification, ownership, mandate, scale and funding.

## Current Review And Deep-Research Routing

These files are current generated/review-routing artifacts.

| File | Use |
| --- | --- |
| `phase31.4-review-triage-deep-research-offload.md` | Human-readable routing of review items into human-only, deep-research, mixed and pipeline-cleanup buckets. |
| `phase31.4-deep-research-agent-prompts.md` | Ready-to-send deep research prompts. |
| `phase31.3-human-review-round.md` | Generated human-review pack per perspective. It is useful context, but Phase 31.4 is the more current routing layer. |

Deep research reports are not sources. Put reports in `docs/dr/`, extract their suggested public sources, ingest selected public sources through the pipeline, and then test whether the findings appear in the top data layers.

## Archive

Archived review documents live under `archive/`. They are kept for provenance and should not be treated as the active review entry point.

| File | Why archived |
| --- | --- |
| `archive/d6-handoff/almere_d6_validation_handoff_summary.md` | Superseded by the current validation pack, public-source boundary note, safe wording library, decision-needed list and funding gap table. |

## Maintenance Rule

When a new review document becomes the current entry point, update this README, `AGENTS.md`, `RESEARCH_AGENT_MAP.md`, and the internal review dashboard inputs. Archive superseded material instead of deleting it.
