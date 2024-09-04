import pytest
from pydantic import ValidationError
from contextlib import nullcontext as does_not_raise
from pymarc import Field, Subfield
from shelf_ready_validator.marc_scratch import MonographRecord


def test_ScratchMonographRecord_valid():
    with does_not_raise():
        MonographRecord(
            leader="00000cam a2200000 a 4500",
            fields=[
                {
                    "050": {
                        "ind1": " ",
                        "ind2": "4",
                        "subfields": [{"a": "F00"}, {"b": ".F00"}],
                    }
                },
                {"245": {"ind1": "0", "ind2": "0", "subfields": [{"a": "The Title"}]}},
                {
                    "852": {
                        "ind1": "8",
                        "ind2": " ",
                        "subfields": [{"h": "ReCAP 24-111111"}],
                    }
                },
                {"901": {"ind1": " ", "ind2": " ", "subfields": [{"a": "EVP"}]}},
                {"910": {"ind1": " ", "ind2": " ", "subfields": [{"a": "RL"}]}},
                {
                    "960": {
                        "ind1": " ",
                        "ind2": " ",
                        "subfields": [{"s": "100"}, {"t": "MAL"}, {"u": "123456apprv"}],
                    }
                },
                {
                    "980": {
                        "ind1": " ",
                        "ind2": " ",
                        "subfields": [
                            {"a": "240101"},
                            {"b": "100"},
                            {"c": "0"},
                            {"d": "0"},
                            {"f": "1"},
                            {"e": "100"},
                            {"g": "1"},
                        ],
                    }
                },
                {
                    "949": {
                        "ind1": " ",
                        "ind2": "1",
                        "subfields": [
                            {"z": "8528"},
                            {"a": "ReCAP 24-111111"},
                            {"i": "33433123456789"},
                            {"p": "1.00"},
                            {"v": "EVP"},
                            {"h": "43"},
                            {"l": "rc2ma"},
                            {"t": "55"},
                            {"c": "1"},
                            {"u": "foo"},
                            {"m": "bar"},
                        ],
                    }
                },
            ],
        )


def test_ScratchMonographRecord_from_marc_dict_valid(stub_record):
    record_dict = stub_record.as_dict()
    with does_not_raise():
        MonographRecord(**record_dict)


def test_ScratchMonographRecord_from_marc_valid(stub_record):
    with does_not_raise():
        MonographRecord(leader=stub_record.leader, fields=stub_record.fields)


def test_ScratchMonographRecord_from_marc_invalid(stub_record):
    stub_record.remove_fields("901", "852")
    stub_record.add_field(
        Field(
            tag="852",
            indicators=["8", " "],
            subfields=[Subfield(code="h", value="foo")],
        )
    )
    with pytest.raises(ValidationError) as e:
        MonographRecord(leader=stub_record.leader, fields=stub_record.fields)
    assert len(e.value.errors()) == 2
    assert sorted([i["type"] for i in e.value.errors()]) == sorted(
        ["missing_before_validation", "string_pattern_mismatch"]
    )


def test_ScratchMonographRecord_invalid():
    record_dict = {
        "leader": "00000cam a2200000 a 4500",
        "fields": [
            {"245": {"ind1": "0", "ind2": "0", "subfields": [{"a": "The Title"}]}},
            {
                "852": {
                    "ind1": "8",
                    "ind2": " ",
                    "subfields": [{"h": "foo"}],
                }
            },
            {"901": {"ind1": " ", "ind2": " ", "subfields": [{"a": "EVP"}]}},
            {"910": {"ind1": " ", "ind2": " ", "subfields": [{"a": "RL"}]}},
            {
                "960": {
                    "ind1": " ",
                    "ind2": " ",
                    "subfields": [{"s": "100"}, {"t": "bar"}, {"u": "123456apprv"}],
                }
            },
            {
                "980": {
                    "ind1": " ",
                    "ind2": " ",
                    "subfields": [
                        {"a": "240101"},
                        {"b": "100"},
                        {"c": "0"},
                        {"d": "0"},
                        {"f": "1"},
                        {"e": "100"},
                        {"g": "1"},
                    ],
                }
            },
            {
                "949": {
                    "ind1": " ",
                    "ind2": "1",
                    "subfields": [
                        {"z": "8528"},
                        {"a": "ReCAP 24-111111"},
                        {"i": "33433123456789"},
                        {"p": "1.00"},
                        {"v": "EVP"},
                        {"h": "43"},
                        {"l": "rc2ma"},
                        {"t": "55"},
                        {"c": "1"},
                        {"u": "foo"},
                        {"m": "bar"},
                    ],
                }
            },
        ],
    }
    with pytest.raises(ValidationError) as e:
        MonographRecord(**record_dict)
    assert len(e.value.errors()) == 3
    assert sorted([i["type"] for i in e.value.errors()]) == sorted(
        ["literal_error", "string_pattern_mismatch", "missing_before_validation"]
    )
