from rl_sr_validation.models import Record
from pydantic import ValidationError
from rich import print
from pymarc import MARCReader

with open("temp/EastView-sample.mrc", "rb") as f:
    reader = MARCReader(f)
    for record in reader:
        dict_output = {
            "item": {
                "item_call_tag": record.get("949").get("z"),
                "item_call_no": record.get("949").get("a"),
                "item_barcode": record.get("949").get("i"),
                "item_price": record.get("949").get("p"),
                "item_volume": record.get("949").get("c"),
                "item_message": record.get("949").get("u"),
                "message": record.get("949").get("m"),
                "item_vendor_code": record.get("949").get("v"),
                "item_agency": record.get("949").get("h"),
                "item_location": record.get("949").get("l"),
                "item_type": record.get("949").get("t"),
            },
            "order": {
                "order_price": record.get("960").get("s"),
                "order_location": record.get("960").get("t"),
                "order_fund": record.get("960").get("u"),
            },
            "invoice": {
                "invoice_date": record.get("980").get("a"),
                "invoice_price": record.get("980").get("b"),
                "invoice_shipping": record.get("980").get("c"),
                "invoice_tax": record.get("980").get("d"),
                "invoice_net_price": record.get("980").get("e"),
                "invoice_number": record.get("980").get("f"),
                "invoice_copies": record.get("980").get("g"),
            },
            "bib_call_no": record.get("852").get("h"),
            "bib_vendor_code": record.get("901").get("a"),
            "rl_identifier": record.get("910").get("a"),
            "lcc": record.get("050").get("a"),
        }
        try:
            Record(**dict_output)
        except ValidationError as e:
            print(e.errors())
