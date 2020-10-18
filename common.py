import uuid
import os
import shutil
import re
import time
import datetime
import enum
import vars
import subprocess
from vars import *


def get_file_size(file_name: str, human_readable: bool = True):
    """
    Get file in size in given unit like KB, MB or GB

    :param file_name:
    :param human_readable:
    :return:
    """
    size = os.path.getsize(file_name)
    if human_readable is False:
        return size
    elif size > (1024*1024*1024):
        return '{:.2f} Gb'.format(size/(1024*1024*1024))
    elif size > (1024*1024):
        return '{:.2f} Mb'.format(size/(1024*1024))
    elif size > 1024:
        return '{:.2f} Kb'.format(size/1024)
    else:
        return '{} bytes'.format(size)


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


def listDir(dirName: str, ext: str = None):
    """
    Recursive function for listing files in a folder and his sub folders

    :param dirName: path of the parsed dir
    :return: list(str)
    """
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if ext is not None and os.path.isfile(fullPath):
            if re.search("\\.({})$".format(ext), entry) is None: continue
        if os.path.isdir(fullPath):
            allFiles = allFiles + listDir(fullPath, ext)
        else:
            allFiles.append(fullPath)
    return allFiles


def listDirTree(dirName: str, ext: str = None):
    listOfFile = listDir(dirName, ext)
    listOfFile.sort()
    treeFiles = {}
    for file in listOfFile:
        recurListDirTree(file, dirName + os.sep, treeFiles)
    return treeFiles


def recurListDirTree(file: str, path: str, treeFiles: dir):
    tmpl = file.replace(path, '')
    tmpp = tmpl.split(os.sep)
    if len(tmpp) > 1:
        if tmpp[0] not in treeFiles:
            treeFiles[tmpp[0]] = {}
        return recurListDirTree(file, path + tmpp[0] + os.sep, treeFiles[tmpp[0]])
    else:
        treeFiles[tmpp[0]] = file
        return treeFiles


def cleanDir(src_dir: str):
    for dirpath, _, _ in os.walk(src_dir, topdown=False):  # Listing the files
        if dirpath == src_dir: break
        try:
            os.rmdir(dirpath)
        except Exception:
            {}


def rmDir(src_dir: str):
    shutil.rmtree(src_dir, ignore_errors=True)


def cleanStringForUrl(string: str):
    return string\
        .replace(':', '_')\
        .replace(';', '_')\
        .replace('\\', '_')\
        .replace('/', '_')\
        .replace('"', '_')\
        .replace(',', '_')\
        .replace('?', '_')


def deflate(src: str, dest: str):
    global env_vars
    list_args = list()  # create list argument for external command execution
    list_args.append(env_vars['tools']['7zip'][os.name]['path'])  # insert executable path
    temp_args = env_vars['tools']['7zip'][os.name]['params_deflate'].split(' ')  # create table of raw command arguments
    for var in temp_args:  # parse table of raw command arguments
        # insert parsed param
        list_args.append(var.replace('%input%', src).replace('%output%', dest))
    # print(list_args)
    return subprocess.check_output(list_args, universal_newlines=True)  # execute the command
