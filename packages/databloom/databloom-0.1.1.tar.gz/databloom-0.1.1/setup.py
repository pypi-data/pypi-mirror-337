from setuptools import setup, find_packages

setup(
    name="databloom",
    version="0.1.1",
    author="DataBloom Team",
    description="DataBloom Connector Package",
    packages=find_packages(exclude=["tests*", "examples*"]),
    python_requires=">=3.9",
    install_requires=[
        "pandas>=2.2.3",
        "psycopg2-binary>=2.9.10",
        "sqlalchemy>=2.0.38",
        "trino>=0.333.0",
        "pyspark>=3.5.1",
        "requests>=2.31.0",
        "duckdb>=0.10.0",
        "mysql-connector-python>=8.0.0",
        "google-auth>=2.0.0",
        "google-auth-oauthlib>=1.0.0",
        "google-auth-httplib2>=0.1.0",
        "google-api-python-client>=2.0.0"
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=4.1.0",
            "black>=24.0.0",
            "isort>=5.13.0",
            "flake8>=7.0.0",
        ],
    },
) 