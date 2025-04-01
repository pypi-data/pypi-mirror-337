import os
import json
import gspread
import pandas as pd
from google.oauth2.credentials import Credentials
from ..api import CredentialsAPI
from .base import BaseConnector

class GoogleSheetsConnector(BaseConnector):
    def __init__(self, name=None):
        super().__init__()
        self.client = None
        self._token = None
        self._source_name = name
        self._scopes = [
            "https://www.googleapis.com/auth/spreadsheets.readonly",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        # Auto-connect on initialization
        self.connect()
    
    def connect(self, token=None):
        """Connect to Google Sheets API"""
        try:
            if token is None and self._source_name:
                # Get credentials from API
                creds = CredentialsAPI.get_credentials(self._source_name)
                if creds["type"] != "google_sheets":
                    raise ValueError(f"Invalid credential type: {creds['type']}")
                token = creds["token"]
            elif token is None:
                raise ValueError("Neither token nor source_name provided")
            
            # Parse token if it's a string
            if isinstance(token, str):
                token = json.loads(token)
            
            # Save token to temporary file
            token_path = "/tmp/token.json"
            with open(token_path, "w") as f:
                json.dump(token, f)
            
            # Create credentials and authorize
            if os.path.exists(token_path):
                creds = Credentials.from_authorized_user_file(token_path, self._scopes)
                self.client = gspread.authorize(creds)
                self._token = token
                return True
            return False
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def read(self, sheet_name, worksheet_name=None):
        """Read data from Google Sheet into pandas DataFrame"""
        try:
            if not self.client and not self.connect():
                raise ValueError("Not connected to Google Sheets")
            
            # Open the spreadsheet
            sheet = self.client.open(sheet_name)
            
            # Get specific worksheet or first worksheet if not specified
            if worksheet_name:
                worksheet = sheet.worksheet(worksheet_name)
            else:
                worksheet = sheet.get_worksheet(0)
            
            # Get all records and convert to DataFrame
            data = worksheet.get_all_records()
            self.data = pd.DataFrame(data)
            return self.data
        except Exception as e:
            print(f"Error reading sheet: {e}")
            return None

    def read_sheet(self, sheet_name, worksheet_name=None):
        """Alias for read method to match the desired interface"""
        return self.read(sheet_name, worksheet_name)
    
    def write(self, data, sheet, worksheet_name=None):
        """Write DataFrame to Google Sheet"""
        try:
            if not isinstance(data, pd.DataFrame):
                raise ValueError("Data must be a pandas DataFrame")
            
            if not self.client and not self.connect():
                raise ValueError("Not connected to Google Sheets")
            
            if isinstance(sheet, str):
                sheet = self.client.open(sheet)
            
            if worksheet_name:
                worksheet = sheet.worksheet(worksheet_name)
            else:
                worksheet = sheet.get_worksheet(0)
            
            worksheet.update([data.columns.values.tolist()] + data.values.tolist())
            return True
        except Exception as e:
            print(f"Error writing to sheet: {e}")
            return False 