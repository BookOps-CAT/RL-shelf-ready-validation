"""This module contains pydantic models for validating vendor-provided MARC records."""

from collections import defaultdict
from typing import Annotated, DefaultDict, Dict, List, Optional, Union
from pydantic import BaseModel, Field, model_validator, ConfigDict
from pydantic_core import PydanticCustomError, ValidationError, InitErrorDetails
from pymarc import Field as MarcField
from shelf_ready_validator.field_models import (
    BibCallNoModel,
    BibVendorCodeModel,
    InvoiceFieldModel,
    ItemFieldModel,
    LCClassModel,
    LibraryFieldModel,
    OrderFieldModel,
)
from shelf_ready_validator.vendor_fields import (
    BibVendorCode,
    LCClass,
    Library,
    Order,
    Invoice,
    Item,
)
from shelf_ready_validator.fields_scratch import BibCallNo


def get_subfield_from_field(
    field: Union[dict, MarcField], code: str
) -> Optional[Union[str, List[str]]]:
    """A helper function to extract a subfield as a str from a pymarc Field object."""
    if isinstance(field, dict):
        subfield_dict: Union[dict, DefaultDict] = defaultdict(list)
        subfields = field.get("subfields", [])
        if subfields == []:
            return None
        for subfield in subfields:
            for key, value in subfield.items():
                subfield_dict[key].append(value)
    else:
        subfield_dict = field.subfields_as_dict()
    subfield_list = subfield_dict.get(code, None)
    if subfield_list is not None and len(subfield_list) == 1:
        return subfield_list[0]
    else:
        return subfield_list


def validate_indiv_fields_dict(fields) -> list:
    validation_errors = []
    for field in fields:
        if "852" in field:
            subfield_h = get_subfield_from_field(field["852"], "h")
            try:
                BibCallNoModel(
                    ind1=field["852"]["ind1"],
                    ind2=field["852"]["ind2"],
                    call_no=subfield_h,
                )
            except ValidationError as e:
                validation_errors.extend(e.errors())
        elif "901" in field:
            subfield_a = get_subfield_from_field(field["901"], "a")
            try:
                BibVendorCodeModel(
                    ind1=field["901"]["ind1"],
                    ind2=field["901"]["ind2"],
                    vendor_code=subfield_a,
                )
            except ValidationError as e:
                validation_errors.extend(e.errors())
        elif "050" in field:
            try:
                LCClassModel(
                    ind1=field["050"]["ind1"],
                    ind2=field["050"]["ind2"],
                    lcc=get_subfield_from_field(field["050"], "a"),
                )
            except ValidationError as e:
                validation_errors.extend(e.errors())
        elif "910" in field:
            try:
                LibraryFieldModel(
                    ind1=field["910"]["ind1"],
                    ind2=field["910"]["ind2"],
                    library=get_subfield_from_field(field["910"], "a"),
                )
            except ValidationError as e:
                validation_errors.extend(e.errors())
        elif "960" in field:
            try:
                OrderFieldModel(
                    ind1=field["960"]["ind1"],
                    ind2=field["960"]["ind2"],
                    order_price=get_subfield_from_field(field["960"], "s"),
                    order_location=get_subfield_from_field(field["960"], "t"),
                    order_fund=get_subfield_from_field(field["960"], "u"),
                )
            except ValidationError as e:
                validation_errors.extend(e.errors())
        elif "980" in field:
            try:
                InvoiceFieldModel(
                    ind1=field["980"]["ind1"],
                    ind2=field["980"]["ind2"],
                    invoice_date=get_subfield_from_field(field["980"], "a"),
                    invoice_price=get_subfield_from_field(field["980"], "b"),
                    invoice_shipping=get_subfield_from_field(field["980"], "c"),
                    invoice_tax=get_subfield_from_field(field["980"], "d"),
                    invoice_net_price=get_subfield_from_field(field["980"], "e"),
                    invoice_number=get_subfield_from_field(field["980"], "f"),
                    invoice_copies=get_subfield_from_field(field["980"], "g"),
                )
            except ValidationError as e:
                validation_errors.extend(e.errors())
        elif "949" in field:
            try:
                ItemFieldModel(
                    ind1=field["949"]["ind1"],
                    ind2=field["949"]["ind2"],
                    item_call_tag=get_subfield_from_field(field["949"], "z"),
                    item_call_no=get_subfield_from_field(field["949"], "a"),
                    item_barcode=get_subfield_from_field(field["949"], "i"),
                    item_price=get_subfield_from_field(field["949"], "p"),
                    item_vendor_code=get_subfield_from_field(field["949"], "v"),
                    item_agency=get_subfield_from_field(field["949"], "h"),
                    item_location=get_subfield_from_field(field["949"], "l"),
                    item_type=get_subfield_from_field(field["949"], "t"),
                    item_volume=get_subfield_from_field(field["949"], "c"),
                    item_message=get_subfield_from_field(field["949"], "u"),
                    message=get_subfield_from_field(field["949"], "m"),
                )
            except ValidationError as e:
                validation_errors.extend(e.errors())
    return validation_errors


def validate_indiv_fields_marc(fields) -> list:
    validation_errors = []
    for field in fields:
        if field.tag == "852":
            try:
                BibCallNoModel.model_validate(
                    BibCallNo(field=field), from_attributes=True
                )
            except ValidationError as e:
                validation_errors.extend(e.errors())
        elif field.tag == "901":
            try:
                BibVendorCodeModel.model_validate(
                    BibVendorCode.from_field(field), from_attributes=True
                )
            except ValidationError as e:
                validation_errors.extend(e.errors())
        elif field.tag == "050":
            try:
                LCClassModel.model_validate(
                    LCClass.from_field(field), from_attributes=True
                )
            except ValidationError as e:
                validation_errors.extend(e.errors())
        elif field.tag == "910":
            try:
                LibraryFieldModel.model_validate(
                    Library.from_field(field), from_attributes=True
                )
            except ValidationError as e:
                validation_errors.extend(e.errors())
        elif field.tag == "960":
            try:
                OrderFieldModel.model_validate(
                    Order.from_field(field), from_attributes=True
                )
            except ValidationError as e:
                validation_errors.extend(e.errors())
        elif field.tag == "980":
            try:
                InvoiceFieldModel.model_validate(
                    Invoice.from_field(field), from_attributes=True
                )
            except ValidationError as e:
                validation_errors.extend(e.errors())
        elif field.tag == "949":
            try:
                ItemFieldModel.model_validate(
                    Item.from_field(field), from_attributes=True
                )
            except ValidationError as e:
                validation_errors.extend(e.errors())
    return validation_errors


def check_missing_fields(fields):
    validation_errors = []
    required_field_tags = ["852", "901", "050", "910", "960", "980", "949"]
    if all(isinstance(i, dict) for i in fields):
        all_fields = []
        keys = [list(i.keys()) for i in fields]
        for key in keys:
            all_fields.extend(key)
    elif all(isinstance(i, MarcField) for i in fields):
        all_fields = [i.tag for i in fields]
    else:
        all_fields = []
    for tag in required_field_tags:
        if tag not in all_fields:
            validation_errors.append(
                InitErrorDetails(
                    type=PydanticCustomError(
                        "missing_before_validation", f"Field required: {tag}"
                    ),
                    input=tag,
                )
            )
    return validation_errors


class MonographRecord(BaseModel):
    """
    A class to define a valid, full MARC record for a monograph.

    Fields marked with the annotation `Field(exclude=True)` are not included when
    serializing the model.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    leader: Annotated[
        str,
        Field(
            min_length=24,
            max_length=24,
            pattern=r"^[0-9]{5}[acdnp][acdefgijkmoprt][abcdims][\sa][\sa]22[0-9]{5}[\s12345678uz][\sacinu][\sabc]4500$",  # noqa E501
        ),
    ]
    fields: List[
        Union[
            MarcField,
            Dict[str, Union[str, Dict[str, Union[str, List[Dict[str, str]]]]]],
        ]
    ]

    @model_validator(mode="after")
    def validate_indiv_fields(self):
        fields = self.fields
        if all(isinstance(i, dict) for i in fields):
            validation_errors = validate_indiv_fields_dict(fields)
        elif all(isinstance(i, MarcField) for i in fields):
            validation_errors = validate_indiv_fields_marc(fields)
        else:
            validation_errors = []
        validation_errors.extend(check_missing_fields(fields))
        if validation_errors:
            raise ValidationError.from_exception_data(
                title=self.__class__.__name__, line_errors=validation_errors
            )
        else:
            return self
