# This Python file uses the following encoding: utf-8
import sys
import os
import sqlite3
# sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from common import *


def dict_factory(cursor, row):
    """
    factory for sqlite permiting the return of request in dict format

    :param cursor: cursor of the sqlite object
    :param row: a request return row
    :return: dict
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class BDD:
    def __init__(self):
        self.connexion = sqlite3.connect('database.db')
        self.connexion.row_factory = dict_factory
        self.cursor = self.connexion.cursor()

        self.cursor.execute('''PRAGMA table_info('books')''')
        ret = self.cursor.fetchone()
        if ret is None:
            self.cursor.execute('''CREATE TABLE books('guid' TEXT PRIMARY KEY NOT NULL, 'title' TEXT NOT NULL, 
            'authors' TEXT, 'serie' TEXT, 'size' TEXT NOT NULL, 'format' TEXT NOT NULL, 'link' TEXT NOT NULL, 
            'import_date' TEXT NOT NULL, 'last_update_date' TEXT NOT NULL, 'last_read_date' TEXT NOT NULL, 
            'bookmark' TEXT, 'tags' TEXT, 
            'cover' TEXT NOT NULL)''')

        self.cursor.execute('''PRAGMA table_info('settings')''')
        ret = self.cursor.fetchone()
        if ret is None:
            self.cursor.execute('''CREATE TABLE settings('name' TEXT PRIMARY KEY NOT NULL, 'value' TEXT)''')

        self.connexion.commit()

    def getParam(self, name: str):
        """
        Get setting value in database

        :param name: param value
        :return: string|None
        """
        try:
            self.cursor.execute('''SELECT value FROM settings WHERE name = ?''', (name))
            return self.cursor.fetchone()
        except Exception:
            return None

    def setParam(self, name: str, value: str):
        """
        Set setting value in database

        :param name: param name
        :param value: param value
        :return:
        """
        if self.getParam(name) is None:
            self.cursor.execute('''INSERT INTO settings('name','value') VALUES(?, ?)''', (name, value))
        else:
            self.cursor.execute('''UPDATE settings SET value = ? WHERE name = ?''', (value, name))
        self.connexion.commit()

    def getBooks(self, guid: str = None, search: str = None):
        """
        get registred book in database

        :param guid: guid of the book
        :param search: research patern
        :return: list(dict)
        """
        ret = []
        if guid is None and search is None:
            self.cursor.execute('''SELECT * FROM books''')
            ret = self.cursor.fetchall()
        return ret