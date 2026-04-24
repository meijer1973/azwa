# Research agent map — AZWA / IZA / GALA corpus (Almere focus)

This repository curates and structures policy documents on the Dutch **Aanvullend Zorg- en Welzijnsakkoord (AZWA)**, its predecessors the **Integraal Zorgakkoord (IZA)** and **Gezond en Actief Leven Akkoord (GALA)**, the **CW 3.1 frameworks** for D5/D6 building blocks, and the **Almere / Flevoland** implementation context. It exposes both the raw corpus and a layered set of derived data products.

**Repository location:** https://github.com/meijer1973/azwa

If you are a research agent working on a deep-research task over this corpus, read this file first. It tells you what exists, where to look, and how the pieces relate.

---

## Quick orientation

- **Domain:** Dutch zorg-en-welzijn (health & social-care) policy — national, regional (Flevoland), municipal (Almere).
- **Language:** All source documents and extractions are in **Dutch**. Queries, keywords, and claim text are Dutch; write search terms accordingly (e.g. *"basisinfrastructuur"*, *"middelen"*, *"uitvoeringscapaciteit"*, *"transformatiemiddelen"*, *"regioplan"*).
- **Time span:** IZA (2022) → GALA (2023) → AZWA onderhandelaarsakkoord (2025) → AZWA definitief + CW 3.1-kaders (2025–2026) → Almere PGA / begroting (2024–2026).
- **Corpus size:** 18 numbered sources; 33 per-document structured extractions; one master claims register.
- **What this is not:** not a public website. The repo also *builds* a static site (`dist/`), but that output is generated and not authoritative — always read from sources and data layers, not from `dist/`.
- **Regional caution:** do not treat "Flevoland", "de regio", "mandaatgemeente", GGD-regio, zorgkantoorregio, ROAZ and practical execution as interchangeable. Read `docs/regional-roles-and-splits-almere-flevoland.md` before drawing regional conclusions.

---

## Key acronyms

| Term | Meaning |
|------|---------|
| AZWA | Aanvullend Zorg- en Welzijnsakkoord (2025) — the agreement this repo centers on |
| IZA | Integraal Zorgakkoord (2022) — predecessor framework for healthcare agreements |
| GALA | Gezond en Actief Leven Akkoord (2023) — prevention/healthy-living agreement |
| D5 | AZWA building block 5 — basisfunctionaliteiten (functional services) |
| D6 | AZWA building block 6 — basisinfrastructuur (digital/organizational infrastructure) |
| CW 3.1 | Comptabiliteitswet art. 3.1 — framework for assessing policy instruments (used for D5/D6) |
| PGA | Positief Gezond Almere — Almere's local transformation programme |
| SPUK | Specifieke Uitkering — earmarked grant mechanism (transformatiemiddelen) |
| VNG | Vereniging van Nederlandse Gemeenten — national municipal association (publisher of ledenbrieven, FAQs) |
| VWS | Ministerie van Volksgezondheid, Welzijn en Sport |
| BZK | Ministerie van Binnenlandse Zaken en Koninkrijksrelaties (gemeentefonds) |
| DUS-I | Dienst Uitvoering Subsidies aan Instellingen (executes SPUK regelingen) |

---

## Repository structure

The repo has two kinds of content:

1. **Source corpus** — primary policy documents (PDFs) and their markdown extractions. Numbered `01`..`18`.
2. **Data layers** — pipeline outputs derived from the corpus, in progressive stages: `raw → intermediate → extracted → site`.

All paths below are relative to the repo root (`C:\Projects\azwa\` locally, or the root of https://github.com/meijer1973/azwa on GitHub).

Build plumbing (source code, tests, rendered site output, pipeline config, phase docs) is intentionally omitted from this map — agents doing research on the AZWA/IZA/GALA/Almere case should look here first.

### Entry points

```
RESEARCH_AGENT_MAP.md                 First-read map for research agents
README.md                           Project overview
AGENTS.md                           Guidance for agents working in this repo
source-curation.md                  Which source files are canonical vs context; preferred replacements
source-curation.json                Same curation as structured data
sources/manifest.json               Mapping of source index (01..18) → source_url + saved file names
```

Start with `source-curation.md` + `sources/manifest.json`. Together they tell you which 18 sources exist, where they came from, and which markdown extraction to prefer.

### Source corpus (primary documents)

Six parallel directories hold the same 18 sources in different forms. Note the **space** in folder names.

```
sources/                            Original downloads: .html landing pages + .pdf primary docs (01..18)
sources canonical/                  Subset recommended as canonical raw archive (PDFs only for doc-backed sources)
sources context/                    Supporting/context sources only (06 ledenbrief, 13–16 municipal gateways)
sources markdown/                   Markdown extraction of every source (full set, including duplicates)
sources markdown canonical/         Markdown of the canonical subset — PREFERRED TEXT BASIS for JSON extractions
sources markdown context/           Markdown of context-only sources
```

**Recommendation (from `source-curation.md`):** for textual evidence, read `sources markdown canonical/`. Treat `sources markdown context/` as supporting material. Use `sources canonical/` PDFs only when page/line fidelity matters.

#### The 18 sources (stable index → topic)

| # | Topic | Origin |
|---|-------|--------|
| 01 | Aanvullend Zorg- en Welzijnsakkoord (AZWA) — definitief | rijksoverheid.nl |
| 02 | Kamerbrief aanbieding AZWA | rijksoverheid.nl |
| 03 | Kamerbrief CW 3.1-kaders voor AZWA-onderdelen | rijksoverheid.nl |
| 04 | CW 3.1-kader basisfunctionaliteiten & basisinfrastructuur (D5/D6) | rijksoverheid.nl |
| 05 | Kamerbrief voortgang IZA en AZWA | rijksoverheid.nl |
| 06 | Onderhandelaarsakkoord AZWA (+ VNG ledenbrief, context) | vng.nl / rijksoverheid.nl |
| 07 | VNG FAQ — middelen AZWA | vng.nl |
| 08 | VNG FAQ — uitvoeringscapaciteit AZWA | vng.nl |
| 09 | Integraal Zorgakkoord (IZA) 2022 | rijksoverheid.nl |
| 10 | Gezond en Actief Leven Akkoord (GALA) 2023 | rijksoverheid.nl |
| 11 | Regiobeeld Flevoland 2023 | regional |
| 12 | Regioplan IZA Flevoland — ZorgzaamFlevoland 2023 | regional |
| 13 | Informatiepagina sociaal domein (Almere, context) | almere.nl |
| 14 | Sociale Staat van Almere — gateway page (context) | almere.nl |
| 15 | Maatschappelijke Agenda 2024–2034 — council summary (context) | almere.nl |
| 16 | Visie Gezondheidsbeleid Almere 2024–2026 — council summary (context) | almere.nl |
| 17 | Transformatieplan Positief Gezond Almere (PGA) | positiefgezondalmere.nl |
| 18 | Beleidstheorie & businesscase PGA — SEO / Wouter Vermeulen 2021 | SEO report |

Filename pattern in each `sources*/` folder: `<NN>-<slug>__<doc-id>.<ext>` (long form) or `<NN>-<slug>.<ext>` (short form, drops the doc-id). The long form is the actual document; the short form is typically the HTML landing page or a redundant export. See `sources/manifest.json` for the authoritative list of saved files per source.

### Data layer: raw intake

```
data/raw/
├── manifest.json                       Intake manifest
├── source_intake_candidates.json       Queue of candidate sources under evaluation
├── municipal/                          Municipal (Almere) raw captures
├── national/                           National (Rijk / VNG / ministries) raw captures
└── regional/                           Regional (Flevoland) raw captures
```

Use when you need to trace a source back to its intake record.

### Data layer: intermediate extractions

```
data/intermediate/
├── source_markdown/                    Per-source markdown normalized for pipeline use
├── text/                               Flat-text extractions
├── chunks/                             Chunked text for retrieval (per source)
└── tables/                             Extracted tables (per source)
```

Not the primary search surface — prefer `sources markdown canonical/` for human-readable text. Chunks/tables are useful when you need structure rather than prose.

### Data layer: structured extractions (main research surface)

```
data/extracted/
├── documents/                          Per-document structured JSON (one file per source)
├── claims/                             Per-document claim extractions + master registers
├── municipal/                          Almere-specific composed views
├── document_inventory.json             Index of all extracted documents (start here)
├── data_quality_audit.json             Sprint 24.2 data-quality audit results
├── qc_report.json                      Quality-control report across all extractions
└── review_queue.json                   Items flagged for human review
```

#### Naming convention (documents/, claims/)

Every file under `data/extracted/documents/` and `data/extracted/claims/` is named `<scope>_<slug>.json` where `<scope>` is:

- `nat_` — national policy (AZWA, IZA, GALA, CW 3.1, VNG / VWS / BZK documents)
- `reg_` — regional (Flevoland regiobeeld, regioplan IZA)
- `mun_` — municipal (Almere: visie gezondheidsbeleid, maatschappelijke agenda, PGA, begroting, raadskalender, etc.)

The **same slug** appears in both `documents/` (document-level extraction: metadata, sections, key statements) and `claims/` (atomic claims with provenance). So `documents/nat_iza_2022_integraal_zorgakkoord.json` pairs with `claims/nat_iza_2022_integraal_zorgakkoord.json`.

#### Key aggregated files in `data/extracted/claims/`

```
claims/claims_master.jsonl                     All claims from all sources, one per line
claims/conflict_register.json                  Claims that conflict across sources
claims/current_interpretation.json             Resolved "current best interpretation"
claims/d5_d6_master.json                       D5/D6-specific consolidated claims
```

### Data layer: site view models (pre-composed topical views)

```
data/site/
├── site_manifest.json                  Site structure manifest
├── dashboard_view.json                 Dashboard composition
├── site_home_view.json                 Home page composition
├── site_almere_view.json               Almere-specific composed view
├── site_themes_view.json               Themes index
├── site_sources_view.json              Sources index
├── site_timeline_view.json             Timeline index
├── site_reference_view.json            Reference/glossary index
├── site_updates_view.json              Recent-updates feed
├── timeline_register.json              Timeline events register
├── theme_view_models/                  One JSON per theme (D5, D6, financiering, governance, mentale gezondheid, monitoring)
├── source_view_models/                 One JSON per source (pre-composed)
├── decision_view_models/               Open decision questions
├── action_view_models/                 Candidate follow-up actions
└── reference_topic_view_models/        Glossary/reference topics
```

These are the most agent-friendly reads when you want topical synthesis (one theme, one source, one decision) without joining across `documents/` + `claims/` yourself.

---

### Curated interpretation aids

```
data/curated/
└── regional_roles_and_splits_almere_flevoland.json  Machine-readable map of regional roles and splits

docs/regional-roles-and-splits-almere-flevoland.md   Human-readable guide to the same regional distinctions
```

Use these before summarizing Almere's position in Flevoland. They distinguish the IZA/AZWA-regio Flevoland, GGD-regio Flevoland, zorgkantoorregio 't Gooi, ROAZ/subregional structures, Zeewolde's Noord-Veluwe route, formal mandaatgemeente roles, and practical task ownership that still needs source-specific checking.

---

## Schema & taxonomy (how to interpret the data)

```
data/schemas/claim.schema.json          JSON schema for individual claims (fields, provenance, authority)
config/site_taxonomy.json               Theme hierarchy used by site/theme_view_models
config/data_quality_perspectives.json   DQ perspective taxonomy used by data_quality_audit.json
config/authority_rules.json             How source authority is ranked (used by claim resolution)
config/claim_resolution_rules.json      Rules for resolving conflicting claims
config/timeline_curation.json           Which events make the timeline
```

Read these when a field's meaning is ambiguous.

---

## Synthesized reports

```
docs/rapporten/
├── plan-van-aanpak-v1.md / v2.md / v3.md            Iterated plan-of-approach narratives (v3 is newest)
├── plan-van-aanpak-v1..v3.docx                      Word versions (same content)
├── bestuurlijke-planning-azwa-almere-2026.md        Governance timeline for Almere
└── schrijfrichtlijn-plan-van-aanpak.md              Writing guidelines for the above

docs/data-quality-checklist.md                       Checklist applied in data_quality_audit.json
docs/human-review-guidance.md                        Guidance for human review of extractions
```

The `plan-van-aanpak-v*.md` files are the current synthesized narrative outputs. Prefer the highest version number for the latest thinking.

---

## Search guidance

- **Full-text search over source prose:** `sources markdown canonical/` (+ `sources markdown context/` if context is needed). Search with Dutch terms.
- **Structured search for specific claims or provisions:** `data/extracted/claims/claims_master.jsonl`, then follow `source_id` back to the per-document file.
- **"What does source X say about topic Y?"** `data/extracted/documents/<scope>_<slug>.json` or `data/site/source_view_models/<slug>.json`.
- **"What is the position across sources on theme Z?"** `data/site/theme_view_models/<theme>.json`.
- **"Where do sources disagree?"** `data/extracted/claims/conflict_register.json`.
- **"What's the current best interpretation?"** `data/extracted/claims/current_interpretation.json`.
- **Almere-specific questions:** `data/extracted/municipal/almere_current_view.json` + `mun_*` files under `documents/` and `claims/`.
- **Chronology / what-changed-when:** `data/site/timeline_register.json` and `data/site/site_timeline_view.json`.
- **Regional role/split questions:** `docs/regional-roles-and-splits-almere-flevoland.md` and `data/curated/regional_roles_and_splits_almere_flevoland.json`.

## Authority hints when sources disagree

When multiple sources speak to the same point, prefer them roughly in this order (and consult `config/authority_rules.json` for the precise rules the pipeline used):

1. **Primary agreement text** — the signed akkoord itself (AZWA definitief #01, IZA #09, GALA #10).
2. **Kamerbrieven / CW 3.1 documents** (#02–#05) — official government framing and financial frameworks.
3. **Onderhandelaarsakkoord** (#06) — what was negotiated before formal adoption; use for intent, not for final terms.
4. **VNG ledenbrieven & FAQ** (#07, #08, #06 context) — municipal-association interpretation; authoritative for implementation-capacity questions but secondary on policy scope.
5. **Regional plans** (#11 Regiobeeld, #12 Regioplan) — authoritative for Flevoland facts.
6. **Municipal PGA / SEO** (#17, #18) — authoritative for Almere's transformation strategy.
7. **Municipal gateway/summary pages** (#13–#16) — orientation only, not evidence; look for the underlying policy document referenced there.

If you find a conflict, `data/extracted/claims/conflict_register.json` likely already records it — check there before concluding the corpus is silent or contradictory.

## Maintenance note

Keep this file aligned with the repository. When sources, data-layer paths, generated outputs, synthesized reports, or agent guidance change, check whether `RESEARCH_AGENT_MAP.md` should be updated in the same work.
