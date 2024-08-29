from enum import Enum
from typing import Tuple, Union
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
    """A class to translate an error from the validator to a more readable format"""

    def __init__(self, error: ErrorDetails):
        self.original_error = error
        self.type = error.get("type", None)
        self.msg = error.get("msg", None)
        self.ctx = error.get("ctx", None)
        self.url = error.get("url", None)
        self.input = self._convert_input()
        self.loc = self._error_loc_to_marc()

    def _error_loc_to_marc(self) -> Union[str, Tuple[str, str, str]]:
        if self.type == "order_item_mismatch":
            order = "".join(
                [
                    MarcEncoding["order_field"].value,
                    MarcEncoding["order_location"].value,
                ]
            )
            item_location = "".join(
                [MarcEncoding["item_fields"].value, MarcEncoding["item_type"].value]
            )
            item_type = "".join(
                [MarcEncoding["item_fields"].value, MarcEncoding["item_location"].value]
            )
            return (order, item_location, item_type)
        elif self.original_error["loc"][0] == "material_type":
            return "material_type"
        elif self.original_error["loc"][0] == "item_fields" and self.original_error[
            "input"
        ] == [{}]:
            return MarcEncoding[str(self.original_error["loc"][0])].value
        elif (
            self.type == "extra_forbidden"
            and self.original_error["loc"][0] == "item_fields"
        ):
            return MarcEncoding[str(self.original_error["loc"][0])].value
        elif self.original_error["loc"][0] == "item_fields":
            tag = MarcEncoding[str(self.original_error["loc"][0])].value
            subfield_code = MarcEncoding[str(self.original_error["loc"][2])].value
            item_num = f"_{int(self.original_error["loc"][1]) + 1}"
            return "".join([tag, subfield_code, item_num])
        elif all(isinstance(i, str) for i in self.original_error["loc"]):
            loc_parts = [MarcEncoding[str(i)].value for i in self.original_error["loc"]]
            return "".join(loc_parts)
        else:
            return MarcEncoding[str(self.original_error["loc"][0])].value

    def _convert_input(self):
        input = self.original_error.get("input", None)
        if input is None:
            return None
        elif self.original_error["type"] == "order_item_mismatch":
            return self.original_error["input"]["order_item_data"][0]
        else:
            return input


class MarcValidationError:
    """A class to translate a list of errors from the `errors()` method of a
    `ValidationError` object to a more readable format"""

    def __init__(self, errors: list):
        self.errors = [MarcError(i) for i in errors]
        self.missing_fields = self._get_missing_fields()
        self.extra_fields = self._get_extra_fields()
        self.invalid_fields = self._get_invalid_fields()
        self.order_item_mismatches = self._get_order_item_mismatch_errors()

    def _get_missing_fields(self) -> list:
        return [i for i in self.errors if i.type == "missing"]

    def _get_extra_fields(self) -> list:
        return [i for i in self.errors if i.type == "extra_forbidden"]

    def _get_invalid_fields(self) -> list:
        invalid_fields = [
            i
            for i in self.errors
            if i.type in ["string_pattern_mismatch", "literal_error"]
        ]

        invalid_field_list = []
        for error in invalid_fields:
            invalid_field_list.append(
                {
                    "invalid_field": error.loc,
                    "input": error.input,
                    "expectation": error.ctx,
                }
            )
        return invalid_field_list

    def _get_order_item_mismatch_errors(self) -> dict:
        return {
            "input": [i.input for i in self.errors if i.type == "order_item_mismatch"],
            "location": [i.loc for i in self.errors if i.type == "order_item_mismatch"],
        }

    def to_dict(self):
        out_dict = {
            "valid": False,
            "error_count": 0,
            "missing_field_count": len(self.missing_fields),
            "missing_fields": [i.loc for i in self.missing_fields],
            "extra_field_count": len(self.extra_fields),
            "extra_fields": [i.loc for i in self.extra_fields],
            "invalid_field_count": len(self.invalid_fields),
            "invalid_fields": self.invalid_fields,
            "order_item_mismatches": self.order_item_mismatches,
        }
        out_dict["error_count"] = (
            out_dict["missing_field_count"]
            + out_dict["extra_field_count"]
            + out_dict["invalid_field_count"]
        )
        if out_dict["invalid_field_count"] == 0:
            out_dict["invalid_fields"] = None
        if out_dict["missing_field_count"] == 0:
            out_dict["missing_fields"] = None
        if out_dict["extra_field_count"] == 0:
            out_dict["extra_fields"] = None
        if out_dict["order_item_mismatches"] == {"input": [], "location": []}:
            out_dict["order_item_mismatches"] = None
        else:
            out_dict["error_count"] += 1
        return out_dict
