import pytest
from pydantic import ValidationError
from contextlib import nullcontext as does_not_raise
from src.validate.models import Order


@pytest.mark.parametrize("order_price", ["123", "1234", "12345"])
def test_order_price_valid(order_price):
    with does_not_raise():
        Order(order_location="MAB", order_fund="99999apprv", order_price=order_price)


@pytest.mark.parametrize("order_price", ["1.00", "12.00", "123.00"])
def test_order_price_invalid(order_price):
    with pytest.raises(ValidationError) as e:
        Order(order_location="MAB", order_fund="99999apprv", order_price=order_price)
    assert e.value.errors()[0]["type"] == "string_pattern_mismatch"


@pytest.mark.parametrize(
    "order_location",
    ["MAB", "MAF", "MAG", "MAL", "MAP", "MAS", "PAD", "PAH", "PAM", "PAT", "SC"],
)
def test_order_location_valid(order_location):
    with does_not_raise():
        Order(order_location=order_location, order_fund="99999apprv", order_price="123")


@pytest.mark.parametrize("order_location", [123, "ZZZ", "MALMALMAL", 123.45, None])
def test_order_location_invalid(order_location):
    with pytest.raises(ValidationError) as e:
        Order(order_location=order_location, order_fund="99999apprv", order_price="123")
    assert e.value.errors()[0]["type"] == "literal_error"


@pytest.mark.parametrize("order_fund", ["12345apprv", "99999apprv", "foobar"])
def test_order_fund_valid(order_fund):
    with does_not_raise():
        Order(order_location="MAB", order_fund=order_fund, order_price="123")


@pytest.mark.parametrize(
    "order_fund", [1.00, 12, None, ["12345apprv", "99999apprv", {"fund": "12345apprv"}]]
)
def test_order_fund_invalid(order_fund):
    with pytest.raises(ValidationError) as e:
        Order(order_location="MAB", order_fund=order_fund, order_price="123")
    assert e.value.errors()[0]["type"] == "string_type"
