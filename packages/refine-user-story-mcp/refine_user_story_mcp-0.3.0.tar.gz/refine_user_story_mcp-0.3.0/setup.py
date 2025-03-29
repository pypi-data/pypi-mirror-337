from setuptools import setup, find_packages

setup(
    name="refine-user-story-mcp",
    version="0.3.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv",
        "fastmcp",
        "langchain_groq",
        "langchain"

    ],
    author="B. Anil Kumar",
    author_email="anilkumarbaatula@gmail.com",
    description="A refine user story MCP server",
    long_description_content_type="text/markdown",
)