import json
from typing import List
from collections import Counter
from rich import print
from pydantic import ValidationError
from shelf_ready_validator.utils import marc2json, read_marc_records
from shelf_ready_validator.models_scratch import VendorRecordModel
from shelf_ready_validator.vendor_marc import VendorRecord


def full_marc_file(file_path: str) -> None:
    records = read_marc_records(file_path)
    record_list = []
    for record in records:
        record_list.append(VendorRecord(leader=record.leader, fields=record.fields))
    print(record_list[0])
    # for record in record_list:
    #     try:
    #         print(record)
    #         model = VendorRecordModel.model_validate_json(record)
    #         print(model.model_dump())
    #         print("Record is valid")
    #     except ValidationError as e:
    #         print(e.errors())


def single_marc_json(record: str) -> None:
    json_record = json.dumps(record)
    try:
        model = VendorRecordModel.model_validate_json(json_record)
        print(model.model_dump(by_alias=True))
        print("Record is valid")
    except ValidationError as e:
        print(e.errors())


def count_fields(field_list: List):
    field_count: Counter = Counter()
    for field in field_list:
        for key, value in field.items():
            field_count[key] += 1
    return field_count


if __name__ == "__main__":
    full_marc_file("tests/test.mrc")
    # with open("temp/example_marc.json", "r") as f:
    #     record = json.load(f)
    #     single_marc_json(record)
