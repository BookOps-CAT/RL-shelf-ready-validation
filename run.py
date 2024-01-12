from src.validate.models import Record
import click
import json
from pydantic import ValidationError
from rich import print


valid_bpl_record = {
    "item": {
        "material_type": "monograph_record",
        "item_call_tag": "8528",
        "item_call_no": "ReCAP 23-999999",
        "item_barcode": "34444678901234",
        "item_price": "12.34",
        "item_vendor_code": "EVP",
        "item_location": "aaaaa",
        "item_type": "2",
        "item_agency": "43",
    },
    "order": {
        "order_location": "aaa",
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
    "bib_vendor_code": "EVIS",
    "rl_identifier": "RLRL",
    "lcc": "Z123",
}
# valid_bpl_record["invoice"]["invoice_price"] = "2.00"
try:
    r = Record(**valid_bpl_record)
    print(f"Record validates.")
    # return validated_record
except ValidationError as e:
    # new_errors = convert_error_messages(e)
    # parsed_errors = parse_errors(e.errors())
    # print("This record doesn't validate")
    print(e)
