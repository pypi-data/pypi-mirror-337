from Qt import QtCore, QtGui, QtWidgets

from .mixins import WidgetColorMixin
from .RelationshipRecordDetail import RelationshipRecordDetail
from .utils import LayoutMods


class RelationshipDetailViewer(QtWidgets.QScrollArea, WidgetColorMixin):
    """Scrolling widget that displays the details of a set of RelationshipRecord
    objects, by arranging a series of RelationshipRecordDetail objects in a vertical
    arrangement, with horizontal lines between them.
    """

    # signals - arguments are PrimRelationshipRecord, QMouseEvent
    PrimClicked = QtCore.Signal(object, object)
    PrimDoubleClicked = QtCore.Signal(object, object)

    # child widget classes
    REL_DETAIL_WIDGET_CLASS = RelationshipRecordDetail

    # child widget color roles/values (see WidgetColorMixin)
    EMPTY_LABEL_BG_ROLE = QtGui.QPalette.Dark
    EMPTY_LABEL_BG_COLOR = None

    EMPTY_LABEL_FG_ROLE = None
    EMPTY_LABEL_FG_COLOR = None

    WIDGET_BG_ROLE = QtGui.QPalette.Dark
    WIDGET_BG_COLOR = None

    WIDGET_FG_ROLE = None
    WIDGET_FG_COLOR = None

    REL_DETAIL_BG_ROLE = None
    REL_DETAIL_BG_COLOR = None

    # constants for sizes of things etc.
    LAYOUT_MODS = LayoutMods(contentsMargins=(5, 5, 5, 5), spacing=5)
    DIVIDER_LINE_HEIGHT = 30

    def __init__(self, parent=None):
        super().__init__(parent)

        self._detailWidgets = []
        self._dividerLines = []

        self._buildUI()

    #
    # public API
    #
    def setRecords(self, relationshipRecords):
        self._clear()
        self._showEmpty(not relationshipRecords)
        self._createDetailWidgetsFor(relationshipRecords)

    #
    # slots
    #
    def _detailWidPrimClickedSLOT(self, relationshipRecord, mouseEvent):
        self.PrimClicked.emit(relationshipRecord, mouseEvent)

    def _detailWidPrimDoubleClickedSLOT(self, relationshipRecord, mouseEvent):
        self.PrimDoubleClicked.emit(relationshipRecord, mouseEvent)

    #
    # private helper methods
    #
    def _buildUI(self):
        self.setWidgetResizable(True)

        self._emptyLabel = QtWidgets.QLabel("(no selection)", self)
        self._emptyLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.setBackgroundColorOf(
            self._emptyLabel, self.EMPTY_LABEL_BG_ROLE, self.EMPTY_LABEL_BG_COLOR
        )
        self.setForegroundColorOf(
            self._emptyLabel, self.EMPTY_LABEL_FG_ROLE, self.EMPTY_LABEL_FG_COLOR
        )

        self._widget = QtWidgets.QWidget(self)
        self.setBackgroundColorOf(
            self._widget, self.WIDGET_BG_ROLE, self.WIDGET_BG_COLOR
        )
        self.setForegroundColorOf(
            self._widget, self.WIDGET_FG_ROLE, self.WIDGET_FG_COLOR
        )

        self._showEmpty(True)

        self._layout = QtWidgets.QVBoxLayout()
        self.LAYOUT_MODS.modify(self._layout)
        self._layout.addStretch(1)  # stretchy area at bottom - so insert above
        self._widget.setLayout(self._layout)

    def _showEmpty(self, show):
        _ = self.takeWidget()
        # note: reparenting to self since calling setWidget() unparents the current
        # widget ugh
        self._emptyLabel.setParent(self)
        self._emptyLabel.setVisible(show)
        self._widget.setParent(self)
        self._widget.setVisible(not show)
        self.setWidget(self._emptyLabel if show else self._widget)

    def _createDetailWidgetsFor(self, relationshipRecords):
        lastIdx = len(relationshipRecords) - 1
        for idx, relRecord in enumerate(relationshipRecords):
            self._addDetailWidgetFor(relRecord)
            if idx < lastIdx:
                self._addDividerLine()

    def _addDetailWidgetFor(self, relRecord):
        detailWidget = self.REL_DETAIL_WIDGET_CLASS(relRecord, self._widget)
        self.setBackgroundColorOf(
            detailWidget, self.REL_DETAIL_BG_ROLE, self.REL_DETAIL_BG_COLOR
        )
        self._addWidgetToLayout(detailWidget, 0)
        self._detailWidgets.append(detailWidget)
        detailWidget.PrimClicked.connect(self._detailWidPrimClickedSLOT)
        detailWidget.PrimDoubleClicked.connect(self._detailWidPrimDoubleClickedSLOT)

    def _addDividerLine(self):
        dividerLine = QtWidgets.QFrame(self._widget)
        dividerLine.setFrameShape(QtWidgets.QFrame.HLine)
        dividerLine.setFixedHeight(self.DIVIDER_LINE_HEIGHT)
        self._addWidgetToLayout(dividerLine, 0)
        self._dividerLines.append(dividerLine)

    def _addWidgetToLayout(self, widget, *args):
        self._layout.insertWidget(self._layout.count() - 1, widget, *args)

    def _clear(self):
        for childWidget in self._detailWidgets + self._dividerLines:
            self._layout.removeWidget(childWidget)
            childWidget.setParent(None)
            childWidget.deleteLater()
        self._detailWidgets = []
        self._dividerLines = []
