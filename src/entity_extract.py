import dateparser


def extract_date(dates):
    for date in dates:
        dateparser.parse(date)
