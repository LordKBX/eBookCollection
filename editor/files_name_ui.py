# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\CODES\Python\EbookCollection\editor\files_name.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dialog(object):
    def setupUi(self, dialog: QtWidgets.QDialog):
        dialog.setObjectName("dialog")
        dialog.resize(300, 120)
        dialog.setMinimumSize(QtCore.QSize(300, 120))
        dialog.setMaximumSize(QtCore.QSize(300, 120))
        self.verticalLayout = QtWidgets.QVBoxLayout(dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.setObjectName("horizontal_layout")
        self.label = QtWidgets.QLabel(dialog)
        self.label.setObjectName("label")
        self.horizontal_layout.addWidget(self.label)
        self.line_edit = QtWidgets.QLineEdit(dialog)
        self.line_edit.setObjectName("line_edit")
        self.horizontal_layout.addWidget(self.line_edit)
        self.verticalLayout.addLayout(self.horizontal_layout)
        self.button_box = QtWidgets.QDialogButtonBox(dialog)
        self.button_box.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.verticalLayout.addWidget(self.button_box)

        self.retranslateUi(dialog)
        self.button_box.accepted.connect(dialog.accept)
        self.button_box.rejected.connect(dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog: QtWidgets.QDialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "Dialog"))
        self.label.setText(_translate("dialog", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Ui_dialog()
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())
