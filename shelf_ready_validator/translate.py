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
    def __init__(self, error: ErrorDetails):
        self.original_error = error
        self.loc = self._error_loc_to_marc()
        self.type = error.get("type", None)
        self.msg = error.get("msg", None)
        self.ctx = error.get("ctx", None)
        self.input = error.get("input", None)
        self.url = error.get("url", None)

    def _error_loc_to_marc(self) -> Union[str, Tuple[str, str, str]]:
        if self.original_error["loc"][0] == "material_type":
            return "material_type"
        elif self.original_error["loc"][0] == "item_fields" and self.original_error[
            "input"
        ] == [{}]:
            return MarcEncoding[str(self.original_error["loc"][0])].value
        elif self.original_error["loc"][0] == "item_fields":
            tag = MarcEncoding[str(self.original_error["loc"][0])].value
            subfield_code = MarcEncoding[str(self.original_error["loc"][2])].value
            item_num = f"_{int(self.original_error["loc"][1]) + 1}"
            return "".join([tag, subfield_code, item_num])
        elif (
            self.original_error["loc"][0] == "order_item_data"
            and self.original_error["type"] == "order_item_location"
        ):
            order_tag = MarcEncoding["order_field"].value
            order_subfield_code = MarcEncoding["order_location"].value
            item_tag = MarcEncoding["item_fields"].value
            item_location_subfield_code = MarcEncoding["item_type"].value
            item_type_subfield_code = MarcEncoding["item_location"].value
            order = "".join([order_tag, order_subfield_code])
            item_location = "".join([item_tag, item_location_subfield_code])
            item_type = "".join([item_tag, item_type_subfield_code])
            return (order, item_location, item_type)

        elif (
            self.original_error["loc"][0] == "order_item_data"
            and self.original_error["loc"][2] == "order_location"
        ):
            tag = MarcEncoding["order_field"].value
            subfield_code = MarcEncoding[str(self.original_error["loc"][2])].value
            item_num = f"_{int(self.original_error["loc"][1]) + 1}"
            return "".join([tag, subfield_code, item_num])
        elif self.original_error["loc"][0] == "order_item_data" and self.original_error[
            "loc"
        ][2] in [
            "item_location",
            "item_type",
        ]:
            tag = MarcEncoding["item_fields"].value
            subfield_code = MarcEncoding[str(self.original_error["loc"][2])].value
            item_num = f"_{int(self.original_error["loc"][1]) + 1}"
            return "".join([tag, subfield_code, item_num])
        elif all(isinstance(i, str) for i in self.original_error["loc"]):
            loc_parts = [MarcEncoding[str(i)].value for i in self.original_error["loc"]]
            return "".join(loc_parts)
        else:
            return MarcEncoding[str(self.original_error["loc"][0])].value


class MarcValidationError:
    def __init__(self, errors: list):
        self.errors = [MarcError(i) for i in errors]
        self.missing_fields = self._get_missing_fields()
        self.extra_fields = self._get_extra_fields()
        self.invalid_fields = self._get_invalid_fields()
        self.missing_field_count = len(self.missing_fields)
        self.extra_field_count = len(self.extra_fields)
        self.invalid_field_count = len(self.invalid_fields)
        self.other_errors = self._get_other_errors()

    def _get_missing_fields(self) -> list:
        return [i for i in self.errors if i.type == "missing"]

    def _get_extra_fields(self) -> list:
        return [i for i in self.errors if i.type == "extra_forbidden"]

    def _get_invalid_fields(self) -> list:
        return [
            i
            for i in self.errors
            if i.type in ["literal_error", "string_pattern_mismatch"]
        ]

    def _get_other_errors(self) -> list:
        return [
            i
            for i in self.errors
            if i.type
            not in [
                "missing",
                "extra_forbidden",
                "literal_error",
                "string_pattern_mismatch",
            ]
        ]

    def to_dict(self):
        return {
            "missing_field_count": self.missing_field_count,
            "missing_fields": [i.loc for i in self.missing_fields],
            "extra_field_count": len(self.extra_fields),
            "extra_fields": [i.loc for i in self.extra_fields],
            "invalid_field_count": len(self.invalid_fields),
            "invalid_fields": [i.loc for i in self.invalid_fields],
            "other_errors": [i.loc for i in self.other_errors],
        }


# def count_errors(error_list: list) -> Counter:
#     error_types: Counter = Counter()
#     for error in error_list:
#         error_types[error["type"]] += 1
#     return error_types


# def count_missing_extra_fields(error_list: list) -> dict:
#     missing_fields = [i for i in error_list if i["type"] == "missing"]
#     extra_fields = [i for i in error_list if i["type"] == "extra_forbidden"]
#     out_dict = {
#         "missing_field_count": len(missing_fields),
#         "missing_fields": [i["loc"] for i in missing_fields],
#         "extra_field_count": len(extra_fields),
#         "extra_fields": [i["loc"] for i in extra_fields],
#     }
#     return out_dict


# def count_converted_errors(error_list: list) -> dict:
#     invalid_fields = [
#         i
#         for i in error_list
#         if i["type"] in ["literal_error", "string_pattern_mismatch"]
#     ]
#     missing_fields = [i for i in error_list if i["type"] == "missing"]
#     extra_fields = [i for i in error_list if i["type"] == "extra_forbidden"]
#     other_errors = [
#         i
#         for i in error_list
#         if i["type"]
#         not in [
#             "missing",
#             "extra_forbidden",
#             "literal_error",
#             "string_pattern_mismatch",
#         ]
#     ]
#     out_dict = {
#         "invalid_field_count": len(invalid_fields),
#         "invalid_fields": [i["loc"] for i in invalid_fields],
#         "missing_field_count": len(missing_fields),
#         "missing_fields": [i["loc"] for i in missing_fields],
#         "extra_field_count": len(extra_fields),
#         "extra_fields": [i["loc"] for i in extra_fields],
#         "other_errors": [i["loc"] for i in other_errors],
#     }
#     return out_dict
