"""Provider F24."""

from datetime import datetime, timedelta

import pytz
import requests

from ...consts import DIESEL, DIESEL_PLUS, OCTANE_95, OCTANE_95_PLUS
from ...exceptions import ErrorRefreshingPrices
from ...helpers.prices import add_price_to_product, clean_price

NAME = "F24"
URL = "https://www.f24.dk/-/api/PriceViewProduct/GetPriceViewProducts"
PRODUCTS = {
    OCTANE_95: {"name": "GoEasy 95 E10", "ProductCode": 22253},
    OCTANE_95_PLUS: {"name": "GoEasy 95 Extra E5", "ProductCode": 22603},
    DIESEL: {"name": "GoEasy Diesel", "ProductCode": 24453},
    DIESEL_PLUS: {"name": "GoEasy Diesel Extra", "ProductCode": 24338},
}

__all__ = ["Provider", "NAME"]

DK_TZ = pytz.timezone("Europe/Copenhagen")


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
            headers = {"Content-Type": "application/json"}
            now = datetime.now()
            payload = {}

            # F24/Q8 wish to have a "FromDate", we use today - 31 days as timestamp
            payload["FromDate"] = int((now - timedelta(days=31)).timestamp())

            # Today as timestamp
            payload["ToDate"] = int(now.timestamp())

            # Lets cook up some wanted fueltypes with a empty list
            payload["FuelsIdList"] = []

            # We can control the order of the returned data with a Index
            index = 0

            # Loop through the products
            for productDict in PRODUCTS.values():
                # Add "Index" to the dictionary of the product
                productDict["Index"] = index

                # Append the product to the list
                payload["FuelsIdList"].append(productDict)

                # increment the index
                index += 1

            # Send our payload and headers to the URL as a POST
            r = self._session.post(URL, headers=headers, data=str(payload))
            if r.status_code == 200:
                # Loop through the products
                for key, product in PRODUCTS.items():
                    # Extract the data of the product at the given Index from the dictionary
                    # Remember we told the server in which order we wanted the data
                    json_product = r.json()["Products"][product["Index"]]
                    self._products.update(
                        {
                            key: add_price_to_product(
                                product, json_product["PriceInclVATInclTax"]
                            )
                        }
                    )
            else:
                raise ErrorRefreshingPrices
        except ErrorRefreshingPrices as erp:
            raise ErrorRefreshingPrices from erp
