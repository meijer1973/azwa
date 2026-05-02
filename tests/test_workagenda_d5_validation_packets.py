from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKETS_PATH = REPO_ROOT / "data" / "workagenda" / "d5_validation_packets.json"
TICKETS_PATH = REPO_ROOT / "data" / "workagenda" / "d5_validation_tickets.json"
PACKET_DOC_PATH = REPO_ROOT / "docs" / "workagenda-d5-validation-format.md"


class WorkagendaD5ValidationPacketsTests(unittest.TestCase):
    def test_packets_cover_all_validation_tickets(self) -> None:
        packets = json.loads(PACKETS_PATH.read_text(encoding="utf-8"))
        tickets = json.loads(TICKETS_PATH.read_text(encoding="utf-8"))

        packet_ticket_ids = {
            ticket_id
            for packet in packets["packets"]
            for ticket_id in packet["ticket_ids"]
        }
        source_ticket_ids = {ticket["ticket_id"] for ticket in tickets["tickets"]}

        self.assertEqual(packet_ticket_ids, source_ticket_ids)
        self.assertEqual(packets["summary"]["ticket_count"], 47)
        self.assertEqual(packets["summary"]["packet_count"], 6)

    def test_packet_csvs_exist_with_blank_answer_fields(self) -> None:
        packets = json.loads(PACKETS_PATH.read_text(encoding="utf-8"))
        expected_columns = packets["csv_columns"]

        for packet in packets["packets"]:
            csv_path = REPO_ROOT / packet["csv_path"]
            self.assertTrue(csv_path.exists(), packet["csv_path"])
            with csv_path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0].keys(), set(expected_columns))
            self.assertEqual(len(rows), packet["ticket_count"])
            for row in rows:
                self.assertEqual(row["answer"], "")
                self.assertEqual(row["evidence_path_or_document"], "")
                self.assertTrue(row["evidence_gate"])

    def test_expected_packets_are_present(self) -> None:
        packets = json.loads(PACKETS_PATH.read_text(encoding="utf-8"))
        packet_ids = {packet["packet_id"] for packet in packets["packets"]}

        self.assertEqual(
            packet_ids,
            {
                "d6_dependency",
                "decision_phasing",
                "finance_controller",
                "gemeente_sociaal_domein",
                "jgz_ggd",
                "zorgverzekeraar",
            },
        )

    def test_human_format_doc_names_blocked_next_step(self) -> None:
        text = PACKET_DOC_PATH.read_text(encoding="utf-8")

        self.assertIn("Current sprint: Sprint 32.2", text)
        self.assertIn("Sprint 32.3 remains blocked", text)
        self.assertIn("Do not fill blank answers from repository inference", text)


if __name__ == "__main__":
    unittest.main()
