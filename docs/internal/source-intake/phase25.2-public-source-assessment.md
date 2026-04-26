# Sprint 25.2 Public Source Probe

Summary: first public-source probe completed on 2026-04-24; first formal intake completed on 2026-04-26. Selected Documentwijzer council attachments, GGD Flevoland table books, the GGD Valpreventie Almere page, and the ZonMw Zorgzaam Flevoland page are now in `data/raw/manifest.json` and have been processed through inventory, extraction, claims, site view models, and the internal dashboard. Sprint 25.2 is a public-source intake sprint: material that cannot be obtained or responsibly used from public sources is carried forward to local-staff validation or later decision workflows, not treated as a blocker for filling the public workagenda structure.

## Public-only rule

Use only public sources. Do not add private correspondence, non-public personal data, or resident-level health data. If a public page contains named contacts, phone numbers, email addresses, or speaker lists, the formal extraction should suppress those details and retain only organization, role, geography, policy, and aggregate-statistical facts.

## Intake Read

| Source group | Download result | Usefulness | Recommendation |
| --- | --- | --- | --- |
| Documentwijzer 24118 Visie Gezondheidsbeleid | Public Notubiz attachments downloaded; selected documents converted to page-markdown and ingested | High | Ingested selected primary documents: `VISIE 2024-2026`, geamendeerd raadsvoorstel, besluitenlijst, and Brede SPUK/GALA plan van aanpak. Defer gesprekswijzers, duplicate process files, and ASD advice unless needed for review. Review generated claims before public policy use. |
| Documentwijzer 24161 Maatschappelijke agenda | Public Notubiz attachments downloaded; selected documents converted to page-markdown and ingested | High | Ingested selected primary documents: `MAATSCHAPPELIJKE AGENDA`, geamendeerd raadsvoorstel, besluitenlijst, and `Opzet procesevaluatie en monitor Sociaal Domein`. Defer gesprekswijzers and advice/reaction material unless needed for review. Review generated claims before public policy use. |
| Raadsbrief `Stand van zaken Gezondheidsbeleid (IZA en GALA)` | Not found in this public probe | Unknown | Do not ingest or cite. Carry forward to local-staff validation if public search remains exhausted; do not block the public-source workagenda structure. |
| GGD Flevoland 2024 table books | Public municipality-level adult and older-person PDFs downloaded, converted to page-markdown, and ingested | High | Ingested the two municipality-level table books for Sprint 25.3 nulmeting/capacity work. They contain aggregate Almere indicators for overgewicht, valrisico, eenzaamheid, mentale gezondheid, bewegen, and vulnerability. Review generated claims before public policy use. |
| GGD Flevoland Valpreventie Almere | Public general and Almere-specific pages downloaded; Almere page ingested | High | Ingested the Almere-specific page as operational execution evidence for valpreventie. Review generated claims before public policy use. |
| ZonMw Doorontwikkeling Zorgzaam Flevoland | Public project page downloaded and ingested | Medium-high | Ingested as supporting governance source only. It is a project registration, not an adopted local policy document. |
| Mentale gezondheidsnetwerken listing | Public listing downloaded | High for role/scope only | Not ingested into the formal corpus because it needs a sanitized role/geography extract. Carry forward to role validation; do not block Sprint 25.2 closure. |
| Almere Programmarekening 2024 | Public PDF downloaded | Medium | Defer unless needed for money/governance; too broad for the first 25.2 intake batch. |
| CBS 2025 population-growth news | Public page downloaded | Low-medium | Defer. Use a stable CBS/BRP table for Sprint 25.3 denominator calculations instead of a news page. |

## First Intake Batch

Completed first formal corpus batch:

- `Visie Gezondheidsbeleid Almere 2024-2026`.
- `Raadsvoorstel Visie Gezondheidsbeleid Almere 2024-2026 - geamendeerd`.
- `Besluitenlijst Visie Gezondheidsbeleid Almere 2024-2026`.
- `Integraal plan van aanpak 2024-2026` for Brede SPUK/GALA.
- `Maatschappelijke agenda 2024-2034`.
- `Raadsvoorstel Maatschappelijke agenda 2024-2034 - geamendeerd`.
- `Besluitenlijst Maatschappelijke agenda 2024-2034`.
- `Opzet procesevaluatie en monitor Sociaal Domein`.
- GGD Flevoland `Tabellenboek Volwassenen 2024 Gemeenten`.
- GGD Flevoland `Tabellenboek Ouderen 2024 Gemeenten`.
- GGD Flevoland `Valpreventie Gemeente Almere`.
- ZonMw `Doorontwikkeling Zorgzaam Flevoland`, supporting only.

## Carry Forward

- The 2 February 2025 raadsbrief remains a local-validation lookup because no public URL was found.
- MGN role/geography evidence should be handled through a sanitized extract or later role-validation workflow.
- Generated claims from the newly ingested Documentwijzer, GGD, and ZonMw sources must be reviewed before they are promoted into public-facing policy conclusions.
- Gaps that require non-public local knowledge, staff confirmation, or formal decisions should be sent forward in the workflow after the public-source structure is filled.
