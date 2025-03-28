from typing import Dict, Any, Optional, List, Union
import pandas as pd

from ..utils import validate_symbols, response_to_df, clean_params


class NewsEndpoints:
    """Endpoints for retrieving news and press releases."""

    def __init__(self, client):
        """
        Initialize the News endpoints.

        Args:
            client: The FMP client instance
        """
        self._client = client

    def fmp_articles(
        self,
        page: Optional[int] = 0,
        size: Optional[int] = 10,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get FMP articles.

        Args:
            page: Page number
            size: Number of articles per page
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            FMP articles or DataFrame if as_dataframe=True
        """
        params = clean_params({"page": page, "size": size})

        response = self._client.get("fmp-articles", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "publishedDate" in df.columns:
                df["publishedDate"] = pd.to_datetime(df["publishedDate"])
            return df
        return response

    def general_news(
        self, limit: Optional[int] = None, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get general news articles.

        Args:
            limit: Maximum number of news articles to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            General news articles or DataFrame if as_dataframe=True
        """
        params = clean_params({"limit": limit})

        response = self._client.get("news/general-latest", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "publishedDate" in df.columns:
                df["publishedDate"] = pd.to_datetime(df["publishedDate"])
            return df
        return response

    def press_releases(
        self, limit: Optional[int] = None, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get latest press releases.

        Args:
            limit: Maximum number of press releases to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Press releases or DataFrame if as_dataframe=True
        """
        params = clean_params({"limit": limit})

        response = self._client.get("news/press-releases-latest", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "publishedDate" in df.columns:
                df["publishedDate"] = pd.to_datetime(df["publishedDate"])
            return df
        return response

    def stock_news(
        self, limit: Optional[int] = None, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get latest stock news.

        Args:
            limit: Maximum number of news articles to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Stock news or DataFrame if as_dataframe=True
        """
        params = clean_params({"limit": limit})

        response = self._client.get("news/stock-latest", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "publishedDate" in df.columns:
                df["publishedDate"] = pd.to_datetime(df["publishedDate"])
            return df
        return response

    def crypto_news(
        self, limit: Optional[int] = None, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get latest cryptocurrency news.

        Args:
            limit: Maximum number of news articles to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Cryptocurrency news or DataFrame if as_dataframe=True
        """
        params = clean_params({"limit": limit})

        response = self._client.get("news/crypto-latest", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "publishedDate" in df.columns:
                df["publishedDate"] = pd.to_datetime(df["publishedDate"])
            return df
        return response

    def forex_news(
        self, limit: Optional[int] = None, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get latest forex news.

        Args:
            limit: Maximum number of news articles to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Forex news or DataFrame if as_dataframe=True
        """
        params = clean_params({"limit": limit})

        response = self._client.get("news/forex-latest", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "publishedDate" in df.columns:
                df["publishedDate"] = pd.to_datetime(df["publishedDate"])
            return df
        return response

    def search_press_releases(
        self,
        symbols: Union[str, List[str]],
        limit: Optional[int] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Search for press releases by symbol.

        Args:
            symbols: Stock symbol or list of symbols
            limit: Maximum number of press releases to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Press releases or DataFrame if as_dataframe=True
        """
        params = clean_params({"symbols": validate_symbols(symbols), "limit": limit})

        response = self._client.get("news/press-releases", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "publishedDate" in df.columns:
                df["publishedDate"] = pd.to_datetime(df["publishedDate"])
            return df
        return response

    def search_stock_news(
        self,
        symbols: Union[str, List[str]],
        limit: Optional[int] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Search for stock news by symbol.

        Args:
            symbols: Stock symbol or list of symbols
            limit: Maximum number of news articles to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Stock news or DataFrame if as_dataframe=True
        """
        params = clean_params({"symbols": validate_symbols(symbols), "limit": limit})

        response = self._client.get("news/stock", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "publishedDate" in df.columns:
                df["publishedDate"] = pd.to_datetime(df["publishedDate"])
            return df
        return response

    def search_crypto_news(
        self,
        symbols: Union[str, List[str]],
        limit: Optional[int] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Search for cryptocurrency news by symbol.

        Args:
            symbols: Cryptocurrency symbol or list of symbols
            limit: Maximum number of news articles to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Cryptocurrency news or DataFrame if as_dataframe=True
        """
        params = clean_params({"symbols": validate_symbols(symbols), "limit": limit})

        response = self._client.get("news/crypto", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "publishedDate" in df.columns:
                df["publishedDate"] = pd.to_datetime(df["publishedDate"])
            return df
        return response

    def search_forex_news(
        self,
        symbols: Union[str, List[str]],
        limit: Optional[int] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Search for forex news by symbol.

        Args:
            symbols: Forex pair or list of pairs
            limit: Maximum number of news articles to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Forex news or DataFrame if as_dataframe=True
        """
        params = clean_params({"symbols": validate_symbols(symbols), "limit": limit})

        response = self._client.get("news/forex", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "publishedDate" in df.columns:
                df["publishedDate"] = pd.to_datetime(df["publishedDate"])
            return df
        return response
