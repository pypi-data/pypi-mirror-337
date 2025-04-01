import os
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from ..api import CredentialsAPI
from .base import BaseConnector

class MySQLConnector(BaseConnector):
    def __init__(self, name=None):
        """Initialize MySQL connector with credentials"""
        super().__init__()
        self.engine = None
        self.connection = None
        self._source_name = name
        # Auto-connect on initialization
        self.connect()
    
    def connect(self):
        """Connect to MySQL database using credentials from API"""
        try:
            if not self._source_name:
                raise ValueError("Source name is required")
            
            # Get credentials from API
            creds = CredentialsAPI.get_credentials(self._source_name)
            if creds["type"] != "mysql":
                raise ValueError(f"Invalid credential type: {creds['type']}")
            
            # Extract credentials
            host = creds.get("host")
            port = creds.get("port", "3306")
            user = creds.get("user")
            password = creds.get("password")
            database = creds.get("database", "mysql")
            
            # Validate credentials
            if not all([host, user, password]):
                raise ValueError("Missing required MySQL credentials")
            
            # Create SQLAlchemy engine with escaped password
            connection_str = (
                f"mysql+pymysql://{quote_plus(user)}:{quote_plus(password)}"
                f"@{host}:{port}/{database}"
            )
            self.engine = create_engine(connection_str)
            self.connection = self.engine.connect()
            
            # Test connection
            self.execute_query("SELECT 1")
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def execute_query(self, query):
        """Execute a SQL query and return results as DataFrame"""
        try:
            if not isinstance(query, (str, text)):
                raise ValueError("Query must be a string")
            
            if not self.connection and not self.connect():
                raise ValueError("Not connected to MySQL")
            
            # Convert string query to SQLAlchemy text
            if isinstance(query, str):
                query = text(query)
            
            return pd.read_sql_query(query, self.connection)
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            return None
    
    def read(self, query):
        """Alias for execute_query to match BaseConnector interface"""
        return self.execute_query(query)
    
    def read_table(self, table_name, columns=None, limit=None):
        """Read a table into DataFrame with optional column selection and limit"""
        try:
            if not table_name:
                raise ValueError("Table name is required")
            
            # Sanitize column names
            if columns:
                if not all(isinstance(col, str) for col in columns):
                    raise ValueError("All column names must be strings")
                cols = ", ".join(f"`{col}`" for col in columns)
            else:
                cols = "*"
            
            # Build query with proper escaping
            query = f"SELECT {cols} FROM `{table_name}`"
            if limit:
                if not isinstance(limit, int) or limit <= 0:
                    raise ValueError("Limit must be a positive integer")
                query += f" LIMIT {limit}"
            
            # Store result in self.data for get_sample
            self.data = self.execute_query(query)
            return self.data
        except Exception as e:
            print(f"Error reading table: {str(e)}")
            return None
    
    def list_tables(self):
        """List all tables in the current database"""
        try:
            query = """
            SELECT TABLE_NAME 
            FROM information_schema.tables 
            WHERE table_schema = DATABASE()
            AND table_type = 'BASE TABLE'
            ORDER BY table_name
            """
            result = self.execute_query(query)
            if result is not None and not result.empty:
                return result['TABLE_NAME'].tolist()
            return []
        except Exception as e:
            print(f"Error listing tables: {str(e)}")
            return []
    
    def write(self, data, table_name, if_exists='fail'):
        """Write DataFrame to MySQL table"""
        try:
            if not isinstance(data, pd.DataFrame):
                raise ValueError("Data must be a pandas DataFrame")
            
            if not self.engine and not self.connect():
                raise ValueError("Not connected to MySQL")
            
            # Write DataFrame to table
            data.to_sql(table_name, self.engine, if_exists=if_exists, index=False)
            return True
        except Exception as e:
            print(f"Error writing to table: {str(e)}")
            return False
    
    def __del__(self):
        """Close connection when object is destroyed"""
        try:
            if hasattr(self, 'connection') and self.connection:
                self.connection.close()
            if hasattr(self, 'engine') and self.engine:
                self.engine.dispose()
        except Exception as e:
            print(f"Error closing connection: {str(e)}") 