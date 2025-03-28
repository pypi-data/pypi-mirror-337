from setuptools import setup, find_packages

setup(
    name="serp-geo-mcp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv",
        "fastmcp",
    ],
    author="anil kumar",
    author_email="anilkumarbaatula@gmail.com",
    description="A geo-location based MCP server using SerpApi",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/serp-geo-mcp",  # Optional
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)