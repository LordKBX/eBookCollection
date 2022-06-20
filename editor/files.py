# This Python file uses the following encoding: utf-8
import os, sys
import traceback
from typing import Union
from PyQt5.QtWidgets import *
import PyQt5.uic
from PyQt5.uic import *

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from common import lang
import common.common, common.files, common.dialog, common.qt
from common.vars import *


class FilesNameWindow(QDialog):
    def __init__(self, parent):
        super(FilesNameWindow, self).__init__(parent, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        PyQt5.uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'files_name.ui'.replace('/', os.sep), self)  # Load the .ui file
        lng = parent.lng
        self.BDD = parent.BDD
        style = self.BDD.get_param('style')
        self.setStyleSheet(get_style_var(style, 'QDialog'))
        self.setWindowTitle(lng['Editor']['FilesWindow']['FileNameWindowTitle'])
        self.label.setText(lng['Editor']['FilesWindow']['FileNameWindowLabel'])
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setText(lng['Editor']['FilesWindow']['btnOk'])
        self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText(lng['Editor']['FilesWindow']['btnCancel'])
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setStyleSheet(get_style_var(style, 'defaultButton'))
        self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setStyleSheet(get_style_var(style, 'defaultButton'))
        cursor = QtGui.QCursor(QtCore.Qt.PointingHandCursor)
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setCursor(cursor)
        self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setCursor(cursor)

    def open_exec(self, text: str = None):
        if text is not None:
            self.line_edit.setText(text)
        ret = self.exec_()
        if ret == 1:
            print('name = ', self.line_edit.text())
            return self.line_edit.text()
        else:
            return None


class FilesWindow(QDialog):
    def __init__(self, parent, folder: str):
        super(FilesWindow, self).__init__(parent, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        PyQt5.uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'files.ui'.replace('/', os.sep), self)  # Load the .ui file
        self.BDD = parent.BDD
        self.style = self.BDD.get_param('style')
        lng = lang.Lang()
        lng.set_lang(self.BDD.get_param('lang'))
        self.lng = lng
        self.setWindowTitle(lng['Editor']['FilesWindow']['WindowTitle'])
        self.setStyleSheet(get_style_var(self.style, 'QDialog') + get_style_var(self.style, 'EditorFileDialogAdditional'))
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setText(lng['Editor']['FilesWindow']['btnOk'])
        self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText(lng['Editor']['FilesWindow']['btnCancel'])
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setStyleSheet(get_style_var(self.style, 'defaultButton'))
        self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setStyleSheet(get_style_var(self.style, 'defaultButton'))
        cursor = QtGui.QCursor(QtCore.Qt.PointingHandCursor)
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setCursor(cursor)
        self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setCursor(cursor)
        self.file_tree.setStyleSheet(get_style_var(self.style, 'fullTreeView'))
        self.file_tree.headerItem().setText(0, lng['Editor']['FileTableHeader'])
        self.file_tree.itemClicked.connect(self.item_click)
        self.file_tree.header().setSectionsClickable(True)
        self.file_tree.header().sectionClicked.connect(self.raz_selection)
        self.btn_import.clicked.connect(self.importer)
        self.btn_new_file.clicked.connect(lambda: self.new_file(True))
        self.btn_new_folder.clicked.connect(self.new_folder)
        self.btn_rename.clicked.connect(self.rename)
        self.btn_delete.clicked.connect(self.delete)
        self.folder = folder
        self.selected_folder = ''
        self.list_delete = dict()
        self.list_rename = dict()
        self.list_new = dict()
        self.lock_list = [os.sep + 'mimetype', os.sep + 'META-INF', os.sep + 'META-INF' + os.sep + 'container.xml']

    def open_exec(self, text: str = None, url: str = None):
        self.file_tree.clear()
        tree = common.files.list_directory_tree(self.folder)
        # for index in tree:
        #     item = QtWidgets.QTreeWidgetItem(self.fileTree)
        #     item.setText(0, index)
        #     if isinstance(tree[index], dict):
        #         item.setData(0, 100, ':dir:')
        #         item.setData(0, 99, index)
        #         common.qt.setQTreeItemFolderIcon(item, self.style)
        #
        #         item = self.recur_file_table_insert(item, tree[index], index)
        #     else:
        #         item.setData(0, 99, tree[index].replace(self.folder, ''))
        #         item.setData(0, 100, ':file:')
        #     self.fileTree.insertTopLevelItem(0, item)
        print(self.lock_list)
        self.file_tree = self.recur_file_table_insert(self.file_tree, tree, '')

        ret = self.exec_()
        if ret == 1:
            return {
                'delete': self.list_delete,
                'rename': self.list_rename,
                'new': self.list_new,
            }
        else:
            return None

    def recur_file_table_insert(self, base_item: Union[QtWidgets.QTreeWidgetItem, QtWidgets.QTreeWidget], tree: dict,
                                previous_dir: str = '') -> Union[QtWidgets.QTreeWidgetItem, QtWidgets.QTreeWidget]:
        for indexr in tree:
            itemr = QtWidgets.QTreeWidgetItem(base_item)
            itemr.setText(0, indexr)
            if isinstance(tree[indexr], dict):
                itemr.setData(0, 100, ':dir:')
                itemr.setData(0, 99, previous_dir + os.sep + indexr)
                common.qt.setQTreeItemFolderIcon(itemr, self.style)

                itemr = self.recur_file_table_insert(itemr, tree[indexr], previous_dir + os.sep + indexr)
            else:
                itemr.setData(0, 100, ':file:')
                itemr.setData(0, 99, tree[indexr].replace(self.folder, ''))
            print(previous_dir + os.sep + indexr)
            if previous_dir + os.sep + indexr in self.lock_list or re.search('\\.opf$', indexr) is not None:
                itemr.setData(0, 98, True)
                common.qt.setQTreeItemLockIcon(itemr, self.style)
            if isinstance(base_item, QtWidgets.QTreeWidget):
                self.file_tree.insertTopLevelItem(0, itemr)
            else:
                base_item.addChild(itemr)
        return base_item

    def raz_selection(self):
        print('raz_selection')
        self.selected_folder = ''
        self.file_tree.clearSelection()

    def item_click(self, itm: QTreeWidgetItem):
        file_path = itm.data(0, 99)
        file_type = itm.data(0, 100)
        if file_type == ':dir:':
            itm.setExpanded(True)
            self.selected_folder = file_path
            print(file_path)

    def get_item(self, itm=None) -> QTreeWidgetItem:
        try:
            items = self.file_tree.selectedItems()
            if itm is not None: items = [itm]
            if items is None: return self.file_tree
            if len(items) == 0: return self.file_tree

            item = items[0]
            while item.data(0, 99) in self.list_delete:
                if item.parent() is not None:
                    item = item.parent()
                    self.selected_folder = item.data(0, 99)
                else:
                    self.selected_folder = ''
                    return self.file_tree

            while item.data(0, 100) == ':file:':
                if isinstance(item.parent(), QtWidgets.QTreeWidget) or item.parent() is None:
                    item = self.file_tree
                    self.selected_folder = ''
                    break
                else:
                    item = item.parent()
                    self.selected_folder = item.data(0, 99)

            return item
        except Exception:
            traceback.print_exc()
            return None

    def importer(self):
        try:
            options = QFileDialog.Options()
            #options |= QFileDialog.DontUseNativeDialog
            files, _ = QFileDialog.getOpenFileNames(
                self,
                self.lng['Editor']['FilesWindow']['ImportWindowTitle'],
                "",
                "All Files (*.*)", options=options
            )
            item = self.get_item()

            prepath = self.selected_folder
            if self.selected_folder != '':
                prepath = os.sep + self.selected_folder

            for file in files:
                file = file.replace('/', os.sep)
                tb = file.split(os.sep)
                self.list_new[prepath + os.sep + tb[len(tb)-1]] = {'innerPath': prepath + os.sep + tb[len(tb)-1], 'type': 'import', 'original': file}

                if isinstance(item, QtWidgets.QTreeWidget):
                    itemr = QtWidgets.QTreeWidgetItem(self.file_tree)
                else:
                    itemr = QtWidgets.QTreeWidgetItem(item)
                itemr.setText(0, tb[len(tb)-1])
                itemr.setForeground(0, QtGui.QColor(get_style_var(self.style, 'partialTreeViewItemColorNew')))

                if isinstance(item, QtWidgets.QTreeWidget): self.file_tree.insertTopLevelItem(0, itemr)
                else: item.addChild(itemr)
        except Exception:
            traceback.print_exc()

    def new_file(self, is_file: bool = True):
        try:
            wn = FilesNameWindow(self)
            file = wn.open_exec()

            item = self.get_item()

            if file is not None:

                if isinstance(item, QtWidgets.QTreeWidget): itemr = QtWidgets.QTreeWidgetItem(self.file_tree)
                else: itemr = QtWidgets.QTreeWidgetItem(item)
                prepath = self.selected_folder
                if self.selected_folder != '':
                    prepath = os.sep + self.selected_folder

                itemr.setForeground(0, QtGui.QColor(get_style_var(self.style, 'partialTreeViewItemColorNew')))
                itemr.setText(0, file)
                if is_file is True:
                    itemr.setData(0, 100, ':file:')
                    self.list_new[prepath + os.sep + file] = {'innerPath': prepath + os.sep + file, 'type': 'new_file'}
                else:
                    itemr.setData(0, 100, ':dir:')
                    self.list_new[prepath + os.sep + file] = {'innerPath': prepath + os.sep + file, 'type': 'new_folder'}
                    common.qt.setQTreeItemFolderIcon(itemr, self.style)
                itemr.setData(0, 99, prepath + os.sep + file)

                if isinstance(item, QtWidgets.QTreeWidget):
                    self.file_tree.insertTopLevelItem(0, itemr)
                else:
                    item.addChild(itemr)
        except Exception:
            traceback.print_exc()

    def new_folder(self):
        self.new_file(False)

    def rename(self):
        try:
            items = self.file_tree.selectedItems()
            if items is None: return
            if len(items) == 0: return
            item = items[0]

            self.get_item()
            pre_file = item.text(0)
            wn = FilesNameWindow(self)
            file = wn.open_exec(item.text(0))

            if file is not None:
                if isinstance(item, QtWidgets.QTreeWidget): return

                prepath = ''
                if self.selected_folder != file and os.sep in self.selected_folder:
                    prepath = self.selected_folder[(self.selected_folder.rindex(os.sep)):]
                path = (prepath + os.sep + file).replace(os.sep + os.sep, os.sep)[1:]
                if self.list_new.get(file) is not None:
                    self.list_new[path] = self.list_new[pre_file]
                    del self.list_new[pre_file]
                    self.list_new[path]['innerPath'] = path
                else:
                    if item.data(0, 100) == ':dir:':
                        prepath = ''
                        self.list_rename[path] = {
                            'newPath': path, 'type': 'renameFolder',
                            'original': prepath + os.sep + pre_file}
                    else:
                        self.list_rename[self.selected_folder + os.sep + file] = {
                            'newPath': self.selected_folder + os.sep + file, 'type': 'renameFile',
                            'original': prepath + os.sep + pre_file}
                item.setText(0, file)
                item.setForeground(0, QtGui.QColor(get_style_var(self.style, 'partialTreeViewItemColorMod')))
        except Exception:
            traceback.print_exc()

    def delete(self):
        try:
            items = self.file_tree.selectedItems()
            if items is None: return
            if len(items) == 0: return
            item = items[0]
            if item.data(0, 98) is True: return

            parent = self.get_item()
            file = item.data(0, 99)

            ret = common.dialog.WarnDialogConfirm('title', 'text', 'yes', 'no', self)
            if ret is None or ret is False: return

            if file is not None:
                if isinstance(item, QtWidgets.QTreeWidget):
                    return
                ret1 = False
                try: ret1 = self.remove_from_dict(self.list_new, file, parent)
                except Exception: traceback.print_exc()
                if ret1 is not True:
                    if self.list_rename.get(file) is None:
                        prepath = ''
                        if self.selected_folder != file and os.sep in self.selected_folder:
                            prepath = self.selected_folder[(self.selected_folder.rindex(os.sep)):]
                        path = (prepath + os.sep + file).replace(os.sep + os.sep, os.sep)
                        if item.data(0, 100) == ':dir:':
                            self.list_delete[path] = {'innerPath': path, 'type': 'deleteFolder'}
                        else:
                            self.list_delete[path] = {'innerPath': file, 'type': 'deleteFile'}
                    else:
                        original = self.list_rename[file]['original']
                        tbo = original.split(os.sep)

                        if item.data(0, 100) == ':dir:':
                            self.list_delete[original] = {'innerPath': original, 'type': 'deleteFolder'}
                        else:
                            self.list_delete[original] = {'innerPath': original, 'type': 'deleteFile'}
                        ret2 = self.remove_from_dict(self.list_rename, file, parent)
                        item.setText(tbo[len(tbo)-1])

                    item.setForeground(0, QtGui.QColor(get_style_var(self.style, 'partialTreeViewItemColorDel')))
        except Exception:
            traceback.print_exc()

    def remove_from_dict(self, tree: dict, path: str, parent_item: QTreeWidget or QTreeWidgetItem):
        if tree.get(path) is not None:
            del tree[path]
            if isinstance(parent_item, QTreeWidget) or parent_item is None:
                for index in range(0, parent_item.topLevelItemCount()):
                    item = parent_item.topLevelItem(index)
                    if parent_item.topLevelItem(index).data(0, 99) == path:
                        parent_item.takeTopLevelItem(index)
                        break
            else:
                print("P2")
                parent_item.removeChild(path)
            ld = list()
            for fi in tree:
                if path in fi:
                    ld.append(fi)
            for id in ld:
                del tree[id]
            return True
        return False
