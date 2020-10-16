from PyQt5 import QtCore, QtGui, QtWidgets
from lang import *

dialogStyle = """
        QMessageBox { background-color: rgb(62, 62, 62); color: rgb(255, 255, 255); }
        QWidget{ background-color: rgb(62, 62, 62); color: rgb(255, 255, 255); }
        QPushButton{ height:30px; }
    """
dialogStyleBtnGeneric = 'background-color: rgb(90, 90, 90); color: rgb(255, 255, 255);'
dialogStyleBtnRed = 'background-color: rgb(234, 86, 86); color: rgb(255, 255, 255);'
dialogStyleBtnGreen = 'background-color: rgb(0, 153, 15); color: rgb(255, 255, 255);'


def InfoDialog(title: str, text: str, parent: any = None):
    lang = Lang()
    msgBox = QtWidgets.QMessageBox(parent)
    msgBox.setStyleSheet(dialogStyle)
    msgBox.setWindowTitle(title)
    msgBox.setText(text)
    msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msgBox.button(QtWidgets.QMessageBox.Ok).setText(lang['Generic']['DialogBtnOk'])
    msgBox.button(QtWidgets.QMessageBox.Ok).setStyleSheet(dialogStyleBtnGeneric)
    msgBox.button(QtWidgets.QMessageBox.Ok).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
    msgBox.setIcon(QtWidgets.QMessageBox.Information)
    ret = msgBox.exec()


def InfoDialogConfirm(title: str, text: str, yes: str, no: str, parent: any = None):
    msgBox = QtWidgets.QMessageBox(parent)
    msgBox.setStyleSheet(dialogStyle)
    msgBox.setWindowTitle(title)
    msgBox.setText(text)
    msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    msgBox.button(QtWidgets.QMessageBox.Yes).setText(yes)
    msgBox.button(QtWidgets.QMessageBox.Yes).setStyleSheet(dialogStyleBtnGreen)
    msgBox.button(QtWidgets.QMessageBox.Yes).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    msgBox.button(QtWidgets.QMessageBox.No).setText(no)
    msgBox.button(QtWidgets.QMessageBox.No).setStyleSheet(dialogStyleBtnRed)
    msgBox.button(QtWidgets.QMessageBox.No).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    msgBox.setDefaultButton(QtWidgets.QMessageBox.No)
    msgBox.setIcon(QtWidgets.QMessageBox.Information)
    ret = msgBox.exec()
    if ret == QtWidgets.QMessageBox.Yes: return True
    else: return False


def WarnDialog(title: str, text: str, parent: any = None):
    lang = Lang()
    msgBox = QtWidgets.QMessageBox(parent)
    msgBox.setStyleSheet(dialogStyle)
    msgBox.setWindowTitle(title)
    msgBox.setText(text)
    msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msgBox.button(QtWidgets.QMessageBox.Ok).setText(lang['Generic']['DialogBtnOk'])
    msgBox.button(QtWidgets.QMessageBox.Ok).setStyleSheet(dialogStyleBtnGeneric)
    msgBox.button(QtWidgets.QMessageBox.Ok).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
    msgBox.setIcon(QtWidgets.QMessageBox.Warning)
    ret = msgBox.exec()


def WarnDialogConfirm(title: str, text: str, yes: str, no: str, parent: any = None):
    msgBox = QtWidgets.QMessageBox(parent)
    msgBox.setStyleSheet(dialogStyle)
    msgBox.setWindowTitle(title)
    msgBox.setText(text)
    msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    msgBox.button(QtWidgets.QMessageBox.Yes).setText(yes)
    msgBox.button(QtWidgets.QMessageBox.Yes).setStyleSheet(dialogStyleBtnRed)
    msgBox.button(QtWidgets.QMessageBox.Yes).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    msgBox.button(QtWidgets.QMessageBox.No).setText(no)
    msgBox.button(QtWidgets.QMessageBox.No).setStyleSheet(dialogStyleBtnGreen)
    msgBox.button(QtWidgets.QMessageBox.No).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    msgBox.setDefaultButton(QtWidgets.QMessageBox.No)
    msgBox.setIcon(QtWidgets.QMessageBox.Warning)
    ret = msgBox.exec()
    if ret == QtWidgets.QMessageBox.Yes: return True
    else: return False

