# This Python file uses the following encoding: utf-8
import os, sys
from PyQt5.QtWidgets import *
import PyQt5.uic
from PyQt5.uic import *

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from common import lang
import common.common, common.files, common.qt
from common.vars import *


class LinkWindow(QDialog):
    def __init__(self, parent, folder: str):
        super(LinkWindow, self).__init__(parent, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        PyQt5.uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'link.ui'.replace('/', os.sep), self)  # Load the .ui file
        BDD = parent.BDD
        lng = parent.lang
        self.style = BDD.get_param('style')
        self.setWindowTitle(lng['Editor']['LinkWindow']['WindowTitle'])
        self.labelUrl.setText(lng['Editor']['LinkWindow']['labelUrl'])
        self.labelText.setText(lng['Editor']['LinkWindow']['labelText'])
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText(lng['Editor']['LinkWindow']['btnOk'])
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText(lng['Editor']['LinkWindow']['btnCancel'])
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setStyleSheet(get_style_var(self.style, 'fullAltButton'))
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setStyleSheet(get_style_var(self.style, 'fullAltButton'))
        self.fileTree.setStyleSheet(get_style_var(self.style, 'fullTreeView'))
        self.fileTree.headerItem().setText(0, lng['Editor']['FileTableHeader'])
        self.fileTree.itemClicked.connect(self.itemClick)
        self.folder = folder

    def openExec(self, text: str = None, url: str = None):
        if url is not None: self.editUrl.setText(url)
        else: self.editUrl.setText('')

        if text is not None: self.editText.setText(text)
        else: self.editText.setText('')

        self.fileTree.clear()
        liste = common.files.list_directory_tree(self.folder, None)
        for index in liste:
            item = QtWidgets.QTreeWidgetItem(self.fileTree)
            item.setText(0, index)
            if isinstance(liste[index], dict):
                item.setData(0, 99, ':dir:')
                common.qt.setQTreeItemFolderIcon(item)

                item = self.recurFileTableInsert(item, liste[index])
            else:
                item.setData(0, 99, liste[index].replace(self.folder, ''))
            self.fileTree.insertTopLevelItem(0, item)

        ret = self.exec_()  # Show the GUI
        if ret == 1:
            return {'url': self.editUrl.text(), 'text': self.editText.text()}
        else:
            return None

    def recurFileTableInsert(self, baseItem: QtWidgets.QTreeWidgetItem, tree: dict):
        for indexr in tree:
            itemr = QtWidgets.QTreeWidgetItem(baseItem)
            itemr.setText(0, indexr)
            if isinstance(tree[indexr], dict):
                itemr.setData(0, 99, ':dir:')
                common.qt.setQTreeItemFolderIcon(itemr)

                itemr = self.recurFileTableInsert(itemr, tree[indexr])
            else:
                itemr.setData(0, 99, tree[indexr].replace(self.folder, ''))
            baseItem.addChild(itemr)
        return baseItem

    def itemClick(self, event):
        info = event.data(0, 99)
        if info != ':dir:':
            self.editUrl.setText(info.replace(os.sep, '/')[1:])
