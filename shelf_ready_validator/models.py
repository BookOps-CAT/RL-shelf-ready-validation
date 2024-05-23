from typing import Literal, Optional, Annotated, Union, List

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    ValidationError,
    model_validator,
)
from pydantic_core import InitErrorDetails, PydanticCustomError


class ItemBPL(BaseModel):
    """
    a class to define an item record for BPL collections

    """

    model_config = ConfigDict(validate_default=True, revalidate_instances="always")

    item_call_tag: Literal["8528"]
    item_call_no: str
    item_barcode: Annotated[str, Field(pattern=r"^34444[0-9]{9}$")]
    item_price: Annotated[str, Field(pattern=r"^\d{1,}\.\d{2}$")]
    item_volume: Optional[str] = None
    item_message: Optional[str] = None
    message: Optional[str] = None
    item_vendor_code: str
    item_agency: str
    item_location: str
    item_type: str
    library: Annotated[Literal["BPL"], Field(...)]
    item_ind1: Literal[" "]
    item_ind2: Literal["1"]


class ItemNYPLBL(BaseModel):
    """
    a class to define an item record for NYPL Branch Library collections

    """

    model_config = ConfigDict(validate_default=True, revalidate_instances="always")

    item_call_tag: Literal["8528"]
    item_call_no: str
    item_barcode: Annotated[str, Field(pattern=r"^33333[0-9]{9}$")]
    item_price: Annotated[str, Field(pattern=r"^\d{1,}\.\d{2}$")]
    item_volume: Optional[str] = None
    item_message: Optional[str] = None
    message: Optional[str] = None
    item_vendor_code: str
    item_agency: str
    item_location: str
    item_type: str
    library: Annotated[Literal["BL"], Field(...)]
    item_ind1: Literal[" "]
    item_ind2: Literal["1"]


class ItemNYPLRL(BaseModel):
    """
    a class to define an item record for NYPL Research Library collections

    """

    model_config = ConfigDict(validate_default=True, revalidate_instances="always")

    item_call_tag: Annotated[Literal["8528"], Field(...)]
    item_call_no: Annotated[
        str, Field(..., pattern=r"^ReCAP 23-\d{6}$|^ReCAP 24-\d{6}$")
    ]
    item_barcode: Annotated[str, Field(..., pattern=r"^33433[0-9]{9}$")]
    item_price: Annotated[str, Field(..., pattern=r"^\d{1,}\.\d{2}$")]
    item_volume: Optional[str] = None
    item_message: Optional[Annotated[str, Field(..., pattern=r"^[^a-z]+")]] = None
    message: Optional[Annotated[str, Field(..., pattern=r"^[^a-z]+")]] = None
    item_vendor_code: Annotated[Literal["EVP", "AUXAM", "LEILA"], Field(...)]
    item_agency: Literal["43"]
    item_location: Optional[
        Literal[
            "rcmb2",
            "rcmf2",
            "rcmg2",
            "rc2ma",
            "rcmp2",
            "rcmb2",
            "rcph2",
            "rcpm2",
            "rcpt2",
            "rc2cf",
        ]
    ] = None
    item_type: Optional[Literal["55", "2"]] = None
    library: Annotated[Literal["RL"], Field(...)]
    item_ind1: Literal[" "]
    item_ind2: Literal["1"]


Item = Annotated[
    Union[ItemNYPLRL, ItemNYPLBL, ItemBPL], Field(..., discriminator="library")
]
"""
When initializing an instance of a MonographRecord, a list of items is created
The model for each Item to be validated against is selected based on the "library" field

"""


class MonographRecord(BaseModel):
    """
    A class to define a valid MARC record for monographs:
     - contains item, order and invoice data
     - order locations are only valid for shelf-ready research materials

    """

    model_config = ConfigDict(validate_default=True, revalidate_instances="always")

    material_type: Literal["monograph_record"]
    bib_call_no: Annotated[str, Field(pattern=r"^ReCAP 23-\d{6}$|^ReCAP 24-\d{6}$")]
    bib_call_no_ind1: Literal["8"]
    bib_call_no_ind2: Literal[" "]
    bib_vendor_code: Literal["EVP", "AUXAM", "LEILA"]
    lcc: str
    invoice_date: Annotated[str, Field(pattern=r"^\d{6}$")]
    invoice_price: Annotated[str, Field(pattern=r"^\d{3,}$")]
    invoice_shipping: Annotated[str, Field(pattern=r"^\d{1,}$")]
    invoice_tax: Annotated[str, Field(pattern=r"^\d{1,}$")]
    invoice_net_price: Annotated[str, Field(pattern=r"^\d{3,}$")]
    invoice_number: str
    invoice_copies: Annotated[str, Field(pattern=r"^[0-9]+$")]
    order_price: Annotated[str, Field(pattern=r"^\d{3,}$")]
    order_location: Literal[
        "MAB", "MAF", "MAG", "MAL", "MAP", "MAS", "PAD", "PAH", "PAM", "PAT", "SC"
    ]
    order_fund: str
    order_ind1: Literal[" "]
    order_ind2: Literal[" "]
    items: List[Item]

    @model_validator(mode="wrap")
    def match_locations(self, handler) -> "MonographRecord":
        """
        check MonographRecord contains a valid combination of:
         - item location
         - item type
         - order location
        """

        validation_errors = []
        order_location = self.get("order_location")
        item_list = self.get("items")
        if item_list is not None:
            item_number = 0
            for item in item_list:
                item_location = item.get("item_location")
                item_type = item.get("item_type")
                valid_types = [
                    ("rcmb2", "2", "MAB"),
                    (
                        "rcmf2",
                        "55",
                        "MAF",
                    ),
                    (
                        "rcmf2",
                        None,
                        "MAF",
                    ),
                    (
                        "rcmg2",
                        "55",
                        "MAG",
                    ),
                    (
                        "rcmg2",
                        None,
                        "MAG",
                    ),
                    (
                        "rc2ma",
                        "55",
                        "MAL",
                    ),
                    ("rc2ma", None, "MAL"),
                    (None, None, "MAL"),
                    (None, "55", "MAL"),
                    (
                        "rcmp2",
                        "2",
                        "MAP",
                    ),
                    (
                        "rcmb2",
                        "2",
                        "MAS",
                    ),
                    (
                        "rcph2",
                        "55",
                        "PAH",
                    ),
                    (
                        "rcph2",
                        None,
                        "PAH",
                    ),
                    (
                        "rcpm2",
                        "55",
                        "PAM",
                    ),
                    (
                        "rcpm2",
                        None,
                        "PAM",
                    ),
                    (
                        "rcpt2",
                        "55",
                        "PAT",
                    ),
                    (
                        "rcpt2",
                        None,
                        "PAT",
                    ),
                    (
                        "rc2cf",
                        "55",
                        "SC",
                    ),
                    (
                        "rc2cf",
                        None,
                        "SC",
                    ),
                ]
                item_group = (item_location, item_type, order_location)
                if item_group in valid_types:
                    pass
                elif None in item_group:
                    pass
                else:
                    validation_errors.append(
                        InitErrorDetails(
                            type=PydanticCustomError(
                                "Item/Order location check",
                                "Check item and order data; combination is not valid.",
                            ),
                            loc=(
                                f"{item_number}",
                                "item_location",
                                "item_type",
                                "order_location",
                            ),
                            input=(item_location, item_type, order_location),
                        ),
                    )
                item_number += 1
        try:
            # after checking item/order information, validate the model
            validated_self = handler(self)
        except ValidationError as e:
            validation_errors.extend(e.errors())

        if validation_errors:
            raise ValidationError.from_exception_data(
                title=self.__class__.__name__, line_errors=validation_errors
            )
        return validated_self


class OtherMaterialRecord(BaseModel):
    """
    a class to define a valid MARC record for non-monograph types including:
     - Catalogues Raissonnes
     - Performing Arts - Dance materials
     - Multivolume monographs
     - Pamphlets
     - Materials with non-standard binding or packaging

    """

    model_config = ConfigDict(
        extra="forbid", validate_default=True, revalidate_instances="always"
    )
    material_type: Literal[
        "catalogue_raissonne",
        "dance",
        "multipart",
        "pamphlet",
        "non-standard_binding_packaging",
    ]
    bib_vendor_code: Literal["EVP", "AUXAM", "LEILA"]
    lcc: str
    invoice_date: Annotated[str, Field(pattern=r"^\d{6}$")]
    invoice_price: Annotated[str, Field(pattern=r"^\d{3,}$")]
    invoice_shipping: Annotated[str, Field(pattern=r"^\d{1,}$")]
    invoice_tax: Annotated[str, Field(pattern=r"^\d{1,}$")]
    invoice_net_price: Annotated[str, Field(pattern=r"^\d{3,}$")]
    invoice_number: str
    invoice_copies: Annotated[str, Field(pattern=r"^[0-9]+$")]
    order_price: Annotated[str, Field(pattern=r"^\d{3,}$")]
    order_location: Literal[
        "MAB", "MAF", "MAG", "MAL", "MAP", "MAS", "PAD", "PAH", "PAM", "PAT", "SC"
    ]
    order_fund: str
    order_ind1: Literal[" "]
    order_ind2: Literal[" "]
    library: Literal["RL", "BPL", "BL"]
