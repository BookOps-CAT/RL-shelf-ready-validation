from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Union
from pymarc import Field


def get_subfield_from_field(field: Field, code: str) -> Union[str, List[str], None]:
    subfield_dict = field.subfields_as_dict()
    subfield_list = subfield_dict.get(code, None)
    if subfield_list is not None and len(subfield_list) == 1:
        return subfield_list[0]
    else:
        return subfield_list


@dataclass
class BibCallNo:
    ind1: Optional[str]
    ind2: Optional[str]
    call_no: Union[str, List[str], None]

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
    ind1: Optional[str]
    ind2: Optional[str]
    vendor_code: Union[str, List[str], None]

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
    ind1: Optional[str]
    ind2: Optional[str]
    lcc: Union[str, List[str], None]

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
    ind1: Optional[str]
    ind2: Optional[str]
    library: Union[str, List[str], None]

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
    ind1: Optional[str]
    ind2: Optional[str]
    order_price: Union[str, List[str], None]
    order_location: Union[str, List[str], None]
    order_fund: Union[str, List[str], None]

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
    ind1: Optional[str]
    ind2: Optional[str]
    invoice_date: Union[str, List[str], None]
    invoice_price: Union[str, List[str], None]
    invoice_shipping: Union[str, List[str], None]
    invoice_tax: Union[str, List[str], None]
    invoice_net_price: Union[str, List[str], None]
    invoice_number: Union[str, List[str], None]
    invoice_copies: Union[str, List[str], None]

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
    ind1: Optional[str]
    ind2: Optional[str]
    item_call_tag: Union[str, List[str], None]
    item_call_no: Union[str, List[str], None]
    item_barcode: Union[str, List[str], None]
    item_price: Union[str, List[str], None]
    item_message: Union[str, List[str], None]
    message: Union[str, List[str], None]
    item_vendor_code: Union[str, List[str], None]
    item_agency: Union[str, List[str], None]
    item_location: Union[str, List[str], None]
    item_volume: Union[str, List[str], None]
    item_type: Union[str, List[str], None]

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


@dataclass
class OrderItemData:
    order_location: Union[str, List[str], None]
    item_location: Union[str, List[str], None]
    item_type: Union[str, List[str], None]

    def filter_none_vals(self) -> Dict:
        return {k: v for k, v in asdict(self).items() if v is not None}
