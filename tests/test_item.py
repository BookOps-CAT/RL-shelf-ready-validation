import pytest
from pydantic import ValidationError
from contextlib import nullcontext
from rl_sr_validation.models import Item, Record


@pytest.mark.parametrize("item_price", ["1.23", "12.34", "123.45"])
def test_item_price_valid(item_price):
    with nullcontext():
        Item(
            item_call_tag="8528",
            item_call_no="ReCAP 23-100000",
            item_barcode="12345678901234",
            item_price=item_price,
            item_vendor_code="EVIS",
            item_agency="43",
            item_location="rcmg2",
            item_type="55",
        )


@pytest.mark.parametrize("item_price", ["123", "1234", "12345"])
def test_item_price_invalid(item_price):
    with pytest.raises(ValidationError):
        Item(
            item_call_tag="8528",
            item_call_no="ReCAP 23-100000",
            item_barcode="12345678901234",
            item_price=item_price,
            item_vendor_code="EVIS",
            item_agency="43",
            item_location="rcmg2",
            item_type="55",
        )


@pytest.mark.parametrize("call_tag", ["8528"])
def test_item_call_tag_valid(call_tag):
    with nullcontext():
        Item(
            item_call_tag=call_tag,
            item_call_no="ReCAP 23-100000",
            item_barcode="12345678901234",
            item_price="12.34",
            item_vendor_code="EVIS",
            item_agency="43",
            item_location="rcmg2",
            item_type="55",
        )


@pytest.mark.parametrize("call_tag", ["852"])
def test_item_call_tag_invalid(call_tag):
    with pytest.raises(ValidationError):
        Item(
            item_call_tag=call_tag,
            item_call_no="ReCAP 23-100000",
            item_barcode="12345678901234",
            item_price="12.34",
            item_vendor_code="EVIS",
            item_agency="43",
            item_location="rcmg2",
            item_type="55",
        )


@pytest.mark.parametrize(
    "call_no",
    ["ReCAP 23-100000", "ReCAP 23-111111", "ReCAP 23-123456", "ReCAP 23-999999"],
)
def test_item_call_no_valid(call_no):
    with nullcontext():
        Item(
            item_call_tag="8528",
            item_call_no=call_no,
            item_barcode="12345678901234",
            item_price="12.34",
            item_vendor_code="EVIS",
            item_agency="43",
            item_location="rcmg2",
            item_type="55",
        )
