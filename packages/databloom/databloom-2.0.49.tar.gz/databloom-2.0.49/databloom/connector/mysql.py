"""MySQL connector implementation."""
import os
import pandas as pd
from sqlalchemy import create_engine, text
from typing import List, Optional
from urllib.parse import quote_plus

from ..api import CredentialsAPI
from .base import BaseConnector


class MySQLConnector(BaseConnector):
    """MySQL connector class."""

    def __init__(self, name: str):
        """Initialize MySQL connector.

        Args:
            name: Name of the connector instance
        """
        super().__init__(name)
        self.engine = None
        self.connect()

    def connect(self):
        """Connect to MySQL database using credentials from API."""
        creds = CredentialsAPI.get_credentials(self.name)
        # URL encode password to handle special characters
        password = quote_plus(creds['password'])
        conn_str = f"mysql+pymysql://{creds['user']}:{password}@{creds['host']}:{creds['port']}"
        self.engine = create_engine(conn_str)

    def execute_query(self, query: str):
        """Execute a query without returning results.

        Args:
            query: SQL query to execute
        """
        with self.engine.connect() as conn:
            conn.execute(text(query))
            conn.commit()

    def read(self, query: str) -> pd.DataFrame:
        """Execute query and return results as DataFrame.

        Args:
            query: SQL query to execute

        Returns:
            DataFrame containing query results
        """
        with self.engine.connect() as conn:
            return pd.read_sql(text(query), conn)

    def read_table(
        self, table: str, columns: Optional[List[str]] = None, where: str = None
    ) -> pd.DataFrame:
        """Read data from a table.

        Args:
            table: Table name
            columns: List of columns to select
            where: WHERE clause for filtering

        Returns:
            DataFrame containing table data
        """
        cols = "*" if not columns else ", ".join(columns)
        query = f"SELECT {cols} FROM {table}"
        if where:
            query += f" WHERE {where}"
        return self.read(query)

    def list_tables(self, database: Optional[str] = None) -> List[str]:
        """List all tables in the database.

        Args:
            database: Database name, uses current if None

        Returns:
            List of table names
        """
        if database:
            self.execute_query(f"USE {database}")
        
        df = self.read("SHOW TABLES")
        return df[df.columns[0]].tolist()

    def write(
        self,
        df: pd.DataFrame,
        table: str,
        if_exists: str = "fail",
        index: bool = False,
        **kwargs
    ):
        """Write DataFrame to MySQL table.

        Args:
            df: DataFrame to write
            table: Target table name
            if_exists: How to behave if table exists
            index: Whether to write index as column
            **kwargs: Additional arguments for to_sql
        """
        df.to_sql(
            table,
            self.engine,
            if_exists=if_exists,
            index=index,
            **kwargs
        ) 