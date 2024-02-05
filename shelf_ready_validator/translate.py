from enum import Enum

from bookops_marc import SierraBibReader


class RLMarcEncoding(Enum):
    """
    A class to translate fields used in the validator to MARC fields/subfields
    """

    bib_call_no = "852"
    bib_call_no_ind1 = "852_ind1"
    bib_call_no_ind2 = "852_ind2"
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
    order_fund = "960$u"
    order_ind1 = "960_ind1"
    order_ind2 = "960_ind2"
    item_call_tag = "949$z"
    item_call_no = "949$a"
    item_barcode = "949$i"
    item_price = "949$p"
    item_message = "949$u"
    message = "949$m"
    item_vendor_code = "949$v"
    item_agency = "949$h"
    item_location = "949$l"
    item_type = "949$t"
    library = "910$a"
    item_ind1 = "949_ind1"
    item_ind2 = "949_ind2"
    items = "949"


def read_marc_records(file):
    """
    Reads .mrc file and returns a record
    """
    with open(file, "rb") as fh:
        reader = SierraBibReader(fh)
        for record in reader:
            yield record


def get_field_subfield(record, f, s):
    """
    Gets value of subfield and returns it to be assigned to a variable
    if subfield does not exist, returns KeyError
    KeyError can be stripped out before reading input into validator
    """
    try:
        field_subfield = record[f][s]
        return field_subfield
    except KeyError as e:
        return e


def get_field_indicators(record, f, i):
    """
    Gets value of subfield and returns it to be assigned to a variable
    if subfield does not exist, returns KeyError
    KeyError can be stripped out before reading input into validator
    """
    if i == "indicator1":
        try:
            field = record[f]
            field_indicator = field.indicator1
            return field_indicator
        except KeyError as e:
            return e
    elif i == "indicator2":
        try:
            field = record[f]
            field_indicator = field.indicator2
            return field_indicator
        except KeyError as e:
            return e
    else:
        pass


def get_material_type(record):
    """
    Reads record data to determine material type
    Validator chooses model to validate against based on material type

    this function needs to be built out more
    """
    subjects = record.subjects
    subject_subfield_v = []
    for subject in subjects:
        subfield_v = subject.get_subfields("v")
        subject_subfield_v.append(subfield_v)
    subject_subfield_list = [item for listed in subject_subfield_v for item in listed]
    physical_desc = record.physicaldescription
    field_300a = physical_desc[0].get_subfields("a")
    split_300a = field_300a[0].split()
    if "Catalogues Raisonnes" in subject_subfield_list:
        return "catalogue_raissonne"
    elif "Catalogue Raissonne" in subject_subfield_list:
        return "catalogue_raissonne"
    elif "volumes" in split_300a[1]:
        return "multipart"
    elif "pages" in split_300a[1]:
        try:
            pages = int(split_300a[0])
            if pages < 50:
                return "pamphlet"
            else:
                return "monograph_record"
        except ValueError:
            return "monograph_record"
    else:
        return "monograph_record"


def get_record_input(record):
    """
    Reads a MARC record and creates dict input for validation
    Uses get_field_subfield function to return KeyErrors for missing fields
    KeyErrors removed from dict to ensure validator recognizes missing fields
    """
    library = get_field_subfield(record, "910", "a")
    record_data = {
        "material_type": get_material_type(record),
        "bib_call_no": get_field_subfield(record, "852", "h"),
        "bib_call_no_ind1": get_field_indicators(record, "852", "indicator1"),
        "bib_call_no_ind2": get_field_indicators(record, "852", "indicator2"),
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
        "order_ind1": get_field_indicators(record, "960", "indicator1"),
        "order_ind2": get_field_indicators(record, "960", "indicator1"),
        "library": library,
    }
    record_input = {
        key: val for key, val in record_data.items() if type(val) is not KeyError
    }
    items = record.get_fields("949")
    if items:
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
                "item_ind1": item.indicator1,
                "item_ind2": item.indicator2,
            }
            edited_item = {
                key: val for key, val in item_output.items() if val is not None
            }
            item_list.append(edited_item)
        record_input["items"] = item_list
    if record_data["material_type"] == "monograph_record":
        del record_input["library"]
        return record_input
    else:
        return record_input
