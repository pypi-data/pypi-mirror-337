#!/usr/bin/env python
from setuptools import setup, find_packages
import os

# Read the README file if it exists
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
long_description = ""
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    # Use client_readme.md if README.md doesn't exist
    client_readme_path = os.path.join(os.path.dirname(__file__), "client_readme.md")
    if os.path.exists(client_readme_path):
        with open(client_readme_path, "r", encoding="utf-8") as fh:
            long_description = fh.read()

# Define requirements directly instead of reading from file
requirements = [
    "requests>=2.25.0",
    "pydantic>=2.0.0",
    "python-dateutil>=2.8.1",
    "urllib3>=1.26.0",
    "azure-storage-table>=2.0.0",
    "azure-storage-blob>=12.0.0",
    "azure-identity>=1.5.0",
]

setup(
    name="auth-api-client",
    version="1.0.1",  # Incrementing version for 404 handling fix
    author="Perceptive Focus",
    author_email="info@perceptivefocus.com",
    description="A robust client for interacting with the Auth API service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/perceptivefocus/auth",
    packages=find_packages(),
    py_modules=["client"],  # Include the client.py module directly
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    keywords="api, authentication, client, api-key",
    project_urls={
        "Bug Tracker": "https://github.com/perceptivefocus/auth/issues",
        "Documentation": "https://github.com/perceptivefocus/auth/blob/main/api_keys/README.md",
        "Source Code": "https://github.com/perceptivefocus/auth",
    },
) 