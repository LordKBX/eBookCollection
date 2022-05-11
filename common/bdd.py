# This Python file uses the following encoding: utf-8
import sys, os, shutil, traceback, time
import PyQt5.QtCore
import sqlite3

from typing import List

from .common import *
from .files import *
from .vars import *


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
    # /!\ FOR PREVENTING AUTO MIGRATION ERROR FOLLOW THE RULES :
    # - DO NOT PUT 'NOT NULL' ON NUMERIC COLUMN
    # - IF YOU ADD A COLUMN PUT IT AT THE END OF THE CONCERNED TABLE
    # - DO NOT RENAME A COLUMN
    # - DO NOT DELETE A COLUMN
    tables = {
        'versions': [
            {'name': 'name', 'type': 'TEXT', 'ext': 'TEXT PRIMARY KEY NOT NULL'},
            {'name': 'version', 'type': 'NUMERIC', 'ext': 'NUMERIC DEFAULT 1'}
        ],
        'books': [
            {'name': 'table_version', 'type': 'CONTROL', 'ext': '2'},
            {'name': 'guid', 'type': 'TEXT', 'ext': 'TEXT PRIMARY KEY NOT NULL'},
            {'name': 'title', 'type': 'TEXT', 'ext': 'TEXT NOT NULL'},
            {'name': 'authors', 'type': 'TEXT', 'ext': 'TEXT', 'def': ''},
            {'name': 'series', 'type': 'TEXT', 'ext': 'TEXT', 'def': ''},
            {'name': 'tags', 'type': 'TEXT', 'ext': 'TEXT', 'def': ''},
            {'name': 'synopsis', 'type': 'TEXT', 'ext': 'TEXT', 'def': ''},
            {'name': 'cover', 'type': 'TEXT', 'ext': 'TEXT NOT NULL'},
            {'name': 'import_date', 'type': 'NUMERIC', 'ext': 'NUMERIC DEFAULT 0', 'def': '0'},
            {'name': 'last_update_date', 'type': 'NUMERIC', 'ext': 'NUMERIC DEFAULT 0', 'def': '0'},
            {'name': 'series_vol', 'type': 'NUMERIC', 'ext': 'NUMERIC DEFAULT 0', 'def': '0'}
        ],
        'files': [
            {'name': 'table_version', 'type': 'CONTROL', 'ext': '3'},
            {'name': 'guid_file', 'type': 'TEXT', 'ext': 'TEXT PRIMARY KEY NOT NULL'},
            {'name': 'book_id', 'type': 'TEXT', 'ext': 'TEXT NOT NULL'},
            {'name': 'size', 'type': 'TEXT', 'ext': 'TEXT NOT NULL'},
            {'name': 'format', 'type': 'TEXT', 'ext': 'TEXT NOT NULL'},
            {'name': 'link', 'type': 'TEXT', 'ext': 'TEXT NOT NULL'},
            {'name': 'file_hash', 'type': 'TEXT', 'ext': 'TEXT NOT NULL'},
            {'name': 'bookmark', 'type': 'TEXT', 'ext': 'TEXT', 'def': ''},
            {'name': 'file_import_date', 'type': 'NUMERIC', 'ext': 'NUMERIC DEFAULT 0', 'def': '0'},
            {'name': 'file_last_update_date', 'type': 'NUMERIC', 'ext': 'NUMERIC DEFAULT 0', 'def': '0'},
            {'name': 'file_last_read_date', 'type': 'NUMERIC', 'ext': 'NUMERIC DEFAULT 0', 'def': '0'},
            {'name': 'editors', 'type': 'TEXT', 'ext': 'TEXT', 'def': ''},
            {'name': 'lang', 'type': 'TEXT', 'ext': 'TEXT', 'def': ''},
            {'name': 'publication_date', 'type': 'NUMERIC', 'ext': 'NUMERIC DEFAULT 0', 'def': '0'}
        ]
    }
    old_tables = {
        'versions': {
            1: [
                {'name': 'name', 'type': 'TEXT', 'ext': 'TEXT PRIMARY KEY NOT NULL'},
                {'name': 'version', 'type': 'NUMERIC', 'ext': 'NUMERIC DEFAULT 1'}
            ]
        },
        'books': {
            1: [
                {'name': 'guid', 'type': 'TEXT', 'ext': 'TEXT PRIMARY KEY NOT NULL'},
                {'name': 'title', 'type': 'TEXT', 'ext': 'TEXT NOT NULL'},
                {'name': 'authors', 'type': 'TEXT', 'ext': 'TEXT'},
                {'name': 'serie', 'type': 'TEXT', 'ext': 'TEXT'},
                {'name': 'tags', 'type': 'TEXT', 'ext': 'TEXT'},
                {'name': 'synopsis', 'type': 'TEXT', 'ext': 'TEXT'},
                {'name': 'cover', 'type': 'TEXT', 'ext': 'TEXT NOT NULL'},
                {'name': 'import_date', 'type': 'NUMERIC', 'ext': 'NUMERIC DEFAULT 0'},
                {'name': 'last_update_date', 'type': 'NUMERIC', 'ext': 'NUMERIC DEFAULT 0'}
            ]
        },
        'files': {
            1: [
                {'name': 'guid_file', 'type': 'TEXT', 'ext': 'TEXT PRIMARY KEY NOT NULL'},
                {'name': 'book_id', 'type': 'TEXT', 'ext': 'TEXT NOT NULL'},
                {'name': 'size', 'type': 'TEXT', 'ext': 'TEXT NOT NULL'},
                {'name': 'format', 'type': 'TEXT', 'ext': 'TEXT NOT NULL'},
                {'name': 'link', 'type': 'TEXT', 'ext': 'TEXT NOT NULL'},
                {'name': 'file_hash', 'type': 'TEXT', 'ext': 'TEXT NOT NULL'},
                {'name': 'bookmark', 'type': 'TEXT', 'ext': 'TEXT'},
                {'name': 'file_import_date', 'type': 'NUMERIC', 'ext': 'NUMERIC DEFAULT 0'},
                {'name': 'file_last_update_date', 'type': 'NUMERIC', 'ext': 'NUMERIC DEFAULT 0'},
                {'name': 'file_last_read_date', 'type': 'NUMERIC', 'ext': 'NUMERIC DEFAULT 0'}
            ],
            2: [
                {'name': 'table_version', 'type': 'CONTROL', 'ext': '2'},
                {'name': 'guid_file', 'type': 'TEXT', 'ext': 'TEXT PRIMARY KEY NOT NULL'},
                {'name': 'book_id', 'type': 'TEXT', 'ext': 'TEXT NOT NULL'},
                {'name': 'size', 'type': 'TEXT', 'ext': 'TEXT NOT NULL'},
                {'name': 'format', 'type': 'TEXT', 'ext': 'TEXT NOT NULL'},
                {'name': 'link', 'type': 'TEXT', 'ext': 'TEXT NOT NULL'},
                {'name': 'file_hash', 'type': 'TEXT', 'ext': 'TEXT NOT NULL'},
                {'name': 'bookmark', 'type': 'TEXT', 'ext': 'TEXT'},
                {'name': 'file_import_date', 'type': 'NUMERIC', 'ext': 'NUMERIC DEFAULT 0'},
                {'name': 'file_last_update_date', 'type': 'NUMERIC', 'ext': 'NUMERIC DEFAULT 0'},
                {'name': 'file_last_read_date', 'type': 'NUMERIC', 'ext': 'NUMERIC DEFAULT 0'},
                {'name': 'editors', 'type': 'TEXT', 'ext': 'TEXT'},
                {'name': 'lang', 'type': 'TEXT', 'ext': 'TEXT'}
            ]
        }
    }
    param_defaults = {
        'sync/ip': '0.0.0.0',
        'sync/port': 33004,
        'sync/user': 'admin',
        'sync/password': 'BookOfTheYear'
    }

    def __init__(self, directory: str = None):
        self.settings = PyQt5.QtCore.QSettings(app_editor, app_name)
        self.connexion = None
        self.cursor = None
        self.__directory = self.get_param('library/directory')
        if directory is None and self.__directory is None:
            self.__directory = env_vars['vars']['default_storage']
            if os.path.isdir(self.__directory) is False:
                os.makedirs(self.__directory)
        elif directory is not None:
            self.__directory = directory
        self.__database_filename = 'database.db'

        self.__directory = self.__directory
        if os.path.isdir(self.__directory) is False:
            self.__directory = env_vars['vars']['default_storage']
            self.set_param('library/directory', env_vars['vars']['default_storage'])
        print(self.__directory)
        # self.__start()

    def __create_table_request(self, table: str, alt_name: str = None) -> str or None:
        if table not in self.tables:
            return None
        if alt_name is not None and alt_name.strip() != '':
            ret = 'CREATE TABLE ' + alt_name.strip() + '('
        else:
            ret = 'CREATE TABLE ' + table + '('
        i = 0
        ver = 0
        for line in self.tables[table]:
            if line['name'] == 'table_version':
                ver = int(float(line['ext']))
                continue
            if i > 0: ret += ', '
            ret += '\'' + line['name'] + '\' ' + line['ext']
            i += 1
        ret += ')'
        return ret, ver

    def __test_table(self, table: str, request_ret: list) -> bool:
        if table not in self.tables: return None
        for line in self.tables[table]:
            if line['name'] == 'table_version':
                continue
            line_ok = False
            for req_line in request_ret:
                if req_line['name'] == line['name']:
                    if req_line['type'] == line['type']:
                        line_ok = True
                        break
            if line_ok is False:
                return False
        return True

    def __auto_refit_table(self, table: str):
        if table not in self.tables: return None
        alt_table = table + '_alt'

        try:
            ret, ver = self.__create_table_request(table, alt_table)
            self.cursor.execute(ret)
        except Exception:
            traceback.print_exc()

        self.cursor.execute('SELECT * from "' + table + '"')
        ret = self.cursor.fetchall()
        req = 'INSERT INTO "' + alt_table + '"('
        part1_Ok = False
        blocks = []
        if ret is not None:
            for row in ret:
                block = '('
                for req_line in self.tables[table]:
                    if req_line['name'] == 'table_version':
                        continue
                    if part1_Ok is False:
                        if req_line['name'] in row or 'def' in req_line:
                            req += ',"' + req_line['name'] + '"'
                    if block != '(':
                        block += ','
                    if req_line['name'] in row:
                        block += '"{}" '.format(row[req_line['name']])
                    else:
                        if 'def' in req_line:
                            if req_line['def'] is None:
                                block += 'NULL '
                            else:
                                block += '"{}" '.format(req_line['def'])
                        else:
                            block += 'NULL '
                blocks.append(block + ')')
                part1_Ok = True
            req = req.replace("(,", "(")
            req += ') VALUES'
            reqf = req + ','.join(blocks)

        print(reqf)
        self.cursor.execute(reqf)

        self.cursor.execute("PRAGMA defer_foreign_keys = '1'")
        self.cursor.execute('DROP TABLE "main"."' + table + '"')
        self.cursor.execute('ALTER TABLE "main"."' + alt_table + '" RENAME TO "' + table + '"')
        self.connexion.commit()

    def __start(self):
        if os.path.isdir(self.__directory) is False:
            try: os.makedirs(self.__directory)
            except Exception: traceback.print_exc()
        clean_dir(self.__directory)
        self.connexion = sqlite3.connect(self.__directory + os.sep + self.__database_filename, check_same_thread=False)
        self.connexion.row_factory = dict_factory
        self.cursor = self.connexion.cursor()

        for table in self.tables:
            self.cursor.execute("PRAGMA table_xinfo('" + table + "')")
            ret = self.cursor.fetchall()
            req, ver = self.__create_table_request(table)
            if len(ret) == 0:
                self.cursor.execute(req)
                if ver > 0:
                    self.cursor.execute('INSERT INTO versions(name, version)  VALUES(?, ?)', (table, ver))
            else:
                if self.__test_table(table, ret) is False:
                    self.__auto_refit_table(table)
                    self.cursor.execute('UPDATE versions SET version = ? WHERE name = ?', (ver, table))

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
            self.cursor.execute("UPDATE files SET link = REPLACE(link, '" + self.__directory + "', '" + new_folder + "')")
            if self.connexion is not None:
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
        if name in self.param_defaults:
            return self.settings.value(name, self.param_defaults[name], str)
        else:
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
        if self.connexion is None:
            self.__start()
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
        if self.connexion is None:
            self.__start()
        ret = []
        self.cursor.execute('''SELECT series FROM books GROUP BY series ORDER BY series ASC''')
        re = self.cursor.fetchall()
        if re is not None:
            for row in re:
                ret.append(row['series'])
        return ret

    def get_books(self, guid: str or List[str] = None, search: str = None, no_file_path: bool = False):
        """
        get registred book in database

        :param guid: guid or list of guid of the book(s)
        :param search: research patern
        :param no_file_path: secify if file path must be send
        :return: list(dict)
        """
        if self.connexion is None:
            self.__start()
        return_list = []
        ret = None
        if guid is None and search is None:
            self.cursor.execute('SELECT * FROM books LEFT JOIN files ON(files.book_id = books.guid) '
                                'ORDER BY title ASC')
            ret = self.cursor.fetchall()
        else:
            if guid is not None:
                if isinstance(guid, str):
                    self.cursor.execute("SELECT * FROM books LEFT JOIN files ON(files.book_id = books.guid) "
                                        "WHERE guid = '" + guid + "'")
                elif isinstance(guid, list):
                    guil = ''
                    for gu in guid:
                        if guil != '':
                            guil += ','
                        guil += '\'' + gu + '\''
                    query = "SELECT * FROM books LEFT JOIN files ON(files.book_id = books.guid) WHERE guid IN (" + guil + ")"
                    print(query)
                    self.cursor.execute(query)
                ret = self.cursor.fetchall()
            elif search is not None:
                tab = search.split(':')
                if tab[0] == "authors" or tab[0] == "series":
                    print(tab[0])
                    self.cursor.execute("SELECT * FROM books LEFT JOIN files ON(files.book_id = books.guid) WHERE " + tab[0] + " = ?", [tab[1]])
                    ret = self.cursor.fetchall()
                elif tab[0] == "file":
                    self.cursor.execute(
                        "SELECT * FROM books JOIN files ON(files.book_id = books.guid) WHERE files.link = ?", [tab[1]])
                    ret = self.cursor.fetchall()
                elif re.search("^search:", search):
                    item = tab[1].lower()
                    self.cursor.execute(
                        "SELECT * FROM books JOIN files ON(files.book_id = books.guid) WHERE LOWER(books.title) LIKE ? OR LOWER(books.series) LIKE ? OR LOWER(books.authors) LIKE ? OR LOWER(books.tags) LIKE ?",
                        ['%' + item + '%', '%' + item + '%', '%' + item + '%', '%' + item + '%']
                    )
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
                        'series_vol': row['series_vol'],
                        'import_date': row['import_date'],
                        'last_update_date': row['last_update_date'],
                        'tags': row['tags'],
                        'synopsis': row['synopsis'],
                        'cover': row['cover'],
                        'files': []
                    })
                if no_file_path is False:
                    return_list[len(return_list) - 1]['files'].append({
                        'guid': row['guid_file'],
                        'size': row['size'],
                        'format': row['format'],
                        'link': row['link'],
                        'editors': row['editors'],
                        'publication_date': row['publication_date'],
                        'lang': row['lang'],
                        'import_date': row['file_import_date'],
                        'last_update_date': row['file_last_update_date'],
                        'last_read_date': row['file_last_read_date'],
                        'file_hash': row['file_hash'],
                        'bookmark': row['bookmark']
                    })
                else:
                    return_list[len(return_list) - 1]['files'].append({
                        'guid': row['guid_file'],
                        'size': row['size'],
                        'format': row['format'],
                        'editors': row['editors'],
                        'publication_date': row['publication_date'],
                        'lang': row['lang'],
                        'import_date': row['file_import_date'],
                        'last_update_date': row['file_last_update_date'],
                        'last_read_date': row['file_last_read_date'],
                        'file_hash': row['file_hash'],
                        'bookmark': row['bookmark']
                    })

        return return_list

    def insert_book(self, guid: str, title: str = None, series: str = None, authors: str = None,
                    tags: str = None, size: str = None, file_format: str = None, link: str = None, cover: str = "",
                    lang: str = None, editors: str = None, publication_date: int = 0):
        """

        :param guid:
        :param title:
        :param series:
        :param authors:
        :param tags:
        :param size:
        :param file_format:
        :param link:
        :param cover:
        :param lang:
        :param editors:
        :param publication_date:
        :return:
        """
        if self.connexion is None:
            self.__start()
        dt = time.time()
        if cover is None: cover = ""
        if title is not None and title.strip() != '':
            self.cursor.execute(
                '''INSERT INTO books(
                    'guid','title','series','authors','tags','cover',
                    'import_date','last_update_date') 
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?)''',
                (guid, title, series, authors, tags, cover, dt, dt)
            )
        if link is not None:
            link = link.replace('/', os.sep)
            file_hash = hashFile(link)
            self.cursor.execute(
                '''INSERT INTO files(
                    'guid_file','book_id','size','format','link','file_import_date',
                    'file_last_update_date','file_last_read_date','file_hash','bookmark','lang', 'editors', 'publication_date') 
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (uid(), guid, size, file_format, link, dt, dt, dt, file_hash, None, lang, editors, publication_date)
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
        if self.connexion is None:
            self.__start()
        try:
            dt = time.time()
            if file_guid is None:
                print('UPDATE books SET `' + col + '` = ?, last_update_date = ? WHERE guid = ?', (value, dt, guid))
                self.cursor.execute(
                    'UPDATE books SET `' + col + '` = ?, last_update_date = ? WHERE guid = ?', (value, dt, guid)
                )
            else:
                print('UPDATE files SET `' + col + '` = ?, file_last_update_date = ? WHERE book_id = ? AND guid_file = ?',
                    (value, dt, guid, file_guid))
                self.cursor.execute(
                    'UPDATE files SET `' + col + '` = ?, file_last_update_date = ? WHERE book_id = ? AND guid_file = ?',
                    (value, dt, guid, file_guid)
                )
            self.connexion.commit()
        except Exception:
            traceback.print_exc()

    def delete_book(self, guid: str = None, file_guid: str = None):
        """

        :param guid:
        :param file_guid:
        :return:
        """
        if guid is None and file_guid is None:
            return None
        if guid is not None and guid.strip() == '':
            return None
        if file_guid is not None and file_guid.strip() == '':
            return None
        if self.connexion is None:
            self.__start()
        try:
            dt = time.time()
            if guid is not None and file_guid is None:
                self.cursor.execute('DELETE FROM books WHERE guid = \'{}\''.format(guid))
                self.cursor.execute('DELETE FROM files WHERE book_id = \'{}\''.format(guid))
            elif guid is None and file_guid is not None:
                self.cursor.execute(
                    'DELETE FROM files WHERE guid_file = \'{}\' OR link = \'{}\''.format(file_guid, file_guid))
            else:
                self.cursor.execute('DELETE FROM files WHERE book_id = ? AND guid_file = ?', (guid, file_guid))
            self.connexion.commit()
        except Exception:
            traceback.print_exc()
