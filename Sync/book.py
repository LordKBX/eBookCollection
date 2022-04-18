import traceback, asyncio
import base64
import time
import copy
import common.common
import common.bdd
import json
import Sync


def get_book_cover(parent: any, book_id: str = None) -> ([{}], int, str):
    rez = []
    data = None
    error_id = 0
    error_label = ""
    try:
        if book_id is not None:
            rez = parent.server.parent.bddd.get_books(book_id)
        if rez is None or rez.__len__() == 0:
            error_id = 7
            error_label = "Invalid book ID"
        else:
            data = rez[0]['cover']
    except:
        traceback.print_exc()

    return data, error_id, error_label


def get_book_files_info(parent: any, book_id: str = None) -> ([{}], int, str):
    rez = []
    data = None
    error_id = 0
    error_label = ""
    if book_id is not None:
        rez = parent.server.parent.bddd.get_books(book_id)
    if rez.__len__() == 0:
        error_id = 7
        error_label = "Invalid book ID"
    else:
        data = rez[0]['files']
        for i in range(0, len(data)):
            del data[i]['link']

    return data, error_id, error_label


def get_book_file(parent: any, book_id: str = None, file_id: str = None) -> ([{}], int, str):
    rez = []
    data = None
    error_id = 0
    error_label = ""
    if book_id is not None:
        rez = parent.server.parent.bddd.get_books(book_id)
    if rez.__len__() == 0:
        error_id = 7
        error_label = "Invalid book ID"
    else:
        if file_id is None:
            data = rez[0]['files'][0]
        else:
            for file in rez[0]['files']:
                print(file)
                if file['guid'] == file_id:
                    data = file
                    break
        data['name'] = common.common.filename_cleaner(rez[0]['authors'] + ' - ' + rez[0]['series'] + ' - ' + rez[0]['title']) + '.' + data['format'].lower()

    return data, error_id, error_label
