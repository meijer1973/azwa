from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
EXTRACTED_DIR = REPO_ROOT / "data" / "extracted"
MUNICIPAL_DIR = EXTRACTED_DIR / "municipal"
D6_GOVERNANCE_PATH = EXTRACTED_DIR / "d6_governance_collaboration.json"
OUTPUT_PATH = MUNICIPAL_DIR / "almere_d6_responsibility_register.json"

DECISION_STATUS_MAP = {
    "source_backed_prefill": "inferred",
    "decision_needed": "unknown",
    "review_needed": "review_needed",
    "settled": "settled",
    "proposed": "proposed",
    "inferred": "inferred",
    "unknown": "unknown",
}


PUBLIC_SOURCE_CANDIDATES = [
    {
        "source_id": "mun_almere_2026_stevige_lokale_teams_raad",
        "title": "Stevige Lokale Teams en inzet Investeringsfonds jeugd en gezin",
        "publisher": "Raad van Almere",
        "source_url": "https://raadvanalmere.nl/article/stevige-lokale-teams-en-inzet-investeringsfonds-jeugd-en-gezin1",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_27",
        "why_it_matters": (
            "Candidate local decision source for one recognizable team per wijk, professionals with mandate, "
            "continuous regie, 2026 start in two wijkteamgebieden, and involvement of JGZ Almere and wijkteams."
        ),
        "intake_action": "Verify council page and Documentwijzer 26006 attachments; ingest selected decision documents.",
    },
    {
        "source_id": "mun_almere_2026_stevige_lokale_teams_geamendeerd_raadsvoorstel",
        "title": "Stevige Lokale Teams en inzet Investeringsfonds jeugd en gezin - geamendeerd raadsvoorstel",
        "publisher": "Raad van Almere",
        "source_url": "https://api.notubiz.nl/document/16660072/2",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "pdf_downloaded_2026_04_27",
        "why_it_matters": "Adopted/amended local council proposal for Stevige Lokale Teams and local decision traceability.",
        "intake_action": "Use for source-backed local decision evidence; do not use it to settle D6 classification without review.",
    },
    {
        "source_id": "mun_almere_2026_stevige_lokale_teams_begrotingswijziging",
        "title": "Stevige Lokale Teams en inzet Investeringsfonds jeugd en gezin - begrotingswijziging",
        "publisher": "Raad van Almere",
        "source_url": "https://api.notubiz.nl/document/16421447/1",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "pdf_downloaded_2026_04_27",
        "why_it_matters": "Local budget-change attachment for the Stevige Lokale Teams council route.",
        "intake_action": "Use for local financing evidence and anti-dubbeltelling review.",
    },
    {
        "source_id": "mun_almere_2026_stevige_lokale_teams_besluitenlijst",
        "title": "Stevige Lokale Teams en inzet Investeringsfonds jeugd en gezin - besluitenlijst",
        "publisher": "Raad van Almere",
        "source_url": "https://api.notubiz.nl/document/16520063/2",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "pdf_downloaded_2026_04_27",
        "why_it_matters": "Decision-list evidence for the Stevige Lokale Teams route.",
        "intake_action": "Use for adoption/voting traceability.",
    },
    {
        "source_id": "mun_almere_wijkteams",
        "title": "Wijkteams Almere",
        "publisher": "Wijkteams Almere / Gemeente Almere",
        "source_url": "https://wijkteams.almere.nl/",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_27",
        "why_it_matters": "Baseline public source for existing local access and wijkteam support structure.",
        "intake_action": "Add as municipal implementation source for D6 access and social infrastructure.",
    },
    {
        "source_id": "nat_vng_richtinggevend_kader_toegang_lokale_teams",
        "title": "Richtinggevend kader: toegang, lokale teams en integrale dienstverlening",
        "publisher": "VNG",
        "source_url": "https://vng.nl/publicaties/richtinggevend-kader-toegang-lokale-teams-en-integrale-dienstverlening",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "pdf_downloaded_2026_04_27",
        "why_it_matters": (
            "National assessment frame for access, local teams and integrated services; useful as benchmark, "
            "not as an Almere decision."
        ),
        "intake_action": "Add as national implementation benchmark and preserve distinction from local decisions.",
    },
    {
        "source_id": "nat_tsd_basisfuncties_lokale_teams",
        "title": "Basisfuncties voor lokale teams",
        "publisher": "Toezicht Sociaal Domein",
        "source_url": "https://www.toezichtsociaaldomein.nl/documenten/2021/10/06/basisfuncties-voor-lokale-teams",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_27",
        "why_it_matters": "Quality and assessment framework for low-threshold, nearby and integrated local teams.",
        "intake_action": "Add as assessment framework for Wijkteams Almere and Stevige Lokale Teams.",
    },
    {
        "source_id": "reg_ggd_flevoland_begroting_2026",
        "title": "Begroting 2026 GGD Flevoland",
        "publisher": "GGD Flevoland",
        "source_url": "https://www.ggdflevoland.nl/app/uploads/sites/6/2025/10/Begroting-2026-GGD-Flevoland.pdf",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "pdf_downloaded_2026_04_27",
        "why_it_matters": (
            "Current public source for GGD governance, JGZ, Kennis en Advies, prevention, finance, "
            "plustaken and GGD-region scale."
        ),
        "intake_action": "Add as regional raw PDF and link to D6 GGD/JGZ/monitoring responsibilities.",
    },
    {
        "source_id": "reg_ggd_flevoland_kennis_en_advies",
        "title": "Kennis en Advies",
        "publisher": "GGD Flevoland",
        "source_url": "https://www.ggdflevoland.nl/professional/kennis-en-advies/",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_27",
        "why_it_matters": "Public source for monitors, dashboards, epidemiology, data analysis and advice.",
        "intake_action": "Add as monitoring and knowledge source.",
    },
    {
        "source_id": "reg_ggd_flevoland_jgz_almere_profile",
        "title": "Profiel Jeugdgezondheidszorg",
        "publisher": "GGD Flevoland",
        "source_url": "https://www.ggdflevoland.nl/professional/jeugdgezondheidszorg/",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_27",
        "why_it_matters": "Public source for JGZ Almere 0-18, school links, youth support and care-chain role.",
        "intake_action": "Add as D6/JGZ implementation evidence.",
    },
    {
        "source_id": "mun_almere_samen_sterker_in_de_wijk_story",
        "title": "Samen Sterker in de Wijk",
        "publisher": "Gemeente Almere",
        "source_url": "https://www.almere.nl/zorg-en-welzijn/wonen-en-zorg/informatie-voor-onze-inwoners/verhalen-over-wonen-en-zorg/zorgvrager-en-zorgdrager/samen-sterker-in-de-wijk",
        "repository_status": "candidate_public_source_not_ingested",
        "verification_status": "search_result_available_but_direct_download_returned_404_2026_04_27",
        "why_it_matters": "Public narrative source for mental-health neighbourhood cooperation and one-plan/steungroep logic.",
        "intake_action": "Add as supporting local implementation source; avoid treating interview text as formal mandate.",
    },
    {
        "source_id": "mun_almere_samenwerkingsprojecten",
        "title": "Samenwerkingsprojecten",
        "publisher": "Gemeente Almere",
        "source_url": "https://www.almere.nl/zorg-en-welzijn/wonen-en-zorg/informatie-voor-onze-partners/samenwerkingsprojecten",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "browser_verified_and_saved_extract_2026_04_27",
        "why_it_matters": "Public source for Samen Sterker in de Wijk partners, pilots, netwerkteams, learning cycle and related local projects.",
        "intake_action": "Add as implementation source for mental-health wijk infrastructure and partner mapping.",
    },
    {
        "source_id": "mun_almere_pga_current_home",
        "title": "Positief Gezond Almere",
        "publisher": "Positief Gezond Almere",
        "source_url": "https://positiefgezondalmere.nl/",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_27",
        "why_it_matters": "Current public PGA source for cooperation themes, healthy neighbourhoods, learning networks and professional information picture.",
        "intake_action": "Use as current implementation context; keep separate from formal PGA transformation-plan evidence.",
    },
    {
        "source_id": "reg_ggd_flevoland_kadernota_2025",
        "title": "Kadernota GGD Flevoland 2025",
        "publisher": "GGD Flevoland",
        "source_url": "https://www.ggdflevoland.nl/app/uploads/sites/6/2024/04/3.2-Kadernota-kern-GGD-2025-v-29mrt2024-gg10042024_.pdf",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "pdf_downloaded_2026_04_30",
        "why_it_matters": "Regional public-authority source for GGD involvement in local GALA plans, Regiobeeld/Regioplan, PGA monitoring and prevention infrastructure.",
        "intake_action": "Use as GGD interface and monitoring/advisory evidence; do not use as final D6 mandate or budget split.",
    },
    {
        "source_id": "reg_flever_zorgzaam_flevoland_project",
        "title": "Zorgzaam Flevoland",
        "publisher": "Flever",
        "source_url": "https://flever.nl/project/zorgzaam-flevoland/",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "Public Flever source distinguishing Zorgzaam Flevoland as regional IZA movement and Flever as resident-perspective support actor.",
        "intake_action": "Use for PGA/Zorgzaam/Flever role splitting; keep formal ownership and mandate open.",
    },
    {
        "source_id": "reg_flever_meerjarenplan_2025_2028",
        "title": "Meerjarenplan Flever 2025-2028",
        "publisher": "Flever",
        "source_url": "https://flever.nl/wp-content/uploads/2025/04/Meerjarenplan-Flever-JvG5-DEF.pdf",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "pdf_downloaded_2026_04_30",
        "why_it_matters": "Flever policy source for support, participation, network and research roles in Flevoland.",
        "intake_action": "Use as supporting role/context evidence below official regional and municipal sources.",
    },
    {
        "source_id": "reg_flever_inwoners_onderdeel_pga",
        "title": "Inwoners onderdeel van Positief Gezond Almere (PGA)",
        "publisher": "Flever",
        "source_url": "https://flever.nl/sterk-met-inwoners/",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "Public source for Flever's project-lead role around inwonerparticipatie within PGA.",
        "intake_action": "Use as narrow Flever-PGA partner-role evidence; do not infer formal D6 coordinator responsibility.",
    },
    {
        "source_id": "reg_noordoostpolder_iza_status_memo_2024",
        "title": "Memo stand van zaken Integraal Zorgakkoord in Flevoland 2024",
        "publisher": "Gemeente Noordoostpolder",
        "source_url": "https://raad.noordoostpolder.nl/Documenten/D05-00-Memo-stand-van-zaken-Integraal-Zorgakkoord-2024.pdf",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "pdf_downloaded_2026_05_11",
        "why_it_matters": "Council memo that names Verbindende Coalitie steering, subregional execution and Netwerkbureau setup/financing.",
        "intake_action": "Use for regional-governance role evidence; keep execution ownership and mandate as validation questions.",
    },
    {
        "source_id": "reg_provincie_flevoland_verbindende_coalitie_2024",
        "title": "Van Zorgtafel naar Verbindende Coalitie Zorgzaam Flevoland",
        "publisher": "Provincie Flevoland",
        "source_url": "https://stateninformatie.flevoland.nl/Documenten/DOCUVITP-3332275-v6-Mededeling-m-b-t-Van-Zorgtafel-naar-Verbindende-Coalitie-Zorgzaam-Flevoland.PDF",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "pdf_downloaded_2026_05_11",
        "why_it_matters": "Provincial memo distinguishing province context, the IZA/AZWA-regio split, Zeewolde exception and the Verbindende Coalitie platform.",
        "intake_action": "Use for scale separation and governance-platform evidence; do not make the province or coalition the mandaatgemeente.",
    },
    {
        "source_id": "reg_zonmw_zorgzaam_flevoland_project",
        "title": "Zorgzaam Flevoland",
        "publisher": "ZonMw",
        "source_url": "https://projecten.zonmw.nl/nl/project/zorgzaam-flevoland",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "html_downloaded_2026_05_11",
        "why_it_matters": "Project page that explicitly names the regional Netwerkbureau, three subregions and PGA as subregion Zuid example.",
        "intake_action": "Use to keep Netwerkbureau visible in top layers; do not settle host, owner or structural funding.",
    },
    {
        "source_id": "nat_dusi_spuk_iza_2023_2026",
        "title": "Specifieke uitkering IZA-doelen 2023-2026",
        "publisher": "Dienst Uitvoering Subsidies aan Instellingen / Ministerie van VWS",
        "source_url": "https://www.dus-i.nl/subsidies/zorg-en-gezondheid/specifieke-uitkering-integraal-zorgakkoord",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "html_downloaded_2026_05_11",
        "why_it_matters": "Official SPUK IZA source for mandate-structure, municipal coordination, mandaathouder and SiSa context.",
        "intake_action": "Use for the financing/mandate route; do not infer local execution ownership.",
    },
    {
        "source_id": "nat_vws_spuk_iza_brede_spuk_mandaatgemeente_2025",
        "title": "Wijziging SPUK IZA en Brede SPUK",
        "publisher": "Ministerie van Volksgezondheid, Welzijn en Sport",
        "source_url": "https://zwolle.bestuurlijkeinformatie.nl/Document/View/73c9ebe8-9347-42f0-9980-15a7f54cdca3",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "pdf_downloaded_2026_05_11",
        "why_it_matters": "Official annex/source for reading 'Flevoland - Almere' as region plus mandaatgemeente, and for SPUK IZA coordination funding context.",
        "intake_action": "Use as mandate/finance evidence; keep 'Flevoland' and 'Almere' as separate fields and actors.",
    },
    {
        "source_id": "reg_centrumregeling_sociaal_domein_flevoland",
        "title": "Centrumregeling Sociaal Domein Flevoland",
        "publisher": "Lokale wet- en regelgeving / Gemeente Almere",
        "source_url": "https://lokaleregelgeving.overheid.nl/CVDR730330/1",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "html_downloaded_2026_05_11",
        "why_it_matters": "Official regulation showing Almere as centrumgemeente for specified social-domain cooperation tasks, separate from IZA/AZWA mandaatgemeente wording.",
        "intake_action": "Use for mandate mechanics and role-split context; do not collapse with province or IZA/AZWA-region definitions.",
    },
    {
        "source_id": "reg_proscoop_zorgzaam_flevoland_netwerkbureau_2024",
        "title": "Drie vloten, een missie: Zorgzaam Flevoland",
        "publisher": "Proscoop",
        "source_url": "https://proscoop.nl/actueel/drie-vloten-een-missie-zorgzaam-flevoland/",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "html_downloaded_2026_05_11",
        "why_it_matters": "Supporting public source for Proscoop coordinator/secretary contribution and Netwerkbureau overview, alignment, learning and connection role.",
        "intake_action": "Use as supporting role evidence; do not infer budget holder or formal owner.",
    },
    {
        "source_id": "reg_ggd_flevoland_bestuursrapportage_aug_2024",
        "title": "GGD Flevoland Bestuursrapportage januari 2024 tot en met augustus 2024",
        "publisher": "GGD Flevoland",
        "source_url": "https://www.ggdflevoland.nl/app/uploads/sites/6/2024/11/Agendabundel-AB-7-november-GGD-Flevoland.pdf",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "pdf_downloaded_2026_05_11",
        "why_it_matters": "GGD board report with advisory/monitoring context around Netwerkbureau Zorgzaam Flevoland.",
        "intake_action": "Use for GGD advisory and monitoring context; do not infer final D6 ownership.",
    },
    {
        "source_id": "mun_almere_gezonde_scholen",
        "title": "Gezonde scholen",
        "publisher": "Gemeente Almere",
        "source_url": "https://www.almere.nl/zorg-en-welzijn/gezond-in-almere/gezonde-scholen",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": (
            "Municipal public page showing Almere-specific school-health support, including the GGD Gezonde "
            "School adviser and referral to central support for children and families around healthy weight."
        ),
        "intake_action": "Use as local implementation evidence; do not use as formal D6 owner or funding decision.",
    },
    {
        "source_id": "mun_almere_gezond_in_almere",
        "title": "Gezond in Almere",
        "publisher": "Gemeente Almere",
        "source_url": "https://www.almere.nl/zorg-en-welzijn/gezond-in-almere",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "Municipal health/prevention gateway that places Gezonde School and mentale gezondheid in the same public context.",
        "intake_action": "Use as context for prevention framing; do not use as a D6 responsibility decision.",
    },
    {
        "source_id": "reg_ggd_flevoland_gezonde_school",
        "title": "De Gezonde School",
        "publisher": "GGD Flevoland",
        "source_url": "https://www.ggdflevoland.nl/professional/scholen-en-kinderopvang/gezonde-school/",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": (
            "Regional public-health source for Gezonde School advisers, school wellbeing, health themes and "
            "GGD support to schools."
        ),
        "intake_action": "Use as GGD-side implementation evidence; keep D6 mandate and funding open.",
    },
    {
        "source_id": "reg_ggd_flevoland_ketenaanpak_gezond_gewicht_almere",
        "title": "Ketenaanpak gezond gewicht - Gezond Gewicht Almere",
        "publisher": "GGD Flevoland",
        "source_url": "https://www.ggdflevoland.nl/professional/gemeenten/ketenaanpak-gezond-gewicht/",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": (
            "Stable public GGD page for Gezond Gewicht Almere, collective prevention, JGZ route and Pact met "
            "impact reference. The referenced PDF remains a candidate if a stable downloadable URL is available."
        ),
        "intake_action": "Use as source-backed prevention/JGZ context; do not use to settle D6 funding.",
    },
    {
        "source_id": "mun_almere_lea_2024_2028",
        "title": "LEA 2024-2028",
        "publisher": "Sociaal Domein Almere / Gemeente Almere",
        "source_url": "https://sociaaldomein.almere.nl/onderwijs/lea-2024-2028",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": (
            "Local education-agenda source for school wellbeing, youth-health/youth-help partner involvement, "
            "joint responsibility and budget-context caveats."
        ),
        "intake_action": "Use as school-wellbeing and governance-context evidence; do not use as D6 classification.",
    },
    {
        "source_id": "nat_zorgakkoorden_pga_20_miljoen_2024",
        "title": "20 miljoen voor transformatieplan Positief Gezond Almere",
        "publisher": "Zorgakkoorden / Ministerie van VWS",
        "source_url": "https://www.zorgakkoorden.nl/actueel/nieuws/Transformatieplan_Positief_Mooi_Almere/",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "Official public confirmation that PGA received IZA funding for concrete care/wellbeing transformation work.",
        "intake_action": "Use as PGA funding/context evidence; do not use as component-level D6 budget allocation.",
    },
    {
        "source_id": "mun_almere_pga_regionaal_transferpunt",
        "title": "Regionaal Transferpunt (RTP) Almere",
        "publisher": "Positief Gezond Almere",
        "source_url": "https://positiefgezondalmere.nl/projecten/regionaal-transferpunt/",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "PGA page describing RTP as a care-coordination project and implementation component.",
        "intake_action": "Use as implementation evidence for operational coordination; keep D6 classification open.",
    },
    {
        "source_id": "reg_flevoziekenhuis_rtp_flevoland_2025",
        "title": "Regionaal Transferpunt Flevoland van start",
        "publisher": "Flevoziekenhuis",
        "source_url": "https://www.flevoziekenhuis.nl/verwijzers/nieuwsoverzicht-verwijzers/2025/01/regionaal-transferpunt-flevoland-van-start/",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "Provider source showing RTP Flevoland is live, its PGA origin and participating care partners.",
        "intake_action": "Use as operational implementation evidence; avoid treating provider implementation as municipal D6 mandate.",
    },
    {
        "source_id": "reg_rtp_flevoland_home",
        "title": "Regionaal Transferpunt Flevoland",
        "publisher": "RTP Flevoland",
        "source_url": "https://rtpflevoland.nl/",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "Live service source for RTP scope, access and operational routing.",
        "intake_action": "Use as current operational evidence; keep owner, mandate and funding open.",
    },
    {
        "source_id": "mun_almere_pga_rso_data_infrastructuur",
        "title": "Regionale Samenwerkingsorganisatie (RSO)",
        "publisher": "Positief Gezond Almere",
        "source_url": "https://positiefgezondalmere.nl/projecten/regionale-samenwerkingsorganisatie-rso/",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "PGA source for RSO, data-infrastructure and shared information workstream.",
        "intake_action": "Use as source-backed digital-exchange prefill; do not settle data-governance roles.",
    },
    {
        "source_id": "reg_flevoziekenhuis_thuismonitoring",
        "title": "Thuismonitoring en het Flevoziekenhuis",
        "publisher": "Flevoziekenhuis",
        "source_url": "https://www.flevoziekenhuis.nl/opname-bezoek/thuismonitoring-en-het-flevoziekenhuis/",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "Provider source showing actual telemonitoring/thuismonitoring practice in Almere.",
        "intake_action": "Use as implementation evidence; validate relation to PGA Monitoring@home before stronger wording.",
    },
    {
        "source_id": "reg_ggd_flevoland_kadernota_2027",
        "title": "Kadernota 2027 GGD Flevoland",
        "publisher": "GGD Flevoland",
        "source_url": "https://www.ggdflevoland.nl/app/uploads/sites/6/2026/01/002025-GGD-Flevo-Kadernota-2026.pdf",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "pdf_downloaded_2026_04_30",
        "why_it_matters": "GGD source for Kennis & Advies, monitoring, data availability and IZA/GALA/AZWA linkage.",
        "intake_action": "Use for monitoring/data capability and GGD scale; do not use as Almere D6 mandate decision.",
    },
    {
        "source_id": "reg_woonzorg_flevoland_beleidsplan_2026",
        "title": "Beleidsplan 2026 Woonzorg Flevoland",
        "publisher": "Woonzorg Flevoland",
        "source_url": "https://woonzorgflevoland.nl/wp-content/uploads/Beleidsplan-2026-Woonzorg-Flevoland_DEF.pdf",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "pdf_downloaded_2026_04_30",
        "why_it_matters": "Provider policy source that corroborates PGA, RSO, care coordination and data-exchange context.",
        "intake_action": "Use as supporting provider evidence; keep governance hierarchy clear.",
    },
    {
        "source_id": "reg_npz_almere_pilot_viewer_acp",
        "title": "Pilot viewer-ACP",
        "publisher": "Netwerk Palliatieve Zorg Almere",
        "source_url": "https://www.npzalmere.nl/pilot-viewer-acp/",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "Public project page for ACP/PZP digital data-sharing pilot in Almere.",
        "intake_action": "Use as concrete use-case evidence; do not generalize to all digital infrastructure.",
    },
    {
        "source_id": "reg_npz_almere_evaluatie_viewer_pzp_acp_2025",
        "title": "Evaluatie viewer PZP/ACP pilot Almere 2024-2025",
        "publisher": "Netwerk Palliatieve Zorg Almere",
        "source_url": "https://www.npzalmere.nl/wp-content/uploads/2025/09/Evaluatie-viewer-PZP-ACP-pilot-Almere-20242025-def.pdf",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "pdf_downloaded_2026_04_30",
        "why_it_matters": "Evaluation source for the ACP/PZP viewer pilot, HINQ technique, stakeholder mandate needs and follow-up requirements.",
        "intake_action": "Use for use-case and review-question sharpening; do not settle platform owner or privacy roles.",
    },
    {
        "source_id": "nat_palliaweb_digitale_initiatieven_pzp",
        "title": "Digitale initiatieven proactieve zorgplanning",
        "publisher": "Palliaweb / PZNL",
        "source_url": "https://palliaweb.nl/initiatieven-proactieve-zorgplanning",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "National overview naming the PGA PZP digital initiative and participating Almere and Flevoland-region organizations.",
        "intake_action": "Use as sector corroboration for the use case; keep local mandate and funding open.",
    },
    {
        "source_id": "reg_npz_almere_jaarplan_2025",
        "title": "Jaarplan 2025 Netwerk Palliatieve Zorg Almere",
        "publisher": "Netwerk Palliatieve Zorg Almere",
        "source_url": "https://www.npzalmere.nl/wp-content/uploads/2025/05/Jaarplan-2025-NPZAlmere-DEF-.pdf",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "pdf_downloaded_2026_04_30",
        "why_it_matters": "Year-plan source for ACP/PZP data exchange goals and evaluation action in Almere.",
        "intake_action": "Use as use-case evidence; the later Jaarverslag 2025 URL found by deep research is deferred because it returned 404 locally.",
    },
    {
        "source_id": "mun_almere_welzijnskader_2020",
        "title": "Welzijnskader: WELzijn in Almere",
        "publisher": "Gemeente Almere",
        "source_url": "https://www.almere.nl/fileadmin/files/almere/bestuur_en_organisatie/beleidsstukken/Beleidsnota_s/Welzijnskader__WELzijn_in_Almere_.pdf",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "pdf_downloaded_2026_04_30",
        "why_it_matters": "Municipal policy frame for social base, meeting places, volunteer support and mantelzorg.",
        "intake_action": "Use for public-source prefill; keep live inventory and D6 classification open.",
    },
    {
        "source_id": "mun_almere_subsidie_buurtontmoeting",
        "title": "Financiele ondersteuning voor (buurt)ontmoeting",
        "publisher": "Gemeente Almere",
        "source_url": "https://www.almere.nl/subsidies/financiele-ondersteuning-voor-buurtontmoeting",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "Current municipal subsidy route for neighbourhood meeting places and activities.",
        "intake_action": "Use as public evidence for support route and funding questions, not formal D6 classification.",
    },
    {
        "source_id": "mun_almere_nadere_regels_buurtontmoeting",
        "title": "Nadere regels (buurt)ontmoetingsplekken en -activiteiten",
        "publisher": "Gemeente Almere",
        "source_url": "https://www.almere.nl/subsidies/soorten-subsidies/nadere-regels-buurtontmoetingsplekken-en-activiteiten",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "Municipal rules for resident-led neighbourhood meeting places, activities, criteria and cofinancing.",
        "intake_action": "Use for subsidy criteria and double-funding controls; do not infer D6 owner.",
    },
    {
        "source_id": "mun_almere_wijkbudget",
        "title": "Wijkbudget",
        "publisher": "Gemeente Almere",
        "source_url": "https://www.almere.nl/subsidies/wijkbudget",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "Municipal funding route for resident ideas and activities for other residents.",
        "intake_action": "Use for citizen-initiative prefill and finance-gap review.",
    },
    {
        "source_id": "mun_almere_ondersteuning_mantelzorg",
        "title": "Ondersteuning voor mantelzorg",
        "publisher": "Gemeente Almere",
        "source_url": "https://www.almere.nl/zorg-en-welzijn/mantelzorg/ondersteuning-voor-mantelzorg",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "Municipal service source for Wmo and VMCA routes for mantelzorg support.",
        "intake_action": "Use as informal-care support evidence; keep final D6 grouping open.",
    },
    {
        "source_id": "mun_almere_mantelzorgwaardering",
        "title": "Mantelzorgwaardering",
        "publisher": "Gemeente Almere",
        "source_url": "https://www.almere.nl/zorg-en-welzijn/mantelzorg/mantelzorgwaardering",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "Municipal source for mantelzorgwaardering, VMCA advice and support route.",
        "intake_action": "Use for actor and finance mapping; do not turn into D6 ownership.",
    },
    {
        "source_id": "mun_almere_sociaal_domein_aanbod_jeugd_gezin",
        "title": "Aanbod jeugd en gezin",
        "publisher": "Sociaal Domein Almere / Gemeente Almere",
        "source_url": "https://sociaaldomein.almere.nl/preventie-voor-jeugd-en-gezin/aanbod-jeugd-en-gezin",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "Official preventive-offer page using Sociale Kaart Flevoland and annual GGD information checks.",
        "intake_action": "Use as referral/inventory evidence; do not treat as complete D6 register.",
    },
    {
        "source_id": "mun_almere_sociale_veerkracht_almeerders",
        "title": "Sociale veerkracht van Almeerders",
        "publisher": "Gemeente Almere / Movisie / Platform31 / Verwey-Jonker Instituut",
        "source_url": "https://www.almere.nl/zorg-en-welzijn/sociale-staat-van-almere/sociale-veerkracht-van-almeerders",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "Municipal-commissioned advice on social resilience, social base, meeting places and volunteers.",
        "intake_action": "Use for context and gap framing; validate before using as implementation commitment.",
    },
    {
        "source_id": "mun_deschoor_buurtkamers",
        "title": "Buurtkamers",
        "publisher": "De Schoor",
        "source_url": "https://www.deschoor.nl/buurtkamers",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "Partner implementation source for named buurtkamers and low-threshold meeting functions.",
        "intake_action": "Use as live inventory evidence; keep municipal mandate and funding open.",
    },
    {
        "source_id": "mun_deschoor_initiatievenbureau",
        "title": "Initiatievenbureau",
        "publisher": "De Schoor",
        "source_url": "https://www.deschoor.nl/initiatievenbureau",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "Partner source for helping residents translate ideas into activities through buurtcentra.",
        "intake_action": "Use for partner mapping; do not infer final D6 owner.",
    },
    {
        "source_id": "mun_deschoor_buurtkracht",
        "title": "Buurtkracht",
        "publisher": "De Schoor",
        "source_url": "https://www.deschoor.nl/buurtkracht",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "Partner source for resident initiatives, neighbourhood activation and collective activity.",
        "intake_action": "Use for citizen-initiative prefill; keep formal classification open.",
    },
    {
        "source_id": "mun_deschoor_opbouwwerk_almere",
        "title": "Opbouwwerk in Almere",
        "publisher": "De Schoor",
        "source_url": "https://www.deschoor.nl/opbouwwerkalmere",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "Partner source for opbouwwerk, wijkteams connection and resident initiatives.",
        "intake_action": "Use for implementation detail and partner mapping; keep governance owner open.",
    },
    {
        "source_id": "mun_vmca_meerjarenvisie_2022_2025",
        "title": "Meerjarenvisie 2022-2025",
        "publisher": "Vrijwilligers en Mantelzorg Centrale Almere",
        "source_url": "https://www.vmca.nl/uploads/content/file/www.vmca.nl/meerjarenvisie-vmca-2022-2025.pdf",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "pdf_downloaded_2026_04_30",
        "why_it_matters": "Partner policy plan for volunteer work, mantelzorg and contribution to wijkteams.",
        "intake_action": "Use as partner role evidence; do not use as municipal D6 mandate.",
    },
    {
        "source_id": "mun_humanitas_almere",
        "title": "Humanitas Almere",
        "publisher": "Humanitas",
        "source_url": "https://www.humanitas.nl/afdeling/almere/",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "Supporting source for local volunteer-backed support themes.",
        "intake_action": "Use as lower-priority partner mapping evidence.",
    },
    {
        "source_id": "mun_almere_almeers_preventieakkoord",
        "title": "Almeers Preventieakkoord",
        "publisher": "Gemeente Almere",
        "source_url": "https://www.almere.nl/zorg-en-welzijn/almeers-preventieakkoord",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "Municipal prevention-network source for initiatives, network support and mental wellbeing.",
        "intake_action": "Use as bridge/context evidence; do not conflate prevention-network role with D6 owner.",
    },
    {
        "source_id": "mun_almere_wijkteams_ontmoeting",
        "title": "Ontmoeting",
        "publisher": "Wijkteams Almere / Gemeente Almere",
        "source_url": "https://wijkteams.almere.nl/ontmoeting",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_04_30",
        "why_it_matters": "Current wijkteam source for coffee moments, social contact and links to VMCA, Humanitas and De Schoor.",
        "intake_action": "Use as local access/social-base evidence; keep D6 classification open.",
    },
    {
        "source_id": "reg_almere_zorglandschap_wmo",
        "title": "Zorglandschap Wmo",
        "publisher": "Regio Almere",
        "source_url": "https://regio.almere.nl/zorglandschap-wmo",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_05_01",
        "why_it_matters": "Regional public page for Zorglandschap Wmo and mental-health support landscape around Almere.",
        "intake_action": "Use as regional programme context for Samen Sterker; keep formal D6 ownership open.",
    },
    {
        "source_id": "reg_zorglandschap_wmo_uitvoeringsprogramma_2022",
        "title": "Uitvoeringsprogramma Zorglandschap Wmo Flevoland 2022",
        "publisher": "Zorglandschap Wmo Flevoland",
        "source_url": "https://sociaaldomeinflevoland.nl/sites/default/files/documents/Uitvoeringsprogramma%20Zorglandschap%20Wmo%20%282%29.pdf",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "pdf_downloaded_2026_05_01",
        "why_it_matters": "Regional implementation programme source for Samen Sterker start, method, partners and expansion.",
        "intake_action": "Use as implementation evidence; do not treat it as D6 mandate or structural funding proof.",
    },
    {
        "source_id": "reg_zorglandschap_wmo_monitor_2025",
        "title": "Monitor Zorglandschap Wmo 2025",
        "publisher": "Regio Flevoland / Gemeente Lelystad",
        "source_url": "https://lelystad.bestuurlijkeinformatie.nl/Document/View/e42037b5-60d3-43bf-b89a-1c3f36028809",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "pdf_downloaded_2026_05_01",
        "why_it_matters": "Current regional monitor source for Samen Sterker and cross-domain work between wijk social domain and curative care.",
        "intake_action": "Use for current implementation and monitoring context; keep ownership and accepted steering conclusions open.",
    },
    {
        "source_id": "reg_zonmw_samen_sterker_uitvoeringsplan",
        "title": "Uitvoeringsplan: Samen Sterker in de Wijk in Flevoland",
        "publisher": "ZonMw",
        "source_url": "https://projecten.zonmw.nl/nl/project/uitvoeringsplan-samen-sterker-de-wijk-flevolandmentale-veerkracht-de-wijk",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_05_01",
        "why_it_matters": "ZonMw implementation-subsidy page for programme timing and funder context.",
        "intake_action": "Use as programme/timeline evidence only; do not infer local governance settlement.",
    },
    {
        "source_id": "reg_zonmw_samen_sterker_startsubsidie",
        "title": "Samen sterker in de wijk",
        "publisher": "ZonMw",
        "source_url": "https://projecten.zonmw.nl/nl/project/samen-sterker-de-wijk",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_05_01",
        "why_it_matters": "ZonMw start-subsidy page for historical programme context and public funder trace.",
        "intake_action": "Use as historical programme evidence; keep current D6 classification open.",
    },
    {
        "source_id": "mun_almere_pga_samen_sterker_wijk",
        "title": "Samen Sterker in de Wijk: mentale veerkracht in Almere",
        "publisher": "Positief Gezond Almere",
        "source_url": "https://positiefgezondalmere.nl/projecten/samen-sterker-in-de-wijk/",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_05_01",
        "why_it_matters": "Row-specific PGA project page for Samen Sterker in de Wijk in Almere.",
        "intake_action": "Use as project-context evidence; do not treat PGA context as formal D6 ownership.",
    },
    {
        "source_id": "mun_almere_subsidieregister_2023",
        "title": "Subsidieregister 2023",
        "publisher": "Gemeente Almere",
        "source_url": "https://www.almere.nl/subsidies/subsidieregister/subsidieregister-2023",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_05_01",
        "why_it_matters": "Municipal funding trace that may point to project or partner funding around Samen Sterker.",
        "intake_action": "Use as funding trace only; do not infer structural D6 funding.",
    },
    {
        "source_id": "mun_almere_evaluatie_schakelteams_2021",
        "title": "Evaluatie schakelteams",
        "publisher": "Gemeente Almere Onderzoek & Statistiek",
        "source_url": "https://oens.almere.nl/fileadmin/files/sites/OenS/2022/Evaluatie_schakelteams.pdf",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "pdf_downloaded_2026_05_01",
        "why_it_matters": "Municipal evaluation source for adjacent mental-health/wijkteam interface history.",
        "intake_action": "Use as historical interface evidence; validate relation to current Samen Sterker governance.",
    },
    {
        "source_id": "reg_samen_sterker_in_de_wijk_home",
        "title": "Samen Sterker in de Wijk",
        "publisher": "Samen Sterker in de Wijk",
        "source_url": "https://www.ssidw.nl/",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_05_01",
        "why_it_matters": "Current project-owned public page for programme framing and public-facing description.",
        "intake_action": "Use as lower-authority current project evidence; prefer municipal/regional/ZonMw sources for stronger claims.",
    },
    {
        "source_id": "mun_almere_subsidieregister_2024",
        "title": "Subsidieregister 2024",
        "publisher": "Gemeente Almere",
        "source_url": "https://www.almere.nl/subsidies/subsidieregister/subsidieregister-2024",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_05_01",
        "why_it_matters": "Municipal subsidy register for GGD, JGZ, Wijkteams and social-base funding traces.",
        "intake_action": "Use as funding-context evidence only; do not infer D6 budget allocation.",
    },
    {
        "source_id": "mun_almere_subsidieregister_2025",
        "title": "Subsidieregister 2025",
        "publisher": "Gemeente Almere",
        "source_url": "https://www.almere.nl/subsidies/subsidieregister/subsidieregister-2025",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_05_01",
        "why_it_matters": "Municipal subsidy register for current GGD/JGZ/SLT-related and partner funding traces.",
        "intake_action": "Use as funding-context evidence only; require finance/controller validation for component splits.",
    },
    {
        "source_id": "mun_almere_mentale_gezondheid",
        "title": "Mentale gezondheid",
        "publisher": "Gemeente Almere",
        "source_url": "https://www.almere.nl/zorg-en-welzijn/gezond-in-almere/mentale-gezondheid",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_05_01",
        "why_it_matters": "Municipal implementation context for youth mental health and prevention.",
        "intake_action": "Use as local prevention context; do not infer D6 classification, owner or funding.",
    },
    {
        "source_id": "reg_ggd_flevoland_voortgang_gala_regio_2023",
        "title": "Voortgang GALA in de regio",
        "publisher": "GGD Flevoland",
        "source_url": "https://www.ggdflevoland.nl/app/uploads/sites/6/2023/07/4.-Oplegnotitie-voortgang-GALA-in-de-regio.pdf",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "pdf_downloaded_2026_05_01",
        "why_it_matters": "GGD/BOSD governance context for regional GALA/IZA progress and GGD advisory role.",
        "intake_action": "Use as regional governance context; do not treat it as Almere D6 row mandate.",
    },
    {
        "source_id": "nat_zorgakkoorden_werkagenda_handvatten_2026",
        "title": "Handvatten voor het opstellen van de regionale werkagenda",
        "publisher": "Zorgakkoorden / Ministerie van VWS",
        "source_url": "https://www.zorgakkoorden.nl/programmas/aanvullend-zorg-en-welzijnsakkoord/handvatten-voor-het-opstellen-van-de-regionale-werkagenda/",
        "repository_status": "ingested_formal_corpus",
        "verification_status": "downloaded_2026_05_01",
        "why_it_matters": "Canonical national process source for regional workagenda governance and deadlines.",
        "intake_action": "Use for workagenda process hierarchy; do not use as proof of Almere adoption.",
    },
]


COMPONENTS = [
    {
        "component_id": "inloopvoorzieningen_sociaal_en_gezond",
        "component_label": "Inloopvoorzieningen sociaal en gezond",
        "existing_almere_provision": (
            "Public sources now show municipal subsidy routes for buurtontmoeting, wijkteam ontmoeting pages, "
            "De Schoor buurtkamers and broader social-base policy/advice context."
        ),
        "required_upgrade": (
            "Validate which specific inloop, buurtkamer, buurtcentrum and wijkteam access points count as formal "
            "D6 infrastructure and which remain adjacent social-base provision."
        ),
        "owner": "Gemeente Almere and social-base partner roles need validation",
        "executors": ["wijkteams candidate", "De Schoor candidate", "resident-led meeting-place initiatives"],
        "cooperation_partners": ["social work", "GGD/JGZ", "citizen initiatives", "informal support", "VMCA", "Humanitas"],
        "scale": "almere_local_needs_validation",
        "funding_sources": ["municipal_subsidy_routes_candidate", "wijkbudget_candidate", "unknown_needs_decision"],
        "decision_status": "source_backed_prefill",
        "evidence_sources": [
            "mun_almere_welzijnskader_2020",
            "mun_almere_subsidie_buurtontmoeting",
            "mun_almere_nadere_regels_buurtontmoeting",
            "mun_almere_wijkteams_ontmoeting",
            "mun_deschoor_buurtkamers",
            "mun_deschoor_initiatievenbureau",
            "mun_almere_sociale_veerkracht_almeerders",
        ],
        "confidence": "medium",
        "open_issue": "Public evidence is stronger, but formal D6 classification, exact local inventory, owner, mandate and funding split remain validation questions.",
    },
    {
        "component_id": "wijkteams_almere",
        "component_label": "Wijkteams Almere",
        "existing_almere_provision": "Public page confirms wijkteams as local support route with wijkwerkers from diverse care and welfare organizations.",
        "required_upgrade": "Map governance, mandate, partners, wijk coverage, relation to D6 and relation to Stevige Lokale Teams.",
        "owner": "Gemeente Almere needs confirmation",
        "executors": ["wijkwerkers", "care and welfare organizations represented in wijkteams"],
        "cooperation_partners": ["Gemeente Almere", "zorg- en welzijnsorganisaties"],
        "scale": "almere_local",
        "funding_sources": ["unknown_needs_decision"],
        "decision_status": "source_backed_prefill",
        "evidence_sources": ["mun_almere_wijkteams"],
        "confidence": "medium",
        "open_issue": "Baseline function is public, but formal D6 classification and responsibility allocation remain unsettled.",
    },
    {
        "component_id": "stevige_lokale_teams",
        "component_label": "Stevige Lokale Teams",
        "existing_almere_provision": "Council page and Documentwijzer attachments give local decision evidence for a 2026 start in two wijkteamgebieden and involvement of JGZ Almere and wijkteams.",
        "required_upgrade": "Review the amended proposal, budget change and decision list before marking exact owner, executor and D6 classification as settled.",
        "owner": "Almere council/college line needs source-passage confirmation",
        "executors": ["JGZ Almere", "wijkteams", "schools and childcare partners"],
        "cooperation_partners": ["social and pedagogical basis", "specialists", "schools", "childcare", "JGZ Almere", "wijkteams"],
        "scale": "almere_local",
        "funding_sources": ["Investeringsfonds Jeugd en Gezin candidate", "unknown_needs_source_confirmation"],
        "decision_status": "source_backed_prefill",
        "evidence_sources": [
            "mun_almere_2026_stevige_lokale_teams_raad",
            "mun_almere_2026_stevige_lokale_teams_geamendeerd_raadsvoorstel",
            "mun_almere_2026_stevige_lokale_teams_begrotingswijziging",
            "mun_almere_2026_stevige_lokale_teams_besluitenlijst",
        ],
        "confidence": "medium",
        "open_issue": "Decision documents are now ingested; formal D6 classification, exact execution ownership and budget allocation still need local validation.",
    },
    {
        "component_id": "jgz_almere",
        "component_label": "JGZ Almere",
        "existing_almere_provision": (
            "GGD Flevoland public profile describes JGZ Almere as 0-18 jeugdgezondheidszorg with broader local "
            "configuration; Gezonde School and LEA sources add school/prevention context."
        ),
        "required_upgrade": "Validate which JGZ school, SLT, Kansrijke Start, mental-health prevention and local-team roles are D6-specific.",
        "owner": "JGZ Almere / GGD Flevoland, municipal governance needs confirmation",
        "executors": ["JGZ Almere"],
        "cooperation_partners": ["schools", "huisartsen", "Passend Onderwijs", "wijkteams", "jeugdhulp"],
        "scale": "almere_local_with_ggd_flevoland_governance",
        "funding_sources": ["GGD/JGZ funding needs source-specific split"],
        "decision_status": "source_backed_prefill",
        "evidence_sources": [
            "reg_ggd_flevoland_jgz_almere_profile",
            "reg_ggd_flevoland_begroting_2026",
            "reg_ggd_flevoland_gezonde_school",
            "reg_ggd_flevoland_ketenaanpak_gezond_gewicht_almere",
            "mun_almere_lea_2024_2028",
            "mun_almere_subsidieregister_2024",
            "mun_almere_subsidieregister_2025",
        ],
        "confidence": "medium",
        "open_issue": "Operational role is public, but exact D6 ownership and budget status need local validation.",
    },
    {
        "component_id": "ggd_flevoland_coordination",
        "component_label": "GGD Flevoland-coordinatie",
        "existing_almere_provision": "GGD Begroting 2026 is a candidate source for governance, public health, prevention and municipal contribution context.",
        "required_upgrade": "Ingest the 2026 budget and connect relevant sections to D6 governance, JGZ, Gezond Leven and monitoring.",
        "owner": "GGD Flevoland under six-municipality governance",
        "executors": ["GGD Flevoland"],
        "cooperation_partners": ["Flevoland municipalities", "Zorgzaam Flevoland/PGA", "public-health and prevention partners"],
        "scale": "ggd_regio_flevoland",
        "funding_sources": ["inwonerbijdrage", "municipal subsidies/plustaken", "other source-specific funding"],
        "decision_status": "source_backed_prefill",
        "evidence_sources": [
            "reg_ggd_flevoland_begroting_2026",
            "reg_ggd_flevoland_kadernota_2025",
            "reg_ggd_flevoland_voortgang_gala_regio_2023",
            "mun_almere_subsidieregister_2024",
            "mun_almere_subsidieregister_2025",
        ],
        "confidence": "medium",
        "open_issue": "Separate GGD-region tasks from IZA/AZWA-region and Almere-local execution.",
    },
    {
        "component_id": "gezonde_school_mentale_gezonde_school",
        "component_label": "Gezonde School / mentale gezonde school",
        "existing_almere_provision": (
            "Municipal and GGD public pages now show Almere-specific Gezonde School support, GGD Gezonde "
            "School advisers, school wellbeing/prevention context and JGZ/LEA partner links."
        ),
        "required_upgrade": (
            "Validate whether this is formal D6 infrastructure, adjacent school-prevention infrastructure or "
            "candidate infrastructure, and confirm owner, coordinator, mandate and funding."
        ),
        "owner": None,
        "executors": ["GGD Gezonde School advisers candidate", "schools candidate", "JGZ Almere candidate"],
        "cooperation_partners": ["schools", "GGD Flevoland", "JGZ Almere", "Gemeente Almere", "youth partners"],
        "scale": "almere_local_or_ggd_regio_needs_validation",
        "funding_sources": ["unknown_needs_decision"],
        "decision_status": "source_backed_prefill",
        "evidence_sources": [
            "mun_almere_gezonde_scholen",
            "mun_almere_gezond_in_almere",
            "reg_ggd_flevoland_gezonde_school",
            "reg_ggd_flevoland_ketenaanpak_gezond_gewicht_almere",
            "mun_almere_lea_2024_2028",
            "reg_ggd_flevoland_jgz_almere_profile",
            "reg_ggd_flevoland_begroting_2026",
            "mun_almere_mentale_gezondheid",
        ],
        "confidence": "medium",
        "open_issue": (
            "Public evidence is stronger, but formal D6 classification, accountable owner, mandate, scale and "
            "component-level funding remain local validation questions."
        ),
    },
    {
        "component_id": "kennis_advies_monitoring_dashboards",
        "component_label": "Kennis & Advies / monitoring / dashboards",
        "existing_almere_provision": "GGD Kennis en Advies page describes monitors, dashboards, epidemiology, data analysis and advice.",
        "required_upgrade": "Map which dashboards and monitors are used for D6 workagenda steering and who owns reporting.",
        "owner": "GGD Flevoland candidate, decision owner needs confirmation",
        "executors": ["GGD Flevoland Kennis en Advies"],
        "cooperation_partners": ["municipality", "regional programme structures", "knowledge institutions"],
        "scale": "ggd_regio_flevoland_with_almere_use",
        "funding_sources": ["unknown_needs_source_specific_split"],
        "decision_status": "source_backed_prefill",
        "evidence_sources": [
            "reg_ggd_flevoland_kennis_en_advies",
            "reg_ggd_flevoland_begroting_2026",
            "reg_ggd_flevoland_kadernota_2025",
            "reg_ggd_flevoland_voortgang_gala_regio_2023",
        ],
        "confidence": "medium",
        "open_issue": "Public monitoring function is clear; D6-specific steering arrangement is not yet settled.",
    },
    {
        "component_id": "samen_sterker_wijk_mental_health",
        "component_label": "Samen Sterker in de Wijk / mentale-gezondheidswijkinfrastructuur",
        "existing_almere_provision": (
            "Public sources now give a stronger implementation picture for Samen Sterker in de Wijk: municipal "
            "partner material, Zorglandschap Wmo programme and monitor sources, ZonMw project pages, a PGA project "
            "page, a municipal subsidy trace, adjacent schakelteams evaluation context and the current project site."
        ),
        "required_upgrade": (
            "Validate whether Samen Sterker is formal D6 infrastructure, adjacent PGA/mental-health/neighbourhood "
            "implementation, or supporting evidence; confirm owner/coordinator, citywide or pilot status, mandate, "
            "structural funding, formal SLT relation and accepted evaluation steering."
        ),
        "owner": "shared responsibility needs validation",
        "executors": [
            "Zorgplatform Flevoland partners",
            "GGZ Centraal candidate",
            "GGD Flevoland candidate",
            "Zorggroep Almere candidate",
            "Triade Vitree candidate",
            "Kwintes candidate",
            "Leger des Heils candidate",
            "local professionals and ervaringsdeskundigen",
        ],
        "cooperation_partners": [
            "Triade Vitree",
            "GGZ Centraal",
            "Amethist",
            "Kwintes",
            "Leger des Heils",
            "GGD Flevoland",
            "Zorggroep Almere",
            "Zilveren Kruis",
            "Gemeente Almere",
            "PGA",
            "Zorgplatform Flevoland",
        ],
        "scale": "almere_local_and_regional_project_scale",
        "funding_sources": ["municipal_subsidy_trace_2023", "PGA/IZA context", "unknown_needs_decision"],
        "decision_status": "source_backed_prefill",
        "evidence_sources": [
            "mun_almere_samenwerkingsprojecten",
            "reg_almere_zorglandschap_wmo",
            "reg_zorglandschap_wmo_uitvoeringsprogramma_2022",
            "reg_zorglandschap_wmo_monitor_2025",
            "reg_zonmw_samen_sterker_uitvoeringsplan",
            "reg_zonmw_samen_sterker_startsubsidie",
            "mun_almere_pga_samen_sterker_wijk",
            "mun_almere_pga_seo_businesscase_2024",
            "nat_zorgakkoorden_pga_20_miljoen_2024",
            "mun_almere_subsidieregister_2023",
            "mun_almere_evaluatie_schakelteams_2021",
            "reg_samen_sterker_in_de_wijk_home",
        ],
        "confidence": "medium",
        "open_issue": (
            "Public evidence is stronger, but formal D6 classification, final owner/coordinator, mandate, structural "
            "or component-level funding, SLT relation and accepted evaluation steering remain validation questions."
        ),
    },
    {
        "component_id": "pga_zorgzaam_flevoland_interface",
        "component_label": "Positief Gezond Almere / Zorgzaam Flevoland-interface",
        "existing_almere_provision": (
            "Public sources now support a stricter role split: PGA as local transformation programme with an approved "
            "IZA plan; IZA/AZWA-regio Flevoland as a regional route, not the province; Gemeente Almere as "
            "mandaatgemeente for the Flevoland SPUK/IZA route; Verbindende Coalitie Zorgzaam Flevoland as regional "
            "steering forum; Netwerkbureau Zorgzaam Flevoland as support bureau; Flever as resident-participation "
            "and connecting actor; and GGD Flevoland as monitoring/advisory partner."
        ),
        "required_upgrade": (
            "Validate whether these structures are formal D6 infrastructure, adjacent programme infrastructure or "
            "implementation support, separate PGA transformation funding from D5/D6/AZWA and regular budgets, and "
            "avoid treating 'Flevoland - Almere' or slash shorthand as a combined actor."
        ),
        "owner": "shared programme and regional roles need validation",
        "executors": [
            "PGA programme candidate",
            "Verbindende Coalitie steering-forum candidate",
            "Netwerkbureau support-bureau candidate",
            "Zorgzaam Flevoland regional movement candidate",
            "Flever participation-support candidate",
            "GGD Flevoland monitoring/advice candidate",
        ],
        "cooperation_partners": [
            "Gemeente Almere",
            "PGA partners",
            "Verbindende Coalitie Zorgzaam Flevoland",
            "Netwerkbureau Zorgzaam Flevoland",
            "Zorgzaam Flevoland",
            "Flever",
            "GGD Flevoland",
            "care and welfare partners",
        ],
        "scale": "almere_local_and_iza_azwa_regio_flevoland",
        "funding_sources": ["IZA/PGA transformation funding context", "GALA/SPUK prevention and knowledge context", "AZWA/D5/D6 funding needs separation"],
        "decision_status": "source_backed_prefill",
        "evidence_sources": [
            "mun_almere_pga_transformatieplan",
            "mun_almere_pga_current_home",
            "nat_zorgakkoorden_pga_20_miljoen_2024",
            "reg_flevoland_2023_regioplan_iza",
            "reg_zonmw_doorontwikkeling_zorgzaam_flevoland",
            "reg_ggd_flevoland_kadernota_2025",
            "reg_ggd_flevoland_begroting_2026",
            "reg_ggd_flevoland_voortgang_gala_regio_2023",
            "reg_flever_zorgzaam_flevoland_project",
            "reg_flever_meerjarenplan_2025_2028",
            "reg_flever_inwoners_onderdeel_pga",
            "reg_noordoostpolder_iza_status_memo_2024",
            "reg_provincie_flevoland_verbindende_coalitie_2024",
            "reg_zonmw_zorgzaam_flevoland_project",
            "nat_dusi_spuk_iza_2023_2026",
            "nat_vws_spuk_iza_brede_spuk_mandaatgemeente_2025",
            "reg_centrumregeling_sociaal_domein_flevoland",
            "reg_proscoop_zorgzaam_flevoland_netwerkbureau_2024",
            "reg_ggd_flevoland_bestuursrapportage_aug_2024",
        ],
        "confidence": "medium",
        "open_issue": (
            "Public evidence is stronger and now names Verbindende Coalitie and Netwerkbureau, but formal D6 "
            "classification, final owner/coordinator, host, mandate, continuity after current funding and "
            "component-level budget split remain validation questions."
        ),
    },
    {
        "component_id": "digital_operational_infrastructure",
        "component_label": "Digitale en operationele infrastructuur",
        "existing_almere_provision": (
            "Public sources now show separate but related components: RTP Flevoland and Almere-specific PGA context for care coordination, "
            "PGA RSO/data-infrastructure work, Flevoziekenhuis thuismonitoring, GGD monitoring/data capability and "
            "ACP/PZP digital data-sharing pilots."
        ),
        "required_upgrade": (
            "Split or validate the subcomponents before drafting: digital exchange/data platform, operational transfer "
            "and care coordination, remote monitoring/telemonitoring, and public-health/dashboard/knowledge capability."
        ),
        "owner": "mixed owner candidates; formal D6 owner needs validation",
        "executors": [
            "RTP Flevoland candidate",
            "Flevoziekenhuis candidate",
            "PGA/RSO workstream candidate",
            "GGD Flevoland candidate",
            "NPZ Almere/PZP pilot partners candidate",
        ],
        "cooperation_partners": [
            "Gemeente Almere",
            "Flevoziekenhuis",
            "Woonzorg Flevoland",
            "Zorggroep Almere",
            "GGD Flevoland",
            "ReHA",
            "PGA partners",
            "Zilveren Kruis",
            "Netwerk Palliatieve Zorg Almere",
        ],
        "scale": "programme_or_project_scale_needs_validation",
        "funding_sources": ["unknown_needs_decision"],
        "decision_status": "source_backed_prefill",
        "evidence_sources": [
            "reg_flevoland_2023_regioplan_iza",
            "mun_almere_pga_transformatieplan",
            "mun_almere_pga_current_home",
            "nat_zorgakkoorden_pga_20_miljoen_2024",
            "mun_almere_pga_regionaal_transferpunt",
            "reg_flevoziekenhuis_rtp_flevoland_2025",
            "reg_rtp_flevoland_home",
            "mun_almere_pga_rso_data_infrastructuur",
            "reg_flevoziekenhuis_thuismonitoring",
            "reg_ggd_flevoland_begroting_2026",
            "reg_ggd_flevoland_kadernota_2027",
            "reg_ggd_flevoland_kennis_en_advies",
            "reg_woonzorg_flevoland_beleidsplan_2026",
            "reg_npz_almere_pilot_viewer_acp",
            "reg_npz_almere_evaluatie_viewer_pzp_acp_2025",
            "nat_palliaweb_digitale_initiatieven_pzp",
            "reg_npz_almere_jaarplan_2025",
        ],
        "confidence": "medium",
        "open_issue": (
            "Public evidence is stronger, but formal D6 classification, single owner, data-governance mandate, "
            "privacy/security accountability, component split and structural funding remain validation questions."
        ),
    },
    {
        "component_id": "citizen_initiatives_informal_support",
        "component_label": "Burgerinitiatieven en informele steun",
        "existing_almere_provision": (
            "Public sources show wijkbudget, resident-led neighbourhood meeting support, De Schoor Buurtkracht/"
            "opbouwwerk, VMCA volunteer and mantelzorg support, Humanitas Almere and preventive-network context."
        ),
        "required_upgrade": (
            "Split subsidy instruments, partner-run informal support, resident initiatives and prevention-network "
            "activity before using this row for work-agenda wording."
        ),
        "owner": "mixed public actors; final coordination owner needs validation",
        "executors": ["resident initiatives candidate", "VMCA candidate", "De Schoor candidate", "Humanitas candidate"],
        "cooperation_partners": ["social work", "VMCA", "De Schoor", "Humanitas", "wijkteams", "neighbourhood networks"],
        "scale": "almere_local",
        "funding_sources": ["wijkbudget_candidate", "municipal_social_base_subsidies_candidate", "unknown_needs_decision"],
        "decision_status": "source_backed_prefill",
        "evidence_sources": [
            "mun_almere_wijkbudget",
            "mun_almere_ondersteuning_mantelzorg",
            "mun_almere_mantelzorgwaardering",
            "mun_almere_sociaal_domein_aanbod_jeugd_gezin",
            "mun_deschoor_buurtkracht",
            "mun_deschoor_opbouwwerk_almere",
            "mun_vmca_meerjarenvisie_2022_2025",
            "mun_humanitas_almere",
            "mun_almere_almeers_preventieakkoord",
            "mun_almere_sociale_veerkracht_almeerders",
        ],
        "confidence": "medium",
        "open_issue": "Public evidence is stronger, but formal D6 classification, owner, mandate, complete inventory and structural funding remain validation questions.",
    },
    {
        "component_id": "funding_budget_alignment",
        "component_label": "Financiering en budgetafbakening",
        "existing_almere_provision": (
            "National funding architecture and workagenda process sources are present, and municipal subsidy "
            "registers now give stronger local funding-context traces. DUS-I and VWS sources make the SPUK/IZA "
            "mandate route more explicit, including Almere as mandaatgemeente for the Flevoland route. "
            "Almere-specific D6 allocation is not settled."
        ),
        "required_upgrade": "Map AZWA-D6, D5 workagenda, SPUK IZA, Brede SPUK/GALA, PGA transformation funding, municipal regular budget and Zvw lines per component.",
        "owner": "mandaatgemeente, municipality and regional workagenda governance need component-specific validation",
        "executors": [],
        "cooperation_partners": [
            "Gemeente Almere as mandaatgemeente",
            "preferente zorgverzekeraar",
            "Verbindende Coalitie Zorgzaam Flevoland",
            "Netwerkbureau Zorgzaam Flevoland",
            "financial controllers",
            "regional table",
        ],
        "scale": "mixed_scale_must_be_split",
        "funding_sources": ["unknown_needs_decision"],
        "decision_status": "decision_needed",
        "evidence_sources": [
            "data/extracted/workagenda_d5_operational_requirements.json",
            "nat_zorgakkoorden_werkagenda_handvatten_2026",
            "mun_almere_subsidieregister_2023",
            "mun_almere_subsidieregister_2024",
            "mun_almere_subsidieregister_2025",
            "reg_ggd_flevoland_begroting_2026",
            "nat_zorgakkoorden_pga_20_miljoen_2024",
            "nat_dusi_spuk_iza_2023_2026",
            "nat_vws_spuk_iza_brede_spuk_mandaatgemeente_2025",
            "reg_centrumregeling_sociaal_domein_flevoland",
        ],
        "confidence": "medium",
        "open_issue": "This is the main anti-dubbeltelling control point for D6.",
    },
]


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def enrich_component(component: dict[str, Any], source_index: dict[str, dict[str, Any]]) -> dict[str, Any]:
    evidence = []
    for source_id in component["evidence_sources"]:
        source = source_index.get(source_id)
        if source:
            evidence.append(
                {
                    "source_id": source_id,
                    "title": source["title"],
                    "source_url": source["source_url"],
                    "repository_status": source["repository_status"],
                    "verification_status": source["verification_status"],
                }
            )
        else:
            evidence.append({"source_id": source_id, "repository_status": "existing_repository_layer_or_prior_source"})

    decision_status = DECISION_STATUS_MAP.get(component["decision_status"], "review_needed")
    human_review_needed = decision_status != "settled"
    return {
        **component,
        "d6_component": component["component_label"],
        "executor_or_executors": component["executors"],
        "funding_source": component["funding_sources"],
        "decision_status": decision_status,
        "prefill_status": component["decision_status"],
        "evidence_source": component["evidence_sources"],
        "evidence": evidence,
        "human_review_needed": human_review_needed,
        "needs_human_review": human_review_needed,
        "fact_interpretation_proposal_status": (
            "public_prefill_needs_local_validation"
            if decision_status in {"inferred", "review_needed"}
            else "decision_needed"
        ),
    }


def build_payload() -> dict[str, Any]:
    d6_governance = load_json(D6_GOVERNANCE_PATH, {})
    source_index = {source["source_id"]: source for source in PUBLIC_SOURCE_CANDIDATES}
    components = [enrich_component(component, source_index) for component in COMPONENTS]

    return {
        "layer_run_id": "phase25_4b_almere_d6_responsibility_register_v1",
        "generated_on": date.today().isoformat(),
        "status": "active_sprint_support",
        "sprint": "25.4b D6 Almere responsibility pack",
        "purpose": (
            "Create an execution-oriented D6 Almere register that separates public prefill, "
            "local validation, decision needs, scale, funding, and evidence status."
        ),
        "public_source_boundary": (
            "This register is public-source prefill. It does not settle local ownership, execution, "
            "budget or D6 classification without ingested decision sources or local validation."
        ),
        "inputs": [
            "docs/phase25-sprint25.4-d6-almere-responsibility-pack-plan.md",
            "data/extracted/d6_governance_collaboration.json",
            "public URL verification performed 2026-04-26",
        ],
        "summary": {
            "component_count": len(components),
            "candidate_source_count": len(PUBLIC_SOURCE_CANDIDATES),
            "settled_count": sum(1 for component in components if component["decision_status"] == "settled"),
            "inferred_count": sum(1 for component in components if component["decision_status"] == "inferred"),
            "proposed_count": sum(1 for component in components if component["decision_status"] == "proposed"),
            "unknown_count": sum(1 for component in components if component["decision_status"] == "unknown"),
            "review_needed_count": sum(1 for component in components if component["decision_status"] == "review_needed"),
            "decision_needed_count": sum(1 for component in components if component["decision_status"] == "unknown"),
            "source_backed_prefill_count": sum(
                1 for component in components if component.get("prefill_status") == "source_backed_prefill"
            ),
            "d6_prefill_dimension_count": (d6_governance.get("summary") or {}).get("dimension_count"),
        },
        "scale_guardrail": (
            "Keep Almere-local, IZA/AZWA-regio Flevoland, GGD-regio Flevoland, zorgkantoorregio "
            "and project/programme scale separate in every D6 row."
        ),
        "public_source_candidates": PUBLIC_SOURCE_CANDIDATES,
        "components": components,
        "next_actions": [
            "Ingest the highest-priority verified public sources into data/raw/manifest.json.",
            "Convert council Documentwijzer attachments for Stevige Lokale Teams to page-markdown before claim extraction.",
            "Regenerate inventory, structural extraction, claims, D6 layers, QC and dashboard after formal source intake.",
            "Ask local employees to validate D6 classification, owner, executor, budget and monitoring fields after public-source exhaustion.",
        ],
    }


def main() -> None:
    payload = build_payload()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"Components: {payload['summary']['component_count']}")


if __name__ == "__main__":
    main()
