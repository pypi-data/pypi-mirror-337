"""
Exceptions for Payler SDK.
"""

from typing import Any, Optional


class PaylerError(Exception):
    """Base class for all Payler SDK exceptions."""
    pass


class PaylerApiError(PaylerError):
    """Error when interacting with Payler API."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[Any] = None
    ) -> None:
        """
        Initialize API error.

        Args:
            message: Error message
            status_code: HTTP code of response, if applicable
            response: Full response from API, if available
        """
        self.status_code = status_code
        self.response = response
        super().__init__(message)


class PaylerSessionError(PaylerError):
    """Error when creating or using Payler session."""
    pass


class PaylerTransactionNotFoundError(PaylerError):
    """Error when trying to find non-existent transaction."""
    pass


class PaylerValidationError(PaylerError):
    """Error when validating incoming or outgoing data."""
    pass


class PaylerRefundError(PaylerError):
    """Error when performing refund operation."""
    pass
