from pydantic import BaseModel, Field, ConfigDict, model_validator, ValidationError
from typing import Literal, Optional, Annotated


class Order(BaseModel):
    """
    a class to define an order record from marc 960 field
    subfields include:
        s: price (required)
        t: location code (required)
        u: fund code (required)

    """

    model_config = ConfigDict(extra="ignore", validate_default=True)

    price: Annotated[str, Field(pattern=r"^\d{3,}$")]
    location: Literal[
        "MAB", "MAF", "MAG", "MAL", "MAP", "MAS", "PAD", "PAH", "PAM", "PAT", "SC"
    ]
    fund: str  # should this follow a pattern?


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

    call_tag: Literal["8528"]
    call_no: str = Field(pattern=r"^ReCAP 23-\d{5}$")  # year is hardcoded, change this
    barcode: str = Field(pattern=r"^\d{14}$")  # how are these formatted?
    price: str = Field(pattern=r"^\d{1,}\.\d{2}$")
    volume: Optional[str] = None
    item_message: Optional[str] = None  # uppercase only?
    message: Optional[str] = None  # uppercase only?
    initials: Literal["EV", "AUXAM"]  # 3, 4, 5 digit code
    agency: Optional[str] = None
    location: Optional[str] = None
    item_type: Optional[str] = None


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

    date: str
    price: str = Field(pattern=r"^\d{3,}$")  # these prices all assume a minimum of $1
    # shipping: str = Field(pattern=r"^\d{3}$")
    # tax: str = Field(pattern=r"^\d{3}$")
    # net_price: str = Field(pattern=r"^\d{3}$")
    # invoice_number: str  # add pattern for AUX and EV invoice numbers if they have one
    # copies: str = Field(pattern=r"^\d+$")  # this allows for many copies,  change?


class BibData(BaseModel):
    """
    a class to define bib data that should be validated
    from marc fields 852, 901, 910, 050
    fields/subfields include:
        852$h: call number (required)
        901$a: vendor code (required)
        910$a: research libraries idenfier (required)
        050: lcc
    """

    model_config = ConfigDict(extra="ignore", validate_default=True)

    call_no: str = Field(pattern=r"^ReCAP 23-\d{5}$")  # year is hard coded, change this
    vendor: Literal["AUXAM", "EV"]
    rl_identifier: Literal["RL"]
    lcc: str  # add a pattern?


class Record(BaseModel):
    """
    a class to define a full record, made up of Item, Order, Invoice, and BibData
    this can then be used to validate combinations of data
    """

    item_data: Item
    order_data: Order
    invoice_data: Invoice
    bib_data: BibData

    @model_validator(mode="after")
    def check_location_combinations(self) -> "Record":
        """
        check that an instance of a Record contains a valid combination of order and item data
        """
        match self:
            case Record(
                item_data=Item(location="rcmb2", item_type="2", agency="43"),
                order_data=Order(location="MAB"),
            ):
                print("item and order combination is valid for MAB")
            case Record(
                item_data=Item(location="rcmf2", item_type="55", agency="43"),
                order_data=Order(location="MAF"),
            ):
                print("item and order combination is valid for MAF")
            case Record(
                item_data=Item(location="rcmg2", item_type="55", agency="43"),
                order_data=Order(location="MAG"),
            ):
                print("item and order combination is valid for MAG")
            case Record(
                item_data=Item(location="rc2ma", item_type="55", agency="43"),
                order_data=Order(location="MAL"),
            ):
                print("item and order combination is valid for MAL")
            case Record(
                item_data=Item(location="rcmp2", item_type="2", agency="43"),
                order_data=Order(location="MAP"),
            ):
                print("item and order combination is valid for MAP")
            case Record(
                item_data=Item(location="rcmb2", item_type="2", agency="43"),
                order_data=Order(location="MAS"),
            ):
                print("item and order combination is valid for MAS")
            case Record(
                item_data=Item(location="rcph2", item_type="55", agency="43"),
                order_data=Order(location="PAH"),
            ):
                print("item and order combination is valid for PAH")
            case Record(
                item_data=Item(location="rcpm2", item_type="55", agency="43"),
                order_data=Order(location="PAM"),
            ):
                print("item and order combination is valid for PAM")
            case Record(
                item_data=Item(location="rcpt2", item_type="55", agency="43"),
                order_data=Order(location="PAT"),
            ):
                print("item and order combination is valid for PAT")
            case Record(
                item_data=Item(location="rc2cf", item_type="55", agency="43"),
                order_data=Order(location="SC"),
            ):
                print("item and order combination is valid for SC")
            case _:
                raise ValidationError("incorrect item/order combo")
        return self
