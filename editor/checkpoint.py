# This Python file uses the following encoding: utf-8
import os, sys
from PyQt5.QtWidgets import *
import PyQt5.uic
from PyQt5.uic import *

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from common import lang
import common.common, common.files
from common.vars import *


class CheckpointWindow(QDialog):
    def __init__(self, parent, folder: str):
        super(CheckpointWindow, self).__init__(parent, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        PyQt5.uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'checkpoint.ui'.replace('/', os.sep), self)  # Load the .ui file
        self.BDD = parent.BDD
        style = self.BDD.get_param('style')
        lng = lang.Lang()
        lng.set_lang(self.BDD.get_param('lang'))
        self.setWindowTitle(lng['Editor/ChechpointWindow/WindowTitle'])
        self.setStyleSheet(get_style_var(style, 'QDialog'))

        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText(lng['Editor/LinkWindow/btnOk'])
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText(lng['Editor/LinkWindow/btnCancel'])
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setStyleSheet(get_style_var(style, 'defaultButton'))
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setStyleSheet(get_style_var(style, 'defaultButton'))
        cursor = QtGui.QCursor(QtCore.Qt.PointingHandCursor)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setCursor(cursor)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setCursor(cursor)

        self.fileTree.setStyleSheet(get_style_var(style, 'fullTreeView'))
        self.fileTree.headerItem().setText(0, lng['Editor']['FileTableHeader'])
        self.fileTree.itemClicked.connect(self.itemClick)
        self.folder = folder
        self.selectedCheckpoint = ''

    def openExec(self):
        self.fileTree.clear()
        liste = common.files.listing_of_directory(path=self.folder, level=1, list_base_content=['original'], list_excluded_directory=['original', 'current'])
        print(liste)
        for fold in liste:
            item = QtWidgets.QTreeWidgetItem(self.fileTree)
            item.setText(0, fold.replace(self.folder + os.sep, ''))
            item.setData(0, 99, fold)
            self.fileTree.insertTopLevelItem(0, item)

        ret = self.exec_()  # Show the GUI
        while ret == 1 and self.selectedCheckpoint == '':
            ret = self.exec_()
        if ret == 1:
            return self.selectedCheckpoint
        else:
            return None

    def itemClick(self, event):
        info = event.data(0, 99)
        self.selectedCheckpoint = info
