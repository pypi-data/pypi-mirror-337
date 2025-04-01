import pandas as pd
from abc import ABC, abstractmethod
from dotenv import load_dotenv

class BaseConnector(ABC):
    def __init__(self):
        self.data = None
        load_dotenv()  # Load environment variables from .env file
        
    @abstractmethod
    def connect(self):
        """Establish connection to the data source"""
        pass
    
    @abstractmethod
    def read(self, **kwargs):
        """Read data from the source"""
        pass
    
    @abstractmethod
    def write(self, data, **kwargs):
        """Write data to the source"""
        pass
    
    def get_data(self):
        """Return the current DataFrame"""
        return self.data
    
    def get_sample(self, n=5):
        """Return a sample of n rows from the DataFrame"""
        if self.data is not None:
            return self.data.head(n)
        return None 