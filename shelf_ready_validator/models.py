from typing import Literal, Optional, Annotated, Union, List, TypeVar, Generic

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    ValidationError,
    model_validator,
    TypeAdapter,
    Tag,
    Discriminator,
)
from pydantic_core import InitErrorDetails, PydanticCustomError
from pymarc import Record
from shelf_ready_validator.utils import material_type_validator

RecordT = TypeVar("RecordT")


class VendorRecord(BaseModel, Generic[RecordT]):
    material_type: Optional[RecordT] = None
    bib_call_no: Optional[RecordT] = None
    bib_vendor_code: Optional[RecordT] = None
    lcc: Optional[RecordT] = None
    invoice_date: Optional[RecordT] = None
    invoice_price: Optional[RecordT] = None
    invoice_shipping: Optional[RecordT] = None
    invoice_tax: Optional[RecordT] = None
    invoice_net_price: Optional[RecordT] = None
    invoice_number: Optional[RecordT] = None
    invoice_copies: Optional[RecordT] = None
    order_price: Optional[RecordT] = None
    order_location: Optional[RecordT] = None
    order_fund: Optional[RecordT] = None
    order_indicators: Optional[RecordT] = None
    library: Optional[RecordT] = None
    items: Optional[RecordT] = None

    @staticmethod
    def get_material_type(record: Record) -> str:
        """
        Reads record data to determine material type
        Validator chooses model to validate against based on material type

        this function needs to be built out more
        """
        subjects = record.subjects
        subject_subfield_v = []
        for subject in subjects:
            subfield_v = subject.get_subfields("v")
            subject_subfield_v.append(subfield_v)
        subject_subfield_list = [
            item for listed in subject_subfield_v for item in listed
        ]
        physical_desc = record.physicaldescription
        field_300a = physical_desc[0].get_subfields("a")
        split_300a = field_300a[0].split()
        if "Catalogues Raisonnes" in subject_subfield_list:
            return "catalogue_raissonne"
        elif "Catalogue Raissonne" in subject_subfield_list:
            return "catalogue_raissonne"
        elif "volumes" in split_300a[1]:
            return "multipart"
        elif "pages" in split_300a[1]:
            try:
                pages = int(split_300a[0])
                if pages < 50:
                    return "pamphlet"
                else:
                    return "monograph_record"
            except ValueError:
                return "monograph_record"
        else:
            return "monograph_record"

    @staticmethod
    def get_pymarc_data(
        marc_record: Record, field: str, subfield: Optional[str] = None
    ) -> Union[str, None]:
        """
        Gets value of field or field/subfield pair. Returns a None if field
        and/or subfield does not exist
        """
        try:
            if subfield:
                field_subfield_value = marc_record[field][subfield]
                return field_subfield_value
            else:
                field_value = str(marc_record[field])
                return field_value
        except KeyError:
            return None

    @classmethod
    def from_marc(cls, record: Record):
        return cls(
            material_type=cls.get_material_type(record),
            bib_call_no=cls.get_pymarc_data(marc_record=record, field="852")[1:],
            bib_vendor_code=cls.get_pymarc_data(
                marc_record=record, field="901", subfield="a"
            ),
            lcc=cls.get_pymarc_data(marc_record=record, field="050", subfield="a"),
            invoice_date=cls.get_pymarc_data(
                marc_record=record, field="980", subfield="a"
            ),
            invoice_price=cls.get_pymarc_data(
                marc_record=record, field="980", subfield="b"
            ),
            invoice_shipping=cls.get_pymarc_data(
                marc_record=record, field="980", subfield="c"
            ),
            invoice_tax=cls.get_pymarc_data(
                marc_record=record, field="980", subfield="d"
            ),
            invoice_net_price=cls.get_pymarc_data(
                marc_record=record, field="980", subfield="e"
            ),
            invoice_number=cls.get_pymarc_data(
                marc_record=record, field="980", subfield="f"
            ),
            invoice_copies=cls.get_pymarc_data(
                marc_record=record, field="980", subfield="g"
            ),
            order_price=cls.get_pymarc_data(
                marc_record=record, field="960", subfield="s"
            ),
            order_location=cls.get_pymarc_data(
                marc_record=record, field="960", subfield="t"
            ),
            order_fund=cls.get_pymarc_data(
                marc_record=record, field="960", subfield="u"
            ),
            order_indicators=cls.get_pymarc_data(marc_record=record, field="960")[6:8],
            library=cls.get_pymarc_data(marc_record=record, field="910", subfield="a"),
            items=[
                {
                    "item_call_tag": cls.get_pymarc_data(
                        marc_record=record, field=i, subfield="z"
                    ),
                    "item_call_no": cls.get_pymarc_data(
                        marc_record=record, field=i, subfield="a"
                    ),
                    "item_barcode": cls.get_pymarc_data(
                        marc_record=record, field=i, subfield="i"
                    ),
                    "item_price": cls.get_pymarc_data(
                        marc_record=record, field=i, subfield="p"
                    ),
                    "item_vendor_code": cls.get_pymarc_data(
                        marc_record=record, field=i, subfield="v"
                    ),
                    "item_agency": cls.get_pymarc_data(
                        marc_record=record, field=i, subfield="h"
                    ),
                    "item_location": cls.get_pymarc_data(
                        marc_record=record, field=i, subfield="l"
                    ),
                    "item_type": cls.get_pymarc_data(
                        marc_record=record, field=i, subfield="t"
                    ),
                    "library": cls.get_pymarc_data(
                        marc_record=record, field="910", subfield="a"
                    ),
                    "item_indicators": cls.get_pymarc_data(marc_record=record, field=i)[
                        6:8
                    ],
                }
                for i in record
                if i == "949"
            ],
        )


class ItemNYPLRL(BaseModel):
    """
    a class to define an item record for NYPL Research Library collections

    """

    model_config = ConfigDict(validate_default=True, revalidate_instances="always")

    item_call_tag: Annotated[Literal["8528"], Field(..., serialization_alias="949$z")]
    item_call_no: Annotated[
        str,
        Field(
            ...,
            pattern=r"^ReCAP 23-\d{6}$|^ReCAP 24-\d{6}$",
            serialization_alias="949$a",
        ),
    ]
    item_barcode: Annotated[
        str, Field(..., pattern=r"^33433[0-9]{9}$", serialization_alias="949$i")
    ]
    item_price: Annotated[
        str, Field(..., pattern=r"^\d{1,}\.\d{2}$", serialization_alias="949$p")
    ]
    item_volume: Annotated[
        Optional[str], Field(default=None, serialization_alias="949$c")
    ]
    item_message: Annotated[
        Optional[str], Field(default=None, serialization_alias="949$u")
    ]
    message: Annotated[Optional[str], Field(default=None, serialization_alias="949$m")]
    item_vendor_code: Annotated[
        Literal["EVP", "AUXAM", "LEILA"], Field(..., serialization_alias="949$v")
    ]
    item_agency: Annotated[Literal["43"], Field(serialization_alias="949$h")]
    item_location: Annotated[
        Optional[
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
        ],
        Field(default=None, serialization_alias="949$l"),
    ]
    item_type: Annotated[
        Optional[Literal["55", "2"]], Field(default=None, serialization_alias="949$t")
    ]
    library: Annotated[Literal["RL"], Field(..., serialization_alias="910$a")]
    item_indicators: Annotated[
        Literal["\\1"], Field(serialization_alias="949_indicators")
    ]


class MonoRecord(BaseModel):
    """
    A class to define a valid MARC record for monographs:
     - contains item, order and invoice data
     - order locations are only valid for shelf-ready research materials

    """

    model_config = ConfigDict(validate_default=True, revalidate_instances="always")

    material_type: Literal[
        "monograph_record",
        "catalogue_raissonne",
        "dance",
        "multipart",
        "pamphlet",
        "non-standard_binding_packaging",
    ]
    bib_call_no: Annotated[
        Union[
            Annotated[
                str,
                Field(pattern=r"^852  8\\\$hReCAP 2(3|4|5)-\d{6}$"),
                Tag("monograph_record"),
            ],
            Annotated[None, Tag("other")],
        ],
        Discriminator(material_type_validator),
    ]
    bib_vendor_code: Annotated[
        Literal["EVP", "AUXAM", "LEILA"], Field(serialization_alias="901$a")
    ]
    lcc: Annotated[str, Field(serialization_alias="050$a")]
    invoice_date: Annotated[str, Field(pattern=r"^\d{6}$", serialization_alias="980$a")]
    invoice_price: Annotated[
        str, Field(pattern=r"^\d{3,}$", serialization_alias="980$b")
    ]
    invoice_shipping: Annotated[
        str, Field(pattern=r"^\d{1,}$", serialization_alias="980$c")
    ]
    invoice_tax: Annotated[str, Field(pattern=r"^\d{1,}$", serialization_alias="980$d")]
    invoice_net_price: Annotated[
        str, Field(pattern=r"^\d{3,}$", serialization_alias="980$e")
    ]
    invoice_number: Annotated[str, Field(serialization_alias="980$f")]
    invoice_copies: Annotated[
        str, Field(pattern=r"^[0-9]+$", serialization_alias="980$g")
    ]
    order_price: Annotated[str, Field(pattern=r"^\d{3,}$", serialization_alias="960$u")]
    order_location: Annotated[
        Literal[
            "MAB", "MAF", "MAG", "MAL", "MAP", "MAS", "PAD", "PAH", "PAM", "PAT", "SC"
        ],
        Field(serialization_alias="960$t"),
    ]
    order_fund: Annotated[str, Field(serialization_alias="960$u")]
    order_indicators: Annotated[
        Literal["\\\\"], Field(serialization_alias="960_indicators")
    ]
    library: Annotated[Literal["RL", "BPL", "BL"], Field(serialization_alias="910$a")]
    items: Annotated[
        Union[
            Annotated[List[Item], Tag("monograph_record")],
            Annotated[None, Tag("other")],
        ],
        Field(serialization_alias="949"),
        Discriminator(material_type_validator),
    ]
