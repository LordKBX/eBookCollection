# This Python file uses the following encoding: utf-8
import sys
import os
import shutil
import subprocess
import traceback

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import PyQt5.uic
from PyQt5.uic import *

# sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from common import *
from lang import *
import bdd


class HomeWindow(QWidget):
    def __init__(self, database: bdd.BDD, translation: Lang, env_vars: dict):
        self.BDD = database
        self.lang = translation
        self.tools = env_vars['tools']
        self.env_vars = env_vars['vars']
        super(HomeWindow, self).__init__()
        PyQt5.uic.loadUi('home/home.ui', self) # Load the .ui file
        self.setLocalisation()
        self.setInfoPanel()
        self.loadooks(self.BDD.getBooks())

        self.CentralBlockTable.currentCellChanged.connect(self.CentralBlockTableNewSelection)
        self.CentralBlockTable.itemChanged.connect(self.CentralBlockTableItemChanged)

        self.HeaderBlockBtnAddBook.clicked.connect(self.HeaderBlockBtnAddBookClicked)
        self.HeaderBlockBtnSettings.clicked.connect(self.HeaderBlockBtnSettingsClicked)

        self.show() # Show the GUI

    def CentralBlockTableNewSelection(self, currentRow, currentColumn, previousRow, previousColumn):
        """
        Slot for new selection on the Central Block Table Widget

        :param currentRow:
        :param currentColumn:
        :param previousRow:
        :param previousColumn:
        :return: void
        """
        print("--------------------------------")
        print("new position : {}x{}".format(currentRow, currentColumn))
        print("old position : {}x{}".format(previousRow, previousColumn))
        print("tag line : {}".format(self.CentralBlockTable.item(currentRow, currentColumn).data(1)))

    def CentralBlockTableItemChanged(self, newItem):
        """
        Slot for new item content on the Central Block Table Widget

        :param newItem: the modified QTableWidgetItem
        :return: void
        """
        print("--------------------------------")
        print("Row = {}".format(newItem.row()))
        print("Column = {}".format(newItem.column()))
        print(newItem.text())

    def HeaderBlockBtnAddBookClicked(self):
        """
        Slot for click on the Add Book Button

        :return: void
        """
        try:
            # load parameters for file import
            file_name_template = self.bdd.getParam('import_file_template')
            file_name_separator = self.bdd.getParam('import_file_separator')
            # test parameters for file import and assign default value if not set
            if file_name_template is None:
                file_name_template = self.env_vars['import_file_template']['default']
            if file_name_separator is None:
                file_name_separator = self.env_vars['import_file_separator']

            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            files, _ = QFileDialog.getOpenFileNames(
                self, self.lang['Home']['AddBookWindowTitle'], "",
                "Ebook (*.epub *.epub2 *.epub3 *.cbz *.cbr *.pdf *.mobi);;Texte (*.txt *.doc *.docx *.rtf)",
                options=options
            )
            print(files)
            if len(files) > 0:
                for file in files:
                    if os.path.isfile(file) is True:
                        # list of var for future injection into database
                        tmp_guid = ''
                        tmp_cover = ''
                        tmp_title = ''
                        tmp_serie = ''
                        tmp_authors = ''
                        tmp_tags = ''
                        tmp_size = ''
                        tmp_format = ''

                        filepath, ext = os.path.splitext(file)  # Get file path and extension
                        tmp_format = ext[1:].upper()  # assign file type into var for future injection into database
                        t = filepath.split('/')  # explode file path into a list
                        filename = t[len(t) - 1]  # get file name without extension
                        tmpdir = 'tmp/'+filename.replace(' ', '_')  # create var for temporary file extraction
                        print('filename = '+filename)
                        print('ext = '+tmp_format)
                        if os.path.isdir(tmpdir) is True: shutil.rmtree(tmpdir)  # delete temp dir if already exist
                        os.makedirs(tmpdir)  # make temp dir

                        tab_mask = file_name_template.split(file_name_separator)
                        tab_file = filename.split(file_name_separator)
                        i = 0
                        while i < len(tab_file):
                            if tab_mask[i] == '%title%': tmp_title = tab_file[i]
                            if tab_mask[i] == '%authors%': tmp_authors = tab_file[i]
                            if tab_mask[i] == '%serie%': tmp_serie = tab_file[i]
                            if tab_mask[i] == '%tags%': tmp_tags = tab_file[i]
                            i += 1

                        if ext in ['.epub', '.epub2', '.epub3']:  # section for EPUB files
                            {}
                        if ext in ['.cbz', '.cbr']:  # section for CBZ and CBR files
                            tmp_guid = uid()  # assign random guid for CBZ and CBR books
                            list_args = list()  # create list argument for external command execution
                            list_args.append(self.tools['7zip'][os.name]['path'])  # insert executable path
                            temp_args = self.tools['7zip'][os.name]['params_deflate'].split(' ')  # create table of raw command arguments
                            for var in temp_args:  # parse table of raw command arguments
                                # insert parsed param
                                list_args.append(var.replace('%input%', file).replace('%output%', tmpdir))
                            print(list_args)
                            ret = subprocess.check_output(list_args, universal_newlines=True)  # execute the command
                            print(ret)
                            tmp_cover = listDir(tmpdir)[0]  # get path of the first image into temp dir

                        #shutil.rmtree(tmpdir)  # delete temp dir
                {}
        except Exception:
            traceback.print_exc()

    def HeaderBlockBtnSettingsClicked(self):
        """
        Slot for click on the Settings Button

        :return: void
        """
        print("Bouton Options clické")

    def setLocalisation(self):
        """
        translate window text with the content of the lang object

        :return: void
        """
        # Titre fenêtre
        self.setWindowTitle(self.lang['Home']['WindowTitle'])
        # Boutons du bandeau
        self.HeaderBlockBtnAddBook.setToolTip(self.lang['Home']['HeaderBlockBtnAddBook'])
        self.HeaderBlockBtnSettings.setToolTip(self.lang['Home']['HeaderBlockBtnSettings'])
        # Panneau de gauche
        self.SortingBlockTree.topLevelItem(0).setText(0, self.lang['Home']['SortingBlockTreeAll'])
        self.SortingBlockTree.topLevelItem(1).setText(0, self.lang['Home']['SortingBlockTreeSeries'])
        self.SortingBlockTree.topLevelItem(2).setText(0, self.lang['Home']['SortingBlockTreeAuthors'])
        # Panneau central
        self.CentralBlockTable.horizontalHeaderItem(0).setText(self.lang['Home']['CentralBlockTableTitle'])
        self.CentralBlockTable.horizontalHeaderItem(1).setText(self.lang['Home']['CentralBlockTableAuthors'])
        self.CentralBlockTable.horizontalHeaderItem(2).setText(self.lang['Home']['CentralBlockTableSeries'])
        self.CentralBlockTable.horizontalHeaderItem(3).setText(self.lang['Home']['CentralBlockTableTags'])
        # Panneau de droite
        self.InfoBlockTitleLabel.setText(self.lang['Home']['InfoBlockTitleLabel'])
        self.InfoBlockSerieLabel.setText(self.lang['Home']['InfoBlockSerieLabel'])
        self.InfoBlockAuthorsLabel.setText(self.lang['Home']['InfoBlockAuthorsLabel'])
        self.InfoBlockFileFormatsLabel.setText(self.lang['Home']['InfoBlockFileFormatsLabel'])
        self.InfoBlockSizeLabel.setText(self.lang['Home']['InfoBlockSizeLabel'])
        self.InfoBlockSynopsisLabel.setText(self.lang['Home']['InfoBlockSynopsisLabel'])

    def setInfoPanel(self, book: dict = None):
        """
        Insert into the info pannel the details values of the book

        :param book: dict of the spécified book
        :return: void
        """
        passed = True
        if book is None: passed = False
        else:
            if not is_in(book, ['title', 'serie', 'authors', 'formats', 'size', 'synopsis']):
                passed = False

        if passed is True:
            self.InfoBlockTitleValue.setText(book['title'])
            self.InfoBlockSerieValue.setText(book['serie'])
            self.InfoBlockAuthorsValue.setText(book['authors'])
            self.InfoBlockFileFormatsValue.setText(book['formats'])
            self.InfoBlockSizeValue.setText(book['size'])
            self.InfoBlockSynopsisValue.setText(book['synopsis'])
        else:
            self.InfoBlockTitleValue.setText("")
            self.InfoBlockSerieValue.setText("")
            self.InfoBlockAuthorsValue.setText("")
            self.InfoBlockFileFormatsValue.setText("")
            self.InfoBlockSizeValue.setText("")
            self.InfoBlockSynopsisValue.setText("")

    def newBookTableItem(self, guid: str, value: str):
        """
        Create item for the Central Block Table Widget

        :param guid: guid book
        :param value: case item value
        :return: QTableWidgetItem
        """
        item = QtWidgets.QTableWidgetItem()
        item.setData(1, guid)
        item.setText(value)
        item.setToolTip(value)
        return item

    def loadooks(self, books: list):
        """
        load book list into the Central Block Table Widget

        :param books: list(dir)
        :return: void
        """
        self.CentralBlockTable.clearContents()
        # self.CentralBlockTable.setCornerButtonEnabled(False)
        line = 0
        self.CentralBlockTable.setRowCount(len(books))
        for book in books:
            """
            item = QtWidgets.QTableWidgetItem()
            item.setText("{}".format(line + 1))
            self.CentralBlockTable.setVerticalHeaderItem(line, item)
            """
            # Title
            self.CentralBlockTable.setItem(line, 0, self.newBookTableItem(book['guid'], book['title']))
            # authors
            self.CentralBlockTable.setItem(line, 1, self.newBookTableItem(book['guid'], book['authors']))
            # serie
            self.CentralBlockTable.setItem(line, 2, self.newBookTableItem(book['guid'], book['serie']))
            # tags
            self.CentralBlockTable.setItem(line, 3, self.newBookTableItem(book['guid'], book['tags']))

            line += 1
