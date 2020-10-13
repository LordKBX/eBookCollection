import json
import subprocess
import traceback
from PyQt5 import QtCore, QtGui, QtWidgets

class HomeWindowCentralBlock:
    def CentralBlockTableDefineSlots(self):
        """
        Define Signal/Sloct connections for CentralBlockTable
        :return:
        """
        self.CentralBlockTable.currentCellChanged.connect(self.CentralBlockTableNewSelection)
        self.CentralBlockTable.itemChanged.connect(self.CentralBlockTableItemChanged)
        self.CentralBlockTable.cellDoubleClicked.connect(self.CentralBlockTableCellDoubleClicked)

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
            sizes = [
                self.CentralBlockTable.columnWidth(0),
                self.CentralBlockTable.columnWidth(1),
                self.CentralBlockTable.columnWidth(2),
                self.CentralBlockTable.columnWidth(3),
                self.CentralBlockTable.columnWidth(4)
            ]
            nsize = json.dumps(sizes)
            if self.old_sizes != nsize:
                self.old_sizes = nsize
                print("--------------------------------")
                print('home_central_table_header_WIDTH')
                print('new size = {}'.format(nsize))
                self.env_vars['home_central_table_header_sizes'] = nsize
                print('old size = {}'.format(self.BDD.getParam('home_central_table_header_sizes')))
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
        print("--------------------------------")
        print("new position : {}x{}".format(currentRow, currentColumn))
        print("old position : {}x{}".format(previousRow, previousColumn))
        guid_book = self.CentralBlockTable.item(currentRow, currentColumn).data(99)
        print("Book GUID : {}".format(guid_book))
        if self.currentBook != guid_book:
            self.currentBook = guid_book
            self.setInfoPanel(self.BDD.getBooks(guid_book)[0])

    def CentralBlockTableCellDoubleClicked(self, currentRow, currentColumn):
        """
        Slot for new selection on the Central Block Table Widget

        :param currentRow:
        :param currentColumn:
        :return: void
        """
        print("--------------------------------")
        print("CentralBlockTableCellDoubleClicked")
        self.CentralBlockTable.item(currentRow, currentColumn)
        item = self.CentralBlockTable.item(currentRow, currentColumn)
        guid_book = item.data(99)
        print("Book GUID : {}".format(guid_book))
        if self.currentBook != guid_book:
            self.currentBook = guid_book
        file = self.BDD.getBooks(guid_book)[0]['files'][0]['link']
        try:
            retcode = subprocess.call(file, shell=True)
            if retcode < 0:
                print("Child was terminated by signal {}".format(-retcode))
            else:
                print("Child returned {}".format(-retcode))
        except Exception:
            traceback.print_exc()



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
        guid_book = newItem.data(99)
        col_type = newItem.data(100)
        book = self.BDD.getBooks(guid_book)[0]
        book[col_type] = newItem.text()
        self.BDD.updateBook(guid_book, col_type, newItem.text())

        self.setInfoPanel(book)