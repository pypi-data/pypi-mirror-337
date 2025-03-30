from setuptools import setup, find_packages

# Fix for UnicodeDecodeError when reading the README file
def read_file(filename):
    with open(filename, encoding="utf-8") as f:
        return f.read()

setup(
    name="botintel-sdk",
    version="0.0.3",
    packages=find_packages(exclude=["tests", "examples"]),  # Excluding unnecessary directories
    install_requires=[
        'requests>=2.25.1,<3.0.0',  # Added upper version limit for requests
    ],
    author="Abdullah Huseynli",
    author_email="botintelai1@gmail.com",
    description="Official Python SDK for BotIntel API",
    long_description=read_file("README.md"),  # Reading README.md for the long description
    long_description_content_type="text/markdown",  # Ensure Markdown content is parsed
    url="https://github.com/DeveleplorAbdullahH/botintel",  # Double-check repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Specify minimum version of Python
)