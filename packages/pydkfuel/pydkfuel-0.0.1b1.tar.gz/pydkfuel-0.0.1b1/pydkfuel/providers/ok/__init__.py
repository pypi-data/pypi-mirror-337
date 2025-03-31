"""Provider OK."""

import requests

from ...consts import DIESEL, OCTANE_95, OCTANE_100
from ...exceptions import ErrorRefreshingPrices
from ...helpers.prices import add_price_to_product
from ...helpers.web_scrape import clean_product_name, get_html_soup, get_website

NAME = "OK"
URL = "https://www.ok.dk/offentlig/produkter/braendstof/priser/vejledende-standerpriser"
PRODUCTS = {
    OCTANE_95: {"name": "Blyfri 95"},
    OCTANE_100: {"name": "Oktan 100"},
    DIESEL: {"name": "Diesel"},
}

__all__ = ["Provider", "NAME"]


class Provider:
    """Provider class."""

    def __init__(self) -> None:
        """Initialize the provider module."""
        self._session = requests.Session()
        self._products = {}

    @property
    def name(self) -> str:
        """Return the human readable name for the provider module."""
        return NAME

    @property
    def products(self) -> dict:
        """Return the products and prices."""
        return self._products

    def get_products(self) -> dict:
        """Get available products from this provider."""
        products = {}
        for key, product in PRODUCTS.items():
            products.update({key: product["name"]})

        return products

    async def update_prices(self) -> None:
        """Update the prices from the provider."""
        try:
            website = get_website(self._session, URL)
            html = get_html_soup(website)
            rows = html.find_all("div", {"role": "row"})
            for key, product in PRODUCTS.items():
                found = False
                for row in rows:
                    if found:
                        continue
                    cells = row.find_all("div", {"role": "gridcell"})
                    if cells:
                        found = product["name"] == clean_product_name(cells[0].text)
                        if found:
                            self._products.update(
                                {key: add_price_to_product(product, cells[1].text)}
                            )

        except ErrorRefreshingPrices as erp:
            raise ErrorRefreshingPrices from erp
