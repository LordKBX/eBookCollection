import os
import sys
import time
from xml.dom import minidom
if os.name == 'nt':
    import ctypes

import PyQt5.uic
import PyQt5.uic
import PyQt5.QtWebKitWidgets

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from editor.editing_pane import *
from editor.window import *
from editor.checkpoint import *
from editor.files import *
from bdd import *
from vars import *
from lang import *
from common.common import *
from common.dialog import *
from common.books import *
from common.files import *
from common.archive import *
import common.qt


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
            """ + env_vars['styles']['black']['defaultAltButton']
        )
        self.btnEbookSave.setStyleSheet(env_vars['styles']['black']['defaultAltButton'])
        self.btnEbookLoadCheckpoint.setStyleSheet(env_vars['styles']['black']['defaultAltButton'])
        self.btnEbookCreateCheckpoint.setStyleSheet(env_vars['styles']['black']['defaultAltButton'])
        self.btnEbookAddFile.setStyleSheet(env_vars['styles']['black']['defaultAltButton'])
        self.btnEbookContentTable.setStyleSheet(env_vars['styles']['black']['defaultAltButton'])

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
        self.btnEbookLoadCheckpoint.setText('Load session checkpoint')
        self.btnEbookLoadCheckpoint.clicked.connect(self.loadCheckpoint)
        self.btnEbookSave.setText('Save Ebook')
        self.btnEbookSave.clicked.connect(self.saveEbook)
        self.btnEbookAddFile.setText('Files Managment')
        self.btnEbookAddFile.clicked.connect(self.loadFileManagment)

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
        self.loadContentTable()

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
        self.treeFileTable.clear()
        liste = listDirTree(self.tmpDir + os.sep + 'current', None)
        # print(liste)
        for index in liste:
            item = QtWidgets.QTreeWidgetItem(self.treeFileTable)
            item.setText(0, index)
            if isinstance(liste[index], dict):
                item.setData(0, 99, ':dir:')
                common.qt.setQTreeItemFolderIcon(item)

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
                common.qt.setQTreeItemFolderIcon(itemr)

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

    def createCheckpoint(self):
        try:
            print("createCheckpoint")
            stime = unixtimeToString(time.time(), template='%Y-%m-%d_%H-%M-%S', isUTC=False)
            shutil.copytree(self.tmpDir + os.sep + 'current', self.tmpDir + os.sep + stime)
            InfoDialog(self.lang['Editor']['DialogCreateCheckpointWindowTitle'], self.lang['Editor']['DialogCreateCheckpointWindowText'].format(stime), self)
        except Exception:
            traceback.print_exc()

    def loadCheckpoint(self):
        try:
            wl = CheckpointWindow(self, self.tmpDir)
            ret = wl.openExec()
            if ret is not None:
                if os.path.isdir(self.tmpDir + os.sep + ret) is True:
                    common.files.rmDir(self.tmpDir + os.sep + 'current')
                    common.files.copyDir(self.tmpDir + os.sep + ret, self.tmpDir + os.sep + 'current')
                    self.tabWidget.reloadContents()
        except Exception:
            traceback.print_exc()

    def saveEbook(self):
        try:
            ret = dialog.InfoDialogConfirm(
                self.lang['Editor']['DialogConfirmSaveWindowTitle'],
                self.lang['Editor']['DialogConfirmSaveWindowText'],
                self.lang['Generic']['DialogBtnYes'],
                self.lang['Generic']['DialogBtnNo'], self.parent()
            )
            if ret is True:
                os.remove(self.openedFile)
                deflate(self.tmpDir + os.sep + 'current' + os.sep + '*', self.openedFile)
        except Exception:
            traceback.print_exc()

    def loadFileManagment(self):
        try:
            wl = FilesWindow(self, self.tmpDir + os.sep + 'current')
            ret = wl.openExec()
            print(ret)
            if ret is not None:
                for file in ret['delete']:
                    if ret['delete'][file]['type'] == 'deleteFile':
                        os.remove(self.tmpDir + os.sep + 'current' + ret['delete'][file]['innerPath'])
                    elif ret['delete'][file]['type'] == 'deleteFolder':
                        rmDir(self.tmpDir + os.sep + 'current' + ret['delete'][file]['innerPath'])
                for file in ret['rename']:
                    if ret['rename'][file]['type'] == 'renameFile':
                        rename(self.tmpDir + os.sep + 'current' + ret['rename'][file]['original'], self.tmpDir + os.sep + 'current' + ret['rename'][file]['newPath'])
                    elif ret['rename'][file]['type'] == 'renameFolder':
                        rename(self.tmpDir + os.sep + 'current' + ret['rename'][file]['original'], self.tmpDir + os.sep + 'current' + ret['rename'][file]['newPath'])
                for file in ret['new']:
                    print(file)
                    if ret['new'][file]['type'] == 'newFile':
                        f = open(self.tmpDir + os.sep + 'current' + ret['new'][file]['innerPath'], 'w', encoding="utf8")
                        f.write(' ')
                        f.close()
                    elif ret['new'][file]['type'] == 'newFolder':
                        os.makedirs(self.tmpDir + os.sep + 'current' + ret['new'][file]['innerPath'])
                    elif ret['new'][file]['type'] == 'import':
                        copyFile(ret['new'][file]['original'], self.tmpDir + os.sep + 'current' + ret['new'][file]['innerPath'])

                self.fileTableLoad()
        except Exception:
            traceback.print_exc()

    def loadContentTable(self):
        ".ncx"
        li = listDir(self.tmpDir + os.sep + 'current', "ncx")
        if len(li) > 0:
            print(li[0])
            with open(li[0], 'r', encoding="utf8") as file:
                content = file.read()
                mydoc = minidom.parseString(content)
                items = mydoc.getElementsByTagName('navPoint')
                for item in items:
                    url = item.getElementsByTagName('content')[0].attributes['src'].value
                    text = item.getElementsByTagName('text')[0].firstChild.data
                    print(url, text)

                # print(items)