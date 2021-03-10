import sys, os
from PyQt5.QtGui import *
from PyQt5.Qsci import *


class SimplePythonEditor(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self, lexer_type, parent=None, style_data: dict = None):
        super(SimplePythonEditor, self).__init__(parent)

        # Set the default font
        font = None
        font_family = 'Courier'
        font_id = None
        if style_data is not None:
            try:
                font_id = QFontDatabase.addApplicationFont(style_data['EditorQsciFont'].replace('/', os.sep))
                font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            except Exception:
                ""
        font = QFont(font_family)
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setMarginsFont(font)

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("00000") + 6)
        self.setMarginLineNumbers(0, True)

        # Clickable margin 1 for showing markers
        self.setMarginSensitivity(1, True)
        self.markerDefine(QsciScintilla.RightArrow, self.ARROW_MARKER_NUM)
        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)

        # Brace matching: enable for a brace immediately before or after
        # the current position
        #
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Current line visible with special background color
        self.setCaretLineVisible(True)

        if lexer_type is not None:
            self.elexer = lexer_type
            self.elexer.setFont(font)
            self.elexer.setDefaultFont(font)
            self.setLexer(self.elexer)
        else:
            self.elexer = None

        style_ok = False
        if style_data is not None:
            try:
                self.setMarginsBackgroundColor(QColor(style_data['EditorQsciMarginsBackgroundColor']))
                self.setMarginsForegroundColor(QColor(style_data['EditorQsciMarginsForegroundColor']))
                self.setMarkerBackgroundColor(QColor(style_data['EditorQsciMarkerBackgroundColor']), self.ARROW_MARKER_NUM)
                self.setFoldMarginColors(
                    QColor(style_data['EditorQsciFoldMarginColor1']),
                    QColor(style_data['EditorQsciFoldMarginColor2'])
                )
                self.setCaretLineBackgroundColor(style_data['EditorQsciCaretLineBackgroundColor'])

                self.setColor(QColor(style_data['EditorQsciDefaultTextColor']))
                self.setPaper(QColor(style_data['EditorQsciDefaultBackgroundColor']))

                if self.elexer is not None:
                    self.elexer.setDefaultColor(QColor(style_data['EditorQsciDefaultTextColor']))
                    self.elexer.setDefaultPaper(QColor(style_data['EditorQsciDefaultBackgroundColor']))
                    self.elexer.setPaper(QColor(style_data['EditorQsciDefaultBackgroundColor']))

                    if isinstance(lexer_type, QsciLexerXML) is True:
                        self.elexer.setColor(QColor(style_data['EditorQsciXMLDefaultTextColor']), QsciLexerXML.Default)
                        self.elexer.setColor(QColor(style_data['EditorQsciXMLDefaultTagColor']), QsciLexerXML.Tag)
                        self.elexer.setColor(QColor(style_data['EditorQsciXMLDefaultTagColor']), QsciLexerXML.UnknownTag)

                style_ok = True
            except Exception:
                ""
        if style_ok is False:
            self.setMarginsBackgroundColor(QColor("#333333"))
            self.setMarginsForegroundColor(QColor("#ffffff"))
            self.setMarkerBackgroundColor(QColor("#ee1111"), self.ARROW_MARKER_NUM)
            self.setFoldMarginColors(QColor("#cccccc"), QColor("#333333"))
            self.setCaretLineBackgroundColor(QColor("#ffe4e4"))

            self.setColor(QColor("#ffffff"))
            self.setPaper(QColor("#A6A6A6"))

            if self.elexer is not None:
                self.elexer.setDefaultPaper(QColor("#A6A6A6"))
                self.elexer.setDefaultColor(QColor("#ffffff"))
                self.elexer.setPaper(QColor("#A6A6A6"))

                if isinstance(lexer_type, QsciLexerXML) is True:
                    self.elexer.setColor(QColor.fromRgb(255, 255, 255), QsciLexerXML.Default)
                    self.elexer.setColor(QColor('#000080'), QsciLexerXML.Tag)
                    self.elexer.setColor(QColor('#000080'), QsciLexerXML.UnknownTag)

        text = bytearray(str.encode(font_family))
# 32, "Courier New"
        self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, text)

        # not too small
        self.setMinimumSize(300, 450)

    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)