import dateparser
import requests


def convert(amount):
    data = requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()
    currencies = data["rates"]
    amount_usd = round(amount / currencies["COP"], 2)
    return amount_usd


def parse_dates(dates):
    parsed_dates = []
    iso_dates = []
    for date in dates:
        temp_date = dateparser.parse(date)
        parsed_dates.append(temp_date)
        iso_dates.append(temp_date.isoformat())
    return iso_dates, parsed_dates
