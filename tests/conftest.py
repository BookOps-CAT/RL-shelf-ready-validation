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
