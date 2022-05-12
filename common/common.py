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


def uid(cleaned: bool = False):
    """
    generate a GUID

    :return: str
    """
    if cleaned is True: return uuid.uuid1().urn.replace('urn:uuid:', '').replace('-', '')
    else: return uuid.uuid1().urn.replace('urn:uuid:', '')


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
    import unicodedata, re, itertools, sys

    all_chars = (chr(i) for i in range(sys.maxunicode))
    categories = {'Cc'}
    # control_chars = ''.join(c for c in all_chars if unicodedata.category(c) in categories)
    # or equivalently and much more efficiently
    control_chars = ''.join(map(chr, itertools.chain(range(0x00, 0x20), range(0x7f, 0xa0))))
    control_char_re = re.compile('[%s]' % re.escape(control_chars))

    path = re.sub('(:|;|\\\\|\\/|"|\,|\?|\*|<|>|\\|)', '', path)
    return control_char_re.sub('', path)


def filename_cleaner(name: str):
    import re
    import unicodedata
    value = name.encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip()
    # value = re.sub('[-\s]+', '-', value)
    return value
