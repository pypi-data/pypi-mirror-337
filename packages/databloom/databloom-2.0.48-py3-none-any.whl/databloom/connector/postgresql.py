"""PostgreSQL connector implementation."""
import pandas as pd
from sqlalchemy import create_engine, text
from typing import List, Optional

from ..api import CredentialsAPI
from .base import BaseConnector


class PostgreSQLConnector(BaseConnector):
    """PostgreSQL connector class."""

    def __init__(self, name: str):
        """Initialize PostgreSQL connector.

        Args:
            name: Name of the connector instance
        """
        super().__init__(name)
        self.engine = None
        self.connect()

    def connect(self):
        """Connect to PostgreSQL database using credentials from API."""
        creds = CredentialsAPI.get_credentials(self.name)
        conn_str = f"postgresql://{creds['user']}:{creds['password']}@{creds['host']}:{creds['port']}/{creds['dbname']}"
        self.engine = create_engine(conn_str)

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

    def write(self, df: pd.DataFrame, table: str, if_exists: str = "fail"):
        """Write DataFrame to PostgreSQL table.

        Args:
            df: DataFrame to write
            table: Target table name
            if_exists: How to behave if table exists
        """
        df.to_sql(table, self.engine, if_exists=if_exists, index=False) 