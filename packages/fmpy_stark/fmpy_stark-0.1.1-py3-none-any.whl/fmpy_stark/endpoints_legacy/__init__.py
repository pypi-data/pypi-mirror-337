"""
Legacy endpoint modules for the Financial Modeling Prep API.

Each module corresponds to a category of legacy endpoints in the FMP API.
These endpoints are expected to be retired in 2025/2026.
"""

from .bulk import BulkEndpointsLegacy

__all__ = [
    "BulkEndpointsLegacy",
]
