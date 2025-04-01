import os
import json
import gspread
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

class GoogleSheetsConnector:
    """Connector for Google Sheets using OAuth 2.0 authentication."""
    
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    def __init__(self, credentials_path=None, name=None):
        """Initialize the connector with OAuth credentials.
        
        Args:
            credentials_path (str, optional): Path to the OAuth 2.0 client credentials JSON file
            name (str, optional): Name for reading credentials from environment variables
        """
        self.credentials_path = credentials_path
        self.name = name
        self._client = None
        self.token_path = 'token.pickle'
    
    def connect(self):
        """Connect to Google Sheets using OAuth 2.0 authentication."""
        creds = None
        
        # Load existing token if available
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Try to get credentials from environment variable first
                creds_json = os.environ.get('GOOGLE_SHEETS_CREDENTIALS')
                if creds_json:
                    try:
                        creds_dict = json.loads(creds_json)
                        flow = InstalledAppFlow.from_client_config(
                            creds_dict, self.SCOPES)
                    except Exception as e:
                        raise ValueError(f"Invalid credentials JSON in environment variable: {str(e)}")
                # Fall back to file if environment variable not set
                elif self.credentials_path and os.path.exists(self.credentials_path):
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, self.SCOPES)
                else:
                    raise ValueError("No valid credentials found in environment or file")
                
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
        
        try:
            self._client = gspread.authorize(creds)
            # Test the connection
            self._client.list_spreadsheet_files()
        except Exception as e:
            raise Exception(f"Failed to connect to Google Sheets: {str(e)}")
    
    @property
    def client(self):
        """Get the gspread client instance."""
        if not self._client:
            raise Exception("Not connected to Google Sheets. Call connect() first.")
        return self._client
    
    def read_sheet(self, spreadsheet_name=None, spreadsheet_url=None, worksheet_name=None):
        """Read data from a Google Sheet.
        
        Args:
            spreadsheet_name (str, optional): Name of the spreadsheet to read
            spreadsheet_url (str, optional): URL of the spreadsheet to read
            worksheet_name (str, optional): Name of the worksheet to read (defaults to first worksheet)
            
        Returns:
            pandas.DataFrame: Data from the worksheet
        """
        try:
            # Open spreadsheet by name or URL
            if spreadsheet_url:
                spreadsheet = self.client.open_by_url(spreadsheet_url)
            elif spreadsheet_name:
                spreadsheet = self.client.open(spreadsheet_name)
            else:
                raise ValueError("Either spreadsheet_name or spreadsheet_url must be provided")
            
            # Get worksheet
            if worksheet_name:
                worksheet = spreadsheet.worksheet(worksheet_name)
            else:
                worksheet = spreadsheet.get_worksheet(0)  # First worksheet
            
            # Get all values including headers
            data = worksheet.get_all_records()
            
            # Convert to DataFrame
            return pd.DataFrame(data)
            
        except Exception as e:
            raise Exception(f"Failed to read sheet: {str(e)}")
    
    def upload_dataframe(self, df, spreadsheet_name, worksheet_name):
        """Upload a pandas DataFrame to Google Sheets.
        
        Args:
            df (pandas.DataFrame): DataFrame to upload
            spreadsheet_name (str): Name of the spreadsheet
            worksheet_name (str): Name of the worksheet
            
        Returns:
            str: URL of the created/updated spreadsheet
        """
        try:
            # Try to open existing spreadsheet or create new one
            try:
                spreadsheet = self.client.open(spreadsheet_name)
            except gspread.SpreadsheetNotFound:
                spreadsheet = self.client.create(spreadsheet_name)
                # Make it accessible to anyone with the link
                spreadsheet.share(None, perm_type='anyone', role='reader')
            
            # Get or create worksheet
            try:
                worksheet = spreadsheet.worksheet(worksheet_name)
            except gspread.WorksheetNotFound:
                worksheet = spreadsheet.add_worksheet(worksheet_name, 
                                                   rows=df.shape[0] + 1,  # +1 for header
                                                   cols=df.shape[1])
            
            # Clear existing content
            worksheet.clear()
            
            # Update with new data
            worksheet.update([df.columns.values.tolist()] + df.values.tolist())
            
            return f"Spreadsheet URL: {spreadsheet.url}"
            
        except Exception as e:
            raise Exception(f"Failed to upload DataFrame: {str(e)}") 

 