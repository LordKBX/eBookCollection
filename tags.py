# This Python file uses the following encoding: utf-8
import os, sys, traceback
from PyQt5.QtWidgets import *
import PyQt5.sip
import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.uic
from PyQt5.uic import *
import zipfile
import jsonschema
import threading

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import common.common
import common.files
import common.books
import common.dialog
import common.archive
from common.vars import *
import tags_ui


class TagsWindow(tags_ui.Ui_Dialog):
    verticalSpacer = None
    parent = None
    style = None
    tags = ""
    taglist = []
    mutex = None
    BDD = None
    lang = None

    def __init__(self, parent, origin_value: str = None):
        super(TagsWindow, self).__init__(parent, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self.mutex = threading.Lock()
        try:
            self.parent = parent
            self.setupUi(self)
            try: self.BDD = parent.parent.BDD
            except Exception: self.BDD = parent.BDD
            try: self.lang = parent.parent.lang
            except Exception: self.lang = parent.lang
            self.BDD.get_param('style')
            self.setStyleSheet(get_style_var(self.style, 'QDialog') + " " + get_style_var(self.style, 'QDialogTextSizeAlt'))
            cursor = QtGui.QCursor(QtCore.Qt.PointingHandCursor)

            self.table.clear()
            self.table.setRowCount(0)
            self.table.setStyleSheet(get_style_var(self.style, 'QTableWidget'))
            self.table.sortItems(0, QtCore.Qt.AscendingOrder)

            print("old tags", origin_value)
            old_tags = []
            if origin_value is not None: old_tags = origin_value.strip().lower().split(";")
            self.tags = ";".join(old_tags)
            self.taglist = tags = self.BDD.get_tags()
            for tag in old_tags:
                if tag not in tags: tags.append(tag)
            for tag in tags:
                selected = False
                if tag in old_tags: selected = True
                self.new_case(tag, selected)

            self.searchbox.textChanged.connect(self.search)
            self.searchbox.setStyleSheet(get_style_var(self.style, 'TagsSearchBox'))

            self.button_new.clicked.connect(lambda: self.new_case())
            self.button_new.setCursor(cursor)
            self.button_new.setStyleSheet(get_style_var(self.style, 'fullAltButton'))
            self.button_new.setText(self.lang.get('Generic/DialogBtnNew'))

            self.setStyleSheet(get_style_var(self.style, 'QDialog') + " " + get_style_var(self.style, 'QDialogTextSizeAlt'))
            self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setStyleSheet(get_style_var(self.style, 'fullAltButton'))
            self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setCursor(cursor)
            self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setStyleSheet(get_style_var(self.style, 'fullAltButton'))
            self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setCursor(cursor)
            self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setText(self.lang.get('Generic/DialogBtnSave'))
            self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText(self.lang.get('Generic/DialogBtnCancel'))

            self.table.cellChanged.connect(self.cellChangeEvent)
        except Exception:
            traceback.print_exc()

    def new_case(self, text: str = None, selected: bool = True) -> None:
        try:
            new_tag = False
            if text is None:
                new_tag = True
                text = common.dialog.InputDialog(
                    self.self.lang.get('Library/Tags/DialogNewTagTitle'),
                    self.self.lang.get('Library/Tags/DialogNewTagText'),
                    self.self.lang.get('Generic/DialogBtnOk'),
                    self.self.lang.get('Generic/DialogBtnSave'), self,
                    self.self.lang.get('Library/Tags/DialogNewTagPlaceholder')
                )
            if text is None or text.strip() == "":
                return
            text = text.strip().lower()
            self.table.setRowCount(self.table.rowCount()+1)
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            if selected is True: item.setCheckState(QtCore.Qt.Checked)
            else: item.setCheckState(QtCore.Qt.Unchecked)
            item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignVCenter)
            item.setText(text.title())
            item.setData(99, text)
            self.table.setItem(self.table.rowCount()-1, 0, item)
        except Exception:
            traceback.print_exc()
        if new_tag is True:
            self.taglist.append(text)
            self.selection_process()

    def cellChangeEvent(self, row: int, column: int) -> None:
        if self.manual_change is True:
            self.manual_change = False
            return
        item = self.table.item(row, column)
        data = item.data(99)
        tags = self.tags.split(";")
        if item.checkState() == QtCore.Qt.Checked:
            if data not in tags:
                tags.append(data)
                tags.sort()
        else:
            if data in tags:
                tags.remove(data)
        self.tags = ";".join(tags)
        self.search()

    def search(self) -> None:
        self.mutex.acquire(True, 0.2)
        try:
            text = self.searchbox.text().lower()
            current_tags = self.tags.split(";")
            for t in range(len(current_tags)):
                current_tags[t] = current_tags[t].lower()

            self.table.clear()
            self.table.setRowCount(1)
            if text is None or text.strip() == "":
                for index in range(len(self.taglist)):
                    selected = False
                    if self.taglist[index] in current_tags: selected = True
                    self.new_case(self.taglist[index], selected)
                return
            elif text.strip() == "*":
                for index in range(len(self.taglist)):
                    if self.taglist[index] in current_tags:
                        self.new_case(self.taglist[index], True)
                return

            tags = []
            for index in range(len(self.taglist)):
                if text in self.taglist[index]:
                    tags.append(self.taglist[index])

            for index in range(len(tags)):
                selected = False
                if tags[index] in current_tags: selected = True
                self.new_case(tags[index], selected)
        except Exception:
            traceback.print_exc()
        self.mutex.release()
