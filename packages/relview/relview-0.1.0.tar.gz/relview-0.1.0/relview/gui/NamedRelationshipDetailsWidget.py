from Qt import QtCore, QtGui, QtWidgets

from .mixins import ClickableMixin, RoundedCornersMixin, WidgetColorMixin
from .nodeStyling import getIconPathForPrimsOfType
from .pixmapCache import getOrCreatePixmapFor
from .utils import FontMods, LayoutMods
from .widgets import ElidedLabel, WarningLabel


class NamedRelationshipDetailsWidget(
    QtWidgets.QWidget, ClickableMixin, RoundedCornersMixin, WidgetColorMixin
):
    """Widget that displays the details of a NamedRelationship object, that's
    a child of a PrimRelationshipRecord object.
    """

    # signals - arguments are PrimRelationshipRecord, QMouseEvent
    PrimClicked = QtCore.Signal(object, object)
    PrimDoubleClicked = QtCore.Signal(object, object)

    # color stuff (see WidgetColorMixin)
    BACKGROUND_ROLE = QtGui.QPalette.AlternateBase

    # constants for sizes of things etc.
    BORDER_RADIUS = 5.0
    PRIM_TYPE_ICON_SIZE = QtCore.QSize(20, 20)
    PRIM_TYPE_ICON_GAP = 7
    INVALID_LABEL_GAP = 5

    LAYOUT_MODS = LayoutMods(contentsMargins=(7, 7, 7, 7), spacing=0)
    LABELS_LAYOUT_MODS = LayoutMods()  # currently not being modified
    LINE1_LAYOUT_MODS = LayoutMods(spacing=7)
    LINE2_LAYOUT_MODS = LayoutMods(spacing=7)
    NAME_FONT_MODS = FontMods(sizeScale=1.1)

    def __init__(self, namedRelationship, relationshipRecord, parent=None):
        super().__init__(parent)

        self._namedRelationship = namedRelationship
        self._relationshipRecord = relationshipRecord
        self._isInvalidRel = self._namedRelationship.isInvalid()
        self._isPropertyRel = self._namedRelationship.isPropertyRelationship()

        self.applyWidgetColors()

        self._stage = relationshipRecord.getStage()

        primPath = self._namedRelationship.getPrimPath()
        self._primName = primPath.name or ""
        self._primTypeName = None
        prim = self._stage.GetPrimAtPath(primPath)
        if prim:
            self._primTypeName = prim.GetTypeName()

        self._layout = QtWidgets.QHBoxLayout()
        self.LAYOUT_MODS.modify(self._layout)
        self.setLayout(self._layout)

        self._primTypeIconLabel = QtWidgets.QLabel(self)
        self._primTypeIconLabel.setFixedSize(self.PRIM_TYPE_ICON_SIZE)
        primIconPath = (
            getIconPathForPrimsOfType(self._primTypeName)
            if self._primTypeName
            else None
        )
        if primIconPath:
            self._primTypeIconLabel.setPixmap(
                getOrCreatePixmapFor(primIconPath, self.PRIM_TYPE_ICON_SIZE)
            )
        self._layout.addWidget(self._primTypeIconLabel, 0, QtCore.Qt.AlignTop)

        self._layout.addSpacing(self.PRIM_TYPE_ICON_GAP)

        self._labelsLayout = QtWidgets.QVBoxLayout()
        self.LABELS_LAYOUT_MODS.modify(self._labelsLayout)
        self._layout.addLayout(self._labelsLayout, 1)

        self._line1Layout = QtWidgets.QHBoxLayout()
        self.LINE1_LAYOUT_MODS.modify(self._line1Layout)
        self._labelsLayout.addLayout(self._line1Layout, 0)

        biggerFont = self.NAME_FONT_MODS.getModified(self.font())

        self._primNameLabel = QtWidgets.QLabel(self._primName, self)
        self._primNameLabel.setForegroundRole(QtGui.QPalette.HighlightedText)
        self._primNameLabel.setFont(biggerFont)
        self._line1Layout.addWidget(self._primNameLabel, 0, QtCore.Qt.AlignBottom)

        self._primTypeNameLabel = QtWidgets.QLabel(
            self._primTypeName or "(unknown type)", self
        )
        self._line1Layout.addWidget(self._primTypeNameLabel, 0, QtCore.Qt.AlignBottom)

        self._line1Layout.addStretch(1)

        if self._isPropertyRel:
            self._propNameValLabel = QtWidgets.QLabel(
                self._namedRelationship.getPropertyName(), self
            )
            self._propNameValLabel.setFont(biggerFont)
            self._propNameValLabel.setForegroundRole(QtGui.QPalette.HighlightedText)
            self._line1Layout.addWidget(
                self._propNameValLabel, 0, QtCore.Qt.AlignBottom
            )

        self._line2Layout = QtWidgets.QHBoxLayout()
        self.LINE2_LAYOUT_MODS.modify(self._line2Layout)
        self._labelsLayout.addLayout(self._line2Layout, 0)

        self._primPathLabel = ElidedLabel(primPath.pathString, self)
        self._primPathLabel.setToolTip(primPath.pathString)  # in case it gets elided
        self._line2Layout.addWidget(self._primPathLabel, 1, QtCore.Qt.AlignBottom)

        if self._isPropertyRel:
            self._propNameLabel = QtWidgets.QLabel("Property Name", self)
            self._line2Layout.addWidget(self._propNameLabel, 0, QtCore.Qt.AlignVCenter)

        if self._isInvalidRel:
            self._labelsLayout.addSpacing(self.INVALID_LABEL_GAP)
            self._invalidMessageLabel = WarningLabel(
                self._namedRelationship.getInvalidMessage(), self
            )
            # TODO tooltip?
            # TODO click handling?
            self._labelsLayout.addWidget(self._invalidMessageLabel, 0)

    #
    # ClickableMixin overrides
    #
    def _handleClick(self, clickPos, event):
        self.PrimClicked.emit(self._getRelationshipRecordForClick(), event)

    def _handleDoubleClick(self, clickPos, event):
        self.PrimDoubleClicked.emit(self._getRelationshipRecordForClick(), event)

    #
    # private helper methods
    #
    def _getRelationshipRecordForClick(self):
        # because self._relationshipRecord is the _parent_ of self._namedRelationship,
        # it's probably not "the prim" that we want to emit as having been clicked
        # (or double-clicked) - rather, the PrimRelationshipRecord in the relationship
        # collection representing the prim identified by self._namedRelationship
        # is the one we want, so see if the collection has an entry for that, and
        # if it does, Bob's your uncle. (otherwise just ballback to self._relationshipRecord)
        if self._relationshipRecord.hasRelationshipCollection():
            relColl = self._relationshipRecord.getRelationshipCollection()
            thisPrimPath = self._namedRelationship.getPrimPath()
            if relColl.hasRecordFor(thisPrimPath):
                return relColl.getRecordFor(thisPrimPath)

        return self._relationshipRecord
