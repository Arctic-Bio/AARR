#!/usr/bin/env python3
"""
Setup script for Aerodynamic Simulation System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aerodynamic-simulation-system",
    version="1.0.0",
    author="Aerodynamics Team",
    author_email="team@aerosim.com",
    description="Advanced Aerodynamic Simulation System with Beautiful GUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aerosim/aerodynamic-simulation-system",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PySide6>=6.5.0",
        "numpy>=1.21.0",
        "matplotlib>=3.5.0",
        "scipy>=1.7.0",
        "Pillow>=8.3.0",
        "pyqtgraph>=0.13.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-qt>=4.0",
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.910",
        ],
    },
    entry_points={
        "console_scripts": [
            "aerosim=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
)