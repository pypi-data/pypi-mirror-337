import os
import requests
from typing import Dict, Any, Optional, Union, List
from urllib.parse import urljoin
import pandas as pd
from .exceptions import FMPError, FMPRequestError, FMPAPIError
from .config import BASE_URL
from .endpoints import (
    SearchEndpoints,
    CompanyEndpoints,
    QuoteEndpoints,
    ChartEndpoints,
    StatementsEndpoints,
    AnalystEndpoints,
    CalendarEndpoints,
    NewsEndpoints,
    ETFEndpoints,
    CryptoEndpoints,
    ForexEndpoints,
    SECEndpoints,
    BulkEndpoints,
    DirectoryEndpoints,
)


class FMPClient:
    """
    Client for the Financial Modeling Prep API.

    This client handles authentication and requests to the FMP API.
    """

    def __init__(self, api_key: str = None):
        """
        Initialize the FMP client.

        Args:
            api_key: Your FMP API key. If not provided, the client will look for
                    an environment variable called FMP_API_KEY.
        """
        self.api_key = api_key or os.environ.get("FMP_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key is required. Pass it as api_key parameter or set FMP_API_KEY environment variable."
            )

        self.session = requests.Session()

    def _get_url(self, endpoint: str) -> str:
        """
        Construct the full URL for the given endpoint.

        Args:
            endpoint: The API endpoint path.

        Returns:
            The full URL including the base URL.
        """
        return urljoin(BASE_URL, endpoint)

    def _add_api_key(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add the API key to the request parameters.

        Args:
            params: The request parameters.

        Returns:
            The parameters with the API key added.
        """
        if params is None:
            params = {}

        if any(params):
            params["apikey"] = self.api_key
        else:
            params = {"apikey": self.api_key}

        return params

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expect_csv: bool = False,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], pd.DataFrame]:
        """
        Make a request to the FMP API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            data: Request body for POST/PUT requests
            headers: Request headers
            expect_csv: If True, expect a CSV response instead of JSON

        Returns:
            The response data as a dictionary, list, or pandas DataFrame (for CSV)

        Raises:
            FMPRequestError: If the request fails
            FMPAPIError: If the API returns an error
        """
        url = self._get_url(endpoint)
        params = self._add_api_key(params)

        try:
            response = self.session.request(
                method=method, url=url, params=params, json=data, headers=headers
            )
            response.raise_for_status()

            if expect_csv:
                # Handle CSV response
                try:
                    import io
                    import pandas as pd

                    return pd.read_csv(io.StringIO(response.text))
                except Exception as e:
                    raise FMPAPIError(f"Failed to parse CSV response: {str(e)}")
            else:
                # Handle JSON response
                try:
                    response_data = response.json()
                except ValueError:
                    # Try to handle it as CSV if JSON parsing fails - but only if autodiscovery is active
                    if (
                        len(response.text) > 0
                        and response.text[0] in ['"', ","]
                        and "," in response.text
                    ):
                        try:
                            import io
                            import pandas as pd

                            return pd.read_csv(io.StringIO(response.text))
                        except Exception:
                            # If both JSON and CSV parsing fail, raise the original JSON error
                            raise FMPAPIError(
                                f"Invalid JSON response: {response.text[:500]}..."
                            )
                    else:
                        # Not likely a CSV, raise the original JSON error
                        raise FMPAPIError(
                            f"Invalid JSON response: {response.text[:500]}..."
                        )

                # FMP API sometimes returns an empty list or dictionary for no results
                if not response_data and not isinstance(response_data, (list, dict)):
                    return []

                return response_data

        except requests.exceptions.RequestException as e:
            raise FMPRequestError(f"Request failed: {str(e)}")
        except Exception as e:
            # Don't catch our own custom exceptions
            if isinstance(e, FMPError):
                raise
            # Catch any other unexpected exceptions and wrap them
            raise FMPRequestError(f"Unexpected error: {str(e)}")

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        expect_csv: bool = False,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], pd.DataFrame]:
        """
        Make a GET request to the FMP API.

        Args:
            endpoint: API endpoint path
            params: Query parameters
            expect_csv: If True, expect a CSV response instead of JSON

        Returns:
            The response data
        """
        return self._request("GET", endpoint, params=params, expect_csv=expect_csv)

    def post(
        self,
        endpoint: str,
        data: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None,
        expect_csv: bool = False,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], pd.DataFrame]:
        """
        Make a POST request to the FMP API.

        Args:
            endpoint: API endpoint path
            data: Request body
            params: Query parameters
            expect_csv: If True, expect a CSV response instead of JSON

        Returns:
            The response data
        """
        return self._request(
            "POST", endpoint, params=params, data=data, expect_csv=expect_csv
        )

    @property
    def search(self) -> SearchEndpoints:
        """
        Get the search endpoints.

        Returns:
            The search endpoints
        """
        return SearchEndpoints(self)

    @property
    def company(self) -> CompanyEndpoints:
        """
        Get the company endpoints.

        Returns:
            The company endpoints
        """
        return CompanyEndpoints(self)

    @property
    def quote(self) -> QuoteEndpoints:
        """
        Get the quote endpoints.

        Returns:
            The quote endpoints
        """
        return QuoteEndpoints(self)

    @property
    def chart(self) -> ChartEndpoints:
        """
        Get the chart endpoints.

        Returns:
            The chart endpoints
        """
        return ChartEndpoints(self)

    @property
    def statements(self) -> StatementsEndpoints:
        """
        Get the financial statements endpoints.

        Returns:
            The statements endpoints
        """
        return StatementsEndpoints(self)

    @property
    def analyst(self) -> AnalystEndpoints:
        """
        Get the analyst endpoints.

        Returns:
            The analyst endpoints
        """
        return AnalystEndpoints(self)

    @property
    def calendar(self) -> CalendarEndpoints:
        """
        Get the calendar endpoints.

        Returns:
            The calendar endpoints
        """
        return CalendarEndpoints(self)

    @property
    def news(self) -> NewsEndpoints:
        """
        Get the news endpoints.

        Returns:
            The news endpoints
        """
        return NewsEndpoints(self)

    @property
    def etf(self) -> ETFEndpoints:
        """
        Get the ETF and mutual fund endpoints.

        Returns:
            The ETF endpoints
        """
        return ETFEndpoints(self)

    @property
    def crypto(self) -> CryptoEndpoints:
        """
        Get the cryptocurrency endpoints.

        Returns:
            The cryptocurrency endpoints
        """
        return CryptoEndpoints(self)

    @property
    def forex(self) -> ForexEndpoints:
        """
        Get the forex endpoints.

        Returns:
            The forex endpoints
        """
        return ForexEndpoints(self)

    @property
    def sec(self) -> SECEndpoints:
        """
        Get the SEC filings endpoints.

        Returns:
            The SEC filings endpoints
        """
        return SECEndpoints(self)

    @property
    def bulk(self) -> BulkEndpoints:
        """
        Get the bulk data endpoints.

        Returns:
            The bulk data endpoints
        """
        return BulkEndpoints(self)

    @property
    def directory(self) -> DirectoryEndpoints:
        """
        Get the directory endpoints for listings and symbols information.

        Returns:
            The directory endpoints
        """
        return DirectoryEndpoints(self)
