from typing import Dict, Any, Optional, List, Union
import pandas as pd
from datetime import datetime, date

from ..utils import response_to_df, format_date


class CryptoEndpoints:
    """Endpoints for retrieving cryptocurrency data."""

    def __init__(self, client):
        """
        Initialize the Crypto endpoints.

        Args:
            client: The FMP client instance
        """
        self._client = client

    def list(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get list of available cryptocurrencies.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            List of cryptocurrencies or DataFrame if as_dataframe=True
        """
        response = self._client.get("cryptocurrency-list")

        if as_dataframe:
            return response_to_df(response)
        return response

    def quote(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get cryptocurrency quote.

        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTCUSD')
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Cryptocurrency quote or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("quote", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def quote_short(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get short cryptocurrency quote.

        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTCUSD')
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Short cryptocurrency quote or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("quote-short", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def batch_quotes(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get batch cryptocurrency quotes.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Batch cryptocurrency quotes or DataFrame if as_dataframe=True
        """
        response = self._client.get("batch-crypto-quotes")

        if as_dataframe:
            return response_to_df(response)
        return response

    def historical_price_snapshot(
        self,
        symbol: str,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get historical cryptocurrency price snapshot.

        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTCUSD')
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Historical cryptocurrency price snapshot or DataFrame if as_dataframe=True
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

    def historical_price_full(
        self,
        symbol: str,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get full historical cryptocurrency price data.

        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTCUSD')
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Full historical cryptocurrency price data or DataFrame if as_dataframe=True
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

    def intraday_1min(
        self,
        symbol: str,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get 1-minute intraday cryptocurrency price data.

        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTCUSD')
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            1-minute intraday cryptocurrency price data or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        if from_date:
            params["from"] = format_date(from_date)
        if to_date:
            params["to"] = format_date(to_date)

        response = self._client.get("historical-chart/1min", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def intraday_5min(
        self,
        symbol: str,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get 5-minute intraday cryptocurrency price data.

        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTCUSD')
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            5-minute intraday cryptocurrency price data or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        if from_date:
            params["from"] = format_date(from_date)
        if to_date:
            params["to"] = format_date(to_date)

        response = self._client.get("historical-chart/5min", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def intraday_1hour(
        self,
        symbol: str,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get 1-hour intraday cryptocurrency price data.

        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTCUSD')
            from_date: Start date (format: YYYY-MM-DD)
            to_date: End date (format: YYYY-MM-DD)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            1-hour intraday cryptocurrency price data or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        if from_date:
            params["from"] = format_date(from_date)
        if to_date:
            params["to"] = format_date(to_date)

        response = self._client.get("historical-chart/1hour", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response
