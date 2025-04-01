from .ggsheet import GoogleSheetsConnector
from .postgresql import PostgreSQLConnector
from .base import BaseConnector

class connector:
    @staticmethod
    def GoogleSheetsConnector(name=None):
        return GoogleSheetsConnector(name=name)
    
    @staticmethod
    def PostgreSQLConnector(name=None):
        return PostgreSQLConnector(name=name)

__all__ = ['connector', 'GoogleSheetsConnector', 'PostgreSQLConnector', 'BaseConnector'] 