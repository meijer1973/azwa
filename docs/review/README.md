# Review Folder Guide

## Summary
Current sprint: Sprint 33.P5 - Pre-contact validation-readiness: internal dry run.

This folder now has two active review uses:

- D6 human-facing validation handoff notes.
- D5/D6 pre-contact validation instrument control.

Older detailed packs, generated review snapshots, and source-boundary working papers are archived for traceability.

## Current Files

Only these files should normally be used from the top level of this folder.

| File | Use |
| --- | --- |
| `validation-instrument-register.md` | Current register for the D5 and D6 Excel validation workbooks. Use before editing, sending, or importing answers from the workbooks. |
| `validation-workbook-traceability-audit.md` | Sprint 33.P1 audit of D5/D6 workbook row traceability, generated IDs, routing, evidence gates and remaining send-readiness limits. |
| `validation-workbook-prefill-audit.md` | Sprint 33.P2 audit of current working views, assessment/correction fields, evidence fields, broad questions and stakeholder-facing language. |
| `precontact-agent-prompts.md` | Sprint 33.P3 copy-ready targeted agent prompts for pre-contact QA. Prepared only; not stakeholder contact and not broad research. |
| `precontact-stakeholder-packets.md` | Sprint 33.P4 index of filtered D5/D6 stakeholder packet drafts and CSV send-set files. Prepared only; not sent and not validation results. |
| `D5_validatieformat_werkagenda_Almere_v0.1.xlsx` | D5 pre-validation workbook baseline. This is a validation instrument, not a source or validation result. |
| `Almere_D6_validatieformats.xlsx` | D6 pre-validation workbook baseline. This is a validation instrument, not a source or validation result. |
| `almere_d6_deep_research_learnings.md` | Clear summary of what Sprint 31.5 deep-research intake added to the public-source picture. |
| `almere_d6_open_questions.md` | Clear list of what remains unknown and what must be asked of stakeholders, finance/controller roles or internal document owners. |
| `almere_d6_validation_ticket_matrix.md` | Plain-language validation design with answer choices, stakeholder packets and simple decision rules. Use this for handoff conversations instead of broad research questions. |
| `README.md` | This folder guide. |

The Excel workbooks should not be sent to policymakers until the send-readiness gate in `docs/data-quality-roadmap.md` has passed.

No D6 responsibility-register row may move to `settled` from these notes alone. Settlement requires traceable stakeholder validation, a local decision, or another authoritative source that directly answers classification, ownership, mandate, scale and funding.

## Current Human Reading Order

0. Read `validation-instrument-register.md`, `validation-workbook-traceability-audit.md`, `validation-workbook-prefill-audit.md`, `precontact-agent-prompts.md`, and `precontact-stakeholder-packets.md` if you are working with the D5 or D6 Excel validation workbooks, pre-contact agent routing, or stakeholder packet drafts.
1. Read `almere_d6_deep_research_learnings.md` to see what is now publicly source-backed.
2. Read `almere_d6_open_questions.md` to see what still needs stakeholder, finance/controller, governance or internal-document validation.
3. Use `almere_d6_validation_ticket_matrix.md` when preparing validation requests; it turns open questions into plain-language choices.
4. Use archive files only when you need provenance, detailed tables, or generated sprint snapshots.

Deep research reports are not sources. Put reports in `docs/dr/`, extract their suggested public sources, ingest selected public sources through the pipeline, and then test whether the findings appear in the top data layers.

## Archive

Archived review documents live under `archive/`. They are kept for provenance and should not be treated as the active review entry point.

| File | Why archived |
| --- | --- |
| `archive/d6-handoff/almere_d6_validation_handoff_summary.md` | Superseded by the current validation pack, public-source boundary note, safe wording library, decision-needed list and funding gap table. |
| `archive/d6-support/` | Detailed D6 handoff support files: validation pack, source-boundary note, safe wording, decision-needed list, funding table, stakeholder request and validation log. |
| `archive/phase31/` | Generated Sprint 31.3 and 31.4 review snapshots and deep-research prompts. |

## Maintenance Rule

When a new review document becomes the current entry point, update this README, `AGENTS.md`, `RESEARCH_AGENT_MAP.md`, and the internal review dashboard inputs. Archive superseded material instead of deleting it.
