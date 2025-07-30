"""
Setup configuration for Nihon CLI.

This setup script configures the Nihon CLI package for installation
and creates the 'nihon' command-line tool.
"""

import os

from setuptools import find_packages, setup


def read_long_description():
    """Read the long description from README.md if it exists."""
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "A Python-based CLI tool for learning Japanese characters (Hiragana and Katakana)."


setup(
    name="nihon-cli",
    version="0.1.0",
    author="Nihon CLI Team",
    author_email="",
    description="A CLI tool for learning Japanese characters",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/nihon-cli",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "nihon=nihon_cli.main:main",
        ],
    },
    keywords="japanese hiragana katakana learning cli education",
    project_urls={
        "Bug Reports": "https://github.com/your-username/nihon-cli/issues",
        "Source": "https://github.com/your-username/nihon-cli",
    },
)
