# Agent Instructions

## Repository Workflow
- Before editing a document type or workflow, check whether this file references a relevant guideline.
- If a new guideline, workflow note, style guide, or recurring approach is added anywhere in the repository, add a reference to it in this file so future sessions can discover it quickly.
- Keep project-specific guidance in the relevant folder, but use this file as the central index of guidance that agents should consult.
- When reporting back on sprint or phase work, explicitly name the current sprint being worked on. Before reporting back after repository changes, commit the work and push/update the remote unless the user explicitly asks not to.
- `RESEARCH_AGENT_MAP.md` is the entry-point guide for research agents using the corpus and data layers. When repository structure, source coverage, generated data layers, synthesized reports, or major guidance changes, check whether `RESEARCH_AGENT_MAP.md` also needs an update.
- Every plan or sprint note should start with a brief current-state summary. For multi-sprint plans, prefer a Sprint Ledger at the top with `open` / `completed` status and current sprint. For a one-sprint or smaller plan, use a short Summary section at the top instead.
- This repository is intended to ground outputs in reality. It is heavily source-based: do not present statements, checks, dates, numbers, decisions, or conclusions as factual unless they are supported by the source corpus, generated model data, or an actually performed verification step.
- If something is a useful interpretation, draft proposal, or reviewer task rather than grounded fact, label it explicitly as such.
- For public-source workagenda filling, exhaust public sources first and then mark remaining gaps as local-staff validation tasks or later decision questions. Missing non-public information should not block public-source structuring work.
- Internal developer- and agent-facing material may use English for technical clarity, including pipeline notes, internal dashboards, and issue triage. Dutch policy content, public-facing site text, and bestuurlijke report text should remain Dutch. Mixed Dutch/English is acceptable in internal work where English technical framing helps and Dutch domain labels come from the corpus or roadmap.

## Rapporten
- When writing or revising files in `docs/rapporten/`, first read `docs/rapporten/schrijfrichtlijn-plan-van-aanpak.md`.
- For `plan van aanpak` documents, write from the bestuurlijke opgave, not from the dataset or repository. Avoid main-text phrases such as `de dataset laat zien`, `de repository toont`, `de claimlaag zegt`, or `de JSON maakt zichtbaar`.
- Do not invent policy, staffing, budget, governance, or implementation advice that is not grounded in the data/model/source base. If the source base does not support a concrete recommendation, frame it as a choice question or human review point.
- Do not invent planning dates, deadlines, or milestones. Use only dates grounded in sources or the generated timeline/model; otherwise mark timing as a human planning decision.
- Do not reference attachments, appendices, tables, maps, notes, or other supporting documents unless they actually exist or are explicitly marked as still to be produced.
- Technical source, data, QC, or pipeline details belong in a methodische verantwoording or appendix, not in the main narrative.
- For public-facing or bestuurlijke report text, avoid technical data/pipeline language altogether, including in accountability sections. Use plain source-grounding language instead of filenames, JSON names, claim-layer terminology, QC counts, or pipeline status.
- Internal generated data layers are not public sources. Do not cite names such as `Almere-view`, `site_almere_view.json`, `claims_master.jsonl`, or similar model artifacts in public-facing text; translate them into plain references to the available public source base or source analysis.

## Current Guidelines
- `RESEARCH_AGENT_MAP.md`: first-read map for research agents using the AZWA/IZA/GALA corpus and generated data layers; keep it aligned with repository updates.
- `docs/rapporten/schrijfrichtlijn-plan-van-aanpak.md`: style and structure guidance for Dutch municipal `plan van aanpak` documents.
- `docs/regional-roles-and-splits-almere-flevoland.md`: source-backed guide to regional roles and splits around Almere, Flevoland, mandaatgemeente, GGD-regio, zorgkantoorregio, ROAZ/subregions, Zeewolde/Noord-Veluwe, and practical task ownership.
- `data/curated/regional_roles_and_splits_almere_flevoland.json`: machine-readable role/split map for the same regional distinctions, including review-needed claims such as practical task ownership by Lelystad.
- `docs/data-quality-checklist.md`: working checklist for applying the Norm, Time, Money, Governance, Locality, and Execution perspectives during source and site improvement.
- `docs/research-agent-prompt-template.md`: reusable prompt template for external deep research agents working from `RESEARCH_AGENT_MAP.md`, with instructions to use derived layers for navigation and verify important claims against canonical sources.
- `docs/data-quality-roadmap.md`: long-term roadmap for improving source quality, claim quality, timeline quality, and public-facing site text along the perspectives Norm, Time, Money, Governance, Locality, and Execution. Keep its `Sprintstatus` table current by marking each sprint `open` or `completed` as work progresses.
- `data/extracted/workagenda_nulmeting_capacity.json`: Sprint 25.3 public-source prefill layer for D5 workagenda targets; use it to distinguish public baseline evidence, indicative calculations, local staff validation fields, and later decision questions.
- `data/extracted/d6_governance_collaboration.json`: Sprint 25.4 public-source role map for D6 governance and collaboration; use it to separate public role evidence, scale guardrails, local validation fields, and later decision questions.
- `docs/phase25-sprint25.4-d6-almere-responsibility-pack-plan.md`: active reopened Sprint 25.4 plan for strengthening D6 Almere evidence, responsibility allocation, execution logic, scale separation, financing status, and local validation/decision workflow.
- `docs/review/almere_d6_validation_pack.md`: internal D6 validation pack for stakeholder review; use it as validation material only, not as final public or bestuurlijke D6 text.
- `data/extracted/municipal/almere_d6_responsibility_register.json`: Sprint 25.4b public-source prefill register for Almere D6 components; use it to separate existing provision, owner/executor hypotheses, scale, funding status, decision status, evidence, and local validation needs.
- `data/schemas/almere_d6_responsibility_register.schema.json`: schema for the Almere D6 responsibility register; keep the register, QC checks, and research-agent map aligned with it.
- `docs/internal/review-dashboard.html`: local-only internal dashboard for quality triage; generated by `src/build_internal_review_dashboard.py` and intentionally not part of `dist/` or the public-facing GitHub Pages site. Regenerate it whenever sprint status, current plans, cleanup targets, review data, source coverage, public update history, or dashboard inputs change, so humans always see the latest plan state.
- `docs/completed-plans/phase24-sprint24.2-audit.md`: internal note for the completed Sprint 24.2 audit, including where the saved audit output lives and how to use it in later cleanup sprints.
- `docs/completed-plans/phase24-sprint24.3-review-dashboard.md`: internal note for the completed Sprint 24.3 review dashboard.
- `docs/completed-plans/phase25-sprint25.2-lokale-bronversterking.md`: internal note for the completed Sprint 25.2 public local-source strengthening sprint, including the rule that non-public gaps carry forward to validation or decision workflows rather than blocking public-source structuring.
- `docs/completed-plans/phase25-sprint25.3-nulmeting-capaciteit.md`: internal note for the completed Sprint 25.3 public nulmeting/capacity prefill sprint.
- `docs/completed-plans/phase25-sprint25.4-d6-governance-samenwerking.md`: internal note for the completed Sprint 25.4a D6 governance prefill pass; Sprint 25.4 has since been reopened in `docs/phase25-sprint25.4-d6-almere-responsibility-pack-plan.md`.
