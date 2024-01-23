from src.translate import read_marc_records, get_record_input, get_field_subfield
from pymarc import Field, Subfield
import pytest


def test_read_marc_records():
    reader = read_marc_records("tests/test.mrc")
    n = 0
    for record in reader:
        n += 1
    assert n == 10


def test_get_record_input(stub_record):
    converted = get_record_input(stub_record)
    assert converted["order_fund"] == "123456apprv"


def test_convert_monograph_record_to_input(stub_record):
    converted = get_record_input(stub_record)
    assert converted["material_type"] == "monograph_record"


def test_convert_pamphlet_record_to_input(stub_record):
    stub_record["300"].delete_subfield("a")
    stub_record["300"].add_subfield("a", "10 pages :")
    converted = get_record_input(stub_record)
    assert converted["material_type"] == "pamphlet"


def test_convert_multivol_record_to_input(stub_record):
    stub_record["300"].delete_subfield("a")
    stub_record["300"].add_subfield("a", "10 volumes :")
    converted = get_record_input(stub_record)
    assert converted["material_type"] == "multipart"


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
    converted = get_record_input(stub_record)
    assert converted["material_type"] == "catalogue_raissonne"


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
    converted = get_record_input(stub_record)
    assert len(converted["items"]) == 1
