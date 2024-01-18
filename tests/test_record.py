import pytest
from pydantic import ValidationError
from contextlib import nullcontext as does_not_raise
from src.validate.models import Record


@pytest.mark.parametrize(
    "order_location, item_location",
    [("MAB", "rcmf2"), ("MAF", "rc2ma"), ("MAL", "rcmg2")],
)
def test_record_invalid_combo(order_location, item_location):
    with pytest.raises(ValidationError) as e:
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
    assert e.value.errors()[0]["type"] == "Item/Order location check"


@pytest.mark.parametrize(
    "order_location, item_location",
    [("MAF", "rcmf2"), ("MAL", "rc2ma"), ("MAG", "rcmg2")],
)
def test_record_valid_combo(order_location, item_location):
    with does_not_raise():
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


def test_location_combo(valid_nypl_rl_record):
    valid_nypl_rl_record["item"]["item_type"] = "55"
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
    assert e.value.errors()[0]["type"] == "Item/Order location check"


def test_valid_record(valid_nypl_rl_record):
    with does_not_raise():
        Record(**valid_nypl_rl_record)


def test_invalid_call_no(valid_pamphlet_record):
    valid_pamphlet_record["item"]["item_call_tag"] = "8528"
    with pytest.raises(ValidationError) as e:
        Record(**valid_pamphlet_record)
    assert e.value.errors()[0]["type"] == "extra_forbidden"


def test_valid_call_no(valid_pamphlet_record):
    with does_not_raise():
        Record(**valid_pamphlet_record)


def test_missing_location(valid_nypl_rl_record):
    del valid_nypl_rl_record["item"]["item_location"]
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
    assert e.value.errors()[0]["type"] == "missing"


def test_missing_item_type(valid_nypl_rl_record):
    del valid_nypl_rl_record["item"]["item_type"]
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
    assert e.value.errors()[0]["type"] == "missing"


def test_missing_order_location(valid_nypl_rl_record):
    del valid_nypl_rl_record["order"]["order_location"]
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
    assert e.value.errors()[0]["type"] == "missing"
