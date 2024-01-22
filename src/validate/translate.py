from bookops_marc import SierraBibReader

# from pymarc import MARCReader
from collections import defaultdict
from typing import Dict
from enum import Enum


class RLMarcEncoding(Enum):
    bib_call_no = "852$h"
    bib_vendor_code = "901$a"
    lcc = "050$a"
    invoice_date = "980$a"
    invoice_price = "980$b"
    invoice_shipping = "980$c"
    invoice_tax = "980$d"
    invoice_net_price = "980$e"
    invoice_number = "980$f"
    invoice_copies = "980$g"
    order_price = "960$s"
    order_location = "960$t"
    order_fund = "960$s"
    item_call_tag = "949z"
    item_call_no = "949$a"
    item_barcode = "949$i"
    item_price = "949$p"
    item_vendor_code = "949$v"
    item_agency = "949$h"
    item_location = "949$l"
    item_type = "949$t"
    library = "910$a"
    items = "949"


def read_marc_records(file):
    with open(file, "rb") as fh:
        reader = SierraBibReader(fh)
        for record in reader:
            yield record


def get_field_subfield(record, f, s):
    """
    gets value of subfield and returns it to be assigned to a variable
    if subfield does not exist, returns "no_field" to be parsed in later validator
    """
    try:
        field_subfield = record[f][s]
        return field_subfield
    except KeyError as e:
        return e


def get_material_type(record):
    """
    get material type to determine which model to use when validating a record

    this function needs to be built out more
    """
    subjects = record.subjects
    subjects.append(record.get_fields("600", "610", "650"))
    physical_desc = record.physicaldescription
    series = record.series
    if "Catalogues Raisonnes" in subjects:
        return "catalogue_raissonne"
    elif "Catalogue Raissonne" in subjects:
        return "catalogue_raissonne"
    elif "pages" in physical_desc:
        pages = int(physical_desc[0])
        if pages < 50:
            return "pamphlet"
    elif "volumes" in physical_desc:
        return "multipart"
    elif series:
        return "multipart"
    else:
        return "monograph_record"


def get_record_input(record):
    library = get_field_subfield(record, "910", "a")
    record_data = {
        "material_type": get_material_type(record),
        "bib_call_no": get_field_subfield(record, "852", "h"),
        "bib_vendor_code": get_field_subfield(record, "901", "a"),
        "lcc": get_field_subfield(record, "050", "a"),
        "invoice_date": get_field_subfield(record, "980", "a"),
        "invoice_price": get_field_subfield(record, "980", "b"),
        "invoice_shipping": get_field_subfield(record, "980", "c"),
        "invoice_tax": get_field_subfield(record, "980", "d"),
        "invoice_net_price": get_field_subfield(record, "980", "e"),
        "invoice_number": get_field_subfield(record, "980", "f"),
        "invoice_copies": get_field_subfield(record, "980", "g"),
        "order_price": get_field_subfield(record, "960", "s"),
        "order_location": get_field_subfield(record, "960", "t"),
        "order_fund": get_field_subfield(record, "960", "u"),
    }
    record_input = {
        key: val for key, val in record_data.items() if type(val) is not KeyError
    }
    items = record.get_fields("949")
    if len(items) == 0:
        return record_input
    else:
        item_list = []
        for item in items:
            item_output = {
                "item_call_tag": item.get("z"),
                "item_call_no": item.get("a"),
                "item_barcode": item.get("i"),
                "item_price": item.get("p"),
                "item_vendor_code": item.get("v"),
                "item_agency": item.get("h"),
                "item_location": item.get("l"),
                "item_type": item.get("t"),
                "library": library,
            }
            edited_item = {
                key: val for key, val in item_output.items() if val is not None
            }
            item_list.append(edited_item)
        record_input["items"] = item_list
        return record_input


# def read_marc_to_dict(file):
#     with open(file, "rb") as fh:
#         reader = MARCReader(fh)
#         for record in reader:
#             dict_record = record.as_dict()
#             output = {"leader": dict_record["leader"]}
#             all_fields = []
#             all_field_values = []
#             for field in dict_record["fields"]:
#                 field_keys = list(field.keys())
#                 field_values = list(field.values())
#                 field_tag = field_keys[0]
#                 field_data = field_values[0]
#                 all_fields.append(field_tag)
#                 all_field_values.append(field_data)
#             fields = defaultdict(list)
#             for tag, data in zip(all_fields, all_field_values):
#                 fields[tag].append(data)
#             output.update(fields)
#             yield output
