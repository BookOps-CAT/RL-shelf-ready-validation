from pydantic import BaseModel, Field, ConfigDict, model_validator, ValidationError
from typing import Literal, Optional, Annotated
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
    order_fund: str  # should this follow a pattern?


class Item(BaseModel):
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

    item_call_tag: Literal["8528"]
    item_call_no: str = Field(
        pattern=r"^ReCAP 23-\d{6}$|^ReCAP 24-\d{6}$"
    )  # year is hardcoded, change this
    item_barcode: str = Field(pattern=r"^\d{14}$")  # how are these formatted?
    item_price: str = Field(pattern=r"^\d{1,}\.\d{2}$")
    item_volume: Optional[str] = None
    item_message: Optional[str] = None  # uppercase only?
    message: Optional[str] = None  # uppercase only?
    item_vendor_code: Literal["EVIS", "AUXAM"]  # 3, 4, 5 digit code
    item_agency: str
    item_location: str
    item_type: str


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

    invoice_date: str = Field(pattern=r"^\d{6}$")
    invoice_price: str = Field(pattern=r"^\d{3,}$")
    invoice_shipping: str = Field(pattern=r"^\d{1,}$")
    invoice_tax: str = Field(pattern=r"^\d{1,}$")
    invoice_net_price: str = Field(pattern=r"^\d{3,}$")
    invoice_number: str  # add pattern for AUX and EV invoice numbers if they have one
    invoice_copies: str = Field(pattern=r"^\d+$")


# class Bib(BaseModel):
#     """
#     a class to define bib data that should be validated
#     from marc fields 852, 901, 910, 050
#     fields/subfields include:
#         852$h: call number (required)
#         901$a: vendor code (required)
#         910$a: research libraries idenfier (required)
#         050: lcc
#     """


class Record(BaseModel):
    """
    a class to define a MARC record, made up of Item, Order, Invoice, and BibData
    this can then be used to validate combinations of data
    """

    model_config = ConfigDict(extra="ignore", validate_default=True)

    bib_call_no: str = Field(pattern=r"^ReCAP 23-\d{6}$|^ReCAP 24-\d{6}$")
    bib_vendor_code: Literal["AUXAM", "EVP"]
    rl_identifier: Literal["RL"]
    lcc: str  # create an actual pattern
    # is $a enough to confirm location correlation?

    item: Item
    order: Order
    invoice: Invoice

    @model_validator(mode="wrap")
    def match_locations(self, handler) -> "Record":
        """
        confirm that an instance of a Record contains a valid combination of:
         - item location
         - item type
         - order location

         # are there other fields that need to be validated in this way?
        """
        validation_errors = []
        item_location = self.get("item").get("item_location")
        item_type = self.get("item").get("item_type")
        order_location = self.get("order").get("order_location")

        match (item_location, item_type, order_location):
            case ("rcmb2", "2", "MAB") | ("rcmf2", "55", "MAF") | (
                "rcmg2",
                "55",
                "MAG",
            ) | ("rc2ma", "55", "MAL") | ("rcmp2", "2", "MAP") | (
                "rcmb2",
                "2",
                "MAS",
            ) | (
                "rcph2",
                "55",
                "PAH",
            ) | (
                "rcpm2",
                "55",
                "PAM",
            ) | (
                "rcpt2",
                "55",
                "PAT",
            ) | (
                "rc2cf",
                "55",
                "SC",
            ):
                print("Valid item_location/item_type/order_location combo")
            case (None, *_):
                validation_errors.append(
                    InitErrorDetails(
                        type=PydanticCustomError(
                            "location_test",
                            "could not check item_location, item_type, and order_location combination because item_location is missing",
                        ),
                        loc=("item", "item_location"),
                        input=(self.get("item")),
                    )
                )
            case (item_location, None, *_):
                validation_errors.append(
                    InitErrorDetails(
                        type=PydanticCustomError(
                            "location_test",
                            "could not check item_location, item_type, and order_location combination because item_type is missing",
                        ),
                        loc=("item", "item_location"),
                        input=(self.get("item")),
                    )
                )
            case (item_location, item_type, None):
                validation_errors.append(
                    InitErrorDetails(
                        type=PydanticCustomError(
                            "location_test",
                            "could not check item_location, item_type, and order_location combination because order_location is missing",
                        ),
                        loc=("order", "order_location"),
                        input=(self.get("order")),
                    )
                )
            case _:
                validation_errors.append(
                    InitErrorDetails(
                        type=PydanticCustomError(
                            "location_test",
                            "item_location, item_type, and order_location are not a valid combination",
                        ),
                        loc=("item_location", "item_type", "order_location"),
                        input=(self),
                    )
                )
        try:
            # validate the model
            validated_self = handler(self)
        except ValidationError as e:
            validation_errors.extend(e.errors())

        if validation_errors:
            raise ValidationError.from_exception_data(
                title=self.__class__.__name__, line_errors=validation_errors
            )
        return validated_self
