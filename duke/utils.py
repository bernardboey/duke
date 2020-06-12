import datetime

from duke import exceptions


def get_date(date_string):
    for date_format in ("%d/%m/%Y", "%d/%m/%y", "%d %b %Y", "%d %b", "%d-%m-%Y", "%d-%m-%y"):
        try:
            date = datetime.datetime.strptime(date_string, date_format).date()
            return date
        except ValueError:
            continue
    raise exceptions.DateFormatError("dd/mm/yyyy")


def get_datetime(date_string):
    for date_format in ("%d/%m/%Y", "%d/%m/%y", "%d %b %Y", "%d %b", "%d-%m-%Y", "%d-%m-%y"):
        try:
            date_time = datetime.datetime.strptime(date_string, date_format)
            return date_time
        except ValueError:
            continue
    raise exceptions.DateFormatError("dd/mm/yyyy")
