import os, sys
from PyQt5 import QtCore, QtGui, QtWidgets
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from lang import *
from vars import *

dialogStyle = """
        QMessageBox { background-color: rgb(62, 62, 62); color: rgb(255, 255, 255); }
        QWidget{ background-color: rgb(62, 62, 62); color: rgb(255, 255, 255); }
        QPushButton{ height:30px; }
    """
dialogStyleBtnGeneric = 'background-color: rgb(90, 90, 90); color: rgb(255, 255, 255);'
dialogStyleBtnRed = 'background-color: rgb(234, 86, 86); color: rgb(255, 255, 255);'
dialogStyleBtnGreen = 'background-color: rgb(0, 153, 15); color: rgb(255, 255, 255);'


def InfoDialog(title: str, text: str, parent: any = None):
    language = Lang()
    msg_box = QtWidgets.QMessageBox(parent)
    msg_box.setStyleSheet(dialogStyle)
    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.button(QtWidgets.QMessageBox.Ok).setText(language['Generic']['DialogBtnOk'])
    msg_box.button(QtWidgets.QMessageBox.Ok).setStyleSheet(dialogStyleBtnGeneric)
    msg_box.button(QtWidgets.QMessageBox.Ok).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    msg_box.setDefaultButton(QtWidgets.QMessageBox.Ok)
    msg_box.setIcon(QtWidgets.QMessageBox.Information)
    ret = msg_box.exec()


def InfoDialogConfirm(title: str, text: str, yes: str, no: str, parent: any = None):
    msg_box = QtWidgets.QMessageBox(parent)
    msg_box.setStyleSheet(dialogStyle)
    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    msg_box.button(QtWidgets.QMessageBox.Yes).setText(yes)
    msg_box.button(QtWidgets.QMessageBox.Yes).setStyleSheet(dialogStyleBtnGreen)
    msg_box.button(QtWidgets.QMessageBox.Yes).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    msg_box.button(QtWidgets.QMessageBox.No).setText(no)
    msg_box.button(QtWidgets.QMessageBox.No).setStyleSheet(dialogStyleBtnRed)
    msg_box.button(QtWidgets.QMessageBox.No).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    msg_box.setDefaultButton(QtWidgets.QMessageBox.No)
    msg_box.setIcon(QtWidgets.QMessageBox.Information)
    ret = msg_box.exec()
    if ret == QtWidgets.QMessageBox.Yes:
        return True
    else:
        return False


def WarnDialog(title: str, text: str, parent: any = None):
    language = Lang()
    msg_box = QtWidgets.QMessageBox(parent)
    msg_box.setStyleSheet(dialogStyle)
    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.button(QtWidgets.QMessageBox.Ok).setText(language['Generic']['DialogBtnOk'])
    msg_box.button(QtWidgets.QMessageBox.Ok).setStyleSheet(dialogStyleBtnGeneric)
    msg_box.button(QtWidgets.QMessageBox.Ok).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    msg_box.setDefaultButton(QtWidgets.QMessageBox.Ok)
    msg_box.setIcon(QtWidgets.QMessageBox.Warning)
    ret = msg_box.exec()


def WarnDialogConfirm(title: str, text: str, yes: str, no: str, parent: any = None):
    msg_box = QtWidgets.QMessageBox(parent)
    msg_box.setStyleSheet(dialogStyle)
    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    msg_box.button(QtWidgets.QMessageBox.Yes).setText(yes)
    msg_box.button(QtWidgets.QMessageBox.Yes).setStyleSheet(dialogStyleBtnRed)
    msg_box.button(QtWidgets.QMessageBox.Yes).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    msg_box.button(QtWidgets.QMessageBox.No).setText(no)
    msg_box.button(QtWidgets.QMessageBox.No).setStyleSheet(dialogStyleBtnGreen)
    msg_box.button(QtWidgets.QMessageBox.No).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    msg_box.setDefaultButton(QtWidgets.QMessageBox.No)
    msg_box.setIcon(QtWidgets.QMessageBox.Warning)
    ret = msg_box.exec()
    if ret == QtWidgets.QMessageBox.Yes:
        return True
    else:
        return False

