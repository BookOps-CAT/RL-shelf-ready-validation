import pytest
from typing import TypedDict, Optional, Any


@pytest.fixture
def valid_nypl_rl_record():
    valid_nypl_rl_record = {
        "item": {
            "material_type": "monograph_record",
            "item_call_tag": "8528",
            "item_call_no": "ReCAP 23-999999",
            "item_barcode": "33433678901234",
            "item_price": "12.34",
            "item_vendor_code": "EVP",
            "item_location": "rcmb2",
            "item_type": "2",
            "item_agency": "43",
        },
        "order": {
            "order_location": "MAB",
            "order_price": "1234",
            "order_fund": "123456apprv",
        },
        "invoice": {
            "invoice_date": "240101",
            "invoice_price": "1234",
            "invoice_shipping": "100",
            "invoice_tax": "123",
            "invoice_net_price": "1234",
            "invoice_number": "1234567890",
            "invoice_copies": "1",
        },
        "bib_call_no": "ReCAP 23-999999",
        "bib_vendor_code": "EVP",
        "rl_identifier": "RL",
        "lcc": "Z123",
    }
    return valid_nypl_rl_record


@pytest.fixture
def valid_pamphlet_record():
    valid_pamphlet_record = {
        "item": {
            "material_type": "pamphlet",
        },
        "order": {
            "order_location": "MAB",
            "order_price": "1234",
            "order_fund": "123456apprv",
        },
        "invoice": {
            "invoice_date": "240101",
            "invoice_price": "1234",
            "invoice_shipping": "100",
            "invoice_tax": "123",
            "invoice_net_price": "1234",
            "invoice_number": "1234567890",
            "invoice_copies": "1",
        },
        "bib_vendor_code": "EVP",
        "rl_identifier": "RL",
        "lcc": "Z123",
    }
    return valid_pamphlet_record


@pytest.fixture
def string_barcode_error():
    string_barcode_error = {
        "type": "string_pattern_mismatch",
        "loc": ("item", "monograph_record", "item_barcode"),
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
        "loc": ("item", "monograph_record", "item_vendor_code"),
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
def stub_record_dict():
    stub_record_dict = {
        "leader": "00820cam a22001935i 4500",
        "001": ["on1381158740"],
        "050": [
            {
                "ind1": " ",
                "ind2": "4",
                "subfields": [{"a": "DK504.73"}, {"b": ".D86 2022"}],
            }
        ],
        "245": [
            {
                "ind1": "0",
                "ind2": "0",
                "subfields": [
                    {"a": "Dunikas Laika grāmata 1812-1858 /"},
                    {
                        "c": "atbildīgā redaktore Anita Helviga ; sagatavotāji Agris Dzenis, Mihails Ignats, Inese Veisbuka."
                    },
                ],
            }
        ],
        "300": [
            {
                "ind1": " ",
                "ind2": " ",
                "subfields": [
                    {"a": "248 pages :"},
                    {"b": "color illustrations, color maps, color photographs ;"},
                    {"c": "31 cm"},
                ],
            }
        ],
        "600": [
            {
                "ind1": "1",
                "ind2": "0",
                "subfields": [
                    {"a": "Mucenieks, Jānis,"},
                    {"d": "1800-1885."},
                    {"t": "Laika grāmata."},
                ],
            },
        ],
        "651": [
            {
                "ind1": " ",
                "ind2": "0",
                "subfields": [
                    {"a": "Latvia"},
                    {"x": "History"},
                    {"y": "19th century"},
                    {"v": "Sources."},
                ],
            },
        ],
        "852": [{"ind1": "8", "ind2": " ", "subfields": [{"h": "ReCAP 23-108996"}]}],
        "901": [{"ind1": " ", "ind2": " ", "subfields": [{"a": "EVP"}]}],
        "910": [{"ind1": " ", "ind2": " ", "subfields": [{"a": "RL"}]}],
        "949": [
            {
                "ind1": " ",
                "ind2": "1",
                "subfields": [
                    {"z": "8528"},
                    {"p": "7.77"},
                    {"v": "EVP"},
                    {"h": "43"},
                    {"a": "ReCAP 23-108996"},
                    {"l": "rc2ma"},
                    {"t": "55"},
                    {"i": "33433678901234"},
                ],
            }
        ],
        "960": [
            {
                "ind1": " ",
                "ind2": " ",
                "subfields": [
                    {"s": "8372"},
                    {"t": "MAL"},
                    {"u": "50108latv"},
                    {"d": "r"},
                    {"e": "f"},
                    {"i": "a"},
                    {"g": "q"},
                ],
            }
        ],
        "980": [
            {
                "ind1": " ",
                "ind2": " ",
                "subfields": [
                    {"a": "230918"},
                    {"b": "7700"},
                    {"c": "672"},
                    {"d": "000"},
                    {"e": "8372"},
                    {"f": "20048818"},
                    {"g": "1"},
                ],
            }
        ],
    }
    return stub_record_dict
