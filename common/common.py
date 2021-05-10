import uuid
import os, sys
import datetime
import string

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def is_in(objet: dict, indexes: list):
    """
    check if a list of indexes exist in a dict

    :param objet: reference dict for the search
    :param indexes: list of searched index
    :return: bool
    """
    for elem in indexes:
        if str(elem) in objet:
            continue
        else:
            return False
    return True


def uid():
    """
    generate a GUID

    :return: str
    """
    return uuid.uuid1().urn.replace('urn:uuid:', '')


def unixtime_to_string(value: float, template: str = '%Y-%m-%d %H:%M:%S', months: list = list(), is_utc: bool = True):
    """
    translate unix timestamp into human readable string

    :param value: unix timestamp
    :param template: template format string
    :param months: list of translated names of months, require a full list of 12 string
    :param is_utc: define if function format time in UTC time or local time
    :return: str
    """
    value = int(value)
    if is_utc is True:
        if '$month' in template:
            amonth = months[int(float(datetime.datetime.utcfromtimestamp(value).strftime('%m'))) - 1]
            template = template.replace('$month', amonth)
        return datetime.datetime.utcfromtimestamp(value).strftime(template)
    else:
        if '$month' in template:
            amonth = months[int(float(datetime.datetime.fromtimestamp(value).strftime('%m'))) - 1]
            template = template.replace('$month', amonth)
        return datetime.datetime.fromtimestamp(value).strftime(template)


def clean_string_for_url(path: str):
    printable = set(string.printable)
    return ''.join(filter(lambda x: x in printable, path))\
        .replace(':', '_')\
        .replace(';', '_')\
        .replace('\\', '_')\
        .replace('/', '_')\
        .replace('"', '_')\
        .replace(',', '_')\
        .replace('?', '_')\
        .replace('*', '_')\
        .replace('<', '_')\
        .replace('>', '_')\
        .replace('|', '_')  # .replace(' ', '_')
