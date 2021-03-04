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
        PyQt5.uic.loadUi(app_directory + os.sep + 'editor/checkpoint.ui'.replace('/', os.sep), self)  # Load the .ui file
        lng = lang.Lang()
        self.setWindowTitle(lng['Editor']['LinkWindow']['WindowTitle'])
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText(lng['Editor']['LinkWindow']['btnOk'])
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText(lng['Editor']['LinkWindow']['btnCancel'])
        self.fileTree.setStyleSheet(env_vars['styles']['Dark']['fullTreeView'])
        self.fileTree.headerItem().setText(0, lng['Editor']['FileTableHeader'])
        self.fileTree.itemClicked.connect(self.itemClick)
        self.folder = folder
        self.selectedCheckpoint = ''

    def openExec(self):
        self.fileTree.clear()
        liste = common.files.listOnlyDir(path=self.folder, level=1, startDirs=['original'], excludeDirs=['original', 'current'])
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
