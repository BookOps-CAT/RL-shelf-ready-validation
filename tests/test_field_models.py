import pytest
from pydantic import ValidationError
from contextlib import nullcontext as does_not_raise
from shelf_ready_validator.marc_models import (
    BibCallNoModel,
    BibVendorCodeModel,
    LCClassModel,
    LibraryFieldModel,
    OrderFieldModel,
    InvoiceFieldModel,
    ItemFieldModel,
)


@pytest.mark.parametrize(
    "ind1_value, ind2_value, field_value",
    [
        (
            "8",
            " ",
            "ReCAP 23-000000",
        ),
        (
            "8",
            "",
            "ReCAP 24-000000",
        ),
        (
            "8",
            "",
            "ReCAP 25-000000",
        ),
    ],
)
def test_BibCallNoModel_valid(ind1_value, ind2_value, field_value):
    with does_not_raise():
        BibCallNoModel(ind1=ind1_value, ind2=ind2_value, call_no=field_value)


@pytest.mark.parametrize("field_value", ["foo", "bar", "ReCAP 11-111111"])
def test_BibCallNoModel_invalid_call_no(field_value):
    with pytest.raises(ValidationError) as e:
        BibCallNoModel(ind1="8", ind2=" ", call_no=field_value)
    assert e.value.errors()[0]["type"] == "string_pattern_mismatch"
    assert len(e.value.errors()) == 1


@pytest.mark.parametrize(
    "ind1_value, ind2_value",
    [
        (
            "1",
            "1",
        ),
        (
            "0",
            "0",
        ),
        (
            "2",
            "2",
        ),
    ],
)
def test_BibCallNoModel_invalid_indicators(ind1_value, ind2_value):
    with pytest.raises(ValidationError) as e:
        BibCallNoModel(ind1=ind1_value, ind2=ind2_value, call_no="ReCAP 23-000000")
    error_types = [i["type"] for i in e.value.errors()]
    assert error_types.count("literal_error") == 2
    assert len(e.value.errors()) == 2


@pytest.mark.parametrize(
    "ind1_value, ind2_value, field_value",
    [
        (" ", " ", "EVP"),
        ("", "", "AUXAM"),
        (" ", "", "LEILA"),
        ("", " ", "LEILA"),
    ],
)
def test_BibVendorCodeModel_valid(ind1_value, ind2_value, field_value):
    with does_not_raise():
        BibVendorCodeModel(ind1=ind1_value, ind2=ind2_value, vendor_code=field_value)


@pytest.mark.parametrize("field_value", ["foo", "bar", "baz"])
def test_BibVendorCodeModel_invalid_code(field_value):
    with pytest.raises(ValidationError) as e:
        BibVendorCodeModel(ind1=" ", ind2=" ", vendor_code=field_value)
    assert e.value.errors()[0]["type"] == "literal_error"
    assert len(e.value.errors()) == 1


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
            "0",
        ),
    ],
)
def test_BibVendorCodeModel_invalid_indicators(ind1_value, ind2_value):
    with pytest.raises(ValidationError) as e:
        BibVendorCodeModel(ind1=ind1_value, ind2=ind2_value, vendor_code="EVP")
    error_types = [i["type"] for i in e.value.errors()]
    assert error_types.count("literal_error") == 2
    assert len(e.value.errors()) == 2


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


@pytest.mark.parametrize(
    "ind1_value, ind2_value",
    [
        (
            "5",
            "6",
        ),
        (
            "7",
            "8",
        ),
        (
            "9",
            "1",
        ),
    ],
)
def test_LCClassModel_invalid_indicators(ind1_value, ind2_value):
    with pytest.raises(ValidationError) as e:
        LCClassModel(ind1=ind1_value, ind2=ind2_value, lcc="F00")
    error_types = [i["type"] for i in e.value.errors()]
    assert error_types.count("literal_error") == 2
    assert len(e.value.errors()) == 2


@pytest.mark.parametrize(
    "ind1_value, ind2_value",
    [
        (
            " ",
            "0",
        ),
        (
            "0",
            "4",
        ),
        (
            "",
            "0",
        ),
    ],
)
def test_LCClassModel_invalid_indicator_combo(ind1_value, ind2_value):
    with pytest.raises(ValidationError) as e:
        LCClassModel(ind1=ind1_value, ind2=ind2_value, lcc="F00")
    assert e.value.errors()[0]["type"] == "literal_error"
    assert len(e.value.errors()) == 1


@pytest.mark.parametrize(
    "ind1_value, ind2_value, field_value",
    [
        (" ", " ", "RL"),
        ("", "", "BL"),
        (" ", "", "BPL"),
        ("", " ", "RL"),
    ],
)
def test_LibraryFieldModel_valid(ind1_value, ind2_value, field_value):
    with does_not_raise():
        LibraryFieldModel(ind1=ind1_value, ind2=ind2_value, library=field_value)


@pytest.mark.parametrize(
    "field_value",
    ["foo", "bar", "baz"],
)
def test_LibraryFieldModel_invalid_library_field(field_value):
    with pytest.raises(ValidationError) as e:
        LibraryFieldModel(ind1=" ", ind2=" ", library=field_value)
    assert e.value.errors()[0]["type"] == "literal_error"
    assert len(e.value.errors()) == 1


@pytest.mark.parametrize(
    "ind1_value, ind2_value",
    [("1", "1"), ("2", "0"), ("0", "5")],
)
def test_LibraryFieldModel_invalid_indicators(ind1_value, ind2_value):
    with pytest.raises(ValidationError) as e:
        LibraryFieldModel(ind1=ind1_value, ind2=ind2_value, library="RL")
    error_types = [i["type"] for i in e.value.errors()]
    assert error_types.count("literal_error") == 2
    assert len(e.value.errors()) == 2


@pytest.mark.parametrize(
    "price_field, location_field, fund_field",
    [
        ("100", "MAB", "123456"),
        ("200", "MAF", "789000"),
        ("300", "MAG", "123"),
        ("100", "MAL", "111"),
        ("200", "MAP", "222"),
        ("300", "MAS", "333"),
        ("100", "PAD", "111"),
        ("200", "PAH", "222"),
        ("300", "PAM", "333"),
        ("100", "PAT", "111"),
        ("200", "SC", "222"),
    ],
)
def test_OrderFieldModel_valid(price_field, location_field, fund_field):
    with does_not_raise():
        OrderFieldModel(
            ind1=" ",
            ind2=" ",
            order_price=price_field,
            order_location=location_field,
            order_fund=fund_field,
        )


@pytest.mark.parametrize(
    "location_field",
    ["FOO", "BAR", "BAZ"],
)
def test_OrderFieldModel_invalid_location(location_field):
    with pytest.raises(ValidationError) as e:
        OrderFieldModel(
            ind1=" ",
            ind2=" ",
            order_price="100",
            order_location=location_field,
            order_fund="111",
        )
    assert e.value.errors()[0]["type"] == "literal_error"
    assert len(e.value.errors()) == 1


@pytest.mark.parametrize(
    "price_field, error_type",
    [("1.00", "string_pattern_mismatch"), (1.00, "string_type"), (1, "string_type")],
)
def test_OrderFieldModel_invalid_price(price_field, error_type):
    with pytest.raises(ValidationError) as e:
        OrderFieldModel(
            ind1=" ",
            ind2=" ",
            order_price=price_field,
            order_location="MAL",
            order_fund="111",
        )
    assert e.value.errors()[0]["type"] == error_type
    assert len(e.value.errors()) == 1


@pytest.mark.parametrize(
    "fund_field",
    [[], 1.00, 1, {}],
)
def test_OrderFieldModel_invalid_fund(fund_field):
    with pytest.raises(ValidationError) as e:
        OrderFieldModel(
            ind1=" ",
            ind2=" ",
            order_price="100",
            order_location="MAL",
            order_fund=fund_field,
        )
    assert e.value.errors()[0]["type"] == "string_type"
    assert len(e.value.errors()) == 1


@pytest.mark.parametrize(
    "ind1_value, ind2_value",
    [("1", "1"), ("2", "0"), ("0", "5")],
)
def test_OrderFieldModel_invalid_indicators(ind1_value, ind2_value):
    with pytest.raises(ValidationError) as e:
        OrderFieldModel(
            ind1=ind1_value,
            ind2=ind2_value,
            order_price="100",
            order_location="MAL",
            order_fund="111",
        )
    error_types = [i["type"] for i in e.value.errors()]
    assert error_types.count("literal_error") == 2
    assert len(e.value.errors()) == 2


@pytest.mark.parametrize(
    "ind1_value, ind2_value",
    [(" ", " "), ("", ""), (" ", ""), ("", " ")],
)
def test_InvoiceFieldModel_valid(ind1_value, ind2_value):
    with does_not_raise():
        InvoiceFieldModel(
            ind1=ind1_value,
            ind2=ind2_value,
            invoice_date="240101",
            invoice_price="100",
            invoice_shipping="0",
            invoice_tax="0",
            invoice_net_price="100",
            invoice_number="123456",
            invoice_copies="1",
        )


@pytest.mark.parametrize(
    "ind1_value, ind2_value",
    [("1", "1"), ("2", "0"), ("0", "5")],
)
def test_InvoiceFieldModel_invalid_indicators(ind1_value, ind2_value):
    with pytest.raises(ValidationError) as e:
        InvoiceFieldModel(
            ind1=ind1_value,
            ind2=ind2_value,
            invoice_date="240101",
            invoice_price="100",
            invoice_shipping="0",
            invoice_tax="0",
            invoice_net_price="100",
            invoice_number="123456",
            invoice_copies="1",
        )
    error_types = [i["type"] for i in e.value.errors()]
    assert error_types.count("literal_error") == 2
    assert len(e.value.errors()) == 2


@pytest.mark.parametrize(
    "field_value",
    ["2024-01-01", "2024-01-01T00:00:00", "Jan 1, 2024", "01/01/2024", "01-01-2024"],
)
def test_InvoiceFieldModel_invalid_invoice_date(field_value):
    with pytest.raises(ValidationError) as e:
        InvoiceFieldModel(
            ind1=" ",
            ind2=" ",
            invoice_date=field_value,
            invoice_price="100",
            invoice_shipping="0",
            invoice_tax="0",
            invoice_net_price="100",
            invoice_number="123456",
            invoice_copies="1",
        )
    assert e.value.errors()[0]["type"] == "string_pattern_mismatch"
    assert len(e.value.errors()) == 1


@pytest.mark.parametrize(
    "price_field, error_type",
    [("1.00", "string_pattern_mismatch"), (1.00, "string_type"), (1, "string_type")],
)
def test_InvoiceFieldModel_invalid_prices(price_field, error_type):
    with pytest.raises(ValidationError) as e:
        InvoiceFieldModel(
            ind1=" ",
            ind2=" ",
            invoice_date="240101",
            invoice_price=price_field,
            invoice_shipping=price_field,
            invoice_tax=price_field,
            invoice_net_price=price_field,
            invoice_number="123456",
            invoice_copies="1",
        )
    error_types = [i["type"] for i in e.value.errors()]
    assert error_types.count(error_type) == 4
    assert len(e.value.errors()) == 4


@pytest.mark.parametrize(
    "field_value",
    [[], 1, {}],
)
def test_InvoiceFieldModel_invalid_invoice_number(field_value):
    with pytest.raises(ValidationError) as e:
        InvoiceFieldModel(
            ind1=" ",
            ind2=" ",
            invoice_date="240101",
            invoice_price="100",
            invoice_shipping="0",
            invoice_tax="0",
            invoice_net_price="100",
            invoice_number=field_value,
            invoice_copies="1",
        )
    assert e.value.errors()[0]["type"] == "string_type"
    assert len(e.value.errors()) == 1


@pytest.mark.parametrize(
    "copies_field, error_type",
    [
        ("a", "string_pattern_mismatch"),
        (1, "string_type"),
        ("1a", "string_pattern_mismatch"),
    ],
)
def test_InvoiceFieldModel_invalid_invoice_copies(copies_field, error_type):
    with pytest.raises(ValidationError) as e:
        InvoiceFieldModel(
            ind1=" ",
            ind2=" ",
            invoice_date="240101",
            invoice_price="100",
            invoice_shipping="0",
            invoice_tax="0",
            invoice_net_price="100",
            invoice_number="123456",
            invoice_copies=copies_field,
        )
    assert e.value.errors()[0]["type"] == error_type
    assert len(e.value.errors()) == 1


def test_ItemFieldModel_valid():
    with does_not_raise():
        ItemFieldModel(
            ind1=" ",
            ind2="1",
            item_call_tag="8528",
            item_call_no="ReCAP 23-000000",
            item_barcode="33433123456789",
            item_price="1.00",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmb2",
            item_type="2",
        )


@pytest.mark.parametrize(
    "call_no_value",
    ["ReCAP 23-000000", "ReCAP 24-000000", "ReCAP 25-000000"],
)
def test_ItemFieldModel_valid_call_nos(call_no_value):
    with does_not_raise():
        ItemFieldModel(
            ind1=" ",
            ind2="1",
            item_call_tag="8528",
            item_call_no=call_no_value,
            item_barcode="33433123456789",
            item_price="1.00",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmb2",
            item_type="2",
        )


@pytest.mark.parametrize(
    "vendor_code_value",
    ["EVP", "AUXAM", "LEILA"],
)
def test_ItemFieldModel_valid_vendor_code(vendor_code_value):
    with does_not_raise():
        ItemFieldModel(
            ind1=" ",
            ind2="1",
            item_call_tag="8528",
            item_call_no="ReCAP 23-000000",
            item_barcode="33433123456789",
            item_price="1.00",
            item_vendor_code=vendor_code_value,
            item_agency="43",
            item_location="rcmb2",
            item_type="2",
        )


@pytest.mark.parametrize(
    "item_location_value",
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
def test_ItemFieldModel_valid_item_location(item_location_value):
    with does_not_raise():
        ItemFieldModel(
            ind1=" ",
            ind2="1",
            item_call_tag="8528",
            item_call_no="ReCAP 23-000000",
            item_barcode="33433123456789",
            item_price="1.00",
            item_vendor_code="EVP",
            item_agency="43",
            item_location=item_location_value,
            item_type="2",
        )


@pytest.mark.parametrize(
    "item_type_value",
    [
        "2",
        "55",
    ],
)
def test_ItemFieldModel_valid_item_type(item_type_value):
    with does_not_raise():
        ItemFieldModel(
            ind1=" ",
            ind2="1",
            item_call_tag="8528",
            item_call_no="ReCAP 23-000000",
            item_barcode="33433123456789",
            item_price="1.00",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmb2",
            item_type=item_type_value,
        )


@pytest.mark.parametrize(
    "ind1_value, ind2_value",
    [("1", " "), ("2", "0"), ("0", "5")],
)
def test_ItemFieldModel_invalid_indicators(ind1_value, ind2_value):
    with pytest.raises(ValidationError) as e:
        ItemFieldModel(
            ind1=ind1_value,
            ind2=ind2_value,
            item_call_tag="8528",
            item_call_no="ReCAP 23-000000",
            item_barcode="33433123456789",
            item_price="1.00",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmb2",
            item_type="2",
        )
    error_types = [i["type"] for i in e.value.errors()]
    assert error_types.count("literal_error") == 2
    assert len(e.value.errors()) == 2


@pytest.mark.parametrize(
    "call_tag_value",
    ["8520", "1111", "foo"],
)
def test_ItemFieldModel_invalid_call_tag(call_tag_value):
    with pytest.raises(ValidationError) as e:
        ItemFieldModel(
            ind1=" ",
            ind2="1",
            item_call_tag=call_tag_value,
            item_call_no="ReCAP 24-000000",
            item_barcode="33433123456789",
            item_price="1.00",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmb2",
            item_type="2",
        )
    assert e.value.errors()[0]["type"] == "literal_error"
    assert len(e.value.errors()) == 1


@pytest.mark.parametrize(
    "call_no_value",
    ["ReCAP 23-", "ReCAP", "ReCAP 00-000000", "ReCAP 24-0"],
)
def test_ItemFieldModel_invalid_call_nos(call_no_value):
    with pytest.raises(ValidationError) as e:
        ItemFieldModel(
            ind1=" ",
            ind2="1",
            item_call_tag="8528",
            item_call_no=call_no_value,
            item_barcode="33433123456789",
            item_price="1.00",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmb2",
            item_type="2",
        )
    assert e.value.errors()[0]["type"] == "string_pattern_mismatch"
    assert len(e.value.errors()) == 1


@pytest.mark.parametrize(
    "vendor_code_value",
    ["FOO", "BAR", "BAZ"],
)
def test_ItemFieldModel_invalid_vendor_code(vendor_code_value):
    with pytest.raises(ValidationError) as e:
        ItemFieldModel(
            ind1=" ",
            ind2="1",
            item_call_tag="8528",
            item_call_no="ReCAP 23-000000",
            item_barcode="33433123456789",
            item_price="1.00",
            item_vendor_code=vendor_code_value,
            item_agency="43",
            item_location="rcmb2",
            item_type="2",
        )
    assert e.value.errors()[0]["type"] == "literal_error"
    assert len(e.value.errors()) == 1


@pytest.mark.parametrize(
    "item_location_value",
    ["MAL", "foo", "bar"],
)
def test_ItemFieldModel_invalid_item_location(item_location_value):
    with pytest.raises(ValidationError) as e:
        ItemFieldModel(
            ind1=" ",
            ind2="1",
            item_call_tag="8528",
            item_call_no="ReCAP 23-000000",
            item_barcode="33433123456789",
            item_price="1.00",
            item_vendor_code="EVP",
            item_agency="43",
            item_location=item_location_value,
            item_type="2",
        )
    assert e.value.errors()[0]["type"] == "literal_error"
    assert len(e.value.errors()) == 1


@pytest.mark.parametrize(
    "item_type_value",
    ["monograph", 2, 55, 2.0],
)
def test_ItemFieldModel_invalid_item_type(item_type_value):
    with pytest.raises(ValidationError) as e:
        ItemFieldModel(
            ind1=" ",
            ind2="1",
            item_call_tag="8528",
            item_call_no="ReCAP 23-000000",
            item_barcode="33433123456789",
            item_price="1.00",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rcmb2",
            item_type=item_type_value,
        )
    assert e.value.errors()[0]["type"] == "literal_error"
    assert len(e.value.errors()) == 1
