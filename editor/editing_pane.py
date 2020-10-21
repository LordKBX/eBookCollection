import os
import sys
from PyQt5 import QtWebKitWidgets
import PyQt5.uic
from PyQt5.uic import *
import filetype

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from editor.syntaxHighlight import *
from PyQt5.Qsci import *
import lang
from common.books import *
from common import dialog
import editor.xmlt
import editor.css
import editor.link
import editor.img


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
        self.lang = lang.Lang()

    def setPreviewWebview(self, webview: QtWebKitWidgets.QWebView, default_page: str):
        self.previewWebview = webview
        self.default_page = default_page

    def drawPreview(self):
        if self.count() <= 0: return
        item = self.currentWidget()
        fileDir = os.path.dirname(os.path.realpath(__file__)).replace('file:///', '').replace('/', os.sep)+os.sep+'tmp'
        print('fileDir = ' + fileDir)
        if item.property('fileType') in [] or item.property('fileExt') in ['xhtml', 'html']:
            try:
                txe = item.children().__getitem__(2).text()
                txe = txe\
                    .replace(' href="../', ' href="')\
                    .replace(' src="../', ' src="')\
                    .replace(' href="', ' href="file:///'+fileDir.replace(os.sep, '/')+'/')\
                    .replace(' src="', ' src="file:///'+fileDir.replace(os.sep, '/')+'/')
                self.previewWebview.setHtml(txe)
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
            try:
                file = open(path, "r", encoding="utf8")
                data = file.read()
                file.close()
            except Exception:
                file = open(path, "rb")
                data = file.read()
                file.close()
                kind = FileType('bin', 'binary')

        isText = True
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
                if tab.property('fileExt') not in ['xhtml', 'html', 'css', 'xml', 'opf', 'ncx']:
                    self.clearLayout(block.horizon1_1)
                    self.clearLayout(block.horizon2)
                    block.setMaximumHeight(block.height() - 40)
                    block.setMinimumHeight(block.height() - 40)
                    block.setFixedHeight(block.height() - 40)
                elif tab.property('fileExt') in ['css', 'xml', 'opf', 'ncx']:
                    if tab.property('fileExt') in ['css']:
                        block.btnDebug.setMinimumHeight(0)
                        block.btnDebug.setMaximumWidth(0)
                        block.btnDebug.setMinimumHeight(0)
                        block.btnDebug.setMaximumWidth(0)
                        block.btnDebug.setFixedHeight(0)
                        block.btnDebug.setFixedWidth(0)
                    self.clearLayout(block.horizon2)
                    block.setMaximumHeight(block.height() - 40)
                    block.setMinimumHeight(block.height() - 40)
                    block.setFixedHeight(block.height() - 40)
            except Exception:
                traceback.print_exc()

            verticalLayout.addWidget(block)

            try:
                textEdit = None
                if tab.property('fileExt') in ['xhtml', 'html']:
                    textEdit = SimplePythonEditor(QsciLexerHTML(), tab)
                elif tab.property('fileExt') in ['xml', 'opf', 'ncx']:
                    textEdit = SimplePythonEditor(QsciLexerXML(), tab)
                    textEdit.elexer.setColor(QtGui.QColor.fromRgb(255, 255, 255), QsciLexerXML.Default)
                    textEdit.elexer.setColor(QtGui.QColor('#000080'), QsciLexerXML.Tag)
                    textEdit.elexer.setColor(QtGui.QColor('#000080'), QsciLexerXML.UnknownTag)
                elif tab.property('fileExt') in ['css']:
                    textEdit = SimplePythonEditor(QsciLexerCSS(), tab)
                textEdit.elexer.setDefaultPaper(QColor("#A6A6A6"))
                textEdit.elexer.setDefaultColor(QColor("#ffffff"))
                textEdit.elexer.setPaper(QColor("#A6A6A6"))
                textEdit.setObjectName("textEdit")
                textEdit.setCaretLineBackgroundColor(QColor("#BBBBBB"))
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

        try:
            block.btnSave.setToolTip('Save File in session')
            block.btnSave.clicked.connect(self.saveFile)
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
            block.btnDebug.setToolTip('Debug Document')
            block.btnDebug.clicked.connect(self.debugText)
            block.btnComment.setToolTip('Comment')
            block.btnComment.clicked.connect(self.commentText)
            block.btnPrettify.setToolTip('Prettify File')
            block.btnPrettify.clicked.connect(self.prettifyText)

            block.btnBold.setToolTip('Bold')
            block.btnBold.clicked.connect(lambda: self.blockPasterText('<b>', '</b>'))
            block.btnItalic.setToolTip('Italic')
            block.btnItalic.clicked.connect(lambda: self.blockPasterText('<i>', '</i>'))
            block.btnUnderline.setToolTip('Underline')
            block.btnUnderline.clicked.connect(lambda: self.blockPasterText('<u>', '</u>'))
            block.btnStrikethrough.setToolTip('Strikethrough')
            block.btnStrikethrough.clicked.connect(lambda: self.blockPasterText('<s>', '</s>'))
            block.btnSub.setToolTip('Sub')
            block.btnSub.clicked.connect(lambda: self.blockPasterText('<sub>', '</sub>'))
            block.btnSup.setToolTip('Sup')
            block.btnSup.clicked.connect(lambda: self.blockPasterText('<sup>', '</sup>'))
            block.btnTextColor.setToolTip('Text Color')
            block.btnTextColor.clicked.connect(self.claimTextColor)
            block.btnBackColor.setToolTip('Back Color')
            block.btnBackColor.clicked.connect(self.claimBackColor)
            block.btnAlignLeft.setToolTip('Align Left')
            block.btnAlignLeft.clicked.connect(lambda: self.blockPasterText('<div style="text-align:left;">', '</div>'))
            block.btnAlignCenter.setToolTip('Align Center')
            block.btnAlignCenter.clicked.connect(lambda: self.blockPasterText('<div style="text-align:center;">', '</div>'))
            block.btnAlignRight.setToolTip('Align Right')
            block.btnAlignRight.clicked.connect(lambda: self.blockPasterText('<div style="text-align:right;">', '</div>'))
            block.btnAlignJustify.setToolTip('Align Justify')
            block.btnAlignJustify.clicked.connect(lambda: self.blockPasterText('<div style="text-align:justify;">', '</div>'))
            block.btnList.setToolTip('List')
            block.btnList.clicked.connect(lambda: self.blockList('ul'))
            block.btnNumList.setToolTip('Numeric List')
            block.btnNumList.clicked.connect(lambda: self.blockList('ol'))
            block.btnLink.setToolTip('Link')
            block.btnLink.clicked.connect(self.LinkPoser)
            block.btnImg.setToolTip('Image')
            block.btnImg.clicked.connect(self.imgPoser)
        except Exception:
            {}

    def saveFile(self, evt):
        try:
            item = self.currentWidget()
            newText = item.children().__getitem__(2).text()
            oldText = item.property('originalContent')
            fileName = item.property('fileName')
            if oldText != newText:
                ret = dialog.InfoDialogConfirm(
                    self.lang['Editor']['DialogConfirmSaveWindowTitle'],
                    self.lang['Editor']['DialogConfirmSaveWindowText'],
                    self.lang['Generic']['DialogBtnYes'],
                    self.lang['Generic']['DialogBtnNo'], self.parent()
                )
                if ret is True:
                    print('Save')
                    file = open(fileName, 'w', encoding="utf8")
                    file.write(newText)
                    file.close()
                    item.setProperty('originalContent', newText)
            else:
                print('NO DIF')
        except Exception:
            traceback.print_exc()

    def claimBackColor(self):
        color = self.claimColor()
        if color is not None:
            self.blockPasterText('<p style="background-color:{}">'.format(color.name()), '</p>')

    def claimTextColor(self):
        color = self.claimColor()
        if color is not None:
            self.blockPasterText('<span style="color:{}">'.format(color.name()), '</span>')

    def claimColor(self):
        try:
            color = QtWidgets.QColorDialog.getColor(QtGui.QColor.fromRgb(0,0,0), self)
            if color.isValid() is True:
                return color
        except Exception:
            traceback.print_exc()
        return None

    def debugText(self):
        try:
            item = self.currentWidget()
            txEdit = item.children().__getitem__(2)
            if item.property('fileExt') in ['xhtml', 'html', 'xml', 'opf', 'ncx']:
                ret = editor.xmlt.parse(txEdit.text())
                if ret is not None:
                    dialog.WarnDialog('', 'Error found at line {}, collumn {}'.format(ret[0], ret[1]), self.parent())
                    txEdit.setSelection(ret[0]-1, 0, ret[0]-1, ret[1])
                    # SimplePythonEditor.setFocus()
                    txEdit.setFocus()
            if item.property('fileExt') in ['css']:
                {}
        except Exception:
            traceback.print_exc()

    def commentText(self):
        try:
            item = self.currentWidget()
            txEdit = item.children().__getitem__(2)
            if item.property('fileExt') in ['xhtml', 'html', 'xml', 'opf', 'ncx', 'css']:
                selectedText = txEdit.selectedText()
                sel = txEdit.getSelection()
                if sel[0] == sel[2] and sel[1] == sel[3]:
                    pos = txEdit.getCursorPosition()
                    if item.property('fileExt') in ['xhtml', 'html', 'xml', 'opf', 'ncx']:
                        txEdit.insertAt("<!-- Comment -->", pos[0], pos[1])
                    elif item.property('fileExt') in ['css']:
                        txEdit.insertAt("/* Comment */", pos[0], pos[1])
                else:
                    if item.property('fileExt') in ['xhtml', 'html', 'xml', 'opf', 'ncx']:
                        if selectedText.startswith('<!-- ') and selectedText.endswith(' -->'):
                            txEdit.replaceSelectedText(selectedText[5:][:-4])
                            txEdit.setSelection(sel[0], sel[1], sel[2], sel[3] - 4)
                        else:
                            txEdit.replaceSelectedText('<!-- '+selectedText+' -->')
                            txEdit.setSelection(sel[0], sel[1], sel[2], sel[3] + 4)
                    if item.property('fileExt') in ['css']:
                        if selectedText.startswith('/* ') and selectedText.endswith(' */'):
                            txEdit.replaceSelectedText(selectedText[3:][:-3])
                            txEdit.setSelection(sel[0], sel[1], sel[2], sel[3]-3)
                        else:
                            txEdit.replaceSelectedText('/* '+selectedText+' */')
                            txEdit.setSelection(sel[0], sel[1], sel[2], sel[3]+3)
            else:
                return
        except Exception:
            traceback.print_exc()

    def blockPasterText(self, block_start: str, block_end: str):
        try:
            item = self.currentWidget()
            txEdit = item.children().__getitem__(2)
            selectedText = txEdit.selectedText()
            sel = txEdit.getSelection()
            if sel[0] == sel[2] and sel[1] == sel[3]:
                pos = txEdit.getCursorPosition()
                txEdit.insertAt(block_start + ' ' + block_end, pos[0], pos[1])
            else:
                max = len(block_start) + len(block_end)
                if selectedText.startswith(block_start) and selectedText.endswith(block_end):
                    txEdit.replaceSelectedText(selectedText[len(block_start):][:len(block_end)*-1])
                    txEdit.setSelection(sel[0], sel[1], sel[2], sel[3] - max)
                else:
                    txEdit.replaceSelectedText(block_start + selectedText + block_end)
                    txEdit.setSelection(sel[0], sel[1], sel[2], sel[3] + max)
        except Exception:
            traceback.print_exc()

    def blockList(self, list_type: str = 'ul'):  # list_type = ul or ol
        try:
            block_start = '<'+list_type+'>'
            block_end = '</'+list_type+'>'
            item = self.currentWidget()
            txEdit = item.children().__getitem__(2)
            selectedText = txEdit.selectedText().replace('\t', '').replace('\r', '')
            selectedText = re.sub('\n {2,}', '\n', selectedText)
            sel = txEdit.getSelection()
            if sel[0] == sel[2] and sel[1] == sel[3]:
                pos = txEdit.getCursorPosition()
                txEdit.insertAt(block_start + '\n<li>ligne</li>\n' + block_end, pos[0], pos[1])
            else:
                max = len(block_start) + len(block_end)
                newtx = ''
                if selectedText.startswith(block_start) and selectedText.endswith(block_end):
                    newtx = selectedText[len(block_start):][:len(block_end)*-1].replace('\n', '').replace('<li>', '\n').replace('</li>', '')
                else:
                    newtx = block_start
                    tb = selectedText.split('\n')
                    for line in tb:
                        newtx += '\n    <li>' + line + '</li>'
                    newtx += block_end
                txEdit.replaceSelectedText(newtx)
                tbx = newtx.split('\n')
                txEdit.setSelection(sel[0], sel[1], sel[0] + len(tbx) - 1, len(tbx[len(tbx) - 1]))
        except Exception:
            traceback.print_exc()

    def prettifyText(self):
        try:
            item = self.currentWidget()
            txEdit = item.children().__getitem__(2)
            sel = pos = txEdit.getSelection()
            if sel[0] == sel[2] and sel[1] == sel[3]:
                pos = txEdit.getCursorPosition()
            if item.property('fileExt') in ['xml', 'opf', 'ncx']:
                ret = editor.xmlt.prettify(txEdit.text())
                txEdit.selectAll(True)
                txEdit.replaceSelectedText(ret)
            elif item.property('fileExt') in ['css']:
                ret = editor.css.prettifyCss(txEdit.text())
                txEdit.selectAll(True)
                txEdit.replaceSelectedText(ret)
            else:
                return
            if sel[0] == sel[2] and sel[1] == sel[3]:
                txEdit.setCursorPosition(pos[0], pos[1])
            else:
                txEdit.setSelection(sel[0], sel[1], sel[2], sel[3])
        except Exception:
            traceback.print_exc()

    def LinkPoser(self):
        block_start = '<a '
        block_end = '</a>'
        try:
            item = self.currentWidget()
            window = editor.link.LinkWindow(self.parent(), appDir + os.sep + 'editor' + os.sep + 'tmp')
            txEdit = item.children().__getitem__(2)
            selectedText = txEdit.selectedText()
            sel = txEdit.getSelection()
            if sel[0] == sel[2] and sel[1] == sel[3]:
                ret = window.openExec()
                if ret is not None:
                    pos = txEdit.getCursorPosition()
                    newText = '<a href="' + ret['url'] + '">' + ret['text'] + '</a>'
                    txEdit.insertAt(newText, pos[0], pos[1])
                    tb = newText.split('\n')
                    txEdit.setSelection(pos[0], pos[1], pos[0] + len(tb) - 1, len(tb[len(tb) - 1]) - 1)
            else:
                max = len(block_start) + len(block_end)
                if selectedText.startswith(block_start) and selectedText.endswith(block_end):
                    newText = re.sub('<a(.*)>(.*)</a>', '%2', selectedText)
                    txEdit.replaceSelectedText(newText)
                    tb = newText.split('\n')
                    txEdit.setSelection(sel[0], sel[1], sel[0] + len(tb) - 1, len(tb[len(tb) - 1]) - 1)
                else:
                    ret = window.openExec(selectedText)
                    if ret is not None:
                        newText = '<a href="'+ret['url']+'">'+ret['text']+'</a>'
                        txEdit.replaceSelectedText(newText)
                        tb = newText.split('\n')
                        txEdit.setSelection(sel[0], sel[1], sel[0] + len(tb) - 1, len(tb[len(tb) - 1]) - 1)
        except Exception:
            traceback.print_exc()

    def imgPoser(self):
        try:
            item = self.currentWidget()
            window = editor.img.ImgWindow(self.parent(), appDir + os.sep + 'editor' + os.sep + 'tmp')
            txEdit = item.children().__getitem__(2)
            selectedText = txEdit.selectedText()
            sel = txEdit.getSelection()
            pos = txEdit.getCursorPosition()
            ret = window.openExec(selectedText, None)
            if ret is not None:
                newText = '<img src="' + ret['url'] + '" alt="' + ret['text'] + '" title="' + ret['text'] + '" />'
                txEdit.insertAt(newText, pos[0], pos[1])
                tb = newText.split('\n')
                txEdit.setSelection(pos[0], pos[1], pos[0] + len(tb) - 1, len(tb[len(tb) - 1]) - 1)
        except Exception:
            traceback.print_exc()
