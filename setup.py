#!/usr/bin/env python3
"""
Setup script for HELIX-TTD-DBC-SUITCASE v0.3
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="helix-ttd-dbc-suitcase",
    version="0.3.1",
    author="Stephen Hope",
    author_email="helix.project.ai@helixprojectai.com",
    description="The missing identity & custody primitive for sovereign AI agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/helixprojectai-code/HELIX-TTD-DBC-SUITCASE-v0.3",
    
    # 1. FIND THE CLI PACKAGE (Crucial for cli/dbc_suitcase.py)
    packages=find_packages(),
    
    # 2. INCLUDE THE ROOT SCRIPT (Crucial for helix.py)
    py_modules=["helix"],
    
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.7",
    install_requires=[
        "cryptography>=41.0.0",
        "colorama>=0.4.6",
        "rich>=13.0.0",
        "streamlit>=1.30.0",
    ],
    entry_points={
        "console_scripts": [
            "helix=helix:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.json"],
    },
)
