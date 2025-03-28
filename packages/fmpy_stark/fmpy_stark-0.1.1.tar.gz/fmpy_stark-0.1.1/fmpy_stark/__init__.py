"""
FMPY: Python SDK for Financial Modeling Prep API
================================================

A Python wrapper for the Financial Modeling Prep API that provides
easy access to financial data, stock quotes, and company information.

Example:
    >>> import fmpy
    >>> client = fmpy.Client(api_key="your_api_key")
    >>> apple_profile = client.company.profile("AAPL")
    >>> apple_quote = client.quote.real_time("AAPL")

    # Use the legacy client for v3 API endpoints
    >>> legacy_client = fmpy.ClientLegacy(api_key="your_api_key")
    >>> bulk_profiles = legacy_client.bulk.company_profiles(part=0)
"""

__version__ = "0.1.1"

from .client import FMPClient
from .client_legacy import FMPClientLegacy
from .exceptions import FMPError, FMPRequestError, FMPAPIError, FMPValidationError
from .utils import (
    validate_date,
    format_date,
    validate_symbols,
    response_to_df,
    clean_params,
)

# Create more user-friendly aliases
Client = FMPClient
ClientLegacy = FMPClientLegacy

__all__ = [
    "Client",
    "FMPClient",
    "ClientLegacy",
    "FMPClientLegacy",
    "FMPError",
    "FMPRequestError",
    "FMPAPIError",
    "FMPValidationError",
    "validate_date",
    "format_date",
    "validate_symbols",
    "response_to_df",
    "clean_params",
]
