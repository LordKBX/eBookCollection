# This Python file uses the following encoding: utf-8
import os, sys, traceback
from typing import Union
from PyQt5.QtWidgets import *
import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.uic
from PyQt5.uic import *

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import common.common
import common.files
import common.books
from vars import *


class SettingsWindow(QDialog):
    def __init__(self, parent, bdd):
        super(SettingsWindow, self).__init__(parent, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self.BDD = bdd
        PyQt5.uic.loadUi(app_directory + os.sep + 'home/settings.ui'.replace('/', os.sep), self)  # Load the .ui file
        self.lng = parent.lang  # language
        self.app_lang = self.BDD.get_param('lang')
        self.app_style = self.BDD.get_param('style')
        self.load_languages(self.app_lang)
        self.load_styles(self.app_style)
        self.apply_style()
        self.apply_translation()

        # self.dialog_tabs.setCurrentIndex(0)

        self.tab_global_lang_combo_box.currentIndexChanged.connect(self.change_language)
        self.tab_global_style_combo_box.currentIndexChanged.connect(self.change_style)

        self.tab_global_library_folder_btn.clicked.connect(self.change_library_folder)
        self.tab_global_library_folder_line_edit.setText(self.BDD.get_param('library/directory'))

        default_cover_background = self.BDD.get_param('defaultCover/background')
        default_cover_pattern = self.BDD.get_param('defaultCover/pattern')
        default_cover_pattern_color = self.BDD.get_param('defaultCover/pattern_color')
        default_cover_title = self.BDD.get_param('defaultCover/title')
        default_cover_series = self.BDD.get_param('defaultCover/series')
        default_cover_authors = self.BDD.get_param('defaultCover/authors')

        self.color_selectors = [
            'tab_metadata_default_cover_background_combo_box',
            # 'tab_metadata_default_cover_pattern_combo_box',
            'tab_metadata_default_cover_pattern_color_combo_box',
            'tab_metadata_default_cover_title_combo_box',
            'tab_metadata_default_cover_series_combo_box',
            'tab_metadata_default_cover_authors_combo_box'
        ]
        for id in self.color_selectors:
            selector_type = id.replace('tab_metadata_default_cover_', '').replace('_combo_box', '')
            combo = eval('self.'+id)
            # combo = QComboBox()
            model = combo.model()
            selected = 0
            nb = 0
            for color in env_vars['vars']['default_cover']['colors']:
                entry = PyQt5.QtGui.QStandardItem('█████')
                entry.setForeground(PyQt5.QtGui.QColor(color))
                entry.setData(color, 99)
                model.appendRow(entry)
                # print('color = ', color)
                # print('default_cover_' + selector_type + ' = ', eval('default_cover_'+selector_type))
                if color == eval('default_cover_'+selector_type):
                    selected = nb
                nb += 1
            # print('selected = ', selected)
            combo.setCurrentIndex(selected)
            combo.currentIndexChanged.connect(self.combo_changed)

        selected = 0
        nb = 0
        model = self.tab_metadata_default_cover_pattern_combo_box.model()
        for pattern in env_vars['vars']['default_cover']['patterns']:
            entry = PyQt5.QtGui.QStandardItem(pattern)
            entry.setData(pattern, 99)
            model.appendRow(entry)
            if pattern == default_cover_pattern:
                selected = nb
            nb += 1
        self.tab_metadata_default_cover_pattern_combo_box.setCurrentIndex(selected)
        self.tab_metadata_default_cover_pattern_combo_box.currentIndexChanged.connect(self.combo_changed)

        self.combo_changed()

        self.tab_about_btn_license.clicked.connect(lambda: os.system("start " + app_directory + os.sep + 'LICENSE'))
        self.tab_about_btn_website.clicked.connect(lambda: os.system("start " + app_directory + os.sep + 'LICENSE'))

    def open_exec(self):
        ret = self.exec_()  # Show the GUI
        if ret == 1:
            new_folder = self.tab_global_library_folder_line_edit.text()
            if self.BDD.get_param('library/directory') != new_folder:
                self.BDD.migrate(new_folder)
            data = {}
            return data
        else:
            self.lng.set_lang(self.app_lang)
            self.BDD.set_param('lang', self.app_lang)
            self.BDD.set_param('style', self.app_style)
            return None

    def change_library_folder(self):
        print("test")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.Directory

        dlg = QFileDialog()
        dlg.setOptions(options)
        dlg.setFileMode(QFileDialog.Directory)

        preset = self.BDD.get_param("library_directory").replace('{APP_DIR}', app_directory)
        folder = dlg.getExistingDirectory(self, "Choose Directory", preset).replace(app_directory, '{APP_DIR}')
        print(folder)
        self.tab_global_library_folder_line_edit.setText(folder)

    def load_languages(self, selected_lang: str = None):
        self.tab_global_lang_combo_box.clear()
        self.tab_global_lang_combo_box.addItem(self.lng['Settings']['LanguageAutomatic'])
        self.tab_global_lang_combo_box.setItemData(self.tab_global_lang_combo_box.count() - 1, 'auto', 99)
        languages = self.lng.get_langs()
        i = 1
        sel = 0
        for lg in languages:
            self.tab_global_lang_combo_box.addItem(lg['name'])
            self.tab_global_lang_combo_box.setItemData(self.tab_global_lang_combo_box.count() - 1,
                                                       lg['code'], 99)
            if selected_lang == lg['code']:
                sel = i
            i += 1
        self.tab_global_lang_combo_box.setCurrentIndex(sel)

    def load_styles(self, selected_style: str = None):
        self.tab_global_style_combo_box.clear()
        i = 0
        sel = 0
        for style in env_vars['styles']:
            st = self.lng['Settings/Style'+style]
            if st is None:
                st = style
            self.tab_global_style_combo_box.addItem(st)
            self.tab_global_style_combo_box.setItemData(self.tab_global_style_combo_box.count() - 1, style, 99)
            if selected_style == style:
                sel = i
            i += 1
        self.tab_global_style_combo_box.setCurrentIndex(sel)

    def change_language(self):
        index = self.tab_global_lang_combo_box.currentIndex()
        selected_lang = self.tab_global_lang_combo_box.itemData(index, 99)
        self.lng.set_lang(selected_lang)
        self.BDD.set_param('lang', selected_lang)
        self.apply_translation()

    def change_style(self):
        index = self.tab_global_style_combo_box.currentIndex()
        selected_style = self.tab_global_style_combo_box.itemData(index, 99)
        self.BDD.set_param('style', selected_style)
        self.apply_style(selected_style)

    def apply_translation(self):
        try:
            self.setWindowTitle(self.lng['Settings/WindowTitle'])
            self.button_box.button(QDialogButtonBox.Ok).setText(self.lng.get('Generic/DialogBtnSave'))
            self.button_box.button(QDialogButtonBox.Cancel).setText(self.lng.get('Generic/DialogBtnCancel'))

            # Tabs
            self.dialog_tabs.setTabText(0, self.lng['Settings/TabGlobalTitle'])
            self.dialog_tabs.setTabText(1, self.lng['Settings/TabMetadataTitle'])
            self.dialog_tabs.setTabText(2, self.lng['Settings/TabConversionTitle'])
            self.dialog_tabs.setTabText(3, self.lng['Settings/TabAboutTitle'])

            #   lang group
            self.tab_global_lang_group_box.setTitle(self.lng['Settings/LanguageTitle'])
            self.tab_global_lang_combo_box.setItemText(0, self.lng['Settings/LanguageAutomatic'])
            self.tab_global_lang_btn.setText(self.lng['Settings/Import'])

            #   style group
            self.tab_global_style_group_box.setTitle(self.lng['Settings/StyleTitle'])
            self.tab_global_style_import_btn.setText(self.lng['Settings/Import'])
            for id in range(0, self.tab_global_style_combo_box.count()):
                data = self.tab_global_style_combo_box.itemData(id, 99)
                st = self.lng["Settings/Style" + data]
                if st is None:
                    st = data
                self.tab_global_style_combo_box.setItemText(id, st)

            #   Library group
            self.tab_global_library_group_box.setTitle(self.lng['Settings/LibraryTitle'])
            self.tab_global_library_folder_label.setText(self.lng['Settings/LibraryFolder'])
            self.tab_global_library_folder_btn.setText(self.lng['Settings/LibraryFolderBrowse'])

        except Exception:
            traceback.print_exc()

    def apply_style(self, style: str = None):
        if style is None:
            style = self.BDD.get_param('style')
        cursor = QtGui.QCursor(QtCore.Qt.PointingHandCursor)
        self.setStyleSheet(env_vars['styles'][style]['dialog'])

        cls = self.__dir__()
        for var_name in cls:
            obj = eval('self.'+var_name)
            if isinstance(obj, (QPushButton, QComboBox)) and var_name not in ['tab_metadata_default_cover_preview']:
                obj.setCursor(cursor)
            if isinstance(obj, QWidget):
                obj.setStyleSheet(env_vars['styles'][style]['QTabWidget'])

        self.button_box.button(QDialogButtonBox.Ok).setStyleSheet(env_vars['styles'][style]['fullAltButton'])
        self.button_box.button(QDialogButtonBox.Ok).setCursor(cursor)
        self.button_box.button(QDialogButtonBox.Cancel).setStyleSheet(env_vars['styles'][style]['fullAltButton'])
        self.button_box.button(QDialogButtonBox.Cancel).setCursor(cursor)

        self.tab_global.setStyleSheet(env_vars['styles'][style]['dialog'])
        self.tab_metadata.setStyleSheet(env_vars['styles'][style]['dialog'])
        self.tab_conversion.setStyleSheet(env_vars['styles'][style]['dialog'])
        self.tab_about.setStyleSheet(env_vars['styles'][style]['dialog'])

    def combo_changed(self):
        vals = {
            'background': '',
            'pattern': '',
            'pattern_color': '',
            'title': '',
            'series': '',
            'authors': ''
        }
        for id in self.color_selectors:
            selector_type = id.replace('tab_metadata_default_cover_', '').replace('_combo_box', '')
            combo = eval('self.'+id)
            index = combo.currentIndex()
            color = combo.itemData(index, 99)
            vals[selector_type] = color
            combo.setStyleSheet("QComboBox:!editable {{ color: {}; }} QComboBox::down-arrow {{ image:none; width:0px; }}".format(color))

        vals['pattern'] = self.tab_metadata_default_cover_pattern_combo_box.currentData(99)
        cover = common.books.create_cover("TITRE", "auteur", "La série", 2, style=vals)
        print(cover)
        icon = PyQt5.QtGui.QIcon()
        icon.addPixmap(PyQt5.QtGui.QPixmap(cover, "png"))
        self.tab_metadata_default_cover_preview.setIcon(icon)
