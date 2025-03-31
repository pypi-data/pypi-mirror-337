"""Provider OIL! tank & go."""

import requests

from ...consts import ADBLUE, BIODIESEL, DIESEL, OCTANE_95, OCTANE_95_PLUS
from ...exceptions import ErrorRefreshingPrices
from ...helpers.prices import add_price_to_product
from ...helpers.web_scrape import clean_product_name, get_html_soup, get_website

NAME = "OIL! tank & go"
URL = "https://www.oil-tankstationer.dk/de-gaeldende-braendstofpriser"
PRODUCTS = {
    OCTANE_95: {"name": "95 E10"},
    OCTANE_95_PLUS: {"name": "PREMIUM 98"},
    DIESEL: {"name": "Diesel"},
    BIODIESEL: {"name": "BIO100 Diesel"},
    ADBLUE: {"name": "AdBlue"},
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
            rows = html.find_all("tr")
            for key, product in PRODUCTS.items():
                found = False
                for row in rows:
                    if found:
                        continue
                    cells = row.find_all("td")
                    if cells:
                        found = product["name"] == clean_product_name(cells[0].text)
                        if found:
                            priceSegment = get_html_soup(cells[2])
                            self._products.update(
                                {
                                    key: add_price_to_product(
                                        product,
                                        priceSegment.get_text(),
                                    )
                                }
                            )

        except ErrorRefreshingPrices as erp:
            raise ErrorRefreshingPrices from erp
