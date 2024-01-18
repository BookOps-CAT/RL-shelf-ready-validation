import pytest
from pydantic import ValidationError
from contextlib import nullcontext as does_not_raise
from src.validate.models import Invoice


@pytest.mark.parametrize("invoice_date", ["230101", "240101", "220202"])
def test_invoice_date_valid(invoice_date):
    with does_not_raise():
        Invoice(
            invoice_date=invoice_date,
            invoice_price="123",
            invoice_shipping="1",
            invoice_tax="1",
            invoice_net_price="123",
            invoice_number="12345",
            invoice_copies="1",
        )


@pytest.mark.parametrize(
    "invoice_date",
    ["October 1, 2023", "20231001", "2023-01-01"],
)
def test_invoice_date_invalid(invoice_date):
    with pytest.raises(ValidationError) as e:
        Invoice(
            invoice_date=invoice_date,
            invoice_price="123",
            invoice_shipping="1",
            invoice_tax="1",
            invoice_net_price="123",
            invoice_number="12345",
            invoice_copies="1",
        )
    assert e.value.errors()[0]["type"] == "string_pattern_mismatch"


@pytest.mark.parametrize("invoice_price", ["123", "1234", "222222"])
def test_invoice_price_valid(invoice_price):
    with does_not_raise():
        Invoice(
            invoice_date="230101",
            invoice_price=invoice_price,
            invoice_shipping="1",
            invoice_tax="1",
            invoice_net_price="123",
            invoice_number="12345",
            invoice_copies="1",
        )


@pytest.mark.parametrize(
    "invoice_price, error_type",
    [
        (1.00, "string_type"),
        (12, "string_type"),
        (None, "string_type"),
        ([123, 123.45], "string_type"),
        ("1.00", "string_pattern_mismatch"),
    ],
)
def test_invoice_price_invalid(invoice_price, error_type):
    with pytest.raises(ValidationError) as e:
        Invoice(
            invoice_date="230101",
            invoice_price=invoice_price,
            invoice_shipping="1",
            invoice_tax="1",
            invoice_net_price="123",
            invoice_number="12345",
            invoice_copies="1",
        )
    assert e.value.errors()[0]["type"] == error_type


@pytest.mark.parametrize("invoice_shipping", ["123", "1234", "222222"])
def test_invoice_shipping_valid(invoice_shipping):
    with does_not_raise():
        Invoice(
            invoice_date="230101",
            invoice_price="123",
            invoice_shipping=invoice_shipping,
            invoice_tax="1",
            invoice_net_price="123",
            invoice_number="12345",
            invoice_copies="1",
        )


@pytest.mark.parametrize(
    "invoice_shipping, error_type",
    [
        (1.00, "string_type"),
        (12, "string_type"),
        (None, "string_type"),
        ([123, 123.45], "string_type"),
        ("1.00", "string_pattern_mismatch"),
    ],
)
def test_invoice_shipping_invalid(invoice_shipping, error_type):
    with pytest.raises(ValidationError) as e:
        Invoice(
            invoice_date="230101",
            invoice_price="123",
            invoice_shipping=invoice_shipping,
            invoice_tax="1",
            invoice_net_price="123",
            invoice_number="12345",
            invoice_copies="1",
        )
    assert e.value.errors()[0]["type"] == error_type


@pytest.mark.parametrize("invoice_tax", ["123", "1234", "222222"])
def test_invoice_tax_valid(invoice_tax):
    with does_not_raise():
        Invoice(
            invoice_date="230101",
            invoice_price="123",
            invoice_shipping="1",
            invoice_tax=invoice_tax,
            invoice_net_price="123",
            invoice_number="12345",
            invoice_copies="1",
        )


@pytest.mark.parametrize(
    "invoice_tax, error_type",
    [
        (1.00, "string_type"),
        (12, "string_type"),
        (None, "string_type"),
        ([123, 123.45], "string_type"),
        ("1.00", "string_pattern_mismatch"),
    ],
)
def test_invoice_tax_invalid(invoice_tax, error_type):
    with pytest.raises(ValidationError) as e:
        Invoice(
            invoice_date="230101",
            invoice_price="123",
            invoice_shipping="1",
            invoice_tax=invoice_tax,
            invoice_net_price="123",
            invoice_number="12345",
            invoice_copies="1",
        )
    assert e.value.errors()[0]["type"] == error_type


@pytest.mark.parametrize("invoice_net_price", ["123", "1234", "222222"])
def test_invoice_net_price_valid(invoice_net_price):
    with does_not_raise():
        Invoice(
            invoice_date="230101",
            invoice_price="123",
            invoice_shipping="1",
            invoice_tax="1",
            invoice_net_price=invoice_net_price,
            invoice_number="12345",
            invoice_copies="1",
        )


@pytest.mark.parametrize(
    "invoice_net_price, error_type",
    [
        (1.00, "string_type"),
        (12, "string_type"),
        (None, "string_type"),
        ([123, 123.45], "string_type"),
        ("1.00", "string_pattern_mismatch"),
    ],
)
def test_invoice_net_price_invalid(invoice_net_price, error_type):
    with pytest.raises(ValidationError) as e:
        Invoice(
            invoice_date="230101",
            invoice_price="123",
            invoice_shipping="1",
            invoice_tax="1",
            invoice_net_price=invoice_net_price,
            invoice_number="12345",
            invoice_copies="1",
        )
    assert e.value.errors()[0]["type"] == error_type


@pytest.mark.parametrize("invoice_number", ["12345", "11111", "22222"])
def test_invoice_number_valid(invoice_number):
    with does_not_raise():
        Invoice(
            invoice_date="230101",
            invoice_price="123",
            invoice_shipping="1",
            invoice_tax="1",
            invoice_net_price="123",
            invoice_number=invoice_number,
            invoice_copies="1",
        )


@pytest.mark.parametrize(
    "invoice_number",
    [1, 12, None, ["1", "2"], {"invoice_number": "231001"}],
)
def test_invoice_number_invalid(invoice_number):
    with pytest.raises(ValidationError) as e:
        Invoice(
            invoice_date="230101",
            invoice_price="123",
            invoice_shipping="1",
            invoice_tax="1",
            invoice_net_price="123",
            invoice_number=invoice_number,
            invoice_copies="1",
        )
    assert e.value.errors()[0]["type"] == "string_type"


@pytest.mark.parametrize("invoice_copies", ["1", "2", "12"])
def test_invoice_copies_valid(invoice_copies):
    with does_not_raise():
        Invoice(
            invoice_date="230101",
            invoice_price="123",
            invoice_shipping="1",
            invoice_tax="1",
            invoice_net_price="123",
            invoice_number="12345",
            invoice_copies=invoice_copies,
        )


@pytest.mark.parametrize(
    "invoice_copies, error_type",
    [
        (1.00, "string_type"),
        (12, "string_type"),
        (None, "string_type"),
        ("foo", "string_pattern_mismatch"),
    ],
)
def test_invoice_copies_invalid(invoice_copies, error_type):
    with pytest.raises(ValidationError) as e:
        Invoice(
            invoice_date="230101",
            invoice_price="123",
            invoice_shipping="1",
            invoice_tax="1",
            invoice_net_price="123",
            invoice_number="123455",
            invoice_copies=invoice_copies,
        )
    assert e.value.errors()[0]["type"] == error_type
