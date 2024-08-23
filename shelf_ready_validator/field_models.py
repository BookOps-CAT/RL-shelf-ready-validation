from typing import Annotated, Literal
from pydantic import BaseModel, Field


class ItemVendorCode(BaseModel):
    value: Literal["EVP", "AUXAM", "LEILA"] = Field(alias="v")


class ItemCallTag(BaseModel):
    value: Literal["8528"] = Field(alias="z")


class ItemBarcode(BaseModel):
    value: Annotated[str, Field(pattern=r"^33433[0-9]{9}$", alias="i")]


class ItemAgency(BaseModel):
    value: Literal["43"] = Field(alias="h")


class ItemPrice(BaseModel):
    value: Annotated[str, Field(pattern=r"^\d{1,}\.\d{2}$", alias="p")]


class ItemType(BaseModel):
    value: Literal["55", "2"] = Field(alias="t")


class ItemLocation(BaseModel):
    value: Literal[
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
    ] = Field(alias="l")


class ItemCallNo(BaseModel):
    value: Annotated[
        str, Field(pattern=r"^ReCAP 23-\d{6}$|^ReCAP 24-\d{6}$", alias="a")
    ]


class BibCallNo(BaseModel):
    value: Annotated[
        str, Field(pattern=r"^ReCAP 23-\d{6}$|^ReCAP 24-\d{6}$", alias="h")
    ]
