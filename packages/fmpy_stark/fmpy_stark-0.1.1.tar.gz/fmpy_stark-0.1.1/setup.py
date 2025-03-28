from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fmpy_stark",
    version="0.1.1",
    author="Jimmy",
    author_email="skylinezum@users.noreply.github.com",
    description="Python SDK for Financial Modeling Prep API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stark-tech-space/fmpy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.12",
    install_requires=[
        "requests>=2.32.3",
        "pandas>=2.2.3",
        "python-dateutil>=2.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.12.0",
            "black>=21.5b2",
            "isort>=5.9.1",
            "mypy>=0.812",
            "flake8>=3.9.2",
        ],
        "docs": [
            "sphinx>=4.0.2",
            "sphinx-rtd-theme>=0.5.2",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/stark-tech-space/fmpy/issues",
        "Source": "https://github.com/stark-tech-space/fmpy",
        "Documentation": "https://github.com/stark-tech-space/fmpy",
    },
)
