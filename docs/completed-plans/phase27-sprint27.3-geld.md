# Sprint 27.3 - Geld

## Summary
Sprint 27.3 is afgerond op 29 april 2026. De claimlaag splitst financiele betekenis nu expliciet uit, zodat financieringsroutes, aanvraagvoorwaarden, budgetvensters, verdeelmechanismen, bestedingsruimte, verantwoordingsregels, lokale financieringsgaten, dubbeltellingsrisico's en algemene financiele context niet meer op dezelfde manier worden gelezen.

## What Changed
- `src/build_claims_top5.py` voegt `money_status` toe aan iedere claim.
- `data/schemas/claim.schema.json` beschrijft de nieuwe geldstatusvelden en toegestane waarden.
- `config/data_quality_perspectives.json` en `docs/data-quality-checklist.md` benoemen de geldstatuswaarden en redactionele guardrails.
- `src/build_site_view_models.py` neemt geldstatus mee in evidence entries en update-claimlijsten.
- `src/build_quality_control.py` controleert dat alle claims een geldige geldstatus hebben en markeert lokale financieringsgaten, dubbeltellingsrisico's en algemene financiele context als reviewpunt.
- `src/build_data_quality_audit.py` schrijft een `money_status_audit` met statusverdeling en verificatie-samples.

## Money Status Values
- `funding_route`: bron noemt een route waarlangs middelen of bekostiging lopen.
- `application_condition`: bron noemt een aanvraagvoorwaarde, procesvoorwaarde of randvoorwaarde.
- `budget_window`: bron noemt een budgetvenster, financieel tijdvak of meerjarige middelenperiode.
- `allocation_mechanism`: bron noemt verdeling, toekenning, uitkering of verdeelmechanisme.
- `spending_scope`: bron noemt bestedingsruimte, inzet van middelen of cofinancieringslogica.
- `accountability_rule`: bron noemt verantwoording, rapportage, aanlevering of controle.
- `local_funding_gap`: publieke bronbasis laat lokale budgetverdeling, eigenaar of dekking nog open.
- `double_counting_risk`: bron of analyse waarschuwt dat financieringslijnen gescheiden moeten blijven.
- `finance_context`: financiele context zonder zelfstandige financieringsregel.
- `not_financial`: geen zelfstandige financiele claim.

## Output
- Claims: regenerated with `money_status`.
- Audit: `data/extracted/data_quality_audit.json` includes `money_status_audit`.
- QC: local funding gaps, double-counting risks and finance-context items are review items, not blockers.

## Verification
- Downstream regeneration from claims through site render completed.
- `python src/verify_claim_id_references.py` passed.
- `python -m pytest` passed.

## Carry Forward
Sprint 27.4 should separate governance roles into decision-making, coordination, application, execution, accountability and review roles. Sprint 25.6 remains parked until stakeholder validation or explicit policy decisions are available.
