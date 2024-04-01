from pymarc import Record, Field
from enum import Enum

from bookops_marc import SierraBibReader


class RLMarcEncoding(Enum):
    """
    A class to translate fields used in the validator to MARC fields/subfields
    """

    bib_call_no = "852"
    bib_call_no_ind1 = "852_ind1"
    bib_call_no_ind2 = "852_ind2"
    bib_vendor_code = "901$a"
    lcc = "050$a"
    invoice_date = "980$a"
    invoice_price = "980$b"
    invoice_shipping = "980$c"
    invoice_tax = "980$d"
    invoice_net_price = "980$e"
    invoice_number = "980$f"
    invoice_copies = "980$g"
    order_price = "960$s"
    order_location = "960$t"
    order_fund = "960$u"
    order_ind1 = "960_ind1"
    order_ind2 = "960_ind2"
    item_call_tag = "949$z"
    item_call_no = "949$a"
    item_barcode = "949$i"
    item_price = "949$p"
    item_message = "949$u"
    message = "949$m"
    item_vendor_code = "949$v"
    item_agency = "949$h"
    item_location = "949$l"
    item_type = "949$t"
    library = "910$a"
    item_ind1 = "949_ind1"
    item_ind2 = "949_ind2"
    items = "949"


class VendorRecord:
    """Defines a vendor record and related methods for validator"""

    def __init__(
        self,
        record: Record,
    ) -> None:
        
        self.record = record
        self.dict_input = self._get_dict_input()
        self.material_type = self._get_material_type()



    def _get_field_subfield(self, field: str, subfield: str):
        """
        Gets value of subfield and returns it to be assigned to a variable
        if subfield does not exist, returns KeyError
        KeyError can be stripped out before reading input into validator
        """
        try:
            field_subfield = self.record[field][subfield]
            return field_subfield
        except KeyError as e:
            return e

    def _get_field_indicators(self, field: Field, indicator: str):
        """
        Gets value of subfield and returns it to be assigned to a variable
        if subfield does not exist, returns KeyError
        KeyError can be stripped out before reading input into validator
        """
        if indicator == "indicator1":
            try:
                field = self.record[field]
                field_indicator = field.indicator1
                return field_indicator
            except KeyError as e:
                return e
        elif indicator == "indicator2":
            try:
                field = self.record[field]
                field_indicator = field.indicator2
                return field_indicator
            except KeyError as e:
                return e
        else:
            pass

    def _get_dict_input(self):
        """
        Reads a MARC record and creates dict input for validation
        Uses get_field_subfield function to return KeyErrors for missing fields
        KeyErrors removed from dict to ensure validator recognizes missing fields
        """
        r = self.record
        library = self._get_field_subfield("910", "a")
        record_data = {
            "material_type": self._get_material_type(),
            "bib_call_no": self._get_field_subfield("852", "h"),
            "bib_call_no_ind1": self._get_field_subfield("852", "indicator1"),
            "bib_call_no_ind2": self._get_field_subfield("852", "indicator2"),
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
            "order_ind1": self._get_field_indicators("960", "indicator1"),
            "order_ind2": self._get_field_indicators("960", "indicator2"),
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
                    "item_ind1": item.indicator1,
                    "item_ind2": item.indicator2,
                }
                edited_item = {
                    key: val for key, val in item_output.items() if val is not None
                }
                item_list.append(edited_item)
            dict_input["items"] = item_list
        if dict_input["material_type"] == "monograph_record":
            del dict_input["library"]
            return dict_input
        return dict_input

    def _get_material_type(self):
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
        subject_subfield_list = [item for listed in subject_subfield_v for item in listed]
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
        

def read_marc_records(file):
    """
    Reads .mrc file and returns a record
    """
    with open(file, "rb") as fh:
        reader = SierraBibReader(fh)
        for record in reader:
            yield record