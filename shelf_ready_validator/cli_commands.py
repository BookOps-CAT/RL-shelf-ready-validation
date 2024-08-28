from typing import Generator
from pymarc import MARCReader, Record
from file_retriever.file import File
from pydantic import ValidationError
from shelf_ready_validator.models import (
    VendorMonographRecordModel,
    VendorOtherRecordModel,
)
from shelf_ready_validator.translate import MarcError, count_errors
from shelf_ready_validator.vendor_marc import VendorRecord


def validate_single_record(record: VendorRecord) -> dict:
    input = record.pydantic_dict_input()
    try:
        match input["material_type"]:
            case "monograph":
                VendorMonographRecordModel.model_validate(input)
                return {"valid": True}
            case (
                "catalogue_raissonne"
                | "dance"
                | "multipart"
                | "pamphlet"
                | "non-standard_binding_packaging"
            ):
                VendorOtherRecordModel.model_validate(input)
                return {"valid": True}
            case _:
                return {"valid": False, "errors": "Material type not recognized"}
    except ValidationError as e:
        converted_errors = [MarcError(i).to_dict() for i in e.errors()]
        return {
            "valid": False,
            "errors": converted_errors,
            "error_count": dict(count_errors(e.errors())),
        }


def read_validate_file(file_obj: File) -> list:
    reader = read_marc_records(file_obj.file_stream.getvalue())
    output = []
    record_n = 1
    for record in reader:
        vendor_record = VendorRecord(leader=record.leader, fields=record.fields)
        dict_output = {
            "vendor_code": vendor_record.bib_vendor_code.vendor_code,
            "record_number": record_n,
            # "control_number": get_control_number(vendor_record),
        }
        # print(vendor_record.pydantic_dict_input())
        validation_output = validate_single_record(vendor_record)
        dict_output.update(validation_output)
        # output.append((dict_output, vendor_record.pydantic_dict_input()))
        output.append(dict_output)
        record_n += 1
    return output


def read_marc_records(fh: bytes) -> Generator[Record, None, None]:
    """
    Reads .mrc file and returns a record
    """
    reader = MARCReader(fh)
    for record in reader:
        yield record
