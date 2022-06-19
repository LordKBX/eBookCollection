# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\CODES\Python\EbookCollection\editor\files.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dialog(object):
    def setupUi(self, dialog: QtWidgets.QDialog):
        dialog.setObjectName("dialog")
        dialog.resize(400, 400)
        dialog.setMinimumSize(QtCore.QSize(400, 400))
        dialog.setMaximumSize(QtCore.QSize(400, 400))
        dialog.setModal(True)
        self.horizontalLayout = QtWidgets.QHBoxLayout(dialog)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.file_tree = QtWidgets.QTreeWidget(dialog)
        self.file_tree.setObjectName("file_tree")
        self.file_tree.headerItem().setText(0, "1")
        self.horizontalLayout.addWidget(self.file_tree)
        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.vertical_layout.setSpacing(3)
        self.vertical_layout.setObjectName("vertical_layout")
        self.btn_import = QtWidgets.QPushButton(dialog)
        self.btn_import.setMinimumSize(QtCore.QSize(0, 70))
        self.btn_import.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_import.setObjectName("btn_import")
        self.vertical_layout.addWidget(self.btn_import)
        self.horizontal_layout_2 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_2.setSpacing(2)
        self.horizontal_layout_2.setObjectName("horizontal_layout_2")
        self.btn_new_file = QtWidgets.QPushButton(dialog)
        self.btn_new_file.setMinimumSize(QtCore.QSize(0, 70))
        self.btn_new_file.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_new_file.setObjectName("btn_new_file")
        self.horizontal_layout_2.addWidget(self.btn_new_file)
        self.btn_new_folder = QtWidgets.QPushButton(dialog)
        self.btn_new_folder.setMinimumSize(QtCore.QSize(0, 70))
        self.btn_new_folder.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_new_folder.setObjectName("btn_new_folder")
        self.horizontal_layout_2.addWidget(self.btn_new_folder)
        self.vertical_layout.addLayout(self.horizontal_layout_2)
        self.btn_rename = QtWidgets.QPushButton(dialog)
        self.btn_rename.setMinimumSize(QtCore.QSize(0, 70))
        self.btn_rename.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_rename.setObjectName("btn_rename")
        self.vertical_layout.addWidget(self.btn_rename)
        self.btn_delete = QtWidgets.QPushButton(dialog)
        self.btn_delete.setMinimumSize(QtCore.QSize(0, 70))
        self.btn_delete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete.setObjectName("btn_delete")
        self.vertical_layout.addWidget(self.btn_delete)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.vertical_layout.addItem(spacerItem)
        self.button_box = QtWidgets.QDialogButtonBox(dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_box.sizePolicy().hasHeightForWidth())
        self.button_box.setSizePolicy(sizePolicy)
        self.button_box.setMinimumSize(QtCore.QSize(200, 20))
        self.button_box.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.button_box.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.button_box.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.vertical_layout.addWidget(self.button_box)
        self.horizontalLayout.addLayout(self.vertical_layout)

        self.retranslateUi(dialog)
        self.button_box.accepted.connect(dialog.accept)
        self.button_box.rejected.connect(dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog: QtWidgets.QDialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "Dialog"))
        self.btn_import.setText(_translate("dialog", "Import File"))
        self.btn_new_file.setText(_translate("dialog", "New File"))
        self.btn_new_folder.setText(_translate("dialog", "New Folder"))
        self.btn_rename.setText(_translate("dialog", "Rename"))
        self.btn_delete.setText(_translate("dialog", "Delete"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Ui_dialog()
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())
