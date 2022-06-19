# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\CODES\Python\EbookCollection\editor\text_edit.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(QtWidgets.QWidget):
    def setupUi(self, Form: QtWidgets.QWidget):
        Form.setObjectName("Form")
        Form.resize(300, 120)
        Form.setMinimumSize(QtCore.QSize(300, 120))
        Form.setMaximumSize(QtCore.QSize(16777215, 120))
        Form.setStyleSheet("background:transparent;")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizon1 = QtWidgets.QHBoxLayout()
        self.horizon1.setSpacing(1)
        self.horizon1.setObjectName("horizon1")
        self.btnSave = QtWidgets.QPushButton(Form)
        self.btnSave.setMaximumSize(QtCore.QSize(30, 30))
        self.btnSave.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnSave.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../ressources/icons/white/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSave.setIcon(icon)
        self.btnSave.setIconSize(QtCore.QSize(25, 25))
        self.btnSave.setObjectName("btnSave")
        self.horizon1.addWidget(self.btnSave)
        self.btnUndo = QtWidgets.QPushButton(Form)
        self.btnUndo.setMaximumSize(QtCore.QSize(30, 30))
        self.btnUndo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnUndo.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/edit-undo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnUndo.setIcon(icon1)
        self.btnUndo.setIconSize(QtCore.QSize(25, 25))
        self.btnUndo.setObjectName("btnUndo")
        self.horizon1.addWidget(self.btnUndo)
        self.btnRedo = QtWidgets.QPushButton(Form)
        self.btnRedo.setMaximumSize(QtCore.QSize(30, 30))
        self.btnRedo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnRedo.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/edit-redo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnRedo.setIcon(icon2)
        self.btnRedo.setIconSize(QtCore.QSize(25, 25))
        self.btnRedo.setObjectName("btnRedo")
        self.horizon1.addWidget(self.btnRedo)
        self.btnCut = QtWidgets.QPushButton(Form)
        self.btnCut.setMaximumSize(QtCore.QSize(30, 30))
        self.btnCut.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnCut.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/edit-cut.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCut.setIcon(icon3)
        self.btnCut.setIconSize(QtCore.QSize(25, 25))
        self.btnCut.setObjectName("btnCut")
        self.horizon1.addWidget(self.btnCut)
        self.btnCopy = QtWidgets.QPushButton(Form)
        self.btnCopy.setMaximumSize(QtCore.QSize(30, 30))
        self.btnCopy.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnCopy.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/edit-copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCopy.setIcon(icon4)
        self.btnCopy.setIconSize(QtCore.QSize(25, 25))
        self.btnCopy.setObjectName("btnCopy")
        self.horizon1.addWidget(self.btnCopy)
        self.btnPaste = QtWidgets.QPushButton(Form)
        self.btnPaste.setMaximumSize(QtCore.QSize(30, 30))
        self.btnPaste.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnPaste.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/edit-paste.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnPaste.setIcon(icon5)
        self.btnPaste.setIconSize(QtCore.QSize(25, 25))
        self.btnPaste.setObjectName("btnPaste")
        self.horizon1.addWidget(self.btnPaste)
        self.horizon1_1 = QtWidgets.QHBoxLayout()
        self.horizon1_1.setSpacing(1)
        self.horizon1_1.setObjectName("horizon1_1")
        self.btnDebug = QtWidgets.QPushButton(Form)
        self.btnDebug.setMaximumSize(QtCore.QSize(30, 30))
        self.btnDebug.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnDebug.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/debug.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDebug.setIcon(icon6)
        self.btnDebug.setIconSize(QtCore.QSize(25, 25))
        self.btnDebug.setObjectName("btnDebug")
        self.horizon1_1.addWidget(self.btnDebug)
        self.btnComment = QtWidgets.QPushButton(Form)
        self.btnComment.setMaximumSize(QtCore.QSize(30, 30))
        self.btnComment.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnComment.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("../ressources/icons/white/comment.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnComment.setIcon(icon7)
        self.btnComment.setIconSize(QtCore.QSize(25, 25))
        self.btnComment.setObjectName("btnComment")
        self.horizon1_1.addWidget(self.btnComment)
        self.btnPrettify = QtWidgets.QPushButton(Form)
        self.btnPrettify.setMaximumSize(QtCore.QSize(30, 30))
        self.btnPrettify.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnPrettify.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/beautify.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnPrettify.setIcon(icon8)
        self.btnPrettify.setIconSize(QtCore.QSize(25, 25))
        self.btnPrettify.setObjectName("btnPrettify")
        self.horizon1_1.addWidget(self.btnPrettify)
        self.horizon1.addLayout(self.horizon1_1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizon1.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizon1)
        self.horizon2 = QtWidgets.QHBoxLayout()
        self.horizon2.setSpacing(0)
        self.horizon2.setObjectName("horizon2")
        self.horizon2_2 = QtWidgets.QHBoxLayout()
        self.horizon2_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizon2_2.setSpacing(1)
        self.horizon2_2.setObjectName("horizon2_2")
        self.btnBold = QtWidgets.QPushButton(Form)
        self.btnBold.setMinimumSize(QtCore.QSize(30, 30))
        self.btnBold.setMaximumSize(QtCore.QSize(30, 30))
        self.btnBold.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnBold.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/format-text-bold.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnBold.setIcon(icon9)
        self.btnBold.setIconSize(QtCore.QSize(25, 25))
        self.btnBold.setObjectName("btnBold")
        self.horizon2_2.addWidget(self.btnBold)
        self.btnItalic = QtWidgets.QPushButton(Form)
        self.btnItalic.setMinimumSize(QtCore.QSize(30, 30))
        self.btnItalic.setMaximumSize(QtCore.QSize(30, 30))
        self.btnItalic.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnItalic.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/format-text-italic.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnItalic.setIcon(icon10)
        self.btnItalic.setIconSize(QtCore.QSize(25, 25))
        self.btnItalic.setObjectName("btnItalic")
        self.horizon2_2.addWidget(self.btnItalic)
        self.btnUnderline = QtWidgets.QPushButton(Form)
        self.btnUnderline.setMinimumSize(QtCore.QSize(30, 30))
        self.btnUnderline.setMaximumSize(QtCore.QSize(30, 30))
        self.btnUnderline.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnUnderline.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/format-text-underline.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnUnderline.setIcon(icon11)
        self.btnUnderline.setIconSize(QtCore.QSize(25, 25))
        self.btnUnderline.setObjectName("btnUnderline")
        self.horizon2_2.addWidget(self.btnUnderline)
        self.btnStrikethrough = QtWidgets.QPushButton(Form)
        self.btnStrikethrough.setMinimumSize(QtCore.QSize(30, 30))
        self.btnStrikethrough.setMaximumSize(QtCore.QSize(30, 30))
        self.btnStrikethrough.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnStrikethrough.setText("")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/format-text-strikethrough.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnStrikethrough.setIcon(icon12)
        self.btnStrikethrough.setIconSize(QtCore.QSize(25, 25))
        self.btnStrikethrough.setObjectName("btnStrikethrough")
        self.horizon2_2.addWidget(self.btnStrikethrough)
        self.btnSub = QtWidgets.QPushButton(Form)
        self.btnSub.setMinimumSize(QtCore.QSize(30, 30))
        self.btnSub.setMaximumSize(QtCore.QSize(30, 30))
        self.btnSub.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnSub.setText("")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/format-text-subscript.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSub.setIcon(icon13)
        self.btnSub.setIconSize(QtCore.QSize(25, 25))
        self.btnSub.setObjectName("btnSub")
        self.horizon2_2.addWidget(self.btnSub)
        self.btnSup = QtWidgets.QPushButton(Form)
        self.btnSup.setMinimumSize(QtCore.QSize(30, 30))
        self.btnSup.setMaximumSize(QtCore.QSize(30, 30))
        self.btnSup.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnSup.setText("")
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/format-text-superscript.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSup.setIcon(icon14)
        self.btnSup.setIconSize(QtCore.QSize(25, 25))
        self.btnSup.setObjectName("btnSup")
        self.horizon2_2.addWidget(self.btnSup)
        self.btnTextColor = QtWidgets.QPushButton(Form)
        self.btnTextColor.setMinimumSize(QtCore.QSize(30, 30))
        self.btnTextColor.setMaximumSize(QtCore.QSize(30, 30))
        self.btnTextColor.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnTextColor.setText("")
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/format-text-color.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnTextColor.setIcon(icon15)
        self.btnTextColor.setIconSize(QtCore.QSize(25, 25))
        self.btnTextColor.setObjectName("btnTextColor")
        self.horizon2_2.addWidget(self.btnTextColor)
        self.btnBackColor = QtWidgets.QPushButton(Form)
        self.btnBackColor.setMinimumSize(QtCore.QSize(30, 30))
        self.btnBackColor.setMaximumSize(QtCore.QSize(30, 30))
        self.btnBackColor.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnBackColor.setText("")
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/format-fill-color.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnBackColor.setIcon(icon16)
        self.btnBackColor.setIconSize(QtCore.QSize(25, 25))
        self.btnBackColor.setObjectName("btnBackColor")
        self.horizon2_2.addWidget(self.btnBackColor)
        self.horizon2.addLayout(self.horizon2_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizon2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizon2)
        self.horizon3 = QtWidgets.QHBoxLayout()
        self.horizon3.setSpacing(0)
        self.horizon3.setObjectName("horizon3")
        self.horizon2_1 = QtWidgets.QHBoxLayout()
        self.horizon2_1.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizon2_1.setSpacing(1)
        self.horizon2_1.setObjectName("horizon2_1")
        self.btnAlignLeft = QtWidgets.QPushButton(Form)
        self.btnAlignLeft.setMinimumSize(QtCore.QSize(30, 30))
        self.btnAlignLeft.setMaximumSize(QtCore.QSize(30, 30))
        self.btnAlignLeft.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnAlignLeft.setText("")
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/format-justify-left.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAlignLeft.setIcon(icon17)
        self.btnAlignLeft.setIconSize(QtCore.QSize(25, 25))
        self.btnAlignLeft.setObjectName("btnAlignLeft")
        self.horizon2_1.addWidget(self.btnAlignLeft)
        self.btnAlignCenter = QtWidgets.QPushButton(Form)
        self.btnAlignCenter.setMinimumSize(QtCore.QSize(30, 30))
        self.btnAlignCenter.setMaximumSize(QtCore.QSize(30, 30))
        self.btnAlignCenter.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnAlignCenter.setText("")
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/format-justify-center.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAlignCenter.setIcon(icon18)
        self.btnAlignCenter.setIconSize(QtCore.QSize(25, 25))
        self.btnAlignCenter.setObjectName("btnAlignCenter")
        self.horizon2_1.addWidget(self.btnAlignCenter)
        self.btnAlignRight = QtWidgets.QPushButton(Form)
        self.btnAlignRight.setMinimumSize(QtCore.QSize(30, 30))
        self.btnAlignRight.setMaximumSize(QtCore.QSize(30, 30))
        self.btnAlignRight.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnAlignRight.setText("")
        icon19 = QtGui.QIcon()
        icon19.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/format-justify-right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAlignRight.setIcon(icon19)
        self.btnAlignRight.setIconSize(QtCore.QSize(25, 25))
        self.btnAlignRight.setObjectName("btnAlignRight")
        self.horizon2_1.addWidget(self.btnAlignRight)
        self.btnAlignJustify = QtWidgets.QPushButton(Form)
        self.btnAlignJustify.setMinimumSize(QtCore.QSize(30, 30))
        self.btnAlignJustify.setMaximumSize(QtCore.QSize(30, 30))
        self.btnAlignJustify.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnAlignJustify.setText("")
        icon20 = QtGui.QIcon()
        icon20.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/format-justify-fill.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAlignJustify.setIcon(icon20)
        self.btnAlignJustify.setIconSize(QtCore.QSize(25, 25))
        self.btnAlignJustify.setObjectName("btnAlignJustify")
        self.horizon2_1.addWidget(self.btnAlignJustify)
        self.btnList = QtWidgets.QPushButton(Form)
        self.btnList.setMinimumSize(QtCore.QSize(30, 30))
        self.btnList.setMaximumSize(QtCore.QSize(30, 30))
        self.btnList.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnList.setText("")
        icon21 = QtGui.QIcon()
        icon21.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/format-list-unordered.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnList.setIcon(icon21)
        self.btnList.setIconSize(QtCore.QSize(25, 25))
        self.btnList.setObjectName("btnList")
        self.horizon2_1.addWidget(self.btnList)
        self.btnNumList = QtWidgets.QPushButton(Form)
        self.btnNumList.setMinimumSize(QtCore.QSize(30, 30))
        self.btnNumList.setMaximumSize(QtCore.QSize(30, 30))
        self.btnNumList.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnNumList.setText("")
        icon22 = QtGui.QIcon()
        icon22.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/format-list-ordered.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnNumList.setIcon(icon22)
        self.btnNumList.setIconSize(QtCore.QSize(25, 25))
        self.btnNumList.setObjectName("btnNumList")
        self.horizon2_1.addWidget(self.btnNumList)
        self.btnLink = QtWidgets.QPushButton(Form)
        self.btnLink.setMinimumSize(QtCore.QSize(30, 30))
        self.btnLink.setMaximumSize(QtCore.QSize(30, 30))
        self.btnLink.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnLink.setText("")
        icon23 = QtGui.QIcon()
        icon23.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/insert-link.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnLink.setIcon(icon23)
        self.btnLink.setIconSize(QtCore.QSize(25, 25))
        self.btnLink.setObjectName("btnLink")
        self.horizon2_1.addWidget(self.btnLink)
        self.btnImg = QtWidgets.QPushButton(Form)
        self.btnImg.setMinimumSize(QtCore.QSize(30, 30))
        self.btnImg.setMaximumSize(QtCore.QSize(30, 30))
        self.btnImg.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnImg.setText("")
        icon24 = QtGui.QIcon()
        icon24.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/view-image.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnImg.setIcon(icon24)
        self.btnImg.setIconSize(QtCore.QSize(25, 25))
        self.btnImg.setObjectName("btnImg")
        self.horizon2_1.addWidget(self.btnImg)
        self.horizon3.addLayout(self.horizon2_1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizon3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizon3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form: QtWidgets.QWidget):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
