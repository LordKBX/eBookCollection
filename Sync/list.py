import traceback, asyncio
import base64
import time
import copy
import common.common
import common.bdd
import json
import Sync


def list_books(parent: any, search: str = None) -> ([{}], int, str):
    rez = []
    error_id = 0
    error_label = ""
    if search is not None:
        rez = parent.server.parent.bddd.get_books(None, "search:"+search)
    else:
        rez = parent.server.parent.bddd.get_books()
    rez2 = []
    for book in rez:
        bk = copy.deepcopy(book)
        del bk['files']
        del bk['cover']
        rez2.append(bk)
    rez = rez2

    return rez, error_id, error_label


def list_authors(parent: any) -> ([{}], int, str):
    rez = []
    error_id = 0
    error_label = ""
    rez = parent.server.parent.bddd.get_authors()

    return rez, error_id, error_label


def list_series(parent: any) -> ([{}], int, str):
    rez = []
    error_id = 0
    error_label = ""
    rez = parent.server.parent.bddd.get_series()

    return rez, error_id, error_label
