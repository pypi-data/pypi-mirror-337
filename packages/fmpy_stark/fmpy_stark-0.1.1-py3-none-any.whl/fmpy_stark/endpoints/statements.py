from typing import Dict, Any, Optional, List, Union
import pandas as pd

from ..utils import response_to_df, clean_params


class StatementsEndpoints:
    """Endpoints for retrieving financial statements."""

    def __init__(self, client):
        """
        Initialize the Statements endpoints.

        Args:
            client: The FMP client instance
        """
        self._client = client

    def income_statement(
        self,
        symbol: str,
        period: Optional[str] = "annual",
        limit: Optional[int] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get income statements for a company.

        Args:
            symbol: Stock symbol
            period: Period of reports ('annual' or 'quarter')
            limit: Maximum number of statements to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Income statements or DataFrame if as_dataframe=True
        """
        params = clean_params({"symbol": symbol, "period": period, "limit": limit})

        response = self._client.get("income-statement", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def balance_sheet(
        self,
        symbol: str,
        period: Optional[str] = "annual",
        limit: Optional[int] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get balance sheets for a company.

        Args:
            symbol: Stock symbol
            period: Period of reports ('annual' or 'quarter')
            limit: Maximum number of statements to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Balance sheets or DataFrame if as_dataframe=True
        """
        params = clean_params({"symbol": symbol, "period": period, "limit": limit})

        response = self._client.get("balance-sheet-statement", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def cash_flow(
        self,
        symbol: str,
        period: Optional[str] = "annual",
        limit: Optional[int] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get cash flow statements for a company.

        Args:
            symbol: Stock symbol
            period: Period of reports ('annual' or 'quarter')
            limit: Maximum number of statements to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Cash flow statements or DataFrame if as_dataframe=True
        """
        params = clean_params({"symbol": symbol, "period": period, "limit": limit})

        response = self._client.get("cash-flow-statement", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def latest_financial_statements(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get the latest financial statements for all companies.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Latest financial statements or DataFrame if as_dataframe=True
        """
        response = self._client.get("latest-financial-statements")

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def income_statement_ttm(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get trailing twelve months (TTM) income statement for a company.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            TTM income statement or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("income-statement-ttm", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def balance_sheet_ttm(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get trailing twelve months (TTM) balance sheet for a company.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            TTM balance sheet or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("balance-sheet-statement-ttm", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def cash_flow_ttm(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get trailing twelve months (TTM) cash flow statement for a company.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            TTM cash flow statement or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("cash-flow-statement-ttm", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def key_metrics(
        self,
        symbol: str,
        period: Optional[str] = "annual",
        limit: Optional[int] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get key financial metrics for a company.

        Args:
            symbol: Stock symbol
            period: Period of reports ('annual' or 'quarter')
            limit: Maximum number of reports to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Key metrics or DataFrame if as_dataframe=True
        """
        params = clean_params({"symbol": symbol, "period": period, "limit": limit})

        response = self._client.get("key-metrics", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def financial_ratios(
        self,
        symbol: str,
        period: Optional[str] = "annual",
        limit: Optional[int] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get financial ratios for a company.

        Args:
            symbol: Stock symbol
            period: Period of reports ('annual' or 'quarter')
            limit: Maximum number of reports to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Financial ratios or DataFrame if as_dataframe=True
        """
        params = clean_params({"symbol": symbol, "period": period, "limit": limit})

        response = self._client.get("ratios", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def key_metrics_ttm(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get trailing twelve months (TTM) key metrics for a company.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            TTM key metrics or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("key-metrics-ttm", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def financial_ratios_ttm(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get trailing twelve months (TTM) financial ratios for a company.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            TTM financial ratios or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("ratios-ttm", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def financial_scores(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get financial health scores for a company.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Financial scores or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("financial-scores", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def owner_earnings(
        self,
        symbol: str,
        period: Optional[str] = "annual",
        limit: Optional[int] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get owner earnings for a company.

        Args:
            symbol: Stock symbol
            period: Period of reports ('annual' or 'quarter')
            limit: Maximum number of reports to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Owner earnings or DataFrame if as_dataframe=True
        """
        params = clean_params({"symbol": symbol, "period": period, "limit": limit})

        response = self._client.get("owner-earnings", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def enterprise_values(
        self,
        symbol: str,
        period: Optional[str] = "annual",
        limit: Optional[int] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get enterprise values for a company.

        Args:
            symbol: Stock symbol
            period: Period of reports ('annual' or 'quarter')
            limit: Maximum number of reports to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Enterprise values or DataFrame if as_dataframe=True
        """
        params = clean_params({"symbol": symbol, "period": period, "limit": limit})

        response = self._client.get("enterprise-values", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def income_statement_growth(
        self,
        symbol: str,
        period: Optional[str] = "annual",
        limit: Optional[int] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get income statement growth for a company.

        Args:
            symbol: Stock symbol
            period: Period of reports ('annual' or 'quarter')
            limit: Maximum number of reports to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Income statement growth or DataFrame if as_dataframe=True
        """
        params = clean_params({"symbol": symbol, "period": period, "limit": limit})

        response = self._client.get("income-statement-growth", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def balance_sheet_growth(
        self,
        symbol: str,
        period: Optional[str] = "annual",
        limit: Optional[int] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get balance sheet growth for a company.

        Args:
            symbol: Stock symbol
            period: Period of reports ('annual' or 'quarter')
            limit: Maximum number of reports to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Balance sheet growth or DataFrame if as_dataframe=True
        """
        params = clean_params({"symbol": symbol, "period": period, "limit": limit})

        response = self._client.get("balance-sheet-statement-growth", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def cash_flow_growth(
        self,
        symbol: str,
        period: Optional[str] = "annual",
        limit: Optional[int] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get cash flow growth for a company.

        Args:
            symbol: Stock symbol
            period: Period of reports ('annual' or 'quarter')
            limit: Maximum number of reports to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Cash flow growth or DataFrame if as_dataframe=True
        """
        params = clean_params({"symbol": symbol, "period": period, "limit": limit})

        response = self._client.get("cash-flow-statement-growth", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response

    def financial_growth(
        self,
        symbol: str,
        period: Optional[str] = "annual",
        limit: Optional[int] = None,
        as_dataframe: bool = True,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get financial growth metrics for a company.

        Args:
            symbol: Stock symbol
            period: Period of reports ('annual' or 'quarter')
            limit: Maximum number of reports to return
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Financial growth metrics or DataFrame if as_dataframe=True
        """
        params = clean_params({"symbol": symbol, "period": period, "limit": limit})

        response = self._client.get("financial-growth", params=params)

        if as_dataframe:
            df = response_to_df(response)
            if not df.empty and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
            return df
        return response
