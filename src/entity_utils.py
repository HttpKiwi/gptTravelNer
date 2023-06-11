import dateparser
import requests


def convert(amount):
    data = requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()
    currencies = data["rates"]
    amount_usd = round(amount / currencies["COP"], 2)
    return amount_usd


def parse_dates(dates):
    parsed_dates = []
    for date in dates:
        parsed_dates.append(dateparser.parse(date).isoformat())
    return parsed_dates
