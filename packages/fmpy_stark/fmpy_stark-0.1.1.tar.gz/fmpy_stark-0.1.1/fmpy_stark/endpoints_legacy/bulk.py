from typing import Dict, Any, List, Union
import pandas as pd

from ..utils import response_to_df


class BulkEndpointsLegacy:
    """Endpoints for retrieving legacy bulk financial data."""

    def __init__(self, client):
        """
        Initialize the Legacy Bulk endpoints.

        Args:
            client: The FMP legacy client instance
        """
        self._client = client

    def batch_eod_prices(
        self, date: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get batch end-of-day prices for all stocks on a specific date.

        Args:
            date: Date for which to get EOD data (format: YYYY-MM-DD)
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Batch EOD data or DataFrame if as_dataframe=True
        """
        params = {"date": date}

        response = self._client.get("batch-historical-eod", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def income_statements(
        self, year: int, period: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get bulk income statements for all companies for a specific year and period.

        Args:
            year: The year to retrieve income statements for
            period: The period ('annual' or 'quarter')
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk income statements or DataFrame if as_dataframe=True
        """
        params = {"year": year, "period": period}

        # Always expect CSV for this endpoint
        response = self._client.get(
            "income-statement-bulk", params=params, expect_csv=True
        )

        # Response is already a DataFrame from the CSV parser
        if as_dataframe:
            return response
        # Convert DataFrame to list of dictionaries if as_dataframe is False
        return response.to_dict("records")

    def balance_sheet_statements(
        self, year: int, period: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get bulk balance sheet statements for all companies for a specific year and period.

        Args:
            year: The year to retrieve balance sheet statements for
            period: The period ('annual' or 'quarter')
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk balance sheet statements or DataFrame if as_dataframe=True
        """
        params = {"year": year, "period": period}

        # Always expect CSV for this endpoint
        response = self._client.get(
            "balance-sheet-statement-bulk", params=params, expect_csv=True
        )

        # Response is already a DataFrame from the CSV parser
        if as_dataframe:
            return response
        # Convert DataFrame to list of dictionaries if as_dataframe is False
        return response.to_dict("records")

    def cash_flow_statements(
        self, year: int, period: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get bulk cash flow statements for all companies for a specific year and period.

        Args:
            year: The year to retrieve cash flow statements for
            period: The period ('annual' or 'quarter')
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk cash flow statements or DataFrame if as_dataframe=True
        """
        params = {"year": year, "period": period}

        # Always expect CSV for this endpoint
        response = self._client.get(
            "cash-flow-statement-bulk", params=params, expect_csv=True
        )

        # Response is already a DataFrame from the CSV parser
        if as_dataframe:
            return response
        # Convert DataFrame to list of dictionaries if as_dataframe is False
        return response.to_dict("records")

    def ratios(
        self, year: int, period: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get bulk financial ratios for all companies for a specific year and period.

        Args:
            year: The year to retrieve ratios for
            period: The period ('annual' or 'quarter')
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk financial ratios or DataFrame if as_dataframe=True
        """
        params = {"year": year, "period": period}

        # Always expect CSV for this endpoint
        response = self._client.get("ratios-bulk", params=params, expect_csv=True)

        # Response is already a DataFrame from the CSV parser
        if as_dataframe:
            return response
        # Convert DataFrame to list of dictionaries if as_dataframe is False
        return response.to_dict("records")

    def key_metrics(
        self, year: int, period: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get bulk key metrics for all companies for a specific year and period.

        Args:
            year: The year to retrieve key metrics for
            period: The period ('annual' or 'quarter')
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk key metrics or DataFrame if as_dataframe=True
        """
        params = {"year": year, "period": period}

        # Always expect CSV for this endpoint
        response = self._client.get("key-metrics-bulk", params=params, expect_csv=True)

        # Response is already a DataFrame from the CSV parser
        if as_dataframe:
            return response
        # Convert DataFrame to list of dictionaries if as_dataframe is False
        return response.to_dict("records")

    def earnings_surprises(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get bulk earnings surprises for all companies.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk earnings surprises or DataFrame if as_dataframe=True
        """
        # Always expect CSV for this endpoint
        response = self._client.get("earnings-surprises-bulk", expect_csv=True)

        # Response is already a DataFrame from the CSV parser
        if as_dataframe:
            return response
        # Convert DataFrame to list of dictionaries if as_dataframe is False
        return response.to_dict("records")

    def company_profiles(
        self, part: int = 0, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get bulk company profiles.

        Args:
            part: The part index (0, 1, 2, etc.) to retrieve
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk company profiles or DataFrame if as_dataframe=True
        """
        params = {"part": part}

        # Always expect CSV for this endpoint
        response = self._client.get("profile-bulk", params=params, expect_csv=True)

        # Response is already a DataFrame from the CSV parser
        if as_dataframe:
            return response
        # Convert DataFrame to list of dictionaries if as_dataframe is False
        return response.to_dict("records")

    def stock_ratings(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get bulk stock ratings for all companies.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk stock ratings or DataFrame if as_dataframe=True
        """
        # Always expect CSV for this endpoint
        response = self._client.get("rating-bulk", expect_csv=True)

        # Response is already a DataFrame from the CSV parser
        if as_dataframe:
            return response
        # Convert DataFrame to list of dictionaries if as_dataframe is False
        return response.to_dict("records")

    def dcf_valuations(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get bulk DCF valuations for all companies.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk DCF valuations or DataFrame if as_dataframe=True
        """
        # Always expect CSV for this endpoint
        response = self._client.get("dcf-bulk", expect_csv=True)

        # Response is already a DataFrame from the CSV parser
        if as_dataframe:
            return response
        # Convert DataFrame to list of dictionaries if as_dataframe is False
        return response.to_dict("records")

    def key_metrics_ttm(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get bulk key metrics TTM (trailing twelve months) for all companies.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk key metrics TTM or DataFrame if as_dataframe=True
        """
        # Always expect CSV for this endpoint
        response = self._client.get("key-metrics-ttm-bulk", expect_csv=True)

        # Response is already a DataFrame from the CSV parser
        if as_dataframe:
            return response
        # Convert DataFrame to list of dictionaries if as_dataframe is False
        return response.to_dict("records")

    def ratios_ttm(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get bulk ratios TTM (trailing twelve months) for all companies.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk ratios TTM or DataFrame if as_dataframe=True
        """
        # Always expect CSV for this endpoint
        response = self._client.get("ratios-ttm-bulk", expect_csv=True)

        # Response is already a DataFrame from the CSV parser
        if as_dataframe:
            return response
        # Convert DataFrame to list of dictionaries if as_dataframe is False
        return response.to_dict("records")

    def financial_scores(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get bulk financial scores for all companies.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk financial scores or DataFrame if as_dataframe=True
        """
        # Always expect CSV for this endpoint
        response = self._client.get("scores-bulk", expect_csv=True)

        # Response is already a DataFrame from the CSV parser
        if as_dataframe:
            return response
        # Convert DataFrame to list of dictionaries if as_dataframe is False
        return response.to_dict("records")

    def financial_growth(
        self, year: int, period: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get bulk financial growth data for all companies.

        Args:
            year: The year to retrieve financial growth data for
            period: The period ('annual' or 'quarter')
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk financial growth data or DataFrame if as_dataframe=True
        """
        params = {"year": year, "period": period}

        # Always expect CSV for this endpoint
        response = self._client.get(
            "financial-growth-bulk", params=params, expect_csv=True
        )

        # Response is already a DataFrame from the CSV parser
        if as_dataframe:
            return response
        # Convert DataFrame to list of dictionaries if as_dataframe is False
        return response.to_dict("records")

    def income_statement_growth(
        self, year: int, period: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get bulk income statement growth data for all companies.

        Args:
            year: The year to retrieve income statement growth data for
            period: The period ('annual' or 'quarter')
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk income statement growth data or DataFrame if as_dataframe=True
        """
        params = {"year": year, "period": period}

        # Always expect CSV for this endpoint
        response = self._client.get(
            "income-statement-growth-bulk", params=params, expect_csv=True
        )

        # Response is already a DataFrame from the CSV parser
        if as_dataframe:
            return response
        # Convert DataFrame to list of dictionaries if as_dataframe is False
        return response.to_dict("records")

    def balance_sheet_growth(
        self, year: int, period: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get bulk balance sheet growth data for all companies.

        Args:
            year: The year to retrieve balance sheet growth data for
            period: The period ('annual' or 'quarter')
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk balance sheet growth data or DataFrame if as_dataframe=True
        """
        params = {"year": year, "period": period}

        # Always expect CSV for this endpoint
        response = self._client.get(
            "balance-sheet-statement-growth-bulk", params=params, expect_csv=True
        )

        # Response is already a DataFrame from the CSV parser
        if as_dataframe:
            return response
        # Convert DataFrame to list of dictionaries if as_dataframe is False
        return response.to_dict("records")

    def cash_flow_growth(
        self, year: int, period: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get bulk cash flow growth data for all companies.

        Args:
            year: The year to retrieve cash flow growth data for
            period: The period ('annual' or 'quarter')
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk cash flow growth data or DataFrame if as_dataframe=True
        """
        params = {"year": year, "period": period}

        # Always expect CSV for this endpoint
        response = self._client.get(
            "cash-flow-statement-growth-bulk", params=params, expect_csv=True
        )

        # Response is already a DataFrame from the CSV parser
        if as_dataframe:
            return response
        # Convert DataFrame to list of dictionaries if as_dataframe is False
        return response.to_dict("records")

    def price_target_summary(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get bulk price target summaries for all companies.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk price target summaries or DataFrame if as_dataframe=True
        """
        # Always expect CSV for this endpoint
        response = self._client.get("price-target-summary-bulk", expect_csv=True)

        # Response is already a DataFrame from the CSV parser
        if as_dataframe:
            return response
        # Convert DataFrame to list of dictionaries if as_dataframe is False
        return response.to_dict("records")

    def upgrades_downgrades_consensus(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get bulk upgrades, downgrades, and consensus data for all companies.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk upgrades, downgrades, and consensus data or DataFrame if as_dataframe=True
        """
        # Always expect CSV for this endpoint
        response = self._client.get(
            "upgrades-downgrades-consensus-bulk", expect_csv=True
        )

        # Response is already a DataFrame from the CSV parser
        if as_dataframe:
            return response
        # Convert DataFrame to list of dictionaries if as_dataframe is False
        return response.to_dict("records")

    def etf_holders(
        self, part: int = 0, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get bulk ETF holders data.

        Args:
            part: The part index (0, 1, 2, etc.) to retrieve
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk ETF holders data or DataFrame if as_dataframe=True
        """
        params = {"part": part}

        # Always expect CSV for this endpoint
        response = self._client.get("etf-holder-bulk", params=params, expect_csv=True)

        # Response is already a DataFrame from the CSV parser
        if as_dataframe:
            return response
        # Convert DataFrame to list of dictionaries if as_dataframe is False
        return response.to_dict("records")

    def stock_peers(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get bulk stock peers data for all companies.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk stock peers data or DataFrame if as_dataframe=True
        """
        # Always expect CSV for this endpoint
        response = self._client.get("stock_peers_bulk", expect_csv=True)

        # Response is already a DataFrame from the CSV parser
        if as_dataframe:
            return response
        # Convert DataFrame to list of dictionaries if as_dataframe is False
        return response.to_dict("records")
