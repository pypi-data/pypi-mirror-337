from typing import Dict, Any, List, Union
import pandas as pd

from ..utils import response_to_df


class ETFEndpoints:
    """Endpoints for retrieving ETF and mutual fund data."""

    def __init__(self, client):
        """
        Initialize the ETF endpoints.

        Args:
            client: The FMP client instance
        """
        self._client = client

    def holdings(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get ETF holdings.

        Args:
            symbol: ETF symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            ETF holdings or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("etf/holdings", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def info(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get ETF or mutual fund information.

        Args:
            symbol: ETF or mutual fund symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            ETF or mutual fund information or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("etf/info", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def country_weightings(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get ETF country weightings.

        Args:
            symbol: ETF symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            ETF country weightings or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("etf/country-weightings", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def asset_exposure(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get ETF asset exposure.

        Args:
            symbol: Stock symbol to check which ETFs hold it
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            ETF asset exposure or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("etf/asset-exposure", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def sector_weightings(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get ETF sector weightings.

        Args:
            symbol: ETF symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            ETF sector weightings or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("etf/sector-weightings", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def disclosure_holders_latest(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get latest mutual fund and ETF disclosure holders.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Latest disclosure holders or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("funds/disclosure-holders-latest", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "reportDate" in df.columns:
                df["reportDate"] = pd.to_datetime(df["reportDate"])
            return df
        return response

    def disclosure(
        self, symbol: str, year: int, quarter: int, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get mutual fund disclosures.

        Args:
            symbol: Mutual fund symbol
            year: Year of the disclosure
            quarter: Quarter of the disclosure (1-4)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Mutual fund disclosures or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol, "year": year, "quarter": quarter}

        response = self._client.get("funds/disclosure", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def disclosure_holders_search(
        self, name: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Search for mutual fund and ETF disclosure holders by name.

        Args:
            name: Fund name
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Disclosure holders or DataFrame if as_dataframe=True
        """
        params = {"name": name}

        response = self._client.get("funds/disclosure-holders-search", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def disclosure_dates(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get mutual fund and ETF disclosure dates.

        Args:
            symbol: Fund symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Disclosure dates or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("funds/disclosure-dates", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "reportDate" in df.columns:
                df["reportDate"] = pd.to_datetime(df["reportDate"])
            return df
        return response
