import pytest
from pydantic import ValidationError
from contextlib import nullcontext
from rl_sr_validation.models import Item, BibData


@pytest.mark.parametrize("item_price", ["1.23", "12.34", "123.45"])
def test_item_price_valid(item_price):
    with nullcontext():
        Item(
            call_tag="8528",
            call_no="ReCAP 23-10000",
            barcode="12345667890123",
            price=item_price,
            initials="EV",
            agency="43",
        )


@pytest.mark.parametrize("item_price", ["123", "1234", "12345"])
def test_item_price_invalid(item_price):
    with pytest.raises(ValidationError):
        Item(
            call_tag="8528",
            call_no="ReCAP 23-10000",
            barcode="12345667890123",
            price=item_price,
            initials="EV",
            agency="43",
        )


@pytest.mark.parametrize("call_tag", ["8528"])
def test_item_call_tag_valid(call_tag):
    with nullcontext():
        Item(
            call_tag=call_tag,
            call_no="ReCAP 23-10000",
            barcode="12345667890123",
            price="12.34",
            initials="EV",
            agency="43",
        )


@pytest.mark.parametrize("call_tag", ["852"])
def test_item_call_tag_invalid(call_tag):
    with pytest.raises(ValidationError):
        Item(
            call_tag=call_tag,
            call_no="ReCAP 23-10000",
            barcode="12345667890123",
            price="12.34",
            initials="EV",
            agency="43",
        )


@pytest.mark.parametrize(
    "call_no", ["ReCAP 23-10000", "ReCAP 23-11111", "ReCAP 23-12345", "ReCAP 23-99999"]
)
def test_item_call_no_valid(call_no):
    with nullcontext():
        Item(
            call_tag="8528",
            call_no=call_no,
            barcode="12345667890123",
            price="12.34",
            initials="EV",
            agency="43",
        )


def test_item_bib_call_nos_match():
    i = Item(
        call_tag="8528",
        call_no="ReCAP 23-10000",
        barcode="12345667890123",
        price="12.34",
        initials="EV",
        agency="43",
    )
    b = BibData(call_no="ReCAP 23-10000", vendor="EV", rl_identifier="RL", lcc="DR")
    assert i.call_no == b.call_no
