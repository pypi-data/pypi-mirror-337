from typing import Dict, Any, Optional, List, Union
import pandas as pd
from datetime import datetime, date

from ..utils import response_to_df, format_date


class SECEndpoints:
    """Endpoints for retrieving SEC filings data."""

    def __init__(self, client):
        """
        Initialize the SEC endpoints.

        Args:
            client: The FMP client instance
        """
        self._client = client

    def latest_8k_filings(
        self,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        limit: Optional[int] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get latest 8-K SEC filings.

        Args:
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            limit: Maximum number of filings to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Latest 8-K SEC filings or DataFrame if as_dataframe=True
        """
        params = {}

        if from_date:
            params["from"] = format_date(from_date)
        if to_date:
            params["to"] = format_date(to_date)
        if limit:
            params["limit"] = limit

        response = self._client.get("sec-filings-8k", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "filingDate" in df.columns:
                df["filingDate"] = pd.to_datetime(df["filingDate"])
            return df
        return response

    def latest_filings(
        self,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        limit: Optional[int] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get latest SEC filings.

        Args:
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            limit: Maximum number of filings to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Latest SEC filings or DataFrame if as_dataframe=True
        """
        params = {}

        if from_date:
            params["from"] = format_date(from_date)
        if to_date:
            params["to"] = format_date(to_date)
        if limit:
            params["limit"] = limit

        response = self._client.get("sec-filings-financials", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "filingDate" in df.columns:
                df["filingDate"] = pd.to_datetime(df["filingDate"])
            return df
        return response

    def filings_by_form_type(
        self,
        form_type: str,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        limit: Optional[int] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get SEC filings by form type.

        Args:
            form_type: SEC form type (e.g., '10-K', '10-Q', '8-K')
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            limit: Maximum number of filings to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            SEC filings by form type or DataFrame if as_dataframe=True
        """
        params = {"formType": form_type}

        if from_date:
            params["from"] = format_date(from_date)
        if to_date:
            params["to"] = format_date(to_date)
        if limit:
            params["limit"] = limit

        response = self._client.get("sec-filings-search/form-type", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "filingDate" in df.columns:
                df["filingDate"] = pd.to_datetime(df["filingDate"])
            return df
        return response

    def filings_by_symbol(
        self,
        symbol: str,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        limit: Optional[int] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get SEC filings by symbol.

        Args:
            symbol: Stock symbol
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            limit: Maximum number of filings to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            SEC filings by symbol or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        if from_date:
            params["from"] = format_date(from_date)
        if to_date:
            params["to"] = format_date(to_date)
        if limit:
            params["limit"] = limit

        response = self._client.get("sec-filings-search/symbol", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "filingDate" in df.columns:
                df["filingDate"] = pd.to_datetime(df["filingDate"])
            return df
        return response

    def filings_by_cik(
        self,
        cik: str,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        limit: Optional[int] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get SEC filings by CIK.

        Args:
            cik: Central Index Key (CIK)
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            limit: Maximum number of filings to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            SEC filings by CIK or DataFrame if as_dataframe=True
        """
        params = {"cik": cik}

        if from_date:
            params["from"] = format_date(from_date)
        if to_date:
            params["to"] = format_date(to_date)
        if limit:
            params["limit"] = limit

        response = self._client.get("sec-filings-search/cik", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "filingDate" in df.columns:
                df["filingDate"] = pd.to_datetime(df["filingDate"])
            return df
        return response

    def filings_by_name(
        self, company: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get SEC filings by company name.

        Args:
            company: Company name
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            SEC filings by company name or DataFrame if as_dataframe=True
        """
        params = {"company": company}

        response = self._client.get("sec-filings-company-search/name", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def company_search_by_symbol(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Search for company SEC filings by symbol.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Company search results or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("sec-filings-company-search/symbol", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def company_search_by_cik(
        self, cik: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Search for company SEC filings by CIK.

        Args:
            cik: Central Index Key (CIK)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Company search results or DataFrame if as_dataframe=True
        """
        params = {"cik": cik}

        response = self._client.get("sec-filings-company-search/cik", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def company_profile(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get SEC company profile.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            SEC company profile or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("sec-profile", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response
