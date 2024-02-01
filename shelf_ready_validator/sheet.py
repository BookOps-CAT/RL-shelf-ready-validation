from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
import pandas as pd


# OUTPUT_SPREADSHEET_ID = "1uerf01-YQZaUYCYDBesLiKGmp4gGeVVX89fefLGy_R0"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def write_sheet(spreadsheet_id, range_name, value_input_option, values):
    if os.path.exists("C:/Users/ckostelic/.cred/.google/token.json"):
        creds = Credentials.from_authorized_user_file(
            "C:/Users/ckostelic/.cred/.google/token.json", SCOPES
        )
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "C:/Users/ckostelic/.cred/.google/desktop-app.json", SCOPES
            )
            creds = flow.run_local_server()
        with open("C:/Users/ckostelic/.cred/.google/token.json", "w") as token:
            token.write(creds.to_json())
    # creds, _ = google.auth.default()

    try:
        service = build("sheets", "v4", credentials=creds)

        body = {
            "majorDimension": "ROWS",
            "range": "Sheet1!A1:AA1000",
            "values": values,
        }
        result = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body,
            )
            .execute()
        )
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except Exception as error:
        print(f"An error occurred: {error}")
        return error


# if __name__ == "__main__":
#     # Pass: spreadsheet_id,  range_name, value_input_option and  _values
#     update_values(
#         "1uerf01-YQZaUYCYDBesLiKGmp4gGeVVX89fefLGy_R0",
#         "Sheet1!A1:C2",
#         "USER_ENTERED",
#         [["A", "B"], ["C", "D"]],
#     )
