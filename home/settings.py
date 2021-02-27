# This Python file uses the following encoding: utf-8
import os, sys, re, json
from PyQt5.QtWidgets import *
import PyQt5.uic
from PyQt5.uic import *

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import lang
import common.common, common.files, common.qt
from vars import *


class SettingsWindow(QDialog):
    def __init__(self, parent):
        super(SettingsWindow, self).__init__(parent, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        PyQt5.uic.loadUi(app_directory + os.sep + 'home/settings.ui'.replace('/', os.sep), self)  # Load the .ui file
        self.lng = parent.lang  # language
        self.load_languages()
        self.apply_translation()
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setStyleSheet(env_vars['styles']['black']['fullAltButton'])
        self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setStyleSheet(env_vars['styles']['black']['fullAltButton'])

        self.tab_global_lang_selection_combo_box = QComboBox()
        self.tab_global_lang_selection_combo_box.currentIndexChanged.connect(self.change_language)

    def open_exec(self):
        ret = self.exec_()  # Show the GUI
        if ret == 1:
            data = {}
            return data
        else:
            return None

    def load_languages(self, selected_lang: str = None):
        self.tab_global_lang_selection_combo_box.clear()
        self.tab_global_lang_selection_combo_box.addItem(self.lng['Settings']['languageAutomatic'])
        self.tab_global_lang_selection_combo_box.setItemData(self.tab_global_lang_selection_combo_box.count()-1, 'auto', 99)
        langs = self.lng.get_langs()
        for lg in langs:
            self.tab_global_lang_selection_combo_box.addItem(lg['name'])
            self.tab_global_lang_selection_combo_box.setItemData(self.tab_global_lang_selection_combo_box.count() - 1,
                                                                 lg['code'], 99)

    def change_language(self):
        ""

    def apply_translation(self):
        self.setWindowTitle(self.lng['Editor']['LinkWindow']['WindowTitle'])
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setText(self.lng['Generic']['DialogBtnSave'])
        self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText(self.lng['Generic']['DialogBtnCancel'])
