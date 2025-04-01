"""
Spark session management for DataBloom SDK.
"""
import os
import logging
import sys
from pyspark.sql import SparkSession
from pyspark import SparkConf

logger = logging.getLogger(__name__)

class SparkSessionManager:
    """Manager class for Spark session."""
    
    def __init__(self):
        """Initialize Spark session manager."""
        self._session = None
        
    def get_session(self, app_name: str = "DataBloom") -> SparkSession:
        """
        Get or create a Spark session.
        
        Args:
            app_name: Name for the Spark application
            
        Returns:
            SparkSession instance
        """
        if not self._session:
            try:
                # Get environment variables
                nessie_uri = os.getenv("NESSIE_URI", "http://localhost:19120/api/v1")
                nessie_ref = os.getenv("NESSIE_REF", "main")
                nessie_warehouse = os.getenv("NESSIE_WAREHOUSE", "s3a://nessie/")
                nessie_io_impl = os.getenv("NESSIE_IO_IMPL", "org.apache.iceberg.hadoop.HadoopFileIO")
                warehouse_location = os.getenv("S3_WAREHOUSE", "s3a://nessie/warehouse")
                
                s3_endpoint = os.getenv("S3_ENDPOINT", "localhost:9000")
                s3_access_key = os.getenv("S3_ACCESS_KEY_ID", "admin")
                s3_secret_key = os.getenv("S3_SECRET_ACCESS_KEY", "password")
                
                # Create Spark session builder with packages
                packages = [
                    "org.apache.iceberg:iceberg-spark-runtime-3.4_2.12:1.4.3",
                    "org.apache.iceberg:iceberg-aws:1.4.3",
                    "org.projectnessie.nessie-integrations:nessie-spark-extensions-3.4_2.12:0.103.2",
                    "org.apache.hadoop:hadoop-aws:3.3.4",
                    "software.amazon.awssdk:bundle:2.17.178",
                    "software.amazon.awssdk:url-connection-client:2.17.178"
                ]
                
                # Create Spark configuration
                conf = SparkConf()
                conf.set("spark.app.name", app_name)
                conf.set("spark.master", "local[*]")
                conf.set("spark.jars.packages", ",".join(packages))
                conf.set("spark.sql.extensions", 
                        "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
                conf.set("spark.sql.catalog.nessie", 
                        "org.apache.iceberg.spark.SparkCatalog")
                conf.set("spark.sql.catalog.nessie.catalog-impl", 
                        "org.apache.iceberg.nessie.NessieCatalog")
                conf.set("spark.sql.catalog.nessie.uri", nessie_uri)
                conf.set("spark.sql.catalog.nessie.ref", nessie_ref)
                conf.set("spark.sql.catalog.nessie.warehouse", nessie_warehouse)
                conf.set("spark.sql.catalog.nessie.io-impl", nessie_io_impl)
                conf.set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
                conf.set("spark.hadoop.fs.s3a.access.key", s3_access_key)
                conf.set("spark.hadoop.fs.s3a.secret.key", s3_secret_key)
                conf.set("spark.hadoop.fs.s3a.endpoint", f"http://{s3_endpoint}")
                conf.set("spark.hadoop.fs.s3a.path.style.access", "true")
                conf.set("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
                conf.set("spark.hadoop.fs.s3a.aws.credentials.provider",
                        "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")
                conf.set("spark.sql.warehouse.dir", warehouse_location)
                conf.set("spark.sql.ansi.enabled", "true")
                conf.set("spark.driver.memory", "4g")
                conf.set("spark.executor.memory", "4g")
                conf.set("spark.driver.maxResultSize", "4g")
                conf.set("spark.sql.shuffle.partitions", "10")
                
                # Set SPARK_HOME to the pyspark installation directory
                python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
                # os.environ["SPARK_HOME"] = f"/home/namvq/anaconda3/envs/databloom/lib/{python_version}/site-packages/pyspark"
                # os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64"
                
                # Create session
                self._session = SparkSession.builder \
                    .config(conf=conf) \
                    .enableHiveSupport() \
                    .getOrCreate()
                self._session.sparkContext.setLogLevel("WARN")
                
                # Create default namespace if it doesn't exist
                try:
                    self._session.sql("CREATE NAMESPACE IF NOT EXISTS nessie.default")
                    logger.info("Default namespace created or already exists")
                except Exception as e:
                    logger.warning(f"Failed to create default namespace: {e}")
                
                logger.info("Successfully created Spark session")
                
            except Exception as e:
                logger.error(f"Failed to create Spark session: {e}")
                raise
                
        return self._session
        
    def stop(self):
        """Stop the Spark session if it exists."""
        if self._session:
            try:
                self._session.stop()
                self._session = None
                logger.info("Successfully stopped Spark session")
            except Exception as e:
                logger.error(f"Error stopping Spark session: {e}")
                
    def __del__(self):
        """Clean up Spark session on object destruction."""
        self.stop() 