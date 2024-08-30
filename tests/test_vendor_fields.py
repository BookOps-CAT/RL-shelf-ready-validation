from pymarc import Field, Subfield
from shelf_ready_validator.vendor_fields import (
    get_subfield_from_field,
    BibCallNo,
    BibVendorCode,
    LCClass,
    Library,
    Order,
    Invoice,
    Item,
)


def test_get_subfield_from_field():
    field_245 = Field(
        tag="245",
        indicators=["0", "0"],
        subfields=[
            Subfield(code="a", value="Title :"),
            Subfield(
                code="b",
                value="subtitle /",
            ),
            Subfield(
                code="c",
                value="Author",
            ),
        ],
    )
    field_020 = Field(
        tag="020",
        indicators=[" ", " "],
        subfields=[
            Subfield(code="a", value="9781234567890"),
            Subfield(
                code="z",
                value="9781111111111",
            ),
            Subfield(
                code="z",
                value="9782222222222",
            ),
        ],
    )
    assert get_subfield_from_field(field_245, "a") == "Title :"
    assert get_subfield_from_field(field_245, "b") == "subtitle /"
    assert get_subfield_from_field(field_245, "c") == "Author"
    assert get_subfield_from_field(field_020, "z") == ["9781111111111", "9782222222222"]


def test_BibCallNo():
    bib_1 = BibCallNo(ind1="8", ind2=" ", call_no="ReCAP 23-000000")
    bib_2 = BibCallNo(ind1="8", ind2=" ", call_no=None)
    pymarc_field = Field(
        tag="852",
        indicators=["8", " "],
        subfields=[Subfield(code="h", value="ReCAP 24-111111")],
    )
    bib_3 = BibCallNo(ind1=None, ind2=None, call_no=None)
    assert bib_1.filter_none_vals() == {
        "ind1": "8",
        "ind2": " ",
        "call_no": "ReCAP 23-000000",
    }
    assert bib_2.filter_none_vals() == {"ind1": "8", "ind2": " "}
    assert bib_3.filter_none_vals() == {}
    assert BibCallNo.from_marc_field(pymarc_field) == BibCallNo(
        ind1="8", ind2=" ", call_no="ReCAP 24-111111"
    )


def test_BibVendorCode():
    vendor_1 = BibVendorCode(ind1=" ", ind2=" ", vendor_code="EVP")
    vendor_2 = BibVendorCode(ind1=" ", ind2=" ", vendor_code=None)
    vendor_3 = BibVendorCode(ind1=None, ind2=None, vendor_code=None)
    pymarc_field = Field(
        tag="901",
        indicators=[" ", " "],
        subfields=[Subfield(code="a", value="LEILA")],
    )
    assert vendor_1.filter_none_vals() == {
        "ind1": " ",
        "ind2": " ",
        "vendor_code": "EVP",
    }
    assert vendor_2.filter_none_vals() == {"ind1": " ", "ind2": " "}
    assert vendor_3.filter_none_vals() == {}
    assert BibVendorCode.from_marc_field(pymarc_field) == BibVendorCode(
        ind1=" ", ind2=" ", vendor_code="LEILA"
    )


def test_LCClass():
    lc_1 = LCClass(ind1=" ", ind2=" ", lcc="foo")
    lc_2 = LCClass(ind1=" ", ind2=" ", lcc=None)
    lc_3 = LCClass(ind1=None, ind2=None, lcc=None)
    pymarc_field = Field(
        tag="050",
        indicators=[" ", "4"],
        subfields=[
            Subfield(code="a", value="DK504.73"),
        ],
    )
    assert lc_1.filter_none_vals() == {
        "ind1": " ",
        "ind2": " ",
        "lcc": "foo",
    }
    assert lc_2.filter_none_vals() == {"ind1": " ", "ind2": " "}
    assert lc_3.filter_none_vals() == {}
    assert LCClass.from_marc_field(pymarc_field) == LCClass(
        ind1=" ", ind2="4", lcc="DK504.73"
    )


def test_Library():
    library_1 = Library(ind1=" ", ind2=" ", library="foo")
    library_2 = Library(ind1=" ", ind2=" ", library=None)
    library_3 = Library(ind1=None, ind2=None, library=None)
    pymarc_field = Field(
        tag="910",
        indicators=[" ", " "],
        subfields=[
            Subfield(code="a", value="RL"),
        ],
    )
    assert library_1.filter_none_vals() == {
        "ind1": " ",
        "ind2": " ",
        "library": "foo",
    }
    assert library_2.filter_none_vals() == {"ind1": " ", "ind2": " "}
    assert library_3.filter_none_vals() == {}
    assert Library.from_marc_field(pymarc_field) == Library(
        ind1=" ", ind2=" ", library="RL"
    )


def test_Order():
    order_1 = Order(
        ind1=" ", ind2=" ", order_price="100", order_location="MAL", order_fund="123456"
    )
    order_2 = Order(
        ind1=" ", ind2=" ", order_price=None, order_location=None, order_fund=None
    )
    order_3 = Order(
        ind1=None, ind2=None, order_price=None, order_location=None, order_fund=None
    )
    pymarc_field = Field(
        tag="960",
        indicators=[" ", " "],
        subfields=[
            Subfield(code="s", value="200"),
            Subfield(code="t", value="MAP"),
            Subfield(code="u", value="123"),
        ],
    )
    assert order_1.filter_none_vals() == {
        "ind1": " ",
        "ind2": " ",
        "order_price": "100",
        "order_location": "MAL",
        "order_fund": "123456",
    }
    assert order_2.filter_none_vals() == {"ind1": " ", "ind2": " "}
    assert order_3.filter_none_vals() == {}
    assert Order.from_marc_field(pymarc_field) == Order(
        ind1=" ", ind2=" ", order_price="200", order_location="MAP", order_fund="123"
    )


def test_Invoice():
    invoice_1 = Invoice(
        ind1=" ",
        ind2=" ",
        invoice_date="240701",
        invoice_price="500",
        invoice_shipping="100",
        invoice_tax="200",
        invoice_number="12",
        invoice_net_price="800",
        invoice_copies="5",
    )
    invoice_2 = Invoice(
        ind1=" ",
        ind2=" ",
        invoice_date="240801",
        invoice_price=None,
        invoice_shipping=None,
        invoice_tax="200",
        invoice_number="11",
        invoice_net_price="1300",
        invoice_copies="1",
    )
    invoice_3 = Invoice(
        ind1=None,
        ind2=None,
        invoice_date=None,
        invoice_price=None,
        invoice_shipping=None,
        invoice_tax=None,
        invoice_number=None,
        invoice_net_price=None,
        invoice_copies=None,
    )
    pymarc_field = Field(
        tag="980",
        indicators=[" ", " "],
        subfields=[
            Subfield(code="a", value="240101"),
            Subfield(code="b", value="300"),
            Subfield(code="c", value="100"),
            Subfield(code="d", value="100"),
            Subfield(code="e", value="2"),
            Subfield(code="f", value="500"),
            Subfield(code="g", value="1"),
        ],
    )
    assert invoice_1.filter_none_vals() == {
        "ind1": " ",
        "ind2": " ",
        "invoice_date": "240701",
        "invoice_price": "500",
        "invoice_shipping": "100",
        "invoice_tax": "200",
        "invoice_net_price": "800",
        "invoice_number": "12",
        "invoice_copies": "5",
    }
    assert invoice_2.filter_none_vals() == {
        "ind1": " ",
        "ind2": " ",
        "invoice_date": "240801",
        "invoice_tax": "200",
        "invoice_net_price": "1300",
        "invoice_number": "11",
        "invoice_copies": "1",
    }
    assert invoice_3.filter_none_vals() == {}

    assert Invoice.from_marc_field(pymarc_field) == Invoice(
        ind1=" ",
        ind2=" ",
        invoice_date="240101",
        invoice_price="300",
        invoice_shipping="100",
        invoice_tax="100",
        invoice_net_price="2",
        invoice_number="500",
        invoice_copies="1",
    )


def test_Item():
    item_1 = Item(
        ind1=" ",
        ind2="1",
        item_call_tag="8528",
        item_call_no="ReCAP 23-000000",
        item_barcode="33433987654321",
        item_price="1.00",
        item_message="foo",
        message="bar",
        item_vendor_code="EVP",
        item_agency="43",
        item_location="rcmb2",
        item_volume="1",
        item_type="2",
    )
    item_2 = Item(
        ind1=" ",
        ind2="1",
        item_call_tag="8528",
        item_call_no="ReCAP 24-000000",
        item_barcode="33433123456789",
        item_price="1.00",
        item_message="foo",
        message="bar",
        item_vendor_code="EVP",
        item_agency="43",
        item_location="rcmf2",
        item_volume=None,
        item_type=None,
    )
    item_3 = Item(
        ind1=None,
        ind2=None,
        item_call_tag=None,
        item_call_no=None,
        item_barcode=None,
        item_price=None,
        item_message=None,
        message=None,
        item_vendor_code=None,
        item_agency=None,
        item_location=None,
        item_volume=None,
        item_type=None,
    )
    pymarc_field = Field(
        tag="960",
        indicators=[" ", "1"],
        subfields=[
            Subfield(code="z", value="8528"),
            Subfield(code="a", value="ReCAP 24-999999"),
            Subfield(code="i", value="33433000000000"),
            Subfield(code="p", value="2.00"),
            Subfield(code="v", value="AUXAM"),
            Subfield(code="h", value="43"),
            Subfield(code="l", value="rcmf2"),
            Subfield(code="t", value="55"),
            Subfield(code="c", value="1"),
            Subfield(code="u", value="foo"),
            Subfield(code="m", value="bar"),
        ],
    )
    assert item_1.filter_none_vals() == {
        "ind1": " ",
        "ind2": "1",
        "item_call_tag": "8528",
        "item_call_no": "ReCAP 23-000000",
        "item_barcode": "33433987654321",
        "item_price": "1.00",
        "item_message": "foo",
        "message": "bar",
        "item_vendor_code": "EVP",
        "item_agency": "43",
        "item_location": "rcmb2",
        "item_volume": "1",
        "item_type": "2",
    }
    assert item_2.filter_none_vals() == {
        "ind1": " ",
        "ind2": "1",
        "item_call_tag": "8528",
        "item_call_no": "ReCAP 24-000000",
        "item_barcode": "33433123456789",
        "item_price": "1.00",
        "item_message": "foo",
        "message": "bar",
        "item_vendor_code": "EVP",
        "item_agency": "43",
        "item_location": "rcmf2",
    }
    assert item_3.filter_none_vals() == {}
    assert Item.from_marc_field(pymarc_field) == Item(
        ind1=" ",
        ind2="1",
        item_call_tag="8528",
        item_call_no="ReCAP 24-999999",
        item_barcode="33433000000000",
        item_price="2.00",
        item_message="foo",
        message="bar",
        item_vendor_code="AUXAM",
        item_agency="43",
        item_location="rcmf2",
        item_volume="1",
        item_type="55",
    )
