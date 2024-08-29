import datetime
import os
from typing import Any, Generator, Union
import pandas as pd
from pymarc import MARCReader, Record
from file_retriever.file import File
from google.auth.transport.requests import Request  # type: ignore
from google.oauth2.credentials import Credentials  # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore
from pydantic import ValidationError

from shelf_ready_validator.models import (
    MonographRecord,
    OtherRecord,
)
from shelf_ready_validator.translate import (
    MarcValidationError,
)
from shelf_ready_validator.vendor_marc import VendorRecord


def read_marc_file(file: str) -> Generator[Record, None, None]:
    """
    Reads bytes and returns a generator of pymarc records

    Args:
        fh: MARC data as bytes

    Yields:
        Record: a pymarc record
    """
    with open(file, "rb") as fh:
        reader = MARCReader(fh)
        for record in reader:
            yield record


def read_marc_records(fh: bytes) -> Generator[Record, None, None]:
    """
    Reads bytes and returns a generator of pymarc records

    Args:
        fh: MARC data as bytes

    Yields:
        Record: a pymarc record
    """
    reader = MARCReader(fh)
    for record in reader:
        yield record


def validate_marc_file(
    file_obj: Union[str, File], vendor_code: str
) -> list[dict[str, Any]]:
    """
    Reads a file stream and validates each record.

    Args:
        file_obj: A file object containing a MARC file stream
        vendor_code: The vendor code for the vendor who provided the MARC file

    Returns:
        A list of dictionaries containing validation results for each record in the file
    """
    if not isinstance(file_obj, File):
        reader = read_marc_file(file_obj)
        file_name = os.path.basename(file_obj)
    else:
        reader = read_marc_records(file_obj.file_stream.getvalue())
        file_name = file_obj.file_name
    validation_date = datetime.datetime.today().strftime("%Y-%m-%d %I:%M:%S")
    output = []
    record_n = 1
    for record in reader:
        vendor_record = VendorRecord(leader=record.leader, fields=record.fields)
        dict_output = {
            "validation_date": validation_date,
            "filename": file_name,
            "vendor_code": vendor_code,
            "record_number": record_n,
            "control_number": vendor_record.get_control_number(),
        }
        validation_output = validate_single_record(vendor_record)
        dict_output.update(validation_output)
        dict_output["material_type"] = vendor_record.material_type
        output.append(dict_output)
        record_n += 1
    return output


def validate_single_record(record: VendorRecord) -> dict[str, Any]:
    """
    Validates a MARC record using pydantic models.


    Args:
        record: MARC record as a VendorRecord object

    Returns:
        A dictionary containing the validation results

    """

    input = record.pydantic_dict_input()
    try:
        match input["material_type"]:
            case "monograph":
                MonographRecord.model_validate(input)
                return {"valid": True}
            case _:
                OtherRecord.model_validate(input)
                return {"valid": True}
    except ValidationError as e:
        marc_errors = MarcValidationError(e.errors())
        return marc_errors.to_dict()


def write_vendor_sheet(output: list[dict[str, Any]], vendor_code: str) -> None:
    creds = configure_sheet()
    for out in output:
        out_series = pd.Series(out, dtype=str)
        send_data_to_sheet(
            "1ZYuhMIE1WiduV98Pdzzw7RwZ08O-sJo7HJihWVgSOhQ",
            vendor_code.upper(),
            [out_series.to_list()],
            creds,
        )


def configure_sheet() -> Credentials:
    """
    A function to append data to a google sheet for a specific vendor
    """
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    cred_path = os.path.join(
        os.environ["USERPROFILE"], ".cred/.google/desktop-app.json"
    )
    token_path = os.path.join(os.environ["USERPROFILE"], ".cred/.google/token.json")

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_path, scopes)
            creds = flow.run_local_server()
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    return creds


def send_data_to_sheet(
    spreadsheet_id: str, vendor_code: str, values: list, creds: Credentials
):
    """
    A function to append data to a google sheet for a specific vendor
    """
    try:
        service = build("sheets", "v4", credentials=creds)

        body = {
            "majorDimension": "ROWS",
            "range": f"{vendor_code.upper()}!B1:O10000",
            "values": values,
        }
        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_id,
                range=f"{vendor_code.upper()}!B1:O10000",
                valueInputOption="USER_ENTERED",
                insertDataOption="INSERT_ROWS",
                body=body,
            )
            .execute()
        )
        return result
    except HttpError as error:
        return error
