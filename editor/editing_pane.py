import os
import sys
import PyQt5.QtWebKitWidgets
import PyQt5.uic
from PyQt5.uic import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from syntaxHighlight import *
from common.books import *
from common import dialog, vars
import xmlt
import css
import link
import img


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

        self.previewWebview.page().settings().setUserStyleSheetUrl(QtCore.QUrl.fromLocalFile(self.tmpcss))
        self.previewWebview.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

    def content_update(self):
        if self.currentWidget().property('fileExt') in ['xhtml', 'html', 'css', 'xml', 'opf', 'ncx']:
            old_txt = self.currentWidget().property('originalContent')
            new_txt = self.currentWidget().children().__getitem__(2).text()

            index = self.currentIndex()
            if old_txt != new_txt:
                icon = QtGui.QIcon()
                image = QtGui.QPixmap()
                image.load(vars.get_style_var(self.style, 'icons/edit'))
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

    def create_pane(self, title: str, icon: str, path: str, parent, tmpcss: str = None):
        if self.lang is None:
            self.lang = parent.lang
            self.BDD = parent.BDD
            self.style = style = self.BDD.get_param('style')
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
            'text/plain',
            'image/jpeg', 'image/png', 'image/gif', 'image/bmp'
        ]
        if file_type == "application/octet-stream":
            try:
                file = open(path, "r", encoding="utf8")
                data = file.read()
                file.close()
                file_type = 'text/plain'
                is_text = True
            except Exception:
                ""

        if file_type not in list_type_ok:
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
            block.setStyleSheet(common.vars.get_style_var(style, 'EditorEditPaneButtons'))
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
                    text_edit = SimplePythonEditor(QsciLexerHTML(), tab, vars.env_vars['styles'][style])
                elif tab.property('fileExt') in ['xml', 'opf', 'ncx']:
                    text_edit = SimplePythonEditor(QsciLexerXML(), tab, vars.env_vars['styles'][style])
                elif tab.property('fileExt') in ['css']:
                    text_edit = SimplePythonEditor(QsciLexerCSS(), tab)
                else:
                    text_edit = SimplePythonEditor(None, tab, vars.env_vars['styles'][style])

                if text_edit.elexer is not None:
                    text_edit.setObjectName("textEdit")

                text_edit.setText(data)
                text_edit.textChanged.connect(lambda: self.content_update())

                vertical_layout.addWidget(text_edit)

                shortcut = QtWidgets.QShortcut(QtCore.Qt.ControlModifier | QtCore.Qt.Key_S, text_edit)
                shortcut.activated.connect(lambda: self.save_file(None))

                shortcut = QtWidgets.QShortcut(QtCore.Qt.ControlModifier | QtCore.Qt.Key_D, text_edit)
                shortcut.activated.connect(self.duplication)
            except Exception:
                traceback.print_exc()

        self.addTab(tab, QtGui.QIcon(QtGui.QPixmap(icon)), title)
        self.setTabsClosable(True)
        self.setCurrentIndex(self.count() - 1)

        try:
            block.btnSave.clicked.connect(self.save_file)
            block.btnUndo.clicked.connect(lambda: text_edit.undo())
            block.btnRedo.clicked.connect(lambda: text_edit.redo())
            block.btnCut.clicked.connect(lambda: text_edit.cut())
            block.btnCopy.clicked.connect(lambda: text_edit.copy())
            block.btnPaste.clicked.connect(lambda: text_edit.paste())
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

    def save_file(self, evt):
        try:
            item = self.currentWidget()
            new_text = item.children().__getitem__(2).text()
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
                ret = xmlt.parse(tx_edit.text())
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
                ret = xmlt.prettify(tx_edit.text())
                tx_edit.selectAll(True)
                tx_edit.replaceSelectedText(ret)
            elif item.property('fileExt') in ['css']:
                ret = css.prettifyCss(tx_edit.text())
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
            window = link.LinkWindow(self.parent(), app_directory + os.sep + 'editor' + os.sep + 'tmp'
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
            window = img.ImgWindow(self.parent(), app_directory + os.sep + 'editor' + os.sep + 'tmp' + os.sep + 'current')
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
