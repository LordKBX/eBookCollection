# This Python file uses the following encoding: utf-8
import os, sys, shutil
import traceback
from PyQt5.QtWidgets import *
import PyQt5.uic
from PyQt5.uic import *

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import lang
import common.common, common.files, common.dialog, common.qt
from vars import *


class FilesNameWindow(QDialog):
    def __init__(self, parent):
        super(FilesNameWindow, self).__init__(parent)
        PyQt5.uic.loadUi(appDir + os.sep + 'editor/files_name.ui'.replace('/', os.sep), self)  # Load the .ui file
        lng = lang.Lang()
        self.lang = lng
        self.setWindowTitle(lng['Editor']['FilesWindow']['FileNameWindowTitle'])
        self.label.setText(lng['Editor']['FilesWindow']['FileNameWindowLabel'])
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText(lng['Editor']['FilesWindow']['btnOk'])
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText(lng['Editor']['FilesWindow']['btnCancel'])
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setStyleSheet(env_vars['styles']['black']['fullAltButton'])
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setStyleSheet(env_vars['styles']['black']['fullAltButton'])

    def openExec(self, text: str = None):
        if text is not None:
            self.lineEdit.setText(text)
        ret = self.exec_()
        if ret == 1:
            print('name = ', self.lineEdit.text())
            return self.lineEdit.text()
        else:
            return None


class FilesWindow(QDialog):
    def __init__(self, parent, folder: str):
        super(FilesWindow, self).__init__(parent)
        PyQt5.uic.loadUi(appDir + os.sep + 'editor/files.ui'.replace('/', os.sep), self)  # Load the .ui file
        lng = lang.Lang()
        self.lang = lng
        self.setWindowTitle(lng['Editor']['FilesWindow']['WindowTitle'])
        self.setStyleSheet(env_vars['styles']['black']['fullButton'])
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText(lng['Editor']['FilesWindow']['btnOk'])
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText(lng['Editor']['FilesWindow']['btnCancel'])
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setStyleSheet(env_vars['styles']['black']['fullAltButton'])
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setStyleSheet(env_vars['styles']['black']['fullAltButton'])
        self.fileTree.setStyleSheet(env_vars['styles']['black']['fullTreeView'])
        self.fileTree.headerItem().setText(0, lng['Editor']['FileTableHeader'])
        self.fileTree.itemClicked.connect(self.itemClick)
        self.fileTree.header().setSectionsClickable(True)
        self.fileTree.header().sectionClicked.connect(self.razSelection)
        self.btnImport.clicked.connect(self.importer)
        self.btnNewFile.clicked.connect(lambda: self.newFile(True))
        self.btnNewFolder.clicked.connect(self.newFolder)
        self.folder = folder
        self.selectedFolder = ''
        self.listDelete = list()
        self.listRename = list()
        self.listNew = list()

    def openExec(self, text: str = None, url: str = None):

        self.fileTree.clear()
        tree = common.files.listDirTree(self.folder)
        for index in tree:
            item = QtWidgets.QTreeWidgetItem(self.fileTree)
            item.setText(0, index)
            if isinstance(tree[index], dict):
                item.setData(0, 100, ':dir:')
                item.setData(0, 99, index)
                common.qt.setQTreeItemFolderIcon(item)

                item = self.recurFileTableInsert(item, tree[index], index)
            else:
                item.setData(0, 99, tree[index].replace(self.folder, ''))
                item.setData(0, 100, ':file:')
            self.fileTree.insertTopLevelItem(0, item)


        ret = self.exec_()
        if ret == 1:
            print('self.listNew = ', self.listNew)
            return None
        else:
            return None

    def recurFileTableInsert(self, baseItem: QtWidgets.QTreeWidgetItem, tree: dict, prevDir: str=''):
        for indexr in tree:
            itemr = QtWidgets.QTreeWidgetItem(baseItem)
            itemr.setText(0, indexr)
            if isinstance(tree[indexr], dict):
                itemr.setData(0, 100, ':dir:')
                itemr.setData(0, 99, prevDir + os.sep + indexr)
                common.qt.setQTreeItemFolderIcon(itemr)

                itemr = self.recurFileTableInsert(itemr, tree[indexr], prevDir + os.sep + indexr)
            else:
                itemr.setData(0, 100, ':file:')
                itemr.setData(0, 99, tree[indexr].replace(self.folder, ''))
            baseItem.addChild(itemr)
        return baseItem

    def razSelection(self):
        print('razSelection')
        self.selectedFolder = ''
        self.fileTree.clearSelection()

    def itemClick(self, item: QTreeWidgetItem):
        filePath = item.data(0, 99)
        fileType = item.data(0, 100)
        if fileType == ':dir:':
            item.setExpanded(True)
            self.selectedFolder = filePath
            print(filePath)

    def getItem(self, pitem: QtWidgets.QTableWidgetItem = None):
        items = self.fileTree.selectedItems()
        if pitem is not None:
            if pitem.parent() is not None: items = [pitem.parent()]
            else:
                return self.fileTree
        if len(items) >= 1:
            dt = items[0].data(0, 100)
            while dt == ':file:':
                if isinstance(items[0].parent(), QtWidgets.QTreeWidget):
                    items = [self.fileTree]
                    self.selectedFolder = ''
                    break
                else:
                    items = [items[0].parent()]
                    dt = items[0].data(0, 100)
                    self.selectedFolder = items[0].data(0, 99)
        if len(items) >= 1:
            item = items[0]
            if isinstance(item, QtWidgets.QTreeWidget) is False:
                while isinstance(item, QtWidgets.QTreeWidget) and item.data(0, 99) in self.listDelete:
                    item = self.getItem(item)
                    if isinstance(item, QtWidgets.QTreeWidget) is True:
                        break
            return item
        else: return self.fileTree

    def importer(self):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            files, _ = QFileDialog.getOpenFileNames(
                self,
                self.lang['Editor']['FilesWindow']['ImportWindowTitle'],
                "",
                "All Files (*.*)", options=options
            )
            item = self.getItem()

            for file in files:
                file = file.replace('/', os.sep)
                tb = file.split(os.sep)
                self.listNew.append({'innerPath': self.selectedFolder + os.sep + tb[len(tb)-1], 'type': 'import', 'original': file})

                if isinstance(item, QtWidgets.QTreeWidget): itemr = QtWidgets.QTreeWidgetItem(self.fileTree)
                else: itemr = QtWidgets.QTreeWidgetItem(item)
                common.qt.setQTreeItemFolderIcon(itemr)

                if isinstance(item, QtWidgets.QTreeWidget): self.fileTree.insertTopLevelItem(0, itemr)
                else: item.addChild(itemr)
        except Exception:
            traceback.print_exc()

    def newFile(self, isFile: bool = True):
        try:
            wn = FilesNameWindow(self)
            file = wn.openExec()

            item = self.getItem()

            if file is not None:

                if isinstance(item, QtWidgets.QTreeWidget): itemr = QtWidgets.QTreeWidgetItem(self.fileTree)
                else: itemr = QtWidgets.QTreeWidgetItem(item)

                itemr.setForeground(0, QtGui.QColor(env_vars['styles']['black']['partialTreeViewItemColorNew']))
                itemr.setText(0, file)
                if isFile is True:
                    itemr.setData(0, 100, ':file:')
                    self.listNew.append({'innerPath': self.selectedFolder + os.sep + file, 'type': 'newFile'})
                else:
                    itemr.setData(0, 100, ':dir:')
                    self.listNew.append({'innerPath': self.selectedFolder + os.sep + file, 'type': 'newFolder'})
                    common.qt.setQTreeItemFolderIcon(itemr)
                itemr.setData(0, 99, self.selectedFolder + os.sep + file)

                if isinstance(item, QtWidgets.QTreeWidget):
                    self.fileTree.insertTopLevelItem(0, itemr)
                else:
                    item.addChild(itemr)
        except Exception:
            traceback.print_exc()

    def newFolder(self):
        self.newFile(False)
