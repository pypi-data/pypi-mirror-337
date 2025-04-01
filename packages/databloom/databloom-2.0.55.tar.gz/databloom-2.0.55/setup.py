from setuptools import setup, find_packages
# with open("README.md", "r") as fh:
#     long_description = fh.read()

version = "2.0.55"

setup(
    name="databloom",
    version=version,
    author="gada121982",
    author_email="gada121982@gmail.com",
    description="A small example package",
    long_description="In progress",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'databloom': ["databloom/*"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pandas==2.2.3",
        "pyspark==3.4.2",
        "duckdb>=0.10.0",
        "sqlalchemy>=2.0.38",
        "psycopg2-binary>=2.9.10",
        "mysql-connector-python>=8.0.33",
        "findspark>=2.0.1",
        "requests>=2.31.0",
        "python-dotenv>=0.19.0",
        "trino>=0.333.0",
        "gspread>=5.12.4"
    ]
)
