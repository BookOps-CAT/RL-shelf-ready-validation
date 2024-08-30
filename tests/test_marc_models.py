import pytest
from pydantic import ValidationError
from contextlib import nullcontext as does_not_raise
from shelf_ready_validator.marc_models import MonographRecord, OtherRecord


def test_MonographRecord_valid(
    mock_bib_call_no,
    mock_bib_vendor_code,
    mock_lc_class,
    mock_library,
    mock_order_field,
    mock_invoice_field,
    mock_item_fields,
):
    with does_not_raise():
        MonographRecord(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_call_no=mock_bib_call_no,
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type="monograph",
            order_field=mock_order_field,
            invoice_field=mock_invoice_field,
            item_fields=mock_item_fields,
        )


def test_MonographRecord_multiple_items(
    mock_bib_call_no,
    mock_bib_vendor_code,
    mock_lc_class,
    mock_library,
    mock_order_field,
    mock_invoice_field,
):
    with does_not_raise():
        MonographRecord(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_call_no=mock_bib_call_no,
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type="monograph",
            order_field=mock_order_field,
            invoice_field=mock_invoice_field,
            item_fields=[
                {
                    "ind1": " ",
                    "ind2": "1",
                    "item_call_tag": "8528",
                    "item_call_no": "ReCAP 23-000000",
                    "item_barcode": "33433123456789",
                    "item_price": "1.00",
                    "item_vendor_code": "EVP",
                    "item_agency": "43",
                    "item_location": "rc2ma",
                    "item_type": "55",
                },
                {
                    "ind1": " ",
                    "ind2": "1",
                    "item_call_tag": "8528",
                    "item_call_no": "ReCAP 23-000000",
                    "item_barcode": "33433987654321",
                    "item_price": "1.00",
                    "item_vendor_code": "EVP",
                    "item_agency": "43",
                    "item_location": "rc2ma",
                    "item_type": "55",
                },
            ],
        )


@pytest.mark.parametrize(
    "order_location_value,item_location_value,item_type_value,",
    [
        ("MAB", "rcmb2", "2"),
        ("MAS", "rcmb2", "2"),
        ("MAF", "rcmf2", "55"),
        ("MAF", "rcmf2", None),
        ("MAG", "rcmg2", "55"),
        ("MAG", "rcmg2", None),
    ],
)
def test_MonographRecord_valid_location_combos(
    mock_bib_call_no,
    mock_bib_vendor_code,
    mock_lc_class,
    mock_library,
    mock_invoice_field,
    order_location_value,
    item_location_value,
    item_type_value,
):
    with does_not_raise():
        MonographRecord(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_call_no=mock_bib_call_no,
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type="monograph",
            order_field={
                "ind1": " ",
                "ind2": " ",
                "order_price": "123",
                "order_location": order_location_value,
                "order_fund": "123",
            },
            invoice_field=mock_invoice_field,
            item_fields=[
                {
                    "ind1": " ",
                    "ind2": "1",
                    "item_call_tag": "8528",
                    "item_call_no": "ReCAP 23-000000",
                    "item_barcode": "33433123456789",
                    "item_price": "1.00",
                    "item_vendor_code": "EVP",
                    "item_agency": "43",
                    "item_location": item_location_value,
                    "item_type": item_type_value,
                }
            ],
        )


def test_MonographRecord_order_item_data_not_checked(
    mock_bib_call_no,
    mock_bib_vendor_code,
    mock_lc_class,
    mock_library,
    mock_invoice_field,
):
    with pytest.raises(ValidationError) as e:
        MonographRecord(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_call_no=mock_bib_call_no,
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type="monograph",
            order_field=None,
            invoice_field=mock_invoice_field,
            item_fields=None,
        )
    assert "order_item_mismatch" not in [error["type"] for error in e.value.errors()]
    assert len(e.value.errors()) == 2


def test_MonographRecord_validate_missing_field(
    mock_bib_vendor_code,
    mock_lc_class,
    mock_library,
    mock_invoice_field,
    mock_order_field,
    mock_item_fields,
):
    with pytest.raises(ValidationError) as e:
        MonographRecord(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type="monograph",
            order_field=mock_order_field,
            invoice_field=mock_invoice_field,
            item_fields=mock_item_fields,
        )
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0]["type"] == "missing"


def test_MonographRecord_validate_missing_item_fields(
    mock_bib_call_no,
    mock_bib_vendor_code,
    mock_lc_class,
    mock_library,
    mock_invoice_field,
    mock_order_field,
):
    with pytest.raises(ValidationError) as e:
        MonographRecord(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_call_no=mock_bib_call_no,
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type="monograph",
            order_field=mock_order_field,
            invoice_field=mock_invoice_field,
        )
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0]["type"] == "missing"


@pytest.mark.parametrize(
    "leader_value, leader_error",
    [
        ("foo", "string_too_short"),
        ("bar", "string_too_short"),
        ("foobarfoobarfoobarfoobar", "string_pattern_mismatch"),
    ],
)
def test_MonographRecord_invalid_leader(
    mock_bib_call_no,
    mock_bib_vendor_code,
    mock_lc_class,
    mock_library,
    mock_order_field,
    mock_invoice_field,
    mock_item_fields,
    leader_value,
    leader_error,
):
    with pytest.raises(ValidationError) as e:
        MonographRecord(
            leader=leader_value,
            fields=[{"245": {"a": "The Title"}}],
            bib_call_no=mock_bib_call_no,
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type="monograph",
            order_field=mock_order_field,
            invoice_field=mock_invoice_field,
            item_fields=mock_item_fields,
        )
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0]["type"] == leader_error


@pytest.mark.parametrize(
    "fields_value",
    [{}, None],
)
def test_MonographRecord_invalid_fields(
    mock_bib_call_no,
    mock_bib_vendor_code,
    mock_lc_class,
    mock_library,
    mock_order_field,
    mock_invoice_field,
    mock_item_fields,
    fields_value,
):
    with pytest.raises(ValidationError) as e:
        MonographRecord(
            leader="00000cam a2200000 a 4500",
            fields=fields_value,
            bib_call_no=mock_bib_call_no,
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type="monograph",
            order_field=mock_order_field,
            invoice_field=mock_invoice_field,
            item_fields=mock_item_fields,
        )
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0]["type"] == "list_type"


def test_MonographRecord_invalid_bib_call_no(
    mock_bib_vendor_code,
    mock_lc_class,
    mock_library,
    mock_order_field,
    mock_invoice_field,
    mock_item_fields,
):
    with pytest.raises(ValidationError) as e:
        MonographRecord(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_call_no={"bib_call_no"},
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type="monograph",
            order_field=mock_order_field,
            invoice_field=mock_invoice_field,
            item_fields=mock_item_fields,
        )
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0]["type"] == "model_type"


def test_MonographRecord_invalid_bib_vendor_code(
    mock_bib_call_no,
    mock_lc_class,
    mock_library,
    mock_order_field,
    mock_invoice_field,
    mock_item_fields,
):
    with pytest.raises(ValidationError) as e:
        MonographRecord(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_call_no=mock_bib_call_no,
            bib_vendor_code={"bib_vendor_code"},
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type="monograph",
            order_field=mock_order_field,
            invoice_field=mock_invoice_field,
            item_fields=mock_item_fields,
        )
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0]["type"] == "model_type"


def test_MonographRecord_invalid_lc_class(
    mock_bib_call_no,
    mock_bib_vendor_code,
    mock_library,
    mock_order_field,
    mock_invoice_field,
    mock_item_fields,
):
    with pytest.raises(ValidationError) as e:
        MonographRecord(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_call_no=mock_bib_call_no,
            bib_vendor_code=mock_bib_vendor_code,
            lc_class={"lc_class"},
            library_field=mock_library,
            material_type="monograph",
            order_field=mock_order_field,
            invoice_field=mock_invoice_field,
            item_fields=mock_item_fields,
        )
    assert len(e.value.errors()) == 2
    assert sorted([i["type"] for i in e.value.errors()]) == sorted(
        ["model_type", "model_type"]
    )
    assert sorted([i["loc"][1] for i in e.value.errors()]) == sorted(
        [
            "function-after[validate_indicator_pair(), LCClassModel]",
            "list[function-after[validate_indicator_pair(), LCClassModel]]",
        ]
    )


def test_MonographRecord_invalid_library_field(
    mock_bib_call_no,
    mock_bib_vendor_code,
    mock_lc_class,
    mock_order_field,
    mock_invoice_field,
    mock_item_fields,
):
    with pytest.raises(ValidationError) as e:
        MonographRecord(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_call_no=mock_bib_call_no,
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field={"library_field"},
            material_type="monograph",
            order_field=mock_order_field,
            invoice_field=mock_invoice_field,
            item_fields=mock_item_fields,
        )
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0]["type"] == "model_type"


def test_MonographRecord_invalid_material_type(
    mock_bib_call_no,
    mock_bib_vendor_code,
    mock_lc_class,
    mock_library,
    mock_order_field,
    mock_invoice_field,
    mock_item_fields,
):
    with pytest.raises(ValidationError) as e:
        MonographRecord(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_call_no=mock_bib_call_no,
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type=None,
            order_field=mock_order_field,
            invoice_field=mock_invoice_field,
            item_fields=mock_item_fields,
        )
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0]["type"] == "literal_error"


def test_MonographRecord_invalid_order_field(
    mock_bib_call_no,
    mock_bib_vendor_code,
    mock_lc_class,
    mock_library,
    mock_invoice_field,
    mock_item_fields,
):
    with pytest.raises(ValidationError) as e:
        MonographRecord(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_call_no=mock_bib_call_no,
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type="monograph",
            order_field={"order_field"},
            invoice_field=mock_invoice_field,
            item_fields=mock_item_fields,
        )
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0]["type"] == "model_type"


def test_MonographRecord_invalid_invoice_field(
    mock_bib_call_no,
    mock_bib_vendor_code,
    mock_lc_class,
    mock_library,
    mock_order_field,
    mock_item_fields,
):
    with pytest.raises(ValidationError) as e:
        MonographRecord(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_call_no=mock_bib_call_no,
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type="monograph",
            order_field=mock_order_field,
            invoice_field={"invoice_field"},
            item_fields=mock_item_fields,
        )
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0]["type"] == "model_type"


def test_MonographRecord_invalid_item_fields(
    mock_bib_call_no,
    mock_bib_vendor_code,
    mock_lc_class,
    mock_library,
    mock_order_field,
    mock_invoice_field,
):
    with pytest.raises(ValidationError) as e:
        MonographRecord(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_call_no=mock_bib_call_no,
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type="monograph",
            order_field=mock_order_field,
            invoice_field=mock_invoice_field,
            item_fields=[{"item_field"}],
        )
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0]["type"] == "model_type"


@pytest.mark.parametrize(
    "order_location_value,item_location_value,item_type_value,",
    [
        ("MAB", "rcmf2", "55"),
        ("MAS", "rcmb2", None),
        ("MAF", "rc2ma", "2"),
        ("MAF", "rc2cf", None),
        ("MAG", "rcpt2", "55"),
        ("MAG", "rc2ma", None),
    ],
)
def test_MonographRecord_invalid_order_item_data(
    mock_bib_call_no,
    mock_bib_vendor_code,
    mock_lc_class,
    mock_library,
    mock_invoice_field,
    order_location_value,
    item_location_value,
    item_type_value,
):
    with pytest.raises(ValidationError) as e:
        MonographRecord(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_call_no=mock_bib_call_no,
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type="monograph",
            order_field={
                "ind1": " ",
                "ind2": " ",
                "order_price": "123",
                "order_location": order_location_value,
                "order_fund": "123",
            },
            invoice_field=mock_invoice_field,
            item_fields=[
                {
                    "ind1": " ",
                    "ind2": "1",
                    "item_call_tag": "8528",
                    "item_call_no": "ReCAP 23-000000",
                    "item_barcode": "33433123456789",
                    "item_price": "1.00",
                    "item_vendor_code": "EVP",
                    "item_agency": "43",
                    "item_location": item_location_value,
                    "item_type": item_type_value,
                }
            ],
        )
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0]["type"] == "order_item_mismatch"


@pytest.mark.parametrize(
    "order_location_value,item_location_value,item_type_value,",
    [
        ("MAB", "rcmf2", "55"),
        ("MAS", "rcmb2", None),
        ("MAF", "rc2ma", "2"),
        ("MAF", "rc2cf", None),
        ("MAG", "rcpt2", "55"),
        ("MAG", "rc2ma", None),
    ],
)
def test_MonographRecord_invalid_order_item_data_multiple(
    mock_bib_call_no,
    mock_bib_vendor_code,
    mock_lc_class,
    mock_library,
    mock_invoice_field,
    order_location_value,
    item_location_value,
    item_type_value,
):
    with pytest.raises(ValidationError) as e:
        MonographRecord(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_call_no=mock_bib_call_no,
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type="monograph",
            order_field={
                "ind1": " ",
                "ind2": " ",
                "order_price": "123",
                "order_location": order_location_value,
                "order_fund": "123",
            },
            invoice_field=mock_invoice_field,
            item_fields=[
                {
                    "ind1": " ",
                    "ind2": "1",
                    "item_call_tag": "8528",
                    "item_call_no": "ReCAP 23-000000",
                    "item_barcode": "33433123456789",
                    "item_price": "1.00",
                    "item_vendor_code": "EVP",
                    "item_agency": "43",
                    "item_location": item_location_value,
                    "item_type": item_type_value,
                },
                {
                    "ind1": " ",
                    "ind2": "1",
                    "item_call_tag": "8528",
                    "item_call_no": "ReCAP 23-000000",
                    "item_barcode": "33433987654321",
                    "item_price": "1.00",
                    "item_vendor_code": "EVP",
                    "item_agency": "43",
                    "item_location": item_location_value,
                    "item_type": item_type_value,
                },
            ],
        )
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0]["type"] == "order_item_mismatch"


@pytest.mark.parametrize(
    "material_type_value",
    [
        "catalogue_raissonne",
        "dance",
        "multipart",
        "pamphlet",
        "non-standard_binding_packaging",
    ],
)
def test_OtherRecord_valid(
    mock_bib_vendor_code,
    mock_lc_class,
    mock_library,
    mock_order_field,
    mock_invoice_field,
    material_type_value,
):
    with does_not_raise():
        OtherRecord(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type=material_type_value,
            order_field=mock_order_field,
            invoice_field=mock_invoice_field,
        )


@pytest.mark.parametrize(
    "leader_value, leader_error",
    [
        ("foo", "string_too_short"),
        ("bar", "string_too_short"),
        ("foobarfoobarfoobarfoobar", "string_pattern_mismatch"),
    ],
)
def test_OtherRecord_invalid_leader(
    mock_bib_vendor_code,
    mock_lc_class,
    mock_library,
    mock_order_field,
    mock_invoice_field,
    leader_value,
    leader_error,
):
    with pytest.raises(ValidationError) as e:
        OtherRecord(
            leader=leader_value,
            fields=[{"245": {"a": "The Title"}}],
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type="pamphlet",
            order_field=mock_order_field,
            invoice_field=mock_invoice_field,
        )
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0]["type"] == leader_error


@pytest.mark.parametrize(
    "fields_value",
    [{}, None],
)
def test_OtherRecord_invalid_fields(
    mock_bib_vendor_code,
    mock_lc_class,
    mock_library,
    mock_order_field,
    mock_invoice_field,
    fields_value,
):
    with pytest.raises(ValidationError) as e:
        OtherRecord(
            leader="00000cam a2200000 a 4500",
            fields=fields_value,
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type="pamphlet",
            order_field=mock_order_field,
            invoice_field=mock_invoice_field,
        )
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0]["type"] == "list_type"


def test_OtherRecord_invalid_bib_vendor_code(
    mock_lc_class,
    mock_library,
    mock_order_field,
    mock_invoice_field,
):
    with pytest.raises(ValidationError) as e:
        OtherRecord(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_vendor_code={"bib_vendor_code"},
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type="pamphlet",
            order_field=mock_order_field,
            invoice_field=mock_invoice_field,
        )
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0]["type"] == "model_type"


def test_OtherRecord_invalid_lc_class(
    mock_bib_vendor_code,
    mock_library,
    mock_order_field,
    mock_invoice_field,
):
    with pytest.raises(ValidationError) as e:
        OtherRecord(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_vendor_code=mock_bib_vendor_code,
            lc_class={"lc_class"},
            library_field=mock_library,
            material_type="pamphlet",
            order_field=mock_order_field,
            invoice_field=mock_invoice_field,
        )
    print(e.value.errors())
    assert len(e.value.errors()) == 2
    assert sorted([i["type"] for i in e.value.errors()]) == sorted(
        ["model_type", "model_type"]
    )
    assert sorted([i["loc"][1] for i in e.value.errors()]) == sorted(
        [
            "function-after[validate_indicator_pair(), LCClassModel]",
            "list[function-after[validate_indicator_pair(), LCClassModel]]",
        ]
    )


def test_OtherRecord_invalid_library_field(
    mock_bib_vendor_code,
    mock_lc_class,
    mock_order_field,
    mock_invoice_field,
):
    with pytest.raises(ValidationError) as e:
        OtherRecord(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field={"library_field"},
            material_type="pamphlet",
            order_field=mock_order_field,
            invoice_field=mock_invoice_field,
        )
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0]["type"] == "model_type"


def test_OtherRecord_invalid_material_type(
    mock_bib_vendor_code,
    mock_lc_class,
    mock_library,
    mock_order_field,
    mock_invoice_field,
):
    with pytest.raises(ValidationError) as e:
        OtherRecord(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type=None,
            order_field=mock_order_field,
            invoice_field=mock_invoice_field,
        )
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0]["type"] == "literal_error"


def test_OtherRecord_invalid_order_field(
    mock_bib_vendor_code,
    mock_lc_class,
    mock_library,
    mock_invoice_field,
):
    with pytest.raises(ValidationError) as e:
        OtherRecord(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type="pamphlet",
            order_field={"order_field"},
            invoice_field=mock_invoice_field,
        )
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0]["type"] == "model_type"


def test_OtherRecord_invoice_field(
    mock_bib_vendor_code,
    mock_lc_class,
    mock_library,
    mock_order_field,
):
    with pytest.raises(ValidationError) as e:
        OtherRecord(
            leader="00000cam a2200000 a 4500",
            fields=[{"245": {"a": "The Title"}}],
            bib_vendor_code=mock_bib_vendor_code,
            lc_class=mock_lc_class,
            library_field=mock_library,
            material_type="pamphlet",
            order_field=mock_order_field,
            invoice_field={"invoice_field"},
        )
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0]["type"] == "model_type"
