from enum import Enum
from typing import Counter
from pydantic_core import ErrorDetails


class MarcEncoding(Enum):
    """
    A class to translate fields used in the validator to MARC fields/subfields
    """

    ind1 = "ind1"
    ind2 = "ind2"
    bib_call_no = "852"
    call_no = "$h"
    bib_vendor_code = "901"
    vendor_code = "$a"
    lc_class = "050"
    lcc = "$a"
    order_field = "960"
    order_price = "$s"
    order_location = "$t"
    order_fund = "$u"
    invoice_field = "980"
    invoice_date = "$a"
    invoice_price = "$b"
    invoice_shipping = "$c"
    invoice_tax = "$d"
    invoice_net_price = "$e"
    invoice_number = "$f"
    invoice_copies = "$g"
    item_fields = "949"
    item_call_tag = "$z"
    item_call_no = "$a"
    item_barcode = "$i"
    item_price = "$p"
    item_message = "$u"
    message = "$m"
    item_vendor_code = "$v"
    item_agency = "$h"
    item_location = "$l"
    item_type = "$t"
    library_field = "910"
    library = "$a"


class MarcError:
    def __init__(self, error: ErrorDetails):
        self.original_error = error
        self.error_loc = self._get_error_loc()
        self.error_type = error.get("type", None)
        self.error_msg = error.get("msg", None)
        self.error_ctx = error.get("ctx", None)
        self.error_input = error.get("input", None)
        self.error_url = error.get("url", None)

    def _get_error_loc(self) -> str:
        if self.original_error["loc"][0] == "item_fields":
            loc_parts = [
                MarcEncoding[str(self.original_error["loc"][0])].value,
                MarcEncoding[str(self.original_error["loc"][2])].value,
                f"_{int(self.original_error["loc"][1]) + 1}",
            ]
            return "".join(loc_parts)
        elif (
            self.original_error["loc"][0] == "order_item_data"
            and self.original_error["loc"][2] == "order_location"
        ):
            loc_parts = [
                MarcEncoding["order_field"].value,
                MarcEncoding[str(self.original_error["loc"][2])].value,
                f"_{int(self.original_error["loc"][1]) + 1}",
            ]
            return "".join(loc_parts)
        elif self.original_error["loc"][0] == "order_item_data" and self.original_error[
            "loc"
        ][2] in [
            "item_location",
            "item_type",
        ]:
            loc_parts = [
                MarcEncoding["item_fields"].value,
                MarcEncoding[str(self.original_error["loc"][2])].value,
                f"_{int(self.original_error["loc"][1]) + 1}",
            ]
            return "".join(loc_parts)
        elif all(isinstance(i, str) for i in self.original_error["loc"]):
            loc_parts = [MarcEncoding[str(i)].value for i in self.original_error["loc"]]
            return "".join(loc_parts)
        else:
            return MarcEncoding[str(self.original_error["loc"][0])].value

    def to_dict(self):
        return {
            "error_loc": self.error_loc,
            "error_type": self.error_type,
            "error_msg": self.error_msg,
            "error_ctx": self.error_ctx,
            "error_input": self.error_input,
            "error_url": self.error_url,
        }


def count_errors(error_list: list) -> Counter:
    error_types: Counter = Counter()
    for error in error_list:
        error_types[error["type"]] += 1

    return error_types
