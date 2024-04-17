from typing import Any
from pydantic import ValidationError
from pydantic_core import ErrorDetails
from shelf_ready_validator.translate import RLMarcEncoding


def missing_errors(error: ErrorDetails) -> dict:
    """
    A function to convert error location to MARC tags for "missing" error type.
    Converts error["loc"] values to MARC tags and flattens nested fields
    for item records. Item locations include item number and MARC tag for subfield.

    Args:
        error: pydantic ErrorDetails object

    Returns:
        error data as dict with edited error["loc"] value

    """
    new_error: dict = {}
    new_error.update(error)
    new_error["input"] = error["loc"]
    if error["loc"][0] == "items" and len(error["loc"]) == 4:
        new_error["loc"] = (
            f"item_{error['loc'][1]}",
            RLMarcEncoding[str(error["loc"][3])].value,
        )
        return new_error
    else:
        new_error["loc"] = RLMarcEncoding[str(error["loc"][0])].value
        return new_error


def extra_errors(error: ErrorDetails) -> dict:
    """
    A function to convert error location to MARC tags for "extra_forbidden" error type.
    Converts error["loc"] values to MARC tags and adds suffix for multiple items.

    Args:
        error: pydantic ErrorDetails object

    Returns:
        error data as dict with edited error["loc"] value

    """
    new_error: dict = {}
    new_error.update(error)
    if type(error["input"]) is str:
        new_error["loc"] = RLMarcEncoding[str(error["loc"][0])].value
        return new_error
    else:
        new_error["loc"] = [
            f"{RLMarcEncoding[str(error['loc'][0])].value}_" + str(i)
            for i in range(len(error["input"]))
        ]
        return new_error


def item_order_errors(error: ErrorDetails) -> dict:
    """
    A function to convert error location to MARC tags for "Item/Order location check"
    error type. Converts error["loc"] values to MARC tags and adds item number
    associated with incorrect data. Returns MARC tags for item_location, item_type, and
    order_location.
    Args:
        error: pydantic ErrorDetails object

    Returns:
        error data as dict with edited error["loc"] value

    """
    new_error: dict = {}
    new_error.update(error)
    new_error["loc"] = (
        f"item_{error['loc'][0]}",
        str(RLMarcEncoding[str(error["loc"][1])].value),
        str(RLMarcEncoding[str(error["loc"][2])].value),
        str(RLMarcEncoding[str(error["loc"][3])].value),
    )
    return new_error


def match_errors(error: ErrorDetails) -> dict:
    """
    A function to convert error location to MARC tags and edit error message
    for "literal_error", "string_pattern_mismatch" and "union_tag_invalid" error types.
    Converts error["loc"] values to MARC tags and adds item number associated
    with incorrect data.

    Args:
        error: pydantic ErrorDetails object

    Returns:
        error data as dict with edited error["loc"] and error["msg"] values

    """
    new_error: dict = {}
    new_error.update(error)
    if error["loc"][0] == "items" and len(error["loc"]) == 4:
        new_error["loc"] = (
            f"item_{error['loc'][1]}",
            RLMarcEncoding[str(error["loc"][3])].value,
        )
    elif error["loc"][0] == "items" and len(error["loc"]) == 2:
        new_error["loc"] = (
            f"item_{error['loc'][1]}",
            RLMarcEncoding[str(error["loc"][0])].value,
        )
    else:
        new_error["loc"] = RLMarcEncoding[str(error["loc"][0])].value
    match (error["type"], error["ctx"]):
        case (
            "literal_error",
            {"expected": "' '"},
        ):
            new_error["msg"] = "Invalid indicator"
            return new_error
        case (
            "literal_error",
            {"expected": "'1'"},
        ):
            new_error["msg"] = "Invalid indicator"
            return new_error
        case (
            "literal_error",
            {"expected": "'EVP' or 'AUXAM'"},
        ):
            new_error["msg"] = "Invalid vendor code"
            return new_error
        case (
            "literal_error",
            {"expected": "'RL'"},
        ):
            new_error["msg"] = "Invalid library identifier"
            return new_error
        case (
            "literal_error",
            {"expected": "'8528'"},
        ):
            new_error["msg"] = "Invalid item call tag"
            return new_error
        case (
            "literal_error",
            {
                "expected": "'rcmb2', 'rcmf2', 'rcmg2', 'rc2ma', 'rcmp2', 'rcph2', 'rcpm2', 'rcpt2' or 'rc2cf'"
            },
        ):
            new_error["msg"] = "Item location does not match a valid location"
            return new_error
        case (
            "literal_error",
            {
                "expected": "'MAB', 'MAF', 'MAG', 'MAL', 'MAP', 'MAS', 'PAD', 'PAH', 'PAM', 'PAT' or 'SC'"
            },
        ):
            new_error["msg"] = "Order location does not match a valid location"
            return new_error
        case ("literal_error", {"expected": "'043'"}):
            new_error["msg"] = "Invalid item agency code"
            return new_error
        case (
            "string_pattern_mismatch",
            {"pattern": "^33433[0-9]{9}$|^33333[0-9]{9}$|^34444[0-9]{9}$"},
        ):
            new_error["msg"] = "Invalid barcode"
            return new_error
        case (
            "string_pattern_mismatch",
            {"pattern": "^ReCAP 23-\\d{6}$|^ReCAP 24-\\d{6}$"},
        ):
            new_error["msg"] = "Invalid ReCAP call number"
            return new_error
        case (
            "string_pattern_mismatch",
            {"pattern": "^\\d{3,}$"} | {"pattern": "^\\d{1,}$"},
        ):
            new_error["msg"] = "Invalid price; price should not include a decimal point"
            return new_error
        case (
            "string_pattern_mismatch",
            {"pattern": "^\\d{6}$"},
        ):
            new_error["msg"] = "Invalid date; invoice date should be YYMMDD"
            return new_error
        case (
            "string_pattern_mismatch",
            {"pattern": "^\\d{1,}\\.\\d{2}$"},
        ):
            new_error["msg"] = (
                "Invalid price; item price should include a decimal point"
            )
            return new_error
        case (
            "string_pattern_mismatch",
            {"pattern": "^[^a-z]+"},
        ):
            new_error["msg"] = "Invalid item message; message should be in all caps"
            return new_error
        case _:
            pass
    return new_error


def format_errors(e: ValidationError) -> dict[str, Any]:
    """
    A function to format a list of errors based on error type.
    Formats data to make it easier read when printed to terminal during validation.
    Concatenates missing and extra fields into single item in list to make it easier to
    read when printed to terminal during validation.

    Args:
        e: ValidationError (output from pydantic model)

    Returns:
        dict:
            error_count: int
            missing_field_count: int
            missing_fields: list
            extra_field_count: int
            extra_fields: list
            invalid_field_count: int
            invalid_fields: list
            other_errors: list
            other_error_fields: list
            errors: list

    """
    errors = []
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
            if type(converted_error["loc"]) is list:
                for loc in converted_error["loc"]:
                    extra_fields.append(loc)
            else:
                extra_fields.append(str(converted_error["loc"]))
        elif error["type"] == "Item/Order location check":
            converted_error = item_order_errors(error)
            other_errors.append(
                f"Invalid item/order data combination in {converted_error['loc'][0]}"
            )
            other_error_fields.append(converted_error["loc"])
            errors.append(converted_error)
        elif error["type"] == "union_tag_invalid":
            other_errors.append("Unable to validate item record; invalid 910$a")
            converted_error = match_errors(error)
            errors.append(converted_error)
        else:
            converted_error = match_errors(error)
            invalid_fields.append(converted_error["loc"])
            errors.append(converted_error)
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
        "error_count": len(missing_fields) + len(extra_fields) + len(errors),
        "missing_field_count": len(missing_fields),
        "missing_fields": missing_fields,
        "extra_field_count": len(extra_fields),
        "extra_fields": extra_fields,
        "invalid_field_count": len(invalid_fields),
        "invalid_fields": invalid_fields,
        "other_errors": other_errors,
        "other_error_fields": other_error_fields,
        "errors": errors,
    }
    return error_summary
