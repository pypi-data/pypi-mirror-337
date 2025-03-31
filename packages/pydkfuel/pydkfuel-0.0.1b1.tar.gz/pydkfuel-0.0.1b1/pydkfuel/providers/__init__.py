"""Dynamically load available providers."""

from __future__ import annotations

from importlib import import_module
import logging
from collections import namedtuple
from os import listdir
from posixpath import dirname

from genericpath import isdir

from ..exceptions import UnknownProvider

_LOGGER = logging.getLogger(__name__)


class Providers:
    """Providers class."""

    def __init__(self) -> None:
        """Initialize providers class."""
        self._providers = []

    async def get_providers(self) -> dict:
        """Get available providers."""
        providers = listdir(f"{dirname(__file__)}")

        for module in sorted(providers):
            provider_path = f"{dirname(__file__)}/{module}"
            if isdir(provider_path) and not module.endswith("__pycache__"):
                Provider = namedtuple("Provider", "module namespace name")
                _LOGGER.debug("Adding provider %s in path %s", module, provider_path)
                api_ns = f".{module}"
                mod = import_module(api_ns, __name__)
                prov = Provider(module, f".providers{api_ns}", mod.NAME)
                self._providers.append(prov)

    @property
    def providers(self) -> list:
        """Return valid providers."""
        return self._providers

    async def set_provider(self, provider: str) -> None:
        """Set the provider for this instance."""
        provider_found = False

        for prov in self._providers:
            if prov.module == provider:
                module = import_module(prov.namespace, __name__.removesuffix(".providers"))
                my_class = getattr(module, 'Provider')
                return my_class()

        if not provider_found:
            raise UnknownProvider
