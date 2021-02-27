# This Python file uses the following encoding: utf-8
import os, sys, traceback
from PyQt5.QtWidgets import *
import PyQt5.uic
from PyQt5.uic import *

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import common.common, common.files, common.qt
from vars import *


class SettingsWindow(QDialog):
    def __init__(self, parent):
        super(SettingsWindow, self).__init__(parent, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        PyQt5.uic.loadUi(app_directory + os.sep + 'home/settings.ui'.replace('/', os.sep), self)  # Load the .ui file
        self.lng = parent.lang  # language
        self.load_languages()
        self.apply_translation()
        self.setStyleSheet(env_vars['styles']['black']['dialog']+env_vars['styles']['black']['QTabWidget'])
        self.dialog_tabs.setStyleSheet(env_vars['styles']['black']['QTabWidget'])
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setStyleSheet(
            env_vars['styles']['black']['fullAltButton'])
        self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setStyleSheet(
            env_vars['styles']['black']['fullAltButton'])

        self.tab_global_lang_combo_box.currentIndexChanged.connect(self.change_language)

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
        langs = self.lng.get_langs()
        for lg in langs:
            self.tab_global_lang_combo_box.addItem(lg['name'])
            self.tab_global_lang_combo_box.setItemData(self.tab_global_lang_combo_box.count() - 1,
                                                       lg['code'], 99)

    def change_language(self):
        print("langs")
        index = self.tab_global_lang_combo_box.currentIndex()
        selected_lang = self.tab_global_lang_combo_box.itemData(index, 99)
        self.lng.set_lang(selected_lang)
        self.apply_translation()

    def apply_translation(self):
        try:
            self.setWindowTitle(self.lng['Settings']['WindowTitle'])
            self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setText(self.lng['Generic']['DialogBtnSave'])
            self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText(self.lng['Generic']['DialogBtnCancel'])
            # Global
            self.dialog_tabs = QTabWidget()
            self.dialog_tabs.setTabText(0, self.lng['Settings']['TabGlobalTitle'])
            #   lang group
            self.tab_global_lang_group_box.setTitle(self.lng['Settings']['LanguageTitle'])
            self.tab_global_lang_combo_box.setItemText(0, self.lng['Settings']['LanguageAutomatic'])
            self.tab_global_lang_btn.setText(self.lng['Settings']['Import'])
            #   style group
            self.tab_global_style_group_box.setTitle(self.lng['Settings']['StyleTitle'])
            self.tab_global_style_combo_box.setItemText(0, self.lng['Settings']['StyleDark'])
            self.tab_global_style_combo_box.setItemText(1, self.lng['Settings']['StyleLight'])
            self.tab_global_style_import_btn.setText(self.lng['Settings']['Import'])
        except Exception:
            traceback.print_exc()
