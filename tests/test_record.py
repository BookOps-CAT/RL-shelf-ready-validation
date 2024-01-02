import pytest
from pydantic import ValidationError
from contextlib import nullcontext
from rl_sr_validation.models import Order, Item, Invoice, BibData, Record


@pytest.mark.parametrize("order_location", ["AAA", "BBB", "ZZZ", None])
def test_record_invalid_combo(order_location):
    with pytest.raises(ValidationError):
        item = Item(
            call_tag="8528",
            call_no="ReCAP 23-99999",
            barcode="12345678901234",
            price="12.34",
            initials="EV",
            location="rcmb2",
            item_type="2",
            agency="43",
        )
        order = Order(location=order_location, price="1234", fund="123456apprv")
        bib = BibData(
            call_no="ReCAP 23-99999", vendor="EV", rl_identifier="RL", lcc="Z123"
        )
        invoice = Invoice(date="240101", price="1234")

        Record(item_data=item, order_data=order, bib_data=bib, invoice_data=invoice)


@pytest.mark.parametrize(
    "order_location, item_location",
    [("MAF", "rcmf2"), ("MAL", "rc2ma"), ("MAG", "rcmg2")],
)
def test_record_valid_combo(order_location, item_location):
    with nullcontext():
        item = Item(
            call_tag="8528",
            call_no="ReCAP 23-99999",
            barcode="12345678901234",
            price="12.34",
            initials="EV",
            location=item_location,
            item_type="55",
            agency="43",
        )
        order = Order(location=order_location, price="1234", fund="123456apprv")
        bib = BibData(
            call_no="ReCAP 23-99999", vendor="EV", rl_identifier="RL", lcc="Z123"
        )
        invoice = Invoice(date="240101", price="1234")

        Record(item_data=item, order_data=order, bib_data=bib, invoice_data=invoice)
