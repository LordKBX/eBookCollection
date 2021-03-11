# This Python file uses the following encoding: utf-8
import os, sys
import traceback
from PyQt5.QtWidgets import *
import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.uic
from PyQt5.uic import *
from xml.dom import minidom

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from common import lang
import common.common, common.files, common.dialog, common.qt
from common.vars import *
from common.books import *


class IndexNameWindow(QDialog):
    def __init__(self, parent):
        super(IndexNameWindow, self).__init__(parent, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        PyQt5.uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'files_name.ui'.replace('/', os.sep), self)  # Load the .ui file
        lng = parent.lang
        self.setWindowTitle(lng['Editor']['ContentTableWindow']['NameWindowTitle'])
        self.label.setText(lng['Editor']['ContentTableWindow']['NameWindowLabel'])

        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setText(lng['Editor']['ContentTableWindow']['btnOk'])
        self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText(lng['Editor']['ContentTableWindow']['btnCancel'])

    def open_exec(self, text: str = None):
        if text is not None:
            self.line_edit.setText(text)
        ret = self.exec_()
        if ret == 1:
            print('name = ', self.line_edit.text())
            return self.line_edit.text()
        else:
            return None


class ContentTableWindow(QDialog):
    def __init__(self, parent, folder: str):
        super(ContentTableWindow, self).__init__(parent, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        PyQt5.uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'content_table_editor.ui'.replace('/', os.sep), self)  # Load the .ui file
        self.BDD = parent.BDD
        self.style = self.BDD.get_param('style')
        lng = lang.Lang()
        lng.set_lang(self.BDD.get_param('lang'))
        self.lang = lng
        self.setStyleSheet(env_vars['styles'][self.style]['QDialog'])

        self.setWindowTitle(lng['Editor']['ContentTableWindow']['WindowTitle'])
        self.list_label.setText(lng['Editor']['ContentTableWindow']['ListLabel'])
        self.addindex_label.setText(lng['Editor']['ContentTableWindow']['AddIndexLabel'])
        self.addindex_line_edit.setPlaceholderText(lng['Editor']['ContentTableWindow']['AddIndexPlaceholder'])
        self.modify_index_label.setText(lng['Editor']['ContentTableWindow']['ModifyIndexLabel'])
        self.btn_rename.setText(lng['Editor']['ContentTableWindow']['BtnRename'])
        self.btn_delete.setText(lng['Editor']['ContentTableWindow']['BtnDelete'])

        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setText(lng['Editor']['ContentTableWindow']['btnOk'])
        self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText(lng['Editor']['ContentTableWindow']['btnCancel'])
        
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setStyleSheet(env_vars['styles'][self.style]['fullAltButton'])
        self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setStyleSheet(env_vars['styles'][self.style]['fullAltButton'])

        # self.list_content = QtWidgets.QListWidget()

        self.addindex_btn.clicked.connect(self.new_index)
        self.btn_rename.clicked.connect(self.rename)
        self.btn_delete.clicked.connect(self.delete)
        self.folder = folder
        self.selected_folder = ''
        self.list_data = dict()
        self.files = []

    def open_exec(self, text: str = None, url: str = None):
        self.list_content.clear()
        self.addindex_combobox.clear()

        self.files = common.files.list_directory_tree(self.folder, 'html|xhtml')
        files = common.files.list_directory(self.folder, 'html|xhtml')
        self.addindex_combobox.addItem("")

        print(self.files)
        for file in files:
            self.addindex_combobox.addItem(file.replace(self.folder, ""))

        li = common.files.list_directory(self.folder, "opf")
        data = ''
        with open(li[0]) as myfile:
            data = myfile.read()
        toc_type, chapters = parse_content_table(
            data,
            li[0].replace(self.folder, '').replace(li[0][li[0].rindex(os.sep) + 1:], '').replace(os.sep, '/'),
            self.folder
        )
        for chapter in chapters:
            try:
                item = QtWidgets.QListWidgetItem()
                item.setText(chapter['name'] + " (" + chapter['src'] + ")")
                item.setData(97, chapter['name'])
                item.setData(98, chapter['src'])

                self.list_content.addItem(item)
            except Exception:
                traceback.print_exc()

        ret = self.exec_()

        content_table = []
        max = self.list_content.count()
        i = 0
        while i < max:
            child = self.list_content.item(i)
            content_table.append({'name': child.data(97), 'url': child.data(98).replace("\\", "/")})
            i += 1

        print(content_table)
        if ret == 1:
            return content_table
        else:
            return None

    def new_index(self):
        # self.addindex_line_edit = QLineEdit()
        # self.addindex_combobox = QComboBox()
        name = self.addindex_line_edit.text().strip()
        url = self.addindex_combobox.currentText().strip()

        if name == "" or name is None or url == "" or url is None:
            return

        item = QListWidgetItem()
        item.setData(97, name)
        item.setData(98, url)
        item.setText(name + " (" + url + ")")

        # self.list_content = QListWidget()
        self.list_content.insertItem(self.list_content.count(), item)
        self.addindex_combobox.setCurrentIndex(0)
        self.addindex_line_edit.setText("")

    def rename(self):
        try:
            if self.list_content.currentIndex().row() == -1:
                return
            # self.list_content = QListWidget()
            wn = IndexNameWindow(self)
            url = self.list_content.item(self.list_content.currentIndex().row()).data(98)
            tx = self.list_content.item(self.list_content.currentIndex().row()).data(97)
            name = wn.open_exec(tx)

            if name is not None:
                self.list_content.item(self.list_content.currentIndex().row()).setData(97, name)
                self.list_content.item(self.list_content.currentIndex().row()).setText(name + " (" + url + ")")
        except Exception:
            traceback.print_exc()

    def delete(self):
        try:
            if self.list_content.currentIndex().row() == -1:
                return
            # self.list_content = QListWidget()
            self.list_content.takeItem(self.list_content.currentIndex().row())
            # self.list_content.removeItemWidget(self.list_content.item(self.list_content.currentIndex().row()))

        except Exception:
            traceback.print_exc()
