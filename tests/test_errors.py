import pytest
from pydantic import ValidationError
from src.validate.models import Record
from src.validate.errors import (
    convert_error_messages,
)


def test_get_error_types(string_pattern_mismatch_error):
    assert string_pattern_mismatch_error["type"] == "string_pattern_mismatch"


def test_invalid_error_types(string_pattern_mismatch_error):
    assert string_pattern_mismatch_error["type"] != "literal_error"


def test_pamphlet_errors(invalid_barcode_record):
    try:
        Record(**invalid_barcode_record)
    except ValidationError as e:
        error = convert_error_messages(e)
        assert error["type"] == "string_pattern_mismatch"


# def test_barcode_error(invalid_barcode_record):
#     try:
#         Record(**invalid_barcode_record)
#     except ValidationError as e:
#         new_error = convert_error_messages(e)
#         assert (
#             new_error["msg"]
#             == "Invalid barcode. Barcodes should be 14 digits long and begin with: '33433' for NYPL Research Libraries, '33333' for NYPL Branch Libraries, or '34444' for BPL."
#         )


@pytest.mark.parametrize(
    "key, value",
    [
        (
            "msg",
            "Invalid barcode. Barcodes should be 14 digits long and begin with: '33433' for NYPL Research Libraries, '33333' for NYPL Branch Libraries, or '34444' for BPL.",
        ),
        ("loc", "item_barcode"),
    ],
)
def test_barcode_error(invalid_barcode_record, key, value):
    try:
        Record(**invalid_barcode_record)
    except ValidationError as e:
        new_error = convert_error_messages(e)
        assert new_error[key] == value


@pytest.mark.parametrize(
    "key, value",
    [
        ("item_call_no", "ReCAP 24-0000"),
        ("bib_call_no", "RECAP 23-00000"),
        ("bib_call_no", "ReCAP 11-11111"),
        ("item_call_no", "ReCAP 11-11111"),
    ],
)
def test_call_no_error(valid_bpl_record, key, value):
    valid_bpl_record[key] = value
    try:
        Record(**valid_bpl_record)
    except ValidationError as e:
        new_error = convert_error_messages(e)
        assert (
            new_error["msg"]
            == "ReCAP call numbers should contain a 2-digit year and match the pattern 'ReCAP YY-999999'."
        )
        assert new_error["loc"] == key


@pytest.mark.parametrize(
    "key, value",
    [
        ("invoice_price", "2.00"),
        ("invoice_shipping", "1.11"),
        ("invoice_tax", "22.22"),
        ("invoice_net_price", "12345"),
    ],
)
def test_price_error(valid_bpl_record, key, value):
    valid_bpl_record["invoice"][key] = value
    try:
        Record(**valid_bpl_record)
    except ValidationError as e:
        new_error = convert_error_messages(e)
        assert new_error["msg"] == "Invoice prices should not include decimal points."
        assert new_error["loc"] == key


@pytest.mark.parametrize(
    "key, value",
    [
        ("order_price", "2.00"),
        ("order_price", "1.11"),
    ],
)
def test_order_price_error(valid_bpl_record, key, value):
    valid_bpl_record[key] = value
    try:
        Record(**valid_bpl_record)
    except ValidationError as e:
        new_error = convert_error_messages(e)
        assert new_error["msg"] == "Order prices should not include decimal points."
        assert new_error["loc"] == ("order_price")


@pytest.mark.parametrize(
    "value",
    ["20240101", "01012024", "January 1, 2024"],
)
def test_invoice_date_error(valid_bpl_record, value):
    valid_bpl_record["invoice_date"] = value
    try:
        Record(**valid_bpl_record)
    except ValidationError as e:
        new_error = convert_error_messages(e)
        assert new_error["msg"] == "Invoice dates should match the pattern YYMMDD."
        assert new_error["loc"] == ("invoice_date")


@pytest.mark.parametrize(
    "value",
    ["100", "1", "10", "222"],
)
def test_item_price_error(valid_bpl_record, value):
    valid_bpl_record["item_price"] = value
    try:
        Record(**valid_bpl_record)
    except ValidationError as e:
        new_error = convert_error_messages(e)
        assert new_error["msg"] == "Item prices must include decimal points."
        assert new_error["loc"] == ("item_price")


@pytest.mark.parametrize(
    "key, value",
    [
        ("item_message", "foobar"),
        ("item_message", "lower case message"),
        ("message", "foo"),
        ("message", "bar"),
    ],
)
def test_message_error(valid_bpl_record, key, value):
    valid_bpl_record[key] = value
    try:
        Record(**valid_bpl_record)
    except ValidationError as e:
        new_error = convert_error_messages(e)
        assert new_error["msg"] == "Messages in item records should be all caps."
        assert new_error["loc"] == key


@pytest.mark.parametrize(
    "key, value",
    [
        ("item_vendor_code", "AUX"),
        ("item_vendor_code", "EV"),
        ("bib_vendor_code", "EVIS"),
        ("bib_vendor_code", "Amalivre"),
    ],
)
def test_vendor_code_error(valid_bpl_record, key, value):
    valid_bpl_record[key] = value
    try:
        Record(**valid_bpl_record)
    except ValidationError as e:
        new_error = convert_error_messages(e)
        assert new_error["msg"] == "Invalid vendor code."
        assert new_error["loc"] == key


@pytest.mark.parametrize(
    "value",
    ["rl", "research libraries", "nypl", "NYPL"],
)
def test_RL_identifier_error(valid_bpl_record, value):
    valid_bpl_record["rl_identifier"] = value
    try:
        Record(**valid_bpl_record)
    except ValidationError as e:
        new_error = convert_error_messages(e)
        assert new_error["msg"] == "Invalid research libraries identifier."
        assert new_error["loc"] == "rl_identifier"


@pytest.mark.parametrize(
    "value",
    [100, "1", "10", "222"],
)
def test_call_tag_error(valid_bpl_record, value):
    valid_bpl_record["item"]["item_call_tag"] = value
    try:
        Record(**valid_bpl_record)
    except ValidationError as e:
        new_error = convert_error_messages(e)
        assert new_error["msg"] == "Invalid item call tag. Should be '8528'."
        assert new_error["loc"] == "item_call_tag"


@pytest.mark.parametrize(
    "value",
    ["foo", "bar", "MAL", "item_location", "1"],
)
def test_item_location_error(valid_bpl_record, value):
    valid_bpl_record["item_location"] = value
    try:
        Record(**valid_bpl_record)
    except ValidationError as e:
        new_error = convert_error_messages(e)
        assert new_error["msg"] == "Item location does not match a valid location."
        assert new_error["loc"] == "item_location"


@pytest.mark.parametrize(
    "value",
    ["bbb", "aaa", "10", "222"],
)
def test_order_location_error(valid_bpl_record, value):
    valid_bpl_record["order_location"] = value
    try:
        Record(**valid_bpl_record)
    except ValidationError as e:
        new_error = convert_error_messages(e)
        assert new_error["msg"] == "Order location does not match a valid location."
        assert new_error["loc"] == "order_location"


def test_extra_field_error(invalid_pamphlet_record):
    try:
        Record(**invalid_pamphlet_record)
    except ValidationError as e:
        new_error = convert_error_messages(e)
        assert (
            new_error["msg"]
            == "This bib record should not contain an item record. Check the material type."
        )
        assert new_error["type"] == "extra_forbidden"
