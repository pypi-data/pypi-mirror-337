#!/usr/bin/env python
"""
Setup script for pica-ai package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pica-ai",
    version="0.1.0",
    author="Pica",
    author_email="support@picaos.com",
    description="Client for interacting with the Pica API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/picahq/pica-ai",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests==2.32.3",
        "requests-toolbelt==1.0.0",
        "pydantic==2.11.1",
        "pytest==8.3.5",
    ],
) 