"""
Credentials management for DataBloom SDK.
"""
import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional

class CredentialsAPI:
    @staticmethod
    def get_credentials(source_name):
        """Get credentials for a given source name
        For now, if source_name is FAKE_CODE_UUID, read from .env
        Later this will be replaced with actual API calls
        """
        load_dotenv()
        
        if source_name == "FAKE_CODE_UUID":
            cred_type = os.environ.get("CRED_TYPE", "google_sheets")
            
            if cred_type == "google_sheets":
                token = os.environ.get("GGSHEET_TOKEN")
                if not token:
                    raise ValueError("GGSHEET_TOKEN not found in environment")
                return {
                    "token": token,
                    "type": "google_sheets"
                }
            elif cred_type == "postgresql":
                return {
                    "type": "postgresql",
                    "host": os.environ.get("POSTGRES_HOST"),
                    "port": os.environ.get("POSTGRES_PORT", "5432"),
                    "user": os.environ.get("POSTGRES_USER"),
                    "password": os.environ.get("POSTGRES_PASSWORD"),
                    "database": os.environ.get("POSTGRES_DBNAME")
                }
            elif cred_type == "mysql":
                return {
                    "type": "mysql",
                    "host": os.environ.get("MYSQL_HOST"),
                    "port": os.environ.get("MYSQL_PORT", "3306"),
                    "user": os.environ.get("MYSQL_USER"),
                    "password": os.environ.get("MYSQL_PASSWORD"),
                    "database": os.environ.get("MYSQL_DATABASE", "mysql")
                }
            else:
                raise ValueError(f"Unknown credential type: {cred_type}")
        else:
            # TODO: Implement actual API call to get credentials
            raise NotImplementedError(f"Getting credentials for {source_name} not yet implemented")

class CredentialsManager:
    """Manager class for handling credentials."""
    
    def __init__(self):
        """Initialize CredentialsManager."""
        pass
        
    def get_credentials_by_uuid(self, uuid: str) -> Optional[Dict[str, Any]]:
        """
        Get credentials by UUID.
        
        Args:
            uuid: UUID for credentials
            
        Returns:
            Dict containing credentials or None if not found
        """
        # For testing, return dummy credentials
        if uuid == "postgresql/postgres_source":
            return {
                "host": os.getenv("POSTGRES_HOST", "localhost"),
                "port": os.getenv("POSTGRES_PORT", "5432"),
                "user": os.getenv("POSTGRES_USER", "postgres"),
                "password": os.getenv("POSTGRES_PASSWORD", "password"),
                "database": os.getenv("POSTGRES_DBNAME", "postgres")
            }
        elif uuid == "mysql/mysql_source":
            return {
                "host": os.getenv("MYSQL_HOST", "localhost"),
                "port": os.getenv("MYSQL_PORT", "3306"),
                "user": os.getenv("MYSQL_USER", "root"),
                "password": os.getenv("MYSQL_PASSWORD", "password"),
                "database": os.getenv("MYSQL_DBNAME", "mysql")
            }
        return None
        
    def get_s3_credentials(self) -> Dict[str, str]:
        """
        Get S3 credentials from environment.
        
        Returns:
            Dict containing S3 credentials
        """
        return {
            "endpoint": os.getenv("S3_ENDPOINT", "localhost:9000"),
            "region": os.getenv("S3_REGION", "us-east-1"),
            "access_key": os.getenv("S3_ACCESS_KEY_ID", "admin"),
            "secret_key": os.getenv("S3_SECRET_ACCESS_KEY", "password")
        } 