import os, sys, traceback, json, subprocess, base64, datetime
import concurrent.futures
import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtWidgets

from common.files import *
from common.common import *
from common.vars import *
from common.dialog import *
import color_picker


class MetadataWindow:
    metadata_ui = None
    metadata_file_index = 0
    metadata_book_index = 0
    metadata_tmp_data = {}

    def metadata_window_load(self) -> None:
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
        self.metadata_tmp_data = self.BDD.get_books(books_id)
        print(self.metadata_tmp_data)
        if len(self.metadata_tmp_data) <= 0:
            return
        try:
            style = self.BDD.get_param('style')
            self.metadata_ui = QtWidgets.QDialog(self, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
            PyQt5.uic.loadUi(app_directory + os.sep + 'metadata.ui'.replace('/', os.sep), self.metadata_ui)
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
                icon_size = PyQt5.QtCore.QSize(160, 160)
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
                    icon.addPixmap(PyQt5.QtGui.QPixmap(self.app_directory + '/ressources/icons/white/book.png'),
                                   PyQt5.QtGui.QIcon.Normal, PyQt5.QtGui.QIcon.Off)
                # self.metadata_ui.label_cover_view = QtWidgets.QPushButton()
                self.metadata_ui.label_cover_view.setStyleSheet(
                    '*{border:0;padding:0;margin:0;background:transparent;height:'
                    + icon_size.height().__str__() + 'px; width: '
                    + icon_size.width().__str__() + 'px;}'
                )
                self.metadata_ui.label_cover_view.setIcon(icon)
                self.metadata_ui.label_cover_view.setIconSize(icon_size)
                self.metadata_ui.label_cover_view.setMinimumSize(icon_size)
                self.metadata_ui.label_cover_view.setFixedSize(icon_size)

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
                    item.setData(90, file['guid'])
                    item.setData(91, file['size'])
                    item.setData(92, file['format'])
                    item.setData(93, file['link'])
                    item.setData(94, file['lang'])
                    item.setData(95, file['editors'])
                    item.setData(96, file['publication_date'])
                    self.metadata_ui.list_view_files.addItem(item)
                self.metadata_ui.list_view_files.setCurrentRow(0)


            ret = self.metadata_ui.exec_()
            if ret == 1:
                print('OK')
        except Exception:
            traceback.print_exc()

    def metadata_window_clear_layout(self, layout: QtWidgets.QLayout):
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

    def metadata_window_cursor_layout(self, layout: QtWidgets.QLayout, cursor: QtGui.QCursor):
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

    def metadata_window_find_guid(self):
        print('metadata_window_find_guid')

    def metadata_window_generate_guid(self):
        print('metadata_window_generate_guid')
        guid = uuid.uuid4().__str__()
        print(guid)
        self.metadata_ui.edit_book_id.setText(guid)

    def metadata_window_unix_to_qdate(self, unix_time: int):
        print('metadata_window_unix_to_qdate')
        process = QtCore.QDateTime()
        process.setTime_t(unix_time)
        return process.date()

    def metadata_window_clean_series(self):
        self.metadata_ui.edit_series.setText('')
        self.metadata_ui.spin_volume.setValue(0.0)

    def metadata_window_synopsis_text_effect(self, effect: str):
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

    def metadata_window_file_list_index_changed(self):
        try:
            line = self.metadata_ui.list_view_files.currentRow()
            item = self.metadata_ui.list_view_files.item(line)
            print(item.data(90), item.data(91), item.data(92), item.data(93), item.data(94), item.data(95), item.data(96))
            if item.data(95) is None:
                self.metadata_ui.edit_editors.setText("")
            else:
                self.metadata_ui.edit_editors.setText(item.data(95))
            if item.data(94) is None:
                self.metadata_ui.edit_langs.setText("")
            else:
                self.metadata_ui.edit_langs.setText(item.data(94))
            # publication_date
            datetime.date.fromtimestamp(item.data(96))
            self.metadata_ui.edit_plublish_date.setDate(datetime.date.fromtimestamp(item.data(96)))

        except Exception:
            traceback.print_exc()

    def metadata_window_update_tmp_data(self):
        ""
