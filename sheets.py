from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = 'keys/key.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']



creds = None
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '18W9AWoLYdYarcNqqPyeFJHnOh_-M_gKgcluRR6ga80w'


service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Raw Data!A:V").execute()

input = [["test"]]
request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                 range="Raw Data!A2",
                                                 valueInputOption="USER_ENTERED",
                                                 body={"values": input}).execute()


