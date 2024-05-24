from typing import Generator
import os.path
from pymarc import MARCReader, Record
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def read_marc_records(file: str) -> Generator[Record, None, None]:
    """
    Reads .mrc file and returns a record
    """
    with open(file, "rb") as fh:
        reader = MARCReader(fh)
        for record in reader:
            yield record


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
