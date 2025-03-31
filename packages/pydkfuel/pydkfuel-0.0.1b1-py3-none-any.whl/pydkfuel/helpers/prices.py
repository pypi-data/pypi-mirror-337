"""Handle price data."""

from datetime import datetime

import pytz

DK_TZ = pytz.timezone("Europe/Copenhagen")


def add_price_to_product(product_dict, product_price):
    product_dict.update({"price": clean_price(product_price)})
    dt = datetime.now(DK_TZ)
    product_dict.update({"lastUpdate": dt})
    return product_dict


def clean_price(price):
    price = str(price)  # Typecast to String
    price = price.replace("Pris inkl. moms: ", "")  # Remove 'Pris inkl. moms: '
    price = price.replace(" kr.", "")  # Remove ' kr.'
    price = price.replace(",", ".")  # Replace ',' with '.'
    price = price.strip()  # Remove leading or trailing whitespaces
    return float("{:.2f}".format(float(price)))  # Return the price with 2 decimals
