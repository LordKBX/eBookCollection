# This Python file uses the following encoding: utf-8
import sys, os, shutil, traceback, time
import PyQt5.QtCore
import sqlite3
# sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from common.common import *
from common.files import *
from common.vars import *


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
    def __init__(self, directory: str = None):
        self.settings = PyQt5.QtCore.QSettings("LordKBX Workshop", app_name)
        self.connexion = None
        self.cursor = None
        self.__directory = self.get_param('library/directory')
        if directory is None and self.__directory is None:
            self.__directory = os.path.expanduser('~') + os.sep + app_name + os.sep + 'data'
            if os.path.isdir(self.__directory) is False:
                os.makedirs(self.__directory)
        elif directory is not None:
            self.__directory = directory
        self.__database_filename = 'database.db'

        self.__directory = self.__directory.replace('{APP_DIR}', app_directory)
        if os.path.isdir(self.__directory) is False:
            self.__directory = app_directory + os.sep + 'data'
            self.set_param('library/directory', '{APP_DIR}' + os.sep + 'data')
        print(self.__directory)
        self.__start()

    def __start(self):
        self.connexion = sqlite3.connect(self.__directory + os.sep + self.__database_filename)
        self.connexion.row_factory = dict_factory
        self.cursor = self.connexion.cursor()

        self.cursor.execute('''PRAGMA table_info('books')''')
        ret = self.cursor.fetchone()
        if ret is None:
            self.cursor.execute('''CREATE TABLE books('guid' TEXT PRIMARY KEY NOT NULL, 'title' TEXT NOT NULL, 
                    'authors' TEXT, 'series' TEXT, 'import_date' TEXT NOT NULL, 'last_update_date' TEXT NOT NULL, 
                    'tags' TEXT, 'synopsis' TEXT, 'cover' TEXT NOT NULL)''')

        self.cursor.execute('''PRAGMA table_info('files')''')
        ret = self.cursor.fetchone()
        if ret is None:
            self.cursor.execute('''CREATE TABLE files(
                    'guid_file' TEXT PRIMARY KEY NOT NULL, 
                    'book_id' TEXT NOT NULL, 
                    'size' TEXT NOT NULL, 
                    'format' TEXT NOT NULL, 
                    'link' TEXT NOT NULL, 
                    'file_import_date' TEXT NOT NULL, 
                    'file_last_update_date' TEXT NOT NULL, 
                    'file_last_read_date' TEXT NOT NULL, 
                    'file_hash' TEXT NOT NULL, 
                    'bookmark' TEXT)''')

        self.connexion.commit()

    def close(self):
        """
        Close database
        """
        if self.connexion is not None:
            self.cursor.close()
            self.connexion.close()
            self.cursor = None
            self.connexion = None

    def migrate(self, new_folder: str):
        """
        Migrate database file

        :param new_folder:
        :return:
        """
        try:
            if os.path.isdir(new_folder) is False:
                return
            self.close()
            copyDir(self.__directory, new_folder)
            rmDir(self.__directory)
            self.__directory = new_folder
            self.set_param('library/directory', new_folder)
            self.__start()
        except Exception:
            traceback.print_exc()

    def get_param(self, name: str):
        """
        Get setting value in database

        :param name: param value
        :return: string|None
        """
        return self.settings.value(name, None, str)

    def set_param(self, name: str, value: str):
        """
        Set setting value in database

        :param name: param name
        :param value: param value
        :return:
        """
        self.settings.setValue(name, value)

    def get_authors(self):
        """
        get Authors in database

        :return: list(str)
        """
        ret = []
        self.cursor.execute('''SELECT authors FROM books GROUP BY authors ORDER BY authors ASC''')
        rows = self.cursor.fetchall()
        if rows is not None:
            for row in rows:
                ret.append(row['authors'])
        return ret

    def get_series(self):
        """
        get Series in database

        :return: list(str)
        """
        ret = []
        self.cursor.execute('''SELECT series FROM books GROUP BY series ORDER BY series ASC''')
        re = self.cursor.fetchall()
        if re is not None:
            for row in re:
                ret.append(row['series'])
        return ret

    def get_books(self, guid: str = None, search: str = None):
        """
        get registred book in database

        :param guid: guid of the book
        :param search: research patern
        :return: list(dict)
        """
        return_list = []
        ret = None
        if guid is None and search is None:
            self.cursor.execute('SELECT * FROM books LEFT JOIN files ON(files.book_id = books.guid) '
                                'ORDER BY title ASC')
            ret = self.cursor.fetchall()
        else:
            if guid is not None:
                self.cursor.execute("SELECT * FROM books LEFT JOIN files ON(files.book_id = books.guid) "
                                    "WHERE guid = '"+guid+"'")
                ret = self.cursor.fetchall()
            elif search is not None:
                if re.search("^authors:", search) or re.search("^serie:", search):
                    tab = search.split(':')
                    self.cursor.execute("SELECT * FROM books LEFT JOIN files ON(files.book_id = books.guid) "
                                        "WHERE " + tab[0] + " = '" + tab[1] + "'")
                    ret = self.cursor.fetchall()
        if ret is not None:
            prev_guid = ''
            for row in ret:
                if prev_guid != row['guid']:
                    prev_guid = row['guid']
                    return_list.append({
                        'guid': row['guid'],
                        'title': row['title'],
                        'authors': row['authors'],
                        'series': row['series'],
                        'import_date': row['import_date'],
                        'last_update_date': row['last_update_date'],
                        'tags': row['tags'],
                        'synopsis': row['synopsis'],
                        'cover': row['cover'],
                        'files': []
                    })
                return_list[len(return_list) - 1]['files'].append({
                    'guid': row['guid_file'],
                    'size': row['size'],
                    'format': row['format'],
                    'link': row['link'],
                    'import_date': row['file_import_date'],
                    'last_update_date': row['file_last_update_date'],
                    'last_read_date': row['file_last_read_date'],
                    'file_hash': row['file_hash'],
                    'bookmark': row['bookmark']
                })

        return return_list

    def insert_book(self, guid: str, title: str, series: str, authors: str, tags: str, size: str, format: str, link: str, cover: str):
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
        self.cursor.execute(
                '''INSERT INTO books(
                'guid','title','series','authors','tags','cover',
                'import_date','last_update_date') 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?)''',
                (guid, title, series, authors, tags, cover, dt, dt)
            )
        file_hash = hashFile(link)
        self.cursor.execute(
                '''INSERT INTO files(
                'guid_file','book_id','size','format','link','file_import_date',
                'file_last_update_date','file_last_read_date','file_hash','bookmark') 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (uid(), guid, size, format, link, dt, dt, dt, file_hash, None)
            )
        self.connexion.commit()

    def update_book(self, guid: str, col: str, value: str, file_guid: str = None):
        """

        :param guid:
        :param col:
        :param value:
        :param file_guid:
        :return:
        """
        try:
            dt = time.time()
            if file_guid is None:
                self.cursor.execute(
                    'UPDATE books SET `'+col+'` = ?, last_update_date = ? WHERE guid = ?', (value, dt, guid)
                )
            else:
                self.cursor.execute(
                    'UPDATE files SET `'+col+'` = ?, file_last_update_date = ? WHERE book_id = ? AND guid_file = ?',
                    (value, dt, guid, file_guid)
                )
            self.connexion.commit()
        except Exception:
            traceback.print_exc()

    def delete_book(self, guid: str, file_guid: str = None):
        """

        :param guid:
        :param file_guid:
        :return:
        """
        try:
            dt = time.time()
            if file_guid is None:
                self.cursor.execute('DELETE FROM books WHERE guid = \'{}\''.format(guid))
                self.cursor.execute('DELETE FROM files WHERE book_id = \'{}\''.format(guid))
            else:
                self.cursor.execute('DELETE FROM files WHERE book_id = ? AND guid_file = ?', (guid, file_guid))
            self.connexion.commit()
        except Exception:
            traceback.print_exc()