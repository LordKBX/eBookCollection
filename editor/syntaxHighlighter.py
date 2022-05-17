import re
import traceback
from enum import Enum

from PyQt5 import QtCore, QtGui, QtWidgets


def format(color, style=''):
    """Return a QTextCharFormat with the given attributes.
    """
    _color = QtGui.QColor()
    _color.setNamedColor(color)

    _format = QtGui.QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QtGui.QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


# Syntax styles that can be shared by all languages
STYLES = {
    'keyword': format('yellow'),
    'operator': format('#FF6666'),
    'brace': format('lightBlue'),
    'defclass': format('black', 'bold'),
    'string': format('magenta'),
    'string2': format('darkMagenta'),
    'comment': format('lightGreen', 'italic'),
    'self': format('black', 'italic'),
    'numbers': format('orange'),
}


class MODES(Enum):
    TEXT = 1
    XML = 2
    HTML = 3
    CSS = 4


class SyntaxHighlighter (QtGui.QSyntaxHighlighter):
    """Syntax highlighter for the Python language.
    """
    keywordsXML = [
        'class', 'href', 'src', 'rel', 'type', 'alt', 'id'
    ]
    keywordsHTML = [
        'class', 'href', 'src', 'rel', 'type', 'alt', 'id'
    ]
    keywordsCSS1 = [
        '\\@annotation', '\\@bottom\\-center', '\\@character\\-variant', '\\@charset', '\\@counter\\-style', '\\@font\\-face', '\\@font\\-feature\\-values',
        '\\@historical\\-forms', '\\@import', '\\@keyframes', '\\@layer', '\\@left\\-bottom', '\\@media', '\\@namespace', '\\@ornaments',
        '\\@page', '\\@property', '\\@right\\-bottom', '\\@scroll\\-timeline', '\\@styleset', '\\@stylistic', '\\@supports', '\\@swash',
        '\\@top\\-center', '\\@viewport',
        'h1', 'h2', 'h3', 'h4', 'h5', 'img',
        'img[ ]{0,5}\{', '[a-zA-Z0-9\_\-]{1,20}[ ]{0,5}\{',
    ]
    keywordsCSS2 = [
        '--[a-zA-Z0-9\_\-\.]{1,100}', 'accent-color', 'additive-symbols', 'align-content', 'align-items', 'align-self',
        'align-tracks', 'all', 'animation', 'animation-delay', 'animation-direction', 'animation-duration', 'animation-fill-mode',
        'animation-iteration-count', 'animation-name', 'animation-play-state', 'animation-timeline', 'animation-timing-function',
        'appearance', 'ascent-override', 'aspect-ratio', 'backdrop-filter', 'backface-visibility', 'background', 'background-attachment',
        'background-blend-mode', 'background-clip', 'background-color', 'background-image', 'background-origin', 'background-position',
        'background-position-x', 'background-position-y', 'background-repeat', 'background-size', 'bleed', 'block-overflow', 'block-size',
        'border', 'border-block', 'border-block-color', 'border-block-end', 'border-block-end-color', 'border-block-end-style',
        'border-block-end-width', 'border-block-start', 'border-block-start-color', 'border-block-start-style', 'border-block-start-width',
        'border-block-style', 'border-block-width', 'border-bottom', 'border-bottom-color', 'border-bottom-left-radius', 'border-bottom-right-radius',
        'border-bottom-style', 'border-bottom-width', 'border-collapse', 'border-color', 'border-end-end-radius', 'border-end-start-radius',
        'border-image', 'border-image-outset', 'border-image-repeat', 'border-image-slice', 'border-image-source', 'border-image-width', 'border-inline',
        'border-inline-color', 'border-inline-end', 'border-inline-end-color', 'border-inline-end-style', 'border-inline-end-width', 'border-inline-start',
        'border-inline-start-color', 'border-inline-start-style', 'border-inline-start-width', 'border-inline-style', 'border-inline-width', 'border-left',
        'border-left-color', 'border-left-style', 'border-left-width', 'border-radius', 'border-right', 'border-right-color', 'border-right-style',
        'border-right-width', 'border-spacing', 'border-start-end-radius', 'border-start-start-radius', 'border-style', 'border-top', 'border-top-color',
        'border-top-left-radius', 'border-top-right-radius', 'border-top-style', 'border-top-width', 'border-width', 'bottom', 'box-decoration-break', 'box-shadow',
        'box-sizing', 'break-after', 'break-before', 'break-inside', 'caption-side', 'caret-color', 'clear', 'clip', 'clip-path', 'color', 'color-scheme',
        'column-count', 'column-fill', 'column-gap', 'column-rule', 'column-rule-color', 'column-rule-style', 'column-rule-width', 'column-span', 'column-width',
        'columns', 'contain', 'content', 'content-visibility', 'counter-increment', 'counter-reset', 'counter-set', 'cursor', 'descent-override', 'direction',
        'display', 'empty-cells', 'fallback', 'filter', 'flex', 'flex-basis', 'flex-direction', 'flex-flow', 'flex-grow', 'flex-shrink', 'flex-wrap', 'flex_value',
        'float', 'font', 'font-display', 'font-family', 'font-feature-settings', 'font-kerning', 'font-language-override', 'font-optical-sizing', 'font-size',
        'font-size-adjust', 'font-stretch', 'font-style', 'font-synthesis', 'font-variant', 'font-variant-alternates', 'font-variant-caps', 'font-variant-east-asian',
        'font-variant-ligatures', 'font-variant-numeric', 'font-variant-position', 'font-variation-settings', 'font-weight', 'forced-color-adjust', 'gap', 'grid',
        'grid-area', 'grid-auto-columns', 'grid-auto-flow', 'grid-auto-rows', 'grid-column', 'grid-column-end', 'grid-column-start', 'grid-row', 'grid-row-end',
        'grid-row-start', 'grid-template', 'grid-template-areas', 'grid-template-columns', 'grid-template-rows', 'hanging-punctuation', 'height', 'hyphenate-character',
        'hyphens', 'image-orientation', 'image-rendering', 'image-resolution', 'inherit', 'inherits', 'initial', 'initial-letter', 'initial-letter-align',
        'initial-value', 'inline-size', 'input-security', 'inset', 'inset-block', 'inset-block-end', 'inset-block-start', 'inset-inline', 'inset-inline-end',
        'inset-inline-start', 'isolation', 'justify-content', 'justify-items', 'justify-self', 'justify-tracks', 'left', 'letter-spacing', 'line-break',
        'line-clamp', 'line-gap-override', 'line-height', 'line-height-step', 'list-style', 'list-style-image', 'list-style-position', 'list-style-type',
        'margin', 'margin-block', 'margin-block-end', 'margin-block-start', 'margin-bottom', 'margin-inline', 'margin-inline-end', 'margin-inline-start',
        'margin-left', 'margin-right', 'margin-top', 'margin-trim', 'marks', 'mask', 'mask-border', 'mask-border-mode', 'mask-border-outset', 'mask-border-repeat',
        'mask-border-slice', 'mask-border-source', 'mask-border-width', 'mask-clip', 'mask-composite', 'mask-image', 'mask-mode', 'mask-origin', 'mask-position',
        'mask-repeat', 'mask-size', 'mask-type', 'masonry-auto-flow', 'math-style', 'max-block-size', 'max-height', 'max-inline-size', 'max-lines', 'max-width',
        'max-zoom', 'min-block-size', 'min-height', 'min-inline-size', 'min-width', 'min-zoom', 'mix-blend-mode', 'negative', 'object-fit', 'object-position',
        'offset', 'offset-anchor', 'offset-distance', 'offset-path', 'offset-position', 'offset-rotate', 'opacity', 'order', 'orientation', 'orphans',
        'outline', 'outline-color', 'outline-offset', 'outline-style', 'outline-width', 'overflow', 'overflow-anchor', 'overflow-block', 'overflow-clip-margin',
        'overflow-inline', 'overflow-wrap', 'overflow-x', 'overflow-y', 'overscroll-behavior', 'overscroll-behavior-block', 'overscroll-behavior-inline',
        'overscroll-behavior-x', 'overscroll-behavior-y', 'pad', 'padding', 'padding-block', 'padding-block-end', 'padding-block-start', 'padding-bottom',
        'padding-inline', 'padding-inline-end', 'padding-inline-start', 'padding-left', 'padding-right', 'padding-top', 'page-break-after', 'page-break-before',
        'page-break-inside', 'paint-order', 'perspective', 'perspective-origin', 'place-content', 'place-items', 'place-self', 'pointer-events', 'position',
        'prefix', 'print-color-adjust', 'quotes', 'range', 'resize', 'revert', 'right', 'rotate', 'row-gap', 'ruby-align', 'ruby-merge', 'ruby-position',
        'scale', 'scroll-behavior', 'scroll-margin', 'scroll-margin-block', 'scroll-margin-block-end', 'scroll-margin-block-start', 'scroll-margin-bottom',
        'scroll-margin-inline', 'scroll-margin-inline-end', 'scroll-margin-inline-start', 'scroll-margin-left', 'scroll-margin-right', 'scroll-margin-top',
        'scroll-padding', 'scroll-padding-block', 'scroll-padding-block-end', 'scroll-padding-block-start', 'scroll-padding-bottom', 'scroll-padding-inline',
        'scroll-padding-inline-end', 'scroll-padding-inline-start', 'scroll-padding-left', 'scroll-padding-right', 'scroll-padding-top', 'scroll-snap-align',
        'scroll-snap-stop', 'scroll-snap-type', 'scrollbar-color', 'scrollbar-gutter', 'scrollbar-width', 'shape-image-threshold', 'shape-margin', 'shape-outside',
        'size', 'size-adjust', 'speak-as', 'src', 'suffix', 'symbols', 'syntax', 'system', 'tab-size', 'table-layout', 'text-align', 'text-align-last',
        'text-combine-upright', 'text-decoration', 'text-decoration-color', 'text-decoration-line', 'text-decoration-skip', 'text-decoration-skip-ink',
        'text-decoration-style', 'text-decoration-thickness', 'text-emphasis', 'text-emphasis-color', 'text-emphasis-position', 'text-emphasis-style',
        'text-indent', 'text-justify', 'text-orientation', 'text-overflow', 'text-rendering', 'text-shadow', 'text-size-adjust', 'text-transform',
        'text-underline-offset', 'text-underline-position', 'top', 'touch-action', 'transform', 'transform-box', 'transform-origin', 'transform-style',
        'transition', 'transition-delay', 'transition-duration', 'transition-property', 'transition-timing-function', 'translate', 'unicode-bidi', 'unicode-range',
        'unset', 'user-select', 'user-zoom', 'vertical-align', 'viewport-fit', 'visibility', 'white-space', 'widows', 'width', 'will-change', 'word-break',
        'word-spacing', 'word-wrap', 'writing-mode', 'z-index', 'zoom'
    ]

    # Python operators
    operators = [
        '=',
        # Comparison
        # '==', '!=', '<', '<=', '>', '>=',
        # Arithmetic
        # '\+', '-', '\*', '\%', '\*\*',
        # In-place
        '\+=', '-=', '\*=', '/=', '\%=', '\~=',
        # Bitwise
        '\^', '\|', '\&', '\~', '>>', '<<',
        '<\!\[CDATA\[', '\]\]>', '^[ \t]{0,100}\.[a-zA-Z0-9\_\-]{1,20}[ ]{0,5}'
    ]

    # Python braces
    braces = [
        '\{', '\}', '\(', '\)', '\[', '\]', '\<[a-zA-Z0-9]{1,}', '\>', '\<\/[a-zA-Z0-9]{1,}', '\/\>', '\*[ ]{0,5}\{', '!\.[a-zA-Z0-9\_\-\.]{1,20}[ ]{0,5}\{',
    ]

    def __init__(self, parent: QtGui.QTextDocument, mode: MODES) -> None:
        super().__init__(parent)

        # Multi-line strings (expression, flag, style)
        self.tri_single = (QtCore.QRegExp("'''"), 1, STYLES['string2'])
        self.tri_double = (QtCore.QRegExp('"""'), 2, STYLES['string2'])
        self.comment_block1 = (QtCore.QRegExp('/\\*'), 3, STYLES['comment'])
        self.comment_block2 = (QtCore.QRegExp('\\*/'), 3, STYLES['comment'])

        rules = []

        # All other rules
        rules += [
            # Numeric literals
            (r'\b[0-9]{1,10}(%|px|em){0,1}', 0, STYLES['numbers']),
            (r'\b[0-9]{1,10}.{0,1}[0-9]{1,10}(%|px|em){0,1}', 0, STYLES['numbers']),
            # COLORS
            (r'#[0-9A-Fa-f]{3,8}', 0, STYLES['numbers']),
            (r'rgb[ ]{0,}\([0-9]{1,3}[ ]{0,}\,[ ]{0,}[0-9]{1,3}[ ]{0,}\,[ ]{0,}[0-9]{1,3}\)', 0, STYLES['numbers']),
            (r'rgba[ ]{0,}\([0-9]{1,3}[ ]{0,}\,[ ]{0,}[0-9]{1,3}[ ]{0,}\,[ ]{0,}[0-9]{1,3}[ ]{0,}\,[ ]{0,}[0-9]{1,3}\)', 0, STYLES['numbers']),

            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string'])
        ]

        # Keyword, operator, and brace rules
        if mode == MODES.HTML:
            rules += [(r'\b%s\b' % w, 0, STYLES['keyword']) for w in SyntaxHighlighter.keywordsHTML]
            rules += [(r'%s' % b, 0, STYLES['brace']) for b in SyntaxHighlighter.braces]
            rules += [(r'%s' % o, 0, STYLES['operator']) for o in SyntaxHighlighter.operators]
            rules += [(r'<!--(.|\r|\n|\t){0,}-->', 0, STYLES['comment'])]
        elif mode == MODES.XML:
            rules += [(r'\b%s\b' % w, 0, STYLES['keyword']) for w in SyntaxHighlighter.keywordsXML]
            rules += [(r'%s' % b, 0, STYLES['brace']) for b in SyntaxHighlighter.braces]
            rules += [(r'%s' % o, 0, STYLES['operator']) for o in SyntaxHighlighter.operators]
            rules += [(r'<!--(.|\r|\n|\t){0,}-->', 0, STYLES['comment'])]
        elif mode == MODES.CSS:
            print("MODE CSS")
            rules += [(r'\b%s\b' % w, 0, STYLES['keyword']) for w in SyntaxHighlighter.keywordsCSS2]
            rules += [(r'%s' % w, 0, STYLES['brace']) for w in SyntaxHighlighter.keywordsCSS1]
            rules += [(r'%s' % o, 0, STYLES['operator']) for o in SyntaxHighlighter.operators]
            rules += [(r'%s' % b, 0, STYLES['brace']) for b in SyntaxHighlighter.braces]
            rules += [(r'//[^\n]*', 0, STYLES['comment']), (r'/\*', 0, STYLES['comment']), (r'/\*([^*]|(\*+([^*/])))*\*+/', 0, STYLES['comment'])]

        # Build a QRegExp for each pattern
        self.rules = [(QtCore.QRegExp(pat), index, fmt)
            for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        self.tripleQuoutesWithinStrings = []
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)
            if index >= 0:
                # if there is a string we check
                # if there are some triple quotes within the string
                # they will be ignored if they are matched again
                if expression.pattern() in [r'"[^"\\]*(\\.[^"\\]*)*"', r"'[^'\\]*(\\.[^'\\]*)*'", r'/\*']:
                    # print(expression.pattern())
                    innerIndex = self.tri_single[0].indexIn(text, index + 1)
                    if innerIndex == -1:
                        innerIndex = self.tri_double[0].indexIn(text, index + 1)

                    if innerIndex == -1:
                        innerIndex = self.comment_block2[0].indexIn(text, index + 1)

                    if innerIndex != -1:
                        tripleQuoteIndexes = range(innerIndex, innerIndex + 3)
                        self.tripleQuoutesWithinStrings.extend(tripleQuoteIndexes)

            while index >= 0:
                # skipping triple quotes within strings
                if index in self.tripleQuoutesWithinStrings:
                    index += 1
                    expression.indexIn(text, index)
                    continue

                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style):
        """Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter.indexIn(text)
            # skipping triple quotes within strings
            if start in self.tripleQuoutesWithinStrings:
                return False
            # Move past this match
            add = delimiter.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False