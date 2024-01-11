import pytest


@pytest.fixture
def valid_bpl_record():
    valid_bpl_record = {
        "item": {
            "material_type": "monograph_record",
            "item_call_tag": "8528",
            "item_call_no": "ReCAP 23-999999",
            "item_barcode": "34444678901234",
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
    return valid_bpl_record


@pytest.fixture
def valid_nypl_bl_record():
    valid_nypl_bl_record = {
        "item": {
            "material_type": "monograph_record",
            "item_call_tag": "8582",
            "item_call_no": "ReCAP 23-999999",
            "item_barcode": "33333678901234",
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
    return valid_nypl_bl_record


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
def invalid_bpl_record():
    invalid_bpl_record = {
        "item": {
            "material_type": "monograph_record",
            "item_call_tag": "8528",
            "item_call_no": "ReCAP 23-999999",
            "item_barcode": "12345678901234",
            "item_price": "12.34",
            "item_vendor_code": "EVP",
            "item_location": "rcmb2",
            "item_type": "55",
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
    return invalid_bpl_record


@pytest.fixture
def invalid_nypl_bl_record():
    invalid_nypl_bl_record = {
        "item": {
            "material_type": "monograph_record",
            "item_call_tag": "8528",
            "item_call_no": "ReCAP 23-999999",
            "item_barcode": "12345678901234",
            "item_price": "12.34",
            "item_vendor_code": "EVP",
            "item_location": "rcmb2",
            "item_type": "55",
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
    return invalid_nypl_bl_record


@pytest.fixture
def invalid_nypl_rl_record():
    invalid_nypl_rl_record = {
        "item": {
            "material_type": "monograph_record",
            "item_call_tag": "8528",
            "item_call_no": "ReCAP 23-999999",
            "item_barcode": "12345678901234",
            "item_price": "12.34",
            "item_vendor_code": "EVP",
            "item_location": "rcmb2",
            "item_type": "55",
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
    return invalid_nypl_rl_record


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
def invalid_pamphlet_record():
    invalid_pamphlet_record = {
        "item": {
            "material_type": "pamphlet",
            "item_call_tag": "8528",
            "item_call_no": "ReCAP 23-999999",
            "item_barcode": "34444678901234",
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
    return invalid_pamphlet_record


@pytest.fixture
def missing_fields():
    missing_fields = {
        "item": {
            "material_type": "monograph_record",
            "item_call_tag": "8528",
            "item_call_no": "ReCAP 23-999999",
            "item_barcode": "34444678901234",
            "item_price": "12.34",
            "item_vendor_code": "EVP",
            "item_location": "rcmb2",
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
    return missing_fields
