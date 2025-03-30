from setuptools import setup, find_packages

setup(
    name="sql-connector-mcp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy",
        "pymysql",
        "fastmcp",
    ],
    author="Battula Anil Kumar",
    author_email="anilkumarbaatula@gmail.com",
    description="An MCP server for SQL database connectivity",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)