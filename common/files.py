import os, sys, shutil, re
import traceback
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


def listDir(dirName: str, ext: str = None):
    """
    Recursive function for listing files in a folder and his sub folders

    :param dirName: path of the parsed dir
    :return: list(str)
    """
    allFiles = list()
    for root, directories, files in os.walk(dirName, topdown=False):
        for name in files:
            fullPath = os.path.join(root, name)
            if ext is not None:
                if re.search("\\.({})$".format(ext), name) is None: continue
            allFiles.append(fullPath)
        if ext is None:
            for name in directories:
                allFiles.append(os.path.join(root, name))
    return allFiles


def listOnlyDir(path: str, level: int = 1, startDirs: list = [], excludeDirs: list = []):
    some_dir = path.rstrip(os.path.sep)
    listDir = startDirs
    if os.path.isdir(some_dir):
        num_sep = some_dir.count(os.path.sep)
        for root, dirs, files in os.walk(some_dir):
            num_sep_this = root.count(os.path.sep)
            for name in dirs:
                if name in excludeDirs: continue
                if num_sep + level > num_sep_this:
                    listDir.append(name)
    return listDir


def listDirTree(dirName: str, ext: str = None):
    listOfFile = listDir(dirName, ext)
    listOfFile.sort()
    # print(listOfFile)

    treeFiles = dict()
    for file in listOfFile:
        recurListDirTree(file, dirName + os.sep, treeFiles)
    return treeFiles


def recurListDirTree(file: str, path: str, treeFiles: dict):
    tmpl = file.replace(path, '')
    tmpp = tmpl.split(os.sep)

    if isinstance(tmpp, list):
        if len(tmpp) > 1:
            if tmpp[0] not in treeFiles:
                treeFiles[tmpp[0]] = dict()
            if isinstance(treeFiles[tmpp[0]], dict):
                recurListDirTree(file, path + tmpp[0] + os.sep, treeFiles[tmpp[0]])
        else:
            if os.path.isfile(file): treeFiles[tmpl] = file
            else: treeFiles[tmpl] = dict()


def cleanDir(src_dir: str):
    for dirpath, _, _ in os.walk(src_dir, topdown=False):  # Listing the files
        if dirpath == src_dir: break
        try: os.rmdir(dirpath)
        except Exception: ''


def rmDir(src_dir: str):
    shutil.rmtree(src_dir, ignore_errors=True)


def copyDir(src_dir: str, dest_dir: str):
    shutil.copytree(src_dir, dest_dir)