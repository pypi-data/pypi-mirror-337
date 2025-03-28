from typing import Dict, Any, Optional, List, Union
import pandas as pd

from ..utils import response_to_df, clean_params


class AnalystEndpoints:
    """Endpoints for retrieving analyst data and recommendations."""

    def __init__(self, client):
        """
        Initialize the Analyst endpoints.

        Args:
            client: The FMP client instance
        """
        self._client = client

    def financial_estimates(
        self,
        symbol: str,
        period: Optional[str] = "annual",
        limit: Optional[int] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get analyst financial estimates for a company.

        Args:
            symbol: Stock symbol
            period: Period of estimates ('annual' or 'quarter')
            limit: Maximum number of estimates to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Financial estimates or DataFrame if as_dataframe=True
        """
        params = clean_params({"symbol": symbol, "period": period, "limit": limit})

        response = self._client.get("analyst-estimates", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def ratings_snapshot(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get ratings snapshot for a company.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Ratings snapshot or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("ratings-snapshot", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def historical_ratings(
        self, symbol: str, limit: Optional[int] = None, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get historical ratings for a company.

        Args:
            symbol: Stock symbol
            limit: Maximum number of ratings to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Historical ratings or DataFrame if as_dataframe=True
        """
        params = clean_params({"symbol": symbol, "limit": limit})

        response = self._client.get("ratings-historical", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def price_target_summary(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get price target summary for a company.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Price target summary or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("price-target-summary", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def price_target_consensus(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get price target consensus for a company.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Price target consensus or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("price-target-consensus", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def price_target_news(
        self, symbol: str, limit: Optional[int] = None, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get price target news for a company.

        Args:
            symbol: Stock symbol
            limit: Maximum number of news items to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Price target news or DataFrame if as_dataframe=True
        """
        params = clean_params({"symbol": symbol, "limit": limit})

        response = self._client.get("price-target-news", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "publishedDate" in df.columns:
                df["publishedDate"] = pd.to_datetime(df["publishedDate"])
            return df
        return response

    def price_target_latest_news(
        self, limit: Optional[int] = None, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get latest price target news for all companies.

        Args:
            limit: Maximum number of news items to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Latest price target news or DataFrame if as_dataframe=True
        """
        params = clean_params({"limit": limit})

        response = self._client.get("price-target-latest-news", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "publishedDate" in df.columns:
                df["publishedDate"] = pd.to_datetime(df["publishedDate"])
            return df
        return response

    def grades(
        self, symbol: str, limit: Optional[int] = None, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get stock grades (analyst ratings) for a company.

        Args:
            symbol: Stock symbol
            limit: Maximum number of grades to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Stock grades or DataFrame if as_dataframe=True
        """
        params = clean_params({"symbol": symbol, "limit": limit})

        response = self._client.get("grades", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def historical_grades(
        self, symbol: str, limit: Optional[int] = None, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get historical stock grades for a company.

        Args:
            symbol: Stock symbol
            limit: Maximum number of grades to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Historical stock grades or DataFrame if as_dataframe=True
        """
        params = clean_params({"symbol": symbol, "limit": limit})

        response = self._client.get("grades-historical", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def grades_summary(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get stock grades summary for a company.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Stock grades summary or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("grades-consensus", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def grade_news(
        self, symbol: str, limit: Optional[int] = None, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get stock grade news for a company.

        Args:
            symbol: Stock symbol
            limit: Maximum number of news items to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Stock grade news or DataFrame if as_dataframe=True
        """
        params = clean_params({"symbol": symbol, "limit": limit})

        response = self._client.get("grades-news", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "publishedDate" in df.columns:
                df["publishedDate"] = pd.to_datetime(df["publishedDate"])
            return df
        return response

    def grade_latest_news(
        self, limit: Optional[int] = None, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get latest stock grade news for all companies.

        Args:
            limit: Maximum number of news items to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Latest stock grade news or DataFrame if as_dataframe=True
        """
        params = clean_params({"limit": limit})

        response = self._client.get("grades-latest-news", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "publishedDate" in df.columns:
                df["publishedDate"] = pd.to_datetime(df["publishedDate"])
            return df
        return response
