# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\CODES\Python\EbookCollection\color_picker.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(QtWidgets.QDialog):
    def setupUi(self, Dialog: QtWidgets.QDialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 410)
        Dialog.setMinimumSize(QtCore.QSize(500, 410))
        Dialog.setMaximumSize(QtCore.QSize(500, 410))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.paletteLabel = QtWidgets.QLabel(Dialog)
        self.paletteLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        self.paletteLabel.setObjectName("paletteLabel")
        self.verticalLayout_3.addWidget(self.paletteLabel)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.chromaGraphLabel = QtWidgets.QLabel(Dialog)
        self.chromaGraphLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        self.chromaGraphLabel.setObjectName("chromaGraphLabel")
        self.verticalLayout_3.addWidget(self.chromaGraphLabel)
        self.rgbPicker = RgbPicker(Dialog)
        self.rgbPicker.setMinimumSize(QtCore.QSize(250, 250))
        self.rgbPicker.setMaximumSize(QtCore.QSize(250, 250))
        self.rgbPicker.setText("")
        self.rgbPicker.setObjectName("rgbPicker")
        self.verticalLayout_3.addWidget(self.rgbPicker)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.RGB_GROUP = QtWidgets.QGroupBox(Dialog)
        self.RGB_GROUP.setObjectName("RGB_GROUP")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.RGB_GROUP)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.RGB_G_SPIN = QtWidgets.QSpinBox(self.RGB_GROUP)
        self.RGB_G_SPIN.setMaximumSize(QtCore.QSize(80, 16777215))
        self.RGB_G_SPIN.setMaximum(255)
        self.RGB_G_SPIN.setObjectName("RGB_G_SPIN")
        self.gridLayout_2.addWidget(self.RGB_G_SPIN, 1, 2, 1, 1)
        self.RGB_B_SPIN = QtWidgets.QSpinBox(self.RGB_GROUP)
        self.RGB_B_SPIN.setMaximumSize(QtCore.QSize(80, 16777215))
        self.RGB_B_SPIN.setMaximum(255)
        self.RGB_B_SPIN.setObjectName("RGB_B_SPIN")
        self.gridLayout_2.addWidget(self.RGB_B_SPIN, 2, 2, 1, 1)
        self.RGB_R_LABEL = QtWidgets.QLabel(self.RGB_GROUP)
        self.RGB_R_LABEL.setMaximumSize(QtCore.QSize(20, 16777215))
        self.RGB_R_LABEL.setObjectName("RGB_R_LABEL")
        self.gridLayout_2.addWidget(self.RGB_R_LABEL, 0, 0, 1, 1)
        self.RGB_R_SLIDER = QtWidgets.QSlider(self.RGB_GROUP)
        self.RGB_R_SLIDER.setMaximumSize(QtCore.QSize(100, 16777215))
        self.RGB_R_SLIDER.setMaximum(255)
        self.RGB_R_SLIDER.setOrientation(QtCore.Qt.Horizontal)
        self.RGB_R_SLIDER.setObjectName("RGB_R_SLIDER")
        self.gridLayout_2.addWidget(self.RGB_R_SLIDER, 0, 1, 1, 1)
        self.RGB_G_LABEL = QtWidgets.QLabel(self.RGB_GROUP)
        self.RGB_G_LABEL.setMaximumSize(QtCore.QSize(20, 16777215))
        self.RGB_G_LABEL.setObjectName("RGB_G_LABEL")
        self.gridLayout_2.addWidget(self.RGB_G_LABEL, 1, 0, 1, 1)
        self.RGB_G_SLIDER = QtWidgets.QSlider(self.RGB_GROUP)
        self.RGB_G_SLIDER.setMaximumSize(QtCore.QSize(100, 16777215))
        self.RGB_G_SLIDER.setMaximum(255)
        self.RGB_G_SLIDER.setOrientation(QtCore.Qt.Horizontal)
        self.RGB_G_SLIDER.setObjectName("RGB_G_SLIDER")
        self.gridLayout_2.addWidget(self.RGB_G_SLIDER, 1, 1, 1, 1)
        self.RGB_R_SPIN = QtWidgets.QSpinBox(self.RGB_GROUP)
        self.RGB_R_SPIN.setMaximumSize(QtCore.QSize(80, 16777215))
        self.RGB_R_SPIN.setMaximum(255)
        self.RGB_R_SPIN.setObjectName("RGB_R_SPIN")
        self.gridLayout_2.addWidget(self.RGB_R_SPIN, 0, 2, 1, 1)
        self.RGB_B_SLIDER = QtWidgets.QSlider(self.RGB_GROUP)
        self.RGB_B_SLIDER.setMaximumSize(QtCore.QSize(100, 16777215))
        self.RGB_B_SLIDER.setMaximum(255)
        self.RGB_B_SLIDER.setOrientation(QtCore.Qt.Horizontal)
        self.RGB_B_SLIDER.setObjectName("RGB_B_SLIDER")
        self.gridLayout_2.addWidget(self.RGB_B_SLIDER, 2, 1, 1, 1)
        self.RGB_B_LABEL = QtWidgets.QLabel(self.RGB_GROUP)
        self.RGB_B_LABEL.setMaximumSize(QtCore.QSize(20, 16777215))
        self.RGB_B_LABEL.setObjectName("RGB_B_LABEL")
        self.gridLayout_2.addWidget(self.RGB_B_LABEL, 2, 0, 1, 1)
        self.RGB_HEXA_LABEL = QtWidgets.QLabel(self.RGB_GROUP)
        self.RGB_HEXA_LABEL.setMaximumSize(QtCore.QSize(80, 16777215))
        self.RGB_HEXA_LABEL.setObjectName("RGB_HEXA_LABEL")
        self.gridLayout_2.addWidget(self.RGB_HEXA_LABEL, 3, 0, 1, 2)
        self.RGB_HEXA_EDIT = QtWidgets.QLineEdit(self.RGB_GROUP)
        self.RGB_HEXA_EDIT.setMaximumSize(QtCore.QSize(80, 16777215))
        self.RGB_HEXA_EDIT.setObjectName("RGB_HEXA_EDIT")
        self.gridLayout_2.addWidget(self.RGB_HEXA_EDIT, 3, 2, 1, 1)
        self.verticalLayout_2.addWidget(self.RGB_GROUP)
        self.previewLabel = QtWidgets.QLabel(Dialog)
        self.previewLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        self.previewLabel.setObjectName("previewLabel")
        self.verticalLayout_2.addWidget(self.previewLabel)
        self.preview = QtWidgets.QLabel(Dialog)
        self.preview.setText("")
        self.preview.setObjectName("preview")
        self.verticalLayout_2.addWidget(self.preview)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog: QtWidgets.QDialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.paletteLabel.setText(_translate("Dialog", "paletteLabel"))
        self.chromaGraphLabel.setText(_translate("Dialog", "Chroma Graph"))
        self.RGB_GROUP.setTitle(_translate("Dialog", "RGB"))
        self.RGB_R_LABEL.setText(_translate("Dialog", "R"))
        self.RGB_G_LABEL.setText(_translate("Dialog", "G"))
        self.RGB_B_LABEL.setText(_translate("Dialog", "B"))
        self.RGB_HEXA_LABEL.setText(_translate("Dialog", "Hexa"))
        self.previewLabel.setText(_translate("Dialog", "Preview"))
from color_picker import RgbPicker


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())