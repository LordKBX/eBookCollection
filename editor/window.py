import os
import sys
import time
if os.name == 'nt':
    import ctypes

import PyQt5.uic
from PyQt5.uic import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from editor.editing_pane import *
from editor.window import *
from bdd import *
from vars import *
from lang import *
from common.common import *
from common.dialog import *
from common.books import *
from common.files import *
from common.archive import *


class editorWindow(QtWidgets.QMainWindow):
    def __init__(self, parent: QtWidgets.QMainWindow, openedFile):
        super(editorWindow, self).__init__(parent)
        PyQt5.uic.loadUi(appDir + '/editor/editor.ui'.replace('/', os.sep), self)
        self.openedFile = openedFile
        self.tmpDir = appDir + os.sep + 'editor' + os.sep + 'tmp'
        self.lang = Lang()
        self.default_page = self.lang['Editor']['WebViewDefaultPageContent']

        self.setStyleSheet("""
            QMainWindow::separator { background: rgba(63, 63, 63); }
            QMainWindow::separator:hover { background: rgba(120, 120, 120); }
            QWidget{ background: rgba(63, 63, 63); color:white; }
            QDockWidget { border: 0; margin:0; padding:0; }
            QDockWidget::title { font: bold; text-align: left; background: #333333; padding-left: 5px; }
            """ + env_vars['styles']['black']['fullButton']
        )
        self.dockTop1.setStyleSheet(env_vars['styles']['black']['defaultButton'])

        # ui.tabWidget
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
            QTabBar::close-button {  border-image: none; image: url('""" + appDir.replace(os.sep, '/') + """/icons/white/close.png'); }
            QTabBar::close-button:hover {  border-image: none; image: url('""" + appDir.replace(os.sep, '/') + """/icons/black/close.png'); }
            """
        )
        self.tabWidget.setPreviewWebview(self.webView, self.default_page)
        self.tabWidget.tabCloseRequested.connect(self.onCloseTab)
        self.tabWidget.currentChanged.connect(self.onChangeTab)

        # Processing File Table
        self.treeFileTable.clear()
        self.treeFileTable.headerItem().setText(0, self.lang['Editor']['FileTableHeader'])
        self.treeFileTable.itemDoubleClicked.connect(self.fileTableItemDoubleClicked)
        self.treeFileTable.setIndentation(10)
        self.treeFileTable.setCursor(QtCore.Qt.PointingHandCursor)
        self.treeFileTable.setStyleSheet(env_vars['styles']['black']['fullTreeView'])

        # Processing Content Table
        self.treeContentTable.clear()
        self.treeContentTable.headerItem().setText(0, self.lang['Editor']['ContentTableHeader'])
        self.treeContentTable.currentItemChanged.connect(self.ContentTableCurrentItemChanged)
        self.treeContentTable.setIndentation(0)
        self.treeContentTable.setCursor(QtCore.Qt.PointingHandCursor)

        # Processing global buttons
        self.btnEbookCreateCheckpoint.setText('Create session checkpoint')
        self.btnEbookCreateCheckpoint.clicked.connect(self.createCheckpoint)
        self.webView.setHtml(self.lang['Editor']['WebViewDefaultPageContent'])

        filepath, ext = os.path.splitext(self.openedFile)
        mappdir = appDir.replace(os.sep, '/') + '/data/'
        self.setWindowTitle(
            self.lang['Editor']['WindowTitle'] + ' - ' + self.openedFile.replace(os.sep, '/')
            .replace(mappdir, '').replace('/', ' / ').replace(ext, '')
        )
        # EditorWindow.show()
        rmDir(self.tmpDir)
        if os.path.isdir(self.tmpDir) is not True:
            os.makedirs(self.tmpDir + os.sep + 'original')
            os.makedirs(self.tmpDir + os.sep + 'current')

        if ext in ['.epub', '.epub2', '.epub3']:
            ret = inflate(self.openedFile, self.tmpDir + os.sep + 'original')
            ret = inflate(self.openedFile, self.tmpDir + os.sep + 'current')

        elif ext in ['.cbz', '.cbr']:
            ret = inflate(self.openedFile, self.tmpDir + os.sep + 'original')
            ret = inflate(self.openedFile, self.tmpDir + os.sep + 'current')
        else:
            WarnDialog(self.lang['Editor']['DialogInfoBadFileWindowTitle'], self.lang['Editor']['DialogInfoBadFileWindowText'], self)
            exit(0)

        tmpcss = self.tmpDir + os.sep + "tmp.css"
        filePage = open(tmpcss, "w", encoding="utf8")
        filePage.write("body { background:#999999;color:#ffffff; }")
        filePage.close()
        self.webView.page().settings().setUserStyleSheetUrl(QtCore.QUrl.fromLocalFile(tmpcss))
        # self.webView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)
        self.webView.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

        self.fileTableLoad()

    def ContentTableCurrentItemChanged(self, current: QtWidgets.QTreeWidgetItem, previous: QtWidgets.QTreeWidgetItem):
        print(current.data(0, 99))
        data = current.data(0, 99)

    def fileTableItemDoubleClicked(self, current: QtWidgets.QTreeWidgetItem, previous: QtWidgets.QTreeWidgetItem):
        data = current.data(0, 99)
        text = current.text(0)
        if data != ':dir:':
            print(data)
            print(text)
            self.tabWidget.createPane(text, data)

    def fileTableLoad(self):
        liste = listDirTree(self.tmpDir + os.sep + 'current', None)
        print(liste)
        for index in liste:
            item = QtWidgets.QTreeWidgetItem(self.treeFileTable)
            item.setText(0, index)
            if isinstance(liste[index], dict):
                item.setData(0, 99, ':dir:')
                item = self.recurFileTableInsert(item, liste[index])
            else:
                item.setData(0, 99, liste[index])
            self.treeFileTable.insertTopLevelItem(0, item)

    def recurFileTableInsert(self, baseItem: QtWidgets.QTreeWidgetItem, tree: dict):
        for indexr in tree:
            itemr = QtWidgets.QTreeWidgetItem(baseItem)
            itemr.setText(0, indexr)
            if isinstance(tree[indexr], dict):
                itemr.setData(0, 99, ':dir:')
                itemr = self.recurFileTableInsert(itemr, tree[indexr])
            else:
                itemr.setData(0, 99, tree[indexr])
            baseItem.addChild(itemr)
        return baseItem

    def onCloseTab(self, indexTab: int):
        if self.tabWidget.count() == 0: return
        print('onCloseTab')
        if self.tabWidget.count() > indexTab >= 0:
            self.tabWidget.removeTab(indexTab)

    def onChangeTab(self, indexTab: int):
        self.tabWidget.drawPreview()

    def createCheckpoint(self, indexTab: int):
        try:
            print("createCheckpoint")
            shutil.copytree(self.tmpDir + os.sep + 'current', self.tmpDir + os.sep + unixtimeToString(time.time(), '%Y-%m-%d_%H-%M-%S'))
        except Exception:
            traceback.print_exc()