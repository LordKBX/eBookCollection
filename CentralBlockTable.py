import os, sys, traceback, json, subprocess
import concurrent.futures
import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtWidgets
from common.files import *
from common.common import *
from common.vars import *
import SortingBlockTree
import settings
import InfoPanel

executor = concurrent.futures.ThreadPoolExecutor(max_workers=50)
executor_dir = ''
executor_file = ''


def wait_on_editor():
    global executor_dir, executor_file
    args = list()
    exe = executor_dir + '/editor.exe'.replace('/', os.sep)
    if os.path.isfile(exe):
        args.append(executor_dir + '/editor.exe'.replace('/', os.sep))
        args.append(executor_file.replace('/', os.sep))
        args.append('debug')
    else:
        args.append('python')
        args.append(executor_dir + '/editor/editor.py'.replace('/', os.sep))
        args.append(executor_file.replace('/', os.sep))
        args.append('debug')

    try:
        return_code = subprocess.call(args, shell=True)
    except Exception:
        traceback.print_exc()


def wait_on_reader():
    global executor_dir, executor_file
    args = list()
    exe = executor_dir + '/reader.exe'.replace('/', os.sep)
    if os.path.isfile(exe):
        if os.name == 'nt':
            args.append('start')
        args.append(executor_dir + '/reader.exe'.replace('/', os.sep))
        args.append(executor_file.replace('/', os.sep))
        # args.append('debug')
    else:
        # if os.name == 'nt':
        #     args.append('start')
        args.append('python')
        args.append(executor_dir + '/reader/reader.py'.replace('/', os.sep))
        args.append(executor_file.replace('/', os.sep))
        args.append('debug')

    try:
        return_code = subprocess.call(args, shell=True)
    except Exception:
        traceback.print_exc()


def wait_on_open_ext():
    global executor_file
    try:
        os.system('"'+executor_file.replace('/', os.sep)+'"')
    except Exception:
        traceback.print_exc()


class HomeWindowCentralBlock(InfoPanel.HomeWindowInfoPanel):
    central_block_table_cases_uid_list = []
    central_block_table_lock = False
    central_block_table_sort_previous_index = 0
    central_block_table_sort_previous_order = QtCore.Qt.AscendingOrder
    header_policy = ''
    BDD = None
    vars = None
    app_directory = None
    central_block_table = None
    currentBook = ''

    def central_block_table_define_slots(self):
        """
        Define Signal/Sloct connections for CentralBlockTable
        :return:
        """
        self.central_block_table.currentCellChanged.connect(self.central_block_table_new_selection)
        self.central_block_table.setContextMenuPolicy(PyQt5.QtCore.Qt.CustomContextMenu)
        self.central_block_table.customContextMenuRequested.connect(self.central_block_table_context_menu)
        self.central_block_table.itemChanged.connect(self.central_block_table_item_changed)
        self.central_block_table.cellDoubleClicked.connect(self.central_block_table_cell_double_clicked)
        self.central_block_table.horizontalHeader().sortIndicatorChanged.connect(self.central_block_table_sort_indicator_changed)
        self.central_block_table.horizontalHeader().sectionResized.connect(self.central_block_table_get_column_width)

        sizes = []
        print('header_size_policy')
        try:
            self.header_policy = self.BDD.get_param('library/headers_size_policy')
            if self.header_policy is None or self.header_policy == '':
                self.header_policy = self.vars['library']['headers_size_policy']
            print(self.header_policy)
            if self.header_policy in ['ResizeToContents', 'ResizeToContentsAndInteractive']:
                self.central_block_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
            if self.header_policy == 'Stretch':
                self.central_block_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            if self.header_policy == 'UserDefined':
                self.central_block_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
                tx = self.BDD.get_param('library/headers_size')
                if tx is None or tx == '':
                    sizes = json.loads(self.vars['library']['headers_size'])
                else:
                    sizes = json.loads(tx)
                print(sizes)
                self.central_block_table.setColumnWidth(0, sizes[0])
                self.central_block_table.setColumnWidth(1, sizes[1])
                self.central_block_table.setColumnWidth(2, sizes[2])
                self.central_block_table.setColumnWidth(3, sizes[3])
                self.central_block_table.setColumnWidth(4, sizes[4])
        except Exception:
            traceback.print_exc()

    def central_block_table_get_column_width(self):
        """
        slot for timer checking columns size

        :return: void
        """
        try:
            sizes = list()
            i = 0
            my_max = len(self.central_block_table.horizontalHeader())
            while i < my_max:
                sizes.append(self.central_block_table.columnWidth(i))
                i += 1
            new_size = json.dumps(sizes)
            print(new_size)
            self.BDD.set_param('library/headers_size', new_size)
            self.BDD.set_param('library/headers_size_policy', self.header_policy)

        except Exception:
            ""

    def central_block_table_new_selection(self, current_row, current_column, previous_row, previous_column):
        """
        Slot for new selection on the Central Block Table Widget

        :param current_row:
        :param current_column:
        :param previous_row:
        :param previous_column:
        :return: void
        """
        if self.central_block_table_lock is True: return
        if current_row < 0 or current_column < 0: return
        if current_row >= self.central_block_table.rowCount() or current_column < 0: return
        # print("central_block_table_new_selection")
        guid_book = self.central_block_table.item(current_row, current_column).data(99)
        if self.currentBook != guid_book:
            try:
                self.set_info_panel(self.BDD.get_books(guid_book)[0])
                self.currentBook = guid_book
            except Exception:
                traceback.print_exc()

    def central_block_table_sort_indicator_changed(self, index: int, order: QtCore.Qt.SortOrder):
        try:
            # test and exclude locked column for sorting
            if isinstance(self.central_block_table.horizontalHeaderItem(index), QTableAltItem):
                if self.central_block_table.horizontalHeaderItem(index).locked is True:
                    # timer = QtCore.QTimer()
                    # timer.singleShot(100, self.central_block_table_sort_reset)
                    return
            self.central_block_table_sort_previous_index = index
            self.central_block_table_sort_previous_order = order

            i = 0
            my_max = len(self.central_block_table.horizontalHeader())
            while i < my_max:
                item = None
                if isinstance(self.central_block_table.horizontalHeaderItem(i), QTableAltItem):
                    item = QTableAltItem()
                    item.lock(self.central_block_table.horizontalHeaderItem(i).locked)
                else:
                    item = QtWidgets.QTableWidgetItem()
                item.setText(self.central_block_table.horizontalHeaderItem(i).text())
                self.central_block_table.setHorizontalHeaderItem(i, item)
                i += 1
            icon = QtGui.QIcon()
            if order == QtCore.Qt.AscendingOrder:
                icon.addPixmap(QtGui.QPixmap(self.app_directory + '/icons/white/sort_up.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            else:
                icon.addPixmap(QtGui.QPixmap(self.app_directory + '/icons/white/sort_down.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.central_block_table.horizontalHeaderItem(index).setIcon(icon)
        except Exception:
            traceback.print_exc()

    def central_block_table_sort_reset(self):
        self.central_block_table.sortByColumn(
            self.central_block_table_sort_previous_index,
            self.central_block_table_sort_previous_order
        )

    def central_block_table_cell_double_clicked(self, current_row, current_column):
        """
        Slot for new selection on the Central Block Table Widget

        :param current_row:
        :param current_column:
        :return: void
        """
        global executor_dir, executor_file
        # print("--------------------------------")
        # print("central_block_table_cell_double_clicked")
        item = self.central_block_table.item(current_row, current_column)
        guid_book = item.data(99)
        # print("Book GUID : {}".format(guid_book))
        if self.currentBook != guid_book:
            self.currentBook = guid_book
        files = self.BDD.get_books(guid_book)[0]['files']
        if files[0]['format'] in ['CBZ', 'CBR', 'EPUB']:
            executor_dir = self.app_directory
            executor_file = files[0]['link']
            executor.submit(wait_on_reader)
        else:
            executor_file = files[0]['link']
            executor.submit(wait_on_open_ext)

    def central_block_table_item_changed(self, new_item):
        """
        Slot for new item content on the Central Block Table Widget

        :param new_item: the modified QTableWidgetItem
        :return: void
        """
        try:
            # print("--------------------------------")
            # print("Row = {}".format(newItem.row()))
            # print("Column = {}".format(newItem.column()))
            # print(newItem.text())
            guid_case = new_item.data(98)
            if guid_case not in self.central_block_table_cases_uid_list:
                self.central_block_table_cases_uid_list.append(guid_case)
                return
            guid_book = new_item.data(99)
            col_type = new_item.data(100)
            book = self.BDD.get_books(guid_book)[0]
            book[col_type] = new_item.text()
            self.BDD.update_book(guid_book, col_type, new_item.text())
            if col_type in ['title', 'authors', 'series']:
                index = 0
                while index < len(book['files']):
                    old_path = book['files'][index]['link']
                    new_path = self.BDD.get_param('library/directory').replace('{APP_DIR}', app_directory)
                    if book['authors'] is not None:
                        if book['authors'].strip() != '':
                            new_path += '/' + clean_string_for_url(book['authors'])
                    if book['series'] is not None:
                        if book['series'].strip() != '':
                            new_path += '/' + clean_string_for_url(book['series'])
                    if os.path.isdir(new_path) is False:
                        os.makedirs(new_path)
                    new_path += '/' + book['title'] + '.' + book['files'][index]['format'].lower()
                    shutil.move(old_path, new_path)
                    book['files'][index]['link'] = new_path
                    self.BDD.update_book(guid_book, 'link', new_path, book['files'][index]['guid'])
                    index += 1

            self.sorting_block_tree_load_data()
            self.set_info_panel(book)

            # Cleanup all empty folder in data folder
            clean_dir('./data')
        except Exception:
            traceback.print_exc()

    def central_block_table_context_menu(self, point: PyQt5.QtCore.QPoint):
        global executor_dir, executor_file
        try:
            # self.central_block_table = QtWidgets.QTableWidget()
            selection = self.central_block_table.selectedRanges()[0]
            selection = [selection.topRow(), selection.bottomRow()]
            print(selection)
            current_row = self.central_block_table.currentRow()
            current_column = self.central_block_table.currentColumn()
            guid_book = self.central_block_table.item(current_row, current_column).data(99)
            book_infos = self.BDD.get_books(guid_book)[0]
            menu = PyQt5.QtWidgets.QMenu()
            action0 = PyQt5.QtWidgets.QAction(self.lang['Library/CentralBlockTableContextMenu/EditMetadata'], None)
            action0.triggered.connect(self.metadata_window_load)
            menu.addAction(action0)
            for file in book_infos['files']:
                if file['format'] == 'EPUB':
                    executor_dir = self.app_directory
                    executor_file = file['link']
                    action1 = PyQt5.QtWidgets.QAction(self.lang['Library/CentralBlockTableContextMenu/EditBook'], None)
                    action1.triggered.connect(lambda: executor.submit(wait_on_editor))
                    menu.addAction(action1)

                plugs = common.vars.get_plugins('library', 'contextMenu', 'central_block_table', file['format'])
                for plug in plugs:
                    lg = self.lang.test_lang()
                    tx = None
                    for label in plug['interface']['label']:
                        if label['lang'] == self.lang.default_language and tx is None:
                            tx = label['content']
                        if label['lang'] == lg:
                            tx = label['content']
                    action2 = PyQt5.QtWidgets.QAction(tx, None)
                    action2.setProperty('plugin', plug['name'])
                    action2.setProperty('book_id', guid_book)
                    tt = [plug['archetype']]
                    try:
                        tt = plug['archetype'].split(':')
                    except Exception:
                        pass
                    action2.setProperty('archetype', tt[0])
                    if tt[0] == 'conversion':
                        tt2 = ['.', 'conv']
                        try:
                            tt2 = tt[1].split('-')
                            action2.setProperty('end_format', tt2[1])
                        except Exception:
                            action2.setProperty('end_format', 'CONV')
                        pf = file['link'].replace('/', os.sep)
                        rp = pf.rindex('.')
                        action2.setProperty('args', {
                            'input': pf,
                            'output': os.path.dirname(os.path.realpath(pf)),
                            'output2': pf[:rp]
                        })
                    else:
                        action2.setProperty('args', {})
                    # plugin_exec(executor_dir, {'input': executor_file, 'output': executor_file2})
                    action2.triggered.connect(self.context_menu_plugin_exec)
                    menu.addAction(action2)
            menu.exec(PyQt5.QtGui.QCursor.pos())

        except Exception:
            traceback.print_exc()

    def context_menu_plugin_exec(self):
        try:
            plugin = self.sender().property('plugin')
            archetype = self.sender().property('archetype')
            args = self.sender().property('args')
            ret = common.vars.plugin_exec(plugin, args)
            print('archetype=', archetype)
            if archetype == 'conversion':
                book_id = self.sender().property('book_id')
                end_format = self.sender().property('end_format')
                file_size = get_file_size(ret)
                self.BDD.insert_book(book_id, file_format=end_format, size=file_size, link=ret)
                self.set_info_panel(self.BDD.get_books(book_id)[0])
        except Exception:
            traceback.print_exc()

    @staticmethod
    def new_book_table_item(guid: str, book_type: str, value: str, editable: bool = True, alt: any = None,
                            alt_type: str = None, locked: bool = False):
        """
        Create item for the Central Block Table Widget

        :param guid: guid book
        :param book_type: case item type
        :param value: case item value
        :param editable:
        :param alt:
        :param alt_type:
        :param locked:
        :return: QTableWidgetItem
        """
        item = QtWidgets.QTableWidgetItem()
        if alt is not None:
            item = QTableAltItem()
            item.setValue(alt)
            item.setType(alt_type)
            item.lock(locked)
        if editable is True:
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
        else:
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        item.setData(98, uid())
        item.setData(99, guid)
        item.setData(100, book_type)
        item.setText(value)
        item.setToolTip(value)
        return item

    def load_books(self, books: list) -> None:
        """
        load book list into the Central Block Table Widget

        :param books: list(dict)
        :return: void
        """
        self.central_block_table_cases_uid_list.clear()
        try:
            self.central_block_table_lock = True
            self.central_block_table.clearSelection()
            self.central_block_table.clearContents()
        except Exception:
            traceback.print_exc()
        self.central_block_table_lock = False
        # self.CentralBlockTable.setCornerButtonEnabled(False)
        line = 0
        self.central_block_table.setRowCount(len(books))
        for book in books:
            try:
                list_items = [
                    'title',
                    'authors',
                    'series',
                    'tags',
                    'import_date',
                    'last_update_date'
                ]
                list_items_locked = [
                    'import_date',
                    'last_update_date'
                ]
                # Title
                col = 0
                for case in list_items:
                    if case not in list_items_locked:
                        self.central_block_table.setItem(
                            line, col,
                            self.new_book_table_item(
                                guid=book['guid'],  book_type=case, value=book[case],
                                editable=True, alt=None, alt_type=None, locked=False
                            )
                        )
                    else:
                        self.central_block_table.setItem(
                            line, col,
                            self.new_book_table_item(
                                guid=book['guid'],  book_type=case,
                                value=unixtime_to_string(
                                    float(book[case]),
                                    self.lang['Time']['template']['textual_date'],
                                    self.lang['Time']['months_short']
                                ),
                                editable=False,
                                alt=float(book['last_update_date']),
                                alt_type='float',
                                locked=True
                            )
                        )
                    col += 1
            except Exception:
                traceback.print_exc()

            line += 1
        if line > 0:
            self.set_info_panel(books[0])
        else:
            self.set_info_panel(None)
        self.central_block_table_sort_reset()
        self.central_block_table.setCurrentCell(0, 0)

class QTableAltItem(QtWidgets.QTableWidgetItem):
    value = 0.0
    var_type = 'float'
    locked = False

    def setValue(self, value):
        self.value = value

    def setType(self, stype: str):
        self.var_type = stype

    def lock(self, locked: bool):
        self.locked = locked

    def __eq__(self, other: QtWidgets.QTableWidgetItem):
        if self.locked is True: return False
        if self.var_type == 'float':
            return self.value == other.value
        elif self.var_type == 'str':
            return self.value.lower() == other.value.lower()
        else:
            return False

    def __lt__(self, other: QtWidgets.QTableWidgetItem):
        if self.locked is True: return False
        if self.var_type == 'float':
            return self.value < other.value
        elif self.var_type == 'str':
            return self.value.lower() < other.value.lower()
        else:
            return False

    def __gt__(self, other: QtWidgets.QTableWidgetItem):
        if self.locked is True: return False
        if self.var_type == 'float':
            return self.value > other.value
        elif self.var_type == 'str':
            return self.value.lower() > other.value.lower()
        else:
            return False
