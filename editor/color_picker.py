import os
import sys
import traceback
from PyQt5 import QtCore, QtGui, QtWidgets
import PyQt5.uic
from PyQt5.uic import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from syntaxHighlight import *
from common.books import *
from common import bdd
from common import lang
from common import vars


class RgbPicker(QtWidgets.QLabel):
    # create a vertical color gradient similar to the "Color Shower"
    # used in QColorDialog
    colorGrads = QtGui.QLinearGradient(0, 0, 1, 0)
    colorGrads.setCoordinateMode(colorGrads.ObjectBoundingMode)
    xRatio = 1. / 6
    colorGrads.setColorAt(0, QtCore.Qt.red)
    colorGrads.setColorAt(xRatio, QtCore.Qt.red)
    colorGrads.setColorAt(xRatio * 2, QtCore.Qt.magenta)
    colorGrads.setColorAt(xRatio * 3, QtCore.Qt.blue)
    colorGrads.setColorAt(xRatio * 4, QtCore.Qt.cyan)
    colorGrads.setColorAt(xRatio * 5, QtCore.Qt.green)
    colorGrads.setColorAt(xRatio * 6, QtCore.Qt.yellow)

    # add a "mask" gradient to support gradients to lighter colors
    maskGrad = QtGui.QLinearGradient(0, 0, 0, 1)
    maskGrad.setCoordinateMode(maskGrad.ObjectBoundingMode)
    maskGrad.setColorAt(0, QtCore.Qt.black)
    maskGrad.setColorAt(0.5, QtCore.Qt.transparent)
    maskGrad.setColorAt(1, QtCore.Qt.white)

    # create a cross cursor to show the selected color, if any
    cursorPath = QtGui.QPainterPath()
    cursorPath.moveTo(-10, 0)
    cursorPath.lineTo(-4, 0)
    cursorPath.moveTo(0, -10)
    cursorPath.lineTo(0, -4)
    cursorPath.moveTo(4, 0)
    cursorPath.lineTo(10, 0)
    cursorPath.moveTo(0, 4)
    cursorPath.lineTo(0, 10)
    cursorPen = QtGui.QPen(QtCore.Qt.black, 3)

    colorChanged = QtCore.pyqtSignal(QtGui.QColor)
    colorSelected = QtCore.pyqtSignal(QtGui.QColor)
    showCursor = False
    cursorPos = QtCore.QPoint()
    clicked = False
    pix_size = QtCore.QSize(250, 250)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setFixedSize(self.pix_size)
        # create a pixmap and paint it with the gradients
        pixmap = QtGui.QPixmap(self.pix_size)
        qp = QtGui.QPainter(pixmap)
        qp.fillRect(pixmap.rect(), self.colorGrads)
        qp.fillRect(pixmap.rect(), self.maskGrad)
        qp.end()
        self.setPixmap(pixmap)
        # a QImage is required to get the color of a specific pixel
        self.image = pixmap.toImage()
        self.currentColor = QtGui.QColor()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked = True
            # set the current color and emit the colorChanged signal
            self.currentColor = QtGui.QColor(self.image.pixel(event.pos()))
            self.cursorPos = event.pos()
            self.showCursor = True
            self.update()
            self.colorSelected.emit(self.currentColor)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked = False

    def mouseMoveEvent(self, event):
        if self.clicked is True:
            pos = event.pos()
            if pos.x() >= self.rect().topRight().x():
                pos.setX(self.rect().topRight().x())
            if pos.x() <= self.rect().topLeft().x():
                pos.setX(self.rect().topLeft().x())

            if pos.y() >= self.rect().bottomRight().y():
                pos.setY(self.rect().bottomRight().y())
            if pos.y() <= self.rect().topRight().y():
                pos.setY(self.rect().topRight().y())
            if event.buttons() == QtCore.Qt.LeftButton:
                color = QtGui.QColor(self.image.pixel(pos))
                self.colorChanged.emit(color)
                self.currentColor = color
                self.cursorPos = pos
                self.update()

    def paintEvent(self, event):
        # paint the "color shower"
        QtWidgets.QLabel.paintEvent(self, event)
        if self.showCursor:
            # paint the color "cursor"
            qp = QtGui.QPainter(self)
            qp.setPen(self.cursorPen)
            qp.translate(self.cursorPos)
            qp.drawPath(self.cursorPath)


class ColorPicker(QtWidgets.QDialog):
    def __init__(self, parent: any = None):
        super(ColorPicker, self).__init__(None, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        PyQt5.uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'color_picker.ui'.replace('/', os.sep), self)
        self.lang = lang.Lang()
        self.BDD = parent.BDD
        self.style = self.BDD.get_param('style')
        self.lang.set_lang(self.BDD.get_param('lang'))
        self.setStyleSheet(get_style_var(self.style, 'EditorColorPicker'))
        self.setWindowTitle(self.lang['Editor/ColorPicker/WindowTitle'])

        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText(self.lang['Editor/FilesWindow/btnOk'])
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText(self.lang['Editor/FilesWindow/btnCancel'])
        cursor = QtGui.QCursor(QtCore.Qt.PointingHandCursor)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setCursor(cursor)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setCursor(cursor)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setStyleSheet(get_style_var(self.style, 'EditorColorPickerFullAltButton'))
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setStyleSheet(get_style_var(self.style, 'EditorColorPickerFullAltButton'))

        self.paletteLabel.setText(self.lang['Editor/ColorPicker/Palette'])
        self.chromaGraphLabel.setText(self.lang['Editor/ColorPicker/ChromaGraph'])
        self.RGB_GROUP.setTitle(self.lang['Editor/ColorPicker/RgbBox'])
        self.RGB_R_LABEL.setText(self.lang['Editor/ColorPicker/RgbR'])
        self.RGB_G_LABEL.setText(self.lang['Editor/ColorPicker/RgbG'])
        self.RGB_B_LABEL.setText(self.lang['Editor/ColorPicker/RgbB'])
        self.RGB_HEXA_LABEL.setText(self.lang['Editor/ColorPicker/RgbHexa'])
        self.previewLabel.setText(self.lang['Editor/ColorPicker/Preview'])

        try:
            self.rgbPicker.colorChanged.connect(self.__set_color_changed)
            self.rgbPicker.colorSelected.connect(self.__color_clicked)
            self.buttonBox.accepted.connect(self.accept)
            self.buttonBox.rejected.connect(self.reject)

            paletteColors = [
                "#000000", "#404040", "#FF0000", "#FF6A00", "#FFD800", "#B6FF00", "#4CFF00", "#00FF21",
                "#00FF90", "#00FFFF", "#0094FF", "#0026FF", "#4800FF", "#B200FF", "#FF00DC", "#FF006E",

                "#FFFFFF", "#808080", "#7F0000", "#7F3300", "#7F6A00", "#5B7F00", "#267F00", "#007F0E",
                "#007F46", "#007F7F", "#004A7F", "#00137F", "#21007F", "#57007F", "#7F006E", "#7F0037",

                "#A0A0A0", "#303030", "#FF7F7F", "#FFB27F", "#FFE97F", "#DAFF7F", "#A5FF7F", "#7FFF8E",
                "#7FFFC5", "#7FFFFF", "#7FC9FF", "#7F92FF", "#A17FFF", "#D67FFF", "#FF7FED", "#FF7FB6",

                "#C0C0C0", "#606060", "#7F3F3F", "#7F593F", "#7F743F", "#6D7F3F", "#527F3F", "#3F7F47",
                "#3F7F62", "#3F7F7F", "#3F647F", "#3F497F", "#503F7F", "#6B3F7F", "#7F3F76", "#7F3F5B"
            ]

            for i in range(0, len(paletteColors)):
                name = 'pal'
                if i < 9: name += '0'
                name += '{}'.format(i+1)
                button = QtWidgets.QPushButton()
                button.setObjectName(name)
                button.setFixedWidth(16)
                button.setFixedHeight(16)
                button.setCursor(cursor)
                button.setText("█")
                button.setStyleSheet(
                    get_style_var(self.style, 'EditorColorPickerColorBtn')
                        .replace('%1', paletteColors[i])
                        .replace('%2', paletteColors[i])
                        .replace('%3', self.__invert_color(QtGui.QColor(paletteColors[i])).name())
                )
                button.setToolTip("%s" % paletteColors[i])
                button.clicked.connect(self.__palette_set_color)
                row = int(float(i / 16))
                print(i, row)
                self.gridLayout.addWidget(button, row, i - (row * 16))
            self.__set_color(QtGui.QColor(paletteColors[0]))

            self.RGB_R_SLIDER.valueChanged.connect(lambda: self.__update_color('R', 'SLIDER'))
            self.RGB_R_SPIN.valueChanged.connect(lambda: self.__update_color('R', 'SPIN'))
            self.RGB_G_SLIDER.valueChanged.connect(lambda: self.__update_color('G', 'SLIDER'))
            self.RGB_G_SPIN.valueChanged.connect(lambda: self.__update_color('G', 'SPIN'))
            self.RGB_B_SLIDER.valueChanged.connect(lambda: self.__update_color('B', 'SLIDER'))
            self.RGB_B_SPIN.valueChanged.connect(lambda: self.__update_color('B', 'SPIN'))

        except Exception:
            traceback.print_exc()

    def __invert_color(self, ColourToInvert: QtGui.QColor) -> QColor:
        RGBMAX = 255
        R = RGBMAX - ColourToInvert.red()
        G = RGBMAX - ColourToInvert.green()
        B = RGBMAX - ColourToInvert.blue()

        if ColourToInvert.red() + 50 > R > ColourToInvert.red() - 50:
            R = 255
        if ColourToInvert.green() + 50 > G > ColourToInvert.green() - 50:
            G = 255
        if ColourToInvert.blue() + 50 > B > ColourToInvert.blue() - 50:
            B = 255
        return QtGui.QColor.fromRgb(R, G, B)
        
    def __palette_set_color(self):
        try:
            color = QtGui.QColor(self.sender().toolTip())
            self.__set_color(color)
            self.rgbPicker.showCursor = False
            self.rgbPicker.update()
        except Exception:
            traceback.print_exc()

    def __update_color(self, input_type: str, input_mode: str):
        try:
            name_base = ''
            if input_type in ['R', 'G', 'B']:
                name_base = 'RGB_'+input_type+'_'
            else:
                return
            if input_mode not in ['SLIDER', 'SPIN']:
                return

            name = name_base + input_mode
            if input_mode == 'SLIDER':
                name2 = name_base + 'SPIN'
                getattr(self, name2).setValue(getattr(self, name).value())
            elif input_mode == 'SPIN':
                name2 = name_base + 'SLIDER'
                getattr(self, name2).setValue(getattr(self, name).value())

            color = QtGui.QColor(self.RGB_R_SPIN.value(), self.RGB_G_SPIN.value(), self.RGB_B_SPIN.value(), 255)
            self.__set_color(color)
        except Exception:
            traceback.print_exc()

    def __set_color(self, color: QtGui.QColor = None):
        max = color.red()
        if max < color.green():
            max = color.green()
        if max < color.blue():
            max = color.blue()
        max = int(100 * max / 255)
        self.RGB_R_SLIDER.setValue(color.red())
        self.RGB_R_SPIN.setValue(color.red())
        self.RGB_G_SLIDER.setValue(color.green())
        self.RGB_G_SPIN.setValue(color.green())
        self.RGB_B_SLIDER.setValue(color.blue())
        self.RGB_B_SPIN.setValue(color.blue())
        self.RGB_HEXA_EDIT.setText(color.name())

        self.preview.setStyleSheet("background-color:%s;" % color.name())

    def __set_color_changed(self, color):
        self.__set_color(color)

    def __color_clicked(self):
        self.__set_color(self.rgbPicker.currentColor)

    def getColor(self, color=None):
        if isinstance(color, QtGui.QColor):
            self.set_color(color)
        # return a color only if the dialog is accepted
        if self.exec_():
            color = QtGui.QColor(self.RGB_R_SPIN.value(), self.RGB_G_SPIN.value(), self.RGB_B_SPIN.value(), 255)
            return color
        else:
            return None

#
# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     w = ColorPicker(None)
#     w.show()
#     sys.exit(app.exec_())