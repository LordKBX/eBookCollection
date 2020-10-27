# This Python file uses the following encoding: utf-8
import os, sys, shutil, re
import traceback
from typing import Union
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
        self.btnRename.clicked.connect(self.rename)
        self.btnDelete.clicked.connect(self.delete)
        self.folder = folder
        self.selectedFolder = ''
        self.listDelete = dict()
        self.listRename = dict()
        self.listNew = dict()
        self.lockList = [os.sep + 'mimetype', os.sep + 'META-INF', os.sep + 'META-INF' + os.sep + 'container.xml']

    def openExec(self, text: str = None, url: str = None):
        self.fileTree.clear()
        tree = common.files.listDirTree(self.folder)
        # for index in tree:
        #     item = QtWidgets.QTreeWidgetItem(self.fileTree)
        #     item.setText(0, index)
        #     if isinstance(tree[index], dict):
        #         item.setData(0, 100, ':dir:')
        #         item.setData(0, 99, index)
        #         common.qt.setQTreeItemFolderIcon(item)
        #
        #         item = self.recurFileTableInsert(item, tree[index], index)
        #     else:
        #         item.setData(0, 99, tree[index].replace(self.folder, ''))
        #         item.setData(0, 100, ':file:')
        #     self.fileTree.insertTopLevelItem(0, item)
        print(self.lockList)
        self.fileTree = self.recurFileTableInsert(self.fileTree, tree, '')

        ret = self.exec_()
        if ret == 1:
            return {
                'delete': self.listDelete,
                'rename': self.listRename,
                'new': self.listNew,
            }
        else:
            return None

    def recurFileTableInsert(self, baseitem: Union[QtWidgets.QTreeWidgetItem, QtWidgets.QTreeWidget], tree: dict,
                             previousdir: str = '') -> Union[QtWidgets.QTreeWidgetItem, QtWidgets.QTreeWidget]:
        for indexr in tree:
            itemr = QtWidgets.QTreeWidgetItem(baseitem)
            itemr.setText(0, indexr)
            if isinstance(tree[indexr], dict):
                itemr.setData(0, 100, ':dir:')
                itemr.setData(0, 99, previousdir + os.sep + indexr)
                common.qt.setQTreeItemFolderIcon(itemr)

                itemr = self.recurFileTableInsert(itemr, tree[indexr], previousdir + os.sep + indexr)
            else:
                itemr.setData(0, 100, ':file:')
                itemr.setData(0, 99, tree[indexr].replace(self.folder, ''))
            print(previousdir + os.sep + indexr)
            if previousdir + os.sep + indexr in self.lockList or re.search('\\.opf$', indexr) is not None:
                itemr.setData(0, 98, True)
                common.qt.setQTreeItemLockIcon(itemr)
            if isinstance(baseitem, QtWidgets.QTreeWidget):
                self.fileTree.insertTopLevelItem(0, itemr)
            else:
                baseitem.addChild(itemr)
        return baseitem

    def razSelection(self):
        print('razSelection')
        self.selectedFolder = ''
        self.fileTree.clearSelection()

    def itemClick(self, itm: QTreeWidgetItem):
        filePath = itm.data(0, 99)
        fileType = itm.data(0, 100)
        if fileType == ':dir:':
            itm.setExpanded(True)
            self.selectedFolder = filePath
            print(filePath)

    def getItem(self, itm = None):
        try:
            items = self.fileTree.selectedItems()
            if itm is not None: items = [itm]
            if items is None: return self.fileTree
            if len(items) == 0: return self.fileTree

            item = items[0]
            while item.data(0, 99) in self.listDelete:
                if item.parent() is not None:
                    item = item.parent()
                    self.selectedFolder = item.data(0, 99)
                else:
                    self.selectedFolder = ''
                    return self.fileTree

            while item.data(0, 100) == ':file:':
                if isinstance(item.parent(), QtWidgets.QTreeWidget) or item.parent() is None:
                    item = self.fileTree
                    self.selectedFolder = ''
                    break
                else:
                    item = item.parent()
                    self.selectedFolder = item.data(0, 99)

            return item
        except Exception:
            traceback.print_exc()
            return None

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

            prepath = self.selectedFolder
            if self.selectedFolder != '':
                prepath = os.sep + self.selectedFolder

            for file in files:
                file = file.replace('/', os.sep)
                tb = file.split(os.sep)
                self.listNew[prepath + os.sep + tb[len(tb)-1]] = {'innerPath': prepath + os.sep + tb[len(tb)-1], 'type': 'import', 'original': file}

                if isinstance(item, QtWidgets.QTreeWidget):
                    itemr = QtWidgets.QTreeWidgetItem(self.fileTree)
                else:
                    itemr = QtWidgets.QTreeWidgetItem(item)
                itemr.setText(0, tb[len(tb)-1])
                itemr.setForeground(0, QtGui.QColor(env_vars['styles']['black']['partialTreeViewItemColorNew']))

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
                prepath = self.selectedFolder
                if self.selectedFolder != '':
                    prepath = os.sep + self.selectedFolder

                itemr.setForeground(0, QtGui.QColor(env_vars['styles']['black']['partialTreeViewItemColorNew']))
                itemr.setText(0, file)
                if isFile is True:
                    itemr.setData(0, 100, ':file:')
                    self.listNew[prepath + os.sep + file] = {'innerPath': prepath + os.sep + file, 'type': 'newFile'}
                else:
                    itemr.setData(0, 100, ':dir:')
                    self.listNew[prepath + os.sep + file] = {'innerPath': prepath + os.sep + file, 'type': 'newFolder'}
                    common.qt.setQTreeItemFolderIcon(itemr)
                itemr.setData(0, 99, prepath + os.sep + file)

                if isinstance(item, QtWidgets.QTreeWidget):
                    self.fileTree.insertTopLevelItem(0, itemr)
                else:
                    item.addChild(itemr)
        except Exception:
            traceback.print_exc()

    def newFolder(self):
        self.newFile(False)

    def rename(self):
        try:
            items = self.fileTree.selectedItems()
            if items is None: return
            if len(items) == 0: return
            item = items[0]

            self.getItem()
            pre_file = item.text(0)
            wn = FilesNameWindow(self)
            file = wn.openExec(item.text(0))

            if file is not None:
                if isinstance(item, QtWidgets.QTreeWidget): return

                prepath = ''
                if self.selectedFolder != file and os.sep in self.selectedFolder:
                    prepath = self.selectedFolder[(self.selectedFolder.rindex(os.sep)):]
                path = (prepath + os.sep + file).replace(os.sep + os.sep, os.sep)[1:]
                if self.listNew.get(file) is not None:
                    self.listNew[path] = self.listNew[pre_file]
                    del self.listNew[pre_file]
                    self.listNew[path]['innerPath'] = path
                else:
                    if item.data(0, 100) == ':dir:':
                        prepath = ''
                        self.listRename[path] = {
                            'newPath': path, 'type': 'renameFolder',
                            'original': prepath + os.sep + pre_file}
                    else:
                        self.listRename[self.selectedFolder + os.sep + file] = {
                            'newPath': self.selectedFolder + os.sep + file, 'type': 'renameFile',
                            'original': prepath + os.sep + pre_file}
                item.setText(0, file)
                item.setForeground(0, QtGui.QColor(env_vars['styles']['black']['partialTreeViewItemColorMod']))
        except Exception:
            traceback.print_exc()

    def delete(self):
        try:
            items = self.fileTree.selectedItems()
            if items is None: return
            if len(items) == 0: return
            item = items[0]
            if item.data(0, 98) is True: return

            parent = self.getItem()
            file = item.data(0, 99)

            ret = common.dialog.WarnDialogConfirm('title', 'text', 'yes', 'no', self)
            if ret is None or ret is False: return

            if file is not None:
                if isinstance(item, QtWidgets.QTreeWidget): return
                ret1 = self.removeFromDict(self.listNew, file, parent)
                if ret1 is not True:
                    if self.listRename.get(file) is None:
                        prepath = ''
                        if self.selectedFolder != file and os.sep in self.selectedFolder:
                            prepath = self.selectedFolder[(self.selectedFolder.rindex(os.sep)):]
                        path = (prepath + os.sep + file).replace(os.sep + os.sep, os.sep)
                        if item.data(0, 100) == ':dir:':
                            self.listDelete[path] = {'innerPath': path, 'type': 'deleteFolder'}
                        else:
                            self.listDelete[path] = {'innerPath': file, 'type': 'deleteFile'}
                    else:
                        original = self.listRename[file]['original']
                        tbo = original.split(os.sep)

                        if item.data(0, 100) == ':dir:':
                            self.listDelete[original] = {'innerPath': original, 'type': 'deleteFolder'}
                        else:
                            self.listDelete[original] = {'innerPath': original, 'type': 'deleteFile'}
                        ret2 = self.removeFromDict(self.listRename, file, parent)
                        item.setText(tbo[len(tbo)-1])

                    item.setForeground(0, QtGui.QColor(env_vars['styles']['black']['partialTreeViewItemColorDel']))
        except Exception:
            traceback.print_exc()

    def removeFromDict(self, tree: dict, path: str, parentItem: any):
        if tree.get(path) is not None:
            del tree[path]
            if isinstance(parentItem, QTreeWidget) or parentItem is None:
                tree.removeItemWidget(path)
            else:
                parentItem.removeChild(path)
            ld = list()
            for fi in tree:
                if path in fi:
                    ld.append(fi)
            for id in ld:
                del tree[id]
            return True
        return False
