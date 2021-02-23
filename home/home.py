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
        self.app_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.currentBook = ''
        self.BDD = database
        self.lang = translation
        self.tools = env_vars['tools']
        self.env_vars = env_vars['vars']
        super(HomeWindow, self).__init__()
        PyQt5.uic.loadUi('home/home.ui', self) # Load the .ui file
        self.set_localisation()
        self.set_info_panel()
        # self.load_books(self.BDD.getBooks())

        self.header_block_btn_add_book.clicked.connect(self.header_block_btn_add_book_clicked)
        self.header_block_btn_settings.clicked.connect(self.header_block_btn_settings_clicked)
        self.header_block_btn_del_book.clicked.connect(self.header_block_btn_del_book_clicked)

        self.central_block_table_define_slots()

        self.sorting_block_tree_init()
        self.sorting_block_tree_load_data()
        self.sorting_block_tree_set_filter('all')

        self.show() # Show the GUI

    def header_block_btn_add_book_clicked(self):
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
                self.central_block_table.clearSelection()
                self.sorting_block_tree_set_filter(self.sorting_block_tree_actual_filter)

        except Exception:
            traceback.print_exc()

    @staticmethod
    def header_block_btn_settings_clicked():
        """
        Slot for click on the Settings Button

        :return: void
        """
        print("Bouton Options clické")

    def header_block_btn_del_book_clicked(self):
        """
        Slot for click on the Delete book Button

        :return: void
        """
        try:
            print("Bouton Delete book clické")
            if len(self.central_block_table.selectedItems()) > 0:
                ret = WarnDialogConfirm(
                    self.lang['Home']['DialogConfirmDeleteBookWindowTitle'],
                    self.lang['Home']['DialogConfirmDeleteBookWindowText'],
                    self.lang['Home']['DialogConfirmDeleteBookBtnYes'],
                    self.lang['Home']['DialogConfirmDeleteBookBtnNo'],
                    self
                )

                if ret is True:
                    items = self.central_block_table.selectedItems()
                    self.central_block_table.clearSelection()
                    for item in items:
                        if item.column() == 0:
                            book_id = item.data(99)
                            for file in self.BDD.getBooks(book_id)[0]['files']:
                                try: os.remove(self.app_directory + '/' + file['link'])
                                except Exception: {}

                            self.BDD.deleteBook(book_id)
                            print("line n° {}".format(item.row()))
                    # Cleanup all empty folder in data folder
                    cleanDir('./data')
                    self.sorting_block_tree_set_filter(self.sorting_block_tree_actual_filter)
                    self.set_info_panel(None)
        except Exception:
            traceback.print_exc()

    def set_localisation(self):
        """
        translate window text with the content of the lang object

        :return: void
        """
        # Titre fenêtre
        self.setWindowTitle(self.lang['Home']['WindowTitle'])
        # Boutons du bandeau
        self.header_block_btn_add_book.setToolTip(self.lang['Home']['HeaderBlockBtnAddBook'])
        self.header_block_btn_del_book.setToolTip(self.lang['Home']['HeaderBlockBtnDelBook'])
        self.header_block_btn_settings.setToolTip(self.lang['Home']['HeaderBlockBtnSettings'])
        # Panneau de gauche
        self.sorting_block_tree.topLevelItem(0).setText(0, self.lang['Home']['SortingBlockTreeAll'])
        self.sorting_block_tree.topLevelItem(0).setText(1, 'all')
        self.sorting_block_tree.topLevelItem(1).setText(0, self.lang['Home']['SortingBlockTreeAuthors'])
        self.sorting_block_tree.topLevelItem(1).setText(1, 'authors')
        self.sorting_block_tree.topLevelItem(2).setText(0, self.lang['Home']['SortingBlockTreeSeries'])
        self.sorting_block_tree.topLevelItem(2).setText(1, 'serie')

        self.sorting_block_search_label.setText(self.lang['Home']['SortingBlockSearchLabel'])
        # Panneau central
        self.central_block_table.clear()
        self.central_block_table.setColumnCount(6)
        item = QtWidgets.QTableWidgetItem()
        item.setText(self.lang['Home']['CentralBlockTableTitle'])
        self.central_block_table.setHorizontalHeaderItem(0, item)

        item = QtWidgets.QTableWidgetItem()
        item.setText(self.lang['Home']['CentralBlockTableAuthors'])
        self.central_block_table.setHorizontalHeaderItem(1, item)

        item = QtWidgets.QTableWidgetItem()
        item.setText(self.lang['Home']['CentralBlockTableSeries'])
        self.central_block_table.setHorizontalHeaderItem(2, item)

        item = QTableAltItem()
        item.lock(True)
        item.setText(self.lang['Home']['CentralBlockTableTags'])
        self.central_block_table.setHorizontalHeaderItem(3, item)

        item = QtWidgets.QTableWidgetItem()
        item.setText(self.lang['Home']['CentralBlockTableAdded'])
        self.central_block_table.setHorizontalHeaderItem(4, item)

        item = QtWidgets.QTableWidgetItem()
        item.setText(self.lang['Home']['CentralBlockTableModified'])
        self.central_block_table.setHorizontalHeaderItem(5, item)
        # Panneau de info
        self.info_block_title_label.setText(self.lang['Home']['InfoBlockTitleLabel'])
        self.info_block_serie_label.setText(self.lang['Home']['InfoBlockSerieLabel'])
        self.info_block_authors_label.setText(self.lang['Home']['InfoBlockAuthorsLabel'])
        self.info_block_file_formats_label.setText(self.lang['Home']['InfoBlockFileFormatsLabel'])
        self.info_block_size_label.setText(self.lang['Home']['InfoBlockSizeLabel'])

