# This Python file uses the following encoding: utf-8
import os, sys, traceback
from PyQt5.QtWidgets import *
import PyQt5.QtCore
import PyQt5.uic
from PyQt5.uic import *

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import common.common, common.files, common.qt
from vars import *


class SettingsWindow(QDialog):
    def __init__(self, parent, bdd):
        super(SettingsWindow, self).__init__(parent, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self.BDD = bdd
        PyQt5.uic.loadUi(app_directory + os.sep + 'home/settings.ui'.replace('/', os.sep), self)  # Load the .ui file
        self.lng = parent.lang  # language
        app_lang = self.BDD.getParam('lang')
        app_style = self.BDD.getParam('style')
        self.load_languages(app_lang)
        self.apply_translation()
        self.load_styles(app_style)
        self.apply_style()

        self.tab_global_lang_combo_box.currentIndexChanged.connect(self.change_language)
        self.tab_global_style_combo_box.currentIndexChanged.connect(self.change_style)

    def open_exec(self):
        ret = self.exec_()  # Show the GUI
        if ret == 1:
            data = {}
            return data
        else:
            return None

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
            print(selected_lang, lg['code'])
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
        self.BDD.setParam('lang', selected_lang)
        self.apply_translation()

    def change_style(self):
        index = self.tab_global_style_combo_box.currentIndex()
        selected_style = self.tab_global_style_combo_box.itemData(index, 99)
        self.BDD.setParam('style', selected_style)
        self.apply_style(selected_style)

    def apply_translation(self):
        try:
            self.setWindowTitle(self.lng['Settings/WindowTitle'])
            self.button_box.button(QDialogButtonBox.Ok).setText(self.lng.get('Generic/DialogBtnSave'))
            self.button_box.button(QDialogButtonBox.Cancel).setText(self.lng.get('Generic/DialogBtnCancel'))

            # Global
            self.dialog_tabs.setTabText(0, self.lng['Settings/TabGlobalTitle'])
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
        except Exception:
            traceback.print_exc()

    def apply_style(self, style: str = None):
        if style is None:
            style = self.BDD.getParam('style')

        self.setStyleSheet(env_vars['styles'][style]['dialog'])
        self.dialog_tabs.setStyleSheet(env_vars['styles'][style]['QTabWidget'])

        self.tab_global.setStyleSheet(env_vars['styles'][style]['dialog'])
        self.tab_metadata.setStyleSheet(env_vars['styles'][style]['dialog'])
        self.tab_conversion.setStyleSheet(env_vars['styles'][style]['dialog'])
        self.tab_about.setStyleSheet(env_vars['styles'][style]['dialog'])

        cursor = QtGui.QCursor(QtCore.Qt.PointingHandCursor)
        self.button_box.button(QDialogButtonBox.Ok).setStyleSheet(env_vars['styles'][style]['fullAltButton'])
        self.button_box.button(QDialogButtonBox.Ok).setCursor(cursor)
        self.button_box.button(QDialogButtonBox.Cancel).setStyleSheet(env_vars['styles'][style]['fullAltButton'])
        self.button_box.button(QDialogButtonBox.Cancel).setCursor(cursor)
