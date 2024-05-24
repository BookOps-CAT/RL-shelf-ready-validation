from typing import Union, Optional
from pymarc import Record


class VendorRecord:
    """Defines a vendor record and related methods for validator"""

    def __init__(
        self,
        record: Record,
    ) -> None:

        self.record = record
        self.dict_input = self._get_dict_input()
        self.material_type = self._get_material_type()

    def _get_field_subfield(
        self, field: str, subfield: Optional[str] = None
    ) -> Union[str, KeyError]:
        """
        Gets value of field or field/subfield pair. Returns a KeyError if field
        and/or subfield does not exist. KeyError can be stripped out before
        reading input into validator
        """
        try:
            if subfield:
                field_subfield_value = self.record[field][subfield]
                return field_subfield_value
            else:
                field_value = str(self.record[field])
                return field_value
        except KeyError as e:
            return e

    def _get_dict_input(self) -> dict:
        """
        Reads a MARC record and creates dict input for validation
        Uses get_field_subfield function to return KeyErrors for missing fields
        KeyErrors removed from dict to ensure validator recognizes missing fields
        """
        r = self.record
        library = self._get_field_subfield("910", "a")
        record_data = {
            "material_type": self._get_material_type(),
            "bib_call_no": f"{self._get_field_subfield('852')[1:]}",
            "bib_vendor_code": self._get_field_subfield("901", "a"),
            "lcc": self._get_field_subfield("050", "a"),
            "invoice_date": self._get_field_subfield("980", "a"),
            "invoice_price": self._get_field_subfield("980", "b"),
            "invoice_shipping": self._get_field_subfield("980", "c"),
            "invoice_tax": self._get_field_subfield("980", "d"),
            "invoice_net_price": self._get_field_subfield("980", "e"),
            "invoice_number": self._get_field_subfield("980", "f"),
            "invoice_copies": self._get_field_subfield("980", "g"),
            "order_price": self._get_field_subfield("960", "s"),
            "order_location": self._get_field_subfield("960", "t"),
            "order_fund": self._get_field_subfield("960", "u"),
            "order_indicators": f"{self._get_field_subfield('960')[6:8]}",
            "library": library,
        }
        dict_input = {
            key: val for key, val in record_data.items() if type(val) is not KeyError
        }
        items = r.get_fields("949")
        if items:
            item_list = []
            for item in items:
                item_output = {
                    "item_call_tag": item.get("z"),
                    "item_call_no": item.get("a"),
                    "item_barcode": item.get("i"),
                    "item_price": item.get("p"),
                    "item_vendor_code": item.get("v"),
                    "item_agency": item.get("h"),
                    "item_location": item.get("l"),
                    "item_type": item.get("t"),
                    "library": library,
                    "item_indicators": f"{self._get_field_subfield('949')[6:8]}",
                }
                edited_item = {
                    key: val for key, val in item_output.items() if val is not None
                }
                item_list.append(edited_item)
            dict_input["items"] = item_list
        return dict_input

    def _get_material_type(self) -> str:
        """
        Reads record data to determine material type
        Validator chooses model to validate against based on material type

        this function needs to be built out more
        """
        r = self.record
        subjects = r.subjects
        subject_subfield_v = []
        for subject in subjects:
            subfield_v = subject.get_subfields("v")
            subject_subfield_v.append(subfield_v)
        subject_subfield_list = [
            item for listed in subject_subfield_v for item in listed
        ]
        physical_desc = self.record.physicaldescription
        field_300a = physical_desc[0].get_subfields("a")
        split_300a = field_300a[0].split()
        if "Catalogues Raisonnes" in subject_subfield_list:
            return "catalogue_raissonne"
        elif "Catalogue Raissonne" in subject_subfield_list:
            return "catalogue_raissonne"
        elif "volumes" in split_300a[1]:
            return "multipart"
        elif "pages" in split_300a[1]:
            try:
                pages = int(split_300a[0])
                if pages < 50:
                    return "pamphlet"
                else:
                    return "monograph_record"
            except ValueError:
                return "monograph_record"
        else:
            return "monograph_record"
