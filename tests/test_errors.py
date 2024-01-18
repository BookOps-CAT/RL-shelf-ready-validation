import pytest
from pydantic import ValidationError
from contextlib import nullcontext as does_not_raise
from src.validate.models import Record
from src.validate.errors import (
    format_error_messages,
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
        error = format_error_messages(e)
        assert error[0] == ("Invalid barcode", "12345678901234")


def test_extra_field_types(valid_pamphlet_record):
    valid_pamphlet_record["item"]["item_call_tag"] = "8528"
    try:
        Record(**valid_pamphlet_record)
    except ValidationError as e:
        error = format_error_messages(e)
        assert error[0] == ("1 extra field(s)", ["item_call_tag"])


def test_literal_error_types(valid_nypl_rl_record):
    valid_nypl_rl_record["item"]["item_call_tag"] = "8582"
    try:
        Record(**valid_nypl_rl_record)
    except ValidationError as e:
        error = format_error_messages(e)
        assert error[0] == ("Invalid item call tag", "8582")


def test_missing_types(valid_nypl_rl_record):
    del valid_nypl_rl_record["item"]["item_call_tag"]
    try:
        Record(**valid_nypl_rl_record)
    except ValidationError as e:
        error = format_error_messages(e)
        assert error[0] == ("1 missing field(s)", ["item_call_tag"])


def test_location_check_type(valid_nypl_rl_record):
    valid_nypl_rl_record["item"]["item_type"] = "55"
    try:
        Record(**valid_nypl_rl_record)
    except ValidationError as e:
        error = format_error_messages(e)
        assert error[0] == (
            "item_location/item_type/order_location combination is not valid.",
            ("rcmb2", "55", "MAB"),
        )


def test_call_no_test_type(valid_pamphlet_record):
    valid_pamphlet_record["bib_call_no"] = "ReCAP 23-111111"
    try:
        Record(**valid_pamphlet_record)
    except ValidationError as e:
        error = format_error_messages(e)
        assert error[0] == (
            "Record should not have a call_no. Check item type.",
            "ReCAP 23-111111",
        )


@pytest.mark.parametrize(
    "value",
    ["RECAP 23-00000", "ReCAP 11-11111"],
)
def test_bib_call_no_error(valid_nypl_rl_record, value):
    valid_nypl_rl_record["bib_call_no"] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = format_error_messages(e)
        assert new_error[0] == ("Invalid ReCAP call number", value)


@pytest.mark.parametrize(
    "value",
    ["ReCAP 24-0000", "ReCAP 11-11111"],
)
def test_item_call_no_error(valid_nypl_rl_record, value):
    valid_nypl_rl_record["item"]["item_call_no"] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = format_error_messages(e)
        assert new_error[0] == ("Invalid ReCAP call number", value)


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
        new_error = format_error_messages(e)
        assert new_error[0] == (
            "Invalid price; Invoice price should not include a decimal point",
            value,
        )


@pytest.mark.parametrize(
    "value",
    ["2.00", "order_price", "1.11"],
)
def test_order_price_error(valid_nypl_rl_record, value):
    valid_nypl_rl_record["order"]["order_price"] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = format_error_messages(e)
        assert new_error[0] == (
            "Invalid price; Order price should not include a decimal point",
            value,
        )


@pytest.mark.parametrize(
    "value",
    ["20240101", "01012024", "January 1, 2024"],
)
def test_invoice_date_error(valid_nypl_rl_record, value):
    valid_nypl_rl_record["invoice"]["invoice_date"] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = format_error_messages(e)
        assert new_error[0] == ("Invalid date; invoice date should be YYMMDD", value)


@pytest.mark.parametrize(
    "value",
    ["100", "1", "10", "222"],
)
def test_item_price_error(valid_nypl_rl_record, value):
    valid_nypl_rl_record["item"]["item_price"] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = format_error_messages(e)
        assert new_error[0] == (
            "Invalid price; item price should include a decimal point",
            value,
        )


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
        new_error = format_error_messages(e)
        assert new_error[0] == (
            "Invalid item message; message should be in all caps",
            value,
        )


@pytest.mark.parametrize(
    "value",
    ["AUX", "EV"],
)
def test_item_vendor_code_error(valid_nypl_rl_record, value):
    valid_nypl_rl_record["item"]["item_vendor_code"] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = format_error_messages(e)
        assert new_error[0] == ("Invalid vendor code", value)


@pytest.mark.parametrize(
    "value",
    ["EVIS", "Amalivre"],
)
def test_bib_vendor_code_error(valid_nypl_rl_record, value):
    valid_nypl_rl_record["bib_vendor_code"] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = format_error_messages(e)
        assert new_error[0] == ("Invalid vendor code", value)


@pytest.mark.parametrize(
    "value",
    ["rl", "research libraries", "nypl", "NYPL"],
)
def test_RL_identifier_error(valid_nypl_rl_record, value):
    valid_nypl_rl_record["rl_identifier"] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = format_error_messages(e)
        assert new_error[0] == ("Invalid research libraries identifier", value)


@pytest.mark.parametrize(
    "value",
    [100, "1", "10", "222"],
)
def test_call_tag_error(valid_nypl_rl_record, value):
    valid_nypl_rl_record["item"]["item_call_tag"] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = format_error_messages(e)
        assert new_error[0] == ("Invalid item call tag", value)


@pytest.mark.parametrize(
    "value",
    ["foo", "bar", "MAL", "item_location", "1"],
)
def test_item_location_error(valid_nypl_rl_record, value):
    valid_nypl_rl_record["item"]["item_location"] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = format_error_messages(e)
        assert new_error[0] == ("Item location does not match a valid location", value)


@pytest.mark.parametrize(
    "value",
    ["bbb", "aaa", "10", "222"],
)
def test_order_location_error(valid_nypl_rl_record, value):
    valid_nypl_rl_record["order"]["order_location"] = value
    with pytest.raises(ValidationError) as e:
        Record(**valid_nypl_rl_record)
        new_error = format_error_messages(e)
        assert new_error[0] == ("Order location does not match a valid location", value)


def test_extra_field_error(valid_pamphlet_record):
    valid_pamphlet_record["item"]["item_call_tag"] = "8528"
    with pytest.raises(ValidationError) as e:
        Record(**valid_pamphlet_record)
        new_error = format_error_messages(e)
        assert new_error[0] == ("1 extra field(s)", "item_call_tag")


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
            "Invalid vendor code",
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
            "Invalid vendor code",
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
            "Invalid research libraries identifier",
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
            "Invalid item call tag",
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
            "Item location does not match a valid location",
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
            "Order location does not match a valid location",
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
            "Invalid barcode",
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
            "Invalid ReCAP call number",
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
            "Invalid ReCAP call number",
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
            "Invalid price; Invoice price should not include a decimal point",
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
            "Invalid price; Order price should not include a decimal point",
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
            "Invalid date; invoice date should be YYMMDD",
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
            "Invalid price; item price should include a decimal point",
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
            "Invalid item message; message should be in all caps",
        ),
    ],
)
def test_all_string_errors(input, output):
    new_error = string_errors(input)
    assert new_error["msg"] == output


def test_string_error_pass(vendor_code_error):
    with does_not_raise():
        string_errors(vendor_code_error)


def test_literal_error_pass(string_barcode_error):
    with does_not_raise():
        literal_errors(string_barcode_error)


def test_extra_field_error_pass(vendor_code_error):
    with does_not_raise():
        other_errors(vendor_code_error)
