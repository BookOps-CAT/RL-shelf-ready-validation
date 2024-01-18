import pytest
from pydantic import ValidationError
from contextlib import nullcontext as does_not_raise
from src.validate.models import ItemRequired, ItemNotRequired


def test_monograph_type_valid():
    with does_not_raise():
        ItemRequired(
            material_type="monograph_record",
            item_call_tag="8528",
            item_call_no="ReCAP 23-100000",
            item_barcode="33333678901234",
            item_price="12.34",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmg2",
            item_type="55",
        )


@pytest.mark.parametrize(
    "material_type",
    [
        "catalogue_raissonne",
        "performing_arts_dance",
        "multipart",
        "pamphlet",
        "non-standard_binding_packaging",
    ],
)
def test_monograph_type_literal_error(material_type):
    with pytest.raises(ValidationError) as e:
        ItemRequired(
            material_type=material_type,
            item_call_tag="8528",
            item_call_no="ReCAP 23-100000",
            item_barcode="33333678901234",
            item_price="12.34",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmg2",
            item_type="55",
        )
    assert e.value.errors()[0]["type"] == "literal_error"


@pytest.mark.parametrize(
    "material_type",
    [
        "catalogue_raissonne",
        "performing_arts_dance",
        "multipart",
        "pamphlet",
        "non-standard_binding_packaging",
    ],
)
def test_other_material_type_valid(material_type):
    with does_not_raise():
        ItemNotRequired(material_type=material_type)


def test_other_material_type_invalid():
    with pytest.raises(ValidationError) as e:
        ItemNotRequired(
            material_type="monograph_record",
        )
    assert e.value.errors()[0]["type"] == "literal_error"


def test_item_call_tag_valid():
    with does_not_raise():
        ItemRequired(
            material_type="monograph_record",
            item_call_tag="8528",
            item_call_no="ReCAP 23-100000",
            item_barcode="33333678901234",
            item_price="12.34",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmg2",
            item_type="55",
        )


def test_item_call_tag_invalid():
    with pytest.raises(ValidationError) as e:
        ItemRequired(
            material_type="monograph_record",
            item_call_tag="8582",
            item_call_no="ReCAP 23-100000",
            item_barcode="33333678901234",
            item_price="12.34",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmg2",
            item_type="55",
        )
    assert e.value.errors()[0]["type"] == "literal_error"


@pytest.mark.parametrize(
    "item_call_no",
    ["ReCAP 23-100000", "ReCAP 23-111111", "ReCAP 23-123456", "ReCAP 23-999999"],
)
def test_item_call_no_valid(item_call_no):
    with does_not_raise():
        ItemRequired(
            material_type="monograph_record",
            item_call_tag="8528",
            item_call_no=item_call_no,
            item_barcode="33333678901234",
            item_price="12.34",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmg2",
            item_type="55",
        )


@pytest.mark.parametrize(
    "item_call_no",
    ["23-100000", "ReCAP", "PG9050.17.E55"],
)
def test_item_call_no_invalid(item_call_no):
    with pytest.raises(ValidationError) as e:
        ItemRequired(
            material_type="monograph_record",
            item_call_tag="8528",
            item_call_no=item_call_no,
            item_barcode="33333678901234",
            item_price="12.34",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmg2",
            item_type="55",
        )
    assert e.value.errors()[0]["type"] == "string_pattern_mismatch"


@pytest.mark.parametrize(
    "item_barcode", ["33433123456789", "34444123456789", "33333123456789"]
)
def test_item_barcode_valid(item_barcode):
    with does_not_raise():
        ItemRequired(
            material_type="monograph_record",
            item_call_tag="8528",
            item_call_no="ReCAP 23-100000",
            item_barcode=item_barcode,
            item_price="12.34",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmg2",
            item_type="55",
        )


@pytest.mark.parametrize(
    "item_barcode",
    [
        "1234",
        "12345",
        "12345678901234",
        "333331234567.9",
    ],
)
def test_item_barcode_invalid(item_barcode):
    with pytest.raises(ValidationError) as e:
        ItemRequired(
            material_type="monograph_record",
            item_call_tag="8528",
            item_call_no="ReCAP 23-100000",
            item_barcode=item_barcode,
            item_price="12.34",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmg2",
            item_type="55",
        )
    assert e.value.errors()[0]["type"] == "string_pattern_mismatch"


@pytest.mark.parametrize("item_price", ["1.23", "12.34", "123.45"])
def test_item_price_valid(item_price):
    with does_not_raise():
        ItemRequired(
            material_type="monograph_record",
            item_call_tag="8528",
            item_call_no="ReCAP 23-100000",
            item_barcode="33333678901234",
            item_price=item_price,
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmg2",
            item_type="55",
        )


@pytest.mark.parametrize("item_price", ["123", "1234", "12345"])
def test_item_price_invalid(item_price):
    with pytest.raises(ValidationError) as e:
        ItemRequired(
            material_type="monograph_record",
            item_call_tag="8528",
            item_call_no="ReCAP 23-100000",
            item_barcode="33333678901234",
            item_price=item_price,
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmg2",
            item_type="55",
        )
    assert e.value.errors()[0]["type"] == "string_pattern_mismatch"


@pytest.mark.parametrize("item_volume", ["1", "2", "300", None])
def test_item_volume_valid(item_volume):
    with does_not_raise():
        ItemRequired(
            material_type="monograph_record",
            item_call_tag="8528",
            item_call_no="ReCAP 23-100000",
            item_barcode="33333678901234",
            item_price="12.34",
            item_volume=item_volume,
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmg2",
            item_type="55",
        )


@pytest.mark.parametrize("item_volume", [1, 1.5, 2, ["1", "2"], {"item_volume": "1"}])
def test_item_volume_invalid(item_volume):
    with pytest.raises(ValidationError) as e:
        ItemRequired(
            material_type="monograph_record",
            item_call_tag="8528",
            item_call_no="ReCAP 23-100000",
            item_barcode="33333678901234",
            item_price="12.34",
            item_volume=item_volume,
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmg2",
            item_type="55",
        )
    assert e.value.errors()[0]["type"] == "string_type"


@pytest.mark.parametrize("item_vendor_code", ["EVP", "AUXAM"])
def test_item_vendor_code_valid(item_vendor_code):
    with does_not_raise():
        ItemRequired(
            material_type="monograph_record",
            item_call_tag="8528",
            item_call_no="ReCAP 23-100000",
            item_barcode="33333678901234",
            item_price="12.34",
            item_vendor_code=item_vendor_code,
            item_agency="43",
            item_location="rcmg2",
            item_type="55",
        )


@pytest.mark.parametrize(
    "item_vendor_code", [None, 1.5, 2, ["1", "2"], {"vendor": "1"}]
)
def test_item_vendor_code_invalid(item_vendor_code):
    with pytest.raises(ValidationError) as e:
        ItemRequired(
            material_type="monograph_record",
            item_call_tag="8528",
            item_call_no="ReCAP 23-100000",
            item_barcode="33333678901234",
            item_price="12.34",
            item_vendor_code=item_vendor_code,
            item_agency="43",
            item_location="rcmg2",
            item_type="55",
        )
    assert e.value.errors()[0]["type"] == "literal_error"


def test_item_agency_valid():
    with does_not_raise():
        ItemRequired(
            material_type="monograph_record",
            item_call_tag="8528",
            item_call_no="ReCAP 23-100000",
            item_barcode="33333678901234",
            item_price="12.34",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmg2",
            item_type="55",
        )


def test_item_agency_invalid():
    with pytest.raises(ValidationError) as e:
        ItemRequired(
            material_type="monograph_record",
            item_call_tag="8528",
            item_call_no="ReCAP 23-100000",
            item_barcode="33333678901234",
            item_price="12.34",
            item_vendor_code="EVP",
            item_agency=44,
            item_location="rcmg2",
            item_type="55",
        )
    assert e.value.errors()[0]["type"] == "string_type"


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
        ItemRequired(
            material_type="monograph_record",
            item_call_tag="8528",
            item_call_no="ReCAP 23-100000",
            item_barcode="33333678901234",
            item_price="12.34",
            item_vendor_code="EVP",
            item_agency="43",
            item_location=item_location,
            item_type="55",
        )


@pytest.mark.parametrize("item_location", [2, "MAP", ["MAP", "MAL"], None])
def test_item_location_invalid(item_location):
    with pytest.raises(ValidationError) as e:
        ItemRequired(
            material_type="monograph_record",
            item_call_tag="8528",
            item_call_no="ReCAP 23-100000",
            item_barcode="33333678901234",
            item_price="12.34",
            item_vendor_code="EVP",
            item_agency="43",
            item_location=item_location,
            item_type="55",
        )
    assert e.value.errors()[0]["type"] == "literal_error"


@pytest.mark.parametrize("item_type", ["2", "55"])
def test_item_type_valid(item_type):
    with does_not_raise():
        ItemRequired(
            material_type="monograph_record",
            item_call_tag="8528",
            item_call_no="ReCAP 23-100000",
            item_barcode="33333678901234",
            item_price="12.34",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmg2",
            item_type=item_type,
        )


@pytest.mark.parametrize("item_type", [2, 55])
def test_item_type_invalid(item_type):
    with pytest.raises(ValidationError) as e:
        ItemRequired(
            material_type="monograph_record",
            item_call_tag="8528",
            item_call_no="ReCAP 23-100000",
            item_barcode="33333678901234",
            item_price="12.34",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmg2",
            item_type=item_type,
        )
    assert e.value.errors()[0]["type"] == "string_type"
