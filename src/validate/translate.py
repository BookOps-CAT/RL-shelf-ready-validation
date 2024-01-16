from bookops_marc import SierraBibReader
from collections import defaultdict
from typing import Dict


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
            flat_record = {"leader": dict_record["leader"]}
            all_fields = []
            all_field_values = []
            for field in dict_record["fields"]:
                field_keys = list(field.keys())
                field_values = list(field.values())
                field_tag = field_keys[0]
                field_data = field_values[0]
                all_fields.append(field_tag)
                all_field_values.append(field_data)
            flat_fields = defaultdict(list)
            for tag, data in zip(all_fields, all_field_values):
                flat_fields[tag].append(data)
            flat_record.update(flat_fields)
            yield flat_record


def convert_to_input(record: dict) -> Dict:
    # need to add try, except to remove any KeyErrors
    # KeyErrors rise during mapping when a record is missing a field
    items = []
    orders = []
    invoices = []
    item_field = record["949"]
    order_field = record["960"]
    invoice_field = record["980"]
    bib_call_no = record["852"][0]["subfields"][0]["h"]
    bib_vendor_code = record["901"][0]["subfields"][0]["a"]
    rl_identifier = record["910"][0]["subfields"][0]["a"]
    lcc = record["050"][0]["subfields"][0]["a"]
    control_number = record["001"][0]
    for field in item_field:
        item = {}
        for subfield in field["subfields"]:
            item.update(subfield)
            # item["item_call_tag"] = item["z"]
        items.append(item)
    for field in order_field:
        order = {}
        for subfield in field["subfields"]:
            order.update(subfield)
        orders.append(order)
    for field in invoice_field:
        invoice = {}
        for subfield in field["subfields"]:
            invoice.update(subfield)
        invoices.append(invoice)

    record = {
        "control_number": control_number,
        "item_field": item_field,
        "invoice_field": invoice_field,
        "order-field": order_field,
        "bib_vendor_code": bib_vendor_code,
        "rl_identifier": rl_identifier,
        "bib_call_no": bib_call_no,
        "lcc": lcc,
        "items": items,
        "orders": orders,
        "invoices": invoices,
    }
    return record
