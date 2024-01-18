from bookops_marc import SierraBibReader
from collections import defaultdict
from typing import Dict
from unidecode import unidecode


def read_marc_records(file):
    with open(file, "rb") as fh:
        reader = SierraBibReader(fh)
        for record in reader:
            yield record


def read_marc_to_dict(file):
    with open(file, "rb") as fh:
        reader = SierraBibReader(fh)
        for record in reader:
            dict_record = record.as_dict()
            output = {"leader": dict_record["leader"]}
            all_fields = []
            all_field_values = []
            for field in dict_record["fields"]:
                field_keys = list(field.keys())
                field_values = list(field.values())
                field_tag = field_keys[0]
                field_data = field_values[0]
                all_fields.append(field_tag)
                all_field_values.append(field_data)
            fields = defaultdict(list)
            for tag, data in zip(all_fields, all_field_values):
                fields[tag].append(data)
            output.update(fields)
            yield output


def get_field_from_list(record, f):
    try:
        field = record[f][0]
        return field
    except KeyError as e:
        return e


def get_nested_subfield(record, f, s):
    try:
        subfield = record[f][0]["subfields"][0][s]
        return subfield
    except KeyError as e:
        return e


def get_subfield(subfield_list, s):
    try:
        subfield = subfield_list[s]
        return subfield
    except KeyError as e:
        return e


def get_material_type(record: dict) -> str:
    physical_desc = get_nested_subfield(record, "300", "a")
    split_physical_desc = physical_desc.split()
    subject_dict = {
        key: value
        for key, value in record.items()
        if key in ["600", "650", "651", "655"]
    }
    if "pages" in physical_desc:
        pages = int(split_physical_desc[0])
        if pages < 50:
            material_type = "pamphlet"
            return material_type
    if "volumes" in physical_desc:
        material_type = "multipart"
        return material_type
    if "Catalogues Raissonnes" in unidecode(str(subject_dict)):
        material_type = "catalogue_raissonne"
        return material_type
    if "Catalogue Raissonne" in unidecode(str(subject_dict)):
        material_type = "catalogue_raissonne"
        return material_type
    else:
        material_type = "monograph_record"
        return material_type


def get_order_data(record, f):
    order_field = record[f]
    for field in order_field:
        output_dict = {}
        for subfield in field["subfields"]:
            output_dict.update(subfield)
            edited = {
                "order_price": get_subfield(output_dict, "s"),
                "order_location": get_subfield(output_dict, "t"),
                "order_fund": get_subfield(output_dict, "u"),
            }
            output = {
                key: val for key, val in edited.items() if type(val) is not KeyError
            }
    return output


def get_invoice_data(record, f):
    invoice_field = record[f]
    for field in invoice_field:
        output_dict = {}
        for subfield in field["subfields"]:
            output_dict.update(subfield)
            edited = {
                "invoice_date": get_subfield(output_dict, "a"),
                "invoice_price": get_subfield(output_dict, "b"),
                "invoice_shipping": get_subfield(output_dict, "c"),
                "invoice_tax": get_subfield(output_dict, "d"),
                "invoice_net_price": get_subfield(output_dict, "e"),
                "invoice_number": get_subfield(output_dict, "f"),
                "invoice_copies": get_subfield(output_dict, "g"),
            }
            output = {
                key: val for key, val in edited.items() if type(val) is not KeyError
            }
    return output


def get_item_data(record, f):
    item_field = record[f]
    output_list = []
    for field in item_field:
        output_dict = {}
        for subfield in field["subfields"]:
            output_dict.update(subfield)
            edited = {
                "material_type": get_material_type(record),
                "item_call_tag": get_subfield(output_dict, "z"),
                "item_call_no": get_subfield(output_dict, "a"),
                "item_barcode": get_subfield(output_dict, "i"),
                "item_price": get_subfield(output_dict, "p"),
                "item_volume": get_subfield(output_dict, "c"),
                "item_message": get_subfield(output_dict, "u"),
                "message": get_subfield(output_dict, "m"),
                "item_vendor_code": get_subfield(output_dict, "v"),
                "item_agency": get_subfield(output_dict, "h"),
                "item_location": get_subfield(output_dict, "l"),
                "item_type": get_subfield(output_dict, "t"),
            }
            output = {
                key: val for key, val in edited.items() if type(val) is not KeyError
            }
        output_list.append(output)
    return output_list


def convert_to_input(record: dict) -> Dict:
    try:
        items = get_item_data(record, "949")
        order = get_order_data(record, "960")
        invoice = get_invoice_data(record, "980")
        record = {
            "control_number": get_field_from_list(record, "001"),
            "bib_call_no": get_nested_subfield(record, "852", "h"),
            "bib_vendor_code": get_nested_subfield(record, "901", "a"),
            "rl_identifier": get_nested_subfield(record, "910", "a"),
            "lcc": get_nested_subfield(record, "050", "a"),
            "items": items,
            "order": order,
            "invoice": invoice,
        }
        record_output = {
            key: val for key, val in record.items() if type(val) is not KeyError
        }
        if len(record_output["items"]) == 1:
            record_output["item"] = record_output["items"][0]
            del record_output["items"]
        return record_output
    except KeyError as e:
        raise e
