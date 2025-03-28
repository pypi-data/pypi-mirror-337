from typing import Dict, Any, Optional, List, Union
import pandas as pd
from datetime import datetime, date

from ..utils import response_to_df, format_date


class ChartEndpoints:
    """Endpoints for retrieving price chart data."""

    def __init__(self, client):
        """
        Initialize the Chart endpoints.

        Args:
            client: The FMP client instance
        """
        self._client = client

    def basic(
        self,
        symbol: str,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get basic stock chart data (EOD prices).

        Args:
            symbol: Stock symbol
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Basic chart data or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        if from_date:
            params["from"] = format_date(from_date)
        if to_date:
            params["to"] = format_date(to_date)

        response = self._client.get("historical-price-eod/light", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def full(
        self,
        symbol: str,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get full stock chart data (EOD prices with OHLCV).

        Args:
            symbol: Stock symbol
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Full chart data or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        if from_date:
            params["from"] = format_date(from_date)
        if to_date:
            params["to"] = format_date(to_date)

        response = self._client.get("historical-price-eod/full", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def unadjusted(
        self,
        symbol: str,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get unadjusted stock chart data (no split adjustments).

        Args:
            symbol: Stock symbol
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Unadjusted chart data or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        if from_date:
            params["from"] = format_date(from_date)
        if to_date:
            params["to"] = format_date(to_date)

        response = self._client.get(
            "historical-price-eod/non-split-adjusted", params=params
        )

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def dividend_adjusted(
        self,
        symbol: str,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get dividend-adjusted stock chart data.

        Args:
            symbol: Stock symbol
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Dividend-adjusted chart data or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        if from_date:
            params["from"] = format_date(from_date)
        if to_date:
            params["to"] = format_date(to_date)

        response = self._client.get(
            "historical-price-eod/dividend-adjusted", params=params
        )

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def _get_intraday_chart(
        self,
        interval: str,
        symbol: str,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Helper method to get intraday chart data.

        Args:
            interval: Time interval (1min, 5min, 15min, 30min, 1hour, 4hour)
            symbol: Stock symbol
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Intraday chart data or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        if from_date:
            params["from"] = format_date(from_date)
        if to_date:
            params["to"] = format_date(to_date)

        response = self._client.get(f"historical-chart/{interval}", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def one_minute(
        self,
        symbol: str,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get 1-minute interval stock chart data.

        Args:
            symbol: Stock symbol
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            1-minute interval chart data or DataFrame if as_dataframe=True
        """
        return self._get_intraday_chart(
            "1min", symbol, from_date, to_date, as_dataframe
        )

    def five_minute(
        self,
        symbol: str,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get 5-minute interval stock chart data.

        Args:
            symbol: Stock symbol
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            5-minute interval chart data or DataFrame if as_dataframe=True
        """
        return self._get_intraday_chart(
            "5min", symbol, from_date, to_date, as_dataframe
        )

    def fifteen_minute(
        self,
        symbol: str,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get 15-minute interval stock chart data.

        Args:
            symbol: Stock symbol
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            15-minute interval chart data or DataFrame if as_dataframe=True
        """
        return self._get_intraday_chart(
            "15min", symbol, from_date, to_date, as_dataframe
        )

    def thirty_minute(
        self,
        symbol: str,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get 30-minute interval stock chart data.

        Args:
            symbol: Stock symbol
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            30-minute interval chart data or DataFrame if as_dataframe=True
        """
        return self._get_intraday_chart(
            "30min", symbol, from_date, to_date, as_dataframe
        )

    def one_hour(
        self,
        symbol: str,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get 1-hour interval stock chart data.

        Args:
            symbol: Stock symbol
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            1-hour interval chart data or DataFrame if as_dataframe=True
        """
        return self._get_intraday_chart(
            "1hour", symbol, from_date, to_date, as_dataframe
        )

    def four_hour(
        self,
        symbol: str,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get 4-hour interval stock chart data.

        Args:
            symbol: Stock symbol
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            4-hour interval chart data or DataFrame if as_dataframe=True
        """
        return self._get_intraday_chart(
            "4hour", symbol, from_date, to_date, as_dataframe
        )

    def batch_eod(
        self, date: Union[str, datetime, date], as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get EOD prices for all stocks on a specific date.

        Args:
            date: Date for which to get EOD data (format: YYYY-MM-DD)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Batch EOD data or DataFrame if as_dataframe=True
        """
        params = {"date": format_date(date)}

        response = self._client.get("batch-eod", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response
