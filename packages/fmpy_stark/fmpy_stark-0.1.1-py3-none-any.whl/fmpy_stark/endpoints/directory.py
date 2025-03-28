from typing import Dict, Any, List, Union
import pandas as pd

from ..utils import response_to_df


class DirectoryEndpoints:
    """Endpoints for retrieving directory listings and symbol information."""

    def __init__(self, client):
        """
        Initialize the Directory endpoints.

        Args:
            client: The FMP client instance
        """
        self._client = client

    def company_symbols(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get a list of all company symbols.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            List of company symbols or DataFrame if as_dataframe=True
        """
        response = self._client.get("stock-list")

        if as_dataframe:
            return response_to_df(response)
        return response

    def financial_statement_symbols(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get a list of companies with available financial statements.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            List of companies with financial statements or DataFrame if as_dataframe=True
        """
        response = self._client.get("financial-statement-symbol-list")

        if as_dataframe:
            return response_to_df(response)
        return response

    def cik_list(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get a list of all CIK (Central Index Key) numbers.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            List of CIK numbers or DataFrame if as_dataframe=True
        """
        response = self._client.get("cik-list")

        if as_dataframe:
            return response_to_df(response)
        return response

    def symbol_changes(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get a list of stock symbol changes due to mergers, acquisitions, etc.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            List of symbol changes or DataFrame if as_dataframe=True
        """
        response = self._client.get("symbol-change")

        if as_dataframe:
            return response_to_df(response)
        return response

    def etf_list(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get a list of all ETF symbols.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            List of ETF symbols or DataFrame if as_dataframe=True
        """
        response = self._client.get("etf-list")

        if as_dataframe:
            return response_to_df(response)
        return response

    def actively_trading_list(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get a list of all actively trading companies.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            List of actively trading companies or DataFrame if as_dataframe=True
        """
        response = self._client.get("actively-trading-list")

        if as_dataframe:
            return response_to_df(response)
        return response

    def earnings_transcript_list(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get a list of companies with available earnings transcripts.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            List of companies with earnings transcripts or DataFrame if as_dataframe=True
        """
        response = self._client.get("earnings-transcript-list")

        if as_dataframe:
            return response_to_df(response)
        return response

    def available_exchanges(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get a list of all available stock exchanges.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            List of available exchanges or DataFrame if as_dataframe=True
        """
        response = self._client.get("available-exchanges")

        if as_dataframe:
            return response_to_df(response)
        return response

    def available_sectors(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get a list of all available sectors.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            List of available sectors or DataFrame if as_dataframe=True
        """
        response = self._client.get("available-sectors")

        if as_dataframe:
            return response_to_df(response)
        return response

    def available_industries(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get a list of all available industries.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            List of available industries or DataFrame if as_dataframe=True
        """
        response = self._client.get("available-industries")

        if as_dataframe:
            return response_to_df(response)
        return response

    def available_countries(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get a list of all available countries.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            List of available countries or DataFrame if as_dataframe=True
        """
        response = self._client.get("available-countries")

        if as_dataframe:
            return response_to_df(response)
        return response
