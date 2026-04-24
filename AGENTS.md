# Agent Instructions

## Repository Workflow
- Before editing a document type or workflow, check whether this file references a relevant guideline.
- If a new guideline, workflow note, style guide, or recurring approach is added anywhere in the repository, add a reference to it in this file so future sessions can discover it quickly.
- Keep project-specific guidance in the relevant folder, but use this file as the central index of guidance that agents should consult.
- This repository is intended to ground outputs in reality. It is heavily source-based: do not present statements, checks, dates, numbers, decisions, or conclusions as factual unless they are supported by the source corpus, generated model data, or an actually performed verification step.
- If something is a useful interpretation, draft proposal, or reviewer task rather than grounded fact, label it explicitly as such.

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
- `docs/rapporten/schrijfrichtlijn-plan-van-aanpak.md`: style and structure guidance for Dutch municipal `plan van aanpak` documents.
- `docs/data-quality-checklist.md`: working checklist for applying the Norm, Time, Money, Governance, Locality, and Execution perspectives during source and site improvement.
- `docs/phase24-data-quality-roadmap.md`: long-term roadmap for improving source quality, claim quality, timeline quality, and public-facing site text along the perspectives Norm, Time, Money, Governance, Locality, and Execution.
- `docs/phase24-sprint24.2-audit.md`: internal note for the Sprint 24.2 audit, including where the saved audit output lives and how to use it in later cleanup sprints.
