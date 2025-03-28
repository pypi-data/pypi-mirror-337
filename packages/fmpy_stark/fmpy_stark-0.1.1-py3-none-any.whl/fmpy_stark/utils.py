from typing import Dict, Any, List, Union
from datetime import datetime, date
import pandas as pd


def validate_date(date_str: str) -> bool:
    """
    Validate if a string is a valid date in YYYY-MM-DD format.

    Args:
        date_str: String date to validate

    Returns:
        True if the date is valid, False otherwise
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def format_date(date_param: Union[str, datetime, date]) -> str:
    """
    Format a date parameter to YYYY-MM-DD string format.

    Args:
        date_param: Date in string, datetime or date format

    Returns:
        Formatted date string
    """
    if isinstance(date_param, str):
        if validate_date(date_param):
            return date_param
        raise ValueError(f"Invalid date format: {date_param}. Expected: YYYY-MM-DD")
    elif isinstance(date_param, (datetime, date)):
        return date_param.strftime("%Y-%m-%d")
    else:
        raise TypeError("Date must be a string or datetime/date object")


def validate_symbols(symbols: Union[str, List[str]]) -> str:
    """
    Validate and format stock symbols.

    Args:
        symbols: Single symbol or list of symbols

    Returns:
        Comma-separated string of symbols
    """
    if isinstance(symbols, str):
        return symbols
    elif isinstance(symbols, list):
        return ",".join(symbols)
    else:
        raise TypeError("Symbols must be a string or a list of strings")


def response_to_df(
    response: Union[Dict[str, Any], List[Dict[str, Any]]],
) -> pd.DataFrame:
    """
    Convert an API response to a pandas DataFrame.

    Args:
        response: API response data

    Returns:
        pandas DataFrame with the response data
    """
    if isinstance(response, dict):
        return pd.DataFrame([response])
    elif isinstance(response, list):
        if not response:  # Empty list
            return pd.DataFrame()
        return pd.DataFrame(response)
    else:
        raise TypeError("Response must be a dictionary or a list of dictionaries")


def clean_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean parameters by removing None values.

    Args:
        params: Parameters dictionary

    Returns:
        Cleaned parameters dictionary
    """
    return {k: v for k, v in params.items() if v is not None}
