"""Google Sheets connector implementation."""
import os
import json
import pandas as pd
from typing import Optional
import gspread
from google.oauth2.credentials import Credentials

from ..api import CredentialsAPI
from .base import BaseConnector


class GoogleSheetsConnector(BaseConnector):
    """Google Sheets connector class."""

    def __init__(self, name: str):
        """Initialize Google Sheets connector.

        Args:
            name: Name of the connector instance
        """
        super().__init__(name)
        self.client = None
        self.connect()

    def connect(self):
        """Connect to Google Sheets using credentials from API."""
        creds_data = CredentialsAPI.get_credentials(self.name)
        
        # Create credentials object
        creds = Credentials.from_authorized_user_file(
            creds_data['token_file'],
            ['https://www.googleapis.com/auth/spreadsheets']
        )
        
        # Create gspread client
        self.client = gspread.authorize(creds)

    def read(self, query: str) -> pd.DataFrame:
        """Not implemented for Google Sheets.

        Args:
            query: Not used

        Raises:
            NotImplementedError: Google Sheets doesn't support SQL queries
        """
        raise NotImplementedError(
            "Google Sheets connector doesn't support SQL queries"
        )

    def read_sheet(
        self,
        spreadsheet_name: str,
        worksheet_name: str,
        range_name: Optional[str] = None,
    ) -> pd.DataFrame:
        """Read data from a Google Sheet.

        Args:
            spreadsheet_name: Name of the spreadsheet
            worksheet_name: Name of the worksheet to read
            range_name: Optional cell range to read (A1 notation)

        Returns:
            DataFrame containing sheet data
        """
        # Open the spreadsheet
        sheet = self.client.open(spreadsheet_name)
        
        # Get the specified worksheet
        worksheet = sheet.worksheet(worksheet_name)
        
        # Get all records (converts to list of dicts)
        records = worksheet.get_all_records()
        
        # Convert to DataFrame
        return pd.DataFrame(records)

    def write_sheet(
        self,
        df: pd.DataFrame,
        spreadsheet_name: str,
        worksheet_name: str,
        range_name: Optional[str] = None,
        include_header: bool = True
    ):
        """Write DataFrame to Google Sheet.

        Args:
            df: DataFrame to write
            spreadsheet_name: Name of the spreadsheet
            worksheet_name: Name of the worksheet to write to
            range_name: Optional cell range to write to (A1 notation)
            include_header: Whether to write column names
        """
        # Open the spreadsheet
        sheet = self.client.open(spreadsheet_name)
        
        # Get or create the worksheet
        try:
            worksheet = sheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            worksheet = sheet.add_worksheet(worksheet_name, rows=1000, cols=100)
        
        # Convert DataFrame to list of lists
        data = df.values.tolist()
        if include_header:
            data.insert(0, df.columns.tolist())
        
        # Clear existing content if needed
        if range_name:
            worksheet.clear(range_name)
        else:
            worksheet.clear()
        
        # Write the data
        worksheet.update(
            range_name if range_name else 'A1',
            data
        ) 