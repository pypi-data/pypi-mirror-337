# updated setup.py for implementing with PyPI
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pubmed-citation-update",
    version="0.1.5",  # Increment version for the update
    author="Armelle,Brandon,Shanta",
    author_email="your.email@example.com",
    description="A tool for collecting citation data from PubMed and analyzing author relationships",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pubmed-citation",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/pubmed-citation/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
        "numpy>=1.19.0",  # Required for numerical operations
        "scipy>=1.5.0",  # Required for spectral clustering
    ],
    extras_require={
        "viz": ["networkx>=2.5", "matplotlib>=3.3.0"],  # For visualization
    },
    entry_points={
        "console_scripts": [
            "pubmed-citation=pubmed_citation.cli:main",
        ],
    },
)
