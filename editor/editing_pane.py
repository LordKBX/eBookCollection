import os
import sys
import PyQt5.QtWebKitWidgets
import PyQt5.uic
from PyQt5.uic import *
import filetype

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from editor.syntaxHighlight import *
from common.books import *
from common import dialog, lang
import editor.xmlt
import editor.css
import editor.link
import editor.img


class UIClass(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


class FileType:
    def __init__(self, ext: str, mime: str):
        self.extension = ext
        self.mime = mime


class EditorTabManager(QtWidgets.QTabWidget):
    def __init__(self, parent: any):
        QtWidgets.QTabWidget.__init__(self, parent)
        self.setWindowTitle("Tab Dialog")
        self.previewWebview = None
        self.default_page = None
        self.previous_file = ''
        self.lang = lang.Lang()

    def set_preview_webview(self, webview: PyQt5.QtWebKitWidgets.QWebView, default_page: str):
        self.previewWebview = webview
        self.default_page = default_page

    def draw_preview(self):
        if self.count() <= 0:
            return
        item = self.currentWidget()
        file_dir = item.property('fileName').replace(item.property('fileShortName'), '')
        print('fileDir = ' + file_dir)
        print('fileName = ' + item.property('fileName'))
        print('fileShortName = ' + item.property('fileShortName'))
        scroll = None
        if self.previous_file == item.property('fileName'):
            scroll = self.previewWebview.page().currentFrame().scrollPosition()
            print(scroll)
        self.previous_file = item.property('fileName')
        if item.property('fileType') in [] or item.property('fileExt') in ['xhtml', 'html']:
            try:
                txe = item.children().__getitem__(2).text()
                txe = txe\
                    .replace('<head>', '<head><base href="file:///'+file_dir.replace(os.sep, '/')+'">')
                #     .replace(' href="../', ' href="')\
                #     .replace(' src="../', ' src="')\
                #     .replace(' href="', ' href="file:///'+fileDir.replace(os.sep, '/')+'/')\
                #     .replace(' src="', ' src="file:///'+fileDir.replace(os.sep, '/')+'/')
                self.previewWebview.page().currentFrame().setHtml(txe)
                if scroll is not None:
                    self.previewWebview.page().currentFrame().setScrollPosition(scroll)
            except Exception:
                traceback.print_exc()
        else:
            self.previewWebview.setHtml(self.default_page)

    def content_update(self):
        if self.currentWidget().property('fileExt') in ['xhtml', 'html', 'css', 'xml', 'opf', 'ncx']:
            old_txt = self.currentWidget().property('originalContent')
            new_txt = self.currentWidget().children().__getitem__(2).text()

            index = self.currentIndex()
            if old_txt != new_txt:
                icon = QtGui.QIcon()
                image = QtGui.QPixmap()
                image.load(app_directory.replace(os.sep, '/') + '/icons/white/edit.png')
                icon.addPixmap(image, QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.setTabIcon(index, icon)
            else:
                self.setTabIcon(index, QtGui.QIcon())
        self.draw_preview()

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())

    def reload_contents(self):
        try:
            for i in range(0, self.count()):
                item = self.widget(i)
                if item.property('fileExt') in ['xhtml', 'html', 'css', 'xml', 'opf', 'ncx']:
                    file = open(item.property('fileName'), "r", encoding="utf8")
                    data = file.read()
                    file.close()
                    item.children().__getitem__(2).setText(data)
                self.setTabIcon(i, QtGui.QIcon())
        except Exception:
            ''

    def create_pane(self, title: str, path: str):
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

        is_text = True
        if kind.mime in ['image/jpeg', 'image/png', 'image/gif', 'image/bmp']:
            is_text = False
            data = create_thumbnail(path, False)
        if kind.mime == 'binary':
            is_text = False
        if data is None:
            return

        tab = QtWidgets.QWidget()
        # tab.setObjectName("tab")
        tab.setProperty('fileName', path)
        tab.setProperty('fileShortName', path.replace(os.path.dirname(path), '')[1:])
        tab.setProperty('fileType', kind.mime)
        tab.setProperty('fileExt', kind.extension)
        if is_text is True:
            tab.setProperty('originalContent', data)
        vertical_layout = QtWidgets.QVBoxLayout(tab)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.setSpacing(1)

        if is_text is True:
            block = UIClass()
            super(UIClass, block).__init__()
            PyQt5.uic.loadUi(app_directory + '/editor/text_edit.ui'.replace('/', os.sep), block)  # Load the .ui file
            block.setStyleSheet("""
            QPushButton{ background:transparent; }
            QPushButton:hover{ background-color:rgb(120, 120, 120); }
            QPushButton:pressed{ background-color:rgb(120, 120, 120); }
            QPushButton:checked{ background-color:rgb(150, 150, 150);}
            """)
            try:
                block.setMaximumHeight(85)
                block.setMinimumHeight(85)
                block.setFixedHeight(85)
                if tab.property('fileExt') not in ['xhtml', 'html', 'css', 'xml', 'opf', 'ncx']:
                    self.clear_layout(block.horizon1_1)
                    self.clear_layout(block.horizon2)
                    self.clear_layout(block.horizon3)
                    block.setMaximumHeight(30)
                    block.setMinimumHeight(30)
                    block.setFixedHeight(30)
                elif tab.property('fileExt') in ['css', 'xml', 'opf', 'ncx']:
                    if tab.property('fileExt') in ['css']:
                        block.btnDebug.setMinimumHeight(0)
                        block.btnDebug.setMaximumWidth(0)
                        block.btnDebug.setMinimumHeight(0)
                        block.btnDebug.setMaximumWidth(0)
                        block.btnDebug.setFixedHeight(0)
                        block.btnDebug.setFixedWidth(0)
                    self.clear_layout(block.horizon2)
                    self.clear_layout(block.horizon3)
                    block.setMaximumHeight(30)
                    block.setMinimumHeight(30)
                    block.setFixedHeight(30)
            except Exception:
                traceback.print_exc()

            vertical_layout.addWidget(block)

            try:
                text_edit = None
                if tab.property('fileExt') in ['xhtml', 'html']:
                    text_edit = SimplePythonEditor(QsciLexerHTML(), tab)
                elif tab.property('fileExt') in ['xml', 'opf', 'ncx']:
                    text_edit = SimplePythonEditor(QsciLexerXML(), tab)
                    text_edit.elexer.setColor(QtGui.QColor.fromRgb(255, 255, 255), QsciLexerXML.Default)
                    text_edit.elexer.setColor(QtGui.QColor('#000080'), QsciLexerXML.Tag)
                    text_edit.elexer.setColor(QtGui.QColor('#000080'), QsciLexerXML.UnknownTag)
                elif tab.property('fileExt') in ['css']:
                    text_edit = SimplePythonEditor(QsciLexerCSS(), tab)
                else:
                    text_edit = SimplePythonEditor(None, tab)
                    text_edit.setColor(QColor("#ffffff"))
                    text_edit.setPaper(QColor("#A6A6A6"))

                if text_edit.elexer is not None:
                    text_edit.elexer.setDefaultPaper(QColor("#A6A6A6"))
                    text_edit.elexer.setDefaultColor(QColor("#ffffff"))
                    text_edit.elexer.setPaper(QColor("#A6A6A6"))
                    text_edit.setObjectName("textEdit")
                    text_edit.setCaretLineBackgroundColor(QColor("#BBBBBB"))

                font = QFont()
                font.setFamily('Courier')
                font.setFixedPitch(True)
                font.setPointSize(10)
                text_edit.setFont(font)
                text_edit.setMarginsFont(font)
                font_metrics = QFontMetrics(font)
                text_edit.setMarginWidth(0, font_metrics.width("00000") + 1)
                text_edit.setMarginsBackgroundColor(QColor("#333333"))
                text_edit.setMarginsForegroundColor(QColor("#ffffff"))
                text_edit.setFolding(QsciScintilla.BoxedTreeFoldStyle)

                text_edit.setText(data)
                text_edit.textChanged.connect(lambda: self.content_update())

                vertical_layout.addWidget(text_edit)

                shortcut = QtWidgets.QShortcut(QtCore.Qt.ControlModifier | QtCore.Qt.Key_S, text_edit)
                shortcut.activated.connect(lambda: self.save_file(None))

                shortcut = QtWidgets.QShortcut(QtCore.Qt.ControlModifier | QtCore.Qt.Key_D, text_edit)
                shortcut.activated.connect(self.duplication)
            except Exception:
                traceback.print_exc()
        else:
            block = PyQt5.QtWebKitWidgets.QWebView()
            page = 'file:///' + path.replace(os.sep, '/')
            block.setUrl(QtCore.QUrl(page))
            vertical_layout.addWidget(block)

        self.addTab(tab, QtGui.QIcon(), title)
        self.setTabsClosable(True)
        self.setCurrentIndex(self.count() - 1)

        try:
            block.btnSave.setToolTip('Save File in session')
            block.btnSave.clicked.connect(self.save_file)
            block.btnUndo.setToolTip('Undo')
            block.btnUndo.clicked.connect(lambda: text_edit.undo())
            block.btnRedo.setToolTip('Redo')
            block.btnRedo.clicked.connect(lambda: text_edit.redo())
            block.btnCut.setToolTip('Cut')
            block.btnCut.clicked.connect(lambda: text_edit.cut())
            block.btnCopy.setToolTip('Copy')
            block.btnCopy.clicked.connect(lambda: text_edit.copy())
            block.btnPaste.setToolTip('Paste')
            block.btnPaste.clicked.connect(lambda: text_edit.paste())
            block.btnDebug.setToolTip('Debug Document')
            block.btnDebug.clicked.connect(self.debug_text)
            block.btnComment.setToolTip('Comment')
            block.btnComment.clicked.connect(self.comment_text)
            block.btnPrettify.setToolTip('Prettify File')
            block.btnPrettify.clicked.connect(self.prettify_text)

            block.btnBold.setToolTip('Bold')
            block.btnBold.clicked.connect(lambda: self.block_paster_text('<b>', '</b>'))
            block.btnItalic.setToolTip('Italic')
            block.btnItalic.clicked.connect(lambda: self.block_paster_text('<i>', '</i>'))
            block.btnUnderline.setToolTip('Underline')
            block.btnUnderline.clicked.connect(lambda: self.block_paster_text('<u>', '</u>'))
            block.btnStrikethrough.setToolTip('Strikethrough')
            block.btnStrikethrough.clicked.connect(lambda: self.block_paster_text('<s>', '</s>'))
            block.btnSub.setToolTip('Sub')
            block.btnSub.clicked.connect(lambda: self.block_paster_text('<sub>', '</sub>'))
            block.btnSup.setToolTip('Sup')
            block.btnSup.clicked.connect(lambda: self.block_paster_text('<sup>', '</sup>'))
            block.btnTextColor.setToolTip('Text Color')
            block.btnTextColor.clicked.connect(self.claim_text_color)
            block.btnBackColor.setToolTip('Back Color')
            block.btnBackColor.clicked.connect(self.claim_back_color)
            block.btnAlignLeft.setToolTip('Align Left')
            block.btnAlignLeft.clicked.connect(lambda: self.block_paster_text('<div style="text-align:left;">', '</div>'))
            block.btnAlignCenter.setToolTip('Align Center')
            block.btnAlignCenter.clicked.connect(lambda: self.block_paster_text('<div style="text-align:center;">', '</div>'))
            block.btnAlignRight.setToolTip('Align Right')
            block.btnAlignRight.clicked.connect(lambda: self.block_paster_text('<div style="text-align:right;">', '</div>'))
            block.btnAlignJustify.setToolTip('Align Justify')
            block.btnAlignJustify.clicked.connect(lambda: self.block_paster_text('<div style="text-align:justify;">', '</div>'))
            block.btnList.setToolTip('List')
            block.btnList.clicked.connect(lambda: self.block_list('ul'))
            block.btnNumList.setToolTip('Numeric List')
            block.btnNumList.clicked.connect(lambda: self.block_list('ol'))
            block.btnLink.setToolTip('Link')
            block.btnLink.clicked.connect(self.link_poser)
            block.btnImg.setToolTip('Image')
            block.btnImg.clicked.connect(self.img_poser)
        except Exception:
            {}

    def save_file(self, evt):
        try:
            item = self.currentWidget()
            new_text = item.children().__getitem__(2).text()
            old_text = item.property('originalContent')
            file_name = item.property('fileName')
            if old_text != new_text:
                print('Save')
                file = open(file_name, 'w', encoding="utf8")
                file.write(new_text)
                file.close()
                item.setProperty('originalContent', new_text)
                self.setTabIcon(self.currentIndex(), QtGui.QIcon())
            else:
                print('NO DIF')
        except Exception:
            traceback.print_exc()

    def duplication(self):  # duplication of current line or selected block
        try:
            item = self.currentWidget()
            tx_edit = item.children().__getitem__(2)
            sel = tx_edit.getSelection()
            if sel[0] == sel[2] and sel[1] == sel[3]:
                # pos = tx_edit.getCursorPosition()
                SimplePythonEditor.setSelection(sel[0], 0, sel[0]+1, 0)
                selected_text = tx_edit.selectedText()
                tx_edit.insertAt(selected_text, sel[0]+1, 0)
            else:
                selected_text = tx_edit.selectedText()
                new_text = selected_text + selected_text
                tx_edit.replaceSelectedText(new_text)
                tx_edit.setSelection(sel[0], sel[1], sel[2], sel[3])
        except Exception:
            traceback.print_exc()

    def claim_back_color(self):
        color = self.claim_color()
        text = self.currentWidget().children().__getitem__(2).selectedText()
        if color is not None:
            if re.search('<div', text) is not None:
                self.block_paster_text('<div style="background-color:{}">'.format(color.name()), '</div>')
            elif re.search('<p', text) is not None:
                self.block_paster_text('<div style="background-color:{}">'.format(color.name()), '</div>')
            else:
                self.block_paster_text('<span style="background-color:{}">'.format(color.name()), '</span>')

    def claim_text_color(self):
        color = self.claim_color()
        text = self.currentWidget().children().__getitem__(2).selectedText()
        if color is not None:
            if re.search('<div', text) is not None:
                self.block_paster_text('<div style="color:{}">'.format(color.name()), '</div>')
            elif re.search('<p', text) is not None:
                self.block_paster_text('<div style="color:{}">'.format(color.name()), '</div>')
            else:
                self.block_paster_text('<span style="color:{}">'.format(color.name()), '</span>')

    def claim_color(self):
        try:
            color = QtWidgets.QColorDialog.getColor(QtGui.QColor.fromRgb(0, 0, 0), self)
            if color.isValid() is True:
                return color
        except Exception:
            traceback.print_exc()
        return None

    def debug_text(self):
        try:
            item = self.currentWidget()
            tx_edit = item.children().__getitem__(2)
            if item.property('fileExt') in ['xhtml', 'html', 'xml', 'opf', 'ncx']:
                ret = editor.xmlt.parse(tx_edit.text())
                if ret is not None:
                    dialog.WarnDialog('', 'Error found at line {}, collumn {}'.format(ret[0], ret[1]), self.parent())
                    tx_edit.setSelection(ret[0]-1, 0, ret[0]-1, ret[1])
                    # SimplePythonEditor.setFocus()
                    tx_edit.setFocus()
            if item.property('fileExt') in ['css']:
                {}
        except Exception:
            traceback.print_exc()

    def comment_text(self):
        try:
            item = self.currentWidget()
            tx_edit = item.children().__getitem__(2)
            if item.property('fileExt') in ['xhtml', 'html', 'xml', 'opf', 'ncx', 'css']:
                selected_text = tx_edit.selectedText()
                sel = tx_edit.getSelection()
                if sel[0] == sel[2] and sel[1] == sel[3]:
                    pos = tx_edit.getCursorPosition()
                    if item.property('fileExt') in ['xhtml', 'html', 'xml', 'opf', 'ncx']:
                        tx_edit.insertAt("<!-- Comment -->", pos[0], pos[1])
                    elif item.property('fileExt') in ['css']:
                        tx_edit.insertAt("/* Comment */", pos[0], pos[1])
                else:
                    if item.property('fileExt') in ['xhtml', 'html', 'xml', 'opf', 'ncx']:
                        if selected_text.startswith('<!-- ') and selected_text.endswith(' -->'):
                            tx_edit.replaceSelectedText(selected_text[5:][:-4])
                            tx_edit.setSelection(sel[0], sel[1], sel[2], sel[3] - 4)
                        else:
                            tx_edit.replaceSelectedText('<!-- '+selected_text+' -->')
                            tx_edit.setSelection(sel[0], sel[1], sel[2], sel[3] + 4)
                    if item.property('fileExt') in ['css']:
                        if selected_text.startswith('/* ') and selected_text.endswith(' */'):
                            tx_edit.replaceSelectedText(selected_text[3:][:-3])
                            tx_edit.setSelection(sel[0], sel[1], sel[2], sel[3]-3)
                        else:
                            tx_edit.replaceSelectedText('/* '+selected_text+' */')
                            tx_edit.setSelection(sel[0], sel[1], sel[2], sel[3]+3)
            else:
                return
        except Exception:
            traceback.print_exc()

    def block_paster_text(self, block_start: str, block_end: str):
        try:
            item = self.currentWidget()
            tx_edit = item.children().__getitem__(2)
            selected_text = tx_edit.selectedText()
            sel = tx_edit.getSelection()
            if sel[0] == sel[2] and sel[1] == sel[3]:
                pos = tx_edit.getCursorPosition()
                tx_edit.insertAt(block_start + ' ' + block_end, pos[0], pos[1])
            else:
                max_len = len(block_start) + len(block_end)
                if selected_text.startswith(block_start) and selected_text.endswith(block_end):
                    tx_edit.replaceSelectedText(selected_text[len(block_start):][:len(block_end)*-1])
                    tx_edit.setSelection(sel[0], sel[1], sel[2], sel[3] - max_len)
                else:
                    tx_edit.replaceSelectedText(block_start + selected_text + block_end)
                    tx_edit.setSelection(sel[0], sel[1], sel[2], sel[3] + max_len)
        except Exception:
            traceback.print_exc()

    def block_list(self, list_type: str = 'ul'):  # list_type = ul or ol
        try:
            block_start = '<'+list_type+'>'
            block_end = '</'+list_type+'>'
            item = self.currentWidget()
            tx_edit = item.children().__getitem__(2)
            selected_text = tx_edit.selectedText().replace('\t', '').replace('\r', '')
            selected_text = re.sub('\n {2,}', '\n', selected_text)
            sel = tx_edit.getSelection()
            if sel[0] == sel[2] and sel[1] == sel[3]:
                pos = tx_edit.getCursorPosition()
                tx_edit.insertAt(block_start + '\n<li>ligne</li>\n' + block_end, pos[0], pos[1])
            else:
                # max = len(block_start) + len(block_end)
                # new_text = ''
                if selected_text.startswith(block_start) and selected_text.endswith(block_end):
                    new_text = selected_text[len(block_start):][:len(block_end)*-1]\
                        .replace('\n', '').replace('<li>', '\n').replace('</li>', '')
                else:
                    new_text = block_start
                    tb = selected_text.split('\n')
                    for line in tb:
                        new_text += '\n    <li>' + line + '</li>'
                    new_text += block_end
                tx_edit.replaceSelectedText(new_text)
                tbx = new_text.split('\n')
                tx_edit.setSelection(sel[0], sel[1], sel[0] + len(tbx) - 1, len(tbx[len(tbx) - 1]))
        except Exception:
            traceback.print_exc()

    def prettify_text(self):
        try:
            item = self.currentWidget()
            tx_edit = item.children().__getitem__(2)
            sel = pos = tx_edit.getSelection()
            if sel[0] == sel[2] and sel[1] == sel[3]:
                pos = tx_edit.getCursorPosition()
            if item.property('fileExt') in ['xml', 'opf', 'ncx']:
                ret = editor.xmlt.prettify(tx_edit.text())
                tx_edit.selectAll(True)
                tx_edit.replaceSelectedText(ret)
            elif item.property('fileExt') in ['css']:
                ret = editor.css.prettifyCss(tx_edit.text())
                tx_edit.selectAll(True)
                tx_edit.replaceSelectedText(ret)
            else:
                return
            if sel[0] == sel[2] and sel[1] == sel[3]:
                tx_edit.setCursorPosition(pos[0], pos[1])
            else:
                tx_edit.setSelection(sel[0], sel[1], sel[2], sel[3])
        except Exception:
            traceback.print_exc()

    def link_poser(self):
        block_start = '<a '
        block_end = '</a>'
        try:
            item = self.currentWidget()
            window = editor.link.LinkWindow(self.parent(), app_directory + os.sep + 'editor' + os.sep + 'tmp'
                                            + os.sep + 'current')
            tx_edit = item.children().__getitem__(2)
            selected_text = tx_edit.selectedText()
            sel = tx_edit.getSelection()
            if sel[0] == sel[2] and sel[1] == sel[3]:
                ret = window.openExec()
                if ret is not None:
                    pos = tx_edit.getCursorPosition()
                    new_text = '<a href="' + ret['url'] + '">' + ret['text'] + '</a>'
                    tx_edit.insertAt(new_text, pos[0], pos[1])
                    tb = new_text.split('\n')
                    tx_edit.setSelection(pos[0], pos[1], pos[0] + len(tb) - 1, len(tb[len(tb) - 1]) - 1)
            else:
                # max_len = len(block_start) + len(block_end)
                if selected_text.startswith(block_start) and selected_text.endswith(block_end):
                    new_text = re.sub('<a(.*)>(.*)</a>', '%2', selected_text)
                    tx_edit.replaceSelectedText(new_text)
                    tb = new_text.split('\n')
                    tx_edit.setSelection(sel[0], sel[1], sel[0] + len(tb) - 1, len(tb[len(tb) - 1]) - 1)
                else:
                    ret = window.openExec(selected_text)
                    if ret is not None:
                        new_text = '<a href="'+ret['url']+'">'+ret['text']+'</a>'
                        tx_edit.replaceSelectedText(new_text)
                        tb = new_text.split('\n')
                        tx_edit.setSelection(sel[0], sel[1], sel[0] + len(tb) - 1, len(tb[len(tb) - 1]) - 1)
        except Exception:
            traceback.print_exc()

    def img_poser(self):
        try:
            item = self.currentWidget()
            window = editor.img.ImgWindow(self.parent(), app_directory + os.sep + 'editor' + os.sep + 'tmp'
                                          + os.sep + 'current')
            tx_edit = item.children().__getitem__(2)
            selected_text = tx_edit.selectedText()
            # sel = tx_edit.getSelection()
            pos = tx_edit.getCursorPosition()
            ret = window.openExec(selected_text, None)
            if ret is not None:
                tb1 = item.property('fileName').replace(
                    app_directory + os.sep + 'editor' + os.sep + 'tmp' + os.sep + 'current' + os.sep,
                    ''
                ).split(os.sep)
                print(tb1)
                adl = ''
                for i in range(0, len(tb1)-1):
                    adl += '../'
                new_text = '<img src="' + adl + ret['url'] + '" alt="' + ret['text'] \
                           + '" title="' + ret['text'] + '" />'
                tx_edit.insertAt(new_text, pos[0], pos[1])
                tb = new_text.split('\n')
                tx_edit.setSelection(pos[0], pos[1], pos[0] + len(tb) - 1, len(tb[len(tb) - 1]) - 1)
        except Exception:
            traceback.print_exc()
