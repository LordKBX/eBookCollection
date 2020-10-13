# This Python file uses the following encoding: utf-8
import sys
import os
import shutil
import subprocess
import traceback
import json

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import PyQt5.uic
from PyQt5.uic import *

# sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from common import *
from lang import *
from booksTools import *
import bdd

from home.CentralBlockTable import *
from home.InfoPanel import *
from home.SortingBlockTree import *


class HomeWindow(QWidget, HomeWindowCentralBlock, HomeWindowInfoPanel, HomeWindowSortingBlockTree):
    def __init__(self, database: bdd.BDD, translation: Lang, env_vars: dict):
        self.appDir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.currentBook = ''
        self.BDD = database
        self.lang = translation
        self.tools = env_vars['tools']
        self.env_vars = env_vars['vars']
        super(HomeWindow, self).__init__()
        PyQt5.uic.loadUi('home/home.ui', self) # Load the .ui file
        self.setLocalisation()
        self.setInfoPanel()
        self.loadooks(self.BDD.getBooks())

        self.HeaderBlockBtnAddBook.clicked.connect(self.HeaderBlockBtnAddBookClicked)
        self.HeaderBlockBtnSettings.clicked.connect(self.HeaderBlockBtnSettingsClicked)

        self.CentralBlockTableDefineSlots()
        self.SortingBlockTreeInit()

        self.show() # Show the GUI

    def HeaderBlockBtnAddBookClicked(self):
        """
        Slot for click on the Add Book Button

        :return: void
        """
        try:
            # load parameters for file import
            file_name_template = self.BDD.getParam('import_file_template')
            file_name_separator = self.BDD.getParam('import_file_separator')
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
            if len(files) > 0:
                for file in files:
                    # Call booksTools.insertBook
                    insertBook(self.tools, self.BDD, file_name_template, file_name_separator, file)

                self.loadooks(self.BDD.getBooks())
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
        self.CentralBlockTable.horizontalHeaderItem(4).setText(self.lang['Home']['CentralBlockTableModified'])
        # Panneau de droite
        self.InfoBlockTitleLabel.setText(self.lang['Home']['InfoBlockTitleLabel'])
        self.InfoBlockSerieLabel.setText(self.lang['Home']['InfoBlockSerieLabel'])
        self.InfoBlockAuthorsLabel.setText(self.lang['Home']['InfoBlockAuthorsLabel'])
        self.InfoBlockFileFormatsLabel.setText(self.lang['Home']['InfoBlockFileFormatsLabel'])
        self.InfoBlockSizeLabel.setText(self.lang['Home']['InfoBlockSizeLabel'])
        self.InfoBlockSynopsisLabel.setText(self.lang['Home']['InfoBlockSynopsisLabel'])



    def newBookTableItem(self, guid: str, type: str, value: str, editable: bool = True):
        """
        Create item for the Central Block Table Widget

        :param guid: guid book
        :param type: case item type
        :param value: case item value
        :return: QTableWidgetItem
        """
        item = QtWidgets.QTableWidgetItem()
        if editable is True:
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
        else:
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        item.setData(99, guid)
        item.setData(100, type)
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
        header_size_policy = self.env_vars['home_central_table_header_size_policy']
        if header_size_policy in ['ResizeToContents', 'ResizeToContentsAndInteractive']:
            self.CentralBlockTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        if header_size_policy == 'Stretch':
            self.CentralBlockTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        if header_size_policy == 'UserDefined':
            sizes = []
            try:
                sizes = json.loads(self.env_vars['home_central_table_header_sizes'])
                self.CentralBlockTable.setColumnWidth(0, sizes[0])
                self.CentralBlockTable.setColumnWidth(1, sizes[1])
                self.CentralBlockTable.setColumnWidth(2, sizes[2])
                self.CentralBlockTable.setColumnWidth(3, sizes[3])
                self.CentralBlockTable.setColumnWidth(4, sizes[4])
            except Exception:
                traceback.print_exc()
            self.CentralBlockTable.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
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
            self.CentralBlockTable.setItem(line, 0, self.newBookTableItem(book['guid'], 'title', book['title']))
            # authors
            self.CentralBlockTable.setItem(line, 1, self.newBookTableItem(book['guid'], 'authors', book['authors']))
            # serie
            self.CentralBlockTable.setItem(line, 2, self.newBookTableItem(book['guid'], 'serie', book['serie']))
            # tags
            self.CentralBlockTable.setItem(line, 3, self.newBookTableItem(book['guid'], 'tags', book['tags']))
            # Modified
            self.CentralBlockTable.setItem(line, 4,
                self.newBookTableItem(
                    book['guid'],
                    'modified',
                    unixtimeToString(
                        float(book['last_update_date']),
                        self.lang['Time']['template']['textual_date'],
                        self.lang['Time']['months_short']
                    ),
                    False
                )
            )

            line += 1

        if header_size_policy == 'ResizeToContentsAndInteractive':
            timer = QtCore.QTimer()
            timer.singleShot(500, self.delayedTableHeaderInteractiveMode)

    def delayedTableHeaderInteractiveMode(self):
        self.CentralBlockTable.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

