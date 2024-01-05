import pytest
from pydantic import ValidationError
from contextlib import nullcontext
from rl_sr_validation.models import Order, Item, Invoice, Record


@pytest.mark.parametrize(
    "order_location, item_location",
    [("ZZZ", "rcmf2"), ("AAA", "rc2ma"), ("BBB", "rcmg2")],
)
def test_record_invalid_combo(order_location, item_location):
    with pytest.raises(ValidationError):
        item = Item(
            item_call_tag="8528",
            item_call_no="ReCAP 23-999999",
            item_barcode="12345678901234",
            item_price="12.34",
            item_vendor_code="EVIS",
            item_location=item_location,
            item_type="55",
            item_agency="43",
        )
        order = Order(
            location=order_location, order_price="1234", order_fund="123456apprv"
        )
        invoice = Invoice(
            invoice_date="240101",
            invoice_price="1234",
            invoice_shipping="100",
            invoice_tax="123",
            invoice_net_price="1234",
            invoice_number="1234567890",
            invoice_copies="1",
        )

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
            "item_call_tag": "8528",
            "item_call_no": "ReCAP 23-999999",
            "item_barcode": "12345678901234",
            "item_price": "12.34",
            "item_vendor_code": "EVIS",
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
            lcc="Z123.",
        )


def test_location_combo(invalid_record):
    with pytest.raises(ValidationError):
        Record(**invalid_record)


def test_valid_record(valid_record):
    with nullcontext():
        Record(**valid_record)
