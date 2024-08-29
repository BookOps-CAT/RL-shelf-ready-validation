"""This module contains pydantic models for validating vendor-provided MARC records."""

from typing import Annotated, Any, Dict, List, Literal, Union
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from pydantic_core import PydanticCustomError
from shelf_ready_validator.field_models import (
    BibCallNoModel,
    BibVendorCodeModel,
    InvoiceFieldModel,
    ItemFieldModel,
    LCClassModel,
    LibraryFieldModel,
    OrderFieldModel,
)


class MonographRecord(BaseModel):
    """
    A class to define a valid, full MARC record for a monograph.

    Fields marked with the annotation `Field(exclude=True)` are not included when
    serializing the model.
    """

    leader: Annotated[
        str,
        Field(
            min_length=24,
            max_length=24,
            pattern=r"^[0-9]{5}[acdnp][acdefgijkmoprt][abcdims][\sa][\sa]22[0-9]{5}[\s12345678uz][\sacinu][\sabc]4500$",  # noqa E501
        ),
    ]
    fields: List[Dict[str, Union[str, Dict[str, Union[str, List[Dict[str, str]]]]]]]
    bib_call_no: BibCallNoModel
    bib_vendor_code: Annotated[BibVendorCodeModel, Field(exclude=True)]
    lc_class: Annotated[Union[LCClassModel, List[LCClassModel]], Field(exclude=True)]
    library_field: Annotated[LibraryFieldModel, Field(exclude=True)]
    material_type: Annotated[Literal["monograph",], Field(exclude=True)]
    order_field: Annotated[OrderFieldModel, Field(exclude=True)]
    invoice_field: Annotated[InvoiceFieldModel, Field(exclude=True)]
    item_fields: Annotated[List[ItemFieldModel], Field(exclude=True)]

    @model_validator(mode="after")
    def validate_order_item_data(
        self: "MonographRecord",
    ) -> "MonographRecord":
        valid_combos = [
            ("MAB", "rcmb2", "2"),
            ("MAS", "rcmb2", "2"),
            ("MAF", "rcmf2", "55"),
            ("MAF", "rcmf2", None),
            ("MAG", "rcmg2", "55"),
            ("MAG", "rcmg2", None),
            ("MAL", "rc2ma", "55"),
            ("MAL", None, "55"),
            ("MAL", "rc2ma", None),
            ("MAL", None, None),
            ("MAP", "rcmp2", "2"),
            ("PAH", "rcph2", "55"),
            ("PAH", "rcph2", None),
            ("PAM", "rcpm2", "55"),
            ("PAM", "rcpm2", None),
            ("PAT", "rcpt2", "55"),
            ("PAT", "rcpt2", None),
            ("SC", "rc2cf", "55"),
            ("SC", "rc2cf", None),
        ]
        item_fields = self.item_fields
        order_field = self.order_field
        if item_fields is None or order_field is None:
            return self
        else:
            order_location = order_field.order_location
            for item in item_fields:
                combo = (order_location, item.item_location, item.item_type)
                if combo not in valid_combos:
                    raise PydanticCustomError(
                        "order_item_mismatch",
                        f"Invalid combination of item type, order "
                        f"location and item location: {combo}",
                    )
            return self

    @field_validator(
        "bib_call_no",
        "bib_vendor_code",
        "lc_class",
        "library_field",
        "order_field",
        "invoice_field",
        "item_fields",
        mode="before",
    )
    @classmethod
    def validate_missing_fields(
        cls,
        v: Union[
            BibCallNoModel,
            BibCallNoModel,
            LCClassModel,
            List[LCClassModel],
            LibraryFieldModel,
            OrderFieldModel,
            InvoiceFieldModel,
            List[ItemFieldModel],
        ],
    ) -> Any:
        if isinstance(v, list):
            if all(not item for item in v):
                raise PydanticCustomError("missing", "Field required")
        else:
            if not v:
                raise PydanticCustomError("missing", "Field required")
        return v


class OtherRecord(BaseModel):
    """
    A class to define a valid MARC record without an 852 or 949 field. This model
    should be used to validate records for catalogues taissonnes, pamphlets,
    multi-volume works, works with non-standard binding/packaging, and dance
    materials. Extra fields will be flagged as errors.

    Fields marked with the annotation `Field(exclude=True)` are not included when
    serializing the model.
    """

    model_config = ConfigDict(extra="forbid")

    leader: Annotated[
        str,
        Field(
            min_length=24,
            max_length=24,
            pattern=r"^[0-9]{5}[acdnp][acdefgijkmoprt][abcdims][\sa][\sa]22[0-9]{5}[\s12345678uz][\sacinu][\sabc]4500$",  # noqa E501
        ),
    ]
    fields: List[Dict[str, Union[str, Dict[str, Union[str, List[Dict[str, str]]]]]]]
    bib_vendor_code: Annotated[BibVendorCodeModel, Field(exclude=True)]
    lc_class: Annotated[Union[LCClassModel, List[LCClassModel]], Field(exclude=True)]
    library_field: Annotated[LibraryFieldModel, Field(exclude=True)]
    material_type: Annotated[
        Literal[
            "catalogue_raissonne",
            "dance",
            "multipart",
            "pamphlet",
            "non-standard_binding_packaging",
        ],
        Field(exclude=True),
    ]
    order_field: Annotated[OrderFieldModel, Field(exclude=True)]
    invoice_field: Annotated[InvoiceFieldModel, Field(exclude=True)]
