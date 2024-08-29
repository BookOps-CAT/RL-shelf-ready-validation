from pymarc import Record, Field, Subfield, Leader
from shelf_ready_validator.vendor_marc import (
    VendorRecord,
    Item,
    Order,
    Invoice,
    Library,
    LCClass,
    BibVendorCode,
    BibCallNo,
)


def test_VendorRecord(stub_record):
    record = VendorRecord(leader=stub_record.leader, fields=stub_record.fields)
    assert isinstance(record.bib_call_no, BibCallNo)
    assert isinstance(record.bib_vendor_code, BibVendorCode)
    assert isinstance(record.invoice_field, Invoice)
    assert isinstance(record.item_fields[0], Item)
    assert isinstance(record.item_fields, list)
    assert isinstance(record.lc_class, LCClass)
    assert isinstance(record.library_field, Library)
    assert isinstance(record.order_field, Order)
    assert isinstance(record.material_type, str)
    assert record.material_type == "monograph_record"


def test_VendorRecord_field_from_marc(stub_record):
    record = VendorRecord(leader=stub_record.leader, fields=stub_record.fields)
    fake_field = record._field_from_marc("100")
    assert fake_field is None


def test_VendorRecord_dupe_vals(stub_record_with_dupes):
    record = VendorRecord(
        leader=stub_record_with_dupes.leader, fields=stub_record_with_dupes.fields
    )
    assert isinstance(record.bib_call_no, list)
    assert isinstance(record.bib_call_no[0], BibCallNo)
    assert isinstance(record.bib_vendor_code, list)
    assert isinstance(record.bib_vendor_code[0], BibVendorCode)
    assert isinstance(record.invoice_field, list)
    assert isinstance(record.invoice_field[0], Invoice)
    assert isinstance(record.item_fields, list)
    assert isinstance(record.item_fields[0], Item)
    assert isinstance(record.lc_class, list)
    assert isinstance(record.lc_class[0], LCClass)
    assert isinstance(record.library_field, list)
    assert isinstance(record.library_field[0], Library)
    assert isinstance(record.order_field, list)
    assert isinstance(record.order_field[0], Order)


def test_VendorRecord_pydantic_input(stub_record):
    record = VendorRecord(leader=stub_record.leader, fields=stub_record.fields)
    record_input = record.pydantic_dict_input()
    assert record_input["bib_call_no"] == {
        "ind1": "8",
        "ind2": " ",
        "call_no": "ReCAP 23-100000",
    }
    assert record_input["bib_vendor_code"] == {
        "ind1": " ",
        "ind2": " ",
        "vendor_code": "EVP",
    }
    assert record_input["invoice_field"] == {
        "ind1": " ",
        "ind2": " ",
        "invoice_date": "240101",
        "invoice_price": "100",
        "invoice_shipping": "100",
        "invoice_tax": "000",
        "invoice_number": "123456",
        "invoice_net_price": "200",
        "invoice_copies": "1",
    }
    assert record_input["item_fields"] == [
        {
            "ind1": " ",
            "ind2": "1",
            "item_call_tag": "8528",
            "item_call_no": "ReCAP 23-100000",
            "item_barcode": "33433123456789",
            "item_price": "1.00",
            "item_message": "foo",
            "message": "bar",
            "item_vendor_code": "AUXAM",
            "item_agency": "43",
            "item_location": "rcmf2",
            "item_volume": "1",
            "item_type": "55",
        }
    ]
    assert record_input["lc_class"] == {"ind1": " ", "ind2": "4", "lcc": "DK504.73"}
    assert record_input["library_field"] == {"ind1": " ", "ind2": " ", "library": "RL"}
    assert record_input["order_field"] == {
        "ind1": " ",
        "ind2": " ",
        "order_price": "100",
        "order_location": "MAF",
        "order_fund": "123456apprv",
    }
    assert record_input["material_type"] == "monograph"


def test_VendorRecord_pydantic_input_dupe_fields(stub_record_with_dupes):
    record = VendorRecord(
        leader=stub_record_with_dupes.leader, fields=stub_record_with_dupes.fields
    )
    record_input = record.pydantic_dict_input()
    assert isinstance(record_input["leader"], str)
    assert isinstance(record_input["bib_call_no"], list)
    assert isinstance(record_input["bib_vendor_code"], list)
    assert isinstance(record_input["invoice_field"], list)
    assert isinstance(record_input["item_fields"], list)
    assert isinstance(record_input["lc_class"], list)
    assert isinstance(record_input["library_field"], list)
    assert isinstance(record_input["order_field"], list)
    assert isinstance(record_input["material_type"], str)


def test_MaterialType_monograph(stub_record):
    record = VendorRecord(leader=stub_record.leader, fields=stub_record.fields)
    assert "Catalogues Raissones" not in stub_record.subjects
    assert record.material_type == "monograph"


def test_MaterialType_pamphlet():
    pamphlet_record = Record()
    pamphlet_record.leader = Leader("00820cam a22001935i 4500")
    pamphlet_record.add_field(
        Field(
            tag="300",
            indicators=[" ", " "],
            subfields=[
                Subfield(code="a", value="10 pages :"),
            ],
        )
    )
    record = VendorRecord(leader=pamphlet_record.leader, fields=pamphlet_record.fields)
    assert record.material_type == "pamphlet"


def test_MaterialType_multivol():
    multivol_record = Record()
    multivol_record.leader = Leader("00820foo a22001935i 4500")
    multivol_record.add_field(
        Field(
            tag="300",
            indicators=[" ", " "],
            subfields=[
                Subfield(code="a", value="10 volumes :"),
            ],
        )
    )
    record = VendorRecord(leader=multivol_record.leader, fields=multivol_record.fields)
    assert record.material_type == "multipart"


def test_MaterialType_catalogue():
    catalogue_record = Record()
    catalogue_record.leader = Leader("00820cam a22001935i 4500")
    catalogue_record.add_field(
        Field(
            tag="650",
            indicators=[" ", " "],
            subfields=[
                Subfield(code="a", value="foo"),
                Subfield(code="v", value="Catalogues Raisonnes"),
            ],
        )
    )
    record = VendorRecord(
        leader=catalogue_record.leader, fields=catalogue_record.fields
    )
    assert record.material_type == "catalogue_raissonne"


def test_MaterialType_empty_record():
    marc_record = Record()
    record = VendorRecord(leader=marc_record.leader, fields=marc_record.fields)
    assert record.material_type == "unknown"


def test_MaterialType_unknown():
    unknown_record = Record()
    unknown_record.leader = "00820foo a22001935i 4500"
    record = VendorRecord(leader=unknown_record.leader, fields=unknown_record.fields)
    assert record.material_type == "unknown"
