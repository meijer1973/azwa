from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
STATUS_MATRIX_PATH = REPO_ROOT / "data" / "workagenda" / "d5_status_matrix.json"
VALIDATION_TICKETS_PATH = REPO_ROOT / "data" / "workagenda" / "d5_validation_tickets.json"
VALIDATION_TICKETS_DOC_PATH = REPO_ROOT / "docs" / "workagenda-d5-validation-tickets.md"


class WorkagendaD5ValidationTicketsTests(unittest.TestCase):
    def test_ticket_set_covers_status_matrix_components(self) -> None:
        matrix = json.loads(STATUS_MATRIX_PATH.read_text(encoding="utf-8"))
        tickets = json.loads(VALIDATION_TICKETS_PATH.read_text(encoding="utf-8"))

        matrix_ids = {row["target_id"] for row in matrix["rows"]}
        ticket_ids = set(tickets["tickets_by_component"])

        self.assertEqual(ticket_ids, matrix_ids)
        self.assertEqual(tickets["summary"]["component_count"], 11)
        self.assertEqual(tickets["summary"]["ticket_count"], 47)

    def test_required_components_have_five_validation_tickets(self) -> None:
        tickets = json.loads(VALIDATION_TICKETS_PATH.read_text(encoding="utf-8"))
        required_ticket_types = {
            "local_status_capacity",
            "governance_roles",
            "finance_controller",
            "d6_dependency",
            "decision_phasing",
        }

        for target_id, component_ticket_ids in tickets["tickets_by_component"].items():
            ticket_types = {ticket_id.rsplit("__", 1)[1] for ticket_id in component_ticket_ids}
            if len(component_ticket_ids) == 1:
                self.assertEqual(ticket_types, {"scope_choice"})
            else:
                self.assertEqual(ticket_types, required_ticket_types)

    def test_every_ticket_has_constrained_choices_and_evidence_gate(self) -> None:
        tickets = json.loads(VALIDATION_TICKETS_PATH.read_text(encoding="utf-8"))

        for ticket in tickets["tickets"]:
            self.assertTrue(ticket["choice_sets"])
            self.assertTrue(ticket["answer_options"])
            self.assertIn("Onbekend", " ".join(ticket["answer_options"][ticket["choice_sets"][0]]))
            self.assertIn("Anders", " ".join(ticket["answer_options"][ticket["choice_sets"][0]]))
            self.assertTrue(ticket["evidence_options"])
            self.assertTrue(ticket["evidence_gate"])
            self.assertTrue(ticket["default_if_no_evidence"])
            self.assertTrue(ticket["status_matrix_effect"])
            self.assertTrue(ticket["escalation_trigger"])

    def test_finance_tickets_are_routed_to_finance_packet(self) -> None:
        tickets = json.loads(VALIDATION_TICKETS_PATH.read_text(encoding="utf-8"))
        finance_tickets = [ticket for ticket in tickets["tickets"] if ticket["ticket_type"] == "finance_controller"]

        self.assertEqual(len(finance_tickets), 9)
        for ticket in finance_tickets:
            self.assertIn("Finance/controller", ticket["stakeholder_packet"])
            self.assertIn("controller", ticket["evidence_gate"].lower())

    def test_human_ticket_doc_names_sprint_and_guardrails(self) -> None:
        text = VALIDATION_TICKETS_DOC_PATH.read_text(encoding="utf-8")

        self.assertIn("Current sprint: Sprint 32.2", text)
        self.assertIn("Tickets: 47", text)
        self.assertIn("Do not fill stakeholder answers by inference", text)


if __name__ == "__main__":
    unittest.main()
