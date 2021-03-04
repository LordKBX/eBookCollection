import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from common.lang import *
from common.bdd import *

dialogStyleBtnGreen = 'background-color: rgb(0, 153, 15); color: rgb(255, 255, 255);'


def InfoDialog(title: str, text: str, parent: any = None):
    msg_box = QtWidgets.QMessageBox(parent)

    language = Lang()
    bdd = BDD()
    style = bdd.get_param('style')
    msg_box.setStyleSheet(env_vars['styles'][style]['QMessageBox'])

    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.button(QtWidgets.QMessageBox.Ok).setText(language['Generic']['DialogBtnOk'])
    msg_box.button(QtWidgets.QMessageBox.Ok).setFocusPolicy(QtCore.Qt.NoFocus)
    msg_box.button(QtWidgets.QMessageBox.Ok).setStyleSheet(env_vars['styles'][style]['QMessageBoxBtnGeneric'])
    msg_box.button(QtWidgets.QMessageBox.Ok).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    # msg_box.setDefaultButton(QtWidgets.QMessageBox.Ok)
    msg_box.setIcon(QtWidgets.QMessageBox.Information)
    ret = msg_box.exec()


def InfoDialogConfirm(title: str, text: str, yes: str, no: str, parent: any = None):
    msg_box = QtWidgets.QMessageBox(parent)

    bdd = BDD()
    style = bdd.get_param('style')
    msg_box.setStyleSheet(env_vars['styles'][style]['QMessageBox'])

    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    msg_box.button(QtWidgets.QMessageBox.Yes).setText(yes)
    msg_box.button(QtWidgets.QMessageBox.Yes).setFocusPolicy(QtCore.Qt.NoFocus)
    msg_box.button(QtWidgets.QMessageBox.Yes).setStyleSheet(env_vars['styles'][style]['QMessageBoxBtnGreen'])
    msg_box.button(QtWidgets.QMessageBox.Yes).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    msg_box.button(QtWidgets.QMessageBox.No).setText(no)
    msg_box.button(QtWidgets.QMessageBox.No).setFocusPolicy(QtCore.Qt.NoFocus)
    msg_box.button(QtWidgets.QMessageBox.No).setStyleSheet(env_vars['styles'][style]['QMessageBoxBtnRed'])
    msg_box.button(QtWidgets.QMessageBox.No).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    # msg_box.setDefaultButton(QtWidgets.QMessageBox.No)
    msg_box.setIcon(QtWidgets.QMessageBox.Information)
    ret = msg_box.exec()
    if ret == QtWidgets.QMessageBox.Yes:
        return True
    else:
        return False


def WarnDialog(title: str, text: str, parent: any = None):
    msg_box = QtWidgets.QMessageBox(parent)

    language = Lang()
    bdd = BDD()
    style = bdd.get_param('style')
    msg_box.setStyleSheet(env_vars['styles'][style]['QMessageBox'])

    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.button(QtWidgets.QMessageBox.Ok).setText(language['Generic']['DialogBtnOk'])
    msg_box.button(QtWidgets.QMessageBox.Ok).setFocusPolicy(QtCore.Qt.NoFocus)
    msg_box.button(QtWidgets.QMessageBox.Ok).setStyleSheet(env_vars['styles'][style]['QMessageBoxBtnGeneric'])
    msg_box.button(QtWidgets.QMessageBox.Ok).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    # msg_box.setDefaultButton(QtWidgets.QMessageBox.Ok)
    msg_box.setIcon(QtWidgets.QMessageBox.Warning)
    ret = msg_box.exec()


def WarnDialogConfirm(title: str, text: str, yes: str, no: str, parent: any = None):
    msg_box = QtWidgets.QMessageBox(parent)

    bdd = BDD()
    style = bdd.get_param('style')
    msg_box.setStyleSheet(env_vars['styles'][style]['QMessageBox'])

    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    msg_box.setFocusPolicy(QtCore.Qt.NoFocus)
    msg_box.button(QtWidgets.QMessageBox.Yes).setText(yes)
    msg_box.button(QtWidgets.QMessageBox.Yes).setFocusPolicy(QtCore.Qt.NoFocus)
    msg_box.button(QtWidgets.QMessageBox.Yes).setStyleSheet(env_vars['styles'][style]['QMessageBoxBtnRed'])
    msg_box.button(QtWidgets.QMessageBox.Yes).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    msg_box.button(QtWidgets.QMessageBox.No).setText(no)
    msg_box.button(QtWidgets.QMessageBox.No).setFocusPolicy(QtCore.Qt.NoFocus)
    msg_box.button(QtWidgets.QMessageBox.No).setStyleSheet(env_vars['styles'][style]['QMessageBoxBtnGreen'])
    msg_box.button(QtWidgets.QMessageBox.No).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    # msg_box.setDefaultButton(QtWidgets.QMessageBox.No)
    msg_box.setIcon(QtWidgets.QMessageBox.Warning)
    ret = msg_box.exec()
    if ret == QtWidgets.QMessageBox.Yes:
        return True
    else:
        return False

