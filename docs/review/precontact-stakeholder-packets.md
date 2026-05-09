# Pre-contact Stakeholder Packets

## Summary
Current sprint: Sprint 33.P4 - Pre-contact validation-readiness: build stakeholder packets.

Generated on: 2026-05-09.

This file indexes filtered D5/D6 validation packet drafts. They are prepared, not sent. They are not stakeholder validation records.

## Guardrails

- Prepared packets are not sent and are not stakeholder validation records.
- Do not contact policymakers before the P7 send-readiness gate.
- Keep vraag_id values in every outgoing packet and returned answer.
- Human answers must be processed through validation logs, finance matrices, decision registers, dependency maps or source intake as appropriate.
- Do not fill unanswered fields by repository inference.

## Packet Overview

| Packet | Rows | D5 | D6 | CSV | Cleanup before send |
| --- | ---: | ---: | ---: | --- | --- |
| D6 validatie-owner (`d6_validation_owner`) | 9 | 9 | 0 | `data/workagenda/precontact_packets/d6_validation_owner.csv` | 1 item(s) |
| Finance/controller (`finance_controller`) | 53 | 13 | 40 | `data/workagenda/precontact_packets/finance_controller.csv` | 2 item(s) |
| Gemeente Almere sociaal domein - D5 lokale invulling (`gemeente_almere_sociaal_domein_d5`) | 54 | 54 | 0 | `data/workagenda/precontact_packets/gemeente_almere_sociaal_domein_d5.csv` | none |
| Gemeente Almere sociaal domein - D6 validatie (`gemeente_almere_sociaal_domein_d6`) | 79 | 0 | 79 | `data/workagenda/precontact_packets/gemeente_almere_sociaal_domein_d6.csv` | 4 item(s) |
| Gemeente Almere sociaal domein - sturing en afhankelijkheden (`gemeente_almere_sociaal_domein_sturing`) | 14 | 14 | 0 | `data/workagenda/precontact_packets/gemeente_almere_sociaal_domein_sturing.csv` | 1 item(s) |
| GGD/JGZ (`ggd_jgz`) | 71 | 44 | 27 | `data/workagenda/precontact_packets/ggd_jgz.csv` | 2 item(s) |
| GGZ/MGN partners (`ggz_mgn_partners`) | 7 | 7 | 0 | `data/workagenda/precontact_packets/ggz_mgn_partners.csv` | none |
| ICT / data / privacy (`ict_data_privacy`) | 22 | 10 | 12 | `data/workagenda/precontact_packets/ict_data_privacy.csv` | 1 item(s) |
| Kernteam werkagenda (`kernteam_werkagenda`) | 17 | 17 | 0 | `data/workagenda/precontact_packets/kernteam_werkagenda.csv` | 1 item(s) |
| Onderwijs partners (`onderwijs_partners`) | 8 | 0 | 8 | `data/workagenda/precontact_packets/onderwijs_partners.csv` | 1 item(s) |
| PGA / Zorgzaam / Flever / regionale governance (`pga_zorgzaam_flever_regionale_governance`) | 13 | 0 | 13 | `data/workagenda/precontact_packets/pga_zorgzaam_flever_regionale_governance.csv` | 1 item(s) |
| Regionale governance (`regionale_governance`) | 35 | 10 | 25 | `data/workagenda/precontact_packets/regionale_governance.csv` | 1 item(s) |
| Sociale-basis partners (`sociale_basis_partners`) | 13 | 0 | 13 | `data/workagenda/precontact_packets/sociale_basis_partners.csv` | 1 item(s) |
| VSV / geboortezorg / JGZ (`vsv_geboortezorg_jgz`) | 15 | 15 | 0 | `data/workagenda/precontact_packets/vsv_geboortezorg_jgz.csv` | none |
| Welzijn en sociale basis (`welzijn_sociale_basis`) | 14 | 14 | 0 | `data/workagenda/precontact_packets/welzijn_sociale_basis.csv` | none |
| Wijkgerichte GGZ-/welzijnspartners (`wijkgerichte_ggz_welzijnspartners`) | 8 | 0 | 8 | `data/workagenda/precontact_packets/wijkgerichte_ggz_welzijnspartners.csv` | 1 item(s) |
| Wijkteams / SLT-leads (`wijkteams_slt_leads`) | 18 | 0 | 18 | `data/workagenda/precontact_packets/wijkteams_slt_leads.csv` | none |
| Zorgverzekeraar/Zvw (`zorgverzekeraar_zvw`) | 42 | 42 | 0 | `data/workagenda/precontact_packets/zorgverzekeraar_zvw.csv` | none |

## Packet Details

### D6 validatie-owner

Packet ID: `d6_validation_owner`

Status: `prepared_not_sent`

Purpose: D5-D6-afhankelijkheden en D6-randvoorwaarden bewaken.

Instruction: Gebruik dit pakket om D6-afhankelijkheden te controleren; markeer formele D6-settlement als stakeholder-/beleidsbesluit.

CSV: `data/workagenda/precontact_packets/d6_validation_owner.csv`

Contact owner: D6 validation owner

Escalation route: Projectlead werkagenda / D6 beleidsowner

Rows: 9 (9 D5, 0 D6)

Cleanup before send:

- `d5_validation_workbook` / `D6 afhankelijkheden`: Add a concise current working view before stakeholder contact.

Sample questions:

| Vraag ID | Domain | Sheet | Question |
| --- | --- | --- | --- |
| `D5-D6DEP-001` | D5 | D6 afhankelijkheden | Laagdrempelige steunpunten |
| `D5-D6DEP-002` | D5 | D6 afhankelijkheden | Sociaal verwijzen |
| `D5-D6DEP-003` | D5 | D6 afhankelijkheden | Mentale gezondheidsnetwerken |
| `D5-D6DEP-004` | D5 | D6 afhankelijkheden | Valpreventie |
| `D5-D6DEP-005` | D5 | D6 afhankelijkheden | Overgewicht volwassenen |
| `D5-D6DEP-006` | D5 | D6 afhankelijkheden | Kansrijke Start |
| `D5-D6DEP-007` | D5 | D6 afhankelijkheden | Integrale gezinspoli |
| `D5-D6DEP-008` | D5 | D6 afhankelijkheden | Nu Niet Zwanger |
| ... | ... | ... | 1 more row(s) in CSV |

### Finance/controller

Packet ID: `finance_controller`

Status: `prepared_not_sent`

Purpose: Financieringslijn, structureel/projectmatig karakter, dubbeltelling en controllerstatus.

Instruction: Vul geen beleidsinhoud in; beperk antwoorden tot financiering, dekking, dubbeltelling, begrotingsregel en controllerbevestiging.

CSV: `data/workagenda/precontact_packets/finance_controller.csv`

Contact owner: Finance/controller contact

Escalation route: Finance lead / projectlead werkagenda

Rows: 53 (13 D5, 40 D6)

Cleanup before send:

- `d6_validation_workbook` / `Inloopvoorzieningen`: Replace English/technical terms with plain Dutch policy language.
- `d6_validation_workbook` / `Samen Sterker`: Narrow broad monitoring/owner questions before packet export.

Sample questions:

| Vraag ID | Domain | Sheet | Question |
| --- | --- | --- | --- |
| `D5-NNZ-001` | D5 | Nu Niet Zwanger | Structurele regionale coördinatie NNZ |
| `D5-NNZ-002` | D5 | Nu Niet Zwanger | Kinderwensverkenning in reguliere werkwijze |
| `D5-NNZ-003` | D5 | Nu Niet Zwanger | Samenwerking ziekenhuizen, verloskundigen, huisartsen |
| `D5-NNZ-004` | D5 | Nu Niet Zwanger | Toegankelijke anticonceptiezorg en budget |
| `D5-NNZ-005` | D5 | Nu Niet Zwanger | Schaal GGD-regio versus IZA-regio |
| `D5-NNZ-006` | D5 | Nu Niet Zwanger | Privacy en casuïstiekbespreking |
| `D5-OVW-001` | D5 | Overgewicht volwassenen | Doelgroep vanaf licht verhoogd GGR |
| `D5-OVW-002` | D5 | Overgewicht volwassenen | Centrale zorgcoördinator |
| ... | ... | ... | 45 more row(s) in CSV |

### Gemeente Almere sociaal domein - D5 lokale invulling

Packet ID: `gemeente_almere_sociaal_domein_d5`

Status: `prepared_not_sent`

Purpose: D5 lokale status, aanbod, eigenaarschap, prioritering en veilige werkagenda-input.

Instruction: Beantwoord alleen D5-invulling die onder gemeentelijk beleid of sociaal domein valt; verwijs finance-, Zvw- of regionale vragen door.

CSV: `data/workagenda/precontact_packets/gemeente_almere_sociaal_domein_d5.csv`

Contact owner: Gemeente Almere beleidscontact

Escalation route: Projectlead werkagenda / beleidsowner

Rows: 54 (54 D5, 0 D6)

Cleanup before send: none flagged by the prefill audit.

Sample questions:

| Vraag ID | Domain | Sheet | Question |
| --- | --- | --- | --- |
| `D5-KS-001` | D5 | Kansrijke Start | Coalitie Kansrijke Start lokaal en regionaal |
| `D5-KS-002` | D5 | Kansrijke Start | Onderbouwde keuzes hulp- en ondersteuningsaanbod |
| `D5-KS-003` | D5 | Kansrijke Start | Samenwerkingsafspraken uitvoerend/organisatorisch/bestuurlijk |
| `D5-KS-004` | D5 | Kansrijke Start | Professionals kennen belang eerste 1000 dagen en handelen |
| `D5-KS-005` | D5 | Kansrijke Start | Ouders/ervaringskennis/sleutelfiguren betrokken |
| `D5-KS-006` | D5 | Kansrijke Start | Samenhang met Integrale gezinspoli en NNZ |
| `D5-KS-007` | D5 | Kansrijke Start | Financiering en structurele borging |
| `D5-LSP-001` | D5 | Laagdremp. steunpunten | Minimaal één laagdrempelig steunpunt per gemeente |
| ... | ... | ... | 46 more row(s) in CSV |

### Gemeente Almere sociaal domein - D6 validatie

Packet ID: `gemeente_almere_sociaal_domein_d6`

Status: `prepared_not_sent`

Purpose: D6-classificatie, lokale eigenaar, mandaat, veilige formulering en sociaal-domeinrelatie.

Instruction: Bevestig of corrigeer D6-relatie en lokale rol; laat financiering of formele settlement staan als aparte evidence- of besluitvraag.

CSV: `data/workagenda/precontact_packets/gemeente_almere_sociaal_domein_d6.csv`

Contact owner: Gemeente Almere beleidscontact

Escalation route: Projectlead werkagenda / D6 beleidsowner

Rows: 79 (0 D5, 79 D6)

Cleanup before send:

- `d6_validation_workbook` / `Gezonde School`: Narrow broad monitoring/owner questions before packet export.
- `d6_validation_workbook` / `Inloopvoorzieningen`: Replace English/technical terms with plain Dutch policy language.
- `d6_validation_workbook` / `PGA-Zorgzaam-Flever`: Replace English/technical terms with plain Dutch policy language.
- `d6_validation_workbook` / `Samen Sterker`: Narrow broad monitoring/owner questions before packet export.

Sample questions:

| Vraag ID | Domain | Sheet | Question |
| --- | --- | --- | --- |
| `D6-FIN-001` | D6 | Financiering | Inloopvoorzieningen sociaal en gezond |
| `D6-FIN-002` | D6 | Financiering | Wijkteams Almere |
| `D6-FIN-003` | D6 | Financiering | Stevige Lokale Teams |
| `D6-FIN-004` | D6 | Financiering | JGZ Almere |
| `D6-FIN-005` | D6 | Financiering | GGD Flevoland-coördinatie |
| `D6-FIN-006` | D6 | Financiering | Gezonde School / schoolwelzijn |
| `D6-FIN-007` | D6 | Financiering | Kennis & Advies / monitoring / dashboards |
| `D6-FIN-008` | D6 | Financiering | Samen Sterker in de Wijk |
| ... | ... | ... | 71 more row(s) in CSV |

### Gemeente Almere sociaal domein - sturing en afhankelijkheden

Packet ID: `gemeente_almere_sociaal_domein_sturing`

Status: `prepared_not_sent`

Purpose: Governance, D5-D6-afhankelijkheden, optionele ontwikkelagenda en bestuurlijke sturing.

Instruction: Gebruik dit pakket voor sturings- en besluitvoorbereiding; markeer punten die een apart besluit of andere eigenaar nodig hebben.

CSV: `data/workagenda/precontact_packets/gemeente_almere_sociaal_domein_sturing.csv`

Contact owner: Gemeente Almere beleidscontact

Escalation route: Projectlead werkagenda / beleidsowner

Rows: 14 (14 D5, 0 D6)

Cleanup before send:

- `d5_validation_workbook` / `D6 afhankelijkheden`: Add a concise current working view before stakeholder contact.

Sample questions:

| Vraag ID | Domain | Sheet | Question |
| --- | --- | --- | --- |
| `D5-D6DEP-001` | D5 | D6 afhankelijkheden | Laagdrempelige steunpunten |
| `D5-D6DEP-002` | D5 | D6 afhankelijkheden | Sociaal verwijzen |
| `D5-D6DEP-003` | D5 | D6 afhankelijkheden | Mentale gezondheidsnetwerken |
| `D5-D6DEP-004` | D5 | D6 afhankelijkheden | Valpreventie |
| `D5-D6DEP-005` | D5 | D6 afhankelijkheden | Overgewicht volwassenen |
| `D5-D6DEP-006` | D5 | D6 afhankelijkheden | Kansrijke Start |
| `D5-D6DEP-007` | D5 | D6 afhankelijkheden | Integrale gezinspoli |
| `D5-D6DEP-008` | D5 | D6 afhankelijkheden | Nu Niet Zwanger |
| ... | ... | ... | 6 more row(s) in CSV |

### GGD/JGZ

Packet ID: `ggd_jgz`

Status: `prepared_not_sent`

Purpose: JGZ/GGD-taaksplit, publieke gezondheid, preventie, monitoring, Kansrijke Start, NNZ, valpreventie en overgewicht kinderen.

Instruction: Beantwoord taak-, schaal-, uitvoerings- en monitoringvragen; markeer gemeentelijke of financevragen als niet mijn domein.

CSV: `data/workagenda/precontact_packets/ggd_jgz.csv`

Contact owner: GGD/JGZ contact

Escalation route: GGD/JGZ lead / projectlead werkagenda

Rows: 71 (44 D5, 27 D6)

Cleanup before send:

- `d5_validation_workbook` / `Monitoring cyclus`: Add a concise current working view before stakeholder contact.
- `d6_validation_workbook` / `Gezonde School`: Narrow broad monitoring/owner questions before packet export.

Sample questions:

| Vraag ID | Domain | Sheet | Question |
| --- | --- | --- | --- |
| `D5-IGP-001` | D5 | Integrale gezinspoli | Bestaan/status integrale gezinspoli |
| `D5-IGP-002` | D5 | Integrale gezinspoli | Kernteam medisch, publieke gezondheid en sociaal domein |
| `D5-IGP-003` | D5 | Integrale gezinspoli | Eén aanspreekpunt voor het gezin |
| `D5-IGP-004` | D5 | Integrale gezinspoli | Expertise op één plek / huiselijke context |
| `D5-IGP-005` | D5 | Integrale gezinspoli | Multidisciplinair overleg |
| `D5-IGP-006` | D5 | Integrale gezinspoli | Informele steunorganisaties inzetten |
| `D5-IGP-007` | D5 | Integrale gezinspoli | Taakverschuiving en werkproces dreigende ziekenhuisinstroom |
| `D5-IGP-008` | D5 | Integrale gezinspoli | Privacy/casuïstiek en gegevensdeling |
| ... | ... | ... | 63 more row(s) in CSV |

### GGZ/MGN partners

Packet ID: `ggz_mgn_partners`

Status: `prepared_not_sent`

Purpose: Mentale gezondheidsnetwerken, verkennend gesprek, transfermechanisme, LSP-relatie en continuïteit.

Instruction: Bevestig MGN-functies, uitvoeringsmodel, schaal en continuïteit; verwijs financiering door waar nodig.

CSV: `data/workagenda/precontact_packets/ggz_mgn_partners.csv`

Contact owner: GGZ/MGN contact

Escalation route: Regionale governance / projectlead werkagenda

Rows: 7 (7 D5, 0 D6)

Cleanup before send: none flagged by the prefill audit.

Sample questions:

| Vraag ID | Domain | Sheet | Question |
| --- | --- | --- | --- |
| `D5-MGN-001` | D5 | Mentale gezondheid | Regiospecifiek MGN-transformatieplan |
| `D5-MGN-002` | D5 | Mentale gezondheid | Borging na looptijd transformatieplan |
| `D5-MGN-003` | D5 | Mentale gezondheid | Verkennend gesprek |
| `D5-MGN-004` | D5 | Mentale gezondheid | Transfermechanisme |
| `D5-MGN-005` | D5 | Mentale gezondheid | Informatie wachttijden en aanbod |
| `D5-MGN-006` | D5 | Mentale gezondheid | Domeinoverstijgend casusoverleg |
| `D5-MGN-007` | D5 | Mentale gezondheid | Samenhang met sociaal verwijzen en LSP |

### ICT / data / privacy

Packet ID: `ict_data_privacy`

Status: `prepared_not_sent`

Purpose: Operationele eigenaar, data-/privacyverantwoordelijkheid, monitoring, dashboards en digitale infrastructuur.

Instruction: Beantwoord alleen data-, privacy-, security-, dashboard- en operationele systeemverantwoordelijkheid.

CSV: `data/workagenda/precontact_packets/ict_data_privacy.csv`

Contact owner: ICT/data/privacy contact

Escalation route: ICT/privacy lead / projectlead werkagenda

Rows: 22 (10 D5, 12 D6)

Cleanup before send:

- `d5_validation_workbook` / `Monitoring cyclus`: Add a concise current working view before stakeholder contact.

Sample questions:

| Vraag ID | Domain | Sheet | Question |
| --- | --- | --- | --- |
| `D5-MON-001` | D5 | Monitoring cyclus | Overkoepelende doelen |
| `D5-MON-002` | D5 | Monitoring cyclus | Laagdrempelige steunpunten |
| `D5-MON-003` | D5 | Monitoring cyclus | Sociaal verwijzen |
| `D5-MON-004` | D5 | Monitoring cyclus | Valpreventie |
| `D5-MON-005` | D5 | Monitoring cyclus | Overgewicht volwassenen |
| `D5-MON-006` | D5 | Monitoring cyclus | Kansrijke Start |
| `D5-MON-007` | D5 | Monitoring cyclus | Integrale gezinspoli |
| `D5-MON-008` | D5 | Monitoring cyclus | Nu Niet Zwanger |
| ... | ... | ... | 14 more row(s) in CSV |

### Kernteam werkagenda

Packet ID: `kernteam_werkagenda`

Status: `prepared_not_sent`

Purpose: Integratie, voortgangsbewaking en controle op alle pakketten.

Instruction: Gebruik dit pakket voor interne sturing; stuur het niet als volledig validatiepakket naar externe stakeholders.

CSV: `data/workagenda/precontact_packets/kernteam_werkagenda.csv`

Contact owner: Kernteam werkagenda

Escalation route: Projectlead werkagenda

Rows: 17 (17 D5, 0 D6)

Cleanup before send:

- `d5_validation_workbook` / `Overzicht D5`: Add or clarify a short correction/toelichting field.

Sample questions:

| Vraag ID | Domain | Sheet | Question |
| --- | --- | --- | --- |
| `D5-OPT-001` | D5 | Optionele ontwikkelagenda | Dementie |
| `D5-OPT-002` | D5 | Optionele ontwikkelagenda | Nicotinevrij |
| `D5-OPT-003` | D5 | Optionele ontwikkelagenda | Rookvrije start |
| `D5-OPT-004` | D5 | Optionele ontwikkelagenda | Multiproblematiek NPLV-gebieden |
| `D5-OPT-005` | D5 | Optionele ontwikkelagenda | Ontwikkelagenda 2 / overige initiatieven |
| `D5-OVZ-001` | D5 | Overzicht D5 | Laagdrempelige steunpunten |
| `D5-OVZ-002` | D5 | Overzicht D5 | Sociaal verwijzen |
| `D5-OVZ-003` | D5 | Overzicht D5 | Valpreventie |
| ... | ... | ... | 9 more row(s) in CSV |

### Onderwijs partners

Packet ID: `onderwijs_partners`

Status: `prepared_not_sent`

Purpose: Gezonde School, schoolwelzijn en onderwijsgerelateerde preventie.

Instruction: Bevestig alleen school-/onderwijspraktijk, betrokken partners, schaal en bewijsstukken.

CSV: `data/workagenda/precontact_packets/onderwijs_partners.csv`

Contact owner: Onderwijscontact

Escalation route: Gemeente Almere / GGD/JGZ

Rows: 8 (0 D5, 8 D6)

Cleanup before send:

- `d6_validation_workbook` / `Gezonde School`: Narrow broad monitoring/owner questions before packet export.

Sample questions:

| Vraag ID | Domain | Sheet | Question |
| --- | --- | --- | --- |
| `D6-GS-001` | D6 | Gezonde School | D6-relatie: Welke beschrijving past bij Gezonde School / schoolwelzijn in Almere? |
| `D6-GS-002` | D6 | Gezonde School | Verantwoordelijke eigenaar: Wie is verantwoordelijk eigenaar? |
| `D6-GS-003` | D6 | Gezonde School | Coördinator: Wie coördineert? |
| `D6-GS-004` | D6 | Gezonde School | Uitvoerder/partner: Wie voert uit of is partner? |
| `D6-GS-005` | D6 | Gezonde School | Financieringslijn: Welke financieringslijn geldt? |
| `D6-GS-006` | D6 | Gezonde School | Continuïteit: Is dit structureel, projectmatig of nog open? |
| `D6-GS-007` | D6 | Gezonde School | Schaal: Op welke schaal werkt dit? |
| `D6-GS-008` | D6 | Gezonde School | Bewijstype: Welk type bewijs ondersteunt de keuze? |

### PGA / Zorgzaam / Flever / regionale governance

Packet ID: `pga_zorgzaam_flever_regionale_governance`

Status: `prepared_not_sent`

Purpose: Actor-rolscheiding, lokaal/regionaal programma, participatieondersteuning en governance-interface.

Instruction: Bevestig rol en schaal per actor; behandel eigenaarschap, mandaat en financiering als aparte validatie- of besluitvraag.

CSV: `data/workagenda/precontact_packets/pga_zorgzaam_flever_regionale_governance.csv`

Contact owner: PGA/Zorgzaam/Flever contact

Escalation route: Regionale governance / projectlead werkagenda

Rows: 13 (0 D5, 13 D6)

Cleanup before send:

- `d6_validation_workbook` / `PGA-Zorgzaam-Flever`: Replace English/technical terms with plain Dutch policy language.

Sample questions:

| Vraag ID | Domain | Sheet | Question |
| --- | --- | --- | --- |
| `D6-DIG-001` | D6 | Digitaal-operationeel | RTP |
| `D6-DIG-002` | D6 | Digitaal-operationeel | RSO/data-infrastructuur |
| `D6-DIG-003` | D6 | Digitaal-operationeel | Thuismonitoring / Monitoring@home |
| `D6-DIG-004` | D6 | Digitaal-operationeel | GGD dashboards/monitoring |
| `D6-DIG-005` | D6 | Digitaal-operationeel | ACP/PZP data-sharing pilots |
| `D6-DIG-006` | D6 | Digitaal-operationeel | Overig |
| `D6-PZF-001` | D6 | PGA-Zorgzaam-Flever | PGA |
| `D6-PZF-002` | D6 | PGA-Zorgzaam-Flever | Zorgzaam Flevoland |
| ... | ... | ... | 5 more row(s) in CSV |

### Regionale governance

Packet ID: `regionale_governance`

Status: `prepared_not_sent`

Purpose: Regionale rolverdeling, governance, monitoring, D5/D6-samenhang en werkagenda-route.

Instruction: Bevestig alleen regionale proces-, governance- en afstemmingsrollen; markeer lokale uitvoering of financevragen als niet mijn domein.

CSV: `data/workagenda/precontact_packets/regionale_governance.csv`

Contact owner: Regionale governance contact

Escalation route: Mandaatgemeente / projectlead werkagenda

Rows: 35 (10 D5, 25 D6)

Cleanup before send:

- `d5_validation_workbook` / `Monitoring cyclus`: Add a concise current working view before stakeholder contact.

Sample questions:

| Vraag ID | Domain | Sheet | Question |
| --- | --- | --- | --- |
| `D5-MON-001` | D5 | Monitoring cyclus | Overkoepelende doelen |
| `D5-MON-002` | D5 | Monitoring cyclus | Laagdrempelige steunpunten |
| `D5-MON-003` | D5 | Monitoring cyclus | Sociaal verwijzen |
| `D5-MON-004` | D5 | Monitoring cyclus | Valpreventie |
| `D5-MON-005` | D5 | Monitoring cyclus | Overgewicht volwassenen |
| `D5-MON-006` | D5 | Monitoring cyclus | Kansrijke Start |
| `D5-MON-007` | D5 | Monitoring cyclus | Integrale gezinspoli |
| `D5-MON-008` | D5 | Monitoring cyclus | Nu Niet Zwanger |
| ... | ... | ... | 27 more row(s) in CSV |

### Sociale-basis partners

Packet ID: `sociale_basis_partners`

Status: `prepared_not_sent`

Purpose: Inloopvoorzieningen, informele steun, vrijwilligerswerk, mantelzorg en burgerinitiatieven.

Instruction: Bevestig alleen concrete voorzieningen, mechanismen, partners, schaal en bewijs.

CSV: `data/workagenda/precontact_packets/sociale_basis_partners.csv`

Contact owner: Sociale-basis partnercontact

Escalation route: Gemeente Almere sociaal domein

Rows: 13 (0 D5, 13 D6)

Cleanup before send:

- `d6_validation_workbook` / `Inloopvoorzieningen`: Replace English/technical terms with plain Dutch policy language.

Sample questions:

| Vraag ID | Domain | Sheet | Question |
| --- | --- | --- | --- |
| `D6-INF-001` | D6 | Informele steun | Wijkbudget |
| `D6-INF-002` | D6 | Informele steun | Bewonersgestuurde buurtsteun |
| `D6-INF-003` | D6 | Informele steun | VMCA vrijwilligerssteun |
| `D6-INF-004` | D6 | Informele steun | De Schoor sociale-basissteun |
| `D6-INF-005` | D6 | Informele steun | Humanitas informele steun |
| `D6-INF-006` | D6 | Informele steun | Mantelzorgsteun |
| `D6-INF-007` | D6 | Informele steun | Preventienetwerk-actor |
| `D6-INF-008` | D6 | Informele steun | Overig |
| ... | ... | ... | 5 more row(s) in CSV |

### VSV / geboortezorg / JGZ

Packet ID: `vsv_geboortezorg_jgz`

Status: `prepared_not_sent`

Purpose: Kansrijke Start, integrale gezinspoli, Nu Niet Zwanger en geboortezorgafspraken.

Instruction: Bevestig coalitie, afspraken, uitvoering, privacy/casuïstiek en bewijsstukken binnen geboortezorg/JGZ-scope.

CSV: `data/workagenda/precontact_packets/vsv_geboortezorg_jgz.csv`

Contact owner: VSV/geboortezorg/JGZ contact

Escalation route: GGD/JGZ lead / projectlead werkagenda

Rows: 15 (15 D5, 0 D6)

Cleanup before send: none flagged by the prefill audit.

Sample questions:

| Vraag ID | Domain | Sheet | Question |
| --- | --- | --- | --- |
| `D5-IGP-001` | D5 | Integrale gezinspoli | Bestaan/status integrale gezinspoli |
| `D5-IGP-002` | D5 | Integrale gezinspoli | Kernteam medisch, publieke gezondheid en sociaal domein |
| `D5-IGP-003` | D5 | Integrale gezinspoli | Eén aanspreekpunt voor het gezin |
| `D5-IGP-004` | D5 | Integrale gezinspoli | Expertise op één plek / huiselijke context |
| `D5-IGP-005` | D5 | Integrale gezinspoli | Multidisciplinair overleg |
| `D5-IGP-006` | D5 | Integrale gezinspoli | Informele steunorganisaties inzetten |
| `D5-IGP-007` | D5 | Integrale gezinspoli | Taakverschuiving en werkproces dreigende ziekenhuisinstroom |
| `D5-IGP-008` | D5 | Integrale gezinspoli | Privacy/casuïstiek en gegevensdeling |
| ... | ... | ... | 7 more row(s) in CSV |

### Welzijn en sociale basis

Packet ID: `welzijn_sociale_basis`

Status: `prepared_not_sent`

Purpose: Laagdrempelige steunpunten, sociaal verwijzen, brugfunctie, informele steun en lokale uitvoering.

Instruction: Bevestig bestaand aanbod, dekking, uitvoerders, routes en bewijsstukken; markeer besluit- of financevragen als niet mijn domein.

CSV: `data/workagenda/precontact_packets/welzijn_sociale_basis.csv`

Contact owner: Welzijn/sociale-basis contact

Escalation route: Gemeente Almere sociaal domein

Rows: 14 (14 D5, 0 D6)

Cleanup before send: none flagged by the prefill audit.

Sample questions:

| Vraag ID | Domain | Sheet | Question |
| --- | --- | --- | --- |
| `D5-LSP-001` | D5 | Laagdremp. steunpunten | Minimaal één laagdrempelig steunpunt per gemeente |
| `D5-LSP-002` | D5 | Laagdremp. steunpunten | Passend netwerk van verschillende typen LSP's |
| `D5-LSP-003` | D5 | Laagdremp. steunpunten | Doelgroep EPA en sociaal-emotionele kwetsbaarheid |
| `D5-LSP-004` | D5 | Laagdremp. steunpunten | Tien kenmerken voor LSP's |
| `D5-LSP-005` | D5 | Laagdremp. steunpunten | Samenhang met mentale gezondheidsnetwerken |
| `D5-LSP-006` | D5 | Laagdremp. steunpunten | Eigenaar, coördinator en uitvoerders |
| `D5-LSP-007` | D5 | Laagdremp. steunpunten | Financiering en structurele borging |
| `D5-SV-001` | D5 | Sociaal verwijzen | Capaciteit brede gesprek huisarts/eerstelijn |
| ... | ... | ... | 6 more row(s) in CSV |

### Wijkgerichte GGZ-/welzijnspartners

Packet ID: `wijkgerichte_ggz_welzijnspartners`

Status: `prepared_not_sent`

Purpose: Samen Sterker in de Wijk, wijkgerichte mentale-gezondheidsinfrastructuur, schaal en continuïteit.

Instruction: Bevestig actuele status, schaal, partners en bewijs; laat D6-classificatie en financiering expliciet als validatievraag staan.

CSV: `data/workagenda/precontact_packets/wijkgerichte_ggz_welzijnspartners.csv`

Contact owner: Wijkgerichte GGZ-/welzijnscontact

Escalation route: Gemeente Almere / GGZ-MGN lead

Rows: 8 (0 D5, 8 D6)

Cleanup before send:

- `d6_validation_workbook` / `Samen Sterker`: Narrow broad monitoring/owner questions before packet export.

Sample questions:

| Vraag ID | Domain | Sheet | Question |
| --- | --- | --- | --- |
| `D6-SSW-001` | D6 | Samen Sterker | D6-relatie: Welke beschrijving past bij Samen Sterker in de Wijk? |
| `D6-SSW-002` | D6 | Samen Sterker | Schaal: Wat is de huidige schaal? |
| `D6-SSW-003` | D6 | Samen Sterker | Continuïteit: Wat is de huidige continuïteitsstatus? |
| `D6-SSW-004` | D6 | Samen Sterker | Verantwoordelijke eigenaar: Wie is verantwoordelijk eigenaar? |
| `D6-SSW-005` | D6 | Samen Sterker | Coördinator: Wie coördineert? |
| `D6-SSW-006` | D6 | Samen Sterker | Uitvoerder/partner: Wie voert uit of is partner? |
| `D6-SSW-007` | D6 | Samen Sterker | Financieringslijn: Welke financieringslijn geldt? |
| `D6-SSW-008` | D6 | Samen Sterker | Bewijstype: Welk type bewijs ondersteunt de keuze? |

### Wijkteams / SLT-leads

Packet ID: `wijkteams_slt_leads`

Status: `prepared_not_sent`

Purpose: Mandaat, dekking, uitvoeringsmodel en relatie tussen Wijkteams en Stevige Lokale Teams.

Instruction: Bevestig operationele en governancevragen rond wijkteams en SLT; verwijs budgetvragen door naar finance/controller.

CSV: `data/workagenda/precontact_packets/wijkteams_slt_leads.csv`

Contact owner: Wijkteams/SLT lead

Escalation route: Gemeente Almere sociaal domein

Rows: 18 (0 D5, 18 D6)

Cleanup before send: none flagged by the prefill audit.

Sample questions:

| Vraag ID | Domain | Sheet | Question |
| --- | --- | --- | --- |
| `D6-SLT-001` | D6 | SLT | Formele betekenis: Wat regelt de SLT-besluitroute formeel voor D6? |
| `D6-SLT-002` | D6 | SLT | Betrokken onderdelen: Welke onderdelen vallen onder de gekozen interpretatie? |
| `D6-SLT-003` | D6 | SLT | D6-relatie: Welke D6-relatie past het best? |
| `D6-SLT-004` | D6 | SLT | Schaal: Op welke schaal werkt dit? |
| `D6-SLT-005` | D6 | SLT | Verantwoordelijke eigenaar: Welke partij is verantwoordelijk eigenaar? |
| `D6-SLT-006` | D6 | SLT | Coördinator: Welke partij coördineert? |
| `D6-SLT-007` | D6 | SLT | Financieringslijn: Welke financieringslijn geldt? |
| `D6-SLT-008` | D6 | SLT | Continuïteit: Is dit structureel, projectmatig of nog open? |
| ... | ... | ... | 10 more row(s) in CSV |

### Zorgverzekeraar/Zvw

Packet ID: `zorgverzekeraar_zvw`

Status: `prepared_not_sent`

Purpose: Zvw-rol, inkoop, contractering, GLI, CZV, MGN en inzet van zorgprofessionals.

Instruction: Bevestig alleen Zvw-/verzekeraarsrollen, contractering, inkoop en zorgprofessionele inzet.

CSV: `data/workagenda/precontact_packets/zorgverzekeraar_zvw.csv`

Contact owner: Zorgverzekeraar/Zvw contact

Escalation route: Regionale governance / projectlead werkagenda

Rows: 42 (42 D5, 0 D6)

Cleanup before send: none flagged by the prefill audit.

Sample questions:

| Vraag ID | Domain | Sheet | Question |
| --- | --- | --- | --- |
| `D5-IGP-001` | D5 | Integrale gezinspoli | Bestaan/status integrale gezinspoli |
| `D5-IGP-002` | D5 | Integrale gezinspoli | Kernteam medisch, publieke gezondheid en sociaal domein |
| `D5-IGP-003` | D5 | Integrale gezinspoli | Eén aanspreekpunt voor het gezin |
| `D5-IGP-004` | D5 | Integrale gezinspoli | Expertise op één plek / huiselijke context |
| `D5-IGP-005` | D5 | Integrale gezinspoli | Multidisciplinair overleg |
| `D5-IGP-006` | D5 | Integrale gezinspoli | Informele steunorganisaties inzetten |
| `D5-IGP-007` | D5 | Integrale gezinspoli | Taakverschuiving en werkproces dreigende ziekenhuisinstroom |
| `D5-IGP-008` | D5 | Integrale gezinspoli | Privacy/casuïstiek en gegevensdeling |
| ... | ... | ... | 34 more row(s) in CSV |

## Required Before Sending

- Resolve or consciously route cleanup items from `validation-workbook-prefill-audit.md`.
- Confirm that packet CSVs preserve `vraag_id`, evidence fields and `not_my_domain_reroute`.
- Decide whether packet CSVs are the send format or whether they should be converted into filtered Excel tabs.
- Run the internal dry run in Sprint 33.P5 before any stakeholder contact.
- Keep all packet statuses as `prepared_not_sent` until the P7 send-readiness gate passes.

## Next Step

Sprint 33.P5 should run an internal dry run with selected reviewers against these packet drafts: one D5 tab, one D6 tab, one finance row, one evidence field and one `niet mijn domein` case.
