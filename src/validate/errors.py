from pydantic import ValidationError


def convert_error_messages(e: ValidationError):
    for error in e.errors():
        new_error = {}
        locs = list(error["loc"])
        last_loc = locs[-1]
        new_error = {
            "type": error["type"],
            "loc": last_loc,
            "input": error["input"],
            "ctx": error["ctx"],
        }
        match (error["type"], error["loc"], error["ctx"]):
            case (
                "string_pattern_mismatch",
                ("item", "monograph_record", "item_barcode"),
                {"pattern": "^33433[0-9]{9}$|^33333[0-9]{9}$|^34444[0-9]{9}$"},
            ):
                new_error[
                    "msg"
                ] = "Invalid barcode. Barcodes should be 14 digits long and begin with: '33433' for NYPL Research Libraries, '33333' for NYPL Branch Libraries, or '34444' for BPL."
                return new_error
            case (
                "string_pattern_mismatch",
                ("item", "monograph_record", "item_call_no"),
                {"pattern": "^ReCAP 23-\\d{6}$|^ReCAP 24-\\d{6}$"},
            ):
                new_error["loc"] = "item_call_no"
                new_error[
                    "msg"
                ] = "ReCAP call numbers should contain a 2-digit year and match the pattern 'ReCAP YY-999999'."
                return new_error
            case (
                "string_pattern_mismatch",
                ("bib_call_no",),
                {"pattern": "^ReCAP 23-\\d{6}$|^ReCAP 24-\\d{6}$"},
            ):
                new_error["loc"] = "bib_call_no"
                new_error[
                    "msg"
                ] = "ReCAP call numbers should contain a 2-digit year and match the pattern 'ReCAP YY-999999'."
                return new_error
            case (
                "string_pattern_mismatch",
                ("order", "monograph_record", "order_price") | ("invoice", _),
                {"pattern": "^\\d{3,}$"} | {"pattern": "^\\d{1,}$"},
            ):
                new_error[
                    "msg"
                ] = f"{error['loc'][0].title()} prices should not include decimal points."
                return new_error
            case (
                "string_pattern_mismatch",
                ("invoice", "monograph_record", "invoice_date"),
                {"pattern": "^\\d{6}$"},
            ):
                new_error["msg"] = "Invoice dates should match the pattern YYMMDD."
                return new_error
            case (
                "string_pattern_mismatch",
                ("item", _),
                {"pattern": "^\\d{1,}\\.\\d{2}$"},
            ):
                new_error["msg"] = "Item prices must include decimal points."
                return new_error
            case (
                "string_pattern_mismatch",
                ("item", _),
                {"pattern": "^[^a-z]+"},
            ):
                new_error["msg"] = "Messages in item records should be all caps."
                return new_error
            case (
                "literal_error",
                _,
                {"expected": "'AUXAM' or 'EVP'"},
            ):
                new_error["msg"] = "Invalid vendor code."
                return new_error
            case (
                "literal_error",
                ("rl_identifier",),
                {"expected": "'RL'"},
            ):
                new_error["msg"] = "Invalid research libraries identifier."
                return new_error
            case (
                "literal_error",
                ("item", "monograph_record", "item_call_tag"),
                {"expected": "'8528'"},
            ):
                new_error["msg"] = "Invalid item call tag. Should be '8528'."
                return new_error
            case (
                "literal_error",
                ("item", "monograph_record", "item_location"),
                {
                    "expected": "'rcmb2', 'rcmf2', 'rcmg2', 'rc2ma', 'rcmp2', 'rcph2', 'rcpm2', 'rcpt2' or 'rc2cf'"
                },
            ):
                new_error["msg"] = "Item location does not match a valid location."
                new_error = new_error.pop("ctx")
                return new_error
            case (
                "literal_error",
                ("order", "order_location"),
                {
                    "expected": "'MAB', 'MAF', 'MAG', 'MAL', 'MAP', 'MAS', 'PAD', 'PAH', 'PAM', 'PAT' or 'SC'"
                },
            ):
                new_error["msg"] = "Order location does not match a valid location."

                return new_error
            case (
                "extra_forbidden",
                _,
                _,
            ):
                new_error[
                    "msg"
                ] = "This bib record should not contain an item record. Check the material type."

                return new_error
            case _:
                return error
