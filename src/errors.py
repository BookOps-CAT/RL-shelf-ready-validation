from pydantic import ValidationError
from src.translate import RLMarcEncoding
from typing import List


def string_errors(error):
    """
    A function to convert a standard pydantic "string_pattern_mismatch" error output
    Removes regex and other technical info from output

    Returns a new_error dict object containing:
     - error type: str
     - error location: tuple
     - error input: dict
     - error message: str
    """
    if "items" in error["loc"]:
        loc = (f"item_{error['loc'][1]}", RLMarcEncoding[error["loc"][-1]].value)
    else:
        loc = RLMarcEncoding[error["loc"][-1]].value
    new_error = {
        "type": error["type"],
        "loc": loc,
        "input": error["input"],
    }
    match (error["type"], error["loc"], error["ctx"]):
        case (
            "string_pattern_mismatch",
            ("items", _, _, "item_barcode"),
            {"pattern": "^33433[0-9]{9}$|^33333[0-9]{9}$|^34444[0-9]{9}$"},
        ):
            new_error["msg"] = "Invalid barcode"
            return new_error
        case (
            "string_pattern_mismatch",
            _,
            {"pattern": "^ReCAP 23-\\d{6}$|^ReCAP 24-\\d{6}$"},
        ):
            new_error["msg"] = "Invalid ReCAP call number"
            return new_error
        case (
            "string_pattern_mismatch",
            _,
            {"pattern": "^\\d{3,}$"} | {"pattern": "^\\d{1,}$"},
        ):
            new_error[
                "msg"
            ] = f"Invalid price; {error['loc'][0].title()} should not include a decimal point"
            return new_error
        case (
            "string_pattern_mismatch",
            _,
            {"pattern": "^\\d{6}$"},
        ):
            new_error["msg"] = "Invalid date; invoice date should be YYMMDD"
            return new_error
        case (
            "string_pattern_mismatch",
            ("items", _, _, "item_price"),
            {"pattern": "^\\d{1,}\\.\\d{2}$"},
        ):
            new_error[
                "msg"
            ] = "Invalid price; item price should include a decimal point"
            return new_error
        case (
            "string_pattern_mismatch",
            ("items", _, _, _),
            {"pattern": "^[^a-z]+"},
        ):
            new_error["msg"] = "Invalid item message; message should be in all caps"
            return new_error
        case _:
            pass


def literal_errors(error):
    """
    A function to convert a standard pydantic "literal_error" error output

    Returns a new_error dict object containing:
     - error type: str
     - error location: tuple
     - error input: dict
     - error message: str
    """
    if "items" in error["loc"]:
        loc = (f"item_{error['loc'][1]}", RLMarcEncoding[error["loc"][-1]].value)
    else:
        loc = RLMarcEncoding[error["loc"][-1]].value
    new_error = {
        "type": error["type"],
        "loc": loc,
        "input": error["input"],
    }
    match (error["type"], error["ctx"]):
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
        case _:
            pass


def other_errors(error):
    """
    A function to convert a standard pydantic error output for other error types

    Returns an error dict object containing:
     - error type: str
     - error location: tuple
     - error input: dict
     - error message: str
    """
    new_error = {
        "type": error["type"],
        "input": error["input"],
    }
    if error["type"] == "extra_forbidden":
        if "items" in error["loc"]:
            item_number = 0
            new_error["loc"] = (
                f"item_{item_number}",
                RLMarcEncoding[error["loc"][-1]].value,
            )
            item_number = +1
        else:
            new_error["loc"] = RLMarcEncoding[error["loc"][-1]].value
    elif error["type"] == "missing":
        if "items" in error["loc"]:
            item_number = 0
            new_error["loc"] = (
                f"item_{item_number}",
                RLMarcEncoding[error["loc"][-1]].value,
            )
            item_number += 1
        else:
            new_error["loc"] = RLMarcEncoding[error["loc"][-1]].value
    elif error["type"] == "Item/Order location check":
        new_error["loc"] = (
            f"item_{error['loc'][0]}",
            {RLMarcEncoding[error["loc"][1]].value},
            {RLMarcEncoding[error["loc"][2]].value},
            {RLMarcEncoding[error["loc"][3]].value},
        )
    else:
        new_error["loc"] = RLMarcEncoding[error["loc"][-1]].value
    return new_error


def format_error_messages(e: ValidationError) -> List:
    """
    A function to convert a list of errors based on error type
    For "extra_forbidden" and "missing" errors, adds error count to error message

    Returns a list of dicts containing
     - error type: str
     - error location: tuple
     - error input: dict
     - error message: str

    """
    errors = []
    missing_field_list = []
    extra_field_list = []
    missing_field_error = {}
    for error in e.errors():
        if error["type"] == "string_pattern_mismatch":
            converted_error = string_errors(error)
            errors.append(converted_error)
        elif error["type"] == "literal_error":
            converted_error = literal_errors(error)
            errors.append(converted_error)
        elif error["type"] == "extra_forbidden":
            converted_error = other_errors(error)
            extra_field_list.append(converted_error["loc"])
        elif error["type"] == "missing":
            converted_error = other_errors(error)
            missing_field_list.append(converted_error["loc"])
        elif error["type"] == "Item/Order location check":
            converted_error = other_errors(error)
            errors.append(converted_error)
        else:
            converted_error = other_errors(error)
            errors.append(converted_error)
    missing_field_count = len(missing_field_list)
    extra_field_count = len(extra_field_list)
    if missing_field_count > 0:
        missing_field_error = {
            "type": "missing",
            "loc": missing_field_list,
            "input": missing_field_list,
            "msg": f"{missing_field_count} missing field/subfield(s)",
        }
        errors.append(missing_field_error)
    else:
        pass
    if extra_field_count > 0:
        extra_field_error = {
            "type": "extra_forbidden",
            "loc": extra_field_list,
            "input": extra_field_list,
            "msg": f"{extra_field_count} extra field/subfield(s)",
        }
        errors.append(extra_field_error)
    else:
        pass
    return errors
