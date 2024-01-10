from rl_sr_validation.models import Record
from pydantic import ValidationError
from rich import print


def parse_errors(e):
    error_count = e.error_count()
    errors = e.errors()
    error_types = []
    error_locs = []
    for error in errors:
        error_type = error["type"]
        error_loc = error["loc"]
        error_types.append(error_type)
        error_locs.append(error_loc)
    missing_field_count = error_types.count("missing")
    format_error_count = error_types.count("string_pattern_mismatch")
    return {"missing_field_count": missing_field_count,
            "format_error_count": format_error_count,
            "errors": errors, "error_count": error_count}


def validate_records(r):
    n = 0
    for record in r:
        n += 1
        try:
            Record(**record)
            print(f"Record {n} validates.")
        except ValidationError as e:
            parsed_errors = parse_errors(e)
            print(f"Record {n} is not valid. This record contains {parsed_errors["error_count"]} errors including: {parsed_errors["missing_field_count"]} missing field(s) and {parsed_errors["format_error_count"]} incorrectly formatted field(s).")
