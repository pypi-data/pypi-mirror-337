"""Web scaper helper."""

import logging
import requests
from bs4 import BeautifulSoup as BS

from ..exceptions import ErrorRefreshingPrices

_LOGGER = logging.getLogger(__name__)


def get_website(session: requests.session, url):
    """Load the website."""
    r = session.get(url, timeout=5)
    _LOGGER.debug("URL: %s [%s]", url, str(r.status_code))
    if r.status_code != 200:
        raise ErrorRefreshingPrices
    return r


def get_html_soup(web, parser="html.parser"):
    """Convert to SOUP for better handling the data."""
    if web.text:
        return BS(web.text, parser)


def clean_product_name(product_name):
    product_name = product_name.replace("Beskrivelse: ", "")
    product_name = product_name.strip()
    return product_name

def get_data_from_table(self, html, products, product_col, price_col):
    """
    Find all <tr> (rows) in the table
    Loop through all the products with the Key and a dict as Value (Object)
        Set found to False
        Loop through all the Rows
            If we previously have found a product, scontinue with the next product
            Find all the <td> (cells)
            If number of cells is larger than 1
                Set found true/false whether we have found the product
                If found
                    Extract, and clean, and add the price to the products dict
    Return the dict og products
    """
    rows = html.find_all("tr")
    for key, product in products.items():
        found = False
        for row in rows:
            if found:
                continue
            cells = row.findAll("td")
            if cells:
                found = product["name"] == self._cleanProductName(
                    cells[product_col].text
                )
                if found:
                    products[key] = self._addPriceToProduct(
                        product, cells[price_col].text
                    )
    return products