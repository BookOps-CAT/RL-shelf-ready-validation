import pytest
from pydantic import ValidationError
from contextlib import nullcontext as does_not_raise
from src.validate.models_v2 import Record, ItemNYPLRL
from pymarc import MARCReader, Record, Field


def test_mono_record_valid():
    with does_not_raise():
        items = [
            {
                "item_call_tag": "8528",
                "item_call_no": "ReCAP 23-999999",
                "item_barcode": "33433123456789",
                "item_price": "12.34",
                "item_vendor_code": "EVP",
                "item_agency": "43",
                "item_location": "rcmb2",
                "item_type": "2",
                "library": "RL",
            },
            {
                "item_call_tag": "8528",
                "item_call_no": "ReCAP 23-999998",
                "item_barcode": "33433333333333",
                "item_price": "12.34",
                "item_vendor_code": "EVP",
                "item_agency": "43",
                "item_location": "rcmb2",
                "item_type": "2",
                "library": "RL",
            },
        ]
        input = {
            "data": {
                "material_type": "monograph_record",
                "bib_call_no": "ReCAP 23-999999",
                "bib_vendor_code": "EVP",
                "lcc": "Z123",
                "invoice_date": "240101",
                "invoice_price": "1234",
                "invoice_shipping": "100",
                "invoice_tax": "123",
                "invoice_net_price": "1234",
                "invoice_number": "1234567890",
                "invoice_copies": "1",
                "order_price": "1234",
                "order_location": "MAS",
                "order_fund": "123456apprv",
                "library": "RL",
                "items": items,
            }
        }
        mono_record = Record(**input)
    assert mono_record.data.material_type == "monograph_record"


def test_pamphlet_record_valid():
    with does_not_raise():
        input = {
            "data": {
                "material_type": "pamphlet",
                "bib_vendor_code": "EVP",
                "lcc": "Z123",
                "invoice_date": "240101",
                "invoice_price": "1234",
                "invoice_shipping": "100",
                "invoice_tax": "123",
                "invoice_net_price": "1234",
                "invoice_number": "1234567890",
                "invoice_copies": "1",
                "order_price": "1234",
                "order_location": "MAS",
                "order_fund": "123456apprv",
                "library": "RL",
            }
        }
        mono_record = Record(**input)
    assert mono_record.data.material_type == "pamphlet"

def test_everything():
    with open("temp/test.mrc", "rb") as fh:
    reader = MARCReader(fh)
    for record in reader:
        if record:
            try:
                ItemNYPLRL(item_call_tag=record["949"]["z"], item_call_no=record["949"]["a"], item_barcode=record["949"]["i"], item_price=record["949"]["p"], item_vendor_code=["949"]["v"], item_agency=["949"]["h"], item_location=["949"]["l"], item_type=["949"]["t"],library=["RL"])
            except ValidationError as e:
                raise e
