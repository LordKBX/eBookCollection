import PyQt5
from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtGui import QColor, QPainter, QTextFormat
from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QTextEdit


class LineNumberArea(QWidget):
    def __init__(self, editor):
        QWidget.__init__(self, editor)
        self._code_editor = editor

    def sizeHint(self):
        return QSize(self._code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self._code_editor.lineNumberAreaPaintEvent(event)


def formatColor(color):
    """Return a QColor with the given attributes.
    """
    _color = QColor()
    _color.setNamedColor(color)
    return _color


class CodeEditor(QPlainTextEdit):
    style = {
        "EditorQsciFont": "{APP_DIR}/ressources/fonts/Arimo/Regular.ttf",
        "EditorQsciMarginsBackgroundColor": "#333333",
        "EditorQsciMarginsForegroundColor": "#ffffff",
        "EditorQsciCaretLineBackgroundColor": "#BBBBBB",
        "EditorQsciDefaultTextColor": "#ffffff"
    }

    def __init__(self, styleDict: dict = None):
        super().__init__()
        if styleDict is not None:
            for index in styleDict:
                print(index)
                if self.style.__contains__(index):
                    self.style[index] = styleDict.get(index)
                else:
                    self.style[index] = styleDict.get(index)
        self.line_number_area = LineNumberArea(self)

        self.blockCountChanged[int].connect(self.update_line_number_area_width)
        self.updateRequest[QRect, int].connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width(0)
        self.highlight_current_line()

    def line_number_area_width(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num *= 0.1
            digits += 1

        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def resizeEvent(self, e):
        super().resizeEvent(e)
        cr = self.contentsRect()
        width = self.line_number_area_width()
        rect = QRect(cr.left(), cr.top(), width, cr.height())
        self.line_number_area.setGeometry(rect)

    def presentNumber(self, number: int, nb_length: int) -> str:
        ret = "{}".format(number)
        nb_line = len("{}".format(number))
        for i in range(0, nb_length - nb_line):
            ret = "0"+ret
        return ret

    def lineNumberAreaPaintEvent(self, event):
        max = len(self.toPlainText().split('\n'))
        nb_length = len("{}".format(max))
        with QPainter(self.line_number_area) as painter:
            painter.fillRect(event.rect(), formatColor(self.style['EditorQsciMarginsBackgroundColor']))
            block = self.firstVisibleBlock()
            block_number = block.blockNumber()
            offset = self.contentOffset()
            top = self.blockBoundingGeometry(block).translated(offset).top()
            bottom = top + self.blockBoundingRect(block).height()

            while block.isValid() and top <= event.rect().bottom():
                if block.isVisible() and bottom >= event.rect().top():
                    number = self.presentNumber(block_number + 1, nb_length)
                    painter.setPen(formatColor(self.style['EditorQsciMarginsForegroundColor']))
                    width = self.line_number_area.width()
                    height = self.fontMetrics().height()
                    painter.drawText(0, top, width, height, Qt.AlignHCenter, number)

                block = block.next()
                top = bottom
                bottom = top + self.blockBoundingRect(block).height()
                block_number += 1

    def update_line_number_area_width(self, newBlockCount):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            width = self.line_number_area.width()
            self.line_number_area.update(0, rect.y(), width, rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def highlight_current_line(self):
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            line_color = formatColor(self.style['EditorQsciCaretLineBackgroundColor'])
            selection.format.setBackground(line_color)

            selection.format.setProperty(QTextFormat.FullWidthSelection, True)

            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()

            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)