# This Python file uses the following encoding: utf-8
import os, sys
import traceback
from PyQt5.QtWidgets import *
import PyQt5.uic
from PyQt5.uic import *

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import lang
import common.common, common.files, common.books, common.qt
from vars import *


class ImgWindow(QDialog):
    def __init__(self, parent, folder: str):
        super(ImgWindow, self).__init__(parent, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        PyQt5.uic.loadUi(app_directory + os.sep + 'editor/img.ui'.replace('/', os.sep), self)  # Load the .ui file
        lng = lang.Lang()
        self.setWindowTitle(lng['Editor']['ImgWindow']['WindowTitle'])
        self.labelUrl.setText(lng['Editor']['ImgWindow']['labelUrl'])
        self.labelText.setText(lng['Editor']['ImgWindow']['labelText'])
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText(lng['Editor']['ImgWindow']['btnOk'])
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText(lng['Editor']['ImgWindow']['btnCancel'])
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setStyleSheet(env_vars['styles']['Dark']['fullAltButton'])
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setStyleSheet(env_vars['styles']['Dark']['fullAltButton'])
        self.fileTree.setStyleSheet(env_vars['styles']['Dark']['fullTreeView'])
        self.imgButton.setStyleSheet(env_vars['styles']['Dark']['displayButton'])
        self.fileTree.headerItem().setText(0, lng['Editor']['FileTableHeader'])
        self.fileTree.itemClicked.connect(self.itemClick)
        self.folder = folder

    def openExec(self, text: str = None, url: str = None):
        if url is not None: self.editUrl.setText(url)
        else: self.editUrl.setText('')

        if text is not None: self.editText.setText(text)
        else: self.editText.setText('')

        self.fileTree.clear()
        liste = common.files.listDirTree(self.folder, 'jpg|png|gif|bmp|svg|webp')
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
        try:
            info = event.data(0, 99)
            if info != ':dir:':
                self.editUrl.setText(info.replace(os.sep, '/')[1:])
                file = self.folder + info.replace('/', os.sep)
                print(file)
                icon = QtGui.QIcon()
                image = QtGui.QPixmap()
                image.load(file)
                icon.addPixmap(image, QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.imgButton.setIconSize(QtCore.QSize(220, 250))
                self.imgButton.setToolTip("<img src='{}'/>".format(file))
                self.imgButton.setIcon(icon)
        except Exception:
            traceback.print_exc()
