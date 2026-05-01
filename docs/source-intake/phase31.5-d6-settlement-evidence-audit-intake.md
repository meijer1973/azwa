# Sprint 31.5 - D6 Settlement Evidence Audit Intake

## Summary

Current sprint: Sprint 31.5 - Deep-research bronintake en top-layer verificatie.

The deep-research report in `docs/dr/Almere D6 Settlement Evidence Audit.md` is an intake signal, not a corpus source. It was used to test whether the D6 evidence base can move from public-source search to settlement. The answer is conservative: public evidence is strong enough for validation preparation, but not strong enough to settle D6 classification, ownership, mandate or funding.

The audit also relies on the companion report `docs/dr/Stronger official sources for Almere authority and adoption items.md`. That companion report is likewise not evidence, but it identified several stronger public sources worth adding.

## Selected Sources

| Document ID | Source | Intake reason |
| --- | --- | --- |
| `mun_almere_subsidieregister_2024` | Gemeente Almere Subsidieregister 2024 | Stronger municipal funding-context trace for GGD, JGZ, Wijkteams, social-base and partner lines. |
| `mun_almere_subsidieregister_2025` | Gemeente Almere Subsidieregister 2025 | Current municipal funding-context trace, including JGZ/SLT-related and partner lines where present. |
| `mun_almere_mentale_gezondheid` | Gemeente Almere Mentale gezondheid | Local prevention and youth mental-health implementation context. |
| `reg_ggd_flevoland_voortgang_gala_regio_2023` | GGD Flevoland Voortgang GALA in de regio | Regional GGD/BOSD/GALA/IZA governance context. |
| `nat_zorgakkoorden_werkagenda_handvatten_2026` | Zorgakkoorden handvatten regionale werkagenda | Canonical national process source for regional workagenda governance and timing. |

## Deferred Or Not Added

| Candidate | Reason |
| --- | --- |
| Council article for `Stand van zaken Gezondheidsbeleid (IZA en GALA)` | The report identified this as useful, but a stable public URL/download was not found during this intake. Keep as a named source candidate for later targeted search. |
| Council summary pages for Visie Gezondheidsbeleid and Maatschappelijke Agenda | The repository already has stronger underlying Documentwijzer/council-decision material for these dossiers. |
| Broad additional public search for D6 settlement | Deferred by design. The audit confirms there are no named public-search gaps for the D6 register rows. |

## Top-Layer Verification Target

After pipeline regeneration, verify:

- selected public sources appear in `data/raw/manifest.json`;
- selected public sources appear in `data/extracted/document_inventory.json`;
- generated document and claim files exist for the selected sources;
- the D6 responsibility register keeps `settled_count` at `0`;
- the D6 responsibility register still has all 12 rows requiring human review;
- review triage keeps `d6_rows_with_named_public_search_gap` at `0`;
- funding and settlement questions remain human/governance/finance validation work.

## Settlement Boundary

The public source base now supports a stronger validation pack. It does not settle:

- formal D6 classification;
- final owner/coordinator;
- formal mandate;
- continuity funding;
- component-level budget split;
- data/ICT/privacy accountability;
- accepted monitoring/reporting owner;
- safe final work-agenda wording.

These questions require stakeholder validation, local/internal documents, finance/controller confirmation or explicit policy decisions.
