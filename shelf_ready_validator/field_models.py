from typing import Annotated, Literal, Optional
from pydantic import BaseModel, Field


class BibCallNoModel(BaseModel):

    ind1: Literal["8"]
    ind2: Literal[" ", ""]
    call_no: Annotated[
        str, Field(pattern=r"^ReCAP 23-\d{6}$|^ReCAP 24-\d{6}$|^ReCAP 25-\d{6}$")
    ]


class BibVendorCodeModel(BaseModel):

    ind1: Literal[" ", ""]
    ind2: Literal[" ", ""]
    vendor_code: Literal["EVP", "AUXAM", "LEILA"]


class LCClassModel(BaseModel):

    ind1: Literal[" ", "0", "1"]
    ind2: Literal["0", "4"]
    lcc: str


class LibraryFieldModel(BaseModel):

    ind1: Literal[" ", ""]
    ind2: Literal[" ", ""]
    library: Literal["RL", "BL", "BPL"]


class OrderFieldModel(BaseModel):

    ind1: Literal[" ", ""]
    ind2: Literal[" ", ""]
    order_price: Annotated[str, Field(pattern=r"^\d{3,}$")]
    order_location: Literal[
        "MAB", "MAF", "MAG", "MAL", "MAP", "MAS", "PAD", "PAH", "PAM", "PAT", "SC"
    ]
    order_fund: str


class InvoiceFieldModel(BaseModel):

    ind1: Literal[" ", ""]
    ind2: Literal[" ", ""]
    invoice_date: Annotated[str, Field(pattern=r"^\d{6}$")]
    invoice_price: Annotated[str, Field(pattern=r"^\d{3,}$")]
    invoice_shipping: Annotated[str, Field(pattern=r"^\d{1,}$")]
    invoice_tax: Annotated[str, Field(pattern=r"^\d{1,}$")]
    invoice_net_price: Annotated[str, Field(pattern=r"^\d{3,}$")]
    invoice_number: str
    invoice_copies: Annotated[str, Field(pattern=r"^[0-9]+$")]


class ItemFieldModel(BaseModel):

    ind1: Literal[" ", ""]
    ind2: Literal["1"]
    item_call_tag: Annotated[Literal["8528"], Field(...)]
    item_call_no: Annotated[
        str, Field(..., pattern=r"^ReCAP 23-\d{6}$|^ReCAP 24-\d{6}$|^ReCAP 25-\d{6}$")
    ]
    item_barcode: Annotated[str, Field(..., pattern=r"^33433[0-9]{9}$")]
    item_price: Annotated[str, Field(..., pattern=r"^\d{1,}\.\d{2}$")]
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
    item_volume: Optional[str] = None
    item_type: Optional[Literal["55", "2"]] = None
