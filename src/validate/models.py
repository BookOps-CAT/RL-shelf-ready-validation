from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    model_validator,
    ValidationError,
)
from typing import Literal, Optional, Annotated, Union
from pydantic_core import InitErrorDetails, PydanticCustomError


class Order(BaseModel):
    """
    a class to define an order record from marc 960 field
    subfields include:
        s: price (required)
        t: location code (required)
        u: fund code (required)
    """

    model_config = ConfigDict(extra="ignore", validate_default=True)

    order_price: Annotated[str, Field(pattern=r"^\d{3,}$")]
    order_location: Literal[
        "MAB", "MAF", "MAG", "MAL", "MAP", "MAS", "PAD", "PAH", "PAM", "PAT", "SC"
    ]
    order_fund: str


class ItemRequired(BaseModel):
    """
    a class to define an item record from marc 949 field
    subfields include:
        z: call tag (required for general account)
        a: call number (required)
        i: barcode (required)
        p: price with decimal (required)
        c: volume number (required for multivolume works)
        u: item message (optional)
        m: message (optional)
        v: initials (required)
        h: agency (required)
        l: location (required)
        t: item type (required)
    """

    model_config = ConfigDict(extra="ignore", validate_default=True)

    material_type: Literal["monograph_record"]
    item_call_tag: Literal["8528"]
    item_call_no: Annotated[str, Field(pattern=r"^ReCAP 23-\d{6}$|^ReCAP 24-\d{6}$")]
    item_barcode: Annotated[
        str, Field(pattern=r"^33433[0-9]{9}$|^33333[0-9]{9}$|^34444[0-9]{9}$")
    ]
    item_price: Annotated[str, Field(pattern=r"^\d{1,}\.\d{2}$")]
    item_volume: Optional[str] = None
    item_message: Optional[Annotated[str, Field(pattern=r"^[^a-z]+")]] = None
    message: Optional[Annotated[str, Field(pattern=r"^[^a-z]+")]] = None
    item_vendor_code: Literal["EVP", "AUXAM"]
    item_agency: str
    item_location: Literal[
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
    item_type: str


class ItemNotRequired(BaseModel):
    """
    a class to define an item if the material type does not require one
    MARC record should not have a 949 field
    """

    model_config = ConfigDict(extra="forbid", validate_default=True)
    material_type: Literal[
        "catalogue_raissonne",
        "performing_arts_dance",
        "multipart",
        "incomplete_set",
        "pamphlet",
        "non-standard_binding_packaging",
    ]


class Invoice(BaseModel):
    """
    a class to define an invoice record from marc 980 field
    subfields include:
        a: invoice date (required)
        b: list price (required)
        c: shipping cost (required)
        d: sales tax
        e: net ammount (required)
        f: invoice number (required)
        g: number of copies (required)
    """

    model_config = ConfigDict(extra="ignore", validate_default=True)

    invoice_date: Annotated[str, Field(pattern=r"^\d{6}$")]
    invoice_price: Annotated[str, Field(pattern=r"^\d{3,}$")]
    invoice_shipping: Annotated[str, Field(pattern=r"^\d{1,}$")]
    invoice_tax: Annotated[str, Field(pattern=r"^\d{1,}$")]
    invoice_net_price: Annotated[str, Field(pattern=r"^\d{3,}$")]
    invoice_number: str
    invoice_copies: Annotated[str, Field(pattern=r"^[0-9]+$")]


class Record(BaseModel):
    """
    a class to define a MARC record, made up of Item, Order, and Invoice models
    with additional bibliographic data
    """

    model_config = ConfigDict(extra="ignore", validate_default=True)

    bib_call_no: Optional[
        Annotated[str, Field(pattern=r"^ReCAP 23-\d{6}$|^ReCAP 24-\d{6}$")]
    ] = None
    bib_vendor_code: Literal["AUXAM", "EVP"]
    rl_identifier: Literal["RL"]
    lcc: str

    item: Union[ItemRequired, ItemNotRequired] = Field(
        ..., discriminator="material_type"
    )
    order: Order
    invoice: Invoice

    @model_validator(mode="wrap")
    def match_locations(self, handler) -> "Record":
        """
        confirm that an instance of a Record contains a valid combination of:
         - material type
         - item location
         - item type
         - order location
        """
        validation_errors = []
        material_type = self.get("item").get("material_type")
        item_location = self.get("item").get("item_location")
        item_type = self.get("item").get("item_type")
        order_location = self.get("order").get("order_location")
        match (material_type, item_location, item_type, order_location):
            case ("monograph_record", "rcmb2", "2", "MAB") | (
                "monograph_record",
                "rcmf2",
                "55",
                "MAF",
            ) | (
                "monograph_record",
                "rcmg2",
                "55",
                "MAG",
            ) | (
                "monograph_record",
                "rc2ma",
                "55",
                "MAL",
            ) | (
                "monograph_record",
                "rcmp2",
                "2",
                "MAP",
            ) | (
                "monograph_record",
                "rcmb2",
                "2",
                "MAS",
            ) | (
                "monograph_record",
                "rcph2",
                "55",
                "PAH",
            ) | (
                "monograph_record",
                "rcpm2",
                "55",
                "PAM",
            ) | (
                "monograph_record",
                "rcpt2",
                "55",
                "PAT",
            ) | (
                "monograph_record",
                "rc2cf",
                "55",
                "SC",
            ):
                pass
            case ("monograph_record", None, *_):
                validation_errors.append(
                    InitErrorDetails(
                        type=PydanticCustomError(
                            "Item/Order location check",
                            "Could not compare Item and Order records because item_location is missing.",
                        ),
                        loc=("item", "item_location"),
                        input=(self.get("item")),
                    )
                )
            case ("monograph_record", item_location, None, *_):
                validation_errors.append(
                    InitErrorDetails(
                        type=PydanticCustomError(
                            "Item/Order location check",
                            "Could not compare Item and Order records because item_type is missing.",
                        ),
                        loc=("item", "item_location"),
                        input=(self.get("item")),
                    )
                )
            case ("monograph_record", item_location, item_type, None):
                validation_errors.append(
                    InitErrorDetails(
                        type=PydanticCustomError(
                            "Item/Order location check",
                            "Could not compare Item and Order records because order_location is missing.",
                        ),
                        loc=("order", "order_location"),
                        input=(self.get("order")),
                    )
                )
            case (
                "catalog_raissonne"
                | "performing_arts_dance"
                | "multipart"
                | "incomplete_set"
                | "pamphlet"
                | "non-standard_binding_packaging",
                *_,
            ):
                pass
            case _:
                validation_errors.append(
                    InitErrorDetails(
                        type=PydanticCustomError(
                            "Item/Order location check",
                            "(item_location, item_type, order_location) combination is not valid.",
                        ),
                        loc=("item_location", "item_type", "order_location"),
                        input=(
                            self.get("item").get("item_location"),
                            self.get("item").get("item_type"),
                            self.get("order").get("order_location"),
                        ),
                    )
                )
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

    @model_validator(mode="after")
    def check_required_call_no(self) -> "Record":
        """
        check material type of instance of Record
        confirm it has a call_no if necessary
        """
        validation_errors = []
        bib_call_no = self.bib_call_no
        material_type = self.item.material_type
        match (material_type, bib_call_no):
            case ("monograph_record", None):
                validation_errors.append(
                    InitErrorDetails(
                        type=PydanticCustomError(
                            "call_no_missing",
                            "record for this material type should have a call_no",
                        ),
                        loc=("material_type", "bib_call_no"),
                        input=(self.get("item")),
                    )
                )
            case (
                "catalog_raissonne"
                | "performing_arts_dance"
                | "multipart"
                | "incomplete_set"
                | "pamphlet"
                | "non-standard_binding_packaging",
                None,
            ):
                pass
            case (
                "catalog_raissonne"
                | "performing_arts_dance"
                | "multipart"
                | "incomplete_set"
                | "pamphlet"
                | "non-standard_binding_packaging",
                *_,
            ):
                validation_errors.append(
                    InitErrorDetails(
                        type=PydanticCustomError(
                            "call_no_test",
                            "records for this material type should not have a call_no",
                        ),
                        loc=("material_type", "bib_call_no"),
                        input=(self),
                    )
                )
            case _:
                validation_errors.append(
                    InitErrorDetails(
                        type=PydanticCustomError(
                            "call_no_test",
                            "something is wrong with call_no/material_type combination",
                        ),
                        loc=("material_type", "bib_call_no"),
                        input=(self),
                    )
                )
        return self
