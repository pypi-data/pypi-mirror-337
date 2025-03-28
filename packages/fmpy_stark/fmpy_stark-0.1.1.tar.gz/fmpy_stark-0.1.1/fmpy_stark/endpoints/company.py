from typing import Dict, Any, List, Union
import pandas as pd

from ..utils import validate_symbols, response_to_df


class CompanyEndpoints:
    """Endpoints for retrieving company information."""

    def __init__(self, client):
        """
        Initialize the Company endpoints.

        Args:
            client: The FMP client instance
        """
        self._client = client

    def profile(
        self, symbol: Union[str, List[str]], as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get company profile data.

        Args:
            symbol: Stock symbol or list of symbols
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Company profile data or DataFrame if as_dataframe=True
        """
        params = {"symbol": validate_symbols(symbol)}

        response = self._client.get("profile", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def profile_by_cik(
        self, cik: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get company profile data by CIK number.

        Args:
            cik: CIK number
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Company profile data or DataFrame if as_dataframe=True
        """
        params = {"cik": cik}

        response = self._client.get("profile-cik", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def notes(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get company notes.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Company notes or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("company-notes", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def peers(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get company peers (similar companies).

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            List of peer companies or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("stock-peers", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def delisted_companies(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get list of delisted companies.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            List of delisted companies or DataFrame if as_dataframe=True
        """
        response = self._client.get("delisted-companies")

        if as_dataframe:
            return response_to_df(response)
        return response

    def employee_count(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get company employee count.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Employee count data or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("employee-count", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def historical_employee_count(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get historical employee count for a company.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Historical employee count data or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("historical-employee-count", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def market_cap(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get company market capitalization.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Market capitalization data or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("market-capitalization", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def batch_market_cap(
        self, symbols: Union[str, List[str]], as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get market capitalization for multiple companies.

        Args:
            symbols: Stock symbols
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Market capitalization data or DataFrame if as_dataframe=True
        """
        params = {"symbols": validate_symbols(symbols)}

        response = self._client.get("market-capitalization-batch", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def historical_market_cap(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get historical market capitalization for a company.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Historical market capitalization data or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("historical-market-capitalization", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def shares_float(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get company shares float and liquidity information.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Shares float data or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("shares-float", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def all_shares_float(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get shares float for all companies.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Shares float data for all companies or DataFrame if as_dataframe=True
        """
        response = self._client.get("shares-float-all")

        if as_dataframe:
            return response_to_df(response)
        return response

    def executives(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get company executives information.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Company executives data or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("key-executives", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def executive_compensation(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get company executive compensation information.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Executive compensation data or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("governance-executive-compensation", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def executive_compensation_benchmark(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get executive compensation benchmark across industries.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Executive compensation benchmark data or DataFrame if as_dataframe=True
        """
        response = self._client.get("executive-compensation-benchmark")

        if as_dataframe:
            return response_to_df(response)
        return response
