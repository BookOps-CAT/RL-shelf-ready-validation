from src.validate.translate import (
    read_marc_records,
    read_marc_to_dict,
    convert_to_input,
)
import pytest


def test_read_marc_records():
    reader = read_marc_records("tests/test.mrc")
    n = 0
    for record in reader:
        n += 1
    assert n == 6


def test_read_marc_to_dict():
    reader = read_marc_to_dict("tests/test.mrc")
    control_numbers = []
    for record in reader:
        control_number = record["001"]
        control_numbers.append(control_number)
    assert len(control_numbers) == 6


def test_convert_to_input(stub_record_dict):
    converted = convert_to_input(stub_record_dict)
    assert converted["control_number"] == "on1381158740"


def test_convert_pamphlet_record_to_input(stub_record_dict):
    stub_record_dict["300"] = [
        {
            "ind1": " ",
            "ind2": " ",
            "subfields": [{"a": "10 pages :"}],
        }
    ]
    converted = convert_to_input(stub_record_dict)
    assert converted["item"]["material_type"] == "pamphlet"


def test_convert_multivol_record_to_input(stub_record_dict):
    stub_record_dict["300"] = [
        {
            "ind1": " ",
            "ind2": " ",
            "subfields": [{"a": "10 volumes :"}],
        }
    ]
    converted = convert_to_input(stub_record_dict)
    assert converted["item"]["material_type"] == "multipart"


@pytest.mark.parametrize(
    "field",
    [
        [
            {
                "ind1": " ",
                "ind2": "0",
                "subfields": [
                    {"a": "Foo"},
                    {"x": "Bar"},
                    {"y": "19th century"},
                    {"v": "Catalogues Raissonnes"},
                ],
            }
        ],
        [
            {
                "ind1": " ",
                "ind2": "0",
                "subfields": [
                    {"a": "Foo"},
                    {"x": "Bar"},
                    {"y": "19th century"},
                    {"v": "Catalogue Raissonne"},
                ],
            }
        ],
    ],
)
def test_convert_CR_record_to_input(stub_record_dict, field):
    stub_record_dict["650"] = field
    converted = convert_to_input(stub_record_dict)
    assert converted["item"]["material_type"] == "catalogue_raissonne"


def test_convert_invalid_item_record(stub_record_dict):
    del stub_record_dict["949"]
    with pytest.raises(KeyError):
        convert_to_input(stub_record_dict)


def test_convert_invalid_order_record(stub_record_dict):
    del stub_record_dict["960"]
    with pytest.raises(KeyError):
        convert_to_input(stub_record_dict)


def test_convert_invalid_invoice_record(stub_record_dict):
    del stub_record_dict["980"]
    with pytest.raises(KeyError):
        convert_to_input(stub_record_dict)
