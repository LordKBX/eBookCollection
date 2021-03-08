# This Python file uses the following encoding: utf-8
import os, sys
import PyQt5.QtCore
import PyQt5.uic
from PyQt5.uic import *

from common.dialog import *
from common.lang import *
from common.books import *
from common import bdd

from CentralBlockTable import *
from InfoPanel import *
from SortingBlockTree import *
from settings import *
import empty_book


class HomeWindow(QMainWindow, HomeWindowCentralBlock, HomeWindowInfoPanel, HomeWindowSortingBlockTree):
    def __init__(self, database: bdd.BDD, translation: Lang, argv: list, env_vars: dict):
        super(HomeWindow, self).__init__()
        PyQt5.uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'home.ui', self)  # Load the .ui file

        # load vars and base objects
        self.app_directory = app_directory
        self.currentBook = ''
        self.env_vars = env_vars
        self.BDD = database
        self.lang = translation
        self.tools = env_vars['tools']
        self.env_vars = self.vars = env_vars['vars']
        self.argv = argv

        # load window size
        size_tx = self.BDD.get_param('library/windowSize')
        if size_tx is not None and size_tx != '':
            size = eval(size_tx)
            self.resize(size[0], size[1])
        # load window position
        pos_tx = self.BDD.get_param('library/windowPos')
        if pos_tx is not None and pos_tx != '':
            pos = eval(pos_tx)
            self.move(pos[0], pos[1])
            self.pos()

        # load parameters
        self.app_lang = None
        self.app_style = None

        list_test_param = [
            {'parameter': 'defaultCover/background', 'default': self.env_vars["default_cover"]["background"]},
            {'parameter': 'defaultCover/pattern', 'default': self.env_vars["default_cover"]["pattern"]},
            {'parameter': 'defaultCover/pattern_color', 'default': self.env_vars["default_cover"]["pattern_color"]},
            {'parameter': 'defaultCover/title', 'default': self.env_vars["default_cover"]["title"]},
            {'parameter': 'defaultCover/series', 'default': self.env_vars["default_cover"]["series"]},
            {'parameter': 'defaultCover/authors', 'default': self.env_vars["default_cover"]["authors"]},
            {'parameter': 'library/lastOpenDir', 'default': app_directory},
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
        self.load_books(self.BDD.get_books())

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
            if self.tools['archiver']['path'] is None:
                WarnDialog(self.lang['Global/ArchiverErrorTitle'], self.lang['Global/ArchiverErrorText'])
                self.header_block_btn_settings_clicked()
            if "settings" in self.argv:
                self.header_block_btn_settings_clicked()
                sys.exit(0)
        except Exception:
            traceback.print_exc()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        size = self.size()
        tx = [size.width(), size.height()].__str__()
        self.BDD.set_param('library/windowSize', tx)

    def moveEvent(self, a0: QtGui.QMoveEvent) -> None:
        pos = self.pos()
        tx = [pos.x(), pos.y()].__str__()
        self.BDD.set_param('library/windowPos', tx)

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
                self, self.lang['Library']['AddBookWindowTitle'], self.BDD.get_param('library/lastOpenDir'),
                "eBook (*.epub *.epub2 *.epub3 *.cbz *.cbr *.pdf *.mobi);;Texte (*.txt *.doc *.docx *.rtf)",
                options=options
            )
            if len(list_files) > 0:
                selected_directory = list_files[0].replace('/', os.sep)
                selected_index = selected_directory.rindex(""+os.sep)
                selected_directory = selected_directory[0:selected_index]
                self.BDD.set_param('library/lastOpenDir', selected_directory)
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
            empty_ui = empty_book.EmptyBookWindow(self, self.BDD)
            ret = empty_ui.open_exec()
            if ret is not None:
                try:
                    rmDir(app_directory+os.sep+'tmp')
                    os.makedirs(app_directory + os.sep + 'tmp')
                except Exception:
                    ""

                if ret['format'] == 'EPUB':
                    vol = ret['vol']
                    cover_style = {
                        "background": self.BDD.get_param('defaultCover/background'),
                        "pattern": self.BDD.get_param('defaultCover/pattern'),
                        "pattern_color": self.BDD.get_param('defaultCover/pattern_color'),
                        "title": self.BDD.get_param('defaultCover/title'),
                        "series": self.BDD.get_param('defaultCover/series'),
                        "authors": self.BDD.get_param('defaultCover/authors'),
                    }

                    file = create_epub(
                        ret['name'], ret['authors'], ret['series'], vol,
                        file_name_template=self.BDD.get_param('import_file_template'), style=cover_style
                    )

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
                if len(self.argv) > 1:
                    if "settings" in self.argv:
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
                    self.lang['Library']['DialogConfirmDeleteBookWindowTitle'],
                    self.lang['Library']['DialogConfirmDeleteBookWindowText'],
                    self.lang['Library']['DialogConfirmDeleteBookBtnYes'],
                    self.lang['Library']['DialogConfirmDeleteBookBtnNo'],
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
        self.setWindowTitle(self.lang['Library']['WindowTitle'])
        # Titres blocks
        self.header_block.setWindowTitle(self.lang['Library']['blockHeaderTitle'])
        self.sorting_block.setWindowTitle(self.lang['Library']['blockSortTitle'])
        self.info_block.setWindowTitle(self.lang['Library']['blockInfoTitle'])
        # Boutons du bandeau
        self.header_block_btn_add_book.setToolTip(self.lang['Library']['HeaderBlockBtnAddBook'])
        self.header_block_btn_create_book.setToolTip(self.lang['Library']['HeaderBlockBtnCreateBook'])
        self.header_block_btn_del_book.setToolTip(self.lang['Library']['HeaderBlockBtnDelBook'])
        self.header_block_btn_settings.setToolTip(self.lang['Library']['HeaderBlockBtnSettings'])
        # Panneau de gauche
        self.sorting_block_tree.topLevelItem(0).setText(0, self.lang['Library']['SortingBlockTreeAll'])
        self.sorting_block_tree.topLevelItem(0).setText(1, 'all')
        self.sorting_block_tree.topLevelItem(1).setText(0, self.lang['Library']['SortingBlockTreeAuthors'])
        self.sorting_block_tree.topLevelItem(1).setText(1, 'authors')
        self.sorting_block_tree.topLevelItem(2).setText(0, self.lang['Library']['SortingBlockTreeSeries'])
        self.sorting_block_tree.topLevelItem(2).setText(1, 'series')

        self.sorting_block_search_label.setText(self.lang['Library']['SortingBlockSearchLabel'])
        # Panneau central
        self.central_block_table.setColumnCount(6)
        item = QtWidgets.QTableWidgetItem()
        item.setText(self.lang['Library']['CentralBlockTableTitle'])
        self.central_block_table.setHorizontalHeaderItem(0, item)

        item = QtWidgets.QTableWidgetItem()
        item.setText(self.lang['Library']['CentralBlockTableAuthors'])
        self.central_block_table.setHorizontalHeaderItem(1, item)

        item = QtWidgets.QTableWidgetItem()
        item.setText(self.lang['Library']['CentralBlockTableSeries'])
        self.central_block_table.setHorizontalHeaderItem(2, item)

        item = QTableAltItem()
        item.lock(True)
        item.setText(self.lang['Library']['CentralBlockTableTags'])
        self.central_block_table.setHorizontalHeaderItem(3, item)

        item = QtWidgets.QTableWidgetItem()
        item.setText(self.lang['Library']['CentralBlockTableAdded'])
        self.central_block_table.setHorizontalHeaderItem(4, item)

        item = QtWidgets.QTableWidgetItem()
        item.setText(self.lang['Library']['CentralBlockTableModified'])
        self.central_block_table.setHorizontalHeaderItem(5, item)
        # Panneau de info
        self.info_block_title_label.setText(self.lang['Library']['InfoBlockTitleLabel'])
        self.info_block_serie_label.setText(self.lang['Library']['InfoBlockSerieLabel'])
        self.info_block_authors_label.setText(self.lang['Library']['InfoBlockAuthorsLabel'])
        self.info_block_file_formats_label.setText(self.lang['Library']['InfoBlockFileFormatsLabel'])
        self.info_block_size_label.setText(self.lang['Library']['InfoBlockSizeLabel'])

    def set_style(self):
        self.setStyleSheet(env_vars['styles'][self.app_style]['QMainWindow'])
        self.header_block_contents2.setStyleSheet(env_vars['styles'][self.app_style]['QMainWindow'])
        self.sorting_block_contents.setStyleSheet(env_vars['styles'][self.app_style]['QMainWindow'])
        # self.central_block_table = QTableWidget()
        self.central_block_table.horizontalHeader().setStyleSheet(env_vars['styles'][self.app_style]['QTableWidget'])
        self.central_block_table.setStyleSheet(env_vars['styles'][self.app_style]['QTableWidget'])
        self.central_block_table.horizontalHeader().setSortIndicatorShown(True)

        icon_names_list = ['book_add', 'book_new', 'book_del', 'settings']
        icon_dir = {}

        for name in icon_names_list:
            icon_dir[name] = QtGui.QIcon()
            icon_dir[name].addPixmap(
                QtGui.QPixmap(
                    env_vars['styles'][self.app_style]['icons'][name]
                        .replace('{APP_DIR}', self.app_directory)
                        .replace('/', os.sep)
                ),
                QtGui.QIcon.Normal, QtGui.QIcon.Off
            )

        self.header_block_btn_add_book.setIcon(icon_dir['book_add'])
        self.header_block_btn_create_book.setIcon(icon_dir['book_new'])
        self.header_block_btn_del_book.setIcon(icon_dir['book_del'])
        self.header_block_btn_settings.setIcon(icon_dir['settings'])

