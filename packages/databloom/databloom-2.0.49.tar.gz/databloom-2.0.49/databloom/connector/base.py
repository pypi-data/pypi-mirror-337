"""Base connector class for all connectors."""
from abc import ABC, abstractmethod
import pandas as pd


class BaseConnector(ABC):
    """Base class for all connectors."""

    def __init__(self, name: str):
        """Initialize the connector.

        Args:
            name: Name of the connector instance
        """
        self.name = name

    @abstractmethod
    def connect(self):
        """Connect to the data source."""
        pass

    @abstractmethod
    def read(self, query: str) -> pd.DataFrame:
        """Execute a query and return results as a DataFrame.

        Args:
            query: SQL query to execute

        Returns:
            DataFrame containing query results
        """
        pass 