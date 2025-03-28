from typing import Dict, Any, Optional, List, Union
import pandas as pd

from ..utils import response_to_df, clean_params


class SearchEndpoints:
    """Endpoints for searching stock symbols and company information."""

    def __init__(self, client):
        """
        Initialize the Search endpoints.

        Args:
            client: The FMP client instance
        """
        self._client = client

    def symbol(
        self,
        query: str,
        limit: Optional[int] = None,
        exchange: Optional[str] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Search for a stock symbol by company name or ticker.

        Args:
            query: The search query (company name or ticker)
            limit: Maximum number of results to return
            exchange: Filter by exchange (e.g., "NASDAQ")
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            List of matching companies or DataFrame if as_dataframe=True
        """
        params = clean_params({"query": query, "limit": limit, "exchange": exchange})

        response = self._client.get("search-symbol", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def company_name(
        self,
        query: str,
        limit: Optional[int] = None,
        exchange: Optional[str] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Search for companies by name.

        Args:
            query: The company name to search for
            limit: Maximum number of results to return
            exchange: Filter by exchange (e.g., "NASDAQ")
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            List of matching companies or DataFrame if as_dataframe=True
        """
        params = clean_params({"query": query, "limit": limit, "exchange": exchange})

        response = self._client.get("search-name", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def cik(
        self, cik: str, limit: Optional[int] = None, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Search for a company by CIK (Central Index Key).

        Args:
            cik: The CIK number
            limit: Maximum number of results to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            List of matching companies or DataFrame if as_dataframe=True
        """
        params = clean_params({"cik": cik, "limit": limit})

        response = self._client.get("search-cik", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def cusip(
        self, cusip: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Search for a company by CUSIP number.

        Args:
            cusip: The CUSIP number
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            List of matching companies or DataFrame if as_dataframe=True
        """
        params = {"cusip": cusip}

        response = self._client.get("search-cusip", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def isin(
        self, isin: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Search for a company by ISIN (International Securities Identification Number).

        Args:
            isin: The ISIN number
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            List of matching companies or DataFrame if as_dataframe=True
        """
        params = {"isin": isin}

        response = self._client.get("search-isin", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def screener(
        self,
        market_cap_more_than: Optional[int] = None,
        market_cap_lower_than: Optional[int] = None,
        sector: Optional[str] = None,
        industry: Optional[str] = None,
        beta_more_than: Optional[float] = None,
        beta_lower_than: Optional[float] = None,
        price_more_than: Optional[float] = None,
        price_lower_than: Optional[float] = None,
        dividend_more_than: Optional[float] = None,
        dividend_lower_than: Optional[float] = None,
        volume_more_than: Optional[int] = None,
        volume_lower_than: Optional[int] = None,
        exchange: Optional[str] = None,
        country: Optional[str] = None,
        is_etf: Optional[bool] = None,
        is_fund: Optional[bool] = None,
        is_actively_trading: Optional[bool] = None,
        limit: Optional[int] = None,
        include_all_share_classes: Optional[bool] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Screen for stocks based on various criteria.

        Args:
            market_cap_more_than: Minimum market capitalization
            market_cap_lower_than: Maximum market capitalization
            sector: Filter by sector
            industry: Filter by industry
            beta_more_than: Minimum beta value
            beta_lower_than: Maximum beta value
            price_more_than: Minimum stock price
            price_lower_than: Maximum stock price
            dividend_more_than: Minimum dividend
            dividend_lower_than: Maximum dividend
            volume_more_than: Minimum trading volume
            volume_lower_than: Maximum trading volume
            exchange: Filter by exchange
            country: Filter by country
            is_etf: Filter for ETFs
            is_fund: Filter for funds
            is_actively_trading: Filter for actively trading stocks
            limit: Maximum number of results to return
            include_all_share_classes: Include all share classes
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            List of matching stocks or DataFrame if as_dataframe=True
        """
        params = clean_params(
            {
                "marketCapMoreThan": market_cap_more_than,
                "marketCapLowerThan": market_cap_lower_than,
                "sector": sector,
                "industry": industry,
                "betaMoreThan": beta_more_than,
                "betaLowerThan": beta_lower_than,
                "priceMoreThan": price_more_than,
                "priceLowerThan": price_lower_than,
                "dividendMoreThan": dividend_more_than,
                "dividendLowerThan": dividend_lower_than,
                "volumeMoreThan": volume_more_than,
                "volumeLowerThan": volume_lower_than,
                "exchange": exchange,
                "country": country,
                "isEtf": is_etf,
                "isFund": is_fund,
                "isActivelyTrading": is_actively_trading,
                "limit": limit,
                "includeAllShareClasses": include_all_share_classes,
            }
        )

        response = self._client.get("company-screener", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def exchange_variants(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Search for stock variants on different exchanges.

        Args:
            symbol: The stock symbol to search for
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            List of exchange variants or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("search-exchange-variants", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response
