import math

from Qt import QtCore, QtGui, QtWidgets

from .PrimNodeItem import PrimNodeItem


PIOVER3 = math.pi / 3.0  # used below


class RelationshipWireItem(QtWidgets.QGraphicsPathItem):
    """QGraphicsPathItem for a wire that represents one or more relationships
    between two prims (two PrimNodeItem objects). Note that although the two
    node items provided are listed as "from" and "to", there could actually
    be relationships going the opposite direction as well - so potentially
    bidirectional.
    """

    # class variables
    WIRE_COLOR = QtGui.QColor(191, 191, 191)
    WIRE_SELECTED_COLOR = PrimNodeItem.NODE_SELECTED_OUTLINE_COLOR
    WIRE_STYLE = QtCore.Qt.SolidLine
    WIRE_WIDTH = 2
    WIRE_Z_VALUE = 0.0  # beneath nodes
    ARROW_HEIGHT = 14  # pixels

    # some instance state
    _lod = 1
    _line = None
    _shape = None

    def __init__(self, fromNodeItem, toNodeItem, parentItem=None):
        super().__init__(parentItem)

        self.setFlags(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.setZValue(self.WIRE_Z_VALUE)

        self._fromNodeItem = fromNodeItem
        self._toNodeItem = toNodeItem

        self._fromNodeRecord = self._fromNodeItem.getRelationshipRecord()
        self._toNodeRecord = self._toNodeItem.getRelationshipRecord()
        self._fromPath = self._fromNodeRecord.getPrimPath()
        self._toPath = self._toNodeRecord.getPrimPath()
        self._forwardRels = [
            rel
            for rel in self._fromNodeRecord.getToRelationships()
            if rel.getPrimPath() == self._toPath
        ]
        self._backwardRels = [
            rel
            for rel in self._toNodeRecord.getToRelationships()
            if rel.getPrimPath() == self._fromPath
        ]
        self._isBidirectional = bool(self._forwardRels) and bool(self._backwardRels)

        self._setToolTipText()

        # Update position, line and path
        self._update()

    #
    # public API
    #
    def getFromNodeItem(self):
        return self._fromNodeItem

    def getToNodeItem(self):
        return self._toNodeItem

    def getNodeItems(self):
        # wire goes "from" to "to"
        return self._fromNodeItem, self._toNodeItem

    def refresh(self):
        """Update start/end position if provided and force redraw."""
        self.prepareGeometryChange()
        self.update()

    def isBidirectional(self):
        return self._isBidirectional

    #
    # QGraphicsPathItem overrides
    #
    def update(self):
        # Update start, end, path and position before updating
        self._update()
        super().update()

    def shape(self):
        """Re-implement shape method to return a QPainterPath that represents the
        bounding shape.
        """
        return self._shape

    def boundingRect(self):
        # Infer bounding box from shape
        return self._shape.controlPointRect()

    def paint(self, painter, option, widget=None):
        # note: innerLine is the one we draw, outerLine is the one whose endpoints
        # we use for the arrowhead locations
        outerLine, innerLine = self._getLinesForDrawing()
        if not outerLine:
            # we ain't drawing, for whatever reason (nodes too close together etc.)
            return

        # first draw the line
        # TODO set any options on painter? (anti-aliasing etc.)
        # TODO consider self._lod in drawing of things etc.
        wireColor = (
            self.WIRE_SELECTED_COLOR
            if option.state & QtWidgets.QStyle.State_Selected
            else self.WIRE_COLOR
        )
        linePen = QtGui.QPen(wireColor, self.WIRE_WIDTH)
        linePen.setStyle(self.WIRE_STYLE)
        painter.setPen(QtGui.QPen(wireColor, 1))
        painter.setBrush(wireColor)
        painter.drawLine(innerLine)

        # now draw the arrowheads
        # Note: reversing the line start and end points here since the arrowhead
        # painting algorithm is based on arrow _start_ points, not ends (TODO
        # fix the drawing so we don't need to do this)
        # linesNeedingArrowheads = [outerLine]  # see above
        linesNeedingArrowheads = [QtCore.QLineF(outerLine.p2(), outerLine.p1())]
        if self.isBidirectional():
            # linesNeedingArrowheads.append(
            #     QtCore.QLineF(outerLine.p2(), outerLine.p1())
            # )  # see above
            linesNeedingArrowheads.append(outerLine)

        for line in linesNeedingArrowheads:
            angle = math.atan2(-line.dy(), line.dx())
            arrowP1 = line.p1() + QtCore.QPointF(
                math.sin(angle + PIOVER3) * self.ARROW_HEIGHT,
                math.cos(angle + PIOVER3) * self.ARROW_HEIGHT,
            )
            arrowP2 = line.p1() + QtCore.QPointF(
                math.sin(angle + math.pi - PIOVER3) * self.ARROW_HEIGHT,
                math.cos(angle + math.pi - PIOVER3) * self.ARROW_HEIGHT,
            )
            arrowHead = QtGui.QPolygonF([line.p1(), arrowP1, arrowP2])
            painter.drawPolygon(arrowHead)

    #
    # private helper methods
    #
    def _setToolTipText(self):
        ttBits = ["<p>"]
        if self._forwardRels:
            ttBits.append(
                f"From:<br/>  {self._fromPath}<br/>To:<br/>  {self._toPath}:<br/>"
            )
            ttBits += _getTTTextBitsFor(self._forwardRels)
        if self._backwardRels:
            if self._forwardRels:
                ttBits.append("<br/><br/>\n\n\n")
            ttBits.append(
                f"From:<br/>  {self._toPath}<br/>To:<br/>  {self._fromPath}:<br/>"
            )
            ttBits += _getTTTextBitsFor(self._backwardRels)
        ttBits.append("</p>")
        ttText = "\n".join(ttBits)
        ttText = ttText.replace(
            " ", "&nbsp;"
        )  # use non-breaking spaces to avoid wrapping
        self.setToolTip(ttText)

    def _update(self):
        self._updatePosition()
        self._updateLine()
        self._updatePath()

    def _updateLine(self):
        """Resolve start and end point from current source and target position"""
        start = QtCore.QPointF(0, 0)
        end = self._toNodeItem.getCenterPoint() - self._fromNodeItem.getCenterPoint()
        self._line = QtCore.QLineF(start, end)

    def _updatePath(self):
        """Build path which drives shape and bounding box"""
        # start with the "thickened line"
        width = 1 / self._lod if self.WIRE_WIDTH * self._lod < 1 else self.WIRE_WIDTH
        norm = self._line.unitVector().normalVector()
        norm = width * QtCore.QPointF(norm.x2() - norm.x1(), norm.y2() - norm.y1())

        self._shape = QtGui.QPainterPath()
        poly = QtGui.QPolygonF(
            [
                self._line.p1() - norm,
                self._line.p1() + norm,
                self._line.p2() + norm,
                self._line.p2() - norm,
            ]
        )
        self._shape.addPolygon(poly)
        self._shape.closeSubpath()

        # subtract the overlapping areas of the from and to nodes
        # Note: we're extending the bounding rectangles of the nodes by half of
        # PrimNodeItem.NODE_OUTLINE_WIDTH in each dimension first, so there's a
        # small gap between the ends of the wire lines and the node items
        nodePadding = PrimNodeItem.NODE_OUTLINE_WIDTH / 2
        fromNodeRect = self._fromNodeItem.boundingRect()
        expandedFromNodeRect = fromNodeRect.adjusted(
            -nodePadding,
            -nodePadding,
            nodePadding,
            nodePadding,
        )
        fromPath = QtGui.QPainterPath()
        fromPath.addRect(expandedFromNodeRect)

        toNodeRect = self._fromNodeItem.boundingRect()
        expandedToNodeRect = toNodeRect.adjusted(
            -nodePadding,
            -nodePadding,
            nodePadding,
            nodePadding,
        )
        toPath = QtGui.QPainterPath()
        toPath.addRect(expandedToNodeRect)

        self._shape = self._shape.subtracted(
            self.mapFromItem(self._fromNodeItem, fromPath)
        )
        self._shape = self._shape.subtracted(self.mapFromItem(self._toNodeItem, toPath))

        # also capture the shape of the line to be drawn in paint(), since we
        # want the line to be drawn only to the middle of the arrowheads, so no
        # little line pieces will stick out
        linePaddingAmount = nodePadding * 3 / 2
        moreExpandedToNodeRect = toNodeRect.adjusted(
            -linePaddingAmount,
            -linePaddingAmount,
            linePaddingAmount,
            linePaddingAmount,
        )
        moreExpandedToPath = QtGui.QPainterPath()
        moreExpandedToPath.addRect(moreExpandedToNodeRect)
        self._lineShape = QtGui.QPainterPath(self._shape)
        self._lineShape = self._lineShape.subtracted(
            self.mapFromItem(self._toNodeItem, moreExpandedToPath)
        )
        if self.isBidirectional():
            moreExpandedFromNodeRect = fromNodeRect.adjusted(
                -linePaddingAmount,
                -linePaddingAmount,
                linePaddingAmount,
                linePaddingAmount,
            )
            moreExpandedFromPath = QtGui.QPainterPath()
            moreExpandedFromPath.addRect(moreExpandedFromNodeRect)
            self._lineShape = self._lineShape.subtracted(
                self.mapFromItem(self._fromNodeItem, moreExpandedFromPath)
            )

    def _updatePosition(self):
        """Update position to match center of from node item"""
        self.setPos(self._fromNodeItem.getCenterPoint())

    def _getLinesForDrawing(self):
        shapeRect = self._shape.boundingRect()
        shortenedShapeRect = self._lineShape.boundingRect()
        bidir = self.isBidirectional()
        # TODO proooobably a better way to do this (below), eh?
        isLineBackwards = self._line.p1().x() > self._line.p2().x()
        isLineUpsideDown = self._line.p1().y() > self._line.p2().y()
        if isLineBackwards:
            if isLineUpsideDown:
                startPoint, endPoint = shapeRect.bottomRight(), shapeRect.topLeft()
                innerStart, innerEnd = (
                    shortenedShapeRect.bottomRight() if bidir else startPoint
                ), shortenedShapeRect.topLeft()
            else:
                startPoint, endPoint = shapeRect.topRight(), shapeRect.bottomLeft()
                innerStart, innerEnd = (
                    shortenedShapeRect.topRight() if bidir else startPoint
                ), shortenedShapeRect.bottomLeft()
        else:
            if isLineUpsideDown:
                startPoint, endPoint = shapeRect.bottomLeft(), shapeRect.topRight()
                innerStart, innerEnd = (
                    shortenedShapeRect.bottomLeft() if bidir else startPoint
                ), shortenedShapeRect.topRight()
            else:
                startPoint, endPoint = shapeRect.topLeft(), shapeRect.bottomRight()
                innerStart, innerEnd = (
                    shortenedShapeRect.topLeft() if bidir else startPoint
                ), shortenedShapeRect.bottomRight()
        # TODO a better way to do this (above)

        outerLine = QtCore.QLineF(startPoint, endPoint)
        innerLine = QtCore.QLineF(innerStart, innerEnd)
        minLengthNeeded = self.ARROW_HEIGHT * 2 if bidir else self.ARROW_HEIGHT
        outerLine = outerLine if outerLine.length() >= minLengthNeeded else None
        return outerLine, innerLine


#
# some little helper functions
#
def _getTTTextBitsFor(namedRels):
    bits = []
    lastIdx = len(namedRels) - 1
    for idx, namedRel in enumerate(namedRels):
        relText = f"    <b>{namedRel.getName()}</b>"
        if namedRel.isPropertyRelationship():
            relText += f" ({namedRel.getPropertyName()})"
        if idx < lastIdx:
            # don't want line break on last one
            relText += "<br/>"
        bits.append(relText)
    return bits
