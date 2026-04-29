# Monthly Source Audit

## Summary
Current sprint: Sprint 31.2 - Maandelijkse bronaudit.
Generated on: 2026-04-30.
Live link check: True.
Watchlist items: 6.
Candidate sources: 16.
Pending timeline items: 3.
Pending replacements: 1.
Live link issues: 1.
Live link review items: 1.

Boundary: Pending sources and watchlist items are not public evidence until they are saved, added to the raw manifest, processed by the pipeline and represented in generated layers.

## Expected Source Watchlist

| Source | Status | Expected window | Intake rule | Link check |
| --- | --- | --- | --- | --- |
| Meicirculaire gemeentefonds 2026 | `not_due_yet` | 2026-05-01 to 2026-06-15 | Pas toevoegen als eigen bron nadat de 2026-circulairepagina of PDF publiek beschikbaar is. | 200 ok |
| Septembercirculaire gemeentefonds 2026 | `not_due_yet` | 2026-09-01 to 2026-10-15 | Pas toevoegen als eigen bron nadat de 2026-circulairepagina of PDF publiek beschikbaar is. | 200 ok |
| Decembercirculaire gemeentefonds 2026 | `not_due_yet` | 2026-12-01 to 2027-01-15 | Pas toevoegen als eigen bron nadat de 2026-circulairepagina of PDF publiek beschikbaar is. | 200 ok |
| Handreikingen basisfunctionaliteiten AZWA | `not_due_yet` | 2026-05-26 to 2026-06-30 | Handreikingen pas als bron gebruiken nadat de publicatie of download beschikbaar is; tot die tijd blijft het tijdlijnitem een verwacht vrijgavemoment. | 200 ok |
| Nieuwe AZWA-SPUK voor gemeenten 2027-2029 | `not_due_yet` | 2026-06-01 to 2026-12-31 | Pas opnemen als regeling of uitvoeringspagina wanneer een formele publicatie of aanvraagpagina beschikbaar is. | 200 ok |
| Geintegreerde IZA/AZWA-monitor 2026 | `not_due_yet` | 2026-07-01 to 2026-12-31 | Pas opnemen wanneer een concrete monitorrapportage of Kamerbrief met monitorbijlage beschikbaar is. | 200 ok |

## Pending Replacements

- `nat_vng_iza_azwa_wegwijzer_2026`: VNG Wegwijzer IZA / AZWA (404 issue). De oorspronkelijke URL gaf op 2026-04-22 een 404 terug; vervangende VNG-bron nog selecteren.

## Pending Timeline Items

- 30 september 2026 - Subsidietijdvak DUS-I: `pending_source_ingestion`. Eerst via DUS-I en regeling juridisch valideren; nog niet publiceerbaar.
- oktober 2026 - Gemeentelijke begrotingscyclus Almere: `pending_source_ingestion`. Zoek later exacte lokale data in Almere-bronnen en/of raadsvergaderschema.
- november 2026 - Monitoringsrapportage IZA/AZWA: `pending_source_ingestion`. Eerst valideren via officiële bron.

## Link Issues

- `nat_vng_iza_azwa_wegwijzer_2026`: VNG Wegwijzer IZA / AZWA returned `404` / HTTP Error 404: Not Found.

## Link Review Items

- `nat_wetten_spuk_transformatiemiddelen_regeling`: Regeling specifieke uitkering transformatiemiddelen IZA & AZWA 2024-2028 returned `302` / Redirect handling needs manual review; this is not treated as a dead link by itself..

## Use
Use this audit as a monthly internal source-control note. Do not turn watchlist or pending items into claims, timeline facts or public text until formal intake and pipeline processing have happened.
