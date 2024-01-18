import pytest
from pydantic import ValidationError
from contextlib import nullcontext
from src.validate.models import Record
from src.validate.errors import (
    convert_error_messages,
    string_errors,
    literal_errors,
    other_errors,
    get_error_count,
)


def test_error_count(valid_nypl_rl_record):
    valid_nypl_rl_record["item"]["item_barcode"] = "12345678901234"
    try:
        Record(**valid_nypl_rl_record)
    except ValidationError as e:
        error_count = get_error_count(e)
        assert error_count == 1


def test_string_error_types(valid_nypl_rl_record):
    valid_nypl_rl_record["item"]["item_barcode"] = "12345678901234"
    try:
        Record(**valid_nypl_rl_record)
    except ValidationError as e:
        error = convert_error_messages(e)
        assert error[0]["type"] == "string_pattern_mismatch"


def test_extra_field_types(valid_pamphlet_record):
    valid_pamphlet_record["item"]["item_call_tag"] = "8528"
    try:
        Record(**valid_pamphlet_record)
    except ValidationError as e:
        error = convert_error_messages(e)
        assert error[0]["type"] == "extra_forbidden"


def test_literal_error_types(valid_nypl_rl_record):
    valid_nypl_rl_record["item"]["item_call_tag"] = "8582"
    try:
        Record(**valid_nypl_rl_record)
    except ValidationError as e:
        error = convert_error_messages(e)
        assert error[0]["type"] == "literal_error"


def test_missing_types(valid_nypl_rl_record):
    del valid_nypl_rl_record["item"]["item_call_tag"]
    try:
        Record(**valid_nypl_rl_record)
    except ValidationError as e:
        error = convert_error_messages(e)
        assert error[0]["type"] == "missing"


def test_location_check_type(valid_nypl_rl_record):
    valid_nypl_rl_record["item"]["item_type"] = "55"
    try:
        Record(**valid_nypl_rl_record)
    except ValidationError as e:
        error = convert_error_messages(e)
        assert error[0]["type"] == "Item/Order location check"


def test_call_no_test_type(valid_pamphlet_record):
    valid_pamphlet_record["bib_call_no"] = "ReCAP 23-111111"
    try:
        Record(**valid_pamphlet_record)
    except ValidationError as e:
        error = convert_error_messages(e)
        assert error[0]["type"] == "Call Number test"


def test_other_type(valid_nypl_rl_record):
    valid_nypl_rl_record["item"]["item_type"] = 2
    try:
        Record(**valid_nypl_rl_record)
    except ValidationError as e:
        error = convert_error_messages(e)
        assert len(error) == 1


@pytest.mark.parametrize(
    "key, value",
    [
        ("bib_call_no", "RECAP 23-00000"),
        ("bib_call_no", "ReCAP 11-11111"),
    ],
)
def test_bib_call_no_error(valid_nypl_rl_record, key, value):
    valid_nypl_rl_record[key] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = convert_error_messages(e)
        assert (
            new_error[0]["msg"]
            == "ReCAP call numbers should contain a 2-digit year and match the pattern 'ReCAP YY-999999'."
        )
        assert new_error[0]["loc"] == key


@pytest.mark.parametrize(
    "key, value",
    [
        ("item_call_no", "ReCAP 24-0000"),
        ("item_call_no", "ReCAP 11-11111"),
    ],
)
def test_item_call_no_error(valid_nypl_rl_record, key, value):
    valid_nypl_rl_record["item"][key] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = convert_error_messages(e)
        assert (
            new_error[0]["msg"]
            == "ReCAP call numbers should contain a 2-digit year and match the pattern 'ReCAP YY-999999'."
        )
        assert new_error[0]["loc"] == key


@pytest.mark.parametrize(
    "key, value",
    [
        ("invoice_price", "2.00"),
        ("invoice_shipping", "1.11"),
        ("invoice_tax", "22.22"),
        ("invoice_net_price", "12345.00"),
    ],
)
def test_invoice_price_error(valid_nypl_rl_record, key, value):
    valid_nypl_rl_record["invoice"][key] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = convert_error_messages(e)
        assert (
            new_error[0]["msg"] == "Invoice prices should not include decimal points."
        )
        assert new_error[0]["loc"] == key


@pytest.mark.parametrize(
    "key, value",
    [
        ("order_price", "2.00"),
        ("order_price", "1.11"),
    ],
)
def test_order_price_error(valid_nypl_rl_record, key, value):
    valid_nypl_rl_record["order"][key] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = convert_error_messages(e)
        assert new_error[0]["msg"] == "Order prices should not include decimal points."
        assert new_error[0]["loc"] == ("order_price")


@pytest.mark.parametrize(
    "key, value",
    [
        ("invoice_date", "20240101"),
        ("invoice_date", "01012024"),
        ("invoice_date", "January 1, 2024"),
    ],
)
def test_invoice_date_error(valid_nypl_rl_record, key, value):
    valid_nypl_rl_record["invoice"][key] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = convert_error_messages(e)
        assert new_error[0]["msg"] == "Invoice dates should match the pattern YYMMDD."
        assert new_error[0]["loc"] == ("invoice_date")


@pytest.mark.parametrize(
    "key, value",
    [
        ("item_price", "100"),
        ("item_price", "1"),
        ("item_price", "10"),
        ("item_price", "222"),
    ],
)
def test_item_price_error(valid_nypl_rl_record, key, value):
    valid_nypl_rl_record["item"][key] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = convert_error_messages(e)
        assert new_error[0]["msg"] == "Item prices must include decimal points."
        assert new_error[0]["loc"] == ("item_price")


@pytest.mark.parametrize(
    "key, value",
    [
        ("item_message", "foobar"),
        ("item_message", "lower case message"),
        ("message", "foo"),
        ("message", "bar"),
    ],
)
def test_message_error(valid_nypl_rl_record, key, value):
    valid_nypl_rl_record["item"][key] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = convert_error_messages(e)
        assert new_error[0]["msg"] == "Messages in item records should be all caps."
        assert new_error[0]["loc"] == key


@pytest.mark.parametrize(
    "key, value",
    [
        ("item_vendor_code", "AUX"),
        ("item_vendor_code", "EV"),
    ],
)
def test_item_vendor_code_error(valid_nypl_rl_record, key, value):
    valid_nypl_rl_record["item"][key] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = convert_error_messages(e)
        assert new_error[0]["msg"] == "Invalid vendor code."
        assert new_error[0]["loc"] == key


@pytest.mark.parametrize(
    "key, value",
    [
        ("bib_vendor_code", "EVIS"),
        ("bib_vendor_code", "Amalivre"),
    ],
)
def test_bib_vendor_code_error(valid_nypl_rl_record, key, value):
    valid_nypl_rl_record[key] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = convert_error_messages(e)
        assert new_error[0]["msg"] == "Invalid vendor code."
        assert new_error[0]["loc"] == key


@pytest.mark.parametrize(
    "value",
    ["rl", "research libraries", "nypl", "NYPL"],
)
def test_RL_identifier_error(valid_nypl_rl_record, value):
    valid_nypl_rl_record["rl_identifier"] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = convert_error_messages(e)
        assert new_error[0]["msg"] == "Invalid research libraries identifier."
        assert new_error[0]["loc"] == "rl_identifier"


@pytest.mark.parametrize(
    "value",
    [100, "1", "10", "222"],
)
def test_call_tag_error(valid_nypl_rl_record, value):
    valid_nypl_rl_record["item"]["item_call_tag"] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = convert_error_messages(e)
        assert new_error[0]["msg"] == "Invalid item call tag. Should be '8528'."
        assert new_error[0]["loc"] == "item_call_tag"


@pytest.mark.parametrize(
    "value",
    ["foo", "bar", "MAL", "item_location", "1"],
)
def test_item_location_error(valid_nypl_rl_record, value):
    valid_nypl_rl_record["item"]["item_location"] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = convert_error_messages(e)
        assert new_error[0]["msg"] == "Item location does not match a valid location."
        assert new_error[0]["loc"] == "item_location"


@pytest.mark.parametrize(
    "value",
    ["bbb", "aaa", "10", "222"],
)
def test_order_location_error(valid_nypl_rl_record, value):
    valid_nypl_rl_record["order"]["order_location"] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = convert_error_messages(e)
        assert new_error[0]["msg"] == "Order location does not match a valid location."
        assert new_error[0]["loc"] == "order_location"


def test_extra_field_error(valid_pamphlet_record):
    valid_pamphlet_record["item"]["item_call_tag"] = "8528"
    with pytest.raises(ValidationError) as e:
        Record(**valid_pamphlet_record)
        new_error = convert_error_messages(e)
        assert (
            new_error[0]["msg"]
            == "This bib record should not contain an item record. Check the material type."
        )
        assert new_error[0]["type"] == "extra_forbidden"


@pytest.mark.parametrize(
    "input, output",
    [
        (
            {
                "type": "literal_error",
                "loc": ("bib_vendor_code",),
                "msg": "Input should be 'AUXAM' or 'EVP'",
                "input": "EVIS",
                "ctx": {"expected": "'EVP' or 'AUXAM'"},
                "url": "https://errors.pydantic.dev/2.5/v/literal_error",
            },
            "Invalid vendor code.",
        ),
        (
            {
                "type": "literal_error",
                "loc": ("item", "monograph_record", "item_vendor_code"),
                "msg": "Input should be 'AUXAM' or 'EVP'",
                "input": "EVIS",
                "ctx": {"expected": "'EVP' or 'AUXAM'"},
                "url": "https://errors.pydantic.dev/2.5/v/literal_error",
            },
            "Invalid vendor code.",
        ),
        (
            {
                "type": "literal_error",
                "loc": ("rl_identifier",),
                "msg": "Input should be 'RL'",
                "input": "RLRL",
                "ctx": {"expected": "'RL'"},
                "url": "https://errors.pydantic.dev/2.5/v/literal_error",
            },
            "Invalid research libraries identifier.",
        ),
        (
            {
                "type": "literal_error",
                "loc": ("item", "monograph_record", "item_call_tag"),
                "msg": "Input should be '8528'",
                "input": "8582",
                "ctx": {"expected": "'8528'"},
                "url": "https://errors.pydantic.dev/2.5/v/literal_error",
            },
            "Invalid item call tag. Should be '8528'.",
        ),
        (
            {
                "type": "literal_error",
                "loc": ("item", "monograph_record", "item_location"),
                "msg": "Input should be 'rcmb2', 'rcmf2', 'rcmg2', 'rc2ma', 'rcmp2', 'rcph2', 'rcpm2', 'rcpt2' or 'rc2cf'",
                "input": "aaaaa",
                "ctx": {
                    "expected": "'rcmb2', 'rcmf2', 'rcmg2', 'rc2ma', 'rcmp2', 'rcph2', 'rcpm2', 'rcpt2' or 'rc2cf'"
                },
                "url": "https://errors.pydantic.dev/2.5/v/literal_error",
            },
            "Item location does not match a valid location.",
        ),
        (
            {
                "type": "literal_error",
                "loc": ("order", "order_location"),
                "msg": "Input should be 'MAB', 'MAF', 'MAG', 'MAL', 'MAP', 'MAS', 'PAD', 'PAH', 'PAM', 'PAT' or 'SC'",
                "input": "aaa",
                "ctx": {
                    "expected": "'MAB', 'MAF', 'MAG', 'MAL', 'MAP', 'MAS', 'PAD', 'PAH', 'PAM', 'PAT' or 'SC'"
                },
                "url": "https://errors.pydantic.dev/2.5/v/literal_error",
            },
            "Order location does not match a valid location.",
        ),
    ],
)
def test_all_literal_errors(input, output):
    new_error = literal_errors(input)
    assert new_error["msg"] == output


@pytest.mark.parametrize(
    "input, output",
    [
        (
            {
                "type": "string_pattern_mismatch",
                "loc": ("item", "monograph_record", "item_barcode"),
                "msg": "String should match pattern '^33433[0-9]{9}$|^33333[0-9]{9}$|^34444[0-9]{9}$'",
                "input": "12345678901234",
                "ctx": {"pattern": "^33433[0-9]{9}$|^33333[0-9]{9}$|^34444[0-9]{9}$"},
                "url": "https://errors.pydantic.dev/2.5/v/string_pattern_mismatch",
            },
            "Invalid barcode. Barcodes should be 14 digits long and begin with: '33433' for NYPL Research Libraries, '33333' for NYPL Branch Libraries, or '34444' for BPL.",
        ),
        (
            {
                "type": "string_pattern_mismatch",
                "loc": ("item", "monograph_record", "item_call_no"),
                "msg": "String should match pattern '^ReCAP 23-\\d{6}$|^ReCAP 24-\\d{6}$'",
                "input": "ReCAP 23-99999",
                "ctx": {"pattern": "^ReCAP 23-\\d{6}$|^ReCAP 24-\\d{6}$"},
                "url": "https://errors.pydantic.dev/2.5/v/string_pattern_mismatch",
            },
            "ReCAP call numbers should contain a 2-digit year and match the pattern 'ReCAP YY-999999'.",
        ),
        (
            {
                "type": "string_pattern_mismatch",
                "loc": ("bib_call_no",),
                "msg": "String should match pattern '^ReCAP 23-\\d{6}$|^ReCAP 24-\\d{6}$'",
                "input": "ReCAP 23-99999",
                "ctx": {"pattern": "^ReCAP 23-\\d{6}$|^ReCAP 24-\\d{6}$"},
                "url": "https://errors.pydantic.dev/2.5/v/string_pattern_mismatch",
            },
            "ReCAP call numbers should contain a 2-digit year and match the pattern 'ReCAP YY-999999'.",
        ),
        (
            {
                "type": "string_pattern_mismatch",
                "loc": ("invoice", "invoice_price"),
                "msg": "String should match pattern '^\\d{3,}$'",
                "input": "12.34",
                "ctx": {"pattern": "^\\d{3,}$"},
                "url": "https://errors.pydantic.dev/2.5/v/string_pattern_mismatch",
            },
            "Invoice prices should not include decimal points.",
        ),
        (
            {
                "type": "string_pattern_mismatch",
                "loc": ("order", "order_price"),
                "msg": "String should match pattern '^\\d{3,}$'",
                "input": "12.34",
                "ctx": {"pattern": "^\\d{3,}$"},
                "url": "https://errors.pydantic.dev/2.5/v/string_pattern_mismatch",
            },
            "Order prices should not include decimal points.",
        ),
        (
            {
                "type": "string_pattern_mismatch",
                "loc": ("invoice", "invoice_date"),
                "msg": "String should match pattern '^\\d{6}$'",
                "input": "jan. 01, 2023",
                "ctx": {"pattern": "^\\d{6}$"},
                "url": "https://errors.pydantic.dev/2.5/v/string_pattern_mismatch",
            },
            "Invoice dates should match the pattern YYMMDD.",
        ),
        (
            {
                "type": "string_pattern_mismatch",
                "loc": ("item", "monograph_record", "item_price"),
                "msg": "String should match pattern '^\\d{1,}\\.\\d{2}$'",
                "input": "1234",
                "ctx": {"pattern": "^\\d{1,}\\.\\d{2}$"},
                "url": "https://errors.pydantic.dev/2.5/v/string_pattern_mismatch",
            },
            "Item prices must include decimal points.",
        ),
        (
            {
                "type": "string_pattern_mismatch",
                "loc": ("item", "monograph_record", "item_message"),
                "msg": "String should match pattern '^[^a-z]+'",
                "input": "aaaaa",
                "ctx": {"pattern": "^[^a-z]+"},
                "url": "https://errors.pydantic.dev/2.5/v/string_pattern_mismatch",
            },
            "Messages in item records should be all caps.",
        ),
    ],
)
def test_all_string_errors(input, output):
    new_error = string_errors(input)
    assert new_error["msg"] == output


@pytest.mark.parametrize(
    "key, value",
    [
        (
            "msg",
            "This bib record should not contain an item record. Check the material type.",
        ),
        ("loc", ("item", "pamphlet", "item_vendor_code")),
    ],
)
def test_extra_field_errors(extra_field_error, key, value):
    new_error = other_errors(extra_field_error)
    assert new_error[key] == value


def test_string_error_pass(vendor_code_error):
    with nullcontext():
        string_errors(vendor_code_error)


def test_literal_error_pass(string_barcode_error):
    with nullcontext():
        literal_errors(string_barcode_error)


def test_extra_field_error_pass(vendor_code_error):
    with nullcontext():
        other_errors(vendor_code_error)
