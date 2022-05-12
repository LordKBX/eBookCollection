import os
import sys
import PyQt5.QtWebKitWidgets
import PyQt5.uic
from PyQt5.uic import *
from PyQt5.QtWidgets import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from common.books import *
from common import dialog, vars
import xmlt
import css
import link
import img
import color_picker
from codeEditor import CodeEditor
import syntaxHighlighter


class UIClass(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


class FileType:
    def __init__(self, ext: str, mime: str):
        self.extension = ext
        self.mime = mime


class EditorTabManager(QtWidgets.QTabWidget):
    tmpcss = ''
    lang = None
    BDD = None
    style = None
    destDir = ''
    highlight = None

    def __init__(self, parent: any):
        QtWidgets.QTabWidget.__init__(self, parent)
        self.setWindowTitle("Tab Dialog")
        self.previewWebview = None
        self.previous_file = ''
        self.default_page = ''

    def set_preview_webview(self, webview: PyQt5.QtWebKitWidgets.QWebView, default_page: str):
        self.previewWebview = webview
        self.default_page = default_page

    def draw_preview(self):
        if self.count() <= 0:
            return
        item = self.currentWidget()
        file_dir = item.property('fileName').replace(item.property('fileShortName'), '')
        scroll = None
        if self.previous_file == item.property('fileName'):
            scroll = self.previewWebview.page().currentFrame().scrollPosition()
        self.previous_file = item.property('fileName')
        type_ok = ['text/css', 'application/oebps-package+xml', 'application/x-dtbncx+xml', 'application/xml',
                   'application/xhtml+xml', 'text/plain']
        if item.property('fileType') in type_ok:
            try:
                # txe = item.children().__getitem__(2).text()
                obj = item.children().__getitem__(2)
                txe = obj.toPlainText()

                txe = txe\
                    .replace('<head>', '<head><base href="file:///'+self.destDir.replace(os.sep, '/')+'/">')\
                    .replace('="/', '="file:///' + self.destDir.replace(os.sep, '/') + '/') \
                    .replace('="../', '="file:///' + file_dir.replace(os.sep, '/') + '../')
                self.previewWebview.page().currentFrame().setHtml(txe)
                if scroll is not None:
                    self.previewWebview.page().currentFrame().setScrollPosition(scroll)
            except Exception:
                traceback.print_exc()
        else:
            self.previewWebview.setHtml(self.default_page)

        self.previewWebview.page().settings().setUserStyleSheetUrl(QtCore.QUrl.fromLocalFile(self.tmpcss))
        self.previewWebview.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

    def content_update(self):
        try:
            if self.currentWidget().property('fileExt') in ['xhtml', 'html', 'css', 'xml', 'opf', 'ncx']:
                old_txt = self.currentWidget().property('originalContent')
                new_txt = self.currentWidget().children().__getitem__(2).toPlainText()

                index = self.currentIndex()
                if old_txt != new_txt:
                    icon = QtGui.QIcon()
                    image = QtGui.QPixmap()
                    image.load(vars.get_style_var(self.style, 'icons/edit'))
                    icon.addPixmap(image, QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.setTabIcon(index, icon)
                else:
                    self.setTabIcon(index, QtGui.QIcon())
                if self.highlight is not None:
                    self.highlight.rehighlightBlock(self.highlight.currentBlock())
            self.draw_preview()
        except Exception as err:
            traceback.print_exc()

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

    def create_pane(self, title: str, icon: str, path: str, parent, tmpcss: str = None):
        try:
            if self.count() > 0:
                for i in range(0, self.count()):
                    if self.tabToolTip(i) == path:
                        self.setCurrentIndex(i)
                        return
            if self.lang is None:
                self.lang = parent.lang
                self.BDD = parent.BDD
                self.style = style = self.BDD.get_param('style')
                self.destDir = parent.tmpDir + os.sep + 'current'
            if tmpcss is not None:
                self.tmpcss = tmpcss
            data = None
            is_text = None
            file_type, file_ext = get_file_type(path, True)
            list_type_ok = [
                'text/css',
                'application/oebps-package+xml',
                'application/x-dtbncx+xml',
                'application/xml',
                'application/xhtml+xml',
                'text/plain', 'text/html'
            ]
            list_type_img = ['image/jpeg', 'image/png', 'image/gif', 'image/bmp']
            if file_type in list_type_ok:
                try:
                    file = open(path, "r", encoding="utf8")
                    data = file.read()
                    file.close()
                    file_type = 'text/plain'
                    is_text = True
                except Exception:
                    ""
            print("file_type", file_type)

            if file_type not in list_type_ok and file_type not in list_type_img:
                dialog.WarnDialog('', 'File type not treated', self.parent())
                return

            if data is None:
                if file_type in ['image/jpeg', 'image/png', 'image/gif', 'image/bmp']:
                    is_text = False
                    data = create_thumbnail(path, False)
                else:
                    file = open(path, "r", encoding="utf8")
                    data = file.read()
                    file.close()
            if data is None:
                return

            tab = QtWidgets.QWidget()
            # tab.setObjectName("tab")
            tab.setProperty('fileName', path)
            tab.setProperty('fileShortName', path.replace(os.path.dirname(path), '')[1:])
            tab.setProperty('fileType', file_type)
            tab.setProperty('fileExt', file_ext[1:])
            tab.setProperty('fileIcon', icon)
            if is_text is True:
                tab.setProperty('originalContent', data)
            vertical_layout = QtWidgets.QVBoxLayout(tab)
            vertical_layout.setContentsMargins(0, 0, 0, 0)
            vertical_layout.setSpacing(1)

            if is_text is False:
                block = PyQt5.QtWebKitWidgets.QWebView()
                page = 'file:///' + path.replace(os.sep, '/')
                block.setUrl(QtCore.QUrl(page))
                vertical_layout.addWidget(block)
            else:
                block = UIClass()
                super(UIClass, block).__init__()
                PyQt5.uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'text_edit.ui'.replace('/', os.sep), block)  # Load the .ui file
                block.setStyleSheet(common.vars.get_style_var(self.style, 'EditorEditPaneButtons'))
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
                    text_edit = CodeEditor()
                    # text_edit = QPlainTextEdit()
                    text_edit.setTabStopWidth(16)
                    if tab.property('fileExt') in ['xhtml', 'html']:
                        self.highlight = syntaxHighlighter.SyntaxHighlighter(text_edit.document(), syntaxHighlighter.MODES.HTML)
                    elif tab.property('fileExt') in ['xml', 'opf', 'ncx']:
                        self.highlight = syntaxHighlighter.SyntaxHighlighter(text_edit.document(), syntaxHighlighter.MODES.XML)
                    elif tab.property('fileExt') in ['css']:
                        self.highlight = syntaxHighlighter.SyntaxHighlighter(text_edit.document(), syntaxHighlighter.MODES.CSS)

                    print("fileExt", tab.property('fileExt'))
                    # if text_edit.elexer is not None:
                    #     text_edit.setObjectName("textEdit")
                    text_edit.setPlainText(data)
                    text_edit.textChanged.connect(lambda: self.content_update())

                    vertical_layout.addWidget(text_edit)

                    shortcut = QtWidgets.QShortcut(QtCore.Qt.ControlModifier | QtCore.Qt.Key_S, text_edit)
                    shortcut.activated.connect(lambda: self.save_file(None))

                    shortcut = QtWidgets.QShortcut(QtCore.Qt.ControlModifier | QtCore.Qt.Key_D, text_edit)
                    shortcut.activated.connect(self.duplication)
                except Exception:
                    traceback.print_exc()

                try:
                    block.btnSave.clicked.connect(self.save_file)
                    block.btnUndo.clicked.connect(self.undo)
                    block.btnRedo.clicked.connect(self.redo)
                    block.btnCut.clicked.connect(self.cut)
                    block.btnCopy.clicked.connect(self.copy)
                    block.btnPaste.clicked.connect(self.paste)
                    block.btnDebug.clicked.connect(self.debug_text)
                    block.btnComment.clicked.connect(self.comment_text)
                    block.btnPrettify.clicked.connect(self.prettify_text)
                    block.btnBold.clicked.connect(lambda: self.block_paster_text('<b>', '</b>'))
                    block.btnItalic.clicked.connect(lambda: self.block_paster_text('<i>', '</i>'))
                    block.btnUnderline.clicked.connect(lambda: self.block_paster_text('<u>', '</u>'))
                    block.btnStrikethrough.clicked.connect(lambda: self.block_paster_text('<s>', '</s>'))
                    block.btnSub.clicked.connect(lambda: self.block_paster_text('<sub>', '</sub>'))
                    block.btnSup.clicked.connect(lambda: self.block_paster_text('<sup>', '</sup>'))
                    block.btnTextColor.clicked.connect(self.claim_text_color)
                    block.btnBackColor.clicked.connect(self.claim_back_color)
                    block.btnAlignLeft.clicked.connect(lambda: self.block_paster_text('<div style="text-align:left;">', '</div>'))
                    block.btnAlignCenter.clicked.connect(lambda: self.block_paster_text('<div style="text-align:center;">', '</div>'))
                    block.btnAlignRight.clicked.connect(lambda: self.block_paster_text('<div style="text-align:right;">', '</div>'))
                    block.btnAlignJustify.clicked.connect(lambda: self.block_paster_text('<div style="text-align:justify;">', '</div>'))
                    block.btnList.clicked.connect(lambda: self.block_list('ul'))
                    block.btnNumList.clicked.connect(lambda: self.block_list('ol'))
                    block.btnLink.clicked.connect(self.link_poser)
                    block.btnImg.clicked.connect(self.img_poser)
                except Exception:
                    traceback.print_exc()

                block.btnSave.setToolTip(self.lang['Editor/EditPane/Save'])
                block.btnUndo.setToolTip(self.lang['Editor/EditPane/Undo'])
                block.btnRedo.setToolTip(self.lang['Editor/EditPane/Redo'])
                block.btnCut.setToolTip(self.lang['Editor/EditPane/Cut'])
                block.btnCopy.setToolTip(self.lang['Editor/EditPane/Copy'])
                block.btnPaste.setToolTip(self.lang['Editor/EditPane/Paste'])
                block.btnDebug.setToolTip(self.lang['Editor/EditPane/Debug'])
                block.btnComment.setToolTip(self.lang['Editor/EditPane/Comment'])
                block.btnPrettify.setToolTip(self.lang['Editor/EditPane/Prettify'])
                block.btnBold.setToolTip(self.lang['Editor/EditPane/Bold'])
                block.btnItalic.setToolTip(self.lang['Editor/EditPane/Italic'])
                block.btnUnderline.setToolTip(self.lang['Editor/EditPane/Underline'])
                block.btnStrikethrough.setToolTip(self.lang['Editor/EditPane/Strikethrough'])
                block.btnSub.setToolTip(self.lang['Editor/EditPane/Sub'])
                block.btnSup.setToolTip(self.lang['Editor/EditPane/Sup'])
                block.btnTextColor.setToolTip(self.lang['Editor/EditPane/TextColor'])
                block.btnBackColor.setToolTip(self.lang['Editor/EditPane/BackColor'])
                block.btnAlignLeft.setToolTip(self.lang['Editor/EditPane/AlignLeft'])
                block.btnAlignCenter.setToolTip(self.lang['Editor/EditPane/AlignCenter'])
                block.btnAlignRight.setToolTip(self.lang['Editor/EditPane/AlignRight'])
                block.btnAlignJustify.setToolTip(self.lang['Editor/EditPane/AlignJustify'])
                block.btnList.setToolTip(self.lang['Editor/EditPane/List'])
                block.btnNumList.setToolTip(self.lang['Editor/EditPane/NumericList'])
                block.btnLink.setToolTip(self.lang['Editor/EditPane/Link'])
                block.btnImg.setToolTip(self.lang['Editor/EditPane/Image'])

                block.btnSave.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/save'))))
                block.btnUndo.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/undo'))))
                block.btnRedo.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/redo'))))
                block.btnCut.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/cut'))))
                block.btnCopy.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/copy'))))
                block.btnPaste.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/paste'))))
                block.btnDebug.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/debug'))))
                block.btnComment.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/comment'))))
                block.btnPrettify.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/prettify'))))
                block.btnBold.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/bold'))))
                block.btnItalic.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/italic'))))
                block.btnUnderline.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/underline'))))
                block.btnStrikethrough.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/strike_through'))))
                block.btnSub.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/sub'))))
                block.btnSup.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/sup'))))
                block.btnTextColor.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/text_color'))))
                block.btnBackColor.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/back_color'))))
                block.btnAlignLeft.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/align_left'))))
                block.btnAlignCenter.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/align_center'))))
                block.btnAlignRight.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/align_right'))))
                block.btnAlignJustify.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/align_justify'))))
                block.btnList.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/list'))))
                block.btnNumList.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/list_ordered'))))
                block.btnLink.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/link'))))
                block.btnImg.setIcon(QtGui.QIcon(QtGui.QPixmap(vars.get_style_var(self.style, 'icons/image'))))

            self.addTab(tab, QtGui.QIcon(QtGui.QPixmap(icon)), title)
            self.setTabsClosable(True)
            self.setCurrentIndex(self.count() - 1)
            self.setTabToolTip(self.count() - 1, path)
        except Exception:
            traceback.print_exc()

    def save_file(self, evt):
        try:
            item = self.currentWidget()
            new_text = item.children().__getitem__(2).toPlainText()
            old_text = item.property('originalContent')
            file_name = item.property('fileName')
            icon = item.property('fileIcon')
            if old_text != new_text:
                print('Save')
                file = open(file_name, 'w', encoding="utf8")
                file.write(new_text)
                file.close()
                item.setProperty('originalContent', new_text)
                if icon is None:
                    self.setTabIcon(self.currentIndex(), QtGui.QIcon())
                else:
                    self.setTabIcon(self.currentIndex(), QtGui.QIcon(QtGui.QPixmap(icon)))
            else:
                print('NO DIF')
        except Exception:
            traceback.print_exc()

    def undo(self):
        item = self.currentWidget()
        tx_edit = item.children().__getitem__(2)
        tx_edit.setFocus()
        tx_edit.undo()

    def redo(self):
        item = self.currentWidget()
        tx_edit = item.children().__getitem__(2)
        tx_edit.setFocus()
        tx_edit.redo()

    def cut(self):
        item = self.currentWidget()
        tx_edit = item.children().__getitem__(2)
        tx_edit.setFocus()
        tx_edit.cut()

    def copy(self):
        item = self.currentWidget()
        tx_edit = item.children().__getitem__(2)
        tx_edit.setFocus()
        tx_edit.copy()

    def paste(self):
        item = self.currentWidget()
        tx_edit = item.children().__getitem__(2)
        tx_edit.setFocus()
        tx_edit.paste()

    def duplication(self):  # duplication of current line or selected block
        try:
            item = self.currentWidget()
            tx_edit = item.children().__getitem__(2)
            cursor = tx_edit.textCursor()

            # Security
            if cursor.hasSelection():
                selected_text = tx_edit.textCursor().selection().toPlainText()
                # We insert the new text, which will override the selected
                # text
                cursor.insertText(selected_text+selected_text)

                # And set the new cursor
                tx_edit.setTextCursor(cursor)
        except Exception:
            traceback.print_exc()

    def claim_back_color(self):
        color = self.claim_color()
        text = self.currentWidget().children().__getitem__(2).textCursor().selection().toPlainText()
        if color is not None:
            if re.search('<div', text) is not None or re.search('<p', text) is not None:
                self.block_paster_text('<div style="background-color:{}">'.format(color.name()), '</div>')
            else:
                self.block_paster_text('<span style="background-color:{}">'.format(color.name()), '</span>')

    def claim_text_color(self):
        color = self.claim_color()
        text = self.currentWidget().children().__getitem__(2).textCursor().selection().toPlainText()
        if color is not None:
            if re.search('<div', text) is not None or re.search('<p', text) is not None:
                self.block_paster_text('<div style="color:{}">'.format(color.name()), '</div>')
            else:
                self.block_paster_text('<span style="color:{}">'.format(color.name()), '</span>')

    def claim_color(self):
        try:
            color = color_picker.ColorPicker(self).getColor()
            if color is not None:
                return color
        except Exception:
            traceback.print_exc()
        return None

    def debug_text(self):
        try:
            item = self.currentWidget()
            tx_edit = item.children().__getitem__(2)
            # tx_edit = QPlainTextEdit()
            if item.property('fileExt') in ['xhtml', 'html', 'xml', 'opf', 'ncx']:
                ret = xmlt.parse(tx_edit.toPlainText())
                if ret is not None:
                    dialog.WarnDialog('', 'Error found at line {}, collumn {}'.format(ret[0], ret[1]), self.parent())
                    cursor = tx_edit.textCursor()
                    # cursor = QtGui.QTextCursor()
                    cursor.setPosition(ret[2])
                    tx_edit.setTextCursor(cursor)
                    # tx_edit.setTextCursor(QtGui.QTextCursor(ret[0]-1, 0, ret[0]-1, ret[1])).setSelection(ret[0]-1, 0, ret[0]-1, ret[1])
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
                selected_text = tx_edit.textCursor().selection().toPlainText()
                sel = tx_edit.textCursor()
                if sel.hasSelection() is False:
                    if item.property('fileExt') in ['xhtml', 'html', 'xml', 'opf', 'ncx']:
                        self.block_paster_text("<!-- Comment -->", "")
                    elif item.property('fileExt') in ['css']:
                        self.block_paster_text("/* Comment */", "")
                else:
                    if item.property('fileExt') in ['xhtml', 'html', 'xml', 'opf', 'ncx']:
                        if selected_text.startswith('<!-- ') and selected_text.endswith(' -->'):
                            self.replace_text(selected_text[5:][:-4])
                        else:
                            self.replace_text('<!-- '+selected_text+' -->')
                    if item.property('fileExt') in ['css']:
                        if selected_text.startswith('/* ') and selected_text.endswith(' */'):
                            self.replace_text(selected_text[3:][:-3])
                        else:
                            self.replace_text('/* '+selected_text+' */')
            else:
                return
        except Exception:
            traceback.print_exc()

    def block_paster_text(self, block_start: str, block_end: str):
        try:
            item = self.currentWidget()
            tx_edit = item.children().__getitem__(2)
            # tx_edit = QPlainTextEdit()
            cursor = tx_edit.textCursor()

            # Security
            if cursor.hasSelection():
                selected_text = cursor.selection().toPlainText()
                start = cursor.position() - selected_text.__len__()
                end_text = block_start + selected_text + block_end
                # We insert the new text, which will override the selected
                # text
                cursor.insertText(end_text)
                cursor.setPosition(start)
                cursor.setPosition(start + len(end_text), QtGui.QTextCursor.KeepAnchor)

                # And set the new cursor
                tx_edit.setTextCursor(cursor)
            else:
                start = cursor.position()
                cursor.insertText(block_start + block_end)
                cursor.setPosition(start + len(block_start))
                tx_edit.setTextCursor(cursor)
            tx_edit.setFocus()
        except Exception:
            traceback.print_exc()

    def replace_text(self, new_text: str):
        try:
            item = self.currentWidget()
            tx_edit = item.children().__getitem__(2)
            # tx_edit = QPlainTextEdit()
            cursor = tx_edit.textCursor()

            # Security
            if cursor.hasSelection():
                start = cursor.position() - len(cursor.selection().toPlainText())
                print("selection")
                # We insert the new text, which will override the selected
                # text
                cursor.insertText(new_text)
                cursor.setPosition(start)
                cursor.setPosition(start + len(new_text), QtGui.QTextCursor.KeepAnchor)

                # And set the new cursor
                tx_edit.setTextCursor(cursor)
            tx_edit.setFocus()
        except Exception:
            traceback.print_exc()

    def block_list(self, list_type: str = 'ul'):  # list_type = ul or ol
        try:
            block_start = '<'+list_type+'>'
            block_end = '</'+list_type+'>'
            item = self.currentWidget()
            tx_edit = item.children().__getitem__(2)
            cursor = tx_edit.textCursor()

            if cursor.hasSelection() is False:
                cursor.insertText(block_start + '\n<li>ligne</li>\n' + block_end)
            else:
                selected_text = cursor.selection().toPlainText()
                start = cursor.position() - len(selected_text)
                selected_text = selected_text.replace('\t', '').replace('\r', '').replace('  ', ' ')
                selected_text = re.sub('\n{2,}', '\n', selected_text)
                selected_text = re.sub('\n[ ]{1,}\n', '\n', selected_text)
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
                    new_text += '\n' + block_end
                new_text = re.sub('\n{2,}', '\n', new_text)
                new_text = re.sub('\n[ ]{1,}\n', '\n', new_text)
                cursor.insertText(new_text)
                cursor.setPosition(start)
                cursor.setPosition(start + len(new_text), QtGui.QTextCursor.KeepAnchor)
                tx_edit.setTextCursor(cursor)
            tx_edit.setFocus()
        except Exception:
            traceback.print_exc()

    def prettify_text(self):
        try:
            item = self.currentWidget()
            tx_edit = item.children().__getitem__(2)
            # tx_edit = QPlainTextEdit()
            cursor = tx_edit.textCursor()
            end = cursor.position()
            start = end

            if item.property('fileExt') in ['xml', 'opf', 'ncx', 'xhtml', 'html']:  # 'xhtml', 'html'
                ret = xmlt.prettify(tx_edit.toPlainText())
                tx_edit.selectAll()
                tx_edit.textCursor().insertText(ret)
            elif item.property('fileExt') in ['css']:
                ret = css.prettifyCss(tx_edit.toPlainText())
                tx_edit.selectAll()
                tx_edit.textCursor().insertText(ret)
            else:
                dialog.WarnDialog('', 'File type not treated', self.parent())
                tx_edit.setFocus()
                return

            if cursor.hasSelection():
                start = end - len(cursor.selection().toPlainText())
                cursor.setPosition(start)
                cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
            else:
                cursor.setPosition(end)
            tx_edit.setTextCursor(cursor)
            tx_edit.setFocus()
        except Exception:
            traceback.print_exc()

    def link_poser(self):
        print("link_poser")
        block_start = '<a '
        block_end = '</a>'
        try:
            item = self.currentWidget()
            window = link.LinkWindow(self, app_user_directory + os.sep + 'editor' + os.sep + 'tmp' + os.sep + 'current')
            tx_edit = item.children().__getitem__(2)
            cursor = tx_edit.textCursor()

            tb1 = item.property('fileName').replace('/', os.sep).replace(
                app_user_directory + os.sep + 'editor' + os.sep + 'tmp' + os.sep + 'current' + os.sep,
                ''
            ).split(os.sep)
            adl = ''
            for i in range(0, len(tb1) - 1):
                adl += '../'

            new_text = ""
            if cursor.hasSelection() is False:
                ret = window.openExec()
                if ret is not None:
                    new_text = '<a href="' + adl + ret['url'] + '">' + ret['text'] + '</a>'
                    tx_edit.textCursor().insertText(new_text)
            else:
                selected_text = cursor.selection().toPlainText()
                # max_len = len(block_start) + len(block_end)
                if selected_text.startswith(block_start) and selected_text.endswith(block_end):
                    rez = re.findall('<a(.*)>(.*)</a>', selected_text)
                    new_text = rez[0][1]
                    tx_edit.textCursor().insertText(new_text)
                else:
                    if selected_text.startswith("http") or selected_text.startswith("file://") or selected_text.__contains__("/"):
                        ret = window.openExec(None, selected_text)
                    else:
                        ret = window.openExec(selected_text)
                    if ret is not None:
                        new_text = '<a href="' + adl + ret['url'] + '">' + ret['text'] + '</a>'
                        tx_edit.textCursor().insertText(new_text)

            end = cursor.position()
            start = end - len(new_text)
            cursor.setPosition(start)
            cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
            tx_edit.setTextCursor(cursor)
            tx_edit.setFocus()
        except Exception:
            traceback.print_exc()

    def img_poser(self):
        try:
            item = self.currentWidget()
            window = img.ImgWindow(self, app_user_directory + os.sep + 'editor' + os.sep + 'tmp' + os.sep + 'current')
            tx_edit = item.children().__getitem__(2)
            cursor = tx_edit.textCursor()
            selected_text = ""
            if cursor.hasSelection():
                selected_text = cursor.selection().toPlainText()
            ret = None
            if selected_text.startswith("http") or selected_text.startswith("file://") \
                    or selected_text.startswith("/") or selected_text.startswith("./") or selected_text.startswith("../"):
                ret = window.openExec(None, selected_text)
            else:
                ret = window.openExec(selected_text, None)
            if ret is not None:
                tb1 = item.property('fileName').replace('/', os.sep).replace(
                    app_user_directory + os.sep + 'editor' + os.sep + 'tmp' + os.sep + 'current' + os.sep,
                    ''
                ).split(os.sep)
                adl = ''
                for i in range(0, len(tb1)-1):
                    adl += '../'
                new_text = '<img src="' + adl + ret['url'] + '" alt="' + ret['text'] \
                           + '" title="' + ret['text'] + '" />'
                cursor.insertText(new_text)
                end = cursor.position()
                start = end - len(new_text)
                cursor.setPosition(start)
                cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
                tx_edit.setTextCursor(cursor)
                tx_edit.setFocus()
        except Exception:
            traceback.print_exc()
