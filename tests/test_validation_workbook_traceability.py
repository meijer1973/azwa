from src.build_validation_workbook_traceability import build_map


def test_validation_workbook_traceability_ids_are_unique():
    data = build_map()
    uniqueness = data["question_id_uniqueness"]

    assert uniqueness["total_ids"] == uniqueness["unique_ids"]
    assert uniqueness["duplicates"] == []
    assert uniqueness["total_ids"] >= 180


def test_validation_workbook_traceability_covers_d5_and_d6():
    data = build_map()
    workbooks = {workbook["workbook_id"]: workbook for workbook in data["workbooks"]}

    assert set(workbooks) == {"d5_validation_workbook", "d6_validation_workbook"}
    assert sum(sheet["mapped_validation_row_count"] for sheet in workbooks["d5_validation_workbook"]["sheets"]) > 0
    assert sum(sheet["mapped_validation_row_count"] for sheet in workbooks["d6_validation_workbook"]["sheets"]) > 0
    d5_sheet_names = {sheet["sheet"] for sheet in workbooks["d5_validation_workbook"]["sheets"]}
    assert "Financiering" not in d5_sheet_names
    assert "Governance rollen" not in d5_sheet_names


def test_validation_workbook_rows_have_processing_metadata():
    data = build_map()

    for workbook in data["workbooks"]:
        for sheet in workbook["sheets"]:
            for row in sheet["rows"]:
                assert row["vraag_id"]
                assert row["component_id"]
                assert row["stakeholderpakket"]
                assert row["antwoordtype"]
                assert row["validatiestatus_default"] == "nog_niet_gevraagd"
                assert row["bewijstype_verplicht"] is True
                assert row["repo_update_effect"]
                assert row["deadline"] == "pre_contact_send_readiness"
