from typing import Any, List, Dict, Optional, Union
from pymarc import Record, Field, Leader
from shelf_ready_validator.vendor_fields import (
    BibCallNo,
    BibVendorCode,
    Invoice,
    Item,
    LCClass,
    Library,
    Order,
)


class VendorRecord(Record):
    def __init__(self, leader: Leader, fields: List[Field]):
        self.leader = leader
        self.fields = fields
        self.__bib_call_no: Union[BibCallNo, List[BibCallNo]] = self._field_from_marc(
            "852"
        )
        self.__bib_vendor_code: Union[BibVendorCode, List[BibVendorCode]] = (
            self._field_from_marc("901")
        )
        self.__invoice_field: Union[Invoice, List[Invoice]] = self._field_from_marc(
            "980"
        )
        self.__item_fields: List[Item] = self._field_from_marc("949")
        self.__lc_class: Union[LCClass, List[LCClass]] = self._field_from_marc("050")
        self.__library_field: Union[Library, List[Library]] = self._field_from_marc(
            "910"
        )
        self.__order_field: Union[Order, List[Order]] = self._field_from_marc("960")
        self.material_type: str = self._get_material_type()

    def _field_from_marc(self, tag: str) -> Any:
        field_list = [i for i in self.fields if i.tag == tag]
        match (tag, len(field_list)):
            case ("852", 0):
                return BibCallNo(ind1=None, ind2=None, call_no=None)
            case ("852", 1):
                return BibCallNo.from_field(field=field_list[0])
            case ("852", _):
                return [BibCallNo.from_field(field=i) for i in field_list]
            case ("901", 0):
                return BibVendorCode(ind1=None, ind2=None, vendor_code=None)
            case ("901", 1):
                return BibVendorCode.from_field(field=field_list[0])
            case ("901", _):
                return [BibVendorCode.from_field(field=i) for i in field_list]
            case ("050", 0):
                return LCClass(ind1=None, ind2=None, lcc=None)
            case ("050", 1):
                return LCClass.from_field(field=field_list[0])
            case ("050", _):
                return [LCClass.from_field(field=i) for i in field_list]
            case ("910", 0):
                return Library(ind1=None, ind2=None, library=None)
            case ("910", 1):
                return Library.from_field(field=field_list[0])
            case ("910", _):
                return [Library.from_field(field=i) for i in field_list]
            case ("949", 0):
                return [
                    Item(
                        ind1=None,
                        ind2=None,
                        item_call_tag=None,
                        item_call_no=None,
                        item_barcode=None,
                        item_price=None,
                        item_vendor_code=None,
                        item_agency=None,
                        item_message=None,
                        item_location=None,
                        item_type=None,
                        item_volume=None,
                        message=None,
                    )
                ]
            case ("949", _):
                return [Item.from_field(field=i) for i in field_list]
            case ("960", 0):
                return Order(
                    ind1=None,
                    ind2=None,
                    order_location=None,
                    order_fund=None,
                    order_price=None,
                )
            case ("960", 1):
                return Order.from_field(field=field_list[0])
            case ("960", _):
                return [Order.from_field(field=i) for i in field_list]
            case ("980", 0):
                return Invoice(
                    ind1=None,
                    ind2=None,
                    invoice_date=None,
                    invoice_price=None,
                    invoice_shipping=None,
                    invoice_tax=None,
                    invoice_net_price=None,
                    invoice_number=None,
                    invoice_copies=None,
                )
            case ("980", 1):
                return Invoice.from_field(field=field_list[0])
            case ("980", _):
                return [Invoice.from_field(field=i) for i in field_list]
            case _:
                return None

    def _get_material_type(self) -> str:
        subjects = [i for i in self.subjects if self.subjects is not None]
        subjects_subfield_v = [i.get("v") for i in subjects if i.get("v") is not None]
        field300a = [
            i.get("a")
            for i in self.physicaldescription
            if self.physicaldescription is not None
        ]
        field300a_str = "".join(field300a)
        if (
            isinstance(self.__order_field, Order)
            and self.__order_field.order_location is not None
            and "PAD" in self.__order_field.order_location
        ):
            return "dance"
        elif isinstance(self.__order_field, list) and "PAD" in [
            i.order_location for i in self.__order_field if i.order_location is not None
        ]:
            return "dance"
        elif (
            "Catalogues Raisonnes" in subjects_subfield_v
            or "Catalogue Raisonne" in subjects_subfield_v
        ):
            return "catalogue_raissonne"
        elif "volumes" in field300a_str:
            return "multipart"
        elif ("pages" in field300a_str and field300a_str.split()[0].isdigit()) and int(
            field300a_str.split()[0]
        ) < 50:
            return "pamphlet"
        elif self.leader[6:8] == "am":
            return "monograph"

        else:
            return "unknown"

    def to_dict(self) -> Dict[str, Any]:
        record: Dict = {
            "leader": str(self.leader),
            "fields": [],
        }
        for field in self:
            if field.is_control_field():
                record["fields"].append({field.tag: field.data})
            else:
                record["fields"].append(
                    {
                        field.tag: {
                            "ind1": field.indicator1,
                            "ind2": field.indicator2,
                            "subfields": [{s.code: s.value} for s in field.subfields],
                        }
                    }
                )
        record["bib_call_no"] = self.__bib_call_no
        record["bib_vendor_code"] = self.__bib_vendor_code
        record["lc_class"] = self.__lc_class
        record["library_field"] = self.__library_field
        record["order_field"] = self.__order_field
        record["invoice_field"] = self.__invoice_field
        record["item_fields"] = self.__item_fields
        record["material_type"] = self.material_type
        return record

    def pydantic_dict_input(self) -> Dict[str, Any]:
        record: Dict = {
            "leader": str(self.leader),
            "fields": [],
        }
        for field in self:
            if field.is_control_field():
                record["fields"].append({field.tag: field.data})
            else:
                record["fields"].append(
                    {
                        field.tag: {
                            "ind1": field.indicator1,
                            "ind2": field.indicator2,
                            "subfields": [{s.code: s.value} for s in field.subfields],
                        }
                    }
                )
        if isinstance(self.__bib_call_no, list):
            record["bib_call_no"] = [i.filter_none_vals() for i in self.__bib_call_no]
        else:
            record["bib_call_no"] = self.__bib_call_no.filter_none_vals()
        if isinstance(self.__bib_vendor_code, list):
            record["bib_vendor_code"] = [
                i.filter_none_vals() for i in self.__bib_vendor_code
            ]
        else:
            record["bib_vendor_code"] = self.__bib_vendor_code.filter_none_vals()
        if isinstance(self.__lc_class, list):
            record["lc_class"] = [i.filter_none_vals() for i in self.__lc_class]
        else:
            record["lc_class"] = self.__lc_class.filter_none_vals()
        if isinstance(self.__library_field, list):
            record["library_field"] = [
                i.filter_none_vals() for i in self.__library_field
            ]
        else:
            record["library_field"] = self.__library_field.filter_none_vals()
        if isinstance(self.__order_field, list):
            record["order_field"] = [i.filter_none_vals() for i in self.__order_field]
        else:
            record["order_field"] = self.__order_field.filter_none_vals()
        if isinstance(self.__invoice_field, list):
            record["invoice_field"] = [
                i.filter_none_vals() for i in self.__invoice_field
            ]
        else:
            record["invoice_field"] = self.__invoice_field.filter_none_vals()
        record["item_fields"] = [i.filter_none_vals() for i in self.__item_fields]
        record["material_type"] = self.material_type
        return record

    def get_control_number(self) -> Optional[str]:
        for field in self.fields:
            match field.tag:
                case "001":
                    return field.data
                case "035" if field.get("a") is not None:
                    return field.get("a")
                case "020" if field.get("a") is not None:
                    return field.get("a")
                case "022" if field.get("a") is not None:
                    return field.get("a")
                case "024" if field.get("a") is not None:
                    return field.get("a")
                case "010" if field.get("a") is not None:
                    return field.get("a")
                case "852" if field.get("h") is not None:
                    return field.get("h")
                case _:
                    continue
        return None
