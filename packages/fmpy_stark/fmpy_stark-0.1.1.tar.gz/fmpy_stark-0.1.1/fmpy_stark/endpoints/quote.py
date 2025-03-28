from typing import Dict, Any, List, Union
import pandas as pd

from ..utils import validate_symbols, response_to_df


class QuoteEndpoints:
    """Endpoints for retrieving stock quotes and price data."""

    def __init__(self, client):
        """
        Initialize the Quote endpoints.

        Args:
            client: The FMP client instance
        """
        self._client = client

    def real_time(
        self, symbol: Union[str, List[str]], as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get real-time stock quotes.

        Args:
            symbol: Stock symbol or list of symbols
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Real-time stock quotes or DataFrame if as_dataframe=True
        """
        params = {"symbol": validate_symbols(symbol)}

        response = self._client.get("quote", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def short(
        self, symbol: Union[str, List[str]], as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get short-form stock quotes (less detail than real_time).

        Args:
            symbol: Stock symbol or list of symbols
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Short-form stock quotes or DataFrame if as_dataframe=True
        """
        params = {"symbol": validate_symbols(symbol)}

        response = self._client.get("quote-short", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def aftermarket_trade(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get aftermarket trade data for a stock.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Aftermarket trade data or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("aftermarket-trade", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def aftermarket_quote(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get aftermarket quotes for a stock.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Aftermarket quote data or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("aftermarket-quote", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def price_change(
        self, symbol: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get stock price changes over various time periods.

        Args:
            symbol: Stock symbol
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Stock price change data or DataFrame if as_dataframe=True
        """
        params = {"symbol": symbol}

        response = self._client.get("stock-price-change", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def batch(
        self, symbols: Union[str, List[str]], as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get batch quotes for multiple stocks.

        Args:
            symbols: Stock symbols
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Batch stock quotes or DataFrame if as_dataframe=True
        """
        params = {"symbols": validate_symbols(symbols)}

        response = self._client.get("batch-quote", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def batch_short(
        self, symbols: Union[str, List[str]], as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get short-form batch quotes for multiple stocks.

        Args:
            symbols: Stock symbols
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Short-form batch quotes or DataFrame if as_dataframe=True
        """
        params = {"symbols": validate_symbols(symbols)}

        response = self._client.get("batch-quote-short", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def batch_aftermarket_trade(
        self, symbols: Union[str, List[str]], as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get aftermarket trade data for multiple stocks.

        Args:
            symbols: Stock symbols
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Batch aftermarket trade data or DataFrame if as_dataframe=True
        """
        params = {"symbols": validate_symbols(symbols)}

        response = self._client.get("batch-aftermarket-trade", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def batch_aftermarket_quote(
        self, symbols: Union[str, List[str]], as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get aftermarket quotes for multiple stocks.

        Args:
            symbols: Stock symbols
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Batch aftermarket quote data or DataFrame if as_dataframe=True
        """
        params = {"symbols": validate_symbols(symbols)}

        response = self._client.get("batch-aftermarket-quote", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def exchange_quotes(
        self, exchange: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get quotes for all stocks on a specific exchange.

        Args:
            exchange: Exchange name (e.g., "NASDAQ")
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Exchange quotes or DataFrame if as_dataframe=True
        """
        params = {"exchange": exchange}

        response = self._client.get("batch-exchange-quote", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def mutual_fund_quotes(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get quotes for mutual funds.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Mutual fund quotes or DataFrame if as_dataframe=True
        """
        response = self._client.get("batch-mutualfund-quotes")

        if as_dataframe:
            return response_to_df(response)
        return response

    def etf_quotes(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get quotes for ETFs.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            ETF quotes or DataFrame if as_dataframe=True
        """
        response = self._client.get("batch-etf-quotes")

        if as_dataframe:
            return response_to_df(response)
        return response

    def commodity_quotes(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get quotes for commodities.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Commodity quotes or DataFrame if as_dataframe=True
        """
        response = self._client.get("batch-commodity-quotes")

        if as_dataframe:
            return response_to_df(response)
        return response

    def crypto_quotes(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get quotes for cryptocurrencies.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Cryptocurrency quotes or DataFrame if as_dataframe=True
        """
        response = self._client.get("batch-crypto-quotes")

        if as_dataframe:
            return response_to_df(response)
        return response

    def forex_quotes(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get quotes for forex pairs.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Forex quotes or DataFrame if as_dataframe=True
        """
        response = self._client.get("batch-forex-quotes")

        if as_dataframe:
            return response_to_df(response)
        return response

    def index_quotes(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get quotes for market indexes.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Index quotes or DataFrame if as_dataframe=True
        """
        response = self._client.get("batch-index-quotes")

        if as_dataframe:
            return response_to_df(response)
        return response
