from src.validate.models import Record

from src.validate.errors import convert_error_messages

# import src.cli.commands
from pydantic import ValidationError
from rich import print


invalid_monograph_record = {
    "item": {
        "material_type": "monograph_record",
        "item_call_tag": "8582",
        "item_barcode": "33433678901234",
        "item_price": "12.34",
        "item_vendor_code": "EVIS",
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
    "rl_identifier": "RLRL",
    "lcc": "Z123",
}

invalid_pamphlet_record = {
    "item": {
        "material_type": "pamphlet",
        "item_call_tag": "8528",
    },
    "order": {
        "order_location": "AAA",
        "order_price": "1234",
        "order_fund": "123456apprv",
    },
    "invoice": {
        "invoice_date": "240101",
        "invoice_price": "1234",
        "invoice_shipping": "1.00",
        "invoice_tax": "1.23",
        "invoice_net_price": "1234",
        "invoice_number": "1234567890",
    },
    "bib_call_no": "ReCAP 23-99999",
    "bib_vendor_code": "EVIS",
    "rl_identifier": "RLRL",
    "lcc": "Z123",
}
records = [invalid_monograph_record, invalid_pamphlet_record]
for record in records:
    try:
        r = Record(**record)
        print("Record validates.")
    except ValidationError as e:
        converted = convert_error_messages(e)
        total_error_count = len(converted)
        output = f"This record contains {total_error_count} errors: {converted}"
        print(output)
