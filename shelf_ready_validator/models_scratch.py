from typing import Annotated, Union, List, Dict, Literal
from enum import Enum
from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    AliasPath,
    AliasGenerator,
    Tag,
    Discriminator,
)
from shelf_ready_validator.field_models import (
    ItemPrice,
    ItemCallNo,
    ItemVendorCode,
    ItemAgency,
    ItemBarcode,
    ItemLocation,
    ItemCallTag,
    ItemType,
    BibCallNo,
)


def serialize_with_tag(tag: str, data: dict) -> dict:
    if tag in RequiredVendorMarcFields:
        return {RequiredVendorMarcFields(tag).value: data}
    else:
        return data


def get_union_type(v: dict) -> str:
    for key, value in v.items():
        if key in RequiredVendorMarcFields:
            return RequiredVendorMarcFields(key).value
        elif key in MarcControlFields:
            return MarcControlFields(key).value
    return "GenericDataField"


class MarcControlFields(Enum):
    Marc001 = "001"
    Marc003 = "003"
    Marc005 = "005"
    Marc006 = "006"
    Marc007 = "007"
    Marc008 = "008"


class RequiredVendorMarcFields(Enum):
    BibCallNo = "852"
    ItemField = "949"
    OrderField = "960"
    LCC = "050"
    LCCN = "010"
    ISBN = "020"
    InvoiceField = "980"


class OtherMarcFields(Enum):
    Marc035 = "035"
    Marc040 = "040"
    Marc041 = "041"
    Marc042 = "042"
    Marc043 = "043"
    Marc049 = "049"
    Marc100 = "100"
    Marc110 = "110"
    Marc111 = "111"
    Marc130 = "130"
    Marc245 = "245"
    Marc246 = "246"
    Marc250 = "250"
    Marc264 = "264"
    Marc300 = "300"
    Marc336 = "336"
    Marc337 = "337"
    Marc338 = "338"
    Marc500 = "500"
    Marc504 = "504"
    Marc505 = "505"
    Marc506 = "506"
    Marc520 = "520"
    Marc538 = "538"
    Marc546 = "546"
    Marc588 = "588"
    Marc600 = "600"
    Marc650 = "650"
    Marc651 = "651"
    Marc655 = "655"
    Marc700 = "700"
    Marc710 = "710"
    Marc730 = "730"
    Marc740 = "740"
    Marc752 = "752"
    Marc856 = "856"
    Marc900 = "900"
    Marc901 = "901"
    Marc910 = "910"
    Marc920 = "920"
    Marc981 = "981"
    Marc994 = "994"


class Field001(BaseModel):
    """A class to define a valid MARC 001 Control Field"""

    tag: Annotated[str, Field(alias="001")]


class Field003(BaseModel):
    """A class to define a valid MARC 003 Control Field"""

    tag: Annotated[str, Field(alias="003")]


class Field005(BaseModel):
    """A class to define a valid MARC 005 Control Field"""

    tag: Annotated[str, Field(alias="005", pattern=r"^\d{14}\.\d$")]


class Field007(BaseModel):
    """A class to define a valid MARC 007 Control Field"""

    tag: Annotated[str, Field(alias="007")]


class Field008(BaseModel):
    """A class to define a valid MARC 008 Control Field"""

    tag: Annotated[str, Field(alias="008", min_length=40, max_length=40)]


class Field010(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=lambda field_name: AliasPath("010", field_name),
        )
    )
    ind1: Literal[" "]
    ind2: Literal[" "]
    subfields: List[Dict[Annotated[str, Field(pattern=r"^[abz8]$")], str]]


class Field020(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=lambda field_name: AliasPath("020", field_name),
        )
    )

    ind1: Literal[" "]
    ind2: Literal[" "]
    subfields: List[Dict[Annotated[str, Field(pattern=r"^[acqz68]$")], str]]


class Field050(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=lambda field_name: AliasPath("050", field_name),
        )
    )

    ind1: Literal[" ", "1", "0"]
    ind2: Literal["0", "4"]
    subfields: List[Dict[Annotated[str, Field(pattern=r"^[ab01368]$")], str]]


class Field852(BaseModel):

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=lambda field_name: AliasPath("852", field_name),
        )
    )

    ind1: Literal["8"]
    ind2: Literal[" "]
    subfields: List[Union[BibCallNo, Dict[Annotated[str, Field(pattern=r"[^h]")], str]]]


class Field901(BaseModel):

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=lambda field_name: AliasPath("901", field_name),
        )
    )

    ind1: Literal[" "]
    ind2: Literal[" "]
    subfields: List[
        Union[
            Dict[Literal["a"], Literal["EVP", "AUXAM", "LEILA"]],
            Dict[Annotated[str, Field(pattern=r"^[^a]$")], str],
        ]
    ]


class Field910(BaseModel):
    """A class to define a valid MARC 050 Field"""

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=lambda field_name: AliasPath("910", field_name),
        )
    )

    ind1: Literal[" "]
    ind2: Literal[" "]
    subfields: List[
        Union[
            Dict[Literal["a"], Literal["RL", "BL", "BPL"]],
            Dict[Annotated[str, Field(pattern=r"^[^a]$")], str],
        ]
    ]


class Field949(BaseModel):
    """A class to define a valid MARC 050 Field"""

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=lambda field_name: AliasPath("949", field_name),
        )
    )

    ind1: Literal[" "]
    ind2: Literal["1"]
    subfields: List[
        Union[
            ItemPrice,
            ItemCallNo,
            ItemVendorCode,
            ItemAgency,
            ItemBarcode,
            ItemLocation,
            ItemCallTag,
            ItemType,
        ]
    ]


class Field960(BaseModel):
    """A class to define a valid MARC 050 Field"""

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=lambda field_name: AliasPath("960", field_name),
        )
    )

    ind1: Literal[" "]
    ind2: Literal[" "]
    subfields: List[
        Union[
            Annotated[Dict[Literal["u"], str], Field(description="Order Fund")],
            Annotated[
                Dict[Literal["s"], Annotated[str, Field(pattern=r"^\d{3,}$")]],
                Field(description="Order Price"),
            ],
            Annotated[
                Dict[
                    Literal["t"],
                    Literal[
                        "MAB",
                        "MAF",
                        "MAG",
                        "MAL",
                        "MAP",
                        "MAS",
                        "PAD",
                        "PAH",
                        "PAM",
                        "PAT",
                        "SC",
                    ],
                ],
                Field(description="Order Location"),
            ],
            Dict[Annotated[str, Field(pattern=r"[^stu]")], str],
        ]
    ]


class Field980(BaseModel):
    """A class to define a valid MARC 050 Field"""

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=lambda field_name: AliasPath("980", field_name),
        )
    )

    ind1: Literal[" "]
    ind2: Literal[" "]
    subfields: List[
        Union[
            Annotated[
                Dict[Literal["a"], Annotated[str, Field(pattern=r"^\d{6}$")]],
                Field(description="Invoice Date"),
            ],
            Annotated[
                Dict[Literal["b"], Annotated[str, Field(pattern=r"^\d{3,}$")]],
                Field(description="Invoice Price"),
            ],
            Annotated[
                Dict[Literal["c"], Annotated[str, Field(pattern=r"^\d{1,}$")]],
                Field(description="Invoice Shipping"),
            ],
            Annotated[
                Dict[Literal["d"], Annotated[str, Field(pattern=r"^\d{1,}$")]],
                Field(description="Invoice Tax"),
            ],
            Annotated[
                Dict[Literal["e"], Annotated[str, Field(pattern=r"^\d{3,}$")]],
                Field(description="Invoice Net Price"),
            ],
            Annotated[Dict[Literal["f"], str], Field(description="Invoice Number")],
            Annotated[
                Dict[Literal["g"], Annotated[str, Field(pattern=r"^[0-9]+$")]],
                Field(description="Invoice Copies"),
            ],
        ]
    ]


class GenericDataField(BaseModel):
    """A class to define a generic, valid MARC data field"""

    ind1: str
    ind2: str
    subfields: List[Dict]


class VendorRecordModel(BaseModel):
    """A class to define a generic, valid MARC record"""

    leader: Annotated[
        str,
        Field(
            min_length=24,
            max_length=24,
            pattern=r"^[0-9]{5}[acdnp][acdefgijkmoprt][abcdims][\sa][\sa]22[0-9]{5}[\s12345678uz][\sacinu][\sabc]4500$",  # noqa E501
        ),
    ]
    fields: List[
        Annotated[
            Union[
                Annotated[Field001, Tag("001")],
                Annotated[Field003, Tag("003")],
                Annotated[Field005, Tag("005")],
                Annotated[Field007, Tag("007")],
                Annotated[Field008, Tag("008")],
                Annotated[Field010, Tag("010")],
                Annotated[Field020, Tag("020")],
                Annotated[Field050, Tag("050")],
                Annotated[Field852, Tag("852")],
                Annotated[Field949, Tag("949")],
                Annotated[Field960, Tag("960")],
                Annotated[Field980, Tag("980")],
                Annotated[Dict[str, GenericDataField], Tag("GenericDataField")],
            ],
            Discriminator(get_union_type),
        ],
    ]


class GenericVendorRecord(BaseModel):
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
    field_852: Dict[str, Union[str, Dict[str, Union[str, List[Dict[str, str]]]]]]
    field_949: Dict[str, Union[str, Dict[str, Union[str, List[Dict[str, str]]]]]]
