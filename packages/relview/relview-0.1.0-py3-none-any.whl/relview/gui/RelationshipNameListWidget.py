from Qt import QtCore, QtGui, QtWidgets

from .mixins import RoundedCornersMixin, WidgetColorMixin
from .NamedRelationshipDetailsWidget import NamedRelationshipDetailsWidget
from .utils import FontMods, LayoutMods
from .widgets import InfoLabel


class RelationshipNameListWidget(
    QtWidgets.QWidget, RoundedCornersMixin, WidgetColorMixin
):
    """TODO say what this is"""

    # signals - arguments are PrimRelationshipRecord, QMouseEvent
    PrimClicked = QtCore.Signal(object, object)
    PrimDoubleClicked = QtCore.Signal(object, object)

    # child widget classes
    NAMED_REL_DETAILS_WIDGET_CLASS = NamedRelationshipDetailsWidget

    # color roles/values (see WidgetColorMixin)
    BACKGROUND_ROLE = QtGui.QPalette.Base

    NAME_LABEL_FG_ROLE = QtGui.QPalette.HighlightedText
    NAME_LABEL_FG_COLOR = None

    # constants for sizes of things etc.
    BORDER_RADIUS = 10.0
    LAYOUT_MODS = LayoutMods(contentsMargins=(7, 7, 7, 7), spacing=7)
    REL_NAME_FONT_MODS = FontMods(sizeScale=1.1)

    def __init__(
        self, relationshipRecord, relationshipName, namedRelationships, parent=None
    ):
        super().__init__(parent)

        self._relationshipRecord = relationshipRecord
        self._relationshipName = relationshipName
        self._namedRelationships = namedRelationships

        self._buildUI()

    #
    # slots
    #
    def _namedRelWidgetPrimClickedSLOT(self, relationshipRecord, mouseEvent):
        self.PrimClicked.emit(relationshipRecord, mouseEvent)

    def _namedRelWidgetPrimDoubleClickedSLOT(self, relationshipRecord, mouseEvent):
        self.PrimDoubleClicked.emit(relationshipRecord, mouseEvent)

    #
    # private helper methods
    #
    def _buildUI(self):
        self.applyWidgetColors()

        self._layout = QtWidgets.QVBoxLayout()
        self.LAYOUT_MODS.modify(self._layout)
        self.setLayout(self._layout)

        self._topLineLayout = QtWidgets.QHBoxLayout()
        self._layout.addLayout(self._topLineLayout, 0)

        self._relNameLabel = QtWidgets.QLabel(self._relationshipName, self)
        self.setForegroundColorOf(
            self._relNameLabel, self.NAME_LABEL_FG_ROLE, self.NAME_LABEL_FG_COLOR
        )
        self._relNameLabel.setFont(
            self.REL_NAME_FONT_MODS.getModified(self._relNameLabel.font())
        )
        self._topLineLayout.addWidget(self._relNameLabel, 0, QtCore.Qt.AlignVCenter)

        isEmpty = (
            len(self._namedRelationships) == 1 and self._namedRelationships[0].isEmpty()
        )
        if isEmpty:
            self._topLineLayout.addStretch(1)
            self._emptyInfoLabel = InfoLabel("Empty Relationship", self)
            # TODO tooltip?
            # TODO click handling?
            self._topLineLayout.addWidget(
                self._emptyInfoLabel, 0, QtCore.Qt.AlignVCenter
            )
            return  # that's all!

        for namedRel in self._namedRelationships:
            namedRelWidget = self.NAMED_REL_DETAILS_WIDGET_CLASS(
                namedRel, self._relationshipRecord, self
            )
            self._layout.addWidget(namedRelWidget, 0)
            namedRelWidget.PrimClicked.connect(self._namedRelWidgetPrimClickedSLOT)
            namedRelWidget.PrimDoubleClicked.connect(
                self._namedRelWidgetPrimDoubleClickedSLOT
            )
