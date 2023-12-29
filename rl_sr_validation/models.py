from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Optional


class Order(BaseModel):
    """
    a class to define an order record from marc 960 field
    subfields include:
        s: price (required)
        t: location code (required)
        u: fund code (required)

    """

    model_config = ConfigDict(extra="ignore", validate_default=True)

    price: str = Field(pattern=r"^\d{3,}$")
    location: str  # should this follow a pattern?
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
    agency: Literal["43"]


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
    price: str = Field(pattern=r"^\d{3}$")  # these prices all assume a minimum of $1
    shipping: str = Field(pattern=r"^\d{3}$")
    tax: str = Field(pattern=r"^\d{3}$")
    net_price: str = Field(pattern=r"^\d{3}$")
    invoice_number: str  # add pattern for AUX and EV invoice numbers if they have one
    copies: str = Field(pattern=r"^\d+$")  # this allows for many copies, maybe change?


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
