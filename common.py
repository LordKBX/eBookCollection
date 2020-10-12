import uuid
import os


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