# Deep Research Intake

## Summary
Current sprint: Sprint 31.5 - Deep-research source intake and top-layer verification.

Use this folder for external deep-research reports only. A deep-research report is an intake signal, not a source in the corpus and not evidence for public or bestuurlijke conclusions.

## Standard Workflow

1. Extract the suggested public sources from the deep-research report.
2. Decide which suggested sources are source-worthy and which are only context, duplicates, dead links or deferred candidates.
3. Add selected public sources to the formal source corpus through `data/raw/manifest.json` and saved raw files.
4. Run the pipeline from the manifest/inventory layer onward.
5. Test whether the relevant deep-research findings now appear in the top data layers, such as document inventory, claim outputs, D6 responsibility register, review packs, site view models or dashboard data.
6. Keep formal D6 classification, ownership, mandate, funding and `settled` status out of the repository unless traceable validation evidence exists.

## Evidence Rule

Do not cite files in `docs/dr/` as evidence. Cite the ingested public source, generated top layer or validation record that supports the finding.
