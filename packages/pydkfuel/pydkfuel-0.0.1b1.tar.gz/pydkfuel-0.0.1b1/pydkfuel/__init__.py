"""Define pydkfuel library."""

from __future__ import annotations

import logging
import sys

import requests

if sys.version_info < (3, 11, 0):
    sys.exit("The pyWorxcloud module requires Python 3.11.0 or later")

_LOGGER = logging.getLogger(__name__)

class Fuel:
    """
    DK Fuel library.

    Used to fetch furl prices from Danish providers.
    """

    def __init__(self)->None:
        """Initialize the Fuel class."""