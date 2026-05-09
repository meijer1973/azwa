import csv
from pathlib import Path

from src.build_precontact_stakeholder_packets import build_packets


def test_precontact_packets_are_prepared_not_sent_and_filtered():
    packet_index = build_packets()

    assert packet_index["dispatch_status"] == "prepared_not_sent"
    assert packet_index["packet_count"] >= 15
    assert packet_index["unique_vraag_ids"] == 189

    packet_ids = {packet["packet_id"] for packet in packet_index["packets"]}
    assert "gemeente_almere_sociaal_domein" not in packet_ids
    assert {
        "gemeente_almere_sociaal_domein_d5",
        "gemeente_almere_sociaal_domein_d6",
        "gemeente_almere_sociaal_domein_sturing",
    }.issubset(packet_ids)
    assert all(packet["dispatch_status"] == "prepared_not_sent" for packet in packet_index["packets"])


def test_precontact_packets_keep_packet_sizes_reviewable():
    packet_index = build_packets()

    assert max(packet["row_count"] for packet in packet_index["packets"]) <= 80


def test_precontact_packet_csvs_keep_traceability_fields():
    packet_index = build_packets()
    sample_packet = next(packet for packet in packet_index["packets"] if packet["row_count"] > 0)
    csv_path = Path(sample_packet["csv_path"])

    with csv_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        row = next(reader)

    assert row["vraag_id"]
    assert row["component_id"]
    assert row["stakeholderpakket"] == sample_packet["packet_id"]
    assert "evidence_reference" in row
    assert "evidence_type" in row
    assert "not_my_domain_reroute" in row


def test_precontact_packets_keep_required_handoff_fields():
    packet_index = build_packets()

    for packet in packet_index["packets"]:
        assert packet["csv_path"]
        assert packet["rows"]
        assert packet["evidence_required_count"] > 0
        for row in packet["rows"]:
            assert row["vraag_id"]
            assert row["question_text"]
            assert row["bewijstype_verplicht"] is True
