from typing import Dict, Any, List, Union
import pandas as pd

from ..utils import response_to_df


class BulkEndpoints:
    """Endpoints for retrieving bulk financial data."""

    def __init__(self, client):
        """
        Initialize the Bulk endpoints.

        Args:
            client: The FMP client instance
        """
        self._client = client

    def company_profile(
        self, part: int = 0, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get company profiles in bulk.

        Args:
            part: The part index (0, 1, 2, etc.) to retrieve
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk company profiles or DataFrame if as_dataframe=True
        """
        params = {"part": part}

        response = self._client.get("profile-bulk", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def stock_rating(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get stock ratings in bulk.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk stock ratings or DataFrame if as_dataframe=True
        """
        response = self._client.get("rating-bulk")

        if as_dataframe:
            return response_to_df(response)
        return response

    def dcf_valuations(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get DCF valuations in bulk.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk DCF valuations or DataFrame if as_dataframe=True
        """
        response = self._client.get("dcf-bulk")

        if as_dataframe:
            return response_to_df(response)
        return response

    def financial_scores(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get financial scores in bulk.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk financial scores or DataFrame if as_dataframe=True
        """
        response = self._client.get("scores-bulk")

        if as_dataframe:
            return response_to_df(response)
        return response

    def price_target_summary(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get price target summaries in bulk.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk price target summaries or DataFrame if as_dataframe=True
        """
        response = self._client.get("price-target-summary-bulk")

        if as_dataframe:
            return response_to_df(response)
        return response

    def etf_holder(
        self, part: int = 0, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get ETF holders in bulk.

        Args:
            part: The part index (0, 1, 2, etc.) to retrieve
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk ETF holders or DataFrame if as_dataframe=True
        """
        params = {"part": part}

        response = self._client.get("etf-holder-bulk", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def upgrades_downgrades_consensus(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get upgrades, downgrades, and consensus in bulk.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk upgrades, downgrades, and consensus or DataFrame if as_dataframe=True
        """
        response = self._client.get("upgrades-downgrades-consensus-bulk")

        if as_dataframe:
            return response_to_df(response)
        return response

    def key_metrics_ttm(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get key metrics TTM in bulk.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk key metrics TTM or DataFrame if as_dataframe=True
        """
        response = self._client.get("key-metrics-ttm-bulk")

        if as_dataframe:
            return response_to_df(response)
        return response

    def ratios_ttm(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get ratios TTM in bulk.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk ratios TTM or DataFrame if as_dataframe=True
        """
        response = self._client.get("ratios-ttm-bulk")

        if as_dataframe:
            return response_to_df(response)
        return response

    def stock_peers(
        self, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get stock peers in bulk.

        Args:
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk stock peers or DataFrame if as_dataframe=True
        """
        response = self._client.get("peers-bulk")

        if as_dataframe:
            return response_to_df(response)
        return response

    def earnings_surprises(
        self, year: int, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get earnings surprises in bulk.

        Args:
            year: The year to retrieve earnings surprises for
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk earnings surprises or DataFrame if as_dataframe=True
        """
        params = {"year": year}

        response = self._client.get("earnings-surprises-bulk", params=params)

        if as_dataframe:
            return response_to_df(response)
        return response

    def income_statement(
        self, year: int, period: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get income statements in bulk.

        Args:
            year: The year to retrieve income statements for
            period: The period to retrieve ('Q1', 'Q2', 'Q3', 'Q4', or 'FY')
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

    def income_statement_growth(
        self, year: int, period: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get income statement growth in bulk.

        Args:
            year: The year to retrieve income statement growth for
            period: The period to retrieve ('Q1', 'Q2', 'Q3', 'Q4', or 'FY')
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk income statement growth or DataFrame if as_dataframe=True
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

    def balance_sheet_statement(
        self, year: int, period: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get balance sheet statements in bulk.

        Args:
            year: The year to retrieve balance sheet statements for
            period: The period to retrieve ('Q1', 'Q2', 'Q3', 'Q4', or 'FY')
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

    def balance_sheet_statement_growth(
        self, year: int, period: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get balance sheet statement growth in bulk.

        Args:
            year: The year to retrieve balance sheet statement growth for
            period: The period to retrieve ('Q1', 'Q2', 'Q3', 'Q4', or 'FY')
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk balance sheet statement growth or DataFrame if as_dataframe=True
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

    def cash_flow_statement(
        self, year: int, period: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get cash flow statements in bulk.

        Args:
            year: The year to retrieve cash flow statements for
            period: The period to retrieve ('Q1', 'Q2', 'Q3', 'Q4', or 'FY')
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

    def cash_flow_statement_growth(
        self, year: int, period: str, as_dataframe: bool = True
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Get cash flow statement growth in bulk.

        Args:
            year: The year to retrieve cash flow statement growth for
            period: The period to retrieve ('Q1', 'Q2', 'Q3', 'Q4', or 'FY')
            as_dataframe: Return results as a pandas DataFrame if True

        Returns:
            Bulk cash flow statement growth or DataFrame if as_dataframe=True
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
