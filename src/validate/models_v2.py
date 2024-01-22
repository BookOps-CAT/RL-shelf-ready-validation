from pydantic import BaseModel, Field, ConfigDict, ValidationError
from typing import Any, Literal, Optional, Annotated, Union, List


class ItemBPL(BaseModel):
    """
    a class to define an item record for BPL collections

    """

    model_config = ConfigDict(
        extra="ignore", validate_default=True, revalidate_instances="always"
    )

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
    library: Literal["BPL"]


class ItemNYPLBL(BaseModel):
    """
    a class to define an item record for NYPL Branch Library collections

    """

    model_config = ConfigDict(
        extra="ignore", validate_default=True, revalidate_instances="always"
    )

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
    library: Literal["BL"]


class ItemNYPLRL(BaseModel):
    """
    a class to define an item record for NYPL Research Library collections

    """

    model_config = ConfigDict(
        extra="ignore", validate_default=True, revalidate_instances="always"
    )

    item_call_tag: Annotated[Literal["8528"], Field(...)]
    item_call_no: Annotated[
        str, Field(..., pattern=r"^ReCAP 23-\d{6}$|^ReCAP 24-\d{6}$")
    ]
    item_barcode: Annotated[str, Field(..., pattern=r"^33433[0-9]{9}$")]
    item_price: Annotated[str, Field(..., pattern=r"^\d{1,}\.\d{2}$")]
    item_volume: Optional[str] = None
    item_message: Optional[Annotated[str, Field(..., pattern=r"^[^a-z]+")]] = None
    message: Optional[Annotated[str, Field(..., pattern=r"^[^a-z]+")]] = None
    item_vendor_code: Annotated[Literal["EVP", "AUXAM"], Field(...)]
    item_agency: str = Field(...)
    item_location: Annotated[
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
        ],
        Field(...),
    ]
    item_type: str = Field(...)
    library: Annotated[Literal["RL"], Field(...)]


Item = Annotated[
    Union[ItemNYPLRL, ItemNYPLBL, ItemBPL], Field(..., discriminator="library")
]


class MonographRecord(BaseModel):
    """
    a class to define a MARC record, made up of Item, Order, and Invoice models
    with additional bibliographic data
    """

    model_config = ConfigDict(
        extra="ignore", validate_default=True, revalidate_instances="always"
    )

    material_type: Literal["monograph_record"]
    bib_call_no: Annotated[str, Field(pattern=r"^ReCAP 23-\d{6}$|^ReCAP 24-\d{6}$")]
    bib_vendor_code: Literal["EVP", "AUXAM"]
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
    items: List[Item]


class OtherMaterialRecord(BaseModel):
    """
    a class to define a MARC record, made up of Item, Order, and Invoice models
    with additional bibliographic data
    """

    model_config = ConfigDict(
        extra="forbid", validate_default=True, revalidate_instances="always"
    )
    material_type: Literal[
        "catalogue_raissonne",
        "performing_arts_dance",
        "multipart",
        "pamphlet",
        "non-standard_binding_packaging",
    ]
    bib_vendor_code: Literal["EVP", "AUXAM"]
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


# RecordType = Annotated[
#     Union[MonographRecord, OtherMaterialRecord],
#     Field(discriminator="material_type"),
# ]


# class Record(BaseModel):
#     record_type: RecordType
#     library: Literal["BPL", "RL", "BL"]
