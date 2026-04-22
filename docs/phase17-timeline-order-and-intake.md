# Phase 17 - Chronologische tijdlijn en pipeline-first intake

Deze fase corrigeert twee dingen:

1. De publieke tijdlijn is binnen elk jaar nu strikt chronologisch gesorteerd.
2. Nieuwe externe tijdlijnbronnen worden niet meer direct in de publieke tijdlijn gezet; ze gaan eerst naar een intakebestand voor verdere opname in de bronpijplijn.

## Wat is aangepast

- De volgorde binnen een jaar loopt nu van vroeg naar laat.
- Het huidige jaar (`2026`) blijft standaard open, maar de items binnen dat jaar staan niet meer door elkaar.
- Externe, nog niet-ingelezen webbronnen worden voortaan bijgehouden in:
  - `data/raw/source_intake_candidates.json`

## Waarom deze wijziging

Voor bestuurlijke tijdlijnen moet de pagina:

- snel scanbaar zijn
- chronologisch betrouwbaar zijn
- alleen publieke data tonen die terug te voeren is op de formele pijplijn

Daarom is de juiste werkwijze nu expliciet:

1. bron downloaden / opnemen
2. toevoegen aan `data/raw/manifest.json`
3. door structurele extractie, documentextractie, claims en interpretatie
4. pas daarna op de publieke tijdlijn

## Intakebestand

Het intakebestand bevat:

- kandidaat-bronnen
- kandidaat-deadlines
- status `pending_source_ingestion`

Dat maakt het mogelijk om tijdlijnonderzoek te verzamelen zonder de publieke site alvast te vervuilen met niet-geïntegreerde bronnen.

## Verificatie

```powershell
python -m unittest discover -s tests -p "test_*.py"
python src/run_pipeline.py --all --dry-run
```
