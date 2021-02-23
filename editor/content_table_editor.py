# This Python file uses the following encoding: utf-8
import os, sys, shutil, re
import traceback
from typing import Union
from PyQt5.QtWidgets import *
import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.uic
from PyQt5.uic import *
from xml.dom import minidom

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import lang
import common.common, common.files, common.dialog, common.qt
from vars import *


class IndexNameWindow(QDialog):
    def __init__(self, parent):
        super(IndexNameWindow, self).__init__(parent)
        PyQt5.uic.loadUi(appDir + os.sep + 'editor/files_name.ui'.replace('/', os.sep), self)  # Load the .ui file
        lng = lang.Lang()
        self.lang = lng
        self.setWindowTitle(lng['Editor']['FilesWindow']['FileNameWindowTitle'])
        self.label.setText(lng['Editor']['FilesWindow']['FileNameWindowLabel'])
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setText(lng['Editor']['FilesWindow']['btnOk'])
        self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText(lng['Editor']['FilesWindow']['btnCancel'])
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setStyleSheet(env_vars['styles']['black']['fullAltButton'])
        self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setStyleSheet(env_vars['styles']['black']['fullAltButton'])

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
        super(ContentTableWindow, self).__init__(parent)
        PyQt5.uic.loadUi(appDir + os.sep + 'editor/content_table_editor.ui'.replace('/', os.sep), self)  # Load the .ui file
        lng = lang.Lang()
        self.lang = lng
        self.setWindowTitle(lng['Editor']['FilesWindow']['WindowTitle'])
        self.setStyleSheet(env_vars['styles']['black']['fullButton'])
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setText(lng['Editor']['FilesWindow']['btnOk'])
        self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText(lng['Editor']['FilesWindow']['btnCancel'])
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setStyleSheet(env_vars['styles']['black']['fullAltButton'])
        self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setStyleSheet(env_vars['styles']['black']['fullAltButton'])

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

        self.files = common.files.listDirTree(self.folder, 'html|xhtml')
        # print(self.files)
        self.addindex_combobox.addItem("")
        for file in self.files['texte']:
            # print(self.files['texte'][file].replace(self.folder, ""))
            self.addindex_combobox.addItem(self.files['texte'][file].replace(self.folder, ""))

        li = common.files.listDir(self.folder, "ncx")
        if len(li) > 0:
            with open(li[0], 'r', encoding="utf8") as file:
                content = file.read()
                mydoc = minidom.parseString(content)
                points = mydoc.getElementsByTagName('navPoint')
                for point in points:
                    path = point.getElementsByTagName('content')[0].attributes['src'].value.replace('/', os.sep)
                    text = point.getElementsByTagName('text')[0].firstChild.data

                    item = QtWidgets.QListWidgetItem()
                    item.setText(text+" ("+path+")")
                    item.setData(97, text)
                    item.setData(98, path)
                    self.list_content.insertItem(self.list_content.count(), item)

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
