import pytest


@pytest.fixture
def invalid_record():
    invalid_record = {
        "item": {
            "item_call_tag": "8582",
            "item_call_no": "ReCAP 23-999999",
            "item_barcode": "12345678901234",
            "item_price": "12.34",
            "item_vendor_code": "EVIS",
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
    return invalid_record


@pytest.fixture
def valid_record():
    valid_record = {
        "item": {
            "item_call_tag": "8528",
            "item_call_no": "ReCAP 23-999999",
            "item_barcode": "12345678901234",
            "item_price": "12.34",
            "item_vendor_code": "EVIS",
            "item_location": "rcmb2",
            "item_type": "2",
            "item_agency": "43",
        },
        "order": {
            "order_location": "MAB",
            "order_price": "1234",
            "order_fund": "123456apprv",
        },
        "bib_call_no": "ReCAP 23-999999",
        "bib_vendor_code": "EVP",
        "rl_identifier": "RL",
        "lcc": "Z123",
        "invoice": {
            "invoice_date": "240101",
            "invoice_price": "1234",
            "invoice_shipping": "100",
            "invoice_tax": "123",
            "invoice_net_price": "1234",
            "invoice_number": "1234567890",
            "invoice_copies": "1",
        },
    }
    return valid_record
