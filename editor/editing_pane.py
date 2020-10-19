import os
import io
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWebKitWidgets
import PyQt5.uic
from PyQt5.uic import *
import filetype

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from common import *
from vars import *
from booksTools import *
from editor.syntaxHighlight import *


class uiClass(QtWidgets.QWidget):
    def __init__(self):
        {}


class FileType:
    def __init__(self, ext: str, mime: str):
        self.extension = ext
        self.mime = mime


class editorTabManager(QtWidgets.QTabWidget):
    def __init__(self, parent: any):
        QtWidgets.QTabWidget.__init__(self, parent)
        self.setWindowTitle("Tab Dialog")
        self.previewWebview = None
        self.default_page = None

    def setPreviewWebview(self, webview: QtWebKitWidgets.QWebView, default_page: str):
        self.previewWebview = webview
        self.default_page = default_page

    def drawPreview(self):
        if self.count() <= 0: return
        item = self.currentWidget()
        if item.property('fileType') in [] or item.property('fileExt') in ['xhtml', 'html']:
            try:
                txe = item.children().__getitem__(2)
                self.previewWebview.setHtml(txe.text())
            except Exception:
                traceback.print_exc()
        else:
            self.previewWebview.setHtml(self.default_page)

    def contentUpdate(self):
        self.drawPreview()

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def createPane(self, title: str, path: str):
        data = None
        kind = filetype.guess(path)
        if kind is None:
            fn, ext = os.path.splitext(path)
            kind = FileType(ext[1:], 'text/plain')
            print('Cannot guess file type!')
            try:
                with open(path, "r", encoding="utf8") as file:
                    data = file.read()
            except Exception:
                with open(path, "rb") as file:
                    data = file.read()
                kind = FileType('bin', 'binary')

        isText = True
        print('----------')
        print(kind.mime)
        if kind.mime in ['image/jpeg', 'image/png', 'image/gif', 'image/bmp']:
            isText = False
            data = create_thumbnail(path, False)
        if kind.mime == 'binary':
            isText = False
        if data is None:
            return


        tab = QtWidgets.QWidget()
        # tab.setObjectName("tab")
        tab.setProperty('fileName', path)
        tab.setProperty('fileType', kind.mime)
        tab.setProperty('fileExt', kind.extension)
        if isText is True:
            tab.setProperty('originalContent', data)
        verticalLayout = QtWidgets.QVBoxLayout(tab)
        verticalLayout.setContentsMargins(0, 0, 0, 0)

        if isText is True:
            block = uiClass()
            super(uiClass, block).__init__()
            PyQt5.uic.loadUi(appDir+'/editor/text_edit.ui'.replace('/', os.sep), block) # Load the .ui file
            block.setStyleSheet("""
            QPushButton{ background:transparent; }
            QPushButton:hover{ background-color:rgb(120, 120, 120); }
            QPushButton:pressed{ background-color:rgb(120, 120, 120); }
            QPushButton:checked{ background-color:rgb(150, 150, 150);}
            """)
            try:
                if tab.property('fileExt') not in ['xhtml', 'html', 'css']:
                    self.clearLayout(block.horizon1_1)
                    self.clearLayout(block.horizon2)
                    block.setMaximumHeight(block.height() - 40)
                    block.setMinimumHeight(block.height() - 40)
                    block.setFixedHeight(block.height() - 40)
                elif tab.property('fileExt') in ['css', 'xml', 'opf', 'ncx']:
                    self.clearLayout(block.horizon2)
                    block.setMaximumHeight(block.height() - 40)
                    block.setMinimumHeight(block.height() - 40)
                    block.setFixedHeight(block.height() - 40)
            except Exception:
                traceback.print_exc()



            verticalLayout.addWidget(block)

            try:
                textEdit = SimplePythonEditor(tab)
                textEdit.setPaper(QColor("#666666"))
                textEdit.setObjectName("textEdit")
                font = QFont()
                font.setFamily('Courier')
                font.setFixedPitch(True)
                font.setPointSize(10)
                textEdit.setFont(font)
                textEdit.setMarginsFont(font)
                fontmetrics = QFontMetrics(font)
                textEdit.setMarginWidth(0, fontmetrics.width("00000") + 1)
                textEdit.setMarginsBackgroundColor(QColor("#333333"))
                textEdit.setMarginsForegroundColor(QColor("#ffffff"))

                textEdit.elexer.setDefaultPaper(QColor("#A6A6A6"))
                textEdit.elexer.setDefaultColor(QColor("#ffffff"))
                textEdit.elexer.setPaper(QColor("#A6A6A6"))
                textEdit.setText(data)
                textEdit.textChanged.connect(lambda: self.contentUpdate())

                verticalLayout.addWidget(textEdit)
            except Exception:
                traceback.print_exc()
        else:
            block = QtWebKitWidgets.QWebView()
            page = 'file:///' + path.replace(os.sep, '/')
            block.setUrl(QtCore.QUrl(page))
            verticalLayout.addWidget(block)

        app_icon = QtGui.QIcon()
        app_icon.addFile(appDir + '/icons/app_icon16x16.png', QtCore.QSize(16, 16))
        app_icon.addFile(appDir + '/icons/app_icon24x24.png', QtCore.QSize(24, 24))
        app_icon.addFile(appDir + '/icons/app_icon32x32.png', QtCore.QSize(32, 32))
        app_icon.addFile(appDir + '/icons/app_icon48x48.png', QtCore.QSize(48, 48))
        app_icon.addFile(appDir + '/icons/app_icon256x256.png', QtCore.QSize(256, 256))

        self.addTab(tab, app_icon, title)
        self.setTabsClosable(True)
        self.setCurrentIndex(self.count() - 1)

        block.btnUndo.setToolTip('Undo')
        block.btnUndo.clicked.connect(lambda: textEdit.undo())
        block.btnRedo.setToolTip('Redo')
        block.btnRedo.clicked.connect(lambda: textEdit.redo())
        block.btnCut.setToolTip('Cut')
        block.btnCut.clicked.connect(lambda: textEdit.cut())
        block.btnCopy.setToolTip('Copy')
        block.btnCopy.clicked.connect(lambda: textEdit.copy())
        block.btnPaste.setToolTip('Paste')
        block.btnPaste.clicked.connect(lambda: textEdit.paste())
        block.btnFix.setToolTip('Fix Document')
        block.btnComment.setToolTip('Comment')
        block.btnPrettify.setToolTip('Prettify File')
        block.btnBold.setToolTip('Bold')
        block.btnItalic.setToolTip('Italic')
        block.btnUnderline.setToolTip('Underline')
        block.btnStrikethrough.setToolTip('Strikethrough')
        block.btnSub.setToolTip('Sub')
        block.btnSup.setToolTip('Sup')
        block.btnTextColor.setToolTip('Text Color')
        block.btnBackColor.setToolTip('Back Color')
        block.btnAlignLeft.setToolTip('Align Left')
        block.btnAlignCenter.setToolTip('Align Center')
        block.btnAlignRight.setToolTip('Align Right')
        block.btnAlignJustify.setToolTip('Align Justify')
        block.btnList.setToolTip('List')
        block.btnNumList.setToolTip('Numeric List')
        block.btnLink.setToolTip('Link')
        block.btnImg.setToolTip('Image')

    def fixText(self):
        item = self.currentWidget()
        if item.property('fileType') in [] or item.property('fileExt') in ['xhtml', 'html', 'xml', 'opf', 'ncx', 'css']:
            try:
                txt = item.children().__getitem__(2).text()
            except Exception:
                traceback.print_exc()