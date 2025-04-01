"""DataBloom package."""

from .connector.base import BaseConnector
from .connector.postgresql import PostgreSQLConnector
from .connector.mysql import MySQLConnector
from .datasets import Dataset
from databloom.version import __version__

class connector:
    @staticmethod
    def PostgreSQLConnector(name=None):
        return PostgreSQLConnector(name=name)
    
    @staticmethod
    def MySQLConnector(name=None):
        return MySQLConnector(name=name)
    
    @staticmethod
    def GoogleSheetsConnector(name=None):
        from .connector.ggsheet import GoogleSheetsConnector
        return GoogleSheetsConnector(name=name)

__all__ = ['connector', 'BaseConnector', 'PostgreSQLConnector', 'MySQLConnector', 'Dataset', '__version__'] 