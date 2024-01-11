import pytest
from pydantic import ValidationError
from contextlib import nullcontext
from rl_sr_validation.models import Record
from rl_sr_validation.errors import parse_errors


@pytest.mark.parametrize(
    "order_location, item_location",
    [("ZZZ", "rcmf2"), ("AAA", "rc2ma"), ("BBB", "rcmg2")],
)
def test_record_invalid_combo(order_location, item_location):
    with pytest.raises(ValidationError):
        item = {
            "material_type": "monograph_record",
            "item_call_tag": "8528",
            "item_call_no": "ReCAP 23-999999",
            "item_barcode": "33333678901234",
            "item_price": "12.34",
            "item_vendor_code": "EVP",
            "item_location": item_location,
            "item_type": "55",
            "item_agency": "43",
        }
        order = {
            "order_location": order_location,
            "order_price": "1234",
            "order_fund": "123456apprv",
        }
        invoice = {
            "invoice_date": "240101",
            "invoice_price": "1234",
            "invoice_shipping": "100",
            "invoice_tax": "123",
            "invoice_net_price": "1234",
            "invoice_number": "1234567890",
            "invoice_copies": "1",
        }

        Record(
            item=item,
            order=order,
            invoice=invoice,
            bib_call_no="ReCAP 23-999999",
            bib_vendor_code="EVP",
            rl_identifier="RL",
            lcc="Z123",
        )


@pytest.mark.parametrize(
    "order_location, item_location",
    [("MAF", "rcmf2"), ("MAL", "rc2ma"), ("MAG", "rcmg2")],
)
def test_record_valid_combo(order_location, item_location):
    with nullcontext():
        item = {
            "material_type": "monograph_record",
            "item_call_tag": "8528",
            "item_call_no": "ReCAP 23-999999",
            "item_barcode": "33333678901234",
            "item_price": "12.34",
            "item_vendor_code": "EVP",
            "item_agency": "43",
            "item_location": item_location,
            "item_type": "55",
        }
        order = {
            "order_location": order_location,
            "order_fund": "123456apprv",
            "order_price": "1234",
        }
        invoice = {
            "invoice_date": "240101",
            "invoice_price": "1234",
            "invoice_shipping": "100",
            "invoice_tax": "123",
            "invoice_net_price": "1234",
            "invoice_number": "1234567890",
            "invoice_copies": "1",
        }

        Record(
            item=item,
            order=order,
            invoice=invoice,
            bib_call_no="ReCAP 23-999999",
            bib_vendor_code="EVP",
            rl_identifier="RL",
            lcc="Z123.",
        )


def test_location_combo(invalid_bpl_record):
    with pytest.raises(ValidationError):
        Record(**invalid_bpl_record)


def test_valid_record(valid_bpl_record):
    with nullcontext():
        Record(**valid_bpl_record)


def test_invalid_call_no(invalid_pamphlet_record):
    with pytest.raises(ValidationError):
        Record(**invalid_pamphlet_record)


def test_valid_call_no(valid_pamphlet_record):
    with nullcontext():
        Record(**valid_pamphlet_record)


def test_missing_field_errors(missing_fields):
    try:
        Record(**missing_fields)
    except ValidationError as e:
        parsed_errors = parse_errors(e)
        missing_field_count = parsed_errors["missing_field_count"]
        assert missing_field_count == 2
