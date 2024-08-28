from typing import Annotated, Any, Union, List, Dict, Literal, Optional
from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError


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


class OrderItem(BaseModel):
    order_location: Literal[
        "MAB", "MAF", "MAG", "MAL", "MAP", "MAS", "PAD", "PAH", "PAM", "PAT", "SC"
    ]
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


class VendorMonographRecordModel(BaseModel):
    """A class to define a generic, valid MARC record"""

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
    bib_vendor_code: BibVendorCodeModel
    lc_class: Union[LCClassModel, List[LCClassModel]]
    library_field: LibraryFieldModel
    material_type: Literal["monograph"]
    order_field: OrderFieldModel
    invoice_field: InvoiceFieldModel
    item_fields: List[ItemFieldModel]
    order_item_data: List[OrderItem]

    # order_item_data: List[
    #     Annotated[
    #         Union[
    #             MABMASOrderItem,
    #             MAFOrderItem,
    #             MAGOrderItem,
    #             MALOrderItem,
    #             MAPOrderItem,
    #             PAHOrderItem,
    #             PAMOrderItem,
    #             PATOrderItem,
    #             SCOrderItem,
    #         ],
    #         Field(discriminator="order_loc"),
    #     ],
    # ]

    @field_validator("order_item_data", mode="after")
    @classmethod
    def validate_order_item_data(cls, v: List[OrderItem]) -> List[OrderItem]:
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
        for combo in v:
            if (
                combo.order_location,
                combo.item_location,
                combo.item_type,
            ) not in valid_combos:
                raise PydanticCustomError(
                    "order_item_location",
                    f"Invalid combination of item type, order "
                    f"location and item location: {combo}",
                )
        return v

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


class VendorOtherRecordModel(BaseModel):
    """A class to define a generic, valid MARC record"""

    leader: Annotated[
        str,
        Field(
            min_length=24,
            max_length=24,
            pattern=r"^[0-9]{5}[acdnp][acdefgijkmoprt][abcdims][\sa][\sa]22[0-9]{5}[\s12345678uz][\sacinu][\sabc]4500$",  # noqa E501
        ),
    ]
    fields: List[Dict[str, Union[str, Dict[str, Union[str, List[Dict[str, str]]]]]]]
    bib_vendor_code: BibVendorCodeModel
    lc_class: LCClassModel
    library_field: LibraryFieldModel
    material_type: Literal[
        "catalogue_raissonne",
        "dance",
        "multipart",
        "pamphlet",
        "non-standard_binding_packaging",
    ]
    order_field: OrderFieldModel
    invoice_field: InvoiceFieldModel
