import pandas as pd
from sqlalchemy import create_engine, text
from ..api import CredentialsAPI
from .base import BaseConnector

class PostgreSQLConnector(BaseConnector):
    def __init__(self, name=None):
        super().__init__()
        self.engine = None
        self._source_name = name
        self._connection_string = None
        # Auto-connect on initialization
        self.connect()
    
    def connect(self, connection_string=None):
        """Connect to PostgreSQL database"""
        try:
            if connection_string is None and self._source_name:
                # Get credentials from API
                creds = CredentialsAPI.get_credentials(self._source_name)
                if creds["type"] != "postgresql":
                    raise ValueError(f"Invalid credential type: {creds['type']}")
                
                # Build connection string
                connection_string = f"postgresql://{creds['user']}:{creds['password']}@{creds['host']}:{creds['port']}/{creds['database']}"
            elif connection_string is None:
                raise ValueError("Neither connection_string nor source_name provided")
            
            # Create SQLAlchemy engine
            self.engine = create_engine(connection_string)
            self._connection_string = connection_string
            
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def read(self, query, params=None):
        """Execute SQL query and return results as DataFrame"""
        try:
            if not self.engine and not self.connect():
                raise ValueError("Not connected to PostgreSQL")
            
            # Execute query - handle multiple statements
            with self.engine.connect() as conn:
                # Split query into statements
                statements = [s.strip() for s in query.split(';') if s.strip()]
                
                # Execute all statements except the last one
                for stmt in statements[:-1]:
                    conn.execute(text(stmt))
                    conn.commit()
                
                # Execute the last statement and return results as DataFrame
                if statements:
                    if statements[-1].strip().upper().startswith(('SELECT', 'WITH')):
                        # Use pd.read_sql directly with the query string
                        try:
                            result = conn.execute(text(statements[-1]))
                            self.data = pd.DataFrame(result.fetchall(), columns=result.keys())
                            return self.data
                        except Exception as e:
                            print(f"Error executing query: {e}")
                            return None
                    else:
                        conn.execute(text(statements[-1]))
                        conn.commit()
                        return None
                return None
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
    
    def read_table(self, table_name, schema=None, columns=None, where=None):
        """Read a table into DataFrame"""
        try:
            # Build query
            cols = "*" if not columns else ", ".join(columns)
            schema_prefix = f"{schema}." if schema else ""
            where_clause = f" WHERE {where}" if where else ""
            
            query = f"SELECT {cols} FROM {schema_prefix}{table_name}{where_clause}"
            return self.read(query)
        except Exception as e:
            print(f"Error reading table: {e}")
            return None
    
    def write(self, data, table_name, schema=None, if_exists='fail'):
        """Write DataFrame to PostgreSQL table"""
        try:
            if not isinstance(data, pd.DataFrame):
                raise ValueError("Data must be a pandas DataFrame")
            
            if not self.engine and not self.connect():
                raise ValueError("Not connected to PostgreSQL")
            
            # Write DataFrame to table
            schema_name = schema if schema else None
            data.to_sql(table_name, self.engine, schema=schema_name, 
                       if_exists=if_exists, index=False)
            return True
        except Exception as e:
            print(f"Error writing to table: {e}")
            return False
    
    def get_sample(self, n=5):
        """Get a sample of n rows from the current DataFrame"""
        if self.data is None:
            return None
        return self.data.head(n) 