from typing import List, Dict, Any
from pymarc import Record, Field, Leader
from shelf_ready_validator.field_models import (
    Item,
    OrderItemData,
    Order,
    Invoice,
    Library,
    LCClass,
    BibVendorCode,
    BibCallNo,
)


class VendorRecord(Record):
    def __init__(self, leader: Leader, fields: List[Field]):
        self.leader = leader
        self.fields = fields

        self.bib_call_no = self._field_from_marc("852")
        self.bib_vendor_code = self._field_from_marc("901")
        self.invoice_field = self._field_from_marc("980")
        self.item_fields = self._field_from_marc("949")
        self.lc_class = self._field_from_marc("050")
        self.library_field = self._field_from_marc("910")
        self.order_field = self._field_from_marc("960")
        self.order_item_data = self._get_order_item_data_list()
        self.material_type = self._get_material_type()

    def _field_from_marc(self, tag: str) -> Any:
        field_list = [i for i in self.fields if i.tag == tag]
        match (tag, len(field_list)):
            case ("852", 0):
                return BibCallNo(ind1=None, ind2=None, call_no=None)
            case ("852", 1):
                return BibCallNo.from_marc_field(field=field_list[0])
            case ("852", _):
                return [BibCallNo.from_marc_field(field=i) for i in field_list]
            case ("901", 0):
                return BibVendorCode(ind1=None, ind2=None, vendor_code=None)
            case ("901", 1):
                return BibVendorCode.from_marc_field(field=field_list[0])
            case ("901", _):
                return [BibVendorCode.from_marc_field(field=i) for i in field_list]
            case ("050", 0):
                return LCClass(ind1=None, ind2=None, lcc=None)
            case ("050", 1):
                return LCClass.from_marc_field(field=field_list[0])
            case ("050", _):
                return [LCClass.from_marc_field(field=i) for i in field_list]
            case ("910", 0):
                return Library(ind1=None, ind2=None, library=None)
            case ("910", 1):
                return Library.from_marc_field(field=field_list[0])
            case ("910", _):
                return [Library.from_marc_field(field=i) for i in field_list]
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
                return [Item.from_marc_field(field=i) for i in field_list]
            case ("960", 0):
                return Order(
                    ind1=None,
                    ind2=None,
                    order_location=None,
                    order_fund=None,
                    order_price=None,
                )
            case ("960", 1):
                return Order.from_marc_field(field=field_list[0])
            case ("960", _):
                return [Order.from_marc_field(field=i) for i in field_list]
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
                return Invoice.from_marc_field(field=field_list[0])
            case ("980", _):
                return [Invoice.from_marc_field(field=i) for i in field_list]
            case _:
                return None

    def _get_order_item_data_list(self) -> List[OrderItemData]:
        order_item_data_list = []
        if isinstance(self.order_field, list):
            for order_loc in self.order_field:
                for item in self.item_fields:
                    data_combo = OrderItemData(
                        order_location=order_loc.order_location,
                        item_location=item.item_location,
                        item_type=item.item_type,
                    )
                    order_item_data_list.append(data_combo)
        else:
            for item in self.item_fields:
                data_combo = OrderItemData(
                    order_location=self.order_field.order_location,
                    item_location=item.item_location,
                    item_type=item.item_type,
                )
                order_item_data_list.append(data_combo)
        return order_item_data_list

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
        if isinstance(self.bib_call_no, list):
            record["bib_call_no"] = [i.filter_none_vals() for i in self.bib_call_no]
        else:
            record["bib_call_no"] = self.bib_call_no.filter_none_vals()
        if isinstance(self.bib_vendor_code, list):
            record["bib_vendor_code"] = [
                i.filter_none_vals() for i in self.bib_vendor_code
            ]
        else:
            record["bib_vendor_code"] = self.bib_vendor_code.filter_none_vals()
        if isinstance(self.lc_class, list):
            record["lc_class"] = [i.filter_none_vals() for i in self.lc_class]
        else:
            record["lc_class"] = self.lc_class.filter_none_vals()
        if isinstance(self.library_field, list):
            record["library_field"] = [i.filter_none_vals() for i in self.library_field]
        else:
            record["library_field"] = self.library_field.filter_none_vals()
        if isinstance(self.order_field, list):
            record["order_field"] = [i.filter_none_vals() for i in self.order_field]
        else:
            record["order_field"] = self.order_field.filter_none_vals()
        if isinstance(self.invoice_field, list):
            record["invoice_field"] = [i.filter_none_vals() for i in self.invoice_field]
        else:
            record["invoice_field"] = self.invoice_field.filter_none_vals()
        record["item_fields"] = [i.filter_none_vals() for i in self.item_fields]
        record["order_item_data"] = [i.filter_none_vals() for i in self.order_item_data]
        record["material_type"] = self.material_type
        return record
