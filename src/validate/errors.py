from pydantic import ValidationError


def string_errors(error):
    new_error = {
        "type": error["type"],
        "loc": error["loc"][-1],
        "input": error["input"],
    }
    match (error["type"], error["loc"], error["ctx"]):
        case (
            "string_pattern_mismatch",
            ("item", "monograph_record", "item_barcode"),
            {"pattern": "^33433[0-9]{9}$|^33333[0-9]{9}$|^34444[0-9]{9}$"},
        ):
            new_error["msg"] = "Invalid barcode"
            return new_error
        case (
            "string_pattern_mismatch",
            ("item", "monograph_record", "item_call_no"),
            {"pattern": "^ReCAP 23-\\d{6}$|^ReCAP 24-\\d{6}$"},
        ):
            new_error["loc"] = "item_call_no"
            new_error["msg"] = "Invalid ReCAP call number"
            return new_error
        case (
            "string_pattern_mismatch",
            ("bib_call_no",),
            {"pattern": "^ReCAP 23-\\d{6}$|^ReCAP 24-\\d{6}$"},
        ):
            new_error["loc"] = "bib_call_no"
            new_error["msg"] = "Invalid ReCAP call number"
            return new_error
        case (
            "string_pattern_mismatch",
            ("order", "order_price") | ("invoice", _),
            {"pattern": "^\\d{3,}$"} | {"pattern": "^\\d{1,}$"},
        ):
            new_error[
                "msg"
            ] = f"Invalid price; {error['loc'][0].title()} price should not include a decimal point"
            return new_error
        case (
            "string_pattern_mismatch",
            ("invoice", "invoice_date"),
            {"pattern": "^\\d{6}$"},
        ):
            new_error["msg"] = "Invalid date; invoice date should be YYMMDD"
            return new_error
        case (
            "string_pattern_mismatch",
            ("item", _, _),
            {"pattern": "^\\d{1,}\\.\\d{2}$"},
        ):
            new_error[
                "msg"
            ] = "Invalid price; item price should include a decimal point"
            return new_error
        case (
            "string_pattern_mismatch",
            ("item", _, _),
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
            output = (f"{converted_error['msg']}", converted_error["input"])
            errors.append(output)
        elif error["type"] == "literal_error":
            converted_error = literal_errors(error)
            output = (f"{converted_error['msg']}", converted_error["input"])
            errors.append(output)
        elif error["type"] == "extra_forbidden":
            converted_error = other_errors(error)
            extra_field_loc = converted_error["loc"]
            extra_field_list.append(extra_field_loc)
        elif error["type"] == "missing":
            converted_error = other_errors(error)
            missing_field_loc = converted_error["loc"]
            missing_field_list.append(missing_field_loc)
        elif error["type"] == "Item/Order location check":
            output = (error["msg"], error["input"])
            errors.append(output)
        elif error["type"] == "call_no_test":
            output = (error["msg"], error["input"])
            errors.append(output)
        else:
            output = (error["msg"], error["input"])
            errors.append(output)
    missing_field_count = len(missing_field_list)
    extra_field_count = len(extra_field_list)
    if missing_field_count > 0:
        errors.append((f"{missing_field_count} missing field(s)", missing_field_list))
    else:
        pass
    if extra_field_count > 0:
        errors.append((f"{extra_field_count} extra field(s)", extra_field_list))
    else:
        pass
    return errors
