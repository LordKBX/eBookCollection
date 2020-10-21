import json
import traceback
from common.common import *

class HomeWindowCentralBlock:
    CentralBlockTableCasesUidList = []
    CentralBlockTableLock = False
    CentralBlockTableSortPreviousIndex = 0
    CentralBlockTableSortPreviousOrder = QtCore.Qt.AscendingOrder

    def CentralBlockTableDefineSlots(self):
        """
        Define Signal/Sloct connections for CentralBlockTable
        :return:
        """
        # self.CentralBlockTabletableView.setSortIcons(
        #     QtGui.QIcon(self.appDir + "/icons/white/sort_up.png"),
        #     QtGui.QIcon(self.appDir + "/icons/white/sort_down.png")
        # )

        self.CentralBlockTable.currentCellChanged.connect(self.CentralBlockTableNewSelection)
        self.CentralBlockTable.itemChanged.connect(self.CentralBlockTableItemChanged)
        self.CentralBlockTable.cellDoubleClicked.connect(self.CentralBlockTableCellDoubleClicked)
        self.CentralBlockTable.horizontalHeader().sortIndicatorChanged.connect(self.CentralBlockTableSortIndicatorChanged)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.CentralBlockTableGetCollumnWidth)
        self.timer.start(500)
        self.old_sizes = ''


    def CentralBlockTableGetCollumnWidth(self):
        """
        slot for timer checking columns size

        :return: void
        """
        try:
            sizes = list()
            i = 0
            max = len(self.CentralBlockTable.horizontalHeader())
            while i < max:
                sizes.append(self.CentralBlockTable.columnWidth(i))
                i += 1
            nsize = json.dumps(sizes)
            if self.old_sizes != nsize:
                self.old_sizes = nsize
                # print("--------------------------------")
                # print('home_central_table_header_WIDTH')
                # print('new size = {}'.format(nsize))
                self.env_vars['home_central_table_header_sizes'] = nsize
                # print('old size = {}'.format(self.BDD.getParam('home_central_table_header_sizes')))
                self.BDD.setParam('home_central_table_header_sizes', nsize)

        except Exception: {}

    def CentralBlockTableNewSelection(self, currentRow, currentColumn, previousRow, previousColumn):
        """
        Slot for new selection on the Central Block Table Widget

        :param currentRow:
        :param currentColumn:
        :param previousRow:
        :param previousColumn:
        :return: void
        """
        if self.CentralBlockTableLock is True: return
        # print("CentralBlockTableNewSelection")
        guid_book = self.CentralBlockTable.item(currentRow, currentColumn).data(99)
        if self.currentBook != guid_book:
            try: self.setInfoPanel(self.BDD.getBooks(guid_book)[0])
            except Exception: traceback.print_exc()

    def CentralBlockTableSortIndicatorChanged(self, index: int, order: QtCore.Qt.SortOrder):
        try:
            # test and exclude locked column for sorting
            if isinstance(self.CentralBlockTable.horizontalHeaderItem(index), QTableAltItem):
                if self.CentralBlockTable.horizontalHeaderItem(index).locked is True:
                    # timer = QtCore.QTimer()
                    # timer.singleShot(100, self.CentralBlockTableSortReset)
                    return
            self.CentralBlockTableSortPreviousIndex = index
            self.CentralBlockTableSortPreviousOrder = order

            i = 0
            max = len(self.CentralBlockTable.horizontalHeader())
            while i < max:
                item = None
                if isinstance(self.CentralBlockTable.horizontalHeaderItem(i), QTableAltItem):
                    item = QTableAltItem()
                    item.lock(self.CentralBlockTable.horizontalHeaderItem(i).locked)
                else:
                    item = QtWidgets.QTableWidgetItem()
                item.setText(self.CentralBlockTable.horizontalHeaderItem(i).text())
                self.CentralBlockTable.setHorizontalHeaderItem(i, item)
                i += 1
            icon = QtGui.QIcon()
            if order == QtCore.Qt.AscendingOrder:
                icon.addPixmap(QtGui.QPixmap(self.appDir + '/icons/white/sort_up.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            else:
                icon.addPixmap(QtGui.QPixmap(self.appDir + '/icons/white/sort_down.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.CentralBlockTable.horizontalHeaderItem(index).setIcon(icon)
        except Exception:
            traceback.print_exc()

    def CentralBlockTableSortReset(self):
        self.CentralBlockTable.sortByColumn(self.CentralBlockTableSortPreviousIndex, self.CentralBlockTableSortPreviousOrder)

    def CentralBlockTableCellDoubleClicked(self, currentRow, currentColumn):
        """
        Slot for new selection on the Central Block Table Widget

        :param currentRow:
        :param currentColumn:
        :return: void
        """
        # print("--------------------------------")
        # print("CentralBlockTableCellDoubleClicked")
        item = self.CentralBlockTable.item(currentRow, currentColumn)
        guid_book = item.data(99)
        # print("Book GUID : {}".format(guid_book))
        if self.currentBook != guid_book:
            self.currentBook = guid_book
        args = list()
        if self.BDD.getBooks(guid_book)[0]['files'][0]['format'] in ['CBZ', 'CBR', 'EPUB']:
            args.append('python')
            args.append(self.appDir + '/reader/main.py'.replace('/', os.sep))
            args.append(self.appDir + os.sep + self.BDD.getBooks(guid_book)[0]['files'][0]['link'].replace('/', os.sep))
        else:
            args.append(self.BDD.getBooks(guid_book)[0]['files'][0]['link'])
        print(args)
        try: retcode = subprocess.call(args, shell=True)
        except Exception:
            traceback.print_exc()

    def CentralBlockTableItemChanged(self, newItem):
        """
        Slot for new item content on the Central Block Table Widget

        :param newItem: the modified QTableWidgetItem
        :return: void
        """
        try:
            # print("--------------------------------")
            # print("Row = {}".format(newItem.row()))
            # print("Column = {}".format(newItem.column()))
            # print(newItem.text())
            guid_case = newItem.data(98)
            if guid_case not in self.CentralBlockTableCasesUidList:
                self.CentralBlockTableCasesUidList.append(guid_case)
                return
            guid_book = newItem.data(99)
            col_type = newItem.data(100)
            book = self.BDD.getBooks(guid_book)[0]
            book[col_type] = newItem.text()
            self.BDD.updateBook(guid_book, col_type, newItem.text())
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
            cleanDir('./data')
        except Exception:
            traceback.print_exc()

    def newBookTableItem(self, guid: str, type: str, value: str, editable: bool = True, alt: any = None, alt_type: str = None, locked: bool = False):
        """
        Create item for the Central Block Table Widget

        :param guid: guid book
        :param type: case item type
        :param value: case item value
        :param editable:
        :param alt:
        :param alt_type:
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
        self.CentralBlockTableCasesUidList.clear()
        try:
            self.CentralBlockTableLock = True
            self.CentralBlockTable.clearSelection()
            self.CentralBlockTable.clearContents()
        except Exception:
            traceback.print_exc()
        self.CentralBlockTableLock = False
        header_size_policy = self.env_vars['home_central_table_header_size_policy']
        if header_size_policy in ['ResizeToContents', 'ResizeToContentsAndInteractive']:
            self.CentralBlockTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        if header_size_policy == 'Stretch':
            self.CentralBlockTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
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
            self.CentralBlockTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        # self.CentralBlockTable.setCornerButtonEnabled(False)
        line = 0
        self.CentralBlockTable.setRowCount(len(books))
        for book in books:
            try:
                # Title
                self.CentralBlockTable.setItem(line, 0, self.newBookTableItem(book['guid'], 'title', book['title']))
                # authors
                self.CentralBlockTable.setItem(line, 1, self.newBookTableItem(book['guid'], 'authors', book['authors']))
                # serie
                self.CentralBlockTable.setItem(line, 2, self.newBookTableItem(book['guid'], 'serie', book['serie']))
                # tags
                self.CentralBlockTable.setItem(line, 3, self.newBookTableItem(book['guid'], 'tags', book['tags'], True, book['tags'], 'str', True))
                # imported
                self.CentralBlockTable.setItem(line, 4,
                    self.newBookTableItem(
                        book['guid'],
                        'imported',
                        unixtimeToString(
                            float(book['import_date']),
                            self.lang['Time']['template']['textual_date'],
                            self.lang['Time']['months_short']
                        ),
                        False,
                        float(book['import_date']), 'float'
                    )
                )
                # Modified
                self.CentralBlockTable.setItem(line, 5,
                    self.newBookTableItem(
                        book['guid'],
                        'modified',
                        unixtimeToString(
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
        self.setInfoPanel(None)
        self.CentralBlockTableSortReset()
        self.CentralBlockTable.setCurrentCell(0, 0)

        if header_size_policy == 'ResizeToContentsAndInteractive':
            timer = QtCore.QTimer()
            timer.singleShot(500, self.delayedTableHeaderInteractiveMode)

    def delayedTableHeaderInteractiveMode(self):
        self.CentralBlockTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)


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
