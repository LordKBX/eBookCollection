import uuid
import os
import time
import datetime
import enum


class SIZE_UNIT(enum.Enum):
    BYTES = 1
    KB = 2
    MB = 3
    GB = 4


def convert_unit(size_in_bytes, unit):
    """
    Convert the size from bytes to other units like KB, MB or GB

    :param size_in_bytes:
    :param unit:
    :return:
    """
    if unit == SIZE_UNIT.KB:
        return '{:.2f} Kb'.format(size_in_bytes/1024)
    elif unit == SIZE_UNIT.MB:
        return '{:.2f} Mb'.format(size_in_bytes/(1024*1024))
    elif unit == SIZE_UNIT.GB:
        return '{:.2f} Gb'.format(size_in_bytes/(1024*1024*1024))
    else:
        return '{} bytes'.format(size_in_bytes)


def get_file_size(file_name):
    """
    Get file in size in given unit like KB, MB or GB

    :param file_name:
    :param size_type:
    :return:
    """
    size = os.path.getsize(file_name)
    size_type = SIZE_UNIT.BYTES
    if size > (1024*1024*1024): size_type = SIZE_UNIT.GB
    elif size > (1024*1024): size_type = SIZE_UNIT.MB
    if size > 1024: size_type = SIZE_UNIT.KB
    return convert_unit(size, size_type)


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


def listDir(dirName):
    """
    Recursive function for listing files in a folder and his sub folders

    :param dirName: path of the parsed dir
    :return: list(str)
    """
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath): allFiles = allFiles + listDir(fullPath)
        else: allFiles.append(fullPath)
    return allFiles


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