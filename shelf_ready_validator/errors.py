from typing import List, Dict

from pydantic import ValidationError
from shelf_ready_validator.translate import RLMarcEncoding


def missing_errors(error):
    """
    A function to convert a standard pydantic error output
    a function that handles errors for missing fields
    converts error["loc"] values to MARC tags
    flattens nested fields for item records to assign correct tag

    """
    error["input"] = error["loc"]
    if error["loc"][0] == "items" and len(error["loc"]) == 4:
        error["loc"] = (
            f"item_{error['loc'][1]}",
            RLMarcEncoding[error["loc"][3]].value,
        )
        return error
    else:
        error["loc"] = RLMarcEncoding[error["loc"][0]].value
        return error


def extra_errors(error):
    """
    A function to convert a standard pydantic error output
    a function that handles errors for extra fields
    converts error["loc"] values to MARC tags
    flattens nested fields in error["input"] for item records

    """
    if type(error["input"]) is str:
        error["loc"] = RLMarcEncoding[error["loc"][0]].value
        return error
    else:
        extra_fields = []
        n = 0
        for field in error["input"]:
            keys = field.keys()
            for k in keys:
                extra_field = (f"item_{n}", RLMarcEncoding[k].value)
                extra_fields.append(extra_field)
            n += 1
        error["loc"] = extra_fields
        return error


def item_order_errors(error):
    """
    A function to convert a standard pydantic error output
    a function that handles errors incorrect item/order combinations
    converts error["loc"] values to MARC tags
    includes which item is associated with incorrect data
    returns MARC tags for item_location, item_type, and order_location

    """
    error["loc"] = (
        f"item_{error['loc'][0]}",
        (
            RLMarcEncoding[error["loc"][1]].value,
            RLMarcEncoding[error["loc"][2]].value,
            RLMarcEncoding[error["loc"][3]].value,
        ),
    )
    return error


def match_errors(error):
    """
    A function to convert a standard pydantic error output
    matches error type and pattern for string, literal, and union errors
    converts error["loc"] to values with MARC tags

    Returns a new_error dict object containing:
     - error type: str
     - error location: tuple
     - error input: dict
     - error message: str
     - error ctx: str


    """
    if error["loc"][0] == "items" and len(error["loc"]) == 4:
        error["loc"] = (
            f"item_{error['loc'][1]}",
            RLMarcEncoding[error["loc"][3]].value,
        )
    elif error["loc"][0] == "items" and len(error["loc"]) == 2:
        error["loc"] = (
            f"item_{error['loc'][1]}",
            RLMarcEncoding[error["loc"][0]].value,
        )
    else:
        error["loc"] = RLMarcEncoding[error["loc"][0]].value
    match (error["type"], error["ctx"]):
        case (
            "literal_error",
            {"expected": " "},
        ):
            error["msg"] = "Invalid indicator"
            return error
        case (
            "literal_error",
            {"expected": "1"},
        ):
            error["msg"] = "Invalid indicator"
            return error
        case (
            "literal_error",
            {"expected": "'EVP' or 'AUXAM'"},
        ):
            error["msg"] = "Invalid vendor code"
            return error
        case (
            "literal_error",
            {"expected": "'RL'"},
        ):
            error["msg"] = "Invalid library identifier"
            return error
        case (
            "literal_error",
            {"expected": "'8528'"},
        ):
            error["msg"] = "Invalid item call tag"
            return error
        case (
            "literal_error",
            {
                "expected": "'rcmb2', 'rcmf2', 'rcmg2', 'rc2ma', 'rcmp2', 'rcph2', 'rcpm2', 'rcpt2' or 'rc2cf'"
            },
        ):
            error["msg"] = "Item location does not match a valid location"
            return error
        case (
            "literal_error",
            {
                "expected": "'MAB', 'MAF', 'MAG', 'MAL', 'MAP', 'MAS', 'PAD', 'PAH', 'PAM', 'PAT' or 'SC'"
            },
        ):
            error["msg"] = "Order location does not match a valid location"
            return error
        case ("literal_error", {"expected": "'43'"}):
            error["msg"] = "Invalid item agency code"
            return error
        case (
            "string_pattern_mismatch",
            {"pattern": "^33433[0-9]{9}$|^33333[0-9]{9}$|^34444[0-9]{9}$"},
        ):
            error["msg"] = "Invalid barcode"
            return error
        case (
            "string_pattern_mismatch",
            {"pattern": "^ReCAP 23-\\d{6}$|^ReCAP 24-\\d{6}$"},
        ):
            error["msg"] = "Invalid ReCAP call number"
            return error
        case (
            "string_pattern_mismatch",
            {"pattern": "^\\d{3,}$"} | {"pattern": "^\\d{1,}$"},
        ):
            error["msg"] = "Invalid price; price should not include a decimal point"
            return error
        case (
            "string_pattern_mismatch",
            {"pattern": "^\\d{6}$"},
        ):
            error["msg"] = "Invalid date; invoice date should be YYMMDD"
            return error
        case (
            "string_pattern_mismatch",
            {"pattern": "^\\d{1,}\\.\\d{2}$"},
        ):
            error["msg"] = "Invalid price; item price should include a decimal point"
            return error
        case (
            "string_pattern_mismatch",
            {"pattern": "^[^a-z]+"},
        ):
            error["msg"] = "Invalid item message; message should be in all caps"
            return error
        case _:
            pass
    return error


def format_errors(e: ValidationError) -> List:
    """
    A function to convert a list of errors based on error type
    returns error["loc"] values with MARC tags

    Returns a list of dicts containing
     - error type: str
     - error location: tuple
     - error input: dict
     - error message: str
     - error ctx: str (optional)

    """
    errors = []
    missing_fields = []
    extra_fields = []
    for error in e.errors():
        if error["type"] == "missing":
            converted_error = missing_errors(error)
            missing_fields.append(converted_error["loc"])
        elif error["type"] == "extra_forbidden":
            converted_error = extra_errors(error)
            if type(converted_error["loc"]) is str:
                extra_fields.append(converted_error["loc"])
            else:
                for loc in converted_error["loc"]:
                    extra_fields.append(loc)
        elif error["type"] == "Item/Order location check":
            converted_error = item_order_errors(error)
            converted_error["count"] = 1
            errors.append(converted_error)
        else:
            converted_error = match_errors(error)
            converted_error["count"] = 1
            errors.append(converted_error)
    missing_fields[:] = (
        value
        for value in missing_fields
        if value not in ("852_ind1", "852_ind2", "949_ind1", "949_ind2")
    )
    missing_field_count = len(missing_fields)
    extra_fields[:] = (
        value
        for value in extra_fields
        if value not in ("852_ind1", "852_ind2", "949_ind1", "949_ind2")
    )
    extra_field_count = len(extra_fields)
    if len(missing_fields) > 0:
        missing_field_error = {
            "count": missing_field_count,
            "type": "missing",
            "loc": missing_fields,
            "input": missing_fields,
            "msg": "missing field/subfield(s)",
        }
        errors.append(missing_field_error)
    if len(extra_fields) > 0:
        extra_field_error = {
            "count": extra_field_count,
            "type": "extra_forbidden",
            "loc": extra_fields,
            "input": extra_fields,
            "msg": "extra field/subfield(s)",
        }
        errors.append(extra_field_error)
    return errors


def format_error_summary(e: ValidationError) -> Dict:
    """
    A function to convert a list of errors based on error type
    returns summary of errors based on type values with MARC tags

    Returns a dicts containing
     - missing_field_count:
     - missing_fields:
     - extra_field_count:
     - extra_fields:
     - invalid_field_count:
     - invalid_fields:
     - combination_error_count:
     - combination_errors:

    """
    missing_fields = []
    extra_fields = []
    invalid_fields = []
    other_errors = []
    other_error_fields = []
    for error in e.errors():
        if error["type"] == "missing":
            converted_error = missing_errors(error)
            missing_fields.append(converted_error["loc"])
        elif error["type"] == "extra_forbidden":
            converted_error = extra_errors(error)
            if type(converted_error["loc"]) is str:
                extra_fields.append(converted_error["loc"])
            else:
                for loc in converted_error["loc"]:
                    extra_fields.append(loc)
        elif error["type"] == "Item/Order location check":
            converted_error = item_order_errors(error)
            other_errors.append("Check item and order data; combination is not valid.")
            other_error_fields.append(converted_error["loc"])
        elif error["type"] == "union_tag_invalid":
            other_errors.append("Unable to validate item record; invalid 910$a")
        else:
            converted_error = match_errors(error)
            invalid_fields.append(converted_error["loc"])
    missing_fields[:] = (
        value
        for value in missing_fields
        if value not in ("852_ind1", "852_ind2", "949_ind1", "949_ind2")
    )
    extra_fields[:] = (
        value
        for value in extra_fields
        if value not in ("852_ind1", "852_ind2", "949_ind1", "949_ind2")
    )
    error_summary = {
        "missing_field_count": str(len(missing_fields)),
        "missing_fields": missing_fields,
        "extra_field_count": str(len(extra_fields)),
        "extra_fields": extra_fields,
        "invalid_field_count": str(len(invalid_fields)),
        "invalid_fields": invalid_fields,
        "other_errors": other_errors,
        "other_error_fields": other_error_fields,
    }
    return error_summary
