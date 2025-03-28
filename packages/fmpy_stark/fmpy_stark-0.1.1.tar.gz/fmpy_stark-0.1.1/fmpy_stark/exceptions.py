class FMPError(Exception):
    """Base exception for all FMP API errors."""

    pass


class FMPRequestError(FMPError):
    """Raised when a request to the FMP API fails."""

    pass


class FMPAPIError(FMPError):
    """Raised when the FMP API returns an error response."""

    pass


class FMPValidationError(FMPError):
    """Raised when the input parameters for an API call are invalid."""

    pass
