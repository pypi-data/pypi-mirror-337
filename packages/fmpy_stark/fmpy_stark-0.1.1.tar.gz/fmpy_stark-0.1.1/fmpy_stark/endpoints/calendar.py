from typing import Dict, Any, Optional, List, Union
import pandas as pd
from datetime import datetime, date

from ..utils import response_to_df, format_date, clean_params


class CalendarEndpoints:
    """Endpoints for retrieving calendar data like earnings, dividends, IPOs, etc."""

    def __init__(self, client):
        """
        Initialize the Calendar endpoints.

        Args:
            client: The FMP client instance
        """
        self._client = client

    def dividends(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get dividend history for a company.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Dividend history or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("dividends", params=params)

        if as_dataframe:
            df = response_to_df(response)
            for date_column in [
                "date",
                "recordDate",
                "paymentDate",
                "declarationDate",
                "adjustedDividend",
            ]:
                if not df.empty and date_column in df.columns:
                    df[date_column] = pd.to_datetime(df[date_column])
            return df
        return response

    def dividends_calendar(
        self,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get dividends calendar.

        Args:
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Dividends calendar or DataFrame if as_dataframe=True
        """
        params = {}

        if from_date:
            params["from"] = format_date(from_date)
        if to_date:
            params["to"] = format_date(to_date)

        response = self._client.get("dividends-calendar", params=params)

        if as_dataframe:
            df = response_to_df(response)
            for date_column in ["date", "recordDate", "paymentDate", "declarationDate"]:
                if not df.empty and date_column in df.columns:
                    df[date_column] = pd.to_datetime(df[date_column])
            return df
        return response

    def earnings(
        self, symbol: str, limit: Optional[int] = None, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get earnings reports for a company.

        Args:
            symbol: Stock symbol
            limit: Maximum number of reports to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Earnings reports or DataFrame if as_dataframe=True
        """
        params = clean_params({"symbol": symbol, "limit": limit})

        response = self._client.get("earnings", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def earnings_calendar(
        self,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get earnings calendar.

        Args:
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Earnings calendar or DataFrame if as_dataframe=True
        """
        params = {}

        if from_date:
            params["from"] = format_date(from_date)
        if to_date:
            params["to"] = format_date(to_date)

        response = self._client.get("earnings-calendar", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def ipos_calendar(
        self,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get IPOs calendar.

        Args:
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            IPOs calendar or DataFrame if as_dataframe=True
        """
        params = {}

        if from_date:
            params["from"] = format_date(from_date)
        if to_date:
            params["to"] = format_date(to_date)

        response = self._client.get("ipos-calendar", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def ipos_disclosure(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get IPOs disclosure filings.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            IPOs disclosure filings or DataFrame if as_dataframe=True
        """
        response = self._client.get("ipos-disclosure")

        if as_dataframe:
            df = response_to_df(response)
            for date_column in ["filingDate", "effectivenessDate"]:
                if not df.empty and date_column in df.columns:
                    df[date_column] = pd.to_datetime(df[date_column])
            return df
        return response

    def ipos_prospectus(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get IPOs prospectus information.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            IPOs prospectus information or DataFrame if as_dataframe=True
        """
        response = self._client.get("ipos-prospectus")

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def stock_splits(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get stock split history for a company.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Stock split history or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("splits", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def stock_splits_calendar(
        self,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get stock splits calendar.

        Args:
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Stock splits calendar or DataFrame if as_dataframe=True
        """
        params = {}

        if from_date:
            params["from"] = format_date(from_date)
        if to_date:
            params["to"] = format_date(to_date)

        response = self._client.get("splits-calendar", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response
