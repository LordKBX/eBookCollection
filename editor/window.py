import os
import sys
if os.name == 'nt':
    import ctypes

import PyQt5.uic
from PyQt5.uic import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from editor.editing_pane import *
from editor.window import *
from bdd import *
from lang import *
from common.dialog import *
from common.books import *
from common.files import *
from common.archive import *


class editorWindow(QtWidgets.QMainWindow):
    def __init__(self, parent: QtWidgets.QMainWindow):
        super(editorWindow, self).__init__(parent)
        PyQt5.uic.loadUi(appDir + '/editor/editor.ui'.replace('/', os.sep), self)

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

    def onCloseTab(self, indexTab: int):
        if self.tabWidget.count() == 0: return
        print('onCloseTab')
        if self.tabWidget.count() > indexTab >= 0:
            self.tabWidget.removeTab(indexTab)

    def onChangeTab(self, indexTab: int):
        self.tabWidget.drawPreview()

