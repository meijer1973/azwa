# Sprint 25.2 Public Source Probe

Summary: first public-source probe completed on 2026-04-24. The probe downloaded public council, GGD, ZonMw, MGN, CBS, and Almere annual-account material into `docs/internal/source-intake/phase25.2-public-source-probe/` for assessment only. These files are not yet part of the formal corpus because they are not in `data/raw/manifest.json`.

## Public-only rule

Use only public sources. Do not add private correspondence, non-public personal data, or resident-level health data. If a public page contains named contacts, phone numbers, email addresses, or speaker lists, the formal extraction should suppress those details and retain only organization, role, geography, policy, and aggregate-statistical facts.

## Intake Read

| Source group | Download result | Usefulness | Recommendation |
| --- | --- | --- | --- |
| Documentwijzer 24118 Visie Gezondheidsbeleid | Public Notubiz attachments downloaded | High | Ingest selected primary documents: `VISIE 2024-2026`, geamendeerd raadsvoorstel, final decision route, and Brede SPUK/GALA plan van aanpak. Defer gesprekswijzers, duplicate process files, and ASD advice unless needed for review. |
| Documentwijzer 24161 Maatschappelijke agenda | Public Notubiz attachments downloaded | High | Ingest selected primary documents: `MAATSCHAPPELIJKE AGENDA`, geamendeerd raadsvoorstel, final decision route, and `Opzet procesevaluatie en monitor Sociaal Domein`. Defer gesprekswijzers and advice/reaction material unless needed for review. |
| Raadsbrief `Stand van zaken Gezondheidsbeleid (IZA en GALA)` | Not found in this public probe | Unknown | Do not ingest or cite. Keep as human lookup until a public URL is found. |
| GGD Flevoland 2024 table books | Public municipality-level adult and older-person PDFs downloaded | High | Ingest the two municipality-level table books for Sprint 25.3 nulmeting/capacity work. They contain aggregate Almere indicators for overgewicht, valrisico, eenzaamheid, mentale gezondheid, bewegen, and vulnerability. |
| GGD Flevoland Valpreventie Almere | Public general and Almere-specific pages downloaded | High | Ingest the Almere-specific page as operational execution evidence for valpreventie. |
| ZonMw Doorontwikkeling Zorgzaam Flevoland | Public project page downloaded | Medium-high | Ingest as supporting governance source only. It is a project registration, not an adopted local policy document. |
| Mentale gezondheidsnetwerken listing | Public listing downloaded | High for role/scope only | Ingest only sanitized role/geography facts: Almere as mandaatgemeente for MGN Flevoland; Zeewolde listed under Gezond Veluwe. Suppress contact-person details. |
| Almere Programmarekening 2024 | Public PDF downloaded | Medium | Defer unless needed for money/governance; too broad for the first 25.2 intake batch. |
| CBS 2025 population-growth news | Public page downloaded | Low-medium | Defer. Use a stable CBS/BRP table for Sprint 25.3 denominator calculations instead of a news page. |

## First Intake Batch

Recommended first formal corpus batch:

- `Visie Gezondheidsbeleid Almere 2024-2026`.
- `Raadsvoorstel Visie Gezondheidsbeleid Almere 2024-2026 - geamendeerd`.
- `Integraal plan van aanpak 2024-2026` for Brede SPUK/GALA.
- `Maatschappelijke agenda 2024-2034`.
- `Raadsvoorstel Maatschappelijke agenda 2024-2034 - geamendeerd`.
- `Opzet procesevaluatie en monitor Sociaal Domein`.
- GGD Flevoland `Tabellenboek Volwassenen 2024 Gemeenten`.
- GGD Flevoland `Tabellenboek Ouderen 2024 Gemeenten`.
- GGD Flevoland `Valpreventie Gemeente Almere`.
- ZonMw `Doorontwikkeling Zorgzaam Flevoland`, supporting only.
- MGN listing, sanitized role/geography only.

## Still Blocked

- The 2 February 2025 raadsbrief remains blocked because no public URL was found.
- Formal intake still requires moving selected sources into `data/raw/...`, adding manifest entries, and rerunning inventory/extraction/claims.
- Extraction rules should be tightened before ingesting MGN or council-process files so contact details and speaker-list material do not become public claims.
