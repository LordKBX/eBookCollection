import os
import sys
import time
import xml.dom
from xml.dom import minidom
if os.name == 'nt':
    import ctypes

import PyQt5.uic
import PyQt5.QtWidgets
import PyQt5.QtWebKitWidgets

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from editor.editing_pane import *
from editor.window import *
from editor.checkpoint import *
from editor.files import *
from editor.content_table_editor import *
from bdd import *
from vars import *
from lang import *
from common.common import *
from common.dialog import *
from common.books import *
from common.files import *
from common.archive import *
import common.qt


class EditorWindow(QtWidgets.QMainWindow):
    def __init__(self, parent: QtWidgets.QMainWindow, opened_file):
        super(EditorWindow, self).__init__(parent)
        PyQt5.uic.loadUi(app_directory + '/editor/editor.ui'.replace('/', os.sep), self)
        self.opened_file = opened_file
        self.tmpDir = app_directory + os.sep + 'editor' + os.sep + 'tmp'
        self.lang = Lang()
        self.default_page = self.lang['Editor']['WebViewDefaultPageContent']

        self.setStyleSheet("""
            QMainWindow::separator { background: rgba(63, 63, 63); }
            QMainWindow::separator:hover { background: rgba(120, 120, 120); }
            QWidget{ background: rgba(63, 63, 63); color:white; }
            QDockWidget { border: 0; margin:0; padding:0; }
            QDockWidget::title { font: bold; text-align: left; background: #333333; padding-left: 5px; }
            """ + env_vars['styles']['black']['defaultAltButton'])
        self.btnEbookSave.setStyleSheet(env_vars['styles']['black']['defaultAltButton'])
        self.btnEbookLoadCheckpoint.setStyleSheet(env_vars['styles']['black']['defaultAltButton'])
        self.btnEbookCreateCheckpoint.setStyleSheet(env_vars['styles']['black']['defaultAltButton'])
        self.btnEbookAddFile.setStyleSheet(env_vars['styles']['black']['defaultAltButton'])
        self.btnEbookContentTable.setStyleSheet(env_vars['styles']['black']['defaultAltButton'])

        self.dockTop1.setStyleSheet(env_vars['styles']['black']['defaultButton'])

        # ui.tabWidget
        ad = app_directory.replace(os.sep, '/')
        self.tabWidget.clear()
        self.tabWidget.setStyleSheet(
            """
            QFrame {  background: rgb(50, 50, 50); }
            QTabWidget::pane { }
            QTabWidget::tab-bar { }
            QTabBar::tab {
                background: rgb(80, 80, 80) !important;
                color: white; padding: 5px;
                margin-right:2px; border-color:rgb(0,0,0); border-width:1px; border-style:solid;
            }
            QTabBar::tab:selected { background: rgb(0, 135, 202) !important; }
            QTabBar::close-button {  border-image: none; image: url('""" + ad + """/icons/white/close.png'); }
            QTabBar::close-button:hover {  border-image: none; image: url('""" + ad + """/icons/black/close.png'); }
            """
        )
        self.tabWidget.set_preview_webview(self.webView, self.default_page)
        self.tabWidget.tabCloseRequested.connect(self.on_close_tab)
        self.tabWidget.currentChanged.connect(self.on_change_tab)

        # Processing File Table
        self.treeFileTable.clear()
        self.treeFileTable.headerItem().setText(0, self.lang['Editor']['FileTableHeader'])
        self.treeFileTable.itemDoubleClicked.connect(self.file_table_item_double_clicked)
        self.treeFileTable.setIndentation(10)
        self.treeFileTable.setCursor(QtCore.Qt.PointingHandCursor)
        self.treeFileTable.setStyleSheet(env_vars['styles']['black']['fullTreeView'])

        # Processing Content Table
        self.treeContentTable.clear()
        self.treeContentTable.headerItem().setText(0, self.lang['Editor']['ContentTableHeader'])
        self.treeContentTable.currentItemChanged.connect(self.content_table_current_item_changed)
        self.treeContentTable.itemDoubleClicked.connect(self.file_table_item_double_clicked)
        self.treeContentTable.setIndentation(0)
        self.treeContentTable.setCursor(QtCore.Qt.PointingHandCursor)

        # Processing global buttons
        self.btnEbookCreateCheckpoint.setText('Create session checkpoint')
        self.btnEbookCreateCheckpoint.clicked.connect(self.create_check_point)
        self.btnEbookLoadCheckpoint.setText('Load session checkpoint')
        self.btnEbookLoadCheckpoint.clicked.connect(self.load_check_point)
        self.btnEbookSave.setText('Save Ebook')
        self.btnEbookSave.clicked.connect(self.save_ebook)
        self.btnEbookAddFile.setText('Files Managment')
        self.btnEbookAddFile.clicked.connect(self.load_file_managment)

        self.btnEbookContentTable.setText('Edit Content Table')
        self.btnEbookContentTable.clicked.connect(self.load_content_table_managment)

        self.webView.setHtml(self.lang['Editor']['WebViewDefaultPageContent'])

        filepath, ext = os.path.splitext(self.opened_file)
        mappdir = app_directory.replace(os.sep, '/') + '/data/'
        self.setWindowTitle(
            self.lang['Editor']['WindowTitle'] + ' - ' + self.opened_file.replace(os.sep, '/')
            .replace(mappdir, '').replace('/', ' / ').replace(ext, '')
        )
        # EditorWindow.show()
        rmDir(self.tmpDir)
        if os.path.isdir(self.tmpDir) is not True:
            os.makedirs(self.tmpDir + os.sep + 'original')
            os.makedirs(self.tmpDir + os.sep + 'current')

        if ext in ['.epub', '.epub2', '.epub3']:
            ret = inflate(self.opened_file, self.tmpDir + os.sep + 'original')
            ret = inflate(self.opened_file, self.tmpDir + os.sep + 'current')

        elif ext in ['.cbz', '.cbr']:
            ret = inflate(self.opened_file, self.tmpDir + os.sep + 'original')
            ret = inflate(self.opened_file, self.tmpDir + os.sep + 'current')
        else:
            WarnDialog(
                self.lang['Editor']['DialogInfoBadFileWindowTitle'],
                self.lang['Editor']['DialogInfoBadFileWindowText'], self)
            exit(0)

        tmpcss = self.tmpDir + os.sep + "tmp.css"
        file_page = open(tmpcss, "w", encoding="utf8")
        file_page.write("body { background:#999999;color:#ffffff; }")
        file_page.close()
        self.webView.page().settings().setUserStyleSheetUrl(QtCore.QUrl.fromLocalFile(tmpcss))
        # self.webView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)
        self.webView.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

        self.file_table_load()
        self.load_content_table()

    def content_table_current_item_changed(self, current: QTreeWidgetItem, previous: QTreeWidgetItem):
        print(current.data(0, 99))
        data = current.data(0, 99)

    def file_table_item_double_clicked(self, current: QTreeWidgetItem, previous: QTreeWidgetItem):
        try:
            data = current.data(0, 99)
            text = current.data(0, 98)
            print(text)
            if data != ':dir:':
                self.tabWidget.create_pane(text, data)
        except Exception:
            traceback.print_exc()

    def file_table_load(self):
        self.treeFileTable.clear()
        liste = listDirTree(self.tmpDir + os.sep + 'current', None)
        # print(liste)
        for index in liste:
            item = QtWidgets.QTreeWidgetItem(self.treeFileTable)
            item.setText(0, index)
            item.setData(0, 98, index)
            if isinstance(liste[index], dict):
                item.setData(0, 99, ':dir:')
                common.qt.setQTreeItemFolderIcon(item)
                item = self.recur_file_table_insert(item, liste[index])
            else:
                item.setData(0, 99, liste[index])
            self.treeFileTable.insertTopLevelItem(0, item)

    def recur_file_table_insert(self, base_item: QtWidgets.QTreeWidgetItem, tree: dict):
        for indexr in tree:
            itemr = QtWidgets.QTreeWidgetItem(base_item)
            itemr.setText(0, indexr)
            itemr.setData(0, 98, indexr)
            if isinstance(tree[indexr], dict):
                itemr.setData(0, 99, ':dir:')
                common.qt.setQTreeItemFolderIcon(itemr)

                itemr = self.recur_file_table_insert(itemr, tree[indexr])
            else:
                itemr.setData(0, 99, tree[indexr])
            base_item.addChild(itemr)
        return base_item

    def on_close_tab(self, index_tab: int):
        if self.tabWidget.count() == 0: 
            return
        print('on_close_tab')
        if self.tabWidget.count() > index_tab >= 0:
            self.tabWidget.removeTab(index_tab)

    def on_change_tab(self, index_tab: int):
        self.tabWidget.draw_preview()

    def create_check_point(self):
        try:
            print("create_check_point")
            stime = unixtime_to_string(time.time(), template='%Y-%m-%d_%H-%M-%S', is_utc=False)
            shutil.copytree(self.tmpDir + os.sep + 'current', self.tmpDir + os.sep + stime)
            InfoDialog(
                self.lang['Editor']['DialogCreateCheckpointWindowTitle'], 
                self.lang['Editor']['DialogCreateCheckpointWindowText'].format(stime), 
                self
            )
        except Exception:
            traceback.print_exc()

    def load_check_point(self):
        try:
            wl = CheckpointWindow(self, self.tmpDir)
            ret = wl.openExec()
            if ret is not None:
                if os.path.isdir(self.tmpDir + os.sep + ret) is True:
                    common.files.rmDir(self.tmpDir + os.sep + 'current')
                    common.files.copyDir(self.tmpDir + os.sep + ret, self.tmpDir + os.sep + 'current')
                    self.tabWidget.reload_contents()
        except Exception:
            traceback.print_exc()

    def save_ebook(self):
        try:
            ret = dialog.InfoDialogConfirm(
                self.lang['Editor']['DialogConfirmSaveWindowTitle'],
                self.lang['Editor']['DialogConfirmSaveWindowText'],
                self.lang['Generic']['DialogBtnYes'],
                self.lang['Generic']['DialogBtnNo'], self.parent()
            )
            if ret is True:
                os.remove(self.opened_file)
                deflate(self.tmpDir + os.sep + 'current' + os.sep + '*', self.opened_file)
        except Exception:
            traceback.print_exc()

    def load_file_managment(self):
        try:
            wl = FilesWindow(self, self.tmpDir + os.sep + 'current')
            ret = wl.open_exec()
            # print(ret)
            if ret is not None:
                for file in ret['delete']:
                    if ret['delete'][file]['type'] == 'deleteFile':
                        os.remove(self.tmpDir + os.sep + 'current' + ret['delete'][file]['innerPath'])
                    elif ret['delete'][file]['type'] == 'deleteFolder':
                        rmDir(self.tmpDir + os.sep + 'current' + ret['delete'][file]['innerPath'])
                for file in ret['rename']:
                    if ret['rename'][file]['type'] == 'renameFile':
                        rename(
                            self.tmpDir + os.sep + 'current' + ret['rename'][file]['original'],
                            self.tmpDir + os.sep + 'current' + ret['rename'][file]['newPath']
                        )
                    elif ret['rename'][file]['type'] == 'renameFolder':
                        rename(
                            self.tmpDir + os.sep + 'current' + ret['rename'][file]['original'],
                            self.tmpDir + os.sep + 'current' + ret['rename'][file]['newPath']
                        )
                for file in ret['new']:
                    # print(file)
                    if ret['new'][file]['type'] == 'new_file':
                        f = open(self.tmpDir + os.sep + 'current' + ret['new'][file]['innerPath'], 'w', encoding="utf8")
                        f.write(' ')
                        f.close()
                    elif ret['new'][file]['type'] == 'new_folder':
                        os.makedirs(self.tmpDir + os.sep + 'current' + ret['new'][file]['innerPath'])
                    elif ret['new'][file]['type'] == 'import':
                        copyFile(
                            ret['new'][file]['original'],
                            self.tmpDir + os.sep + 'current' + ret['new'][file]['innerPath']
                        )

                self.file_table_load()
        except Exception:
            traceback.print_exc()

    def load_content_table_managment(self):
        try:
            wl = ContentTableWindow(self, self.tmpDir + os.sep + 'current')
            ret = wl.open_exec()

            if ret is not None:
                li = common.files.listDir(self.tmpDir + os.sep + 'current', "ncx")
                if len(li) > 0:
                    file = open(li[0], "r", encoding="utf8")
                    content = file.read()
                    file.close()
                    mydoc = minidom.parseString(content.replace("  ", "").replace("\t", ""))
                    map = mydoc.getElementsByTagName('navMap')[0]
                    points = mydoc.getElementsByTagName('navPoint')
                    for i in range(0, len(points)):
                        map.removeChild(points[i])

                    i = 0
                    for obj in ret:
                        i += 1
                        point = mydoc.createElement('navPoint')
                        point.setAttribute('id', 'num_{}'.format(i))
                        point.setAttribute('playOrder', "{}".format(i))
                        label = mydoc.createElement('navLabel')
                        tx = mydoc.createElement('text')
                        text_node = minidom.Text()
                        text_node.data = obj['name']
                        tx.appendChild(text_node)
                        label.appendChild(tx)
                        point.appendChild(label)
                        content = mydoc.createElement('content')
                        content.setAttribute('src', obj['url'])
                        point.appendChild(content)
                        map.appendChild(point)

                    mydoc.toprettyxml()
                    file = open(li[0], "wt", encoding="utf8")
                    file.write(mydoc.toprettyxml().replace("\r", "").replace("\n", "").replace(">\t", ">\n\t"))
                    file.close()

                self.load_content_table()
        except Exception:
            traceback.print_exc()

    def load_content_table(self):
        # ".ncx"
        li = listDir(self.tmpDir + os.sep + 'current', "ncx")
        if len(li) > 0:
            with open(li[0], 'r', encoding="utf8") as file:
                self.treeContentTable.clear()
                content = file.read()
                mydoc = minidom.parseString(content)
                points = mydoc.getElementsByTagName('navPoint')
                for point in points:
                    path = self.tmpDir + os.sep + 'current' + os.sep + \
                           point.getElementsByTagName('content')[0].attributes['src'].value.replace('/', os.sep)
                    text = point.getElementsByTagName('text')[0].firstChild.data
                    # print(path, text)
                    tb = path.split(os.sep)

                    item = QtWidgets.QTreeWidgetItem(self.treeContentTable)
                    item.setText(0, text)
                    item.setData(0, 98, tb[len(tb)-1])
                    item.setData(0, 99, path)
                    common.qt.setQTreeItemIcon(item, common.qt.QtQIconEnum.file)
                    self.treeContentTable.insertTopLevelItem(0, item)
                # print(items)
