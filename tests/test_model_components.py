import pytest
from pydantic import ValidationError
from contextlib import nullcontext as does_not_raise
from shelf_ready_validator.models import (
    BibCallNoModel,
    BibVendorCodeModel,
    LCClassModel,
    LibraryFieldModel,
    OrderFieldModel,
    InvoiceFieldModel,
    ItemFieldModel,
    MABMASOrderItem,
    MAFOrderItem,
    MAGOrderItem,
    MALOrderItem,
    MAPOrderItem,
    PAHOrderItem,
    PAMOrderItem,
    PATOrderItem,
    SCOrderItem,
    VendorMonographRecordModel,
)


@pytest.mark.parametrize(
    "call_no_value", ["ReCAP 23-000000", "ReCAP 24-000000", "ReCAP 25-000000"]
)
def test_BibCallNoModel_valid(call_no_value):
    with does_not_raise():
        BibCallNoModel(ind1="8", ind2=" ", call_no=call_no_value)


@pytest.mark.parametrize("field_value", ["foo", "bar", "ReCAP 11-111111"])
def test_BibCallNoModel_invalid_call_no(field_value):
    with pytest.raises(ValidationError) as e:
        BibCallNoModel(ind1="8", ind2=" ", call_no=field_value)
    assert e.value.errors()[0]["type"] == "string_pattern_mismatch"


@pytest.mark.parametrize(
    "ind1_value, ind2_value",
    [
        (
            "1",
            "1",
        ),
        (
            "8",
            "0",
        ),
        (
            "1",
            " ",
        ),
    ],
)
def test_BibCallNoModel_invalid_indicators(ind1_value, ind2_value):
    with pytest.raises(ValidationError) as e:
        BibCallNoModel(ind1=ind1_value, ind2=ind2_value, call_no="ReCAP 23-000000")
    assert e.value.errors()[0]["type"] == "literal_error"


@pytest.mark.parametrize("vendor_code_value", ["EVP", "AUXAM", "LEILA"])
def test_BibVendorCodeModel_valid(vendor_code_value):
    with does_not_raise():
        BibVendorCodeModel(ind1=" ", ind2=" ", vendor_code=vendor_code_value)


@pytest.mark.parametrize(
    "ind1_value, ind2_value",
    [
        (
            " ",
            "4",
        ),
        (
            "0",
            "0",
        ),
        (
            "1",
            "0",
        ),
    ],
)
def test_LCClassModel_valid(ind1_value, ind2_value):
    with does_not_raise():
        LCClassModel(ind1=ind1_value, ind2=ind2_value, lcc="F00")


@pytest.mark.parametrize("library_value", ["RL", "BL", "BPL"])
def test_LibraryFieldModel_valid(library_value):
    with does_not_raise():
        LibraryFieldModel(ind1=" ", ind2=" ", library=library_value)


@pytest.mark.parametrize(
    "order_location_value",
    ["MAB", "MAF", "MAG", "MAL", "MAP", "MAS", "PAD", "PAH", "PAM", "PAT", "SC"],
)
def test_OrderFieldModel_valid(order_location_value):
    with does_not_raise():
        OrderFieldModel(
            ind1=" ",
            ind2=" ",
            order_price="100",
            order_location=order_location_value,
            order_fund="123456",
        )


def test_InvoiceFieldModel_valid():
    with does_not_raise():
        InvoiceFieldModel(
            ind1=" ",
            ind2=" ",
            invoice_date="240101",
            invoice_price="100",
            invoice_shipping="0",
            invoice_tax="0",
            invoice_net_price="100",
            invoice_number="123456",
            invoice_copies="1",
        )


@pytest.mark.parametrize(
    "call_no_value, vendor_code_value, loc_value, type_value",
    [
        ("ReCAP 23-000000", "EVP", "rcmb2", "2"),
        ("ReCAP 24-000000", "AUXAM", "rcmf2", "55"),
        ("ReCAP 25-000000", "LEILA", "rcmg2", None),
    ],
)
def test_ItemFieldModel_valid(call_no_value, vendor_code_value, loc_value, type_value):
    with does_not_raise():
        ItemFieldModel(
            ind1=" ",
            ind2="1",
            item_call_tag="8528",
            item_call_no=call_no_value,
            item_barcode="33433123456789",
            item_price="1.00",
            item_vendor_code=vendor_code_value,
            item_agency="43",
            item_location=loc_value,
            item_type=type_value,
        )


@pytest.mark.parametrize(
    "order_loc_value",
    ["MAB", "MAS"],
)
def test_MABMASOrderItem_valid(order_loc_value):
    with does_not_raise():
        MABMASOrderItem(order_loc=order_loc_value, item_loc="rcmb2", item_type="2")


@pytest.mark.parametrize(
    "item_type_value",
    ["55", None],
)
def test_MAFOrderItem_valid(item_type_value):
    with does_not_raise():
        MAFOrderItem(order_loc="MAF", item_loc="rcmf2", item_type=item_type_value)


@pytest.mark.parametrize(
    "item_type_value",
    ["55", None],
)
def test_MAGOrderItem_valid(item_type_value):
    with does_not_raise():
        MAGOrderItem(order_loc="MAG", item_loc="rcmg2", item_type=item_type_value)


@pytest.mark.parametrize(
    "item_loc_value,item_type_value",
    [
        ("rc2ma", "55"),
        ("rc2ma", None),
        (None, "55"),
        (None, None),
    ],
)
def test_MALOrderItem_valid(item_loc_value, item_type_value):
    with does_not_raise():
        MALOrderItem(
            order_loc="MAL", item_loc=item_loc_value, item_type=item_type_value
        )


def test_MAPOrderItem_valid():
    with does_not_raise():
        MAPOrderItem(order_loc="MAP", item_loc="rcmp2", item_type="2")


@pytest.mark.parametrize(
    "item_type_value",
    ["55", None],
)
def test_PAHOrderItem_valid(item_type_value):
    with does_not_raise():
        PAHOrderItem(order_loc="PAH", item_loc="rcph2", item_type=item_type_value)


@pytest.mark.parametrize(
    "item_type_value",
    ["55", None],
)
def test_PAMOrderItem_valid(item_type_value):
    with does_not_raise():
        PAMOrderItem(order_loc="PAM", item_loc="rcpm2", item_type=item_type_value)


@pytest.mark.parametrize(
    "item_type_value",
    ["55", None],
)
def test_PATOrderItem_valid(item_type_value):
    with does_not_raise():
        PATOrderItem(order_loc="PAT", item_loc="rcpt2", item_type=item_type_value)


@pytest.mark.parametrize(
    "item_type_value",
    ["55", None],
)
def test_SCOrderItem_valid(item_type_value):
    with does_not_raise():
        SCOrderItem(order_loc="SC", item_loc="rc2cf", item_type=item_type_value)


def test_VendorMonographRecordModel_valid(
    mock_bib_call_no,
    mock_bib_vendor_code,
    mock_lc_class,
    mock_library,
    mock_order_field,
    mock_invoice_field,
    mock_item_fields,
    mock_valid_order_item,
):
    with does_not_raise():
        VendorMonographRecordModel(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_call_no=mock_bib_call_no,
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type="monograph_record",
            order_field=mock_order_field,
            invoice_field=mock_invoice_field,
            item_fields=mock_item_fields,
            order_item_data=mock_valid_order_item,
        )


@pytest.mark.parametrize(
    "leader_value, leader_error",
    [
        ("foo", "string_too_short"),
        ("bar", "string_too_short"),
        ("foobarfoobarfoobarfoobar", "string_pattern_mismatch"),
    ],
)
def test_VendorMonographRecordModel_invalid_leader(
    mock_bib_call_no,
    mock_bib_vendor_code,
    mock_lc_class,
    mock_library,
    mock_order_field,
    mock_invoice_field,
    mock_item_fields,
    mock_valid_order_item,
    leader_value,
    leader_error,
):
    with pytest.raises(ValidationError) as e:
        VendorMonographRecordModel(
            leader=leader_value,
            fields=[{"245": {"a": "The Title"}}],
            bib_call_no=mock_bib_call_no,
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type="monograph_record",
            order_field=mock_order_field,
            invoice_field=mock_invoice_field,
            item_fields=mock_item_fields,
            order_item_data=mock_valid_order_item,
        )
    assert e.value.errors()[0]["type"] == leader_error
