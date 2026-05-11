"""Setup script for AutoDiag Pro"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="autodiag-pro",
    version="1.0.0",
    author="AutoDiag Pro Team",
    author_email="support@autodiag-pro.com",
    description="Professional Automotive Diagnostic Tool for OBD/ELM interfaces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/autodiag-pro",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: Microsoft :: Windows :: Windows 8",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "autodiag=main:main",
            "autodiag-cli=interfaces.cli:main",
            "autodiag-gui=interfaces.gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "assets": ["*.ico", "*.png"],
    },
)
