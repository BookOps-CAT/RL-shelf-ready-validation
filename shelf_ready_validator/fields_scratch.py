"""
This module contains dataclasses used to model required fields in vendor-provided
MARC records.

Most of the dataclasses in this module have a class method called `from_marc_field`
which is used to instantiate the dataclass from a pymarc Field object. The dataclasses
also have a method called `filter_none_vals` which returns a dictionary of the dataclass
attributes with None values removed.
"""

from collections import defaultdict
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Union, DefaultDict
from pymarc import Field


def get_subfield_from_field(
    field: Union[dict, Field], code: str
) -> Optional[Union[str, List[str]]]:
    """A helper function to extract a subfield as a str from a pymarc Field object."""
    if isinstance(field, dict):
        subfield_dict: Union[dict, DefaultDict] = defaultdict(list)
        subfields = field.get("subfields", [])
        if subfields == []:
            return None
        for subfield in subfields:
            for key, value in subfield.items():
                subfield_dict[key].append(value)
    else:
        subfield_dict = field.subfields_as_dict()
    subfield_list = subfield_dict.get(code, None)
    if subfield_list is not None and len(subfield_list) == 1:
        return subfield_list[0]
    else:
        return subfield_list


class BibCallNo:
    """A dataclass to model the 852 field in a vendor-provided MARC record."""

    def __init__(
        self,
        ind1: Optional[str] = None,
        ind2: Optional[str] = None,
        call_no: Optional[Union[str, List[str]]] = None,
        field: Optional[Union[dict, Field]] = None,
    ):
        self.ind1 = ind1
        self.ind2 = ind2
        self.call_no = call_no

        if all(i is None for i in [ind1, ind2, call_no]) and isinstance(field, Field):
            self.ind1 = field.indicator1
            self.ind2 = field.indicator2
            self.call_no = get_subfield_from_field(field=field, code="h")
        elif all(i is None for i in [ind1, ind2, call_no]) and isinstance(field, dict):
            self.ind1 = field["ind1"]
            self.ind2 = field["ind2"]
            self.call_no = get_subfield_from_field(field=field, code="h")

    # @classmethod
    # def from_field(cls, field: Union[dict, Field]) -> "BibCallNo":
    #     call_no = get_subfield_from_field(field=field, code="h")
    #     if isinstance(field, Field):
    #         return cls(
    #             ind1=field.indicator1,
    #             ind2=field.indicator2,
    #             call_no=call_no,
    #         )
    #     elif isinstance(field, dict):
    #         return cls(
    #             ind1=field["ind1"],
    #             ind2=field["ind2"],
    #             call_no=call_no,
    #         )
    #     else:
    #         raise ValueError("Field must be a dict or pymarc Field object.")

    # def filter_none_vals(self) -> Dict:
    #     return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class BibVendorCode:
    """A dataclass to model the 901 field in a vendor-provided MARC record."""

    ind1: Optional[str]
    ind2: Optional[str]
    vendor_code: Optional[Union[str, List[str]]]

    @classmethod
    def from_field(cls, field: Union[dict, Field]) -> "BibVendorCode":
        vendor_code = get_subfield_from_field(field=field, code="a")
        if isinstance(field, Field):
            return cls(
                ind1=field.indicator1,
                ind2=field.indicator2,
                vendor_code=vendor_code,
            )
        elif isinstance(field, dict):
            return cls(
                ind1=field["ind1"],
                ind2=field["ind2"],
                vendor_code=vendor_code,
            )
        else:
            raise ValueError("Field must be a dict or pymarc Field object.")

    def filter_none_vals(self) -> Dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class LCClass:
    """A dataclass to model the 050 field in a vendor-provided MARC record."""

    ind1: Optional[str]
    ind2: Optional[str]
    lcc: Optional[Union[str, List[str]]]

    @classmethod
    def from_field(cls, field: Union[dict, Field]) -> "LCClass":
        lcc = get_subfield_from_field(field=field, code="a")
        if isinstance(field, Field):
            return cls(
                ind1=field.indicator1,
                ind2=field.indicator2,
                lcc=lcc,
            )
        elif isinstance(field, dict):
            return cls(
                ind1=field["ind1"],
                ind2=field["ind2"],
                lcc=lcc,
            )
        else:
            raise ValueError("Field must be a dict or pymarc Field object.")

    def filter_none_vals(self) -> Dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class Library:
    """A dataclass to model the 910 field in a vendor-provided MARC record."""

    ind1: Optional[str]
    ind2: Optional[str]
    library: Optional[Union[str, List[str]]]

    @classmethod
    def from_field(cls, field: Union[dict, Field]) -> "Library":
        library = get_subfield_from_field(field=field, code="a")
        if isinstance(field, Field):
            return cls(
                ind1=field.indicator1,
                ind2=field.indicator2,
                library=library,
            )
        elif isinstance(field, dict):
            return cls(
                ind1=field["ind1"],
                ind2=field["ind2"],
                library=library,
            )
        else:
            raise ValueError("Field must be a dict or pymarc Field object.")

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
    def from_field(cls, field: Union[dict, Field]) -> "Order":
        order_price = get_subfield_from_field(field=field, code="s")
        order_location = get_subfield_from_field(field=field, code="t")
        order_fund = get_subfield_from_field(field=field, code="u")
        if isinstance(field, Field):
            return cls(
                ind1=field.indicator1,
                ind2=field.indicator2,
                order_price=order_price,
                order_location=order_location,
                order_fund=order_fund,
            )
        elif isinstance(field, dict):
            return cls(
                ind1=field["ind1"],
                ind2=field["ind2"],
                order_price=order_price,
                order_location=order_location,
                order_fund=order_fund,
            )
        else:
            raise ValueError("Field must be a dict or pymarc Field object.")

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
    def from_field(cls, field: Union[dict, Field]) -> "Invoice":
        invoice_date = get_subfield_from_field(field=field, code="a")
        invoice_price = get_subfield_from_field(field=field, code="b")
        invoice_shipping = get_subfield_from_field(field=field, code="c")
        invoice_tax = get_subfield_from_field(field=field, code="d")
        invoice_net_price = get_subfield_from_field(field=field, code="e")
        invoice_number = get_subfield_from_field(field=field, code="f")
        invoice_copies = get_subfield_from_field(field=field, code="g")
        if isinstance(field, Field):
            return cls(
                ind1=field.indicator1,
                ind2=field.indicator2,
                invoice_date=invoice_date,
                invoice_price=invoice_price,
                invoice_shipping=invoice_shipping,
                invoice_tax=invoice_tax,
                invoice_net_price=invoice_net_price,
                invoice_number=invoice_number,
                invoice_copies=invoice_copies,
            )
        elif isinstance(field, dict):
            return cls(
                ind1=field["ind1"],
                ind2=field["ind2"],
                invoice_date=invoice_date,
                invoice_price=invoice_price,
                invoice_shipping=invoice_shipping,
                invoice_tax=invoice_tax,
                invoice_net_price=invoice_net_price,
                invoice_number=invoice_number,
                invoice_copies=invoice_copies,
            )
        else:
            raise ValueError("Field must be a dict or pymarc Field object.")

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
    def from_field(cls, field: Union[dict, Field]) -> "Item":
        item_call_tag = get_subfield_from_field(field=field, code="z")
        item_call_no = get_subfield_from_field(field=field, code="a")
        item_barcode = get_subfield_from_field(field=field, code="i")
        item_price = get_subfield_from_field(field=field, code="p")
        item_vendor_code = get_subfield_from_field(field=field, code="v")
        item_agency = get_subfield_from_field(field=field, code="h")
        item_location = get_subfield_from_field(field=field, code="l")
        item_type = get_subfield_from_field(field=field, code="t")
        item_volume = get_subfield_from_field(field=field, code="c")
        item_message = get_subfield_from_field(field=field, code="u")
        message = get_subfield_from_field(field=field, code="m")
        if isinstance(field, dict):
            return cls(
                ind1=field["ind1"],
                ind2=field["ind2"],
                item_call_tag=item_call_tag,
                item_call_no=item_call_no,
                item_barcode=item_barcode,
                item_price=item_price,
                item_vendor_code=item_vendor_code,
                item_agency=item_agency,
                item_location=item_location,
                item_type=item_type,
                item_volume=item_volume,
                item_message=item_message,
                message=message,
            )
        elif isinstance(field, Field):
            return cls(
                ind1=field.indicator1,
                ind2=field.indicator2,
                item_call_tag=item_call_tag,
                item_call_no=item_call_no,
                item_barcode=item_barcode,
                item_price=item_price,
                item_vendor_code=item_vendor_code,
                item_agency=item_agency,
                item_location=item_location,
                item_type=item_type,
                item_volume=item_volume,
                item_message=item_message,
                message=message,
            )
        else:
            raise ValueError("Field must be a dict or pymarc Field object.")

    def filter_none_vals(self) -> Dict:
        return {k: v for k, v in asdict(self).items() if v is not None}
