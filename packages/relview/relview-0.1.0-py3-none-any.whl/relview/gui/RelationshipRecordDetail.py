from Qt import QtCore, QtWidgets, QtGui

from .mixins import ClickableMixin, WidgetColorMixin
from .nodeStyling import getIconPathForPrimsOfType
from .pixmapCache import getOrCreatePixmapFor
from .RelationshipNameListWidget import RelationshipNameListWidget
from .utils import FontMods, LayoutMods
from .widgets import ElidedLabel


class RelationshipRecordDetail(QtWidgets.QWidget, ClickableMixin, WidgetColorMixin):
    """This widget shows the details of a PrimRelationshipRecord object, via
    a series of RelationshipNameListWidgets.
    """

    # signals - arguments are PrimRelationshipRecord, QMouseEvent
    PrimClicked = QtCore.Signal(object, object)
    PrimDoubleClicked = QtCore.Signal(object, object)

    # child widget classes
    REL_NAME_LIST_WIDGET_CLASS = RelationshipNameListWidget

    # child widget color roles/values (see WidgetColorMixin)
    STANDOUT_FG_ROLE = QtGui.QPalette.HighlightedText
    STANDOUT_FG_COLOR = None

    NORMAL_FG_ROLE = QtGui.QPalette.Text
    NORMAL_FG_COLOR = None

    # constants for sizes of things etc.
    TOP_LAYOUT_MODS = LayoutMods(contentsMargins=(0, 0, 0, 0), spacing=0)
    TOP_LINE_LAYOUT_MODS = LayoutMods(contentsMargins=(0, 0, 0, 0), spacing=7)

    PRIM_TYPE_ICON_SIZE = QtCore.QSize(24, 24)

    HEADER_FONT_MODS = FontMods(sizeScale=1.8, bold=True)
    SECTION_FONT_MODS = FontMods(sizeScale=1.3, bold=True)
    PRIM_TYPE_FONT_MODS = FontMods(sizeScale=1.3)
    PRIM_PATH_FONT_MODS = FontMods(sizeScale=1.3)

    SPACING_BEFORE_SECTION = 10
    SPACING_BEFORE_NAMED_REL = 7

    def __init__(self, relationshipRecord, parent=None):
        super().__init__(parent)

        self._relationshipRecord = relationshipRecord

        # grab some prim stuff
        prim = self._relationshipRecord.getPrim()
        primName = prim.GetName()
        primTypeName = prim.GetTypeName()

        # font stuff
        incomingFont = self.font()
        self._headerFont = self.HEADER_FONT_MODS.getModified(incomingFont)
        self._sectionFont = self.SECTION_FONT_MODS.getModified(incomingFont)
        self._primTypeFont = self.PRIM_TYPE_FONT_MODS.getModified(incomingFont)
        self._primPathFont = self.PRIM_PATH_FONT_MODS.getModified(incomingFont)

        # build it
        self._layout = QtWidgets.QVBoxLayout()
        self.TOP_LAYOUT_MODS.modify(self._layout)
        self.setLayout(self._layout)

        # create identification widgets for the prim whose relationships have been
        # captured in the PrimRelationshipRecord passed in to this object,
        # self._relationshipRecord
        self._topLineLayout = QtWidgets.QHBoxLayout()
        self.TOP_LINE_LAYOUT_MODS.modify(self._topLineLayout)
        self._layout.addLayout(self._topLineLayout, 0)

        primIconPath = getIconPathForPrimsOfType(primTypeName)
        if primIconPath:
            self._primTypeIconLabel = QtWidgets.QLabel(self)
            self._primTypeIconLabel.setPixmap(
                getOrCreatePixmapFor(primIconPath, self.PRIM_TYPE_ICON_SIZE)
            )
            self._topLineLayout.addWidget(
                self._primTypeIconLabel, 0, QtCore.Qt.AlignTop
            )

        self._primNameLabel = self._createLabelWith(
            primName,
            font=self._headerFont,
            foregroundRole=self.STANDOUT_FG_ROLE,
            foregroundColor=self.STANDOUT_FG_COLOR,
        )
        self._topLineLayout.addWidget(self._primNameLabel, 0, QtCore.Qt.AlignBottom)

        self._primTypeNameLabel = self._createLabelWith(
            primTypeName,
            foregroundRole=self.NORMAL_FG_ROLE,
            foregroundColor=self.NORMAL_FG_COLOR,
        )
        self._primTypeNameLabel.setFont(self._primTypeFont)
        self._topLineLayout.addWidget(self._primTypeNameLabel, 0, QtCore.Qt.AlignBottom)

        self._topLineLayout.addStretch(1)

        primPathStr = self._relationshipRecord.getPrimPath().pathString
        self._primPathLabel = self._createLabelWith(
            primPathStr,
            foregroundRole=self.NORMAL_FG_ROLE,
            foregroundColor=self.NORMAL_FG_COLOR,
            labelClass=ElidedLabel,
        )
        self._primPathLabel.setToolTip(primPathStr)  # in case it gets elided
        self._primPathLabel.setFont(self._primPathFont)
        self._layout.addWidget(self._primPathLabel, 0)

        if not self._relationshipRecord.hasAnyRelationships():
            self._addNoRelationshipsLabel()
            return

        if self._relationshipRecord.hasToRelationships():
            self._addToRelationshipDetails()

        if self._relationshipRecord.hasFromRelationships():
            self._addFromRelationshipDetails()

        if self._relationshipRecord.hasAdditionalToRelationships():
            self._addAdditionalRelationshipDetails()

    #
    # ClickableMixin overrides
    #
    def _handleClick(self, clickPos, event):
        self.PrimClicked.emit(self._relationshipRecord, event)

    def _handleDoubleClick(self, clickPos, event):
        self.PrimDoubleClicked.emit(self._relationshipRecord, event)

    #
    # slots
    #
    def _relNameListWidPrimClickedSLOT(self, relationshipRecord, mouseEvent):
        self.PrimClicked.emit(relationshipRecord, mouseEvent)

    def _relNameListWidPrimDoubleClickedSLOT(self, relationshipRecord, mouseEvent):
        self.PrimDoubleClicked.emit(relationshipRecord, mouseEvent)

    #
    # private helper methods
    #
    def _addNoRelationshipsLabel(self):
        self._layout.addSpacing(self.SPACING_BEFORE_SECTION)
        self._noRelationshipsLabel = self._createLabelWith(
            "(no relationships)",
            foregroundRole=self.STANDOUT_FG_ROLE,
            foregroundColor=self.STANDOUT_FG_COLOR,
            font=self._sectionFont,
        )
        self._layout.addWidget(self._noRelationshipsLabel, 0)

    def _addToRelationshipDetails(self):
        self._layout.addSpacing(self.SPACING_BEFORE_SECTION)
        self._relationshipsToLabel = self._createLabelWith(
            "Target relationships",
            foregroundRole=self.STANDOUT_FG_ROLE,
            foregroundColor=self.STANDOUT_FG_COLOR,
            font=self._sectionFont,
        )
        self._layout.addWidget(self._relationshipsToLabel, 0)
        self._addRelNameListWidgetsFor(
            self._relationshipRecord.getToRelationshipNames(),
            self._relationshipRecord.getToRelationshipsNamed,
        )

    def _addFromRelationshipDetails(self):
        self._layout.addSpacing(self.SPACING_BEFORE_SECTION)
        self._relationshipsFromLabel = self._createLabelWith(
            "Incoming relationships",
            foregroundRole=self.STANDOUT_FG_ROLE,
            foregroundColor=self.STANDOUT_FG_COLOR,
            font=self._sectionFont,
        )
        self._layout.addWidget(self._relationshipsFromLabel, 0)
        self._addRelNameListWidgetsFor(
            self._relationshipRecord.getFromRelationshipNames(),
            self._relationshipRecord.getFromRelationshipsNamed,
        )

    def _addAdditionalRelationshipDetails(self):
        self._layout.addSpacing(self.SPACING_BEFORE_SECTION)
        self._additionalRelsLabel = self._createLabelWith(
            "Additional relationships",
            foregroundRole=self.STANDOUT_FG_ROLE,
            foregroundColor=self.STANDOUT_FG_COLOR,
            font=self._sectionFont,
        )
        self._layout.addWidget(self._additionalRelsLabel, 0)
        self._addRelNameListWidgetsFor(
            self._relationshipRecord.getAdditionalToRelationshipNames(),
            self._relationshipRecord.getAdditionalToRelationshipsNamed,
        )

    def _createLabelWith(
        self,
        text,
        foregroundRole=None,
        foregroundColor=None,
        font=None,
        labelClass=QtWidgets.QLabel,
    ):
        labelWid = labelClass(text, self)
        self.setForegroundColorOf(labelWid, foregroundRole, foregroundColor)
        if font:
            labelWid.setFont(font)
        return labelWid

    def _addRelNameListWidgetsFor(self, relNames, getForNameFunc):
        for relName in relNames:
            self._layout.addSpacing(self.SPACING_BEFORE_SECTION)
            namedRels = getForNameFunc(relName)
            relNameListWid = self.REL_NAME_LIST_WIDGET_CLASS(
                self._relationshipRecord, relName, namedRels, self
            )
            self._layout.addWidget(relNameListWid, 0)
            relNameListWid.PrimClicked.connect(self._relNameListWidPrimClickedSLOT)
            relNameListWid.PrimDoubleClicked.connect(
                self._relNameListWidPrimDoubleClickedSLOT
            )
