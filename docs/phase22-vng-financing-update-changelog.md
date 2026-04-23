# Phase 22 — VNG Financing Update Changelog

Datum update: `2026-04-23`  
Vergelijkingsbasis: vorige repositorytoestand op `HEAD` voor de intake van de VNG-bronset van `2026-04-22`.

## Ingenomen nieuwe bronnen

1. `nat_vng_brief_azwa_financiering_webpagina_2026`
2. `nat_vng_ledenbrief_azwa_financiering_2026`
3. `nat_vws_brief_azwa_d5_d6_financieringsinstrument_2026`
4. `nat_azwa_opdracht_werkagenda_d5_2026`
5. `nat_azwa_format_werkagenda_d5_2026`
6. `nat_azwa_toelichting_producten_proces_2026`

## Kwantitatieve delta

- Bronnen in `manifest`: `27 -> 33`
- Claims in `claims_master.jsonl`: `298 -> 376`
- Tijdlijnitems in `timeline_register.json`: `26 -> 34`
- Tijdlijnitems in jaar `2026`: `10 -> 17`
- Tijdlijnitems in jaar `2027`: `5 -> 6`
- QC blokkades: `0 -> 0`
- QC waarschuwingen: `0 -> 0`
- Review-items: `35 -> 41`

## Inhoudelijke veranderingen in de dataset

### 1. Financieringsroute scherper vastgelegd

De dataset bevat nu een explicieter landelijk spoor dat gemeenten:

- vanaf `2027` middelen ontvangen via een nieuwe `SPUK`
- die SPUK vooralsnog wordt neergezet als venster voor `2027-2029`
- de nadere SPUK-regeling later in `2026` nog apart gepubliceerd krijgt

Belangrijkste bron:

- `nat_vws_brief_azwa_d5_d6_financieringsinstrument_2026`

Aanwezige claimonderwerpen die hierdoor zijn uitgebreid:

- `finance.d5_d6.funding_instrument`
- `municipal.implementation_translation`
- `timeline.other`

### 2. Werkagenda D5 is nu explicieter verbonden aan geld en bestuurlijke besluitvorming

De dataset bevat nu een duidelijker uitvoeringspad voor de regionale werkagenda:

- de werkagenda is randvoorwaardelijk voor uitkering van middelen nog in `2026`
- de formele bestuurlijke deadline ligt op `15 november 2026`
- de praktische voorbereidende deadline ligt al rond `medio september 2026`
- de IZA-regiotafel, mandaatgemeente en preferente zorgverzekeraar krijgen een explicieter beschreven rol

Belangrijkste bronnen:

- `nat_vng_ledenbrief_azwa_financiering_2026`
- `nat_azwa_opdracht_werkagenda_d5_2026`
- `nat_azwa_toelichting_producten_proces_2026`

### 3. De lokale en regionale schaal is concreter benoemd

De dataset zegt nu explicieter dat:

- gemeentelijke middelen zowel een lokaal als regionaal karakter hebben
- de werkagenda in regionale samenwerking tot stand komt
- de mandaatgemeente namens gemeenten in de regio een centrale uitvoerings- en verantwoordingsrol heeft

De grootste inhoudelijke toename zit daardoor in:

- `municipal.implementation_translation` `+17` claims uit de nieuwe bronset
- `governance_and_finance.other` `+11`
- `monitoring.other` `+10`

## Nieuwe tijdlijnmomenten

De volgende nieuwe expliciete tijdlijnitems zijn toegevoegd:

1. `2026-04-22` — `AZWA-afspraken D5 en D6 en financieringsinstrument`
2. `2026-04-22` — `Opdracht voor de werkagenda samenwerking zorg en sociaal domein voor D5 AZWA`
3. `2026-04-22` — `Toelichting producten en proces`
4. `2026-09-15` — `Werkagenda moet in de praktijk medio september 2026 gereed zijn`
5. `2026-11-15` — `Regionale werkagenda uiterlijk door colleges vastgesteld`
6. `2026-12-01` — `Nieuwe SPUK-regeling voor gemeenten later in 2026 voorzien`
7. `2026-12-15` — `VNG-ledenbrief: werkagenda randvoorwaardelijk voor uitkering van middelen in 2026`
8. `2027-01-02` — `Nieuwe AZWA-SPUK voor gemeenten voorzien voor 2027-2029`

## Review-impact

De review-queue groeide van `35` naar `41` items. Dat komt vooral doordat deze bronset:

- extra `authority_unclear`-signalen toevoegt vanuit VNG- en begeleidende uitvoeringsdocumenten
- extra `municipality_relevance_inferred`-signalering toevoegt waar landelijke of regionale lijnen nog niet letterlijk als Almere-verplichting zijn overgenomen
- één extra `unresolved_conflict` toevoegt door de nieuwe laag van uitvoerings- en financieringsduiding

Belangrijk:

- er zijn geen nieuwe blokkades
- er zijn geen QC-waarschuwingen meer na het aanscherpen van de bronverwachtingen

## Nog niet als tijdlijnitem gepromoveerd

Wel in de nieuwe bronnen gezien, maar nog niet als stabiel tijdlijnitem gepromoveerd omdat de huidige extractie er nog geen voldoende schone claim van maakte:

- webinar van `23 april 2026`
- verwijzing naar handreikingen na de thematafel van `26 mei 2026`

Deze signalen zitten dus inhoudelijk al wel in de ruwe bronset, maar nog niet als apart, formeel tijdlijnobject in de gegenereerde viewlaag.
