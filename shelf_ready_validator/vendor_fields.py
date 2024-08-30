"""
This module contains dataclasses used to model required fields in vendor-provided
MARC records.

Most of the dataclasses in this module have a class method called `from_marc_field`
which is used to instantiate the dataclass from a pymarc Field object. The dataclasses
also have a method called `filter_none_vals` which returns a dictionary of the dataclass
attributes with None values removed.
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Union
from pymarc import Field


def get_subfield_from_field(field: Field, code: str) -> Optional[Union[str, List[str]]]:
    """A helper function to extract a subfield as a str from a pymarc Field object."""
    subfield_dict = field.subfields_as_dict()
    subfield_list = subfield_dict.get(code, None)
    if subfield_list is not None and len(subfield_list) == 1:
        return subfield_list[0]
    else:
        return subfield_list


@dataclass
class BibCallNo:
    """A dataclass to model the 852 field in a vendor-provided MARC record."""

    ind1: Optional[str]
    ind2: Optional[str]
    call_no: Optional[Union[str, List[str]]]

    @classmethod
    def from_marc_field(cls, field: Field) -> "BibCallNo":
        return cls(
            ind1=field.indicator1,
            ind2=field.indicator2,
            call_no=get_subfield_from_field(field=field, code="h"),
        )

    def filter_none_vals(self) -> Dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class BibVendorCode:
    """A dataclass to model the 901 field in a vendor-provided MARC record."""

    ind1: Optional[str]
    ind2: Optional[str]
    vendor_code: Optional[Union[str, List[str]]]

    @classmethod
    def from_marc_field(cls, field: Field) -> "BibVendorCode":
        return cls(
            ind1=field.indicator1,
            ind2=field.indicator2,
            vendor_code=get_subfield_from_field(field=field, code="a"),
        )

    def filter_none_vals(self) -> Dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class LCClass:
    """A dataclass to model the 050 field in a vendor-provided MARC record."""

    ind1: Optional[str]
    ind2: Optional[str]
    lcc: Optional[Union[str, List[str]]]

    @classmethod
    def from_marc_field(cls, field: Field) -> "LCClass":
        return cls(
            ind1=field.indicator1,
            ind2=field.indicator2,
            lcc=get_subfield_from_field(field=field, code="a"),
        )

    def filter_none_vals(self) -> Dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class Library:
    """A dataclass to model the 910 field in a vendor-provided MARC record."""

    ind1: Optional[str]
    ind2: Optional[str]
    library: Optional[Union[str, List[str]]]

    @classmethod
    def from_marc_field(cls, field: Field) -> "Library":
        return cls(
            ind1=field.indicator1,
            ind2=field.indicator2,
            library=get_subfield_from_field(field=field, code="a"),
        )

    def filter_none_vals(self) -> Dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class Order:
    """A dataclass to model the 960 field in a vendor-provided MARC record."""

    ind1: Optional[str]
    ind2: Optional[str]
    order_price: Optional[Union[str, List[str]]]
    order_location: Optional[Union[str, List[str]]]
    order_fund: Optional[Union[str, List[str]]]

    @classmethod
    def from_marc_field(cls, field: Field) -> "Order":
        return cls(
            ind1=field.indicator1,
            ind2=field.indicator2,
            order_price=get_subfield_from_field(field=field, code="s"),
            order_location=get_subfield_from_field(field=field, code="t"),
            order_fund=get_subfield_from_field(field=field, code="u"),
        )

    def filter_none_vals(self) -> Dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class Invoice:
    """A dataclass to model the 980 field in a vendor-provided MARC record."""

    ind1: Optional[str]
    ind2: Optional[str]
    invoice_date: Optional[Union[str, List[str]]]
    invoice_price: Optional[Union[str, List[str]]]
    invoice_shipping: Optional[Union[str, List[str]]]
    invoice_tax: Optional[Union[str, List[str]]]
    invoice_net_price: Optional[Union[str, List[str]]]
    invoice_number: Optional[Union[str, List[str]]]
    invoice_copies: Optional[Union[str, List[str]]]

    @classmethod
    def from_marc_field(cls, field: Field) -> "Invoice":
        return cls(
            ind1=field.indicator1,
            ind2=field.indicator2,
            invoice_date=get_subfield_from_field(field=field, code="a"),
            invoice_price=get_subfield_from_field(field=field, code="b"),
            invoice_shipping=get_subfield_from_field(field=field, code="c"),
            invoice_tax=get_subfield_from_field(field=field, code="d"),
            invoice_number=get_subfield_from_field(field=field, code="f"),
            invoice_net_price=get_subfield_from_field(field=field, code="e"),
            invoice_copies=get_subfield_from_field(field=field, code="g"),
        )

    def filter_none_vals(self) -> Dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class Item:
    """A dataclass to model the 949 field in a vendor-provided MARC record."""

    ind1: Optional[str]
    ind2: Optional[str]
    item_call_tag: Optional[Union[str, List[str]]]
    item_call_no: Optional[Union[str, List[str]]]
    item_barcode: Optional[Union[str, List[str]]]
    item_price: Optional[Union[str, List[str]]]
    item_message: Optional[Union[str, List[str]]]
    message: Optional[Union[str, List[str]]]
    item_vendor_code: Optional[Union[str, List[str]]]
    item_agency: Optional[Union[str, List[str]]]
    item_location: Optional[Union[str, List[str]]]
    item_volume: Optional[Union[str, List[str]]]
    item_type: Optional[Union[str, List[str]]]

    @classmethod
    def from_marc_field(cls, field: Field) -> "Item":
        return cls(
            ind1=field.indicator1,
            ind2=field.indicator2,
            item_call_tag=get_subfield_from_field(field=field, code="z"),
            item_call_no=get_subfield_from_field(field=field, code="a"),
            item_barcode=get_subfield_from_field(field=field, code="i"),
            item_price=get_subfield_from_field(field=field, code="p"),
            item_vendor_code=get_subfield_from_field(field=field, code="v"),
            item_agency=get_subfield_from_field(field=field, code="h"),
            item_location=get_subfield_from_field(field=field, code="l"),
            item_type=get_subfield_from_field(field=field, code="t"),
            item_volume=get_subfield_from_field(field=field, code="c"),
            item_message=get_subfield_from_field(field=field, code="u"),
            message=get_subfield_from_field(field=field, code="m"),
        )

    def filter_none_vals(self) -> Dict:
        return {k: v for k, v in asdict(self).items() if v is not None}
