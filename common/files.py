import os, sys, shutil
import hashlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from common.vars import *
from common.MIME import *


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


def get_file_type(file_path: str) -> str:
    file_path = file_path.replace('/', os.sep)
    file_tab = file_path.split(os.sep)
    ext = file_tab[len(file_tab) - 1]
    file_type = ""
    end = False
    while end is False:
        if ext in EXT_TO_TYPE:
            file_type = EXT_TO_TYPE[ext][0]
            end = True
        else:
            try:
                point_pos = ext.index('.', 1)
                ext = ext[point_pos:]
            except Exception:
                end = True
                file_type = "application/octet-stream"

    return file_type


def list_directory(directory_path: str, expected_extension: str = None):
    """
    Recursive function for listing files in a folder and his sub folders

    :param directory_path: path of the parsed dir
    :param expected_extension: list of extension separated by |
    :return: list(str)
    """
    file_list = list()
    for root, directories, files in os.walk(directory_path, topdown=False):
        for name in files:
            full_path = os.path.join(root, name)
            if expected_extension is not None:
                if re.search("\\.({})$".format(expected_extension), name) is None: continue
            file_list.append(full_path)
        if expected_extension is None:
            for name in directories:
                file_list.append(os.path.join(root, name))
    return file_list


def listing_of_directory(path: str, level: int = 1, list_base_content: list = [], list_excluded_directory: list = []):
    some_dir = path.rstrip(os.path.sep)
    list_of_dir = list_base_content
    if os.path.isdir(some_dir):
        num_sep = some_dir.count(os.path.sep)
        for root, dirs, files in os.walk(some_dir):
            num_sep_this = root.count(os.path.sep)
            for name in dirs:
                if name in list_excluded_directory: continue
                if num_sep + level > num_sep_this:
                    list_of_dir.append(name)
    return list_of_dir


def list_directory_tree(base_directory: str, ext: str = None):
    list_of_file = list_directory(base_directory, ext)
    list_of_file.sort()
    # print(listOfFile)

    tree_files = dict()
    for file in list_of_file:
        __list_directory_tree_recursive(file, base_directory + os.sep, tree_files)
    return tree_files


def __list_directory_tree_recursive(file: str, path: str, parent_file_tree: dict):
    sub_path = file.replace(path, '')
    sub_path_tab = sub_path.split(os.sep)

    if isinstance(sub_path_tab, list):
        if len(sub_path_tab) > 1:
            if sub_path_tab[0] not in parent_file_tree:
                parent_file_tree[sub_path_tab[0]] = dict()
            if isinstance(parent_file_tree[sub_path_tab[0]], dict):
                __list_directory_tree_recursive(file, path + sub_path_tab[0] + os.sep, parent_file_tree[sub_path_tab[0]])
        else:
            if os.path.isfile(file): parent_file_tree[sub_path] = file
            else: parent_file_tree[sub_path] = dict()


def clean_dir(src_dir: str):
    for dirpath, _, _ in os.walk(src_dir, topdown=False):  # Listing the files
        if dirpath == src_dir: break
        try: os.rmdir(dirpath)
        except Exception: ''


def rmDir(src_dir: str):
    shutil.rmtree(src_dir, ignore_errors=True)


def copyDir(src_dir: str, dest_dir: str):
    shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)


def copyFile(src_dir: str, dest_dir: str):
    shutil.copyfile(src_dir, dest_dir)


def rename(src_dir: str, dest_dir: str):
    shutil.move(src_dir, dest_dir)


def hashFile(path: str):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(path, 'rb') as file:
        buf = file.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = file.read(BLOCKSIZE)
    return hasher.hexdigest()
