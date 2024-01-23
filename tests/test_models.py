import pytest
from pydantic import ValidationError
from contextlib import nullcontext as does_not_raise
from src.models import MonographRecord, OtherMaterialRecord


def test_monograph_record_valid(valid_rl_monograph_record):
    with does_not_raise():
        MonographRecord(**valid_rl_monograph_record)


def test_pamphlet_record_valid(valid_pamphlet_record):
    with does_not_raise():
        OtherMaterialRecord(**valid_pamphlet_record)


def test_monograph_record_invalid(valid_rl_monograph_record):
    del valid_rl_monograph_record["bib_call_no"]
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    assert e.value.errors()[0]["type"] == "missing"


def test_pamphlet_record_invalid(valid_pamphlet_record):
    del valid_pamphlet_record["bib_vendor_code"]
    with pytest.raises(ValidationError) as e:
        OtherMaterialRecord(**valid_pamphlet_record)
    assert e.value.errors()[0]["type"] == "missing"


def test_monograph_location_combo_invalid(valid_rl_monograph_record):
    valid_rl_monograph_record["order_location"] = "MAL"
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    assert e.value.errors()[0]["type"] == "Item/Order location check"


def test_monograph_location_missing_invalid(valid_rl_monograph_record):
    del valid_rl_monograph_record["order_location"]
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    assert e.value.errors()[0]["type"] == "missing"


def test_monograph_empty_items(valid_rl_monograph_record):
    del valid_rl_monograph_record["items"]
    with pytest.raises(ValidationError) as e:
        MonographRecord(**valid_rl_monograph_record)
    assert e.value.errors()[0]["type"] == "missing"
