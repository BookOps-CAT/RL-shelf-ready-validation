import os
import yaml
from typing import Generator, List
from pymarc import MARCReader, Record
from google.auth.transport.requests import Request  # type: ignore
from google.oauth2.credentials import Credentials  # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore
from file_retriever.connect import Client
from file_retriever.file import File


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


def load_vendor_creds() -> None:
    """Read yaml file and load vendor ftp/sftp credentials into environment variables"""
    config_path = os.path.join(
        os.environ["USERPROFILE"], ".cred/.sftp/connections.yaml"
    )
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
        if config is None:
            raise ValueError("No credentials found in config file.")
        vendor_list = [
            i.split("_HOST")[0]
            for i in config.keys()
            if i.endswith("_HOST") and "NSDROP" not in i
        ]
        for k, v in config.items():
            os.environ[k] = v
        for vendor in vendor_list:
            os.environ[f"{vendor}_DST"] = f"NSDROP/vendor_records/{vendor.lower()}"


def connect(name: str) -> Client:
    client_name = name.upper()
    return Client(
        name=client_name,
        username=os.environ[f"{client_name}_USER"],
        password=os.environ[f"{client_name}_PASSWORD"],
        host=os.environ[f"{client_name}_HOST"],
        port=os.environ[f"{client_name}_PORT"],
    )


def get_vendor_files(vendor: str) -> List[File]:
    load_vendor_creds()
    vendor_dir = os.environ[f"{vendor.upper()}_DST"]
    all_files = []
    with connect("NSDROP") as client:
        file_list = client.list_file_info(time_delta=0, remote_dir=vendor_dir)
        for file in file_list:
            downloaded_file = client.get_file(file=file, remote_dir=vendor_dir)
            all_files.append(downloaded_file)
    print(f"{len(all_files)} files on {vendor} server")
    return all_files


def read_marc_records_file(file: str) -> Generator[Record, None, None]:
    """
    Reads .mrc file and returns a record
    """
    with open(file, "rb") as fh:
        reader = MARCReader(fh)
        for record in reader:
            yield record
