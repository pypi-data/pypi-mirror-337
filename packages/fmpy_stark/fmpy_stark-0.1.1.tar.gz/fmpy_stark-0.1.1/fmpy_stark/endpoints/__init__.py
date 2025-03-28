"""
Endpoint modules for the Financial Modeling Prep API.

Each module corresponds to a category of endpoints in the FMP API.
"""

from .search import SearchEndpoints
from .company import CompanyEndpoints
from .quote import QuoteEndpoints
from .chart import ChartEndpoints
from .statements import StatementsEndpoints
from .analyst import AnalystEndpoints
from .calendar import CalendarEndpoints
from .news import NewsEndpoints
from .etf import ETFEndpoints
from .crypto import CryptoEndpoints
from .forex import ForexEndpoints
from .sec import SECEndpoints
from .bulk import BulkEndpoints
from .directory import DirectoryEndpoints

__all__ = [
    "SearchEndpoints",
    "CompanyEndpoints",
    "QuoteEndpoints",
    "ChartEndpoints",
    "StatementsEndpoints",
    "AnalystEndpoints",
    "CalendarEndpoints",
    "NewsEndpoints",
    "ETFEndpoints",
    "CryptoEndpoints",
    "ForexEndpoints",
    "SECEndpoints",
    "BulkEndpoints",
    "DirectoryEndpoints",
]
