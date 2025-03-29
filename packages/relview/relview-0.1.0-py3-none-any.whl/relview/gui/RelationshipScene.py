from Qt import QtCore, QtGui, QtWidgets

from .contextManagers import withWaitCursor
from .ForceSimulationNodeLayout import ForceSimulationNodeLayout
from .PrimNodeItem import PrimNodeItem
from .RelationshipWireItem import RelationshipWireItem


class RelationshipScene(QtWidgets.QGraphicsScene):
    """QGraphicsScene for displaying PrimNodeItem and RelationshipWireItem
    instances representing prims and the relationships among them.
    """

    # class constants (overridable)
    SCENE_BACKGROUND_COLOR = QtGui.QColor(32, 31, 31)
    SCENE_GRID_LINE_COLOR = QtGui.QColor(35, 35, 35).darker(50)
    SCENE_GRID_LINE_WIDTH = 0.65  # pixels (qreal)
    SCENE_GRID_SIZE = 50 * 4  # pixels
    CLICK_RADIUS = 5  # TODO good value for this?
    NODE_LAYOUT_CLASS = ForceSimulationNodeLayout

    # signals
    GridEnabledChangedTo = QtCore.Signal(bool)
    RelationshipCollectionChangedTo = QtCore.Signal(object)
    RelationshipCollectionUpdated = QtCore.Signal()

    SelectionChanged = QtCore.Signal(
        object,  # list of PrimNodeItem
        object,  # list of RelationshipWireItem
    )

    NodeClicked = QtCore.Signal(
        object, object
    )  # PrimNodeItem, QGraphicsSceneMouseEvent
    NodeDoubleClicked = QtCore.Signal(
        object, object
    )  # PrimNodeItem, QGraphicsSceneMouseEvent
    WireClicked = QtCore.Signal(
        object, object
    )  # RelationshipWireItem, QGraphicsSceneMouseEvent
    WireDoubleClicked = QtCore.Signal(
        object, object
    )  # RelationshipWireItem, QGraphicsSceneMouseEvent

    ContextMenuRequested = QtCore.Signal(
        object,  # PrimNodeItem (or None)
        object,  # RelationshipWireItem (or None)
        object,  # QGraphicsSceneContextMenuEvent
    )

    # some instance state
    _mousePressPos = None
    _relationshipCollection = None
    _gridEnabled = True
    _nodeItemsByPrimPath = {}
    _wireItemsByFromTo = {}

    def __init__(self, width=0, height=0, parent=None):
        super().__init__(parent)

        if width and height:
            self.setSceneRect(-width / 2, -height / 2, width, height)

        self.setBackgroundBrush(self.SCENE_BACKGROUND_COLOR)

        self.selectionChanged.connect(self._selectionChangedSLOT)

    #
    # public API
    #
    def getRelationshipCollection(self):
        return self._relationshipCollection

    def hasRelationshipCollection(self):
        return self._relationshipCollection is not None

    def setRelationshipCollection(self, relColl):
        if relColl != self._relationshipCollection:
            self._disconnectFromRelationshipCollection()
            self._relationshipCollection = relColl
            self._buildFromRelationshipCollection()
            self._connectToRelationshipCollection()
            self.RelationshipCollectionChangedTo.emit(self._relationshipCollection)

    def toggleGridView(self):
        self.enableGridView(not self.isGridViewEnabled())

    def enableGridView(self, enabled=True):
        if enabled != self._gridEnabled:
            self._gridEnabled = bool(enabled)
            self.update()
            self.GridEnabledChangedTo.emit(self._gridEnabled)

    def isGridViewEnabled(self):
        return self._gridEnabled

    def getNodeItems(self):
        return list(self._nodeItemsByPrimPath.values())

    def getNodeItemCount(self):
        return len(self._nodeItemsByPrimPath.values())

    def getSelectedNodeItems(self):
        selItems = self.selectedItems()
        return [ni for ni in self.getNodeItems() if ni in selItems]

    def getNodeItemForPrimPath(self, primPath):
        return self._nodeItemsByPrimPath.get(primPath)

    def getWireItems(self):
        return list(self._wireItemsByFromTo.values())

    def getSelectedWireItems(self):
        selItems = self.selectedItems()
        return [wi for wi in self.getWireItems() if wi in selItems]

    def getWireItemBetween(self, onePrimPath, otherPrimPath):
        for key in [
            self._getWireKeyFor(onePrimPath, otherPrimPath),
            self._getWireKeyFor(otherPrimPath, onePrimPath),
        ]:
            if key in self._wireItemsByFromTo:
                return self._wireItemsByFromTo[key]

        return None

    def refreshWires(self):
        for wireItem in self._wireItemsByFromTo.values():
            wireItem.refresh()

    def selectOnlyNodeItemsFor(self, primPaths):
        toSelect = [self.getNodeItemForPrimPath(pp) for pp in primPaths]
        for nodeItem in self.getNodeItems():
            nodeItem.setSelected(nodeItem in toSelect)

    #
    # QGraphicsScene overrides
    #
    def clear(self):
        super().clear()
        self._nodeItemsByPrimPath = {}
        self._wireItemsByFromTo = {}

    def contextMenuEvent(self, event):
        nodeItem, wireItem = None, None
        eventPos = event.scenePos()
        nodeItem = self._getNodeItemAt(eventPos)
        if not nodeItem:
            wireItem = self._getWireItemAt(eventPos)
        self.ContextMenuRequested.emit(nodeItem, wireItem, event)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        if self.isGridViewEnabled():
            self._drawGrid(painter, rect)

    def mouseDoubleClickEvent(self, event):
        self._handleDoubleClick(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._mousePressPos = event.screenPos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            # Updating any existing edges in the current scene
            # TODO: performance wise, might be a good idea to only
            #       limit it to edges that are on screen, if possible
            self.refreshWires()
            self.update()

        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self._mousePressPos is not None and event.button() == QtCore.Qt.LeftButton:
            thisPoint = event.screenPos() - self._mousePressPos
            if thisPoint.manhattanLength() <= self.CLICK_RADIUS:
                self._handleClick(event)

            self._mousePressPos = None

        super().mouseReleaseEvent(event)

    #
    # slots
    #
    def _selectionChangedSLOT(self):
        self.SelectionChanged.emit(
            self.getSelectedNodeItems(), self.getSelectedWireItems()
        )

    def _relCollUpdatedSLOT(self):
        self._buildFromRelationshipCollection()
        self.RelationshipCollectionUpdated.emit()

    #
    # private helper methods
    #
    def _connectToRelationshipCollection(self):
        if self.hasRelationshipCollection():
            self._relationshipCollection.Updated.connect(self._relCollUpdatedSLOT)

    def _disconnectFromRelationshipCollection(self):
        if self.hasRelationshipCollection():
            self._relationshipCollection.Updated.disconnect(self._relCollUpdatedSLOT)

    def _buildFromRelationshipCollection(self):
        self.clear()
        if not self.hasRelationshipCollection():
            return

        self._createNodeItems()
        self._arrangeNodeItems()
        self._createWiresBetweenNodes()
        self._selectNodesForCollection()

    def _createNodeItems(self):
        for relationshipRecord in self._relationshipCollection.getAllRecords():
            nodeItem = PrimNodeItem(relationshipRecord)
            self._nodeItemsByPrimPath[relationshipRecord.getPrimPath()] = nodeItem
            self.addItem(nodeItem)

    def _arrangeNodeItems(self):
        layoutObj = self.NODE_LAYOUT_CLASS(self)
        if layoutObj.willTakeAWhile():
            with withWaitCursor():
                layoutObj.doNodeLayout()
        else:
            layoutObj.doNodeLayout()

    def _createWiresBetweenNodes(self):
        for relationshipRecord in self._relationshipCollection.getAllRecords():
            primPath = relationshipRecord.getPrimPath()
            for toPath in relationshipRecord.getPrimsWithToRelationships():
                self._getOrCreateWireItemFor(primPath, toPath)
            for fromPath in relationshipRecord.getPrimsWithFromRelationships():
                self._getOrCreateWireItemFor(fromPath, primPath)

    def _getOrCreateWireItemFor(self, fromPath, toPath):
        wireItem = self.getWireItemBetween(fromPath, toPath)
        if not wireItem:
            wireItem = RelationshipWireItem(
                self.getNodeItemForPrimPath(fromPath),
                self.getNodeItemForPrimPath(toPath),
            )
            self._wireItemsByFromTo[self._getWireKeyFor(fromPath, toPath)] = wireItem
            self.addItem(wireItem)
        return wireItem

    def _selectNodesForCollection(self):
        for primPath in self._relationshipCollection.getPrimPaths():
            nodeItem = self.getNodeItemForPrimPath(primPath)
            if nodeItem:
                nodeItem.setSelected(True)

    def _drawGrid(self, painter, rect):
        """Draws the grid lines in the scene.
        TODO allow changing grid size, line width, and line color
        """
        left = int(rect.left())
        right = int(rect.right())
        top = int(rect.top())
        bottom = int(rect.bottom())

        gridSize = self.SCENE_GRID_SIZE
        firstLeft = left - (left % gridSize)
        firstTop = top - (top % gridSize)

        lines = []
        lines.extend(
            [
                QtCore.QLineF(x, top, x, bottom)
                for x in range(firstLeft, right, gridSize)
            ]
        )
        lines.extend(
            [
                QtCore.QLineF(left, y, right, y)
                for y in range(firstTop, bottom, gridSize)
            ]
        )

        pen = QtGui.QPen(self.SCENE_GRID_LINE_COLOR, self.SCENE_GRID_LINE_WIDTH)
        painter.setPen(pen)
        painter.drawLines(lines)

    def _getWireKeyFor(self, onePrimPath, otherPrimPath):
        return f"{onePrimPath.pathString}_{otherPrimPath.pathString}"

    def _handleClick(self, mouseEvent):
        self._emitNodeOrWireSignalForMouseEvent(
            nodeSignal=self.NodeClicked,
            wireSignal=self.WireClicked,
            mouseEvent=mouseEvent,
        )

    def _handleDoubleClick(self, mouseEvent):
        self._emitNodeOrWireSignalForMouseEvent(
            nodeSignal=self.NodeDoubleClicked,
            wireSignal=self.WireDoubleClicked,
            mouseEvent=mouseEvent,
        )

    def _emitNodeOrWireSignalForMouseEvent(self, nodeSignal, wireSignal, mouseEvent):
        eventPos = mouseEvent.scenePos()
        nodeItem = self._getNodeItemAt(eventPos)
        if nodeItem:
            return nodeSignal.emit(nodeItem, mouseEvent)

        wireItem = self._getWireItemAt(eventPos)
        if wireItem:
            return wireSignal.emit(wireItem, mouseEvent)

    def _getNodeItemAt(self, scenePos):
        items = self.items(scenePos)
        return self._getFirstNodeItemFrom(items) if items else None

    def _getWireItemAt(self, scenePos):
        items = self.items(scenePos)
        return self._getFirstWireItemFrom(items) if items else None

    def _getFirstNodeItemFrom(self, items):
        return self._getFirstItemFrom(items, self.getNodeItems())

    def _getFirstWireItemFrom(self, items):
        return self._getFirstItemFrom(items, self.getWireItems())

    def _getFirstItemFrom(self, items, itemsSource):
        for item in items:
            if item in itemsSource:
                return item
        return None
