from dataclasses import dataclass
from typing import List, Optional, Union, Dict, Any
from pymarc import Record, Field, Leader


def get_reduced_subfields(
    subfield_dict: Dict[str, List[Any]], code: str
) -> Union[str, List[str], None]:
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
        subfields = field.subfields_as_dict()
        return cls(
            ind1=field.indicator1,
            ind2=field.indicator2,
            call_no=get_reduced_subfields(subfield_dict=subfields, code="h"),
        )


@dataclass
class BibVendorCode:
    ind1: Optional[str]
    ind2: Optional[str]
    vendor_code: Union[str, List[str], None]

    @classmethod
    def from_marc_field(cls, field: Field) -> "BibVendorCode":
        subfields = field.subfields_as_dict()
        return cls(
            ind1=field.indicator1,
            ind2=field.indicator2,
            vendor_code=get_reduced_subfields(subfield_dict=subfields, code="a"),
        )


@dataclass
class LCClass:
    ind1: Optional[str]
    ind2: Optional[str]
    lcc: Union[str, List[str], None]

    @classmethod
    def from_marc_field(cls, field: Field) -> "LCClass":
        subfields = field.subfields_as_dict()
        return cls(
            ind1=field.indicator1,
            ind2=field.indicator2,
            lcc=get_reduced_subfields(subfield_dict=subfields, code="a"),
        )


@dataclass
class LibraryField:
    ind1: Optional[str]
    ind2: Optional[str]
    library: Union[str, List[str], None]

    @classmethod
    def from_marc_field(cls, field: Field) -> "LibraryField":
        subfields = field.subfields_as_dict()
        return cls(
            ind1=field.indicator1,
            ind2=field.indicator2,
            library=get_reduced_subfields(subfield_dict=subfields, code="a"),
        )


@dataclass
class MaterialType:
    material_type: str

    @classmethod
    def from_marc(cls, record: Record) -> "MaterialType":
        field300a = [i.get("a") for i in record.physicaldescription]
        if len(field300a) == 1:
            page_count = int(field300a[0].split()[0])
        else:
            page_count = None
        match record:
            case record.leader if record.leader[6:7] == "am":
                return cls(material_type="monograph_record")
            case record.subjects if "Catalogues Raisonnes" or "Catalogue Raissonne" in [
                s.get_subfields("v") for s in record.subjects
            ]:
                return cls(material_type="catalogue_raissonne")
            case (
                record.physicaldescription
            ) if page_count is not None and page_count < 50:
                return cls(material_type="pamphlet")
            case record.physicaldescription if "volumes" in [
                i.get("300").get("a") for i in record
            ]:
                return cls(material_type="multipart")
            case record.leader if record.leader[19] in ["a", "b", "c"]:
                return cls(material_type="multipart")
            case _:
                return cls(material_type="unknown")


@dataclass
class OrderField:
    ind1: Optional[str]
    ind2: Optional[str]
    order_price: Union[str, List[str], None]
    order_location: Union[str, List[str], None]
    order_fund: Union[str, List[str], None]

    @classmethod
    def from_marc_field(cls, field: Field) -> "OrderField":
        subfields = field.subfields_as_dict()
        return cls(
            ind1=field.indicator1,
            ind2=field.indicator2,
            order_price=get_reduced_subfields(subfield_dict=subfields, code="s"),
            order_location=get_reduced_subfields(subfield_dict=subfields, code="t"),
            order_fund=get_reduced_subfields(subfield_dict=subfields, code="u"),
        )


@dataclass
class InvoiceField:
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
    def from_marc_field(cls, field: Field) -> "InvoiceField":
        subfields = field.subfields_as_dict()
        return cls(
            ind1=field.indicator1,
            ind2=field.indicator2,
            invoice_price=get_reduced_subfields(subfield_dict=subfields, code="b"),
            invoice_date=get_reduced_subfields(subfield_dict=subfields, code="a"),
            invoice_shipping=get_reduced_subfields(subfield_dict=subfields, code="c"),
            invoice_tax=get_reduced_subfields(subfield_dict=subfields, code="d"),
            invoice_number=get_reduced_subfields(subfield_dict=subfields, code="f"),
            invoice_net_price=get_reduced_subfields(subfield_dict=subfields, code="e"),
            invoice_copies=get_reduced_subfields(subfield_dict=subfields, code="g"),
        )


@dataclass
class ItemField:
    ind1: str
    ind2: str
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
    def from_marc_field(cls, field: Field) -> "ItemField":
        subfields = field.subfields_as_dict()
        return cls(
            ind1=field.indicator1,
            ind2=field.indicator2,
            item_call_tag=get_reduced_subfields(subfield_dict=subfields, code="z"),
            item_call_no=get_reduced_subfields(subfield_dict=subfields, code="a"),
            item_barcode=get_reduced_subfields(subfield_dict=subfields, code="i"),
            item_price=get_reduced_subfields(subfield_dict=subfields, code="p"),
            item_vendor_code=get_reduced_subfields(subfield_dict=subfields, code="v"),
            item_agency=get_reduced_subfields(subfield_dict=subfields, code="h"),
            item_location=get_reduced_subfields(subfield_dict=subfields, code="l"),
            item_type=get_reduced_subfields(subfield_dict=subfields, code="t"),
            item_volume=get_reduced_subfields(subfield_dict=subfields, code="c"),
            item_message=get_reduced_subfields(subfield_dict=subfields, code="u"),
            message=get_reduced_subfields(subfield_dict=subfields, code="m"),
        )


@dataclass
class OrderItemData:
    order_loc: Union[str, List[str], None]
    item_loc: Union[str, List[str], None]
    item_type: Union[str, List[str], None]


class VendorRecord(Record):
    def __init__(self, leader: Leader, fields: List[Field]):
        self.leader = leader
        self.fields = fields

        self.bib_call_no = self._bib_call_no_from_marc()
        self.bib_vendor_code = self._bib_vendor_code_from_marc()
        self.invoice_field = self._invoice_from_marc()
        self.item_fields = self._items_from_marc()
        self.lc_class = self._lc_class_from_marc()
        self.library_field = self._library_from_marc()
        self.order_field = self._order_from_marc()
        self.order_item_data = self._get_order_item_list()
        self.material_type = MaterialType.from_marc(self)

    def _bib_call_no_from_marc(
        self,
    ) -> Union[BibCallNo, List[BibCallNo,]]:
        field_list = [i for i in self.fields if i.tag == "852"]
        if len(field_list) == 1:
            return BibCallNo.from_marc_field(field=field_list[0])
        else:
            return [BibCallNo.from_marc_field(field=i) for i in field_list]

    def _bib_vendor_code_from_marc(
        self,
    ) -> Union[BibVendorCode, List[BibVendorCode,]]:
        field_list = [i for i in self.fields if i.tag == "901"]
        if len(field_list) == 1:
            return BibVendorCode.from_marc_field(field=field_list[0])
        else:
            return [BibVendorCode.from_marc_field(field=i) for i in field_list]

    def _lc_class_from_marc(
        self,
    ) -> Union[LCClass, List[LCClass]]:
        field_list = [i for i in self.fields if i.tag == "050"]
        if len(field_list) == 1:
            return LCClass.from_marc_field(field=field_list[0])
        else:
            return [LCClass.from_marc_field(field=i) for i in field_list]

    def _library_from_marc(
        self,
    ) -> Union[LibraryField, List[LibraryField]]:
        field_list = [i for i in self.fields if i.tag == "910"]
        if len(field_list) == 1:
            return LibraryField.from_marc_field(field=field_list[0])
        else:
            return [LibraryField.from_marc_field(field=i) for i in field_list]

    def _items_from_marc(
        self,
    ) -> List[ItemField]:
        field_list = [i for i in self.fields if i.tag == "949"]
        return [ItemField.from_marc_field(field=i) for i in field_list]

    def _order_from_marc(
        self,
    ) -> Union[OrderField, List[OrderField]]:
        field_list = [i for i in self.fields if i.tag == "960"]
        if len(field_list) == 1:
            return OrderField.from_marc_field(field=field_list[0])
        else:
            return [OrderField.from_marc_field(field=i) for i in field_list]

    def _invoice_from_marc(
        self,
    ) -> Union[InvoiceField, List[InvoiceField]]:
        field_list = [i for i in self.fields if i.tag == "980"]
        if len(field_list) == 1:
            return InvoiceField.from_marc_field(field=field_list[0])
        else:
            return [InvoiceField.from_marc_field(field=i) for i in field_list]

    def _get_order_item_list(self) -> List[OrderItemData]:
        order_item_data_list = []
        for item in self.item_fields:
            data_combo = OrderItemData(
                order_loc=self.order_field.order_location,
                item_loc=item.item_location,
                item_type=item.item_type,
            )
            order_item_data_list.append(data_combo)
        return order_item_data_list
