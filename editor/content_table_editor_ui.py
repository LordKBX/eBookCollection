# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\CODES\Python\EbookCollection\editor\content_table_editor.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(QtWidgets.QDialog):
    def setupUi(self, Dialog: QtWidgets.QDialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(533, 350)
        Dialog.setMinimumSize(QtCore.QSize(400, 350))
        Dialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        Dialog.setWhatsThis("")
        Dialog.setModal(True)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.list_block = QtWidgets.QVBoxLayout()
        self.list_block.setContentsMargins(-1, 0, -1, -1)
        self.list_block.setSpacing(0)
        self.list_block.setObjectName("list_block")
        self.list_label = QtWidgets.QLabel(Dialog)
        self.list_label.setMinimumSize(QtCore.QSize(0, 20))
        self.list_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.list_label.setWordWrap(True)
        self.list_label.setObjectName("list_label")
        self.list_block.addWidget(self.list_label)
        self.list_content = QtWidgets.QListWidget(Dialog)
        self.list_content.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.list_content.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.list_content.setMovement(QtWidgets.QListView.Snap)
        self.list_content.setProperty("isWrapping", False)
        self.list_content.setResizeMode(QtWidgets.QListView.Adjust)
        self.list_content.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.list_content.setViewMode(QtWidgets.QListView.ListMode)
        self.list_content.setUniformItemSizes(True)
        self.list_content.setObjectName("list_content")
        item = QtWidgets.QListWidgetItem()
        self.list_content.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.list_content.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.list_content.addItem(item)
        self.list_block.addWidget(self.list_content)
        self.horizontalLayout.addLayout(self.list_block)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.addindex_label = QtWidgets.QLabel(Dialog)
        self.addindex_label.setMaximumSize(QtCore.QSize(250, 16777215))
        self.addindex_label.setObjectName("addindex_label")
        self.verticalLayout.addWidget(self.addindex_label)
        self.addindex_box = QtWidgets.QHBoxLayout()
        self.addindex_box.setSpacing(3)
        self.addindex_box.setObjectName("addindex_box")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.addindex_line_edit = QtWidgets.QLineEdit(Dialog)
        self.addindex_line_edit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.addindex_line_edit.setInputMask("")
        self.addindex_line_edit.setText("")
        self.addindex_line_edit.setObjectName("addindex_line_edit")
        self.verticalLayout_2.addWidget(self.addindex_line_edit)
        self.addindex_combobox = QtWidgets.QComboBox(Dialog)
        self.addindex_combobox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.addindex_combobox.setEditable(True)
        self.addindex_combobox.setObjectName("addindex_combobox")
        self.verticalLayout_2.addWidget(self.addindex_combobox)
        self.addindex_box.addLayout(self.verticalLayout_2)
        self.addindex_btn = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addindex_btn.sizePolicy().hasHeightForWidth())
        self.addindex_btn.setSizePolicy(sizePolicy)
        self.addindex_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.addindex_btn.setMaximumSize(QtCore.QSize(50, 16777215))
        self.addindex_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.addindex_btn.setObjectName("addindex_btn")
        self.addindex_box.addWidget(self.addindex_btn)
        self.verticalLayout.addLayout(self.addindex_box)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.modify_index_label = QtWidgets.QLabel(Dialog)
        self.modify_index_label.setMaximumSize(QtCore.QSize(250, 16777215))
        self.modify_index_label.setObjectName("modify_index_label")
        self.verticalLayout.addWidget(self.modify_index_label)
        self.btn_rename = QtWidgets.QPushButton(Dialog)
        self.btn_rename.setMinimumSize(QtCore.QSize(0, 50))
        self.btn_rename.setMaximumSize(QtCore.QSize(250, 16777215))
        self.btn_rename.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_rename.setObjectName("btn_rename")
        self.verticalLayout.addWidget(self.btn_rename)
        self.btn_delete = QtWidgets.QPushButton(Dialog)
        self.btn_delete.setMinimumSize(QtCore.QSize(0, 50))
        self.btn_delete.setMaximumSize(QtCore.QSize(250, 16777215))
        self.btn_delete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete.setObjectName("btn_delete")
        self.verticalLayout.addWidget(self.btn_delete)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.verticalLayout.addItem(spacerItem1)
        self.button_box = QtWidgets.QDialogButtonBox(Dialog)
        self.button_box.setMaximumSize(QtCore.QSize(250, 16777215))
        self.button_box.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.verticalLayout.addWidget(self.button_box)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        self.button_box.accepted.connect(Dialog.accept)
        self.button_box.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog: QtWidgets.QDialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.list_label.setText(_translate("Dialog", "Content Table list"))
        self.list_content.setSortingEnabled(False)
        __sortingEnabled = self.list_content.isSortingEnabled()
        self.list_content.setSortingEnabled(False)
        item = self.list_content.item(0)
        item.setText(_translate("Dialog", "N1"))
        item = self.list_content.item(1)
        item.setText(_translate("Dialog", "N2"))
        item = self.list_content.item(2)
        item.setText(_translate("Dialog", "N3"))
        self.list_content.setSortingEnabled(__sortingEnabled)
        self.addindex_label.setText(_translate("Dialog", "Insert index"))
        self.addindex_line_edit.setPlaceholderText(_translate("Dialog", "Nom d\'index"))
        self.addindex_btn.setText(_translate("Dialog", "+"))
        self.modify_index_label.setText(_translate("Dialog", "Modify index"))
        self.btn_rename.setText(_translate("Dialog", "Rename"))
        self.btn_delete.setText(_translate("Dialog", "Delete"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
