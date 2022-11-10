import os, sys, traceback, json, subprocess, base64, datetime, datetime, copy, re
import concurrent.futures
import urllib
import tempfile
import requests
import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtWidgets
from PyQt5 import QtWebKitWidgets
from PyQt5 import QtWebKit

from common.files import *
from common.common import *
from common.vars import *
from common.books import *
from common.dialog import *
import color_picker
import metadata_ui
import tags
import metadata_cover_download_ui
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'


class MetadataWindow(metadata_ui.Ui_Dialog):
    metadata_ui = None
    metadata_book_index = 0
    metadata_tmp_data = []
    metadata_start_data = []
    metadata_cover_icon_size = PyQt5.QtCore.QSize(160, 160)
    metadata_window_download_cover_dialog = None
    metadata_window_download_cover_clipboard = None

    def metadata_window_load(self) -> list:
        """
        load_metadata

        :return: void
        """
        print("Edit Metadata!")
        selection = self.central_block_table.selectedRanges()[0]
        selection = [selection.topRow(), selection.bottomRow()]
        print(selection)
        books_id = []
        for i in range(selection[0], selection[1]+1):
            books_id.append(self.central_block_table.item(i, 0).data(99))
        print('books_id=', books_id)
        self.metadata_start_data = self.BDD.get_books(books_id)
        self.metadata_tmp_data = copy.deepcopy(self.metadata_start_data)
        # print(self.metadata_tmp_data)
        if len(self.metadata_tmp_data) <= 0:
            return []
        try:
            style = self.BDD.get_param('style')

            self.metadata_ui = metadata_ui.Ui_Dialog()
            self.metadata_ui.parent = self
            self.metadata_ui.setupUi(self.metadata_ui)

            uie = QtWidgets.QWidget()
            pa = app_directory + os.sep + 'text_edit.ui'
            if os.path.isfile(pa) is False:
                pa = app_directory + os.sep + 'editor' + os.sep + 'text_edit.ui'
            PyQt5.uic.loadUi(pa, uie)

            cursor = QtGui.QCursor(QtCore.Qt.PointingHandCursor)
            self.metadata_ui.setStyleSheet(get_style_var(style, 'QDialog') + " " + get_style_var(style, 'QDialogTextSizeAlt'))
            self.metadata_ui.button_box.button(QtWidgets.QDialogButtonBox.Ok).setStyleSheet(get_style_var(style, 'fullAltButton'))
            self.metadata_ui.button_box.button(QtWidgets.QDialogButtonBox.Ok).setCursor(cursor)
            self.metadata_ui.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setStyleSheet(get_style_var(style, 'fullAltButton'))
            self.metadata_ui.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setCursor(cursor)
            self.metadata_ui.button_box.button(QtWidgets.QDialogButtonBox.Ok).setText(self.lang.get('Generic/DialogBtnSave'))
            self.metadata_ui.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText(self.lang.get('Generic/DialogBtnCancel'))

            self.metadata_window_cursor_layout(self.metadata_ui.gridLayout.layout(), cursor)

            self.metadata_ui.setWindowTitle(self.lang['Library/Metadata/WindowTitle'])
            self.metadata_ui.horizontalLayout_9.addWidget(uie)  # add text toolbar in window
            # hide useless buttons
            self.metadata_window_clear_layout(uie.horizon1)
            uie.btnImg.setVisible(False)
            uie.btnTextColor.setVisible(False)
            uie.btnBackColor.setVisible(False)
            uie.horizon2_1.layout().removeWidget(uie.btnImg)
            uie.setMinimumHeight(80)
            uie.setFixedHeight(80)
            uie.setStyleSheet(get_style_var(style, 'EditorEditPaneButtons') + 'QWidget{border:#ffffff px solid;}')

            if len(self.metadata_tmp_data) > 1:
                self.metadata_ui.edit_book_id.setText('MULTIPLE BOOK')
                self.metadata_ui.edit_book_id.setDisabled(True)
                self.metadata_ui.btn_find_book_id.setDisabled(True)
                self.metadata_ui.btn_generate_book_id.setDisabled(True)
                self.metadata_ui.edit_title.setText('MULTIPLE BOOK')
                self.metadata_ui.btn_del_title.setDisabled(True)
            else:
                self.metadata_ui.edit_book_id.setText(self.metadata_tmp_data[0]['guid'])
                self.metadata_ui.btn_find_book_id.clicked.connect(self.metadata_window_find_guid)
                self.metadata_ui.btn_generate_book_id.clicked.connect(self.metadata_window_generate_guid)
                self.metadata_ui.edit_title.setText(self.metadata_tmp_data[0]['title'])
                self.metadata_ui.btn_del_title.clicked.connect(lambda: self.metadata_ui.edit_title.setText(''))

            self.metadata_ui.edit_authors.setText(self.metadata_tmp_data[0]['authors'])
            self.metadata_ui.btn_del_authors.clicked.connect(lambda: self.metadata_ui.edit_authors.setText(''))

            self.metadata_ui.edit_series.setText(self.metadata_tmp_data[0]['series'])
            self.metadata_ui.spin_volume.setValue(float(self.metadata_tmp_data[0]['series_vol']))
            self.metadata_ui.btn_del_series.clicked.connect(self.metadata_window_clean_series)

            self.metadata_ui.edit_tags.setText(self.metadata_tmp_data[0]['tags'])
            self.metadata_ui.btn_tags.clicked.connect(lambda: self.metadata_window_edit_tags(self.metadata_ui.edit_tags))

            self.metadata_ui.btnCoverImport.clicked.connect(self.metadata_window_import_cover)
            self.metadata_ui.btnCoverDel.clicked.connect(self.metadata_window_delete_cover)
            self.metadata_ui.btnCoverGenerate.clicked.connect(self.metadata_window_generate_cover)
            self.metadata_ui.btnCoverDown.clicked.connect(self.metadata_window_download_cover)

            if len(self.metadata_tmp_data) > 1:
                self.metadata_ui.edit_editors.setText('')
                self.metadata_ui.edit_editors.setDisabled(True)
                self.metadata_ui.btn_del_editors.setDisabled(True)
                self.metadata_ui.edit_langs.setText('')
                self.metadata_ui.edit_langs.setDisabled(True)
                self.metadata_ui.btn_del_langs.setDisabled(True)
                self.metadata_ui.edit_plublish_date.setDate(QtCore.QDate.currentDate())
                self.metadata_ui.edit_plublish_date.setDisabled(True)
                self.metadata_ui.btn_del_plublish_date.setDisabled(True)
                self.metadata_ui.text_edit_synopsis.setText("")
                self.metadata_ui.text_edit_synopsis.setDisabled(True)
            else:
                icon = PyQt5.QtGui.QIcon()
                if self.metadata_tmp_data[0]['cover'] is not None and self.metadata_tmp_data[0]['cover'].strip() != '':
                    tbimg = self.metadata_tmp_data[0]['cover'].split(',')
                    by = PyQt5.QtCore.QByteArray()
                    by.fromBase64(tbimg[1].encode('utf-8'))
                    image = PyQt5.QtGui.QPixmap()
                    image.loadFromData(base64.b64decode(tbimg[1]))
                    icon.addPixmap(image, PyQt5.QtGui.QIcon.Normal, PyQt5.QtGui.QIcon.Off)
                    self.metadata_ui.label_cover_view.setToolTip("<img src='{}'/>".format(self.metadata_tmp_data[0]['cover']))
                else:
                    icon.addPixmap(PyQt5.QtGui.QPixmap(get_style_var(style, 'icons/book')),
                                   PyQt5.QtGui.QIcon.Normal, PyQt5.QtGui.QIcon.Off)
                # self.metadata_ui.label_cover_view = QtWidgets.QPushButton()
                self.metadata_ui.label_cover_view.setStyleSheet(
                    '*{border:0;padding:0;margin:0;background:transparent;height:'
                    + self.metadata_cover_icon_size.height().__str__() + 'px; width: '
                    + self.metadata_cover_icon_size.width().__str__() + 'px;}'
                )
                self.metadata_ui.label_cover_view.setIcon(icon)
                self.metadata_ui.label_cover_view.setIconSize(self.metadata_cover_icon_size)
                self.metadata_ui.label_cover_view.setMinimumSize(self.metadata_cover_icon_size)
                self.metadata_ui.label_cover_view.setFixedSize(self.metadata_cover_icon_size)

                # self.metadata_ui.text_edit_synopsis = QtWidgets.QTextEdit()
                self.metadata_ui.text_edit_synopsis.setAcceptRichText(True)
                self.metadata_ui.text_edit_synopsis.setText(self.metadata_tmp_data[0]['synopsis'])

                uie.btnBold.clicked.connect(lambda: self.metadata_window_synopsis_text_effect('bold'))
                uie.btnItalic.clicked.connect(lambda: self.metadata_window_synopsis_text_effect('italic'))
                uie.btnUnderline.clicked.connect(lambda: self.metadata_window_synopsis_text_effect('underline'))
                uie.btnStrikethrough.clicked.connect(lambda: self.metadata_window_synopsis_text_effect('strikethrough'))
                uie.btnSub.clicked.connect(lambda: self.metadata_window_synopsis_text_effect('sub'))
                uie.btnSup.clicked.connect(lambda: self.metadata_window_synopsis_text_effect('sup'))
                uie.btnAlignLeft.clicked.connect(lambda: self.metadata_window_synopsis_text_effect('align-left'))
                uie.btnAlignRight.clicked.connect(lambda: self.metadata_window_synopsis_text_effect('align-right'))
                uie.btnAlignCenter.clicked.connect(lambda: self.metadata_window_synopsis_text_effect('align-center'))
                uie.btnAlignJustify.clicked.connect(lambda: self.metadata_window_synopsis_text_effect('align-justify'))
                uie.btnList.clicked.connect(lambda: self.metadata_window_synopsis_text_effect('list'))
                uie.btnNumList.clicked.connect(lambda: self.metadata_window_synopsis_text_effect('list-numeric'))
                uie.btnLink.clicked.connect(lambda: self.metadata_window_synopsis_text_effect('link'))

                uie.btnTextColor.clicked.connect(lambda: self.metadata_window_synopsis_text_effect('color'))
                uie.btnBackColor.clicked.connect(lambda: self.metadata_window_synopsis_text_effect('background-color'))

                self.metadata_ui.edit_editors.setText('')
                self.metadata_ui.edit_langs.setText('')
                self.metadata_ui.edit_plublish_date.setDate(QtCore.QDate.currentDate())

                # self.metadata_ui.list_view_files = QtWidgets.QListWidget()
                self.metadata_ui.list_view_files.currentRowChanged.connect(lambda: self.metadata_window_file_list_index_changed())
                for file in self.metadata_tmp_data[0]['files']:
                    # print(file['guid'], file['size'], file['format'], file['link'], file['lang'], file['editors'], file['publication_date'])
                    item = QtWidgets.QListWidgetItem()
                    item.setText(file['format'] + " " + file['lang'] + " " + file['size'])
                    self.metadata_ui.list_view_files.addItem(item)
                self.metadata_ui.list_view_files.setCurrentRow(0)

            self.metadata_ui.edit_book_id.textChanged.connect(lambda: self.metadata_window_update_tmp_data('edit_book_id'))
            self.metadata_ui.edit_title.textChanged.connect(lambda: self.metadata_window_update_tmp_data('edit_title'))
            self.metadata_ui.edit_authors.textChanged.connect(lambda: self.metadata_window_update_tmp_data('edit_authors'))
            self.metadata_ui.edit_series.textChanged.connect(lambda: self.metadata_window_update_tmp_data('edit_series'))
            self.metadata_ui.edit_tags.textChanged.connect(lambda: self.metadata_window_update_tmp_data('edit_tags'))
            self.metadata_ui.text_edit_synopsis.textChanged.connect(lambda: self.metadata_window_update_tmp_data('text_edit_synopsis'))
            self.metadata_ui.spin_volume.valueChanged.connect(lambda: self.metadata_window_update_tmp_data('spin_volume'))

            self.metadata_ui.edit_editors.textChanged.connect(lambda: self.metadata_window_update_tmp_data('edit_editors'))
            self.metadata_ui.edit_langs.textChanged.connect(lambda: self.metadata_window_update_tmp_data('edit_langs'))
            self.metadata_ui.edit_plublish_date.dateTimeChanged.connect(lambda: self.metadata_window_update_tmp_data('edit_plublish_date'))

            ret = self.metadata_ui.exec_()
            if ret == 1:
                print('OK')
                bookno = -1
                multi = False
                if len(self.metadata_tmp_data) > 1:
                    multi = True
                for book in self.metadata_tmp_data:
                    bookno += 1
                    for index in book:
                        start_id = self.metadata_start_data[bookno]['guid']
                        if index == 'files':
                            ''
                        else:
                            if multi is True:
                                if index in ["guid", "title", "import_date"]:
                                    continue
                            if self.metadata_start_data[bookno][index] != book[index]:
                                self.BDD.update_book(start_id, index, book[index])
                return self.metadata_tmp_data
            else:
                return []
        except Exception:
            traceback.print_exc()
            return []

    def metadata_window_edit_tags(self, source: object):
        try:
            text = ""
            if isinstance(source, QtWidgets.QLineEdit):
                text = source.text()
            elif isinstance(source, QtWidgets.QTableWidgetItem):
                text = source.text()
            else:
                return
            tagsui = tags.TagsWindow(self.metadata_ui, text)
            ret = tagsui.exec_()
            if ret == 1:
                print("OK")
                tagsret = tagsui.prettyTags()
                self.metadata_ui.edit_tags.setText(tagsret)
            else:
                print("Cancel")
        except Exception:
            traceback.print_exc()

    def metadata_window_clear_layout(self, layout: QtWidgets.QLayout) -> None:
        if layout is None:
            return
        r = []
        i = layout.count()
        while i > 0:
            i -= 1
            r.append(i)

        for i in r:
            child = layout.itemAt(i)
            # print(child)
            if isinstance(child, QtWidgets.QWidgetItem):
                try:
                    child.widget().setVisible(False)
                    layout.removeWidget(child.widget())
                    # child.widget().deleteLater()
                except Exception:
                    traceback.print_exc()
            elif isinstance(child, QtWidgets.QSpacerItem):
                layout.removeItem(child)
            elif isinstance(child, (QtWidgets.QLayoutItem, QtWidgets.QHBoxLayout)):
                self.metadata_window_clear_layout(child)
                layout.removeItem(child)
            del child

    def metadata_window_cursor_layout(self, layout: QtWidgets.QLayout, cursor: QtGui.QCursor) -> None:
        try:
            if layout is None:
                return
            r = []
            i = layout.count()
            while i > 0:
                i -= 1
                r.append(i)

            for i in r:
                child = layout.itemAt(i)
                # print(child)
                if isinstance(child, QtWidgets.QWidgetItem):
                    try:
                        if isinstance(child.widget(), QtWidgets.QPushButton):
                            if child.widget().objectName() == 'label_cover_view':
                                continue
                            child.widget().setCursor(cursor)
                    except Exception:
                        traceback.print_exc()
                elif isinstance(child, QtWidgets.QSpacerItem):
                    ''
                elif isinstance(child, (QtWidgets.QLayoutItem, QtWidgets.QHBoxLayout, QtWidgets.QVBoxLayout, QtWidgets.QGridLayout)):
                    self.metadata_window_cursor_layout(child, cursor)
                del child
        except Exception:
            traceback.print_exc()

    def metadata_window_find_guid(self) -> str:
        print('metadata_window_find_guid')
        bguid = self.metadata_tmp_data[0]['guid']
        title = self.metadata_tmp_data[0]['title']
        series = self.metadata_tmp_data[0]['series']
        link = self.metadata_tmp_data[0]['files'][0]['link']
        editors = self.metadata_tmp_data[0]['files'][0]['editors']

        return ''

    def metadata_window_generate_guid(self) -> None:
        print('metadata_window_generate_guid')
        guid = uuid.uuid4().__str__()
        print(guid)
        self.metadata_ui.edit_book_id.setText(guid)

    def metadata_window_unix_to_qdate(self, unix_time: int) -> QtCore.QDateTime:
        print('metadata_window_unix_to_qdate')
        process = QtCore.QDateTime()
        process.setTime_t(unix_time)
        return process.date()

    def metadata_window_clean_series(self) -> None:
        self.metadata_ui.edit_series.setText('')
        self.metadata_ui.spin_volume.setValue(0.0)

    def metadata_window_synopsis_text_effect(self, effect: str) -> None:
        try:
            print('metadata_window_synopsis_text_effect: ', effect)
            if self.metadata_ui is None:
                self.metadata_ui.text_edit_synopsis = QtWidgets.QTextEdit()
            sel = self.metadata_ui.text_edit_synopsis.textCursor()
            tx = sel.selectedText()

            st = '<!--StartFragment-->'
            et = '<!--EndFragment-->'
            bc = sel.selection().toHtml()
            html = bc[bc.index(st)+len(st):bc.index(et)]
            if tx is not None:
                tx = tx.strip()
            line = sel.blockNumber() + 1
            col = sel.columnNumber()
            print('tx=', tx)
            print('html=', html)

            if effect == 'bold':
                if self.metadata_ui.text_edit_synopsis.fontWeight() == QtGui.QFont.Bold:
                    self.metadata_ui.text_edit_synopsis.setFontWeight(QtGui.QFont.Normal)
                else:
                    self.metadata_ui.text_edit_synopsis.setFontWeight(QtGui.QFont.Bold)

            elif effect == 'italic':
                self.metadata_ui.text_edit_synopsis.setFontItalic(not self.metadata_ui.text_edit_synopsis.fontItalic())

            elif effect == 'underline':
                self.metadata_ui.text_edit_synopsis.setFontUnderline(not self.metadata_ui.text_edit_synopsis.fontUnderline())

            elif effect == 'strikethrough':
                cchf = self.metadata_ui.text_edit_synopsis.currentCharFormat()
                cchf.setFontStrikeOut(not cchf.fontStrikeOut())
                self.metadata_ui.text_edit_synopsis.setCurrentCharFormat(cchf)

            elif effect == 'sub' or effect == 'sup':
                cchf = self.metadata_ui.text_edit_synopsis.currentCharFormat()
                align = cchf.verticalAlignment()
                if align == QtGui.QTextCharFormat.AlignNormal:
                    if effect == 'sub':
                        cchf.setVerticalAlignment(QtGui.QTextCharFormat.AlignSubScript)
                    else:
                        cchf.setVerticalAlignment(QtGui.QTextCharFormat.AlignSuperScript)
                else:
                    cchf.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)
                self.metadata_ui.text_edit_synopsis.setCurrentCharFormat(cchf)

            elif effect.startswith('align-'):
                if effect.startswith('align-left'):
                    self.metadata_ui.text_edit_synopsis.setAlignment(QtCore.Qt.AlignLeft)
                elif effect.startswith('align-right'):
                    self.metadata_ui.text_edit_synopsis.setAlignment(QtCore.Qt.AlignRight)
                elif effect.startswith('align-center'):
                    self.metadata_ui.text_edit_synopsis.setAlignment(QtCore.Qt.AlignCenter)
                elif effect.startswith('align-justify'):
                    self.metadata_ui.text_edit_synopsis.setAlignment(QtCore.Qt.AlignJustify)

            elif effect == 'list' or effect == 'list-numeric':
                if sel.currentList() is None:
                    if effect == 'list':
                        sel.insertList(QtGui.QTextListFormat.ListDisc)
                    else:
                        sel.insertList(QtGui.QTextListFormat.ListDecimal)
                else:
                    liste = sel.currentList()
                    paragraphs = []
                    for i in range(0, liste.count()):
                        paragraphs.append(liste.item(i).text())
                    sel.select(QtGui.QTextCursor.BlockUnderCursor)
                    sel.removeSelectedText()
                    self.metadata_ui.text_edit_synopsis.textCursor().insertText("\n".join(paragraphs))

            elif effect == 'link':
                if tx is None:
                    return
                val = None
                if html.__contains__('<a '):
                    val = html[html.index('href="')+6:]
                    val = val[:val.index('"')]
                link = InputDialog('test', 'link', parent=self.metadata_ui, value=val)
                if link is not None:
                    link = link.strip()
                    linkt = link.lower()
                    ok = False
                    for tpl in ['file://', 'http://', 'https://', 'ftp://', 'sftp://', 'ftps://', './', '../']:
                        if linkt.startswith(tpl):
                            ok = True
                            break
                    if ok is True:
                        sel.removeSelectedText()
                        sel.insertHtml('<a href="' + link + '">' + tx + '</a>')

            elif effect == 'color' or effect == 'background-color':
                if tx is None:
                    return
                if effect == 'color':
                    color = color_picker.ColorPicker(self).getColor(self.metadata_ui.text_edit_synopsis.textColor())
                elif effect == 'background-color':
                    color = color_picker.ColorPicker(self).getColor(self.metadata_ui.text_edit_synopsis.textBackgroundColor())
                if color is None:
                    return

                if effect == 'color':
                    self.metadata_ui.text_edit_synopsis.setTextColor(color)
                elif effect == 'background-color':
                    self.metadata_ui.text_edit_synopsis.setTextBackgroundColor(color)

            self.metadata_ui.text_edit_synopsis.setFocus()
        except Exception:
            traceback.print_exc()

    def metadata_window_file_list_index_changed(self) -> None:
        try:
            line = self.metadata_ui.list_view_files.currentRow()
            file = self.metadata_tmp_data[0]['files'][line]

            print(file['guid'], file['size'], file['format'], file['link'], file['lang'], file['editors'], file['publication_date'])
            if file['editors'] is None:
                self.metadata_ui.edit_editors.setText("")
            else:
                self.metadata_ui.edit_editors.setText(file['editors'])
            if file['lang'] is None:
                self.metadata_ui.edit_langs.setText("")
            else:
                self.metadata_ui.edit_langs.setText(file['lang'])
            # publication_date
            self.metadata_ui.edit_plublish_date.setDate(datetime.date.fromtimestamp(file['publication_date']))
        except Exception:
            traceback.print_exc()

    def metadata_window_update_tmp_data(self, source: str) -> None:
        try:
            ar1 = ['edit_book_id', 'edit_title', 'edit_authors', 'edit_series', 'edit_tags', 'text_edit_synopsis', 'spin_volume']
            rar1 = ['guid', 'title', 'authors', 'series', 'tags', 'synopsis', 'series_vol']

            ar2 = ['edit_editors', 'edit_langs', 'edit_plublish_date']
            rar2 = ['editors', 'lang', 'publication_date']

            if len(self.metadata_tmp_data) > 1:
                if source in ar1:
                    obj = getattr(self.metadata_ui, ar1[ar1.index(source)])
                    if 'spin' in source:
                        start = float(obj.value())
                        for i in range(0, len(self.metadata_tmp_data)):
                            self.metadata_tmp_data[i][rar1[ar1.index(source)]] = start + i
                    else:
                        for i in range(0, len(self.metadata_tmp_data)):
                            self.metadata_tmp_data[i][rar1[ar1.index(source)]] = obj.text()
            else:
                if source in ar1:
                    obj = getattr(self.metadata_ui, ar1[ar1.index(source)])
                    if 'spin' in source:
                        self.metadata_tmp_data[0][rar1[ar1.index(source)]] = obj.value()
                    else:
                        self.metadata_tmp_data[0][rar1[ar1.index(source)]] = obj.text()
                elif source in ar2:
                    Fileline = self.metadata_ui.list_view_files.currentRow()
                    file = self.metadata_tmp_data[0]['files'][Fileline]
                    if 'date' in source:
                        obj = QtWidgets.QDateEdit(getattr(self.metadata_ui, ar2[ar2.index(source)]))
                        # self.metadata_ui.edit_plublish_date = QtWidgets.QDateEdit()
                        self.metadata_tmp_data[0]['files'][Fileline][rar2[ar2.index(source)]] = \
                            datetime.datetime.fromisoformat(obj.date().toPyDate().strftime('%Y-%m-%d %H:%M:%S'))\
                                .replace(tzinfo=datetime.timezone.utc).timestamp()
                    else:
                        obj = QtWidgets.QLineEdit(getattr(self.metadata_ui, ar2[ar2.index(source)]))
                        self.metadata_tmp_data[0]['files'][Fileline][rar2[ar2.index(source)]] = obj.text()

            # print(self.metadata_tmp_data)
        except Exception:
            traceback.print_exc()

    def metadata_window_delete_cover(self) -> None:
        try:
            self.metadata_tmp_data[0]['cover'] = None

            icon = PyQt5.QtGui.QIcon()
            icon.addPixmap(PyQt5.QtGui.QPixmap(get_style_var(self.BDD.get_param('style'), 'icons/book')),
                           PyQt5.QtGui.QIcon.Normal, PyQt5.QtGui.QIcon.Off)

            self.metadata_ui.label_cover_view.setStyleSheet(
                '*{border:0;padding:0;margin:0;background:transparent;height:'
                + self.metadata_cover_icon_size.height().__str__() + 'px; width: '
                + self.metadata_cover_icon_size.width().__str__() + 'px;}'
            )
            self.metadata_ui.label_cover_view.setIcon(icon)
            self.metadata_ui.label_cover_view.setIconSize(self.metadata_cover_icon_size)
            self.metadata_ui.label_cover_view.setMinimumSize(self.metadata_cover_icon_size)
            self.metadata_ui.label_cover_view.setFixedSize(self.metadata_cover_icon_size)
        except Exception as err:
            traceback.print_exc()

    def metadata_window_generate_cover(self) -> None:
        try:
            fd, tmp_file = tempfile.mkstemp()
            style = {
                "background": self.BDD.get_param('defaultCover/background', "#ffffff"),
                "pattern": self.BDD.get_param('defaultCover/pattern', "01"),
                "pattern_color": self.BDD.get_param('defaultCover/pattern_color', '#000000'),
                "title": self.BDD.get_param('defaultCover/title', "#000000"),
                "series": self.BDD.get_param('defaultCover/series', "#0000ff"),
                "authors": self.BDD.get_param('defaultCover/authors', "#000000"),
            }

            create_cover(
                self.metadata_tmp_data[0]['title'],
                self.metadata_tmp_data[0]['authors'],
                self.metadata_tmp_data[0]['series'],
                self.metadata_tmp_data[0]['series_vol'],
                tmp_file, style
                )

            icon = PyQt5.QtGui.QIcon()
            cover = common.books.create_thumbnail(tmp_file)
            if cover is not None and cover.strip() != '':
                tbimg = cover.split(',')
                image = PyQt5.QtGui.QPixmap()
                image.loadFromData(base64.b64decode(tbimg[1]))
                icon.addPixmap(image, PyQt5.QtGui.QIcon.Normal, PyQt5.QtGui.QIcon.Off)
                self.metadata_ui.label_cover_view.setToolTip("<img src='{}'/>".format(cover))
            else: # book
                icon.addPixmap(PyQt5.QtGui.QPixmap(get_style_var(self.BDD.get_param('style'), 'icons/book')), PyQt5.QtGui.QIcon.Normal, PyQt5.QtGui.QIcon.Off)

            self.metadata_tmp_data[0]['cover'] = cover

            self.metadata_ui.label_cover_view.setStyleSheet(
                '*{border:0;padding:0;margin:0;background:transparent;height:'
                + self.metadata_cover_icon_size.height().__str__() + 'px; width: '
                + self.metadata_cover_icon_size.width().__str__() + 'px;}'
            )
            self.metadata_ui.label_cover_view.setIcon(icon)
            self.metadata_ui.label_cover_view.setIconSize(self.metadata_cover_icon_size)
            self.metadata_ui.label_cover_view.setMinimumSize(self.metadata_cover_icon_size)
            self.metadata_ui.label_cover_view.setFixedSize(self.metadata_cover_icon_size)
        except Exception as err:
            traceback.print_exc()

    def metadata_window_import_cover(self) -> None:
        try:
            options = QtWidgets.QFileDialog.Options()
            # options |= PyQt5.QFileDialog.DontUseNativeDialog
            fname = QtWidgets.QFileDialog.getOpenFileName(
                self.metadata_ui, self.lang['Library/Metadata/CoverImport'], self.BDD.get_param('library/lastOpenDir'),
                "Image (*.bmp *.jpg *.jpeg *.png)",
                options=options
            )
            if isinstance(fname, tuple):
                selected_directory = fname[0].replace('/', os.sep)
                selected_index = selected_directory.rindex("" + os.sep)
                selected_directory = selected_directory[0:selected_index]
                self.BDD.set_param('library/lastOpenDir', selected_directory)
                cover = common.books.create_thumbnail(fname[0])

                icon = PyQt5.QtGui.QIcon()
                if cover is not None and cover.strip() != '':
                    tbimg = cover.split(',')
                    image = PyQt5.QtGui.QPixmap()
                    image.loadFromData(base64.b64decode(tbimg[1]))
                    icon.addPixmap(image, PyQt5.QtGui.QIcon.Normal, PyQt5.QtGui.QIcon.Off)
                    self.metadata_ui.label_cover_view.setToolTip("<img src='{}'/>".format(cover))
                else: # book
                    icon.addPixmap(PyQt5.QtGui.QPixmap(get_style_var(self.BDD.get_param('style'), 'icons/book')), PyQt5.QtGui.QIcon.Normal, PyQt5.QtGui.QIcon.Off)
                # self.metadata_ui.label_cover_view = QtWidgets.QPushButton()
                self.metadata_ui.label_cover_view.setStyleSheet(
                    '*{border:0;padding:0;margin:0;background:transparent;height:'
                    + self.metadata_cover_icon_size.height().__str__() + 'px; width: '
                    + self.metadata_cover_icon_size.width().__str__() + 'px;}'
                )
                self.metadata_ui.label_cover_view.setIcon(icon)
                self.metadata_ui.label_cover_view.setIconSize(self.metadata_cover_icon_size)
                self.metadata_ui.label_cover_view.setMinimumSize(self.metadata_cover_icon_size)
                self.metadata_ui.label_cover_view.setFixedSize(self.metadata_cover_icon_size)
                self.metadata_tmp_data[0]['cover'] = cover
        except Exception as err:
            traceback.print_exc()

    def metadata_window_download_cover(self) -> None:
        try:
            search_string = self.metadata_tmp_data[0]['title']
            if self.metadata_tmp_data[0]['series'] is not None and self.metadata_tmp_data[0]['series'] != '':
                search_string += " " + self.metadata_tmp_data[0]['series']
                search_string += " vol{}".format(self.metadata_tmp_data[0]['series_vol'])
            if self.metadata_tmp_data[0]['authors'] is not None and self.metadata_tmp_data[0]['authors'] != '':
                search_string += " " + self.metadata_tmp_data[0]['authors']
            if self.metadata_window_download_cover_dialog is not None:
                self.metadata_window_download_cover_dialog.close()
                self.metadata_window_download_cover_dialog = None
            else:
                self.metadata_window_download_cover_dialog = metadata_cover_download_ui.Ui_Dialog()
            down_ui = self.metadata_window_download_cover_dialog
            down_ui.setupUi(down_ui)
            down_ui.lineEdit.setText("")

            url = "https://www.google.com/search?tbm=isch&q="+urllib.parse.quote(search_string, safe='')
            ## from this tutorial
            request = QtWebKit.QNetworkRequest()
            request.setUrl(QtCore.QUrl(url))
            request.setRawHeader("User-Agent", USER_AGENT)

            down_ui.webView.page().userAgentForUrl = USER_AGENT
            down_ui.webView.setUrl(QtCore.QUrl("https://www.google.com/search?tbm=isch&q="+urllib.parse.quote(search_string, safe='')))
            if self.metadata_window_download_cover_clipboard is not None:
                self.metadata_window_download_cover_clipboard.clear()
                self.metadata_window_download_cover_clipboard = None
            self.metadata_window_download_cover_clipboard = QtGui.QGuiApplication.clipboard()
            self.metadata_window_download_cover_clipboard.changed.connect(self.metadata_window_download_cover_clipboard_update)

            ret = down_ui.exec_()
            if ret == 1:
                print('OK')
                return_url = down_ui.lineEdit.text()
                print(return_url)
                response = requests.get(return_url)
                fd, tmp_file = tempfile.mkstemp()
                with open(tmp_file, "wb") as ob:
                    ob.write(response.content)

                cover = common.books.create_thumbnail(tmp_file)

                icon = PyQt5.QtGui.QIcon()
                if cover is not None and cover.strip() != '':
                    tbimg = cover.split(',')
                    image = PyQt5.QtGui.QPixmap()
                    image.loadFromData(base64.b64decode(tbimg[1]))
                    icon.addPixmap(image, PyQt5.QtGui.QIcon.Normal, PyQt5.QtGui.QIcon.Off)
                    self.metadata_ui.label_cover_view.setToolTip("<img src='{}'/>".format(cover))
                    self.metadata_ui.label_cover_view.setStyleSheet(
                        '*{border:0;padding:0;margin:0;background:transparent;height:'
                        + self.metadata_cover_icon_size.height().__str__() + 'px; width: '
                        + self.metadata_cover_icon_size.width().__str__() + 'px;}'
                    )
                    self.metadata_ui.label_cover_view.setIcon(icon)
                    self.metadata_ui.label_cover_view.setIconSize(self.metadata_cover_icon_size)
                    self.metadata_ui.label_cover_view.setMinimumSize(self.metadata_cover_icon_size)
                    self.metadata_ui.label_cover_view.setFixedSize(self.metadata_cover_icon_size)
                    self.metadata_tmp_data[0]['cover'] = cover
                else:
                    ErrorDialog(
                        self.translation['Library/Metadata/CoverDownloadErrorTitle'],
                        self.translation['Library/Metadata/CoverDownloadErrorMessage2'],
                        self.metadata_ui)

        except Exception as err:
            traceback.print_exc()
            ErrorDialog(
                self.translation['Library/Metadata/CoverDownloadErrorTitle'],
                self.translation['Library/Metadata/CoverDownloadErrorMessage1'],
                self.metadata_ui)

    def metadata_window_download_cover_clipboard_update(self, mode: QtGui.QClipboard.Mode):
        excluding_starting_block_urls = ["https://www.google.com/url?esrc="]
        excluding_regexp_block_urls = ["https://www.google.com/url?(.*)&url="]
        self.metadata_window_download_cover_clipboard = QtGui.QGuiApplication.clipboard()
        data = None
        if mode == QtGui.QClipboard.FindBuffer: return
        dtype = self.metadata_window_download_cover_clipboard.mimeData(mode)

        if dtype.hasImage() is True: data = self.metadata_window_download_cover_clipboard.image(mode)
        elif dtype.hasHtml() is True:
            print("html")
            data = self.metadata_window_download_cover_clipboard.text(mode)
        elif dtype.hasUrls() is True:
            print("url")
            data = self.metadata_window_download_cover_clipboard.text(mode)
        elif dtype.hasText() is True:
            print("text")
            data = self.metadata_window_download_cover_clipboard.text(mode)
            tdata = self.metadata_window_download_cover_strip_html(data)
            if (tdata is None or tdata == '') and 'data:image/' in data:
                m = re.search('"data\:image\/(.*)"', data)
                data = m.group(0).replace('"')
            else: data = tdata
            for stbu in excluding_starting_block_urls:
                if data.startswith(stbu) is True:
                    return

        for rpl in excluding_regexp_block_urls:
            data = re.sub(rpl, '', data)

        print(data)
        self.metadata_window_download_cover_dialog.lineEdit.setText(data)

    def metadata_window_download_cover_strip_html(self, text: str):
        doc = QtGui.QTextDocument()
        doc.setHtml(text)
        return doc.toPlainText().strip()
