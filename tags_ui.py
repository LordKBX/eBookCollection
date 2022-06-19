# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\CODES\Python\EbookCollection\tags.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(QtWidgets.QDialog):
    def setupUi(self, Dialog: QtWidgets.QDialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 240)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.searchbox = QtWidgets.QLineEdit(Dialog)
        self.searchbox.setObjectName("searchbox")
        self.verticalLayout.addWidget(self.searchbox)
        self.table = QtWidgets.QTableWidget(Dialog)
        self.table.setAlternatingRowColors(False)
        self.table.setCornerButtonEnabled(False)
        self.table.setObjectName("table")
        self.table.setColumnCount(1)
        self.table.setRowCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(4, 0, item)
        self.table.horizontalHeader().setVisible(False)
        self.table.horizontalHeader().setCascadingSectionResizes(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.table)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_new = QtWidgets.QPushButton(Dialog)
        self.button_new.setObjectName("button_new")
        self.horizontalLayout.addWidget(self.button_new)
        self.button_box = QtWidgets.QDialogButtonBox(Dialog)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(False)
        self.button_box.setObjectName("button_box")
        self.horizontalLayout.addWidget(self.button_box)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        self.button_box.accepted.connect(Dialog.accept)
        self.button_box.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog: QtWidgets.QDialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.table.setSortingEnabled(True)
        item = self.table.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "Nouvelle ligne"))
        item = self.table.verticalHeaderItem(1)
        item.setText(_translate("Dialog", "Nouvelle ligne"))
        item = self.table.verticalHeaderItem(2)
        item.setText(_translate("Dialog", "Nouvelle ligne"))
        item = self.table.verticalHeaderItem(3)
        item.setText(_translate("Dialog", "Nouvelle ligne"))
        item = self.table.verticalHeaderItem(4)
        item.setText(_translate("Dialog", "Nouvelle ligne"))
        item = self.table.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Tags"))
        __sortingEnabled = self.table.isSortingEnabled()
        self.table.setSortingEnabled(False)
        item = self.table.item(0, 0)
        item.setText(_translate("Dialog", "Magic"))
        item = self.table.item(1, 0)
        item.setText(_translate("Dialog", "Fantasy"))
        item = self.table.item(2, 0)
        item.setText(_translate("Dialog", "Isekai"))
        item = self.table.item(3, 0)
        item.setText(_translate("Dialog", "Manga"))
        item = self.table.item(4, 0)
        item.setText(_translate("Dialog", "Novel"))
        self.table.setSortingEnabled(__sortingEnabled)
        self.button_new.setText(_translate("Dialog", "New"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
