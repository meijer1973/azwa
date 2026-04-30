# Phase 31.5 Healthy School Deep-Research Intake

## Summary
Current sprint: Sprint 31.5 - Deep-research source intake and top-layer verification.

This note records how the deep-research report `docs/dr/Healthy school.md` was processed. The report itself is not a source. It is used only to identify candidate public sources and to test whether the repository's top data layers now reflect the source-backed findings.

## Intake Decision

Selected public sources to ingest:

| Document id | Source | Publisher | Repository action | Why selected |
| --- | --- | --- | --- | --- |
| `mun_almere_gezonde_scholen` | Gezonde scholen | Gemeente Almere | Ingested | Direct Almere implementation evidence for healthy-school support and the GGD Gezonde School adviser. |
| `mun_almere_gezond_in_almere` | Gezond in Almere | Gemeente Almere | Ingested | Local prevention context linking Gezonde School and mentale gezondheid. |
| `reg_ggd_flevoland_gezonde_school` | De Gezonde School | GGD Flevoland | Ingested | GGD implementation evidence for Gezonde School advisers, school wellbeing and support to schools. |
| `reg_ggd_flevoland_ketenaanpak_gezond_gewicht_almere` | Ketenaanpak gezond gewicht - Gezond Gewicht Almere | GGD Flevoland | Ingested | Stable public anchor for Gezond Gewicht Almere, collective prevention, JGZ route and Pact met impact reference. |
| `mun_almere_lea_2024_2028` | LEA 2024-2028 | Sociaal Domein Almere / Gemeente Almere | Ingested | School-wellbeing, LEA partner and budget-context evidence. |

Deferred or existing sources:

| Candidate | Decision | Reason |
| --- | --- | --- |
| `Pact met impact 2023-2026` PDF | Deferred | Public search shows the document, but the candidate GGD PDF URLs return 404 from the local pipeline environment. The stable GGD Ketenaanpak page is ingested as the public anchor until a downloadable PDF URL is available. |
| GGD Flevoland JGZ profile | Already ingested | Already present as `reg_ggd_flevoland_jgz_almere_profile`. |
| GGD Flevoland Begroting 2026 | Already ingested | Already present as `reg_ggd_flevoland_begroting_2026`. |
| Gezonde School case studies and newsletters | Deferred | Useful implementation context, but lower priority than municipal and GGD source anchors. Consider only if a future review question needs school-level examples. |

## Top-Layer Verification Target

After pipeline regeneration, verify that:

- the five selected sources exist in `data/raw/manifest.json`;
- they appear in `data/extracted/document_inventory.json`;
- extracted document and claim files exist for each selected source;
- the `gezonde_school_mentale_gezonde_school` row in `data/extracted/municipal/almere_d6_responsibility_register.json` has source-backed prefill evidence instead of `existing_almere_provision: null`;
- the row remains non-`settled` and keeps formal D6 classification, owner, mandate, scale and funding as validation questions;
- the review pack and public-source boundary note no longer describe this row as a broad unresolved public-source gap.

## Guardrail

This intake may reduce the public-source gap for Gezonde School. It must not settle formal D6 status, final owner, final mandate or funding allocation.
