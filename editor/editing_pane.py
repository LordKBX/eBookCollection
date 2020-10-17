import os
import io
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from common import *


class editorTabManager(QtWidgets.QTabWidget):
    def __init__(self, parent: any):
        QtWidgets.QTabWidget.__init__(self, parent)

    def createPane(self, title: str, path: str):
        tab = QtWidgets.QWidget()
        # tab.setObjectName("tab")
        tab.setProperty('fileName', path)
        verticalLayout = QtWidgets.QVBoxLayout(tab)
        # verticalLayout.setObjectName("verticalLayout")
        scrollArea = QtWidgets.QScrollArea(tab)
        scrollArea.setMaximumSize(QtCore.QSize(16777215, 50))
        scrollArea.setWidgetResizable(True)
        # scrollArea.setObjectName("scrollArea")
        scrollAreaWidgetContents = QtWidgets.QWidget()
        scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 203, 48))
        # scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        scrollArea.setWidget(scrollAreaWidgetContents)
        verticalLayout.addWidget(scrollArea)
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

