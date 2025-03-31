"""Exceptions for pydkfuel."""

from __future__ import annotations


class UnknownProvider(Exception):
    """Raised when trying to set an unknown provider."""


class ErrorRefreshingPrices(Exception):
    """Raised when the price source does not return a valid response."""


class UnavailableProduct(Exception):
    """Raised when the requested product doesn't exist for this provider."""
