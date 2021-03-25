import os, sys, traceback, json, subprocess
import concurrent.futures
import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtWidgets
from common.files import *
from common.common import *
from common.vars import *


class MetadataWindow:
    metadata_ui = None

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
        data = self.BDD.get_books(books_id)
        if len(data) <= 0:
            return
        try:
            print(data)
            style = self.BDD.get_param('style')
            self.metadata_ui = QtWidgets.QDialog(self, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
            PyQt5.uic.loadUi(
                os.path.dirname(os.path.realpath(__file__)) + os.sep + 'metadata.ui'.replace('/', os.sep),
                self.metadata_ui
            )
            uie = QtWidgets.QWidget()
            pa = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'text_edit.ui'.replace('/', os.sep)
            if os.path.isfile(pa) is False:
                pa = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'editor/text_edit.ui'.replace('/', os.sep)
            PyQt5.uic.loadUi(
                pa,
                uie
            )

            cursor = QtGui.QCursor(QtCore.Qt.PointingHandCursor)
            self.metadata_ui.setStyleSheet(get_style_var(style, 'QDialog'))
            self.metadata_ui.button_box.button(QtWidgets.QDialogButtonBox.Ok).setStyleSheet(get_style_var(style, 'fullAltButton'))
            self.metadata_ui.button_box.button(QtWidgets.QDialogButtonBox.Ok).setCursor(cursor)
            self.metadata_ui.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setStyleSheet(get_style_var(style, 'fullAltButton'))
            self.metadata_ui.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setCursor(cursor)
            self.metadata_ui.button_box.button(QtWidgets.QDialogButtonBox.Ok).setText(self.lang.get('Generic/DialogBtnSave'))
            self.metadata_ui.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText(self.lang.get('Generic/DialogBtnCancel'))

            self.metadata_window_cursor_layout(self.metadata_ui.gridLayout.layout(), cursor)

            self.metadata_ui.setWindowTitle(self.lang['Library/Metadata/WindowTitle'])
            self.metadata_ui.horizontalLayout_9.addWidget(uie)
            self.metadata_window_clear_layout(uie.horizon1)
            uie.setMinimumHeight(80)
            uie.setFixedHeight(80)
            uie.setStyleSheet(get_style_var(style, 'EditorEditPaneButtons') + 'QWidget{border:#ffffff px solid;}')

            if len(data) > 1:
                self.metadata_ui.edit_book_id.setText('MULTIPLE BOOK')
                self.metadata_ui.edit_book_id.setDisabled(True)
                self.metadata_ui.btn_find_book_id.setDisabled(True)
                self.metadata_ui.btn_generate_book_id.setDisabled(True)
            else:
                self.metadata_ui.edit_book_id.setText(data[0]['guid'])
                self.metadata_ui.btn_find_book_id.clicked.connect(self.metadata_window_find_guid)
                self.metadata_ui.btn_generate_book_id.clicked.connect(self.metadata_window_generate_guid)

                self.metadata_ui.edit_title.setText(data[0]['title'])
                self.metadata_ui.edit_authors.setText(data[0]['authors'])
                self.metadata_ui.edit_series.setText(data[0]['series'])
                self.metadata_ui.spin_volume.setValue(float(data[0]['series_vol']))

                self.metadata_ui.edit_editors.setText('')
                self.metadata_ui.edit_langs.setText('')
                self.metadata_ui.edit_plublish_date.setDate(QtCore.QDate.currentDate())

                self.metadata_ui.edit_import_date.setDate(self.metadata_window_unix_to_qdate(int(float(data[0]['import_date']))))

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