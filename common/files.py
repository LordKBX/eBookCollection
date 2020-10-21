import os, sys, shutil, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
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


def listDir(dirName: str, ext: str = None, first: bool = True):
    """
    Recursive function for listing files in a folder and his sub folders

    :param dirName: path of the parsed dir
    :return: list(str)
    """
    listOfFile = list()
    if first is True:
        listOfFile = [x[0] for x in os.walk(dirName)]
    listOfFile += os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if ext is not None and os.path.isfile(fullPath):
            if re.search("\\.({})$".format(ext), entry) is None: continue
        if os.path.isdir(fullPath):
            allFiles = allFiles + listDir(fullPath, ext, False)
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