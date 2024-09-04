import pytest
from pydantic import ValidationError
from shelf_ready_validator.translate import MarcError, MarcValidationError
from shelf_ready_validator.marc_models import MonographRecord, OtherRecord


def test_MarcError_string_pattern(mock_monograph_record):
    mock_monograph_record["bib_call_no"]["call_no"] = "ReCAP-24-119100"
    with pytest.raises(ValidationError) as e:
        MonographRecord(**mock_monograph_record)
    error = MarcError(e.value.errors()[0])
    assert len(e.value.errors()) == 1
    assert error.loc == ("bib_call_no", "call_no")
    assert error.input == "ReCAP-24-119100"
    assert isinstance(error.ctx, dict)
    assert error.type == "string_pattern_mismatch"
    assert "String should match pattern " in error.msg
    assert error.loc_marc == "852$h"


def test_MarcError_missing_field(mock_monograph_record):
    del mock_monograph_record["item_fields"][0]["item_agency"]
    with pytest.raises(ValidationError) as e:
        MonographRecord(**mock_monograph_record)
    error = MarcError(e.value.errors()[0])
    assert len(e.value.errors()) == 1
    assert error.loc == ("item_fields", 0, "item_agency")
    assert isinstance(error.input, dict)
    assert error.ctx is None
    assert error.type == "missing"
    assert error.msg == "Field required"
    assert error.loc_marc == "949_1_$h"


def test_MarcError_literal(mock_monograph_record):
    mock_monograph_record["order_field"]["order_location"] = "foo"
    with pytest.raises(ValidationError) as e:
        MonographRecord(**mock_monograph_record)
    error = MarcError(e.value.errors()[0])
    assert len(e.value.errors()) == 1
    assert error.loc == ("order_field", "order_location")
    assert error.input == "foo"
    assert isinstance(error.ctx, dict)
    assert error.type == "literal_error"
    assert "Input should be " in error.msg
    assert error.loc_marc == "960$t"


def test_MarcError_literal_indicator_error(mock_monograph_record):
    mock_monograph_record["order_field"]["ind1"] = "7"
    with pytest.raises(ValidationError) as e:
        MonographRecord(**mock_monograph_record)
    error = MarcError(e.value.errors()[0])
    assert len(e.value.errors()) == 1
    assert error.loc == ("order_field", "ind1")
    assert error.input == "7"
    assert isinstance(error.ctx, dict)
    assert error.type == "literal_error"
    assert "Input should be " in error.msg
    assert error.loc_marc == "960ind1"


def test_MarcError_order_item_mismatch(mock_monograph_record):
    mock_monograph_record["order_field"]["order_location"] = "MAB"
    with pytest.raises(ValidationError) as e:
        MonographRecord(**mock_monograph_record)
    error = MarcError(e.value.errors()[0])
    assert len(e.value.errors()) == 1
    assert error.loc == (
        "order_field",
        "item_location",
        "item_type",
    )
    assert error.input == ("MAB", "rc2ma", "55")
    assert error.ctx is None
    assert error.url is None
    assert error.type == "order_item_mismatch"
    assert (
        "Invalid combination of item type, order location and item location:"
        in error.msg
    )
    assert error.loc_marc == ("960$t", "949_$l", "949_$t")


def test_MarcError_string_type(mock_monograph_record):
    mock_monograph_record["invoice_field"]["invoice_price"] = 1.00
    with pytest.raises(ValidationError) as e:
        MonographRecord(**mock_monograph_record)
    error = MarcError(e.value.errors()[0])
    assert len(e.value.errors()) == 1
    assert error.loc == ("invoice_field", "invoice_price")
    assert isinstance(error.input, float)
    assert error.ctx is None
    assert error.type == "string_type"
    assert error.msg == "Input should be a valid string"
    assert error.loc_marc == "980$b"


def test_MarcError_extra_forbidden(mock_pamphlet_record):
    mock_pamphlet_record["bib_call_no"] = {"call_no": "ReCAP 24-119100"}
    with pytest.raises(ValidationError) as e:
        OtherRecord(**mock_pamphlet_record)
    error = MarcError(e.value.errors()[0])
    assert len(e.value.errors()) == 1
    assert error.loc == ("bib_call_no",)
    assert isinstance(error.input, dict)
    assert error.ctx is None
    assert error.type == "extra_forbidden"
    assert error.msg == "Extra inputs are not permitted"
    assert error.loc_marc == "852"


def test_MarcError_missing_before_validation(mock_monograph_record):
    mock_monograph_record["invoice_field"] = {}
    with pytest.raises(ValidationError) as e:
        MonographRecord(**mock_monograph_record)
    error = MarcError(e.value.errors()[0])
    assert len(e.value.errors()) == 1
    assert error.loc == ("invoice_field",)
    assert isinstance(error.input, dict)
    assert error.ctx is None
    assert error.type == "missing_before_validation"
    assert error.msg == "Field required"
    assert error.loc_marc == "980"


def test_MarcError_model_type(mock_monograph_record):
    mock_monograph_record["invoice_field"] = {"invoice_field"}
    with pytest.raises(ValidationError) as e:
        MonographRecord(**mock_monograph_record)
    error = MarcError(e.value.errors()[0])
    assert len(e.value.errors()) == 1
    assert error.loc == ("invoice_field",)
    assert isinstance(error.input, set)
    assert error.ctx == {"class_name": "InvoiceFieldModel"}
    assert error.type == "model_type"
    assert "Input should be a valid dictionary or instance of " in error.msg
    assert error.loc_marc == "980"


def test_MarcValidationError_extra_fields(mock_monograph_record):
    with pytest.raises(ValidationError) as e:
        OtherRecord(**mock_monograph_record)
    errors = MarcValidationError(e.value.errors())
    assert len(errors.extra_fields) == 2


def test_MarcValidationError_missing_fields(mock_pamphlet_record):
    with pytest.raises(ValidationError) as e:
        MonographRecord(**mock_pamphlet_record)
    errors = MarcValidationError(e.value.errors())
    assert len(errors.missing_fields) == 2


def test_MarcValidationError_monograph_multiple_errors(mock_monograph_record):
    del mock_monograph_record["item_fields"][0]["item_agency"]
    mock_monograph_record["bib_call_no"]["call_no"] = "ReCAP-24-119100"
    mock_monograph_record["order_field"]["order_location"] = "MAG"
    with pytest.raises(ValidationError) as e:
        MonographRecord(**mock_monograph_record)
    errors = MarcValidationError(e.value.errors()).to_dict()
    assert errors["missing_field_count"] == 1
    assert errors["invalid_field_count"] == 1
    assert errors["extra_field_count"] == 0
    assert errors["error_count"] == 2
    assert errors["missing_fields"] == ["949_1_$h"]
    assert errors["invalid_fields"][0]["invalid_field"] == "852$h"
    assert errors["extra_fields"] == []
    assert errors["order_item_mismatches"] == []


def test_MarcValidationError_pamphlet_multiple_errors(mock_pamphlet_record):
    del mock_pamphlet_record["invoice_field"]["invoice_price"]
    mock_pamphlet_record["invoice_field"]["ind1"] = "9"
    mock_pamphlet_record["bib_call_no"] = {"call_no": "ReCAP-24-119100"}
    with pytest.raises(ValidationError) as e:
        OtherRecord(**mock_pamphlet_record)
    errors = MarcValidationError(e.value.errors()).to_dict()
    assert errors["missing_field_count"] == 1
    assert errors["invalid_field_count"] == 1
    assert errors["extra_field_count"] == 1
    assert errors["error_count"] == 3
    assert errors["missing_fields"] == ["980$b"]
    assert errors["invalid_fields"][0]["invalid_field"] == "980ind1"
    assert errors["extra_fields"] == ["852"]
    assert errors["order_item_mismatches"] == []
