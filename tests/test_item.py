import pytest
from pydantic import ValidationError
from contextlib import nullcontext as does_not_raise
from shelf_ready_validator.models import ItemNYPLRL, ItemNYPLBL, ItemBPL


def test_call_tag_valid():
    with does_not_raise():
        ItemNYPLRL(
            item_call_tag="8528",
            item_call_no="ReCAP 23-000000",
            item_barcode="33433123456789",
            item_price="1.00",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmb2",
            item_type="2",
            item_ind1=" ",
            item_ind2="1",
            library="RL",
        )


def test_call_tag_invalid():
    with pytest.raises(ValidationError) as e:
        ItemNYPLRL(
            item_call_tag="8582",
            item_call_no="ReCAP 23-000000",
            item_barcode="33433123456789",
            item_price="1.00",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmb2",
            item_type="2",
            item_ind1=" ",
            item_ind2="1",
            library="RL",
        )
    assert e.value.errors()[0]["type"] == "literal_error"


def test_call_no_valid():
    with does_not_raise():
        ItemNYPLRL(
            item_call_tag="8528",
            item_call_no="ReCAP 23-000000",
            item_barcode="33433123456789",
            item_price="1.00",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmb2",
            item_type="2",
            item_ind1=" ",
            item_ind2="1",
            library="RL",
        )


def test_call_no_invalid():
    with pytest.raises(ValidationError) as e:
        ItemNYPLRL(
            item_call_tag="8528",
            item_call_no="ReCAP 23-00000",
            item_barcode="33433123456789",
            item_price="1.00",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmb2",
            item_type="2",
            item_ind1=" ",
            item_ind2="1",
            library="RL",
        )
    assert e.value.errors()[0]["type"] == "string_pattern_mismatch"


@pytest.mark.parametrize(
    "barcode, library, item_model",
    [
        ("33433123456789", "RL", ItemNYPLRL),
        ("34444123456789", "BPL", ItemBPL),
        ("33333123456789", "BL", ItemNYPLBL),
    ],
)
def test_barcode_valid(barcode, library, item_model):
    with does_not_raise():
        item_model(
            item_call_tag="8528",
            item_call_no="ReCAP 23-000000",
            item_barcode=barcode,
            item_price="1.00",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmb2",
            item_type="2",
            item_ind1=" ",
            item_ind2="1",
            library=library,
        )


@pytest.mark.parametrize(
    "barcode, library, item_model",
    [
        ("33333123456789", "RL", ItemNYPLRL),
        ("33433123456789", "BL", ItemNYPLBL),
        ("33433123456789", "BPL", ItemBPL),
    ],
)
def test_barcode_invalid(barcode, library, item_model):
    with pytest.raises(ValidationError) as e:
        item_model(
            item_call_tag="8528",
            item_call_no="ReCAP 23-000000",
            item_barcode=barcode,
            item_price="1.00",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmb2",
            item_type="2",
            item_ind1=" ",
            item_ind2="1",
            library=library,
        )
    assert e.value.errors()[0]["type"] == "string_pattern_mismatch"


@pytest.mark.parametrize(
    "item_location",
    [
        "rcmb2",
        "rcmf2",
        "rcmg2",
        "rc2ma",
        "rcmp2",
        "rcmb2",
        "rcph2",
        "rcpm2",
        "rcpt2",
        "rc2cf",
    ],
)
def test_item_location_valid(item_location):
    with does_not_raise():
        ItemNYPLRL(
            item_call_tag="8528",
            item_call_no="ReCAP 23-000000",
            item_barcode="33433123456789",
            item_price="1.00",
            item_vendor_code="EVP",
            item_agency="43",
            item_location=item_location,
            item_type="2",
            item_ind1=" ",
            item_ind2="1",
            library="RL",
        )


@pytest.mark.parametrize(
    "item_location",
    ["12345", "aaaaa", 12345],
)
def test_item_location_invalid(item_location):
    with pytest.raises(ValidationError) as e:
        ItemNYPLRL(
            item_call_tag="8528",
            item_call_no="ReCAP 23-000000",
            item_barcode="33433123456789",
            item_price="1.00",
            item_vendor_code="EVP",
            item_agency="43",
            item_location=item_location,
            item_type="2",
            item_ind1=" ",
            item_ind2="1",
            library="RL",
        )
    assert e.value.errors()[0]["type"] == "literal_error"


@pytest.mark.parametrize(
    "item_vendor_code",
    ["EVP", "AUXAM"],
)
def test_item_vendor_code_valid(item_vendor_code):
    with does_not_raise():
        ItemNYPLRL(
            item_call_tag="8528",
            item_call_no="ReCAP 23-000000",
            item_barcode="33433123456789",
            item_price="1.00",
            item_vendor_code=item_vendor_code,
            item_agency="43",
            item_location="rcmb2",
            item_type="2",
            item_ind1=" ",
            item_ind2="1",
            library="RL",
        )


@pytest.mark.parametrize(
    "item_vendor_code",
    ["12345", "aaaaa", 12345],
)
def test_item_vendor_code_invalid(item_vendor_code):
    with pytest.raises(ValidationError) as e:
        ItemNYPLRL(
            item_call_tag="8528",
            item_call_no="ReCAP 23-000000",
            item_barcode="33433123456789",
            item_price="1.00",
            item_vendor_code=item_vendor_code,
            item_agency="43",
            item_location="rcmb2",
            item_type="2",
            item_ind1=" ",
            item_ind2="1",
            library="RL",
        )
    assert e.value.errors()[0]["type"] == "literal_error"


def test_item_agency_valid():
    with does_not_raise():
        ItemNYPLRL(
            item_call_tag="8528",
            item_call_no="ReCAP 23-000000",
            item_barcode="33433123456789",
            item_price="1.00",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmb2",
            item_type="2",
            item_ind1=" ",
            item_ind2="1",
            library="RL",
        )


def test_item_agency_invalid():
    with pytest.raises(ValidationError) as e:
        ItemNYPLRL(
            item_call_tag="8528",
            item_call_no="ReCAP 23-000000",
            item_barcode="33433123456789",
            item_price="1.00",
            item_vendor_code="EVP",
            item_agency=43,
            item_location="rcmb2",
            item_type="2",
            item_ind1=" ",
            item_ind2="1",
            library="RL",
        )
    assert e.value.errors()[0]["type"] == "literal_error"
