from __future__ import annotations

import json
import re
import unicodedata
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = REPO_ROOT / "data" / "extracted" / "document_inventory.json"
TEXT_DIR = REPO_ROOT / "data" / "intermediate" / "text"
OUTPUT_DIR = REPO_ROOT / "data" / "extracted" / "documents"

EXTRACTION_RUN_ID = "phase3_top5_v1"
TOP5_DOCUMENT_IDS = [
    "nat_azwa_2025_definitief",
    "nat_azwa_2025_onderhandelaarsakkoord",
    "nat_azwa_2026_cw31_kader_d5_d6",
    "reg_flevoland_2023_regioplan_iza",
    "mun_almere_pga_transformatieplan",
]


DOCUMENT_SPECS = {
    "nat_azwa_2025_definitief": {
        "document_level_summary": {
            "d5_main_message": {
                "statement": (
                    "D5 establishes nationally defined basisfunctionaliteiten across five leefgebieden, with "
                    "mutual accountability between insurers, municipalities, and providers and with local choice "
                    "over interventions."
                ),
                "evidence_refs": [
                    {
                        "page": 52,
                        "section": "Bijlage D5 / definitie basisfunctionaliteit",
                        "anchor": "Basisfunctionaliteiten zijn ingedeeld naar leefgebieden",
                    },
                    {
                        "page": 32,
                        "section": "D5 main section",
                        "anchor": "Lokaal wordt bepaald welke interventie ingezet wordt",
                    },
                ],
            },
            "d6_main_message": {
                "statement": (
                    "D6 requires a recognizable social-domain basisinfrastructure in neighbourhood and regional "
                    "settings, including inloopvoorzieningen, local teams, and GGD-linked coordination."
                ),
                "evidence_refs": [
                    {
                        "page": 33,
                        "section": "D6 summary",
                        "anchor": "Het gaat daarbij om een herkenbaar aanbod van inloopvoorzieningen sociaal en gezond",
                    },
                    {
                        "page": 34,
                        "section": "D6 implementation detail",
                        "anchor": "Stevige lokale teams36 zijn essentieel",
                    },
                ],
            },
            "combined_d5_d6_logic": {
                "statement": (
                    "The final AZWA treats D5 as the cross-domain functional package and D6 as the structure that "
                    "must exist in wijk and regio to make those functions work."
                ),
                "evidence_refs": [
                    {
                        "page": 33,
                        "section": "D6 summary",
                        "anchor": "De afspraken op het snijvlak zorg-sociaal (D5) vereisen een goede structuur",
                    }
                ],
            },
            "implementation_relevance_for_municipality": {
                "statement": (
                    "Municipalities are a direct implementation and funding channel because the social-domain and "
                    "health middelen are provided to municipalities and monitored in a way that should fit existing "
                    "council accountability."
                ),
                "evidence_refs": [
                    {
                        "page": 34,
                        "section": "Uitgangspunten financieringsvorm",
                        "anchor": "De middelen voor het sociaal domein en gezondheid worden aan gemeenten verstrekt",
                    },
                    {
                        "page": 34,
                        "section": "Uitgangspunten financieringsvorm",
                        "anchor": "reguliere verantwoording aan de gemeenteraad",
                    },
                ],
            },
        },
        "structured_content": {
            "d5": {
                "explicit_reference_present": True,
                "relevance_note": "Direct D5 source text from the final signed AZWA.",
                "items": [
                    {
                        "statement": (
                            "The D5 basisfunctionaliteiten are organized around five life domains: kansrijk "
                            "opgroeien, gezonde leefstijl, mentale gezondheid, vitaal ouder worden, and "
                            "gezondheidsachterstanden verminderen with selfredzaamheid as a cross-cutting line."
                        ),
                        "evidence_refs": [
                            {
                                "page": 52,
                                "section": "Bijlage D5 / definitie basisfunctionaliteit",
                                "anchor": "Kansrijk opgroeien",
                            }
                        ],
                    },
                    {
                        "statement": (
                            "The directly underbouwde D5 set already includes examples such as sociaal verwijzen and "
                            "valpreventie, while other approaches sit on ontwikkelagenda 1 or deel 2."
                        ),
                        "evidence_refs": [
                            {
                                "page": 32,
                                "section": "D5 main section",
                                "anchor": "basisfunctionaliteiten als sociaal verwijzen en valpreventie",
                            }
                        ],
                    },
                    {
                        "statement": (
                            "Regional workagendas must specify which health goals are pursued, how "
                            "basisfunctionaliteiten are used, and which interventions from the gereedschapskist are "
                            "locally applied."
                        ),
                        "evidence_refs": [
                            {
                                "page": 32,
                                "section": "D5 governance and implementation",
                                "anchor": "De regioplannen worden steeds doorontwikkeld",
                            }
                        ],
                    },
                ],
            },
            "d6": {
                "explicit_reference_present": True,
                "relevance_note": "Direct D6 source text from the final signed AZWA.",
                "items": [
                    {
                        "statement": (
                            "D6 requires a herkenbaar aanbod van inloopvoorzieningen sociaal en gezond, stronger "
                            "local teams, supported citizen initiatives, healthy-school work, and GGD coordination."
                        ),
                        "evidence_refs": [
                            {
                                "page": 33,
                                "section": "D6 summary",
                                "anchor": "Het gaat daarbij om een herkenbaar aanbod van inloopvoorzieningen sociaal en gezond",
                            }
                        ],
                    },
                    {
                        "statement": (
                            "The D6 local structure is concretized through strong local teams in hechte wijkverbanden "
                            "and regional agreements about ketenaanpak governance by Q1 2026."
                        ),
                        "evidence_refs": [
                            {
                                "page": 34,
                                "section": "D6 implementation detail",
                                "anchor": "Stevige lokale teams36 zijn essentieel",
                            },
                            {
                                "page": 34,
                                "section": "D6 implementation detail",
                                "anchor": "Uiterlijk in Q1 2026 worden afspraken gemaakt",
                            },
                        ],
                    },
                ],
            },
            "governance_and_finance": {
                "items": [
                    {
                        "statement": (
                            "The financial chapter makes the budgetary agreements leading and couples AZWA to "
                            "sectoral volume-growth and macro-kader arrangements through 2028."
                        ),
                        "evidence_refs": [
                            {
                                "page": 42,
                                "section": "Financien",
                                "anchor": "De budgettaire afspraken in deze financiele paragraaf zijn leidend",
                            }
                        ],
                    },
                    {
                        "statement": (
                            "For the social domain, a two-year start package for 2027-2028 is used to work out and "
                            "evaluate the measures, with a route to structural funding if the evaluation and plans "
                            "are positive."
                        ),
                        "evidence_refs": [
                            {
                                "page": 44,
                                "section": "Financien / sociaal domein",
                                "anchor": "We gaan nu van de kant met een startpakket met financiering voor 2 jaar",
                            }
                        ],
                    },
                    {
                        "statement": (
                            "The financing form for social-domain resources is to be chosen through a dedicated "
                            "process with VNG and the fund managers under the Financiele-verhoudingswet."
                        ),
                        "evidence_refs": [
                            {
                                "page": 34,
                                "section": "Uitgangspunten financieringsvorm",
                                "anchor": "Voor het selecteren van een financieringsvorm wordt een zorgvuldig proces ingericht",
                            }
                        ],
                    },
                ]
            },
            "timeline_and_status": {
                "items": [
                    {
                        "statement": (
                            "The landelijk kader for D5 is to be fixed in BO IZA/AZWA in Q4 2025, with governance "
                            "and further elaboration in Q1 2026."
                        ),
                        "evidence_refs": [
                            {
                                "page": 32,
                                "section": "D5 governance and implementation",
                                "anchor": "Dit landelijk kader wordt uiterlijk in Q4 2025 vastgesteld",
                            },
                            {
                                "page": 32,
                                "section": "D5 governance and implementation",
                                "anchor": "ZN, VNG en VWS werken uiterlijk Q1 2026 een governance uit",
                            },
                        ],
                    },
                    {
                        "statement": (
                            "The agreement aims for landelijke dekking of the known basisfunctionaliteiten by 2030, "
                            "while local-team aansluiting in hechte wijkverbanden must be in place by Q4 2028."
                        ),
                        "evidence_refs": [
                            {
                                "page": 32,
                                "section": "D5 implementation horizon",
                                "anchor": "toegewerkt naar landelijke dekking vanaf 2030",
                            },
                            {
                                "page": 34,
                                "section": "D6 implementation detail",
                                "anchor": "Deze aansluiting is uiterlijk Q4 2028 overal gereed",
                            },
                        ],
                    },
                ]
            },
            "monitoring_and_evaluation": {
                "items": [
                    {
                        "statement": (
                            "AZWA extends the IZA monitoring model across proces, beweging, and doelgroepen, using "
                            "existing data where possible to limit administrative burden."
                        ),
                        "evidence_refs": [
                            {
                                "page": 48,
                                "section": "Monitoring",
                                "anchor": "voortgang op drie niveaus te volgen",
                            }
                        ],
                    },
                    {
                        "statement": (
                            "A mid-term review is scheduled for early 2027 and can trigger sharper afspraken, "
                            "different middeleninzet, or budget-neutral shifts between sectors before decisions for "
                            "2028."
                        ),
                        "evidence_refs": [
                            {
                                "page": 49,
                                "section": "Bijlage Monitoring / Mid-Term Review",
                                "anchor": "begin 2027 een tussentijds evaluatiemoment",
                            },
                            {
                                "page": 49,
                                "section": "Bijlage Monitoring / Mid-Term Review",
                                "anchor": "Overleg en besluitvorming vindt plaats voor 1 juli 2027",
                            },
                        ],
                    },
                    {
                        "statement": (
                            "The D5 annex itself says the mechanism and implementation will be monitored so parties "
                            "can be aangesproken or the afspraken can be adjusted."
                        ),
                        "evidence_refs": [
                            {
                                "page": 51,
                                "section": "Bijlage D5",
                                "anchor": "Het mechanisme en de uitwerking van de afspraken wordt gemonitord",
                            }
                        ],
                    },
                ]
            },
            "municipal_translation": {
                "items": [
                    {
                        "statement": (
                            "Municipal and care parties are expected to translate D5 into region-specific workagendas "
                            "and to use the gereedschapskist for local implementation choices."
                        ),
                        "evidence_refs": [
                            {
                                "page": 32,
                                "section": "D5 governance and implementation",
                                "anchor": "De regioplannen worden steeds doorontwikkeld",
                            }
                        ],
                    },
                    {
                        "statement": (
                            "Municipal implementation also carries local accountability features: funding goes to "
                            "municipalities, monitoring should rely on existing data sources, and accountability "
                            "should fit regular reporting to the gemeenteraad."
                        ),
                        "evidence_refs": [
                            {
                                "page": 34,
                                "section": "Uitgangspunten financieringsvorm",
                                "anchor": "De middelen voor het sociaal domein en gezondheid worden aan gemeenten verstrekt",
                            },
                            {
                                "page": 34,
                                "section": "Uitgangspunten financieringsvorm",
                                "anchor": "reguliere verantwoording aan de gemeenteraad",
                            },
                        ],
                    },
                ]
            },
        },
    },
    "nat_azwa_2025_onderhandelaarsakkoord": {
        "document_level_summary": {
            "d5_main_message": {
                "statement": (
                    "The onderhandelaarsakkoord already proposes D5 as a national set of basisfunctionaliteiten "
                    "across five leefgebieden, split between directly underbouwde items and two development agendas."
                ),
                "evidence_refs": [
                    {
                        "page": 68,
                        "section": "D5 summary",
                        "anchor": "kansrijk opgroeien, gezonde leefstijl, mentale gezondheid, vitaal ouder worden en gezondheidsachterstanden",
                    }
                ],
            },
            "d6_main_message": {
                "statement": (
                    "The onderhandelaarsakkoord already frames D6 as the supporting basisinfrastructuur in wijk and "
                    "regio, including inloopvoorzieningen, local teams, and GGD-related coordination."
                ),
                "evidence_refs": [
                    {
                        "page": 72,
                        "section": "D6 summary",
                        "anchor": "basisvoorzieningen in wijken en buurten op het gebied van gezondheid",
                    }
                ],
            },
            "combined_d5_d6_logic": {
                "statement": (
                    "The negotiation text already treats D5 and D6 as a pair: D5 contains the basisfunctionaliteiten "
                    "and D6 provides the wijk- and regio-level basis that must support them."
                ),
                "evidence_refs": [
                    {
                        "page": 72,
                        "section": "D6 summary",
                        "anchor": "De afspraken op het snijvlak zorg-sociaal (D5) vereisen een goede structuur",
                    }
                ],
            },
            "implementation_relevance_for_municipality": {
                "statement": (
                    "The negotiation text already places municipalities in the implementation chain because "
                    "regions and gemeenten must work out goals and interventions while social-domain middelen are "
                    "to be granted to municipalities."
                ),
                "evidence_refs": [
                    {
                        "page": 69,
                        "section": "D5 operationalization",
                        "anchor": "In de werkagenda behorend bij het regioplan",
                    },
                    {
                        "page": 70,
                        "section": "Uitgangspunten financieringsvorm",
                        "anchor": "De middelen voor het sociaal domein en gezondheid worden aan gemeenten verstrekt",
                    },
                ],
            },
        },
        "structured_content": {
            "d5": {
                "explicit_reference_present": True,
                "relevance_note": "Direct D5 source text from the onderhandelaarsakkoord.",
                "items": [
                    {
                        "statement": (
                            "The negotiation text already names the directly implementable D5 items and the "
                            "ontwikkelagenda split, including sociaal verwijzen, valpreventie, and a short-term "
                            "development path for other approaches."
                        ),
                        "evidence_refs": [
                            {
                                "page": 68,
                                "section": "D5 summary",
                                "anchor": "De basisfunctionaliteiten laagdrempelige steunpunten EPA",
                            }
                        ],
                    },
                    {
                        "statement": (
                            "Regions and municipalities must work out goals, choose interventions from a "
                            "gereedschapskist, and are made mutually aanspreekbaar on the resulting cooperation."
                        ),
                        "evidence_refs": [
                            {
                                "page": 69,
                                "section": "D5 operationalization",
                                "anchor": "Gemeenten, zorgverzekeraars en aanbieders van zorg en ondersteuning zijn hierop wederzijds aanspreekbaar",
                            },
                            {
                                "page": 69,
                                "section": "D5 operationalization",
                                "anchor": "In de werkagenda behorend bij het regioplan",
                            },
                        ],
                    },
                    {
                        "statement": (
                            "The onderhandelaarsakkoord already links D5 to structural financing conditions, a "
                            "regional monitor, and a content update of the basisfunctionaliteiten in 2028."
                        ),
                        "evidence_refs": [
                            {
                                "page": 69,
                                "section": "D5 operationalization",
                                "anchor": "Tussentijdse voortgang op implementatie van de basisfunctionaliteiten zelf zal in de regio gemonitord worden",
                            },
                            {
                                "page": 69,
                                "section": "D5 operationalization",
                                "anchor": "De basisfunctionaliteiten worden inhoudelijke periodiek geupdatet",
                            },
                        ],
                    },
                ],
            },
            "d6": {
                "explicit_reference_present": True,
                "relevance_note": "Direct D6 source text from the onderhandelaarsakkoord.",
                "items": [
                    {
                        "statement": (
                            "D6 is defined as a basisinfrastructuur with inloopvoorzieningen, stronger local teams, "
                            "support for citizen initiatives, healthy-school work, and regional GGD coordination."
                        ),
                        "evidence_refs": [
                            {
                                "page": 72,
                                "section": "D6 summary",
                                "anchor": "Het gaat daarbij om een herkenbaar aanbod van inloopvoorzieningen sociaal en gezond",
                            }
                        ],
                    }
                ],
            },
            "governance_and_finance": {
                "items": [
                    {
                        "statement": (
                            "The onderhandelaarsakkoord already routes social-domain middelen through municipalities "
                            "and ties the choice of financing form to a process with VNG, the fund managers, and the "
                            "responsible ministry."
                        ),
                        "evidence_refs": [
                            {
                                "page": 70,
                                "section": "Uitgangspunten financieringsvorm",
                                "anchor": "De middelen voor het sociaal domein en gezondheid worden aan gemeenten verstrekt",
                            },
                            {
                                "page": 70,
                                "section": "Uitgangspunten financieringsvorm",
                                "anchor": "Voor het selecteren van een financieringsvorm wordt een zorgvuldig proces ingericht",
                            },
                        ],
                    },
                    {
                        "statement": (
                            "The financial framework already runs through 2028 and sets sectoral growth and remgeld "
                            "allocations that are tied to the AZWA goals."
                        ),
                        "evidence_refs": [
                            {
                                "page": 92,
                                "section": "Financien",
                                "anchor": "De financiele afspraken van het aanvullend zorg- en welzijnsakkoord lopen tot en met 2028",
                            },
                            {
                                "page": 93,
                                "section": "Financien / remgelden",
                                "anchor": "Om de toenemende zorgvraag op te vangen worden structureel middelen toegevoegd",
                            },
                        ],
                    },
                    {
                        "statement": (
                            "The onderhandelaarsakkoord also earmarks doorbraakmiddelen for the social domain to "
                            "accelerate D5 and D6 implementation."
                        ),
                        "evidence_refs": [
                            {
                                "page": 70,
                                "section": "Inzet doorbraakmiddelen",
                                "anchor": "100 mln in 2027 en in 2028",
                            }
                        ],
                    },
                ]
            },
            "timeline_and_status": {
                "items": [
                    {
                        "statement": (
                            "The negotiating text already sets the D5 timetable: Q4 2025 for the landelijk kader, "
                            "Q1 2026 for governance and further plans, and periodic herijking after that."
                        ),
                        "evidence_refs": [
                            {
                                "page": 70,
                                "section": "D5 governance and implementation",
                                "anchor": "Dit landelijk kader wordt uiterlijk in Q4 2025 vastgesteld",
                            },
                            {
                                "page": 70,
                                "section": "D5 governance and implementation",
                                "anchor": "ZN, VNG en VWS werken uiterlijk Q1 2026 een governance uit",
                            },
                        ],
                    },
                    {
                        "statement": (
                            "The negotiation text already aims for landelijke dekking of the known "
                            "basisfunctionaliteiten by 2030."
                        ),
                        "evidence_refs": [
                            {
                                "page": 70,
                                "section": "Inzet doorbraakmiddelen",
                                "anchor": "landelijke dekking vanaf 2030",
                            }
                        ],
                    },
                ]
            },
            "monitoring_and_evaluation": {
                "items": [
                    {
                        "statement": (
                            "The onderhandelaarsakkoord already says that regional D5 implementation will be "
                            "monitored and that the content of the basisfunctionaliteiten will be updated in 2028."
                        ),
                        "evidence_refs": [
                            {
                                "page": 69,
                                "section": "D5 operationalization",
                                "anchor": "Tussentijdse voortgang op implementatie van de basisfunctionaliteiten zelf zal in de regio gemonitord worden",
                            },
                            {
                                "page": 69,
                                "section": "D5 operationalization",
                                "anchor": "De basisfunctionaliteiten worden inhoudelijke periodiek geupdatet",
                            },
                        ],
                    },
                    {
                        "statement": (
                            "The overall monitoring chapter builds on the IZA monitor, keeps process-output-outcome "
                            "levels, and asks for a workafspraak on transitiedoelen before the end of 2025."
                        ),
                        "evidence_refs": [
                            {
                                "page": 105,
                                "section": "Monitoring",
                                "anchor": "Eerder is in het IZA afgesproken om voortgang op drie niveaus te volgen",
                            },
                            {
                                "page": 105,
                                "section": "Monitoring",
                                "anchor": "Een werkafspraak omtrent de monitoring van de transitiedoelstellingen zal voor eind 2025 worden vastgesteld",
                            },
                        ],
                    },
                ]
            },
            "municipal_translation": {
                "items": [
                    {
                        "statement": (
                            "The negotiation text expects every region or gemeente to make D5 operational through a "
                            "workagenda, local intervention choice, and mutual accountability between municipalities, "
                            "insurers, and providers."
                        ),
                        "evidence_refs": [
                            {
                                "page": 68,
                                "section": "D5 summary",
                                "anchor": "Deze functionaliteiten zijn in elke regio of gemeente ingevuld en beschikbaar voor inwoners",
                            },
                            {
                                "page": 69,
                                "section": "D5 operationalization",
                                "anchor": "In de werkagenda behorend bij het regioplan",
                            },
                        ],
                    },
                    {
                        "statement": (
                            "Municipal implementation on the D6 side is tied to local teams, public-health links, "
                            "and neighbourhood-level voorzieningen."
                        ),
                        "evidence_refs": [
                            {
                                "page": 72,
                                "section": "D6 summary",
                                "anchor": "het versterken van lokale teams ten dienste van verbinding met de eerste lijn",
                            }
                        ],
                    },
                ]
            },
        },
    },
    "nat_azwa_2026_cw31_kader_d5_d6": {
        "document_level_summary": {
            "d5_main_message": {
                "statement": (
                    "The CW 3.1 sheet defines D5 as basisfunctionaliteiten meant to reduce inflow into Zvw care by "
                    "strengthening cooperation between the care domain and the social domain."
                ),
                "evidence_refs": [
                    {
                        "page": 1,
                        "section": "CW 3.1 sheet",
                        "anchor": "AZWA D5: Het doel van de basisfunctionaliteiten is beperking van de toestroom in de Zvw-zorg",
                    }
                ],
            },
            "d6_main_message": {
                "statement": (
                    "The same sheet defines D6 as the basisinfrastructuur that provides the required structure in "
                    "wijk and regio for executing the D5 afspraken."
                ),
                "evidence_refs": [
                    {
                        "page": 1,
                        "section": "CW 3.1 sheet",
                        "anchor": "AZWA D6: Het doel van de basisinfrastructuur is om een goede structuur en basis in de wijk en de regio te bieden",
                    }
                ],
            },
            "combined_d5_d6_logic": {
                "statement": (
                    "The CW 3.1 justification explicitly treats D5 and D6 as a linked policy pair in which the "
                    "basisinfrastructuur is required for the implementation of the basisfunctionaliteiten."
                ),
                "evidence_refs": [
                    {
                        "page": 1,
                        "section": "CW 3.1 sheet",
                        "anchor": "Deze structuur en basis in de wijk en regio zijn vereist voor de uitvoering van de afspraken over de basisfunctionaliteiten",
                    }
                ],
            },
            "implementation_relevance_for_municipality": {
                "statement": (
                    "The sheet is municipally relevant because the available middelen are to be granted to "
                    "municipalities and are justified as support for stronger care-social collaboration."
                ),
                "evidence_refs": [
                    {
                        "page": 1,
                        "section": "Beleidsinstrumenten",
                        "anchor": "De financiele middelen die voor deze afspraken beschikbaar zijn gesteld, worden aan gemeenten verstrekt",
                    },
                    {
                        "page": 1,
                        "section": "Financiele gevolgen voor maatschappelijke sectoren",
                        "anchor": "worden de gelden volledig aan gemeenten verstrekt",
                    },
                ],
            },
        },
        "structured_content": {
            "d5": {
                "explicit_reference_present": True,
                "relevance_note": "Direct D5 source text from the CW 3.1 explanatory sheet.",
                "items": [
                    {
                        "statement": (
                            "The D5 objective is to strengthen care-social cooperation so people get equal access to "
                            "the care and support they need, with sociaal verwijzen named as an example."
                        ),
                        "evidence_refs": [
                            {
                                "page": 1,
                                "section": "CW 3.1 sheet",
                                "anchor": "Een voorbeeld van een basisfunctionaliteiten is sociaal verwijzen",
                            }
                        ],
                    },
                    {
                        "statement": (
                            "The sheet describes D5 as a way to implement proven effective basisfunctionaliteiten "
                            "such as sociaal verwijzen and valpreventie on a regional scale."
                        ),
                        "evidence_refs": [
                            {
                                "page": 1,
                                "section": "Nagestreefde doelmatigheid",
                                "anchor": "bewezen effectieve basisfunctionaliteiten (zoals sociaal verwijzen en valpreventie)",
                            }
                        ],
                    },
                ],
            },
            "d6": {
                "explicit_reference_present": True,
                "relevance_note": "Direct D6 source text from the CW 3.1 explanatory sheet.",
                "items": [
                    {
                        "statement": (
                            "D6 is framed as the basis in wijk and regio that must support the execution of the "
                            "basisfunctionaliteiten."
                        ),
                        "evidence_refs": [
                            {
                                "page": 1,
                                "section": "CW 3.1 sheet",
                                "anchor": "De afspraken D5 en D6 zijn een manier om de doelstellingen van het AZWA te realiseren",
                            }
                        ],
                    }
                ],
            },
            "governance_and_finance": {
                "items": [
                    {
                        "statement": (
                            "The policy instrument is a bestuurlijke afspraak between care and social-domain parties, "
                            "with the funding instrument to be chosen through VNG, the fund managers, and VWS under "
                            "the Financiele-verhoudingswet."
                        ),
                        "evidence_refs": [
                            {
                                "page": 1,
                                "section": "Beleidsinstrumenten",
                                "anchor": "bestuurlijke afspraken vastgelegd voor de samenwerking",
                            },
                            {
                                "page": 1,
                                "section": "Beleidsinstrumenten",
                                "anchor": "De financieringsvorm wordt geselecteerd in een zorgvuldig proces",
                            },
                        ],
                    },
                    {
                        "statement": (
                            "The sheet presents a multi-year funding horizon for D5 and D6, covering 2026 through "
                            "2031."
                        ),
                        "evidence_refs": [
                            {
                                "page": 1,
                                "section": "Financiele gevolgen",
                                "anchor": "Jaartal 202 6",
                            },
                            {
                                "page": 1,
                                "section": "Financiele gevolgen",
                                "anchor": "203 1 Basisfunctionaliteit",
                            },
                        ],
                    },
                ]
            },
            "timeline_and_status": {
                "items": [
                    {
                        "statement": (
                            "The CW 3.1 sheet gives a phased financing horizon from 2026 to 2031 for the D5/D6 "
                            "package."
                        ),
                        "evidence_refs": [
                            {
                                "page": 1,
                                "section": "Financiele gevolgen",
                                "anchor": "Jaartal 202 6",
                            }
                        ],
                    }
                ]
            },
            "monitoring_and_evaluation": {
                "items": [
                    {
                        "statement": (
                            "The progress of implementation is to be monitored nationally and the content of the "
                            "basisfunctionaliteiten is to be updated in 2028 based on monitoring and evaluation."
                        ),
                        "evidence_refs": [
                            {
                                "page": 1,
                                "section": "Evaluatieparagraaf",
                                "anchor": "landelijk gemonitord worden",
                            },
                            {
                                "page": 1,
                                "section": "Evaluatieparagraaf",
                                "anchor": "periodiek geupdatet op basis van monitoring en evaluatie",
                            },
                        ],
                    },
                    {
                        "statement": (
                            "The D5/D6 evaluation is also tied back to the broader IZA-based AZWA monitoring and "
                            "evaluation framework."
                        ),
                        "evidence_refs": [
                            {
                                "page": 1,
                                "section": "Evaluatieparagraaf",
                                "anchor": "Het AZWA breed wordt gemonitord en geevalueerd op basis van de eerder gemaakte afspraken",
                            }
                        ],
                    },
                ]
            },
            "municipal_translation": {
                "items": [
                    {
                        "statement": (
                            "The CW 3.1 justification makes municipalities the operational channel for the D5/D6 "
                            "middelen."
                        ),
                        "evidence_refs": [
                            {
                                "page": 1,
                                "section": "Beleidsinstrumenten",
                                "anchor": "worden aan gemeenten verstrekt",
                            }
                        ],
                    },
                    {
                        "statement": (
                            "The justification also frames D6 as a required neighbourhood and regional structure for "
                            "municipal implementation."
                        ),
                        "evidence_refs": [
                            {
                                "page": 1,
                                "section": "CW 3.1 sheet",
                                "anchor": "een goede structuur en basis in de wijk en de regio",
                            }
                        ],
                    },
                ]
            },
        },
    },
    "reg_flevoland_2023_regioplan_iza": {
        "document_level_summary": {
            "d5_main_message": {
                "statement": (
                    "The Regioplan does not use D5 terminology directly, but it does set out integrated "
                    "social-medical collaboration as a regional building block, including mental-health and "
                    "domain-overstijgende cooperation."
                ),
                "statement_type": "source_grounded_summary",
                "evidence_refs": [
                    {
                        "page": 40,
                        "section": "Bouwstenen / mentale gezondheid",
                        "anchor": "Een goede kapstok voor wijkgericht samenwerken aan mentale gezondheid",
                    },
                    {
                        "page": 63,
                        "section": "Bouwstenen / integrale domeinoverstijgende samenwerking",
                        "anchor": "integrale domeinoverstijgende samenwerking essentieel",
                    },
                ],
            },
            "d6_main_message": {
                "statement": (
                    "The Regioplan likewise does not name D6 directly, but it identifies enabling infrastructure "
                    "such as digital data exchange, a regional collaboration organization, and information "
                    "architecture."
                ),
                "evidence_refs": [
                    {
                        "page": 85,
                        "section": "Fundamenten / digitale infrastructuur",
                        "anchor": "Een regionale samenwerkingsorganisatie (organisatiestructuur) voor de regio",
                    }
                ],
            },
            "combined_d5_d6_logic": {
                "statement": (
                    "The Regioplan works as a regional precursor in which local and regional work are combined "
                    "through a transformatieagenda that later determines which solutions are tackled where."
                ),
                "evidence_refs": [
                    {
                        "page": 98,
                        "section": "Aan de slag",
                        "anchor": "We werken regionaal samen op dat wat ons bindt",
                    },
                    {
                        "page": 99,
                        "section": "Transformatieagenda",
                        "anchor": "We maken een weloverwogen afweging wat we lokaal, subregionaal en regionaal aanpakken",
                    },
                ],
            },
            "implementation_relevance_for_municipality": {
                "statement": (
                    "Municipal implementation still needs concrete plans, budgets, and local decision-making, "
                    "including a municipal IZA budget for 2024-2026."
                ),
                "evidence_refs": [
                    {
                        "page": 103,
                        "section": "Begroting",
                        "anchor": "De ambities uit dit Regioplan hebben nog geen financiele doorvertaling",
                    },
                    {
                        "page": 103,
                        "section": "Begroting",
                        "anchor": "Voor de gemeentelijke bijdrage aan de realisatie van dit Regioplan wordt een IZA begroting opgesteld",
                    },
                ],
            },
        },
        "structured_content": {
            "d5": {
                "explicit_reference_present": False,
                "relevance_note": (
                    "No explicit D5 label appears in this pre-AZWA regional plan. The items below are contextual "
                    "regional precursors that can later inform D5-related claim extraction."
                ),
                "items": [
                    {
                        "statement": (
                            "The plan highlights Ecosysteem Mentale Gezondheid and Samen Sterker in de Wijk as a "
                            "model for neighbourhood collaboration around psychosocial problems."
                        ),
                        "statement_type": "contextual_relevance",
                        "evidence_refs": [
                            {
                                "page": 40,
                                "section": "Bouwstenen / mentale gezondheid",
                                "anchor": "Een goede kapstok voor wijkgericht samenwerken aan mentale gezondheid",
                            }
                        ],
                    },
                    {
                        "statement": (
                            "The plan also explicitly calls integrale domeinoverstijgende samenwerking essential "
                            "between the social domain, medical domain, long-term care, geriatrics, and wijk care."
                        ),
                        "statement_type": "contextual_relevance",
                        "evidence_refs": [
                            {
                                "page": 63,
                                "section": "Bouwstenen / integrale domeinoverstijgende samenwerking",
                                "anchor": "integrale domeinoverstijgende samenwerking essentieel",
                            }
                        ],
                    },
                ],
            },
            "d6": {
                "explicit_reference_present": False,
                "relevance_note": (
                    "No explicit D6 label appears in this pre-AZWA regional plan. The items below are contextual "
                    "infrastructure precursors that can later inform D6-related reasoning."
                ),
                "items": [
                    {
                        "statement": (
                            "The Regioplan identifies digital infrastructure as essential and names a regional "
                            "collaboration organization, a shared data-availability vision, information architecture, "
                            "and use-case based rollout."
                        ),
                        "statement_type": "contextual_relevance",
                        "evidence_refs": [
                            {
                                "page": 85,
                                "section": "Fundamenten / digitale infrastructuur",
                                "anchor": "Een regionale samenwerkingsorganisatie (organisatiestructuur) voor de regio",
                            },
                            {
                                "page": 85,
                                "section": "Fundamenten / digitale infrastructuur",
                                "anchor": "Een informatiearchitectuur voor de regio",
                            },
                        ],
                    }
                ],
            },
            "governance_and_finance": {
                "items": [
                    {
                        "statement": (
                            "The Verbindende Coalitie, workgroups, and an expert team are used to shape the "
                            "transformatieagenda and test financial feasibility."
                        ),
                        "evidence_refs": [
                            {
                                "page": 98,
                                "section": "Aan de slag",
                                "anchor": "De Verbindende Coalitie geeft aan het begin van het eerste kwartaal richting",
                            },
                            {
                                "page": 98,
                                "section": "Aan de slag",
                                "anchor": "Het expertteam wordt gevormd ter ondersteuning van de verdere uitwerking",
                            },
                        ],
                    },
                    {
                        "statement": (
                            "The plan itself says the ambitions still need concrete budgets and that financing may "
                            "come from SPUK GALA, SPUK IZA, and transformatiemiddelen."
                        ),
                        "evidence_refs": [
                            {
                                "page": 103,
                                "section": "Begroting",
                                "anchor": "De ambities uit dit Regioplan hebben nog geen financiele doorvertaling",
                            },
                            {
                                "page": 103,
                                "section": "Begroting",
                                "anchor": "SPUK GALA en SPUK IZA",
                            },
                        ],
                    },
                ]
            },
            "timeline_and_status": {
                "items": [
                    {
                        "statement": (
                            "In the first and second quarter of 2024 the workgroups are expected to move toward a "
                            "concrete transformatieagenda."
                        ),
                        "evidence_refs": [
                            {
                                "page": 98,
                                "section": "Aan de slag",
                                "anchor": "in het eerste en tweede kwartaal van 2024",
                            }
                        ],
                    },
                    {
                        "statement": (
                            "The plan expects the definite transformatieagenda by the end of the second quarter and "
                            "sets up kwartiermakers for the fundamental work tracks."
                        ),
                        "evidence_refs": [
                            {
                                "page": 100,
                                "section": "Uitgangspunten",
                                "anchor": "De definitieve transformatieagenda wordt uiterlijk eind tweede kwartaal vastgesteld",
                            },
                            {
                                "page": 100,
                                "section": "Fundamenten",
                                "anchor": "We zoeken per fundament in samenspraak met de Verbindende Coalitie een kwartiermaker",
                            },
                        ],
                    },
                ]
            },
            "monitoring_and_evaluation": {
                "items": [
                    {
                        "statement": (
                            "The Regioplan calls for a 2024 monitoringsplan to show whether the transformatie is "
                            "visible and whether the region is on course."
                        ),
                        "evidence_refs": [
                            {
                                "page": 104,
                                "section": "Monitoring en samen leren",
                                "anchor": "zullen we in 2024 samen met elkaar een monitoringsplan ontwikkelen",
                            }
                        ],
                    },
                    {
                        "statement": (
                            "The monitoring approach combines process, output, and outcome monitoring and aims to "
                            "surface the results in a dashboard while reusing existing data sources where possible."
                        ),
                        "evidence_refs": [
                            {
                                "page": 106,
                                "section": "Monitoring en samen leren",
                                "anchor": "We richten procesmonitoring in",
                            },
                            {
                                "page": 107,
                                "section": "Monitoring en samen leren",
                                "anchor": "willen we werken aan een dashboard",
                            },
                        ],
                    },
                ]
            },
            "municipal_translation": {
                "items": [
                    {
                        "statement": (
                            "The Regioplan explicitly combines regional cooperation with local tailoring and says it "
                            "must keep building on local needs and existing initiatives."
                        ),
                        "evidence_refs": [
                            {
                                "page": 98,
                                "section": "Aan de slag",
                                "anchor": "We werken regionaal samen op dat wat ons bindt",
                            }
                        ],
                    },
                    {
                        "statement": (
                            "A key follow-up issue for municipal implementation is clarifying roles and "
                            "responsibilities between municipality, social domain, insurers, and providers."
                        ),
                        "evidence_refs": [
                            {
                                "page": 101,
                                "section": "Aandachtspunten voor het vervolg",
                                "anchor": "We zetten in op verduidelijking van rollen en verantwoordelijkheden",
                            }
                        ],
                    },
                ]
            },
        },
    },
    "mun_almere_pga_transformatieplan": {
        "document_level_summary": {
            "d5_main_message": {
                "statement": (
                    "The Almere transformatieplan does not use D5 terminology directly, but it clearly focuses on "
                    "prevention and better cooperation between informal care, the social domain, and the medical "
                    "domain."
                ),
                "evidence_refs": [
                    {
                        "page": 2,
                        "section": "Waarom is verandering nodig",
                        "anchor": "van zorg achteraf naar gezondheid voorop",
                    },
                    {
                        "page": 5,
                        "section": "Veerkrachtige, zorgzame wijken",
                        "anchor": "Betere samenwerking tussen informele zorg, sociaal en medisch domein",
                    },
                ],
            },
            "d6_main_message": {
                "statement": (
                    "The plan likewise does not use D6 terminology directly, but it does describe enabling local "
                    "infrastructure such as RTP, RSO, data infrastructure, and a current information picture for "
                    "professionals."
                ),
                "evidence_refs": [
                    {
                        "page": 4,
                        "section": "Ambitie",
                        "anchor": "Zorgprofessionals hebben altijd een actueel informatiebeeld van patienten",
                    },
                    {
                        "page": 6,
                        "section": "Zorg dichterbij huis",
                        "anchor": "Regionale Samenwerkingsorganisatie (RSO)",
                    },
                ],
            },
            "combined_d5_d6_logic": {
                "statement": (
                    "The five local pillars combine neighbourhood collaboration, closer-to-home care, chain "
                    "coordination, and data exchange to reduce pressure on care in Almere."
                ),
                "evidence_refs": [
                    {
                        "page": 4,
                        "section": "Ambitie",
                        "anchor": "Pijlers",
                    },
                    {
                        "page": 6,
                        "section": "Zorg dichterbij huis",
                        "anchor": "Betere doorstroom door zorgcoordinatie",
                    },
                ],
            },
            "implementation_relevance_for_municipality": {
                "statement": (
                    "This is a direct local implementation source for Almere because the municipality is part of "
                    "the core coalition and the plan names local 2029 impact goals."
                ),
                "evidence_refs": [
                    {
                        "page": 3,
                        "section": "Wie zijn betrokken",
                        "anchor": "Gemeente Almere",
                    },
                    {
                        "page": 8,
                        "section": "De impact in 2029",
                        "anchor": "De impact in 2029: Samen naar resultaat",
                    },
                ],
            },
        },
        "structured_content": {
            "d5": {
                "explicit_reference_present": False,
                "relevance_note": (
                    "No explicit D5 label appears in the Almere plan. The items below are contextual local "
                    "translation signals that align with later D5-style cooperation themes."
                ),
                "items": [
                    {
                        "statement": (
                            "The plan explicitly aims for better cooperation between informal care, the social "
                            "domain, and the medical domain, supported by initiatives such as Voorzorgcirkels, "
                            "Welzijn op Recept, and Samen Sterker in de Wijk."
                        ),
                        "statement_type": "contextual_relevance",
                        "evidence_refs": [
                            {
                                "page": 5,
                                "section": "Veerkrachtige, zorgzame wijken",
                                "anchor": "Betere samenwerking tussen informele zorg, sociaal en medisch domein",
                            },
                            {
                                "page": 5,
                                "section": "Veerkrachtige, zorgzame wijken",
                                "anchor": "Welzijn op Recept",
                            },
                        ],
                    },
                    {
                        "statement": (
                            "The local shift is framed as moving from care afterwards toward health first and the "
                            "right help in the right place."
                        ),
                        "statement_type": "contextual_relevance",
                        "evidence_refs": [
                            {
                                "page": 2,
                                "section": "Waarom is verandering nodig",
                                "anchor": "van zorg achteraf naar gezondheid voorop",
                            },
                            {
                                "page": 2,
                                "section": "Onze bedoeling",
                                "anchor": "De juiste hulp op de juiste plek",
                            },
                        ],
                    },
                ],
            },
            "d6": {
                "explicit_reference_present": False,
                "relevance_note": (
                    "No explicit D6 label appears in the Almere plan. The items below are contextual "
                    "infrastructure signals that align with later D6-style implementation conditions."
                ),
                "items": [
                    {
                        "statement": (
                            "The local plan names RTP Almere, the RSO, data infrastructure, and Monitoring@home as "
                            "part of the operational infrastructure needed for care closer to home."
                        ),
                        "statement_type": "contextual_relevance",
                        "evidence_refs": [
                            {
                                "page": 6,
                                "section": "Zorg dichterbij huis",
                                "anchor": "Regionaal Transferpunt (RTP) Almere",
                            },
                            {
                                "page": 6,
                                "section": "Zorg dichterbij huis",
                                "anchor": "Data-infrastructuur",
                            },
                        ],
                    },
                    {
                        "statement": (
                            "The plan also makes a current shared information picture for professionals part of the "
                            "local enabling structure."
                        ),
                        "statement_type": "contextual_relevance",
                        "evidence_refs": [
                            {
                                "page": 4,
                                "section": "Ambitie",
                                "anchor": "Zorgprofessionals hebben altijd een actueel informatiebeeld van patienten",
                            }
                        ],
                    },
                ],
            },
            "governance_and_finance": {
                "items": [
                    {
                        "statement": (
                            "The governance base is a broad local coalition of Almere municipality, wijkteams, care "
                            "and welfare organizations, and preventive and public-health institutions."
                        ),
                        "evidence_refs": [
                            {
                                "page": 3,
                                "section": "Wie zijn betrokken",
                                "anchor": "Dit is een brede samenwerking tussen",
                            }
                        ],
                    },
                    {
                        "statement": (
                            "The plan does not set a detailed funding framework, but it does describe a target "
                            "future balance in which care expenditures and social-domain expenditures are better "
                            "aligned."
                        ),
                        "statement_type": "contextual_relevance",
                        "evidence_refs": [
                            {
                                "page": 8,
                                "section": "De impact in 2029",
                                "anchor": "Betere balans in zorguitgaven",
                            }
                        ],
                    },
                ]
            },
            "timeline_and_status": {
                "items": [
                    {
                        "statement": (
                            "The local impact horizon is stated explicitly as 2029."
                        ),
                        "evidence_refs": [
                            {
                                "page": 8,
                                "section": "De impact in 2029",
                                "anchor": "De impact in 2029: Samen naar resultaat",
                            }
                        ],
                    },
                    {
                        "statement": (
                            "The plan describes itself as a transformation rather than a standalone project, which "
                            "signals an ongoing implementation status."
                        ),
                        "evidence_refs": [
                            {
                                "page": 3,
                                "section": "Wat vraagt dit van ons",
                                "anchor": "Positief Gezond Almere is geen los project, maar een transformatie",
                            }
                        ],
                    },
                ]
            },
            "monitoring_and_evaluation": {
                "items": [
                    {
                        "statement": (
                            "Monitoring and learning are explicit parts of the local model, including 'Samen leren' "
                            "and 'Monitoren'."
                        ),
                        "evidence_refs": [
                            {
                                "page": 3,
                                "section": "Wat vraagt dit van ons",
                                "anchor": "Samen leren: Successen en inzichten delen",
                            },
                            {
                                "page": 4,
                                "section": "Ambitie",
                                "anchor": "Monitoren",
                            },
                        ],
                    },
                    {
                        "statement": (
                            "The plan also ties those learning and monitoring efforts to the concrete impact goals it "
                            "wants to reach by 2029."
                        ),
                        "evidence_refs": [
                            {
                                "page": 8,
                                "section": "De impact in 2029",
                                "anchor": "De impact in 2029: Samen naar resultaat",
                            }
                        ],
                    },
                ]
            },
            "municipal_translation": {
                "items": [
                    {
                        "statement": (
                            "The plan translates the local agenda into named Almere initiatives such as Voorzorgcirkels, "
                            "Welzijn op Recept, Leefstijlloket, Samen Sterker in de Wijk, and Opgroeien in een "
                            "Kansrijke Omgeving."
                        ),
                        "evidence_refs": [
                            {
                                "page": 5,
                                "section": "Veerkrachtige, zorgzame wijken",
                                "anchor": "Voorzorgcirkels",
                            },
                            {
                                "page": 5,
                                "section": "Veerkrachtige, zorgzame wijken",
                                "anchor": "Opgroeien in een Kansrijke Omgeving",
                            },
                        ],
                    },
                    {
                        "statement": (
                            "The local implementation remains anchored in Almere-specific pressures such as population "
                            "growth, labour-market pressure, and the health of Almeerders."
                        ),
                        "evidence_refs": [
                            {
                                "page": 2,
                                "section": "Waarom is verandering nodig",
                                "anchor": "De vraag naar zorg en ondersteuning neemt toe door de snelle bevolkingsgroei",
                            }
                        ],
                    },
                ]
            },
        },
    },
}


def normalize_ascii(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip().lower()
    text = unicodedata.normalize("NFKD", text)
    return text.encode("ascii", "ignore").decode("ascii")


def collapse_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def build_normalized_index(text: str) -> tuple[str, list[int]]:
    normalized_chars: list[str] = []
    original_index_map: list[int] = []
    for idx, char in enumerate(text):
        piece = unicodedata.normalize("NFKD", char).encode("ascii", "ignore").decode("ascii").lower()
        if not piece:
            continue
        for piece_char in piece:
            normalized_chars.append(piece_char)
            original_index_map.append(idx)
    return "".join(normalized_chars), original_index_map


def load_inventory() -> dict[str, dict]:
    payload = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    return {item["document_id"]: item for item in payload["documents"]}


def load_pages(document_id: str) -> dict[int, str]:
    payload = json.loads((TEXT_DIR / f"{document_id}.json").read_text(encoding="utf-8"))
    pages = payload.get("pages", [])
    return {page["page_number"]: collapse_whitespace(page["text"]) for page in pages}


def excerpt_from_anchor(text: str, anchor: str, radius: int = 220) -> str:
    normalized_text, original_index_map = build_normalized_index(text)
    normalized_anchor = normalize_ascii(anchor)
    match_index = normalized_text.find(normalized_anchor)
    if match_index == -1:
        raise ValueError(f"Anchor not found: {anchor}")

    original_anchor_start = original_index_map[match_index]
    original_anchor_end = original_index_map[match_index + len(normalized_anchor) - 1] + 1
    start = max(0, original_anchor_start - radius)
    end = min(len(text), original_anchor_end + radius)
    excerpt = text[start:end].strip()
    if start > 0:
        excerpt = "... " + excerpt
    if end < len(text):
        excerpt = excerpt + " ..."
    return excerpt


def build_evidence(page_cache: dict[int, str], ref: dict) -> dict:
    page_text = page_cache[ref["page"]]
    return {
        "evidence_quote": excerpt_from_anchor(page_text, ref["anchor"]),
        "page": ref["page"],
        "section": ref["section"],
        "table_id": ref.get("table_id"),
    }


def render_entry(document_id: str, section_slug: str, index: int, spec: dict, page_cache: dict[int, str]) -> dict:
    return {
        "statement_id": f"{document_id}_{section_slug}_{index:03d}",
        "statement_type": spec.get("statement_type", "direct_extraction"),
        "statement": spec["statement"],
        "evidence": [build_evidence(page_cache, ref) for ref in spec["evidence_refs"]],
    }


def build_document_payload(document_id: str, inventory_map: dict[str, dict]) -> dict:
    inventory = inventory_map[document_id]
    page_cache = load_pages(document_id)
    spec = DOCUMENT_SPECS[document_id]

    summary = {}
    for field_name, field_spec in spec["document_level_summary"].items():
        summary_spec = dict(field_spec)
        summary_spec.setdefault("statement_type", "source_grounded_summary")
        summary[field_name] = render_entry(document_id, f"summary_{field_name}", 1, summary_spec, page_cache)

    structured_content = {}
    for section_name, section_spec in spec["structured_content"].items():
        items = [
            render_entry(document_id, section_name, item_index, item_spec, page_cache)
            for item_index, item_spec in enumerate(section_spec.get("items", []), start=1)
        ]
        structured_content[section_name] = {
            "explicit_reference_present": section_spec.get("explicit_reference_present", True),
            "relevance_note": section_spec.get("relevance_note"),
            "items": items,
        }

    return {
        "document_id": document_id,
        "extraction_run_id": EXTRACTION_RUN_ID,
        "generated_on": date.today().isoformat(),
        "metadata": {
            "document_id": inventory["document_id"],
            "title": inventory["title"],
            "publisher": inventory["publisher"],
            "publication_date": inventory["publication_date"],
            "document_type": inventory["document_type"],
            "jurisdiction_level": inventory["jurisdiction_level"],
            "status": inventory["status"],
            "source_url": inventory["source_url"],
            "file_path": inventory["file_path"],
            "source_classification": inventory["source_classification"],
            "curation_bucket": inventory["curation_bucket"],
        },
        "extraction_scope": {
            "contains_d5": inventory["contains_d5"],
            "contains_d6": inventory["contains_d6"],
            "contains_structured_table": inventory["contains_structured_tables"],
            "contains_financial_framework": inventory["contains_financing_logic"],
            "contains_monitoring_framework": inventory["contains_monitoring_evaluation_logic"],
            "contains_municipal_implications": inventory["contains_municipal_implications"],
            "extraction_priority": inventory["extraction_priority"],
            "traceability_mode": inventory["traceability_mode"],
        },
        "document_level_summary": summary,
        "structured_content": structured_content,
        "quality_notes": {
            "extraction_method": "manual_curated_phase3_top5_v1",
            "limitations": [
                "Summary statements are source-grounded syntheses rather than verbatim document sentences.",
                "Where a source does not explicitly use D5/D6 language, related items are marked as contextual_relevance.",
                "Evidence quotes are short excerpts from the page-level extraction text and should be checked against the raw file for final publication use.",
            ],
        },
    }


def main() -> None:
    inventory_map = load_inventory()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for document_id in TOP5_DOCUMENT_IDS:
        payload = build_document_payload(document_id, inventory_map)
        output_path = OUTPUT_DIR / f"{document_id}.json"
        output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote {output_path.relative_to(REPO_ROOT).as_posix()}")


if __name__ == "__main__":
    main()
