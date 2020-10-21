import uuid
import os, sys
import shutil
import re
import time
import datetime
import enum
import subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from vars import *


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


def unixtimeToString(value: float, template: str = '%Y-%m-%d %H:%M:%S', months: list = list()):
    """
    translate unix timestamp into human readable string

    :param value: unix timestamp
    :param template: template format string
    :param months: list of translated names of months, require a full list of 12 string
    :return: str
    """
    value = int(value)
    if '$month' in template:
        amonth = months[int(float(datetime.datetime.utcfromtimestamp(value).strftime('%m'))) - 1]
        template = template.replace('$month', amonth)
    return datetime.datetime.utcfromtimestamp(value).strftime(template)


def cleanStringForUrl(string: str):
    return string\
        .replace(':', '_')\
        .replace(';', '_')\
        .replace('\\', '_')\
        .replace('/', '_')\
        .replace('"', '_')\
        .replace(',', '_')\
        .replace('?', '_')