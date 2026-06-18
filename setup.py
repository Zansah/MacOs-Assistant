"""Setup script for April (legacy fallback)."""

from setuptools import setup, find_packages

setup(
    name="april",
    version="0.1.0",
    description="April — macOS Voice Assistant & Shortcuts Vault",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.11",
    install_requires=[
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.1",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "black>=23.12.0",
            "ruff>=0.1.6",
            "mypy>=1.7.0",
            "pre-commit>=3.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "april=april.main:main",
        ],
    },
)