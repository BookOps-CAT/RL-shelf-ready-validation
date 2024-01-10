import pytest
from pydantic import ValidationError
from contextlib import nullcontext
from rl_sr_validation.models import ItemRequired, ItemNotRequired


@pytest.mark.parametrize("material_type", ["monograph_record"])
def test_monograph_type_valid(material_type):
    with nullcontext():
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


@pytest.mark.parametrize(
    "material_type",
    [
        "catalog_raissonne",
        "performing_arts_dance",
        "multipart",
        "incomplete_set",
        "pamphlet",
        "non-standard_binding_packaging",
    ],
)
def test_monograph_type_invalid(material_type):
    with pytest.raises(ValidationError):
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


@pytest.mark.parametrize(
    "material_type",
    [
        "catalogue_raissonne",
        "performing_arts_dance",
        "multipart",
        "incomplete_set",
        "pamphlet",
        "non-standard_binding_packaging",
    ],
)
def test_other_material_type_valid(material_type):
    with nullcontext():
        ItemNotRequired(material_type=material_type)


@pytest.mark.parametrize("material_type", ["monograph_record"])
def test_other_material_type_invalid(material_type):
    with pytest.raises(ValidationError):
        ItemNotRequired(
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


@pytest.mark.parametrize("item_call_tag", ["8528"])
def test_item_call_tag_valid(item_call_tag):
    with nullcontext():
        ItemRequired(
            material_type="monograph_record",
            item_call_tag=item_call_tag,
            item_call_no="ReCAP 23-100000",
            item_barcode="33333678901234",
            item_price="12.34",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmg2",
            item_type="55",
        )


@pytest.mark.parametrize("item_call_tag", ["852"])
def test_item_call_tag_invalid(item_call_tag):
    with pytest.raises(ValidationError):
        ItemRequired(
            material_type="monograph_record",
            item_call_tag=item_call_tag,
            item_call_no="ReCAP 23-100000",
            item_barcode="33333678901234",
            item_price="12.34",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmg2",
            item_type="55",
        )


@pytest.mark.parametrize(
    "item_call_no",
    ["ReCAP 23-100000", "ReCAP 23-111111", "ReCAP 23-123456", "ReCAP 23-999999"],
)
def test_item_call_no_valid(item_call_no):
    with nullcontext():
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
    ["23-100000", 23 - 111111, "ReCAP", None, "PG9050.17.E55"],
)
def test_item_call_no_invalid(item_call_no):
    with pytest.raises(ValidationError):
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
    "item_barcode", ["33433123456789", "34444123456789", "33333123456789"]
)
def test_item_barcode_valid(item_barcode):
    with nullcontext():
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
        None,
        "1234",
        "12345",
        "12345678901234",
        33433123456789,
        33433123456789.0,
        "333331234567.9",
    ],
)
def test_item_barcode_invalid(item_barcode):
    with pytest.raises(ValidationError):
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


@pytest.mark.parametrize("item_price", ["1.23", "12.34", "123.45"])
def test_item_price_valid(item_price):
    with nullcontext():
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
    with pytest.raises(ValidationError):
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


@pytest.mark.parametrize("item_volume", ["1", "2", "300", None])
def test_item_volume_valid(item_volume):
    with nullcontext():
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
    with pytest.raises(ValidationError):
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


@pytest.mark.parametrize("item_vendor_code", ["EVP", "AUXAM"])
def test_item_vendor_code_valid(item_vendor_code):
    with nullcontext():
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
    with pytest.raises(ValidationError):
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


@pytest.mark.parametrize("item_agency", ["43"])
def test_item_agency_valid(item_agency):
    with nullcontext():
        ItemRequired(
            material_type="monograph_record",
            item_call_tag="8528",
            item_call_no="ReCAP 23-100000",
            item_barcode="33333678901234",
            item_price="12.34",
            item_vendor_code="EVP",
            item_agency=item_agency,
            item_location="rcmg2",
            item_type="55",
        )


@pytest.mark.parametrize("item_agency", [1, 2, ["1", "2"], {"agency": "43"}])
def test_item_agency_invalid(item_agency):
    with pytest.raises(ValidationError):
        ItemRequired(
            material_type="monograph_record",
            item_call_tag="8528",
            item_call_no="ReCAP 23-100000",
            item_barcode="33333678901234",
            item_price="12.34",
            item_vendor_code="EVP",
            item_agency=item_agency,
            item_location="rcmg2",
            item_type="55",
        )


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
    with nullcontext():
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
    with pytest.raises(ValidationError):
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


@pytest.mark.parametrize("item_type", ["2", "55"])
def test_item_type_valid(item_type):
    with nullcontext():
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


@pytest.mark.parametrize("item_type", [1, ["1", "2"], {"item_type": "1"}, 55])
def test_item_type_invalid(item_type):
    with pytest.raises(ValidationError):
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
