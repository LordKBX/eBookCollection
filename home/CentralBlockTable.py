import json
import traceback
from common.common import *
from common.files import *


class HomeWindowCentralBlock:
    central_block_table_cases_uid_list = []
    central_block_table_lock = False
    central_block_table_sort_previous_index = 0
    central_block_table_sort_previous_order = QtCore.Qt.AscendingOrder
    timer = None
    old_sizes = ''

    def central_block_table_define_slots(self):
        """
        Define Signal/Sloct connections for CentralBlockTable
        :return:
        """
        # self.CentralBlockTabletableView.setSortIcons(
        #     QtGui.QIcon(self.app_directory + "/icons/white/sort_up.png"),
        #     QtGui.QIcon(self.app_directory + "/icons/white/sort_down.png")
        # )

        self.central_block_table.currentCellChanged.connect(self.central_block_table_new_selection)
        self.central_block_table.itemChanged.connect(self.central_block_table_item_changed)
        self.central_block_table.cellDoubleClicked.connect(self.central_block_table_cell_double_clicked)
        self.central_block_table.horizontalHeader().sortIndicatorChanged.connect(self.central_block_table_sort_indicator_changed)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.central_block_table_get_column_width)
        self.timer.start(500)
        self.old_sizes = ''

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
            if self.old_sizes != new_size:
                self.old_sizes = new_size
                # print("--------------------------------")
                # print('home_central_table_header_WIDTH')
                # print('new size = {}'.format(new_size))
                self.env_vars['home_central_table_header_sizes'] = new_size
                # print('old size = {}'.format(self.BDD.getParam('home_central_table_header_sizes')))
                self.BDD.setParam('home_central_table_header_sizes', new_size)

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
        # print("central_block_table_new_selection")
        guid_book = self.central_block_table.item(current_row, current_column).data(99)
        if self.currentBook != guid_book:
            try:
                self.set_info_panel(self.BDD.getBooks(guid_book)[0])
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
        self.central_block_table.sortByColumn(self.central_block_table_sort_previous_index, self.central_block_table_sort_previous_order)

    def central_block_table_cell_double_clicked(self, current_row, current_column):
        """
        Slot for new selection on the Central Block Table Widget

        :param current_row:
        :param current_column:
        :return: void
        """
        # print("--------------------------------")
        # print("central_block_table_cell_double_clicked")
        item = self.central_block_table.item(current_row, current_column)
        guid_book = item.data(99)
        # print("Book GUID : {}".format(guid_book))
        if self.currentBook != guid_book:
            self.currentBook = guid_book
        args = list()
        if self.BDD.getBooks(guid_book)[0]['files'][0]['format'] in ['CBZ', 'CBR', 'EPUB']:
            args.append('python')
            args.append(self.app_directory + '/reader/main.py'.replace('/', os.sep))
            args.append(self.app_directory + os.sep + self.BDD.getBooks(guid_book)[0]['files'][0]['link'].replace('/', os.sep))
        else:
            args.append(self.BDD.getBooks(guid_book)[0]['files'][0]['link'])
        print(args)
        try:
            retcode = subprocess.call(args, shell=True)
        except Exception:
            traceback.print_exc()

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
            book = self.BDD.getBooks(guid_book)[0]
            book[col_type] = new_item.text()
            self.BDD.updateBook(guid_book, col_type, new_item.text())
            if col_type in ['title', 'authors', 'serie']:
                index = 0
                while index < len(book['files']):
                    old_path = book['files'][index]['link']
                    new_path = 'data'
                    if book['authors'] is not None:
                        if book['authors'].strip() != '':
                            new_path += '/' + book['authors']
                    if book['serie'] is not None:
                        if book['serie'].strip() != '':
                            new_path += '/' + book['serie']
                    if os.path.isdir(new_path) is False:
                        os.makedirs(new_path)
                    new_path += '/' + book['title'] + '.' + book['files'][index]['format'].lower()
                    shutil.move(old_path, new_path)
                    book['files'][index]['link'] = new_path
                    self.BDD.updateBook(guid_book, 'link', new_path, book['files'][index]['guid'])
                    index += 1

            self.setInfoPanel(book)

            # Cleanup all empty folder in data folder
            clean_dir('./data')
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

    def load_books(self, books: list):
        """
        load book list into the Central Block Table Widget

        :param books: list(dir)
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
        header_size_policy = self.env_vars['home_central_table_header_size_policy']
        if header_size_policy in ['ResizeToContents', 'ResizeToContentsAndInteractive']:
            self.central_block_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        if header_size_policy == 'Stretch':
            self.central_block_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        if header_size_policy == 'UserDefined':
            sizes = []
            try:
                sizes = json.loads(self.env_vars['home_central_table_header_sizes'])
                self.central_block_table.setColumnWidth(0, sizes[0])
                self.central_block_table.setColumnWidth(1, sizes[1])
                self.central_block_table.setColumnWidth(2, sizes[2])
                self.central_block_table.setColumnWidth(3, sizes[3])
                self.central_block_table.setColumnWidth(4, sizes[4])
            except Exception:
                traceback.print_exc()
            self.central_block_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        # self.CentralBlockTable.setCornerButtonEnabled(False)
        line = 0
        self.central_block_table.setRowCount(len(books))
        for book in books:
            try:
                # Title
                self.central_block_table.setItem(line, 0, self.new_book_table_item(book['guid'], 'title', book['title']))
                # authors
                self.central_block_table.setItem(line, 1, self.new_book_table_item(book['guid'], 'authors', book['authors']))
                # serie
                self.central_block_table.setItem(line, 2, self.new_book_table_item(book['guid'], 'serie', book['serie']))
                # tags
                self.central_block_table.setItem(line, 3, self.new_book_table_item(book['guid'], 'tags', book['tags'], True, book['tags'], 'str', True))
                # imported
                self.central_block_table.setItem(line, 4,
                                                 self.new_book_table_item(
                        book['guid'],
                        'imported',
                        unixtime_to_string(
                            float(book['import_date']),
                            self.lang['Time']['template']['textual_date'],
                            self.lang['Time']['months_short']
                        ),
                        False,
                        float(book['import_date']), 'float'
                    )
                                                 )
                # Modified
                self.central_block_table.setItem(line, 5,
                                                 self.new_book_table_item(
                        book['guid'],
                        'modified',
                        unixtime_to_string(
                            float(book['last_update_date']),
                            self.lang['Time']['template']['textual_date'],
                            self.lang['Time']['months_short']
                        ),
                        False,
                        float(book['last_update_date']), 'float'
                    )
                                                 )
            except Exception:
                traceback.print_exc()

            line += 1
        self.set_info_panel(None)
        self.central_block_table_sort_reset()
        self.central_block_table.setCurrentCell(0, 0)

        if header_size_policy == 'ResizeToContentsAndInteractive':
            timer = QtCore.QTimer()
            timer.singleShot(500, self.delayed_table_header_interactive_mode)

    def delayed_table_header_interactive_mode(self):
        self.central_block_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)


class QTableAltItem(QtWidgets.QTableWidgetItem):
    value = 0.0
    stype = 'float'
    locked = False

    def setValue(self, value):
        self.value = value

    def setType(self, stype: str):
        self.stype = stype

    def lock(self, locked: bool):
        self.locked = locked

    def __eq__(self, other: QtWidgets.QTableWidgetItem):
        if self.locked is True: return False
        if self.stype == 'float':
            return self.value == other.value
        elif self.stype == 'str':
            return self.value.lower() == other.value.lower()
        else:
            return False

    def __lt__(self, other: QtWidgets.QTableWidgetItem):
        if self.locked is True: return False
        if self.stype == 'float':
            return self.value < other.value
        elif self.stype == 'str':
            return self.value.lower() < other.value.lower()
        else:
            return False

    def __gt__(self, other: QtWidgets.QTableWidgetItem):
        if self.locked is True: return False
        if self.stype == 'float':
            return self.value > other.value
        elif self.stype == 'str':
            return self.value.lower() > other.value.lower()
        else:
            return False
