import os
import io
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import PyQt5.uic
from PyQt5.uic import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from common import *
from vars import *


class uiClass(QtWidgets.QWidget):
    def __init__(self):
        {}


class editorTabManager(QtWidgets.QTabWidget):
    def __init__(self, parent: any):
        QtWidgets.QTabWidget.__init__(self, parent)

    def createPane(self, title: str, path: str):
        tab = QtWidgets.QWidget()
        # tab.setObjectName("tab")
        tab.setProperty('fileName', path)
        verticalLayout = QtWidgets.QVBoxLayout(tab)
        # verticalLayout.setObjectName("verticalLayout")

        block = uiClass()
        super(uiClass, block).__init__()
        PyQt5.uic.loadUi(appDir+'/editor/text_edit.ui'.replace('/', os.sep), block) # Load the .ui file

        verticalLayout.addWidget(block)
        textEdit = QtWidgets.QTextEdit(tab)
        textEdit.setStyleSheet("background-color: rgb(154, 154, 154);\n"
                                    "color: rgb(0, 0, 0);")
        # textEdit.setObjectName("textEdit")
        print(path)
        with open(path, "r", encoding="utf8") as file:
            textEdit.setText(file.read())
        verticalLayout.addWidget(textEdit)
        self.addTab(tab, "")
        self.setTabText(self.indexOf(tab), title)

