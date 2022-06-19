# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\CODES\Python\EbookCollection\editor\img.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(QtWidgets.QDialog):
    def setupUi(self, Dialog: QtWidgets.QDialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 350)
        Dialog.setMinimumSize(QtCore.QSize(400, 350))
        Dialog.setMaximumSize(QtCore.QSize(400, 350))
        Dialog.setModal(True)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.fileTree = QtWidgets.QTreeWidget(Dialog)
        self.fileTree.setObjectName("fileTree")
        self.fileTree.headerItem().setText(0, "1")
        self.horizontalLayout_2.addWidget(self.fileTree)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.imgButton = QtWidgets.QPushButton(Dialog)
        self.imgButton.setMinimumSize(QtCore.QSize(220, 250))
        self.imgButton.setText("")
        self.imgButton.setObjectName("imgButton")
        self.verticalLayout.addWidget(self.imgButton)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelUrl = QtWidgets.QLabel(Dialog)
        self.labelUrl.setMinimumSize(QtCore.QSize(100, 0))
        self.labelUrl.setObjectName("labelUrl")
        self.horizontalLayout.addWidget(self.labelUrl)
        self.editUrl = QtWidgets.QLineEdit(Dialog)
        self.editUrl.setObjectName("editUrl")
        self.horizontalLayout.addWidget(self.editUrl)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelText = QtWidgets.QLabel(Dialog)
        self.labelText.setMinimumSize(QtCore.QSize(100, 0))
        self.labelText.setObjectName("labelText")
        self.horizontalLayout_3.addWidget(self.labelText)
        self.editText = QtWidgets.QLineEdit(Dialog)
        self.editText.setObjectName("editText")
        self.horizontalLayout_3.addWidget(self.editText)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog: QtWidgets.QDialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.labelUrl.setText(_translate("Dialog", "TextLabel"))
        self.labelText.setText(_translate("Dialog", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
