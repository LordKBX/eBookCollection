# This Python file uses the following encoding: utf-8
import os, sys
from PyQt5.QtWidgets import *
import PyQt5.uic
from PyQt5.uic import *

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from common.dialog import *
from lang import *
from common.books import *
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
        # self.loadooks(self.BDD.getBooks())

        self.HeaderBlockBtnAddBook.clicked.connect(self.HeaderBlockBtnAddBookClicked)
        self.HeaderBlockBtnSettings.clicked.connect(self.HeaderBlockBtnSettingsClicked)
        self.HeaderBlockBtnDelBook.clicked.connect(self.HeaderBlockBtnDelBookClicked)

        self.CentralBlockTableDefineSlots()

        self.SortingBlockTreeInit()
        self.SortingBlockTreeLoadData()
        self.SortingBlockTreeSetFilter('all')

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
                self, self.lang['Home']['AddBookWindowTitle'], "D:\\Calibre_bookstore\\Kaida Spanner(Gui Ying supana)\\Lazy Dungeon Master Arc 01_ Hey, I' (116)",
                "Ebook (*.epub *.epub2 *.epub3 *.cbz *.cbr *.pdf *.mobi);;Texte (*.txt *.doc *.docx *.rtf)",
                options=options
            )
            if len(files) > 0:
                for file in files:
                    # Call booksTools.insertBook
                    insertBook(self.tools, self.BDD, file_name_template, file_name_separator, file)
                self.CentralBlockTable.clearSelection()
                self.SortingBlockTreeSetFilter(self.SortingBlockTreeActualFilter)

        except Exception:
            traceback.print_exc()

    def HeaderBlockBtnSettingsClicked(self):
        """
        Slot for click on the Settings Button

        :return: void
        """
        print("Bouton Options clické")

    def HeaderBlockBtnDelBookClicked(self):
        """
        Slot for click on the Delete book Button

        :return: void
        """
        try:
            print("Bouton Delete book clické")
            if len(self.CentralBlockTable.selectedItems()) > 0:
                ret = WarnDialogConfirm(
                    self.lang['Home']['DialogConfirmDeleteBookWindowTitle'],
                    self.lang['Home']['DialogConfirmDeleteBookWindowText'],
                    self.lang['Home']['DialogConfirmDeleteBookBtnYes'],
                    self.lang['Home']['DialogConfirmDeleteBookBtnNo'],
                    self
                )

                if ret is True:
                    items = self.CentralBlockTable.selectedItems()
                    self.CentralBlockTable.clearSelection()
                    for item in items:
                        if item.column() == 0:
                            book_id = item.data(99)
                            for file in self.BDD.getBooks(book_id)[0]['files']:
                                try: os.remove(self.appDir + '/' + file['link'])
                                except Exception: {}

                            self.BDD.deleteBook(book_id)
                            print("line n° {}".format(item.row()))
                    # Cleanup all empty folder in data folder
                    cleanDir('./data')
                    self.SortingBlockTreeSetFilter(self.SortingBlockTreeActualFilter)
                    self.setInfoPanel(None)
        except Exception:
            traceback.print_exc()

    def setLocalisation(self):
        """
        translate window text with the content of the lang object

        :return: void
        """
        # Titre fenêtre
        self.setWindowTitle(self.lang['Home']['WindowTitle'])
        # Boutons du bandeau
        self.HeaderBlockBtnAddBook.setToolTip(self.lang['Home']['HeaderBlockBtnAddBook'])
        self.HeaderBlockBtnDelBook.setToolTip(self.lang['Home']['HeaderBlockBtnDelBook'])
        self.HeaderBlockBtnSettings.setToolTip(self.lang['Home']['HeaderBlockBtnSettings'])
        # Panneau de gauche
        self.SortingBlockTree.topLevelItem(0).setText(0, self.lang['Home']['SortingBlockTreeAll'])
        self.SortingBlockTree.topLevelItem(0).setText(1, 'all')
        self.SortingBlockTree.topLevelItem(1).setText(0, self.lang['Home']['SortingBlockTreeAuthors'])
        self.SortingBlockTree.topLevelItem(1).setText(1, 'authors')
        self.SortingBlockTree.topLevelItem(2).setText(0, self.lang['Home']['SortingBlockTreeSeries'])
        self.SortingBlockTree.topLevelItem(2).setText(1, 'serie')

        self.SortingBlockSearchLabel.setText(self.lang['Home']['SortingBlockSearchLabel'])
        # Panneau central
        self.CentralBlockTable.clear()
        self.CentralBlockTable.setColumnCount(6)
        item = QtWidgets.QTableWidgetItem()
        item.setText(self.lang['Home']['CentralBlockTableTitle'])
        self.CentralBlockTable.setHorizontalHeaderItem(0, item)

        item = QtWidgets.QTableWidgetItem()
        item.setText(self.lang['Home']['CentralBlockTableAuthors'])
        self.CentralBlockTable.setHorizontalHeaderItem(1, item)

        item = QtWidgets.QTableWidgetItem()
        item.setText(self.lang['Home']['CentralBlockTableSeries'])
        self.CentralBlockTable.setHorizontalHeaderItem(2, item)

        item = QTableAltItem()
        item.lock(True)
        item.setText(self.lang['Home']['CentralBlockTableTags'])
        self.CentralBlockTable.setHorizontalHeaderItem(3, item)

        item = QtWidgets.QTableWidgetItem()
        item.setText(self.lang['Home']['CentralBlockTableAdded'])
        self.CentralBlockTable.setHorizontalHeaderItem(4, item)

        item = QtWidgets.QTableWidgetItem()
        item.setText(self.lang['Home']['CentralBlockTableModified'])
        self.CentralBlockTable.setHorizontalHeaderItem(5, item)
        # Panneau de info
        self.InfoBlockTitleLabel.setText(self.lang['Home']['InfoBlockTitleLabel'])
        self.InfoBlockSerieLabel.setText(self.lang['Home']['InfoBlockSerieLabel'])
        self.InfoBlockAuthorsLabel.setText(self.lang['Home']['InfoBlockAuthorsLabel'])
        self.InfoBlockFileFormatsLabel.setText(self.lang['Home']['InfoBlockFileFormatsLabel'])
        self.InfoBlockSizeLabel.setText(self.lang['Home']['InfoBlockSizeLabel'])

