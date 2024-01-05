import pytest
from pydantic import ValidationError
from contextlib import nullcontext
from rl_sr_validation.models import Order


@pytest.mark.parametrize("order_price", ["123", "1234", "12345"])
def test_order_price_valid(order_price):
    with nullcontext():
        Order(order_location="MAB", order_fund="99999apprv", order_price=order_price)


@pytest.mark.parametrize("order_price", ["1.00", "12.00", "123.00", 123.45, None])
def test_order_price_invalid(order_price):
    with pytest.raises(ValidationError):
        Order(order_location="MAB", order_fund="99999apprv", order_price=order_price)
