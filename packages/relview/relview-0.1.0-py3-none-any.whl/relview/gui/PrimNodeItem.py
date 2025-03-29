from collections import defaultdict

from Qt import QtCore, QtGui, QtWidgets

from . import icons
from .nodeStyling import getNodeStylingForPrimsOfType
from .pixmapCache import getOrCreatePixmapFor
from .svgRendererCache import getOrCreateSvgRendererFor


class PrimNodeItem(QtWidgets.QGraphicsItem):
    """QGraphicsItem representing a USD prim in a RelationshipScene."""

    # signals
    # TODO some signals?

    # class constants (overridable)
    NODE_WIDTH = 306  # pixels
    NODE_HEIGHT = 71  # pixels
    NODE_OUTLINE_WIDTH = 6  # pixels
    NODE_CORNER_RADIUS = 40  # pixels
    NODE_Z_VALUE = 1.0  # on top of wires

    NODE_OUTLINE_COLOR = QtGui.QColor(90, 90, 90)
    NODE_SELECTED_OUTLINE_COLOR = QtGui.QColor(30, 144, 255)
    NODE_BACKGROUND_COLOR = QtGui.QColor(71, 71, 71)
    NODE_TEXT_COLOR = QtGui.QColor(248, 240, 227)

    DEFAULT_FONT_FAMILY = "Roboto"
    NODE_MAIN_FONT = QtGui.QFont(DEFAULT_FONT_FAMILY, 16)
    NODE_SUB_FONT = QtGui.QFont(DEFAULT_FONT_FAMILY, 10)
    NODE_MAIN_TEXT_Y_OFFSET = -15
    NODE_SUB_TEXT_Y_OFFSET = 30

    ALERT_ICON_PATH = icons.WARNING_ICON_PATH

    # instance state
    _boundingBox = None

    def __init__(self, relationshipRecord, parentItem=None):
        super().__init__(parentItem)

        # note: relationshipRecord should be a PrimRelationshipRecord object
        self._relationshipRecord = relationshipRecord

        # grab a few things from the prim, so we don't need to keep asking for
        # them (like while painting)
        prim = self._relationshipRecord.getPrim()
        self._primName = prim.GetName()
        self._primTypeName = prim.GetTypeName()

        self._setOptions()
        self._setToolTipText()
        self._refreshBoundingBox()

    #
    # public API
    #
    def getRelationshipRecord(self):
        return self._relationshipRecord

    def getWidth(self):
        return self.boundingRect().width()

    def getCenterPoint(self):
        return self.mapToScene(self.boundingRect().center())

    #
    # QGraphicsItem overrides
    #
    def boundingRect(self):
        """Return QRect that represents the bounding box of the node."""
        return self._boundingBox

    def paint(self, painter, option, widget=None):
        """A reimplementation of the QGraphicsItem paint method. Responsible for
        drawing the node.
        TODO we probably want to visually indicate if self._relationshipRecord
        has any invalid relationships (with some kind of "Alert!" icon etc.)
        TODO this is a pretty large method - probably want to break it down into
        some smaller ones...
        """
        lod = option.levelOfDetailFromTransform(painter.worldTransform())

        # Resolve fill, text and outlines brush
        textBrush = self.NODE_TEXT_COLOR

        nodeStyling = getNodeStylingForPrimsOfType(self._primTypeName)
        outlineBrush = (
            nodeStyling.getForegroundColor()
            if (nodeStyling and nodeStyling.hasForegroundColor())
            else self.NODE_OUTLINE_COLOR
        )
        if option.state & QtWidgets.QStyle.State_Selected:
            outlineBrush = self.NODE_SELECTED_OUTLINE_COLOR

        # Draw background
        # Create the rounded path
        path = QtGui.QPainterPath()
        # adjust the outer border drawing rectangle such that the width of the
        # pen drawing the outline won't leave the bounding rectangle (assume
        # pen is centered on that path, so reduce by half the pen width)
        halfLineWidth = self.NODE_OUTLINE_WIDTH / 2
        borderDrawRect = self._boundingBox.adjusted(
            halfLineWidth, halfLineWidth, -halfLineWidth, -halfLineWidth
        )
        path.addRoundedRect(
            borderDrawRect, self.NODE_CORNER_RADIUS, self.NODE_CORNER_RADIUS
        )
        painter.setBrush(self.NODE_BACKGROUND_COLOR)
        painter.setPen(QtGui.QPen(outlineBrush, self.NODE_OUTLINE_WIDTH))
        painter.drawPath(path)

        # Draw text etc.
        # TODO refactor below into some smaller methods?
        if lod >= 0.25:  # TODO define breakpoints in constants
            font = self.NODE_MAIN_FONT
            font.setStyleStrategy(QtGui.QFont.ForceOutline)
            painter.setFont(font)
            painter.setPen(QtGui.QPen(textBrush, 1))
            painter.scale(1, 1)
            mainTextBbox = self._boundingBox.adjusted(
                0, self.NODE_MAIN_TEXT_Y_OFFSET, 0, 0
            )
            painter.drawText(mainTextBbox, QtCore.Qt.AlignCenter, self._primName)

            # Draw subtext (prim type name)
            subFont = self.NODE_SUB_FONT
            subFont.setItalic(True)
            painter.setFont(subFont)
            subtxt_bbox = self._boundingBox.adjusted(
                0, self.NODE_SUB_TEXT_Y_OFFSET, 0, 0
            )
            painter.drawText(subtxt_bbox, QtCore.Qt.AlignCenter, self._primTypeName)

            nodeHeight = int(mainTextBbox.height())
            iconSize = nodeHeight // 2
            iconSizeObj = QtCore.QSize(iconSize, iconSize)
            iconSizeFObj = QtCore.QSizeF(iconSize, iconSize)

            # if there's an icon for this prim type, draw it
            if nodeStyling and nodeStyling.hasIcon():
                iconPath = nodeStyling.getIconPath()
                # TODO put icon next to text? (will need font metrics etc)

                paintAt = mainTextBbox.adjusted(
                    10,
                    (nodeHeight // 2) - (iconSize // 3),
                    0,
                    0,
                ).topLeft()
                paintRect = QtCore.QRectF(paintAt, iconSizeFObj)
                # use the SVG renderer if the icon is an SVG, otherwise just render
                # a pixmap
                if nodeStyling.isSvgIcon():
                    svgRenderer = getOrCreateSvgRendererFor(iconPath)
                    svgRenderer.render(painter, paintRect)
                else:
                    painter.drawPixmap(
                        paintAt,
                        getOrCreatePixmapFor(iconPath, iconSizeObj),
                    )

            # if this prim has additional relationships to other prims that aren't
            # being represented in the scene, add a little "+<num>" indicator
            # TODO we'll probably have "ellipsis bubbles" for these "additional
            # relationships" down the road
            if self._relationshipRecord.hasAdditionalToRelationships():
                font = self.NODE_MAIN_FONT
                font.setStyleStrategy(QtGui.QFont.ForceOutline)
                painter.setFont(font)
                painter.setPen(QtGui.QPen(textBrush, 1))
                painter.scale(1, 1)
                numAddtnlTxt = (
                    f"+{self._relationshipRecord.getNumAdditionalToRelationships()}"
                )
                fm = QtGui.QFontMetrics(font)
                textWidth = fm.boundingRect(numAddtnlTxt).width()
                mainTextBbox = self._boundingBox.adjusted(
                    self.NODE_WIDTH - textWidth - 12, 0, 0, 0
                )  # TODO constant for right side padding (if these labels stick around)
                painter.drawText(mainTextBbox, QtCore.Qt.AlignCenter, numAddtnlTxt)

            # if this prim has an invalid relationships, draw the "alert" icon
            # on the right side of the node
            elif self._relationshipRecord.hasAnyInvalidToRelationships():
                nodeWidth = mainTextBbox.width()
                paintAt = mainTextBbox.adjusted(
                    nodeWidth - iconSize - 12,
                    (nodeHeight // 2) - (iconSize // 3),
                    0,
                    0,
                ).topLeft()
                paintRect = QtCore.QRectF(paintAt, iconSizeFObj)
                svgRenderer = getOrCreateSvgRendererFor(self.ALERT_ICON_PATH)
                svgRenderer.render(painter, paintRect)

    #
    # private helper methods
    #
    def _setOptions(self):
        self.setFlags(
            QtWidgets.QGraphicsItem.ItemIsMovable
            | QtWidgets.QGraphicsItem.ItemIsSelectable
            | QtWidgets.QGraphicsItem.ItemSendsGeometryChanges
        )
        self.setAcceptHoverEvents(False)
        self.setZValue(self.NODE_Z_VALUE)

    _noRelsHTMLStr = "  (none)"

    def _setToolTipText(self):
        # don't love all the HTML-in-text (and the   stuff all over, but
        # it's Qt soooo.... :shrug:)
        primPathStr = self._relationshipRecord.getPrimPath().pathString
        # TODO if not self._relationshipRecord.hasAnyRelationships() "(no relationships)"
        toolTipStr = f"""<p>
<b>{self._primName}</b> ({self._primTypeName})<br/>
{primPathStr}
{self._getToRelationshipsStr()}
{self._getFromRelationshipsStr()}
{self._getAdditionalRelationshipsHTMLStr()}
</p>
"""
        toolTipStr = toolTipStr.replace(
            " ", "&nbsp;"
        )  # use non-breaking spaces to avoid wrapping
        self.setToolTip(toolTipStr)

    def _getToRelationshipsStr(self):
        return self._getRelationshipsHTMLFor(
            "Target relationships:", self._relationshipRecord.getToRelationships
        )

    def _getFromRelationshipsStr(self):
        return self._getRelationshipsHTMLFor(
            "Incoming relationships:", self._relationshipRecord.getFromRelationships
        )

    def _getAdditionalRelationshipsHTMLStr(self):
        return self._getRelationshipsHTMLFor(
            "Additional relationships:",
            self._relationshipRecord.getAdditionalToRelationships,
        )

    def _getRelationshipsHTMLFor(self, headingHTMLStr, getRelsFunc):
        return _getHTMLStrForNamedRelationships(
            f"<b>{headingHTMLStr}</b>",
            getRelsFunc(),
        )

    def _refreshBoundingBox(self):
        self._boundingBox = QtCore.QRectF(
            -self.NODE_OUTLINE_WIDTH / 2,
            -self.NODE_OUTLINE_WIDTH / 2,
            self.NODE_WIDTH + self.NODE_OUTLINE_WIDTH,
            self.NODE_HEIGHT + self.NODE_OUTLINE_WIDTH,
        )


#
# little helper functions
#
def _getHTMLStrForNamedRelationships(headingText, namedRels):
    if not namedRels:
        return ""

    return f"<br/><br/>\n{headingText}<br/>\n{_namedRelationshipsToHTMLStr(namedRels)}"


def _namedRelationshipsToHTMLStr(namedRels):
    namedRelsByName = defaultdict(list)
    for namedRel in sorted(namedRels, key=lambda namedRel: namedRel.getName()):
        namedRelsByName[namedRel.getName()].append(namedRel)
    bits = []
    for relName, namedRels in namedRelsByName.items():
        bits.append(f"   <b>{relName}</b>")
        for namedRel in namedRels:
            invalid = namedRel.isInvalid()
            prefix = f"      {'⚠️ ' if invalid else ''}"
            suffix = " (invalid)" if invalid else ""
            bits.append(
                f"{prefix}{'(empty)' if namedRel.isEmpty() else namedRel.getPath().pathString}{suffix}"
            )

    return "<br/>\n".join(bits)
