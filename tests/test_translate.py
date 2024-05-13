from shelf_ready_validator.translate import VendorRecord, read_marc_records
from pymarc import Field, Subfield
import pytest


def test_read_marc_records():
    reader = read_marc_records("tests/test.mrc")
    n = 0
    for record in reader:
        n += 1
    assert n == 10


def test_get_record_input(stub_record):
    r = VendorRecord(stub_record)
    assert r.dict_input["order_fund"] == "123456apprv"


def test_get_record_input_keyerror(stub_record):
    stub_record["901"].delete_subfield("a")
    r = VendorRecord(stub_record)
    assert r.dict_input["order_fund"] == "123456apprv"


def test_convert_monograph_record_to_input(stub_record):
    r = VendorRecord(stub_record)
    assert r.material_type == "monograph_record"


def test_convert_monograph_record_value_error(stub_record):
    stub_record["300"].delete_subfield("a")
    stub_record["300"].add_subfield("a", "xi pages :")
    r = VendorRecord(stub_record)
    assert r.material_type == "monograph_record"


def test_convert_monograph_record_other(stub_record):
    stub_record["300"].delete_subfield("a")
    stub_record["300"].add_subfield("a", "xi, 120 pages :")
    r = VendorRecord(stub_record)
    assert r.material_type == "monograph_record"


def test_convert_pamphlet_record_to_input(stub_record):
    stub_record["300"].delete_subfield("a")
    stub_record["300"].add_subfield("a", "10 pages :")
    r = VendorRecord(stub_record)
    assert r.material_type == "pamphlet"


def test_convert_multivol_record_to_input(stub_record):
    stub_record["300"].delete_subfield("a")
    stub_record["300"].add_subfield("a", "10 volumes :")
    r = VendorRecord(stub_record)
    assert r.material_type == "multipart"


@pytest.mark.parametrize(
    "subfield",
    ["Catalogues Raisonnes", "Catalogue Raissonne"],
)
def test_convert_CR_record_to_input(stub_record, subfield):
    stub_record.add_field(
        Field(
            tag="650",
            indicators=["", ""],
            subfields=[
                Subfield(code="a", value="foo"),
                Subfield(code="x", value="bar"),
                Subfield(code="y", value="19th century"),
                Subfield(code="v", value=subfield),
            ],
        )
    )
    r = VendorRecord(stub_record)
    assert r.material_type == "catalogue_raissonne"


def test_convert_monograph_with_items(stub_record):
    stub_record.add_field(
        Field(
            tag="949",
            indicators=["", ""],
            subfields=[
                Subfield(code="z", value="8528"),
                Subfield(code="a", value="ReCAP 23-100000"),
                Subfield(code="i", value="33433123456789"),
                Subfield(code="p", value="1.00"),
                Subfield(code="v", value="EVP"),
                Subfield(code="h", value="43"),
                Subfield(code="l", value="rc2ma"),
                Subfield(code="t", value="55"),
            ],
        )
    )
    r = VendorRecord(stub_record)
    assert len(r.dict_input["items"]) == 1


def test_convert_invalid_record(stub_record):
    stub_record.remove_fields("852")
    with pytest.raises(KeyError):
        r = VendorRecord(stub_record)
        r.dict_input["bib_call_no_ind1"]
