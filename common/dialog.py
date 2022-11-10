import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from common.lang import *
from common.bdd import *

dialogStyleBtnGreen = 'background-color: rgb(0, 153, 15); color: rgb(255, 255, 255);'


def __get_bases():
    language = Lang()
    bdd = BDD()
    style = bdd.get_param('style')
    return language, style


def InfoDialog(title: str, text: str, parent: any = None):
    msg_box = QtWidgets.QMessageBox(parent)

    language, style = __get_bases()
    msg_box.setStyleSheet(get_style_var(style, 'QMessageBox'))

    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.button(QtWidgets.QMessageBox.Ok).setText(language['Generic/DialogBtnOk'])
    msg_box.button(QtWidgets.QMessageBox.Ok).setFocusPolicy(QtCore.Qt.NoFocus)
    msg_box.button(QtWidgets.QMessageBox.Ok).setStyleSheet(get_style_var(style, 'QMessageBoxBtnGeneric'))
    msg_box.button(QtWidgets.QMessageBox.Ok).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    # msg_box.setDefaultButton(QtWidgets.QMessageBox.Ok)
    msg_box.setIcon(QtWidgets.QMessageBox.Information)
    ret = msg_box.exec()


def InfoDialogConfirm(title: str, text: str, yes: str, no: str, parent: any = None):
    msg_box = QtWidgets.QMessageBox(parent)

    language, style = __get_bases()
    msg_box.setStyleSheet(get_style_var(style, 'QMessageBox'))

    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    msg_box.button(QtWidgets.QMessageBox.Yes).setText(yes)
    msg_box.button(QtWidgets.QMessageBox.Yes).setFocusPolicy(QtCore.Qt.NoFocus)
    msg_box.button(QtWidgets.QMessageBox.Yes).setStyleSheet(get_style_var(style, 'QMessageBoxBtnGreen'))
    msg_box.button(QtWidgets.QMessageBox.Yes).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    msg_box.button(QtWidgets.QMessageBox.No).setText(no)
    msg_box.button(QtWidgets.QMessageBox.No).setFocusPolicy(QtCore.Qt.NoFocus)
    msg_box.button(QtWidgets.QMessageBox.No).setStyleSheet(get_style_var(style, 'QMessageBoxBtnRed'))
    msg_box.button(QtWidgets.QMessageBox.No).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    # msg_box.setDefaultButton(QtWidgets.QMessageBox.No)
    msg_box.setIcon(QtWidgets.QMessageBox.Information)
    ret = msg_box.exec()
    if ret == QtWidgets.QMessageBox.Yes:
        return True
    else:
        return False


def ErrorDialog(title: str, text: str, parent: any = None):
    msg_box = QtWidgets.QMessageBox(parent)

    language, style = __get_bases()
    msg_box.setStyleSheet(get_style_var(style, 'QMessageBox'))

    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.button(QtWidgets.QMessageBox.Ok).setText(language['Generic/DialogBtnOk'])
    msg_box.button(QtWidgets.QMessageBox.Ok).setFocusPolicy(QtCore.Qt.NoFocus)
    msg_box.button(QtWidgets.QMessageBox.Ok).setStyleSheet(get_style_var(style, 'QMessageBoxBtnGeneric'))
    msg_box.button(QtWidgets.QMessageBox.Ok).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    # msg_box.setDefaultButton(QtWidgets.QMessageBox.Ok)
    msg_box.setIcon(QtWidgets.QMessageBox.Critical)
    ret = msg_box.exec()


def WarnDialog(title: str, text: str, parent: any = None):
    msg_box = QtWidgets.QMessageBox(parent)

    language, style = __get_bases()
    msg_box.setStyleSheet(get_style_var(style, 'QMessageBox'))

    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.button(QtWidgets.QMessageBox.Ok).setText(language['Generic/DialogBtnOk'])
    msg_box.button(QtWidgets.QMessageBox.Ok).setFocusPolicy(QtCore.Qt.NoFocus)
    msg_box.button(QtWidgets.QMessageBox.Ok).setStyleSheet(get_style_var(style, 'QMessageBoxBtnGeneric'))
    msg_box.button(QtWidgets.QMessageBox.Ok).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    # msg_box.setDefaultButton(QtWidgets.QMessageBox.Ok)
    msg_box.setIcon(QtWidgets.QMessageBox.Warning)
    ret = msg_box.exec()


def WarnDialogConfirm(title: str, text: str, yes: str, no: str, parent: any = None):
    msg_box = QtWidgets.QMessageBox(parent)

    language, style = __get_bases()
    msg_box.setStyleSheet(get_style_var(style, 'QMessageBox'))

    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    msg_box.setFocusPolicy(QtCore.Qt.NoFocus)
    msg_box.button(QtWidgets.QMessageBox.Yes).setText(yes)
    msg_box.button(QtWidgets.QMessageBox.Yes).setFocusPolicy(QtCore.Qt.NoFocus)
    msg_box.button(QtWidgets.QMessageBox.Yes).setStyleSheet(get_style_var(style, 'QMessageBoxBtnRed'))
    msg_box.button(QtWidgets.QMessageBox.Yes).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    msg_box.button(QtWidgets.QMessageBox.No).setText(no)
    msg_box.button(QtWidgets.QMessageBox.No).setFocusPolicy(QtCore.Qt.NoFocus)
    msg_box.button(QtWidgets.QMessageBox.No).setStyleSheet(get_style_var(style, 'QMessageBoxBtnGreen'))
    msg_box.button(QtWidgets.QMessageBox.No).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    # msg_box.setDefaultButton(QtWidgets.QMessageBox.No)
    msg_box.setIcon(QtWidgets.QMessageBox.Warning)
    ret = msg_box.exec()
    if ret == QtWidgets.QMessageBox.Yes:
        return True
    else:
        return False


def InputDialog(title: str, text: str, yes: str = None, no: str = None, parent: any = None, value: str = None):
    language, style = __get_bases()
    msg_box = QtWidgets.QDialog(parent, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
    msg_box.setStyleSheet(get_style_var(style, 'QDialog'))
    msg_box.setWindowTitle(title)

    msg_box.setLayout(QtWidgets.QVBoxLayout())

    label = QtWidgets.QLabel(text)
    msg_box.layout().addWidget(label)

    input = QtWidgets.QLineEdit()
    if value is not None:
        input.setText(value)
    msg_box.layout().addWidget(input)

    action = QtWidgets.QAction()
    action.triggered.connect(lambda: print('TESSSSSSST!'))

    button_box = QtWidgets.QDialogButtonBox()
    button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
    button_box.setFocusPolicy(QtCore.Qt.NoFocus)
    if yes is None:
        yes = language['Generic/DialogBtnOk']
    if no is None:
        no = language['Generic/DialogBtnCancel']
    button_box.button(QtWidgets.QDialogButtonBox.Ok).setText(yes)
    button_box.button(QtWidgets.QDialogButtonBox.Ok).setFocusPolicy(QtCore.Qt.NoFocus)
    button_box.button(QtWidgets.QDialogButtonBox.Ok).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText(no)
    button_box.button(QtWidgets.QDialogButtonBox.Cancel).setFocusPolicy(QtCore.Qt.NoFocus)
    button_box.button(QtWidgets.QDialogButtonBox.Cancel).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    button_box.accepted.connect(msg_box.accept)
    button_box.rejected.connect(msg_box.reject)
    msg_box.layout().addWidget(button_box)

    ret = msg_box.exec_()
    if ret == 1:
        return input.text()
    else:
        return None

