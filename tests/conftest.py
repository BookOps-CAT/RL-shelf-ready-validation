import pytest
from bookops_marc import Bib
from pymarc import Field, Subfield
from shelf_ready_validator.models import (
    BibCallNoModel,
    BibVendorCodeModel,
    LCClassModel,
    LibraryFieldModel,
    OrderFieldModel,
    InvoiceFieldModel,
    ItemFieldModel,
    MALOrderItem,
)


@pytest.fixture
def mock_bib_call_no():
    return BibCallNoModel(ind1="8", ind2=" ", call_no="ReCAP 23-000000")


@pytest.fixture
def mock_bib_vendor_code():
    return BibVendorCodeModel(ind1=" ", ind2=" ", vendor_code="EVP")


@pytest.fixture
def mock_lc_class():
    return LCClassModel(ind1=" ", ind2="4", lcc="F00")


@pytest.fixture
def mock_library():
    return LibraryFieldModel(ind1=" ", ind2=" ", library="RL")


@pytest.fixture
def mock_order_field():
    return OrderFieldModel(
        ind1=" ",
        ind2=" ",
        order_price="100",
        order_location="MAL",
        order_fund="123456",
    )


@pytest.fixture
def mock_invoice_field():
    return InvoiceFieldModel(
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


@pytest.fixture
def mock_item_fields():
    return [
        ItemFieldModel(
            ind1=" ",
            ind2="1",
            item_call_tag="8528",
            item_call_no="ReCAP 23-000000",
            item_barcode="33433123456789",
            item_price="1.00",
            item_vendor_code="EVP",
            item_agency="43",
            item_location="rc2ma",
            item_type="55",
        )
    ]


@pytest.fixture
def mock_valid_order_item():
    return [
        MALOrderItem(order_loc="MAL", item_loc="rc2ma", item_type="55"),
    ]


@pytest.fixture
def valid_pamphlet_record():
    valid_pamphlet_record = {
        "material_type": "pamphlet",
        "bib_vendor_code": "EVP",
        "lcc": "Z123",
        "invoice_date": "240101",
        "invoice_price": "100",
        "invoice_shipping": "100",
        "invoice_tax": "000",
        "invoice_net_price": "200",
        "invoice_number": "1234567890",
        "invoice_copies": "1",
        "order_price": "200",
        "order_location": "MAB",
        "order_fund": "123456apprv",
        "order_ind1": " ",
        "order_ind2": " ",
        "library": "RL",
    }
    return valid_pamphlet_record


@pytest.fixture
def string_barcode_error():
    string_barcode_error = {
        "type": "string_pattern_mismatch",
        "loc": ("items", 0, "RL", "item_barcode"),
        "msg": "String should match pattern '^33433[0-9]{9}$|^33333[0-9]{9}$|^34444[0-9]{9}$'",
        "input": "12345678901234",
        "ctx": {"pattern": "^33433[0-9]{9}$|^33333[0-9]{9}$|^34444[0-9]{9}$"},
        "url": "https://errors.pydantic.dev/2.5/v/string_pattern_mismatch",
    }
    return string_barcode_error


@pytest.fixture
def vendor_code_error():
    vendor_code_error = {
        "type": "literal_error",
        "loc": ("items", 0, "RL", "item_barcode"),
        "msg": "Input should be 'EVP' or 'AUXAM'",
        "input": "EVIS",
        "ctx": {"expected": "'EVP' or 'AUXAM'"},
        "url": "https://errors.pydantic.dev/2.5/v/literal_error",
    }
    return vendor_code_error


@pytest.fixture
def extra_field_error():
    extra_field_error = {
        "type": "extra_forbidden",
        "loc": ("item", "pamphlet", "item_vendor_code"),
        "msg": "Extra inputs are not permitted",
        "input": "EVP",
        "url": "https://errors.pydantic.dev/2.5/v/extra_forbidden",
    }
    return extra_field_error


@pytest.fixture(scope="function")
def stub_record():
    bib = Bib()
    bib.leader = "00820cam a22001935i 4500"
    bib.add_field(Field(tag="008", data="190306s2017    ht a   j      000 1 hat d"))
    bib.add_field(Field(tag="001", data="on1381158740"))
    bib.add_field(
        Field(
            tag="050",
            indicators=[" ", "4"],
            subfields=[
                Subfield(code="a", value="DK504.73"),
            ],
        )
    )
    bib.add_field(
        Field(
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
    )
    bib.add_field(
        Field(
            tag="300",
            indicators=[" ", " "],
            subfields=[
                Subfield(code="a", value="100 pages :"),
            ],
        )
    )
    bib.add_field(
        Field(
            tag="852",
            indicators=["8", " "],
            subfields=[
                Subfield(code="h", value="ReCAP 23-100000"),
            ],
        )
    )
    bib.add_field(
        Field(
            tag="901",
            indicators=[" ", " "],
            subfields=[
                Subfield(code="a", value="EVP"),
            ],
        )
    )
    bib.add_field(
        Field(
            tag="910",
            indicators=[" ", " "],
            subfields=[
                Subfield(code="a", value="RL"),
            ],
        )
    )
    bib.add_field(
        Field(
            tag="949",
            indicators=[" ", "1"],
            subfields=[
                Subfield(code="z", value="8528"),
                Subfield(code="a", value="ReCAP 23-100000"),
                Subfield(code="c", value="1"),
                Subfield(code="h", value="43"),
                Subfield(code="i", value="33433123456789"),
                Subfield(code="l", value="rcmf2"),
                Subfield(code="m", value="bar"),
                Subfield(code="p", value="1.00"),
                Subfield(code="t", value="55"),
                Subfield(code="u", value="foo"),
                Subfield(code="v", value="AUXAM"),
            ],
        )
    )
    bib.add_field(
        Field(
            tag="960",
            indicators=[" ", " "],
            subfields=[
                Subfield(code="s", value="100"),
                Subfield(code="t", value="MAF"),
                Subfield(code="u", value="123456apprv"),
            ],
        )
    )
    bib.add_field(
        Field(
            tag="980",
            indicators=[" ", " "],
            subfields=[
                Subfield(code="a", value="240101"),
                Subfield(code="b", value="100"),
                Subfield(code="c", value="100"),
                Subfield(code="d", value="000"),
                Subfield(code="e", value="200"),
                Subfield(code="f", value="123456"),
                Subfield(code="g", value="1"),
            ],
        )
    )
    return bib


@pytest.fixture(scope="function")
def stub_record_with_dupes(stub_record):
    dupe_record = stub_record
    dupe_record.add_field(
        Field(tag="050", indicators=[" ", "4"], subfields=[Subfield("h", "foo")])
    )
    dupe_record.add_field(
        Field(tag="852", indicators=["8", " "], subfields=[Subfield("h", "foo")])
    )
    dupe_record.add_field(
        Field(tag="901", indicators=[" ", " "], subfields=[Subfield("a", "foo")])
    )
    dupe_record.add_field(
        Field(tag="910", indicators=[" ", " "], subfields=[Subfield("a", "foo")])
    )
    dupe_record.add_field(
        Field(tag="949", indicators=[" ", "1"], subfields=[Subfield("z", "foo")])
    )
    dupe_record.add_field(
        Field(tag="960", indicators=[" ", " "], subfields=[Subfield("s", "foo")])
    )
    dupe_record.add_field(
        Field(tag="980", indicators=[" ", " "], subfields=[Subfield("a", "foo")])
    )
    return dupe_record
