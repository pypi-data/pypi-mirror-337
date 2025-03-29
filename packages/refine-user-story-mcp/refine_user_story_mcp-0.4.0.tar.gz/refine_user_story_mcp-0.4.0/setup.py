from setuptools import setup, find_packages
import os

# Read the contents of README.md
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="refine-user-story-mcp",
    version="0.4.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "python-dotenv>=1.0.0",
        "fastmcp>=0.1.0",
        "langchain_groq>=0.1.0",
        "langchain>=0.1.0"
    ],
    author="B. Anil Kumar",
    author_email="anilkumarbaatula@gmail.com",
    description="A tool for analyzing user stories using the INVEST criteria",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/yourusername/refine-user-story-mcp",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "user-story-invest=refine_user_story_mcp.server:main",
        ],
    },
)