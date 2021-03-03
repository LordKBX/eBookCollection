# This Python file uses the following encoding: utf-8
import os, sys
from PyQt5.QtWidgets import *
import PyQt5.QtCore
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
from home.settings import *
import home.empty_book


class HomeWindow(QMainWindow, HomeWindowCentralBlock, HomeWindowInfoPanel, HomeWindowSortingBlockTree):
    def __init__(self, database: bdd.BDD, translation: Lang, env_vars: dict, argv: list):
        self.app_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.currentBook = ''
        self.BDD = database
        self.lang = translation
        self.tools = env_vars['tools']
        self.env_vars = env_vars['vars']
        self.argv = argv
        super(HomeWindow, self).__init__()
        PyQt5.uic.loadUi('home/home.ui', self)  # Load the .ui file*
        size_tx = self.BDD.get_param('home/windowSize')
        if size_tx is not None:
            size = eval(size_tx)
            self.resize(size[0], size[1])

        # load parameters for file import
        self.app_lang = None
        self.app_style = None

        list_test_param = [
            {'parameter': 'defaultCover/background', 'default': self.env_vars["default_cover"]["background"]},
            {'parameter': 'defaultCover/pattern', 'default': self.env_vars["default_cover"]["pattern"]},
            {'parameter': 'defaultCover/pattern_color', 'default': self.env_vars["default_cover"]["pattern_color"]},
            {'parameter': 'defaultCover/title', 'default': self.env_vars["default_cover"]["title"]},
            {'parameter': 'defaultCover/series', 'default': self.env_vars["default_cover"]["series"]},
            {'parameter': 'defaultCover/authors', 'default': self.env_vars["default_cover"]["authors"]},
            {'parameter': 'home/lastOpenDir', 'default': app_directory},
            {'parameter': 'import_file_separator', 'default': self.env_vars["import_file_separator"]},
            {'parameter': 'import_file_template', 'default': self.env_vars['import_file_template']['default']},

            {'parameter': 'style', 'default': self.env_vars["default_style"], 'var': 'app_style'},
            {'parameter': 'lang', 'default': self.env_vars["default_language"], 'var': 'app_lang'}
        ]

        for obj in list_test_param:
            var = self.BDD.get_param(obj['parameter'])
            if var is None or var == '':
                self.BDD.set_param(obj['parameter'], obj['default'])
                var = obj['default']
            if 'var' in obj:
                if obj['var'] == 'app_style':
                    self.app_style = var
                if obj['var'] == 'app_lang':
                    self.app_lang = var

        self.lang.set_lang(self.app_lang)
        self.set_style()
        self.set_localisation()
        self.set_info_panel()
        # self.load_books(self.BDD.get_books())

        self.header_block_btn_add_book.clicked.connect(self.header_block_btn_add_book_clicked)
        self.header_block_btn_create_book.clicked.connect(self.header_block_btn_create_book_clicked)
        self.header_block_btn_settings.clicked.connect(self.header_block_btn_settings_clicked)
        self.header_block_btn_del_book.clicked.connect(self.header_block_btn_del_book_clicked)

        self.central_block_table_define_slots()

        self.sorting_block_tree_init()
        self.sorting_block_tree_load_data()
        self.sorting_block_tree_set_filter('all')

        self.show()  # Show the GUI
        try:
            if self.argv[1] == "settings":
                self.header_block_btn_settings_clicked()
        except Exception:
            ""

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        size = self.size()
        tx = [size.width(), size.height()].__str__()
        self.BDD.set_param('home/windowSize', tx)

    def header_block_btn_add_book_clicked(self):
        """
        Slot for click on the Add Book Button

        :return: void
        """
        try:
            # load parameters for file import
            file_name_template = self.BDD.get_param('import_file_template')
            file_name_separator = self.BDD.get_param('import_file_separator')

            options = QFileDialog.Options()
            # options |= QFileDialog.DontUseNativeDialog
            list_files, _ = QFileDialog.getOpenFileNames(
                self, self.lang['Home']['AddBookWindowTitle'], self.BDD.get_param('home/lastOpenDir'),
                "eBook (*.epub *.epub2 *.epub3 *.cbz *.cbr *.pdf *.mobi);;Texte (*.txt *.doc *.docx *.rtf)",
                options=options
            )
            if len(list_files) > 0:
                selected_directory = list_files[0].replace('/', os.sep)
                selected_index = selected_directory.rindex(""+os.sep)
                selected_directory = selected_directory[0:selected_index]
                self.BDD.set_param('home/lastOpenDir', selected_directory)
                for file in list_files:
                    # Call booksTools.insert_book
                    insert_book(self.BDD, file_name_template, file_name_separator, file)
                self.central_block_table.clearSelection()
                self.sorting_block_tree_set_filter(self.sorting_block_tree_actual_filter)

        except Exception:
            traceback.print_exc()

    def header_block_btn_create_book_clicked(self):
        """
        Slot for click on the Add Book Button

        :return: void
        """
        try:
            empty_ui = home.empty_book.EmptyBookWindow(self, self.BDD)
            ret = empty_ui.open_exec()
            if ret is not None:
                try:
                    rmDir(app_directory+os.sep+'tmp')
                    os.makedirs(app_directory + os.sep + 'tmp')
                except Exception:
                    ""

                if ret['format'] == 'EPUB':
                    vol = ret['vol']
                    file = create_epub(ret['name'], ret['authors'], ret['serie'], vol)

                    # load parameters for file import
                    file_name_template = self.BDD.get_param('import_file_template')
                    file_name_separator = self.BDD.get_param('import_file_separator')
                    insert_book(self.BDD, file_name_template, file_name_separator, file)
                self.central_block_table.clearSelection()
                self.sorting_block_tree_set_filter(self.sorting_block_tree_actual_filter)

            print(ret)
        except Exception:
            traceback.print_exc()

    def header_block_btn_settings_clicked(self):
        """
        Slot for click on the Settings Button

        :return: void
        """
        print("Bouton Options clické")
        try:
            dialog = SettingsWindow(self, self.BDD)
            ret = dialog.open_exec()
            try:
                if ret is not None:
                    self.app_lang = self.BDD.get_param('lang')
                    self.app_style = self.BDD.get_param('style')
                    self.set_localisation()
                    self.set_style()
                if self.argv[1] == "settings":
                    sys.exit(0)
            except Exception:
                traceback.print_exc()
        except Exception:
            traceback.print_exc()

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
                            for file in self.BDD.get_books(book_id)[0]['files']:
                                try:
                                    os.remove(file['link'].replace('\\', '/').replace('/', os.sep))
                                except Exception:
                                    traceback.print_exc()

                            self.BDD.delete_book(book_id)
                            print("line n° {}".format(item.row()))
                    # Cleanup all empty folder in data folder
                    clean_dir('./data')
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
        # Titres blocks
        self.header_block.setWindowTitle(self.lang['Home']['blockHeaderTitle'])
        self.sorting_block.setWindowTitle(self.lang['Home']['blockSortTitle'])
        self.info_block.setWindowTitle(self.lang['Home']['blockInfoTitle'])
        # Boutons du bandeau
        self.header_block_btn_add_book.setToolTip(self.lang['Home']['HeaderBlockBtnAddBook'])
        self.header_block_btn_create_book.setToolTip(self.lang['Home']['HeaderBlockBtnCreateBook'])
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

    def set_style(self):
        self.setStyleSheet(env_vars['styles'][self.app_style]['QMainWindow'])
        self.header_block_contents2.setStyleSheet(env_vars['styles'][self.app_style]['QMainWindow'])
        self.sorting_block_contents.setStyleSheet(env_vars['styles'][self.app_style]['QMainWindow'])
        # self.central_block_table = QTableWidget()
        self.central_block_table.horizontalHeader().setStyleSheet(env_vars['styles'][self.app_style]['QTableWidget'])
        self.central_block_table.setStyleSheet(env_vars['styles'][self.app_style]['QTableWidget'])
        self.central_block_table.horizontalHeader().setSortIndicatorShown(True)

