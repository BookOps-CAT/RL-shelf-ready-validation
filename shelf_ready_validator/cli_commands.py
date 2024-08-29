import os
from typing import Generator
from pymarc import MARCReader, Record
from file_retriever.file import File
from google.auth.transport.requests import Request  # type: ignore
from google.oauth2.credentials import Credentials  # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore
from pydantic import ValidationError

from shelf_ready_validator.models import (
    VendorMonographRecordModel,
    VendorOtherRecordModel,
)
from shelf_ready_validator.translate import (
    MarcValidationError,
)
from shelf_ready_validator.vendor_marc import VendorRecord


def read_marc_records(fh: bytes) -> Generator[Record, None, None]:
    """
    Reads .mrc file and returns a record
    """
    reader = MARCReader(fh)
    for record in reader:
        yield record


def read_marc_records_file(file: str) -> Generator[Record, None, None]:
    """
    Reads .mrc file and returns a record
    """
    with open(file, "rb") as fh:
        reader = MARCReader(fh)
        for record in reader:
            yield record


def read_validate_file(file_obj: File) -> list:
    reader = read_marc_records(file_obj.file_stream.getvalue())
    output = []
    record_n = 1
    for record in reader:
        vendor_record = VendorRecord(leader=record.leader, fields=record.fields)
        dict_output = {
            "vendor_code": vendor_record.bib_vendor_code.vendor_code,
            "record_number": record_n,
        }
        validation_output = validate_single_record(vendor_record)
        dict_output.update(validation_output)
        output.append(dict_output)
        record_n += 1
    return output


def validate_single_record(record: VendorRecord) -> dict:
    input = record.pydantic_dict_input()
    try:
        match input["material_type"]:
            case "monograph":
                VendorMonographRecordModel.model_validate(input)
                return {"valid": True}
            case _:
                VendorOtherRecordModel.model_validate(input)
                return {"valid": True}
    except ValidationError as e:
        marc_errors = MarcValidationError(e.errors())
        return marc_errors.to_dict()


def write_sheet(
    spreadsheet_id, range_name, value_input_option, insert_data_option, values
):
    """
    A function to append data to a google sheet
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

    try:
        service = build("sheets", "v4", credentials=creds)

        body = {
            "majorDimension": "ROWS",
            "range": "RecordOutput!A1:M10000",
            "values": values,
        }
        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                insertDataOption=insert_data_option,
                body=body,
            )
            .execute()
        )
        return result
    except HttpError as error:
        return error


def write_vendor_sheet(
    spreadsheet_id: str,
    vendor_code: str,
    value_input_option: str,
    insert_data_option: str,
    values: list,
):
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

    try:
        service = build("sheets", "v4", credentials=creds)

        body = {
            "majorDimension": "ROWS",
            "range": f"{vendor_code.upper()}!A1:M10000",
            "values": values,
        }
        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_id,
                range=f"{vendor_code.upper()}!A1:M10000",
                valueInputOption=value_input_option,
                insertDataOption=insert_data_option,
                body=body,
            )
            .execute()
        )
        return result
    except HttpError as error:
        return error
