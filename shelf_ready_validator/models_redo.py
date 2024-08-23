from enum import Enum
from typing import Annotated, Union, List, Dict

from pydantic import BaseModel, Field, field_validator


class VendorFields(Enum):
    BibCallNo = "852"
    ItemField = "949"
    OrderField = "960"
    LCC = "050"
    LCCN = "010"
    ISBN = "020"
    InvoiceField = "980"


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
