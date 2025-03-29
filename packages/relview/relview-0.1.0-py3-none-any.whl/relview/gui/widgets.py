from Qt import QtCore, QtGui, QtWidgets

from . import icons
from . import mixins
from .pixmapCache import getOrCreatePixmapFor
from .utils import FontMods, LayoutMods


class ClickableLabel(QtWidgets.QLabel, mixins.ClickableMixin):
    """A QLabel that emits a clicked() signal when clicked, and a doubleClicked()
    signal when double clicked. Easy peasy.
    """

    #
    # signals
    #

    # basic/simple
    clicked = QtCore.Signal()
    doubleClicked = QtCore.Signal()

    # more detailed - arguments are position (QPoint), event (QMouseEvent)
    clickedAt = QtCore.Signal(object, object)
    doubleClickedAt = QtCore.Signal(object, object)

    #
    # ClickableMixin overrides
    #
    def _handleClick(
        self,
        clickPos,
        event,
    ):
        self.clicked.emit()
        self.clickedAt.emit(clickPos, event)

    def _handleDoubleClick(
        self,
        clickPos,
        event,
    ):
        self.doubleClicked.emit()
        self.doubleClickedAt.emit(clickPos, event)


class FilterCountBubble(
    ClickableLabel,
    mixins.HoverMixin,
    mixins.RoundedCornersMixin,
    mixins.WidgetColorMixin,
):
    """Shows a "filter" icon, and when the count is nonzero, a number next to it,
    all in a "bubble" (pill-shaped widget, really).
    """

    # constants for size, colors, etc.
    FILTER_ICON_PATH = icons.FILTER_ICON_PATH
    FILTER_ACTIVE_ICON_PATH = icons.FILTER_ACTIVE_ICON_PATH
    ICON_SIZE = QtCore.QSize(20, 20)
    # ugh don't love having to have a fixed base width like this, but for some
    # reason this widget's width gets squeezed to nothing otherwise :thinking-face:
    NORMAL_WIDTH = 35
    DEFAULT_ALIGNMENT = QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter

    ACTIVE_BACKGROUND_ROLE = QtGui.QPalette.Highlight
    ACTIVE_BACKGROUND_COLOR = None
    ACTIVE_FOREGROUND_ROLE = QtGui.QPalette.HighlightedText
    ACTIVE_FOREGROUND_COLOR = None

    BG_HOVER_LIGHTER_BY = 115  # how much to brighten bbackground by when hovering

    LAYOUT_MODS = LayoutMods(contentsMargins=(7, 2, 7, 2), spacing=6)
    COUNT_LABEL_FONT_MODS = FontMods(bold=True, sizeScale=1.2)

    # instance state
    _count = 0

    def __init__(self, parentWidget=None):
        super().__init__(parentWidget)
        self._initPixmaps()
        self._initColors()
        self._buildUI()
        self.setCount(self._count)

    def getCount(self):
        return self._count

    def setCount(self, count):
        changingPixmap = (not self._count and count) or (self._count and not count)
        self._count = count
        if changingPixmap:
            self._pixmapLabel.setPixmap(
                self._filtersActivePixmap if self._count else self._filtersPixmap
            )
            self._pixmapLabel.update()
        self._countLabel.setText(str(self._count) if self._count else "")
        self._countLabel.setVisible(self._count > 0)
        self._countLabel.setFixedSize(self._countLabel.sizeHint())
        self._updateStyling()
        if self._count:
            wid = self.NORMAL_WIDTH + self._layout.spacing()
            fm = QtGui.QFontMetrics(self._countLabel.font())
            wid += fm.boundingRect(self._countLabel.text()).width()
            self.setFixedWidth(wid)
        else:
            self.setFixedWidth(self.NORMAL_WIDTH)

    #
    # RoundedCornersMixin overrides
    #
    def getBorderRadius(self):
        return self.height() / 2

    #
    # HoverMixin overrides
    #
    def _handleHoverEntered(self):
        self._updateStyling()

    def _handleHoverLeft(self):
        self._updateStyling()

    #
    # private helper methods
    #
    def _initPixmaps(self):
        self._filtersPixmap = getOrCreatePixmapFor(
            self.FILTER_ICON_PATH, self.ICON_SIZE
        )
        self._filtersActivePixmap = getOrCreatePixmapFor(
            self.FILTER_ACTIVE_ICON_PATH, self.ICON_SIZE
        )

    def _initColors(self):
        palette = self.palette()

        # normal (not active, no count) colors
        self._normalBGColor = palette.color(self.backgroundRole())
        self._normalBGHoverColor = self._normalBGColor.lighter(self.BG_HOVER_LIGHTER_BY)
        self._normalFGColor = palette.color(self.foregroundRole())

        # active (count > 0) colors
        self._activeBGColor = self.ACTIVE_BACKGROUND_COLOR or palette.color(
            self.ACTIVE_BACKGROUND_ROLE
        )
        self._activeBGHoverColor = self._activeBGColor.lighter(self.BG_HOVER_LIGHTER_BY)
        self._activeFGColor = self.ACTIVE_FOREGROUND_COLOR or palette.color(
            self.ACTIVE_FOREGROUND_ROLE
        )

    def _buildUI(self):
        self._layout = QtWidgets.QHBoxLayout()
        self.LAYOUT_MODS.modify(self._layout)
        self.setLayout(self._layout)

        self._pixmapLabel = QtWidgets.QLabel(self)
        self._pixmapLabel.setPixmap(self._filtersPixmap)
        self._pixmapLabel.setFixedSize(self.ICON_SIZE)
        self._layout.addWidget(self._pixmapLabel, 0, QtCore.Qt.AlignVCenter)

        self._countLabel = QtWidgets.QLabel(self)
        self._countLabel.setFont(
            self.COUNT_LABEL_FONT_MODS.getModified(self._countLabel.font())
        )
        self._layout.addWidget(self._countLabel, 0, QtCore.Qt.AlignVCenter)

    def _updateStyling(self):
        active = self._count > 0
        hover = self.isMouseHovering()
        if active:
            bgColor = self._activeBGHoverColor if hover else self._activeBGColor
            fgColor = self._activeFGColor
        else:
            bgColor = self._normalBGHoverColor if hover else self._normalBGColor
            fgColor = self._normalFGColor
        self.setBackgroundColorOf(self, colorVal=bgColor)
        self.setForegroundColorOf(self, colorVal=fgColor)


class ElidedLabel(QtWidgets.QLabel):
    """A QLabel whose text gets elided if the width isn't long enough to display
    the full string. Note that this is meant for single-line, simple strings only,
    not some multi-line fancy thing (rich text, text with links, etc.).
    """

    LEFT_MARGIN = 3
    RIGHT_MARGIN = 5
    DEFAULT_ELIDE_MODE = QtCore.Qt.ElideMiddle

    def __init__(self, text="", parent=None):
        super().__init__(parent)

        self._textStr = text

        self.setWordWrap(False)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        self._elideMode = self.DEFAULT_ELIDE_MODE

    #
    # public API
    #
    def getElideMode(self):
        return self._elideMode

    def setElideMode(self, elideMode):
        # note: elideMode should be QtCore.Qt.ElideMiddle, QtCore.Qt.ElideLeft, or
        # QtCore.Qt.ElideRight
        self._elideMode = elideMode
        self.update()

    #
    # QLabel overrides - note: don't want QLabel to know about the text string,
    # since it will size itself based on that, which we don't want
    #
    def text(self):
        return self._textStr

    def setText(self, text):
        if text != self._textStr:
            self._textStr = text
            self.update()

    def paintEvent(self, event):
        QtWidgets.QFrame.paintEvent(self, event)

        font = self.font()
        painter = QtGui.QPainter(self)
        painter.setFont(font)
        fontMetrics = painter.fontMetrics()
        textStr = self.text()
        textLayout = QtGui.QTextLayout(textStr, font)
        textLayout.beginLayout()

        line = textLayout.createLine()
        width = self.width()
        line.setLineWidth(width)

        lastLine = textStr[line.textStart() :]
        elidedLastLine = fontMetrics.elidedText(
            lastLine, self._elideMode, width - self.RIGHT_MARGIN
        )
        rect = QtCore.QRectF(
            self.LEFT_MARGIN, 0, width - self.RIGHT_MARGIN, self.height()
        )
        painter.setPen(self.palette().color(self.foregroundRole()))
        painter.drawText(
            rect,
            self.alignment() | QtCore.Qt.AlignVCenter | QtCore.Qt.TextSingleLine,
            elidedLastLine,
        )
        textLayout.endLayout()


class StatusInfoLabel(
    QtWidgets.QWidget,
    mixins.ClickableMixin,
    mixins.RoundedCornersMixin,
    mixins.WidgetColorMixin,
):
    """Base class for different kinds of informational labels, that have an icon
    on the left with some helpful text to the right. See InfoLabel and WarningLabel,
    below, for examples.
    """

    BORDER_RADIUS = 5.0
    ICON_PATH = ""  # subclasses should set this
    ICON_SIZE = QtCore.QSize(20, 20)
    LAYOUT_MODS = LayoutMods(contentsMargins=(5, 5, 5, 5), spacing=5)

    def __init__(self, text, parent=None):
        super().__init__(parent)
        self._text = text
        self._buildUI()
        self.applyWidgetColors()

    def _buildUI(self):
        self._layout = QtWidgets.QHBoxLayout()
        self.LAYOUT_MODS.modify(self._layout)
        self.setLayout(self._layout)

        self._iconLabel = QtWidgets.QLabel(self)
        self._iconLabel.setPixmap(getOrCreatePixmapFor(self.ICON_PATH, self.ICON_SIZE))
        self._iconLabel.setFixedSize(self.ICON_SIZE)
        self._layout.addWidget(self._iconLabel, 0, QtCore.Qt.AlignVCenter)

        self._textLabel = QtWidgets.QLabel(self._text, self)
        self._layout.addWidget(self._textLabel, 1, QtCore.Qt.AlignVCenter)


class InfoLabel(StatusInfoLabel):
    """Shows the provided text with an "information" label to the left, with
    a darkish blue background color and bright text.
    """

    BACKGROUND_COLOR = QtGui.QColor(42, 56, 66)
    FOREGROUND_COLOR = QtGui.QColor(252, 252, 252)
    ICON_PATH = icons.INFO_ICON_PATH


class WarningLabel(StatusInfoLabel):
    """Shows the provided text with a "warning" label to the left, with
    a darkish red background color and bright text.
    """

    BACKGROUND_COLOR = QtGui.QColor(92, 56, 55)
    FOREGROUND_COLOR = QtGui.QColor(252, 252, 252)
    ICON_PATH = icons.WARNING_ICON_PATH
