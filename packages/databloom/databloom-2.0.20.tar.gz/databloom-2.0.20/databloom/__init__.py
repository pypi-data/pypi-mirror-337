"""DataBloom package."""

from databloom.version import __version__

class connector:
    @staticmethod
    def PostgreSQLConnector(name=None):
        from .connector.postgresql import PostgreSQLConnector
        return PostgreSQLConnector(name=name)
    
    @staticmethod
    def MySQLConnector(name=None):
        from .connector.mysql import MySQLConnector
        return MySQLConnector(name=name)
    
    @staticmethod
    def GoogleSheetsConnector(name=None):
        from .connector.ggsheet import GoogleSheetsConnector
        return GoogleSheetsConnector(name=name)

def get_base_connector():
    from .connector.base import BaseConnector
    return BaseConnector

def get_postgresql_connector():
    from .connector.postgresql import PostgreSQLConnector
    return PostgreSQLConnector

def get_mysql_connector():
    from .connector.mysql import MySQLConnector
    return MySQLConnector

def get_dataset():
    from .datasets import Dataset
    return Dataset

__all__ = ['connector', '__version__', 'get_base_connector', 'get_postgresql_connector', 'get_mysql_connector', 'get_dataset'] 