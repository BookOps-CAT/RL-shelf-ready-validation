import pytest
from bookops_marc import Bib
from pymarc import Field, Subfield


@pytest.fixture
def valid_rl_monograph_record():
    valid_rl_monograph_record = {
        "material_type": "monograph_record",
        "bib_call_no_ind1": "8",
        "bib_call_no_ind2": " ",
        "bib_call_no": "ReCAP 23-999999",
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
        "items": [
            {
                "item_call_tag": "8528",
                "item_call_no": "ReCAP 23-999999",
                "item_barcode": "33433678901234",
                "item_price": "2.00",
                "item_vendor_code": "EVP",
                "item_location": "rcmb2",
                "item_type": "2",
                "item_agency": "43",
                "item_message": "FOO",
                "message": "BAR",
                "library": "RL",
                "item_ind1": " ",
                "item_ind2": "1",
            },
            {
                "item_call_tag": "8528",
                "item_call_no": "ReCAP 23-999998",
                "item_barcode": "33433678901234",
                "item_price": "2.00",
                "item_vendor_code": "EVP",
                "item_location": "rcmb2",
                "item_type": "2",
                "item_agency": "43",
                "library": "RL",
                "item_ind1": " ",
                "item_ind2": "1",
            },
        ],
    }
    return valid_rl_monograph_record


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


@pytest.fixture
def stub_record():
    bib = Bib()
    bib.leader = "00820cam a22001935i 4500"
    bib.add_field(Field(tag="008", data="190306s2017    ht a   j      000 1 hat d"))
    bib.add_field(Field(tag="001", data="on1381158740"))
    bib.add_field(
        Field(
            tag="050",
            indicators=["", "4"],
            subfields=[
                Subfield(code="a", value="DK504.73"),
                {"a": "DK504.73"},
                Subfield(code="b", value=".D86 2022"),
            ],
        )
    )
    bib.add_field(
        Field(
            tag="245",
            indicators=["0", "0"],
            subfields=[
                Subfield(code="a", value="Dunikas Laika grāmata 1812-1858 /"),
                Subfield(
                    code="c",
                    value="atbildīgā redaktore Anita Helviga ; sagatavotāji Agris Dzenis, Mihails Ignats, Inese Veisbuka.",
                ),
            ],
        )
    )
    bib.add_field(
        Field(
            tag="300",
            indicators=[" ", " "],
            subfields=[
                Subfield(code="a", value="200 pages :"),
            ],
        )
    )
    bib.add_field(
        Field(
            tag="600",
            indicators=["1", "0"],
            subfields=[
                Subfield(code="a", value="Mucenieks, Jānis,"),
                Subfield(code="d", value="1800-1885."),
                Subfield(code="t", value="Laika grāmata."),
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
            indicators=["", " "],
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
            tag="960",
            indicators=[" ", " "],
            subfields=[
                Subfield(code="s", value="100"),
                Subfield(code="t", value="MAL"),
                Subfield(code="u", value="123456apprv"),
            ],
        )
    )
    bib.add_field(
        Field(
            tag="980",
            indicators=[" ", " "],
            subfields=[
                Subfield(code="a", value="230918"),
                Subfield(code="b", value="100"),
                Subfield(code="c", value="100"),
                Subfield(code="d", value="000"),
                Subfield(code="e", value="100"),
                Subfield(code="f", value="20048818"),
                Subfield(code="g", value="1"),
            ],
        )
    )
    return bib
