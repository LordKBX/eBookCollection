# This Python file uses the following encoding: utf-8
import sys
import os
import traceback
import time
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
            'bookmark' TEXT, 'tags' TEXT, 'synopsis' TEXT,
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
            self.cursor.execute("SELECT value FROM settings WHERE name = \"{}\"".format(name))
            ret = self.cursor.fetchone()
            if ret is not None: return ret['value']
            else: return None
        except Exception:
            traceback.print_exc()
            return None

    def setParam(self, name: str, value: str):
        """
        Set setting value in database

        :param name: param name
        :param value: param value
        :return:
        """
        try:
            if self.getParam(name) is None:
                self.cursor.execute('''INSERT INTO settings('name','value') VALUES(?, ?)''', (name, value))
            else:
                self.cursor.execute('''UPDATE settings SET value = ? WHERE name = ?''', (value, name))
            self.connexion.commit()
        except Exception:
            traceback.print_exc()

    def getAuthors(self):
        """
        get Authors in database

        :return: list(str)
        """
        ret = []
        self.cursor.execute('''SELECT authors FROM books''')
        re = self.cursor.fetchall()
        for row in re:
            ret.append(row['authors'])
        return ret

    def getSeries(self):
        """
        get Series in database

        :return: list(str)
        """
        ret = []
        self.cursor.execute('''SELECT serie FROM books''')
        re = self.cursor.fetchall()
        for row in re:
            ret.append(row['authors'])
        return ret

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
        else:
            if guid is not None:
                self.cursor.execute("SELECT * FROM books WHERE guid = '"+guid+"'")
                ret = self.cursor.fetchall()
        return ret

    def insertBook(self, guid: str, title: str, serie: str, authors: str, tags: str, size: str, format: str, link: str, cover: str):
        """

        :param guid:
        :param title:
        :param serie:
        :param authors:
        :param tags:
        :param size:
        :param format:
        :param link:
        :param cover:
        :return:
        """
        dt = time.time()
        self.cursor.execute('''INSERT INTO books(
                'guid','title','serie','authors','tags','size','format','link','cover','bookmark',
                'import_date','last_update_date','last_read_date') 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (guid, title, serie, authors, tags, size, format, link, cover, '', dt, dt, dt)
            )
        self.connexion.commit()