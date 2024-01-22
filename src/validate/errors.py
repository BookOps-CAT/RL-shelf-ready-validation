from pydantic import ValidationError
from src.validate.translate import RLMarcEncoding


def string_errors(error):
    loc = error["loc"][-1]
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
            ("items", _, _, "item_call_no"),
            {"pattern": "^ReCAP 23-\\d{6}$|^ReCAP 24-\\d{6}$"},
        ):
            new_error = {
                "type": error["type"],
                "loc": "item_call_no",
                "input": error["input"],
                "msg": "Invalid ReCAP call number",
            }
            return new_error
        case (
            "string_pattern_mismatch",
            ("bib_call_no",),
            {"pattern": "^ReCAP 23-\\d{6}$|^ReCAP 24-\\d{6}$"},
        ):
            new_error = {
                "type": error["type"],
                "loc": "bib_call_no",
                "input": error["input"],
                "msg": "Invalid ReCAP call number",
            }
            return new_error
        case (
            "string_pattern_mismatch",
            ("order_price") | (r"^invoice.+$"),
            {"pattern": "^\\d{3,}$"} | {"pattern": "^\\d{1,}$"},
        ):
            new_error[
                "msg"
            ] = f"Invalid price; {error['loc'][0].title()} price should not include a decimal point"
            return new_error
        case (
            "string_pattern_mismatch",
            ("invoice_date"),
            {"pattern": "^\\d{6}$"},
        ):
            new_error["msg"] = "Invalid date; invoice date should be YYMMDD"
            return new_error
        case (
            "string_pattern_mismatch",
            ("items", _, _, _),
            {"pattern": "^\\d{1,}\\.\\d{2}$"},
        ):
            new_error[
                "msg"
            ] = "Invalid price; item price should include a decimal point"
            return new_error
        case (
            "string_pattern_mismatch",
            ("item", _, _, _),
            {"pattern": "^[^a-z]+"},
        ):
            new_error["msg"] = "Invalid item message; message should be in all caps"
            return new_error
        case _:
            pass


def literal_errors(error):
    new_error = {
        "type": error["type"],
        "loc": error["loc"][-1],
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
            new_error["msg"] = "Invalid research libraries identifier"
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
    if error["type"] != "string_pattern_mismatch" or "literal_error":
        new_error = {
            "type": error["type"],
            "loc": error["loc"][-1],
            "input": error["input"],
        }
        return new_error
    else:
        return error


def get_error_count(e: ValidationError):
    total_errors = e.error_count()
    return total_errors


def format_error_messages(e: ValidationError):
    errors = []
    missing_field_list = []
    extra_field_list = []
    for error in e.errors():
        if error["type"] == "string_pattern_mismatch":
            converted_error = string_errors(error)
            output = (f"{RLMarcEncoding[converted_error["loc"]].value}", f"{converted_error['msg']}", converted_error["input"])
            errors.append(output)
        elif error["type"] == "literal_error":
            converted_error = literal_errors(error)
            output = (f"{RLMarcEncoding[converted_error["loc"]].value}", f"{converted_error['msg']}", converted_error["input"])
            errors.append(output)
        elif error["type"] == "extra_forbidden":
            converted_error = other_errors(error)
            extra_field_loc = RLMarcEncoding[converted_error["loc"]].value
            extra_field_list.append(extra_field_loc)
        elif error["type"] == "missing":
            converted_error = other_errors(error)
            missing_field_loc = RLMarcEncoding[converted_error["loc"]].value
            missing_field_list.append(missing_field_loc)
        elif error["type"] == "Item/Order location check":
            output = (RLMarcEncoding[error["loc"]].value, error["msg"], error["input"])
            errors.append(output)
        elif error["type"] == "call_no_test":
            output = (RLMarcEncoding[error["loc"]].value, error["msg"], error["input"])
            errors.append(output)
        else:
            output = (RLMarcEncoding[error["loc"]].value, error["msg"], error["input"])
            errors.append(output)
    missing_field_count = len(missing_field_list)
    extra_field_count = len(extra_field_list)
    if missing_field_count > 0:
        errors.append((f"{missing_field_count} missing field/subfield(s)", missing_field_list))
    else:
        pass
    if extra_field_count > 0:
        errors.append((f"{extra_field_count} extra field/subfield(s)", extra_field_list))
    else:
        pass
    return errors
