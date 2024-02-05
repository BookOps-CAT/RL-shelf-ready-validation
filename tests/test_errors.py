import pytest
from pydantic import ValidationError
from shelf_ready_validator.models import MonographRecord, OtherMaterialRecord
from contextlib import nullcontext as does_not_raise
from shelf_ready_validator.errors import (
    format_errors,
    match_errors,
    extra_errors,
)


def test_error_count(valid_rl_monograph_record):
    valid_rl_monograph_record["invoice_copies"] = 1
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    error_count = e.value.error_count()
    assert error_count == 1


def test_string_error_types(valid_rl_monograph_record):
    valid_rl_monograph_record["bib_call_no"] = "ReCAP 23-12345"
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    assert e.value.errors()[0]["type"] == "string_pattern_mismatch"


def test_extra_field_types(valid_pamphlet_record):
    valid_pamphlet_record["bib_call_no"] = "ReCAP 23-000000"
    with pytest.raises(ValidationError) as e:
        OtherMaterialRecord(**valid_pamphlet_record)
    errors = e.value
    error = format_errors(errors)
    assert error["extra_field_count"] == 1


def test_literal_error_types(valid_rl_monograph_record):
    valid_rl_monograph_record["items"][0]["item_call_tag"] = "8582"
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    errors = e.value
    error = format_errors(errors)
    assert error["errors"][0]["msg"] == "Invalid item call tag"


def test_missing_item_fields(valid_rl_monograph_record):
    del valid_rl_monograph_record["items"][0]["item_call_tag"]
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    errors = e.value
    error = format_errors(errors)
    assert error["missing_fields"] == [("item_0", "949$z")]


def test_missing_other_fields(valid_rl_monograph_record):
    del valid_rl_monograph_record["bib_call_no"]
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    errors = e.value
    error = format_errors(errors)
    assert error["missing_fields"] == ["852"]


def test_location_check_type(valid_rl_monograph_record):
    valid_rl_monograph_record["items"][0]["item_type"] = "55"
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    errors = e.value
    error = format_errors(errors)
    assert error["errors"][0]["type"] == "Item/Order location check"


@pytest.mark.parametrize(
    "value",
    ["RECAP 23-00000", "ReCAP 11-11111"],
)
def test_bib_call_no_error(valid_rl_monograph_record, value):
    valid_rl_monograph_record["bib_call_no"] = value
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    errors = e.value
    error = format_errors(errors)
    assert error["errors"][0]["msg"] == "Invalid ReCAP call number"


@pytest.mark.parametrize(
    "data",
    ["ReCAP 24-0000", "ReCAP 11-11111"],
)
def test_item_call_no_error(valid_rl_monograph_record, data):
    valid_rl_monograph_record["items"][0]["item_call_no"] = data
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    errors = e.value
    error = format_errors(errors)
    assert error
    assert error["errors"][0]["msg"] == "Invalid ReCAP call number"


@pytest.mark.parametrize(
    "data",
    ["January 1, 2024", "2024-01-01"],
)
def test_invoice_date_error(valid_rl_monograph_record, data):
    valid_rl_monograph_record["invoice_date"] = data
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    errors = e.value
    error = format_errors(errors)
    assert error["errors"][0]["msg"] == "Invalid date; invoice date should be YYMMDD"


@pytest.mark.parametrize(
    "field", ["invoice_price", "invoice_shipping", "invoice_tax", "invoice_net_price"]
)
def test_invoice_price_error_2(valid_rl_monograph_record, field):
    valid_rl_monograph_record[field] = "2.00"
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    errors = e.value
    error = format_errors(errors)
    assert error["errors"][0]["type"] == "string_pattern_mismatch"


@pytest.mark.parametrize(
    "data",
    ["2.00", "order_price", "1.11"],
)
def test_order_price_error(valid_rl_monograph_record, data):
    valid_rl_monograph_record["order_price"] = data
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    errors = e.value
    error = format_errors(errors)
    assert error["errors"][0]["type"] == "string_pattern_mismatch"


@pytest.mark.parametrize(
    "data",
    ["100", "1", "10", "222"],
)
def test_item_price_error(valid_rl_monograph_record, data):
    valid_rl_monograph_record["items"][0]["item_price"] = data
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    errors = e.value
    error = format_errors(errors)
    assert (
        error["errors"][0]["msg"]
        == "Invalid price; item price should include a decimal point"
    )


@pytest.mark.parametrize(
    "field, data",
    [("item_ind1", "0"), ("item_ind2", "0")],
)
def test_item_indictor_error(valid_rl_monograph_record, field, data):
    valid_rl_monograph_record["items"][0][field] = data
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    errors = e.value
    error = format_errors(errors)
    assert error["errors"][0]["msg"] == "Invalid indicator"


@pytest.mark.parametrize(
    "field, data",
    [
        ("item_message", "foobar"),
        ("item_message", "lower case message"),
        ("message", "foo"),
        ("message", "bar"),
    ],
)
def test_message_error(valid_rl_monograph_record, field, data):
    valid_rl_monograph_record["items"][0][field] = data
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    errors = e.value
    error = format_errors(errors)
    assert (
        error["errors"][0]["msg"]
        == "Invalid item message; message should be in all caps"
    )


@pytest.mark.parametrize(
    "data",
    ["AUX", "EV"],
)
def test_item_vendor_code_error(valid_rl_monograph_record, data):
    valid_rl_monograph_record["items"][0]["item_vendor_code"] = data
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    errors = e.value
    error = format_errors(errors)
    assert error["errors"][0]["type"] == "literal_error"


@pytest.mark.parametrize(
    "data",
    ["EVIS", "Amalivre"],
)
def test_bib_vendor_code_error(valid_rl_monograph_record, data):
    valid_rl_monograph_record["bib_vendor_code"] = data
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    errors = e.value
    error = format_errors(errors)
    assert error["errors"][0]["type"] == "literal_error"


def test_item_union_error(valid_rl_monograph_record):
    valid_rl_monograph_record["items"][0]["library"] = "NYPL"
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    errors = e.value
    error = format_errors(errors)
    assert error["errors"][0]["type"] == "union_tag_invalid"


def test_call_tag_error(valid_rl_monograph_record):
    valid_rl_monograph_record["items"][0]["item_call_tag"] = "8582"
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    errors = e.value
    error = format_errors(errors)
    assert error["errors"][0]["msg"] == "Invalid item call tag"


@pytest.mark.parametrize(
    "data",
    ["foo", "bar", "MAL", "item_location", "1"],
)
def test_item_location_error(valid_rl_monograph_record, data):
    """
    Item location/item type/order location check runs before model validatiion
    """

    valid_rl_monograph_record["items"][0]["item_location"] = data
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    errors = e.value
    error = format_errors(errors)
    assert error["errors"][1]["msg"] == "Item location does not match a valid location"


@pytest.mark.parametrize(
    "data",
    ["bbb", "aaa", "10", "222"],
)
def test_order_location_error(valid_rl_monograph_record, data):
    """
    Item location/item type/order location check runs before model validatiion
    With two items on valid_rl_monograph_record, this is the third error to be raised
    """

    valid_rl_monograph_record["order_location"] = data
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    errors = e.value
    error = format_errors(errors)
    assert error["errors"][2]["msg"] == "Order location does not match a valid location"


def test_extra_field_error(valid_pamphlet_record):
    valid_pamphlet_record["items"] = [
        {
            "item_call_tag": "8528",
        }
    ]

    with pytest.raises(ValidationError) as e:
        OtherMaterialRecord(**valid_pamphlet_record)
    errors = e.value
    error = format_errors(errors)
    assert error["extra_fields"] == ["949_0"]


@pytest.mark.parametrize(
    "input, output",
    [
        (
            {
                "type": "literal_error",
                "loc": (
                    "items",
                    0,
                    "RL",
                    "item_agency",
                ),
                "msg": "Input should be '43'",
                "input": "44",
                "ctx": {"expected": "'43'"},
                "url": "https://errors.pydantic.dev/2.5/v/literal_error",
            },
            "Invalid item agency code",
        ),
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
                "loc": ("items", 0, "RL", "item_vendor_code"),
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
                "loc": ("items", 0, "RL", "library"),
                "msg": "Input should be 'RL'",
                "input": "RLRL",
                "ctx": {"expected": "'RL'"},
                "url": "https://errors.pydantic.dev/2.5/v/literal_error",
            },
            "Invalid library identifier",
        ),
        (
            {
                "type": "literal_error",
                "loc": ("items", 0, "RL", "item_call_tag"),
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
                "loc": ("items", 0, "RL", "item_location"),
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
                "loc": ("order_location",),
                "msg": "Input should be 'MAB', 'MAF', 'MAG', 'MAL', 'MAP', 'MAS', 'PAD', 'PAH', 'PAM', 'PAT' or 'SC'",
                "input": "aaa",
                "ctx": {
                    "expected": "'MAB', 'MAF', 'MAG', 'MAL', 'MAP', 'MAS', 'PAD', 'PAH', 'PAM', 'PAT' or 'SC'"
                },
                "url": "https://errors.pydantic.dev/2.5/v/literal_error",
            },
            "Order location does not match a valid location",
        ),
        (
            {
                "type": "string_pattern_mismatch",
                "loc": ("items", 0, "RL", "item_barcode"),
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
                "loc": ("items", 0, "RL", "item_call_no"),
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
                "loc": ("invoice_price",),
                "msg": "String should match pattern '^\\d{3,}$'",
                "input": "12.34",
                "ctx": {"pattern": "^\\d{3,}$"},
                "url": "https://errors.pydantic.dev/2.5/v/string_pattern_mismatch",
            },
            "Invalid price; price should not include a decimal point",
        ),
        (
            {
                "type": "string_pattern_mismatch",
                "loc": ("invoice_date",),
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
                "loc": ("items", 0, "RL", "item_price"),
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
                "loc": ("items", 0, "RL", "item_message"),
                "msg": "String should match pattern '^[^a-z]+'",
                "input": "aaaaa",
                "ctx": {"pattern": "^[^a-z]+"},
                "url": "https://errors.pydantic.dev/2.5/v/string_pattern_mismatch",
            },
            "Invalid item message; message should be in all caps",
        ),
    ],
)
def test_match_errors(input, output):
    new_error = match_errors(input)
    assert new_error["msg"] == output


def test_literal_error_pass(vendor_code_error):
    with does_not_raise():
        match_errors(vendor_code_error)


def test_string_error_pass(string_barcode_error):
    with does_not_raise():
        match_errors(string_barcode_error)


def test_extra_field_error_pass(vendor_code_error):
    with does_not_raise():
        extra_errors(vendor_code_error)
