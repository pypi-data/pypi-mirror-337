from setuptools import setup, find_packages
import os

# Read the contents of README.md
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="databloom",
    version="2.0.1",  # Increased version number
    author="DataBloom Team",
    author_email="team@databloom.ai",
    description="DataBloom Connector Package for Data Integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/databloom-ai/databloom-connector",
    packages=find_packages(exclude=["tests*", "examples*", "*.env", "tests/conftest.py"]),
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
        "gspread>=6.0.0",
        "google-auth>=2.28.0",
        "google-auth-oauthlib>=1.2.0",
        "google-auth-httplib2>=0.2.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=4.1.0",
            "black>=24.0.0",
            "isort>=5.13.0",
            "flake8>=7.0.0",
            "twine>=4.0.0",
            "build>=1.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database",
    ],
    keywords="databloom, data integration, connector, database, warehouse",
) 