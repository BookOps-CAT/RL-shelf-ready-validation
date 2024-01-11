import pytest
from pydantic import ValidationError
from contextlib import nullcontext
from rl_sr_validation.models import Invoice


@pytest.mark.parametrize("invoice_date", ["230101", "240101", "220202"])
def test_invoice_date_valid(invoice_date):
    with nullcontext():
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
    [1.00, 12, None, [231001, "October 1, 2023", {"date": "231001"}]],
)
def test_invoice_date_invalid(invoice_date):
    with pytest.raises(ValidationError):
        Invoice(
            invoice_date=invoice_date,
            invoice_price="123",
            invoice_shipping="1",
            invoice_tax="1",
            invoice_net_price="123",
            invoice_number="12345",
            invoice_copies="1",
        )


@pytest.mark.parametrize("invoice_price", ["123", "1234", "222222"])
def test_invoice_price_valid(invoice_price):
    with nullcontext():
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
    "invoice_price",
    [1.00, 12, None, [123, 123.45]],
)
def test_invoice_price_invalid(invoice_price):
    with pytest.raises(ValidationError):
        Invoice(
            invoice_date="230101",
            invoice_price=invoice_price,
            invoice_shipping="1",
            invoice_tax="1",
            invoice_net_price="123",
            invoice_number="12345",
            invoice_copies="1",
        )


@pytest.mark.parametrize("invoice_shipping", ["123", "1234", "222222"])
def test_invoice_shipping_valid(invoice_shipping):
    with nullcontext():
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
    "invoice_shipping",
    [1.00, 12, None, [123, 123.45]],
)
def test_invoice_shipping_invalid(invoice_shipping):
    with pytest.raises(ValidationError):
        Invoice(
            invoice_date="230101",
            invoice_price="123",
            invoice_shipping=invoice_shipping,
            invoice_tax="1",
            invoice_net_price="123",
            invoice_number="12345",
            invoice_copies="1",
        )


@pytest.mark.parametrize("invoice_tax", ["123", "1234", "222222"])
def test_invoice_tax_valid(invoice_tax):
    with nullcontext():
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
    "invoice_tax",
    [1.00, 12, None, [123, 123.45]],
)
def test_invoice_tax_invalid(invoice_tax):
    with pytest.raises(ValidationError):
        Invoice(
            invoice_date="230101",
            invoice_price="123",
            invoice_shipping="1",
            invoice_tax=invoice_tax,
            invoice_net_price="123",
            invoice_number="12345",
            invoice_copies="1",
        )


@pytest.mark.parametrize("invoice_net_price", ["123", "1234", "222222"])
def test_invoice_net_price_valid(invoice_net_price):
    with nullcontext():
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
    "invoice_net_price",
    [1.00, 12, None, [123, 123.45]],
)
def test_invoice_net_price_invalid(invoice_net_price):
    with pytest.raises(ValidationError):
        Invoice(
            invoice_date="230101",
            invoice_price="123",
            invoice_shipping="1",
            invoice_tax="1",
            invoice_net_price=invoice_net_price,
            invoice_number="12345",
            invoice_copies="1",
        )


@pytest.mark.parametrize("invoice_number", ["12345", "11111", "22222"])
def test_invoice_number_valid(invoice_number):
    with nullcontext():
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
    with pytest.raises(ValidationError):
        Invoice(
            invoice_date="230101",
            invoice_price="123",
            invoice_shipping="1",
            invoice_tax="1",
            invoice_net_price="123",
            invoice_number=invoice_number,
            invoice_copies="1",
        )


@pytest.mark.parametrize("invoice_copies", ["1", "2", "12"])
def test_invoice_copies_valid(invoice_copies):
    with nullcontext():
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
    "invoice_copies",
    [1.00, 12, None, "foo"],
)
def test_invoice_copies_invalid(invoice_copies):
    with pytest.raises(ValidationError):
        Invoice(
            invoice_date="230101",
            invoice_price="123",
            invoice_shipping="1",
            invoice_tax="1",
            invoice_net_price="123",
            invoice_number="123455",
            invoice_copies=invoice_copies,
        )
