from Qt import QtCore, QtGui, QtWidgets


class RelationshipView(QtWidgets.QGraphicsView):
    """QGraphicsView for a RelationshipScene."""

    # signals
    AutoFitChangedTo = QtCore.Signal(bool)

    DragEntered = QtCore.Signal(object)  # QDragEnterEvent object
    DragMoved = QtCore.Signal(object)  # QDragMoveEvent object
    DragDropped = QtCore.Signal(object)  # QDropEvent object
    DragLeft = QtCore.Signal(object)  # QDragLeaveEvent object

    # instance state
    _scene = None
    _zoom = 1
    _scale = 1
    _spaceDown = False
    _shouldAutoFit = True

    def __init__(self, parent=None):
        super().__init__(parent)

        # Scroll bar controls
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # Anchor view controls
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setRenderHint(QtGui.QPainter.Antialiasing)

        # Drag / Selection controls
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.BoundingRectViewportUpdate)
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)

        # Allow drops from outside (will be handled via signals)
        self.setAcceptDrops(True)

        # Defining hotkeys/shortcuts
        self._createShortCuts()

        # Init scene
        self.setInteractive(True)

    #
    # public API
    #
    def setStage(self, stage):
        # TODO not sure how important this is - probably instead want options
        # to "send" prims to the relationship viewer, like we do for material
        # comparison
        self._scene.setStage(stage)

    def getStage(self):
        return self._scene.getStage()

    def setSelectedPaths(self, primPaths):
        # TODO probably temporary
        self._scene.setSelectedPaths(primPaths)

    def getSelectedPaths(self):
        return self._scene.getSelectedPaths()

    def clear(self):
        self._scene.clear()

    #
    # show grid stuff
    #
    def isGridVisible(self):
        return self._scene.isGridViewEnabled()

    def enableGridView(self, enabled=True):
        self._scene.enableGridView(enabled)

    def toggleGridView(self):
        self._scene.toggleGridView()

    #
    # view fitting stuff (all vs. selected)
    #
    def fitToSelected(self):
        selItems = self._getSelectedItems()
        return (
            self._fitInView(self._getBoundingBoxOf(selItems))
            if selItems
            else self.fitAll()
        )

    def fitAll(self):
        self._fitInView(self._getBoundingBoxOf(self._getNodeItems()))

    #
    # auto-fit
    # TODO this auto-fit stuff (_shouldAutoFit boolean, etc.) should probably move
    # to RelationshipBrowser, since that's got the higher-level knowledge over
    # when things are changing
    #
    def shouldAutoFitOnChanges(self):
        return self._shouldAutoFit

    def setAutoFitOnChanges(self, autoFit=True):
        if autoFit != self._shouldAutoFit:
            self._shouldAutoFit = bool(autoFit)
            self.AutoFitChangedTo.emit(self._shouldAutoFit)

    #
    # zoooooming
    #
    def zoomIn(self):
        self._zoom *= 1.10
        self._updateTransformScale()

    def zoomOut(self):
        self._zoom /= 1.10
        self._updateTransformScale()

    #
    # QGraphicsView overrides
    #
    def setScene(self, scene):
        # note: scene here must be a RelationshipScene
        super().setScene(scene)
        self._scene = scene
        self._connectToScene()
        if self.shouldAutoFitOnChanges():
            # do the fit-all in a slightly deferred/async way, since fitting
            # requires window geometry etc. and that likely won't have been done
            # yet when this method is called
            QtCore.QTimer.singleShot(100, self._fitAllDeferredSLOT)

    def wheelEvent(self, event):
        delta = event.angleDelta()
        scale_factor = pow(1.25, delta.y() / 240.0)
        self._scaleView(scale_factor)
        event.accept()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space and not event.isAutoRepeat():
            self._spaceDown = True

            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.OpenHandCursor)

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space and not event.isAutoRepeat():
            self._spaceDown = False

            self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)

            while QtWidgets.QApplication.overrideCursor() is not None:
                QtWidgets.QApplication.restoreOverrideCursor()

    def mousePressEvent(self, event):
        if self._spaceDown:
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.ClosedHandCursor)

            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

        if event.button() == QtCore.Qt.MidButton:
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            # Create a new event that mimics a left click event to take advantage
            # of builtin functionality.
            new_event = QtGui.QMouseEvent(
                QtCore.QEvent.MouseButtonPress,
                QtCore.QPointF(event.pos()),
                QtCore.Qt.LeftButton,
                event.buttons(),
                QtCore.Qt.KeyboardModifiers(),
            )
            self.mousePressEvent(new_event)

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self._spaceDown:
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.OpenHandCursor)
        # else:
        #     while QtWidgets.QApplication.overrideCursor() is not None:
        #         QtWidgets.QApplication.restoreOverrideCursor()

        if event.button() == QtCore.Qt.MidButton:
            new_event = QtGui.QMouseEvent(
                QtCore.QEvent.MouseButtonRelease,
                QtCore.QPointF(event.pos()),
                QtCore.Qt.LeftButton,
                event.buttons(),
                QtCore.Qt.KeyboardModifiers(),
            )
            self.mouseReleaseEvent(new_event)
            self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)

        super().mouseReleaseEvent(event)

    # holding off on context menu stuff for now
    # def contextMenuEvent(self, event):
    #     menu = QtWidgets.QMenu(self)
    #     expandAction = QtWidgets.QAction("Expand", self)
    #     menu.addAction(expandAction)

    #     pos, curr_node = self._getCurrentMouseNode(event)
    #     expandAction.triggered.connect(lambda val=pos: self._expandNodeConnections(pos))
    #     expandAction.setEnabled(bool(curr_node))

    #     menu.exec_(event.globalPos())

    #     super().contextMenuEvent(event)  # TODO do we still want to call this?

    def dragEnterEvent(self, event):
        self.DragEntered.emit(event)

    def dragMoveEvent(self, event):
        self.DragMoved.emit(event)

    def dropEvent(self, event):
        self.DragDropped.emit(event)

    def dragLeaveEvent(self, event):
        self.DragLeft.emit(event)

    #
    # slots
    #
    def _sceneRelationshipCollectionChangedToSLOT(self, relColl):
        if relColl and self.shouldAutoFitOnChanges():
            self.fitAll()

    def _sceneRelationshipCollectionUpdatedSLOT(self):
        if self.shouldAutoFitOnChanges():
            self.fitAll()

    def _focusOnSelectedTriggeredSLOT(self):
        self.fitToSelected()

    def _toggleGridTriggeredSLOT(self):
        self.toggleGridView()

    def _fitAllDeferredSLOT(self):
        self.fitAll()

    #
    # private helper methods
    #
    def _createShortCuts(self):
        # note: these aren't likely to work in Houdini or another app where the
        # keyboard focus is managed very deliberately/specially...
        # TODO: might these be better left for plugins to add, if they want
        # them?

        # Focus on selected node
        focusOnSelectedAction = QtWidgets.QShortcut(QtGui.QKeySequence("f"), self)
        focusOnSelectedAction.activated.connect(self._focusOnSelectedTriggeredSLOT)

        # Enable/Disable grid view
        toggleGridAction = QtWidgets.QShortcut(QtGui.QKeySequence("g"), self)
        toggleGridAction.activated.connect(self._toggleGridTriggeredSLOT)

    def _connectToScene(self):
        self._scene.RelationshipCollectionChangedTo.connect(
            self._sceneRelationshipCollectionChangedToSLOT
        )
        self._scene.RelationshipCollectionUpdated.connect(
            self._sceneRelationshipCollectionUpdatedSLOT
        )

    def _scaleView(self, scale_factor, limits=True):
        new_scale = self._scale * scale_factor
        self._scale = new_scale
        self.setInteractive(False)
        self.scale(scale_factor, scale_factor)
        self.setInteractive(True)

    def _updateTransformScale(self):
        """Update the scale of the transform (node) based on the zoom multiplier"""
        self.setTransform(QtGui.QTransform().scale(self._zoom, self._zoom))

    # def _getCurrentMouseNode(self, event):
    #     pos = self.mapToScene(event.pos())
    #     curr_node = self.scene().itemAt(pos, QtGui.QTransform())
    #     return pos, curr_node

    # def _expandNodeConnections(self, pos):
    #     curr_node = self.scene().itemAt(pos, QtGui.QTransform())

    #     if not curr_node.isExpanded():
    #         self._expandNodeRelationships(curr_node)
    #         curr_node.setExpandedState(True)

    # def _expandNodeRelationships(self, rootNode):
    #     """
    #     Gets the relationships from the prim in a given node
    #     and adds nodes representing those relationships to the view
    #     """
    #     current_x = rootNode.x() + (rootNode.boundingRect().width() * 1.5)
    #     current_y = 0
    #     rootPrim = self.getStage().GetPrimAtPath(rootNode.getPrimPath())
    #     node_height = 120

    #     newRels, _ = self.scene().collectRelationships([rootPrim])
    #     newNodes = self.scene().createNodes(newRels, extend=True)
    #     self.scene().created_nodes_map.update(newNodes)
    #     for idx, nodePath in enumerate(newNodes):
    #         node = newNodes[nodePath]
    #         dy = max(node_height, node.boundingRect().height())
    #         current_y += 0 if idx == 0 else dy

    #         # Set the new x and y positions
    #         node.setX(float(current_x))
    #         node.setY(float(current_y))
    #         current_y += dy * 0.5 + 10

    #     self._scene.refreshWires()

    def _getSelectedBoundingBox(self):
        """For a given selection of node return the bounding box"""
        items = self._getSelectedItems()
        if not items:
            items = self._getNodeItems()
        return self._getBoundingBoxOf(items)

    def _getSelectedItems(self):
        return self.scene().selectedItems()

    def _getNodeItems(self):
        return self._scene.getNodeItems()

    def _getBoundingBoxOf(self, graphicsItems):
        group = self._scene.createItemGroup(graphicsItems)
        rect = group.boundingRect()
        self._scene.destroyItemGroup(group)
        return rect

    def _fitInView(self, sceneRect):
        """Set view transform in order to fit all/selected nodes in scene."""
        # Default scene
        self._scene.refreshWires()

        # Compare ratio in order to calculate the new scale
        # TODO not sure about this logic (below)...
        parentWid = self.parentWidget()
        dimsSourceWidget = parentWid if parentWid else self
        xRatio = sceneRect.width() / float(dimsSourceWidget.width())
        yRatio = sceneRect.height() / float(dimsSourceWidget.height())
        maxRatio = max(xRatio, yRatio)
        new_scale = 1 / maxRatio if maxRatio > 0 else 1

        if new_scale >= 1 or new_scale < 0.1:
            # Minimum/Maximum zoom limit reached.
            self._zoom = 1
            self.resetTransform()
            self.centerOn(sceneRect.center())
        else:
            self._zoom = new_scale
            # Redraw the scene
            self.fitInView(sceneRect, QtCore.Qt.KeepAspectRatio)

        self._updateTransformScale()
