from Qt import QtCore, QtGui, QtWidgets

from pxr import Tf, Usd

from ..data.decorators import callOnceDeferred, waitThisLongBeforeRunning
from ..data.RelationshipFiltering import RelationshipFilteringOptions
from ..data.RelationshipCollectionManager import RelationshipCollectionManager
from . import icons
from .mixins import DoOnFirstShowMixin
from .RelationshipFilteringOptionsDialog import RelationshipFilteringOptionsDialog
from .RelationshipScene import RelationshipScene
from .RelationshipView import RelationshipView
from .RelationshipDetailViewer import RelationshipDetailViewer
from .utils import LayoutMods
from .widgets import FilterCountBubble


class RelationshipBrowser(QtWidgets.QWidget, DoOnFirstShowMixin):
    """This is the top-level widget for "browsing" among a navigable series of
    relationship views. Note that if an instance of RelationshipCollectionManager
    isn't provided to the constructor, the RelationshipCollectionManager singleton
    instance will be used. Updates the active RelationshipCollection when its
    stage changes.
    """

    # child widget classes
    REL_SCENE_CLASS = RelationshipScene
    REL_VIEW_CLASS = RelationshipView
    REL_DETAIL_VIEW_CLASS = RelationshipDetailViewer

    # constants for sizes of things etc.
    TOP_LAYOUT_MODS = LayoutMods(contentsMargins=(0, 0, 0, 0), spacing=0)
    TOP_BAR_LAYOUT_MODS = LayoutMods(contentsMargins=(2, 2, 2, 2), spacing=5)
    TOOLBAR_ICON_SIZE = QtCore.QSize(20, 20)
    SCENE_WIDTH = 32000
    SCENE_HEIGHT = SCENE_WIDTH
    DETAILS_PANEL_WIDTH_RATIO = 1 / 4  # details panel takes 1/4 the overall width

    # constants for other options
    DEFAULT_AUTO_FIT = True
    DEFAULT_SHOW_GRID = True

    # some instance state
    _activeCollection = None
    _objectsChangedKey = None

    def __init__(self, parent=None, relCollMgr=None):
        super().__init__(parent)

        self._relMgr = relCollMgr or RelationshipCollectionManager.getInstance()

        self._initialSplitterSizes = []
        self._buildUI()
        self._makeConnections()

        self._initFromActiveCollection()

    #
    # public API
    #
    def getRelationshipScene(self):
        return self._relationshipScene

    def getRelationshipView(self):
        return self._relationshipView

    def hasActiveRelationshipCollection(self):
        return self._activeCollection is not None

    def getActiveRelationshipCollection(self):
        return self._activeCollection

    def getRelationshipCollectionManager(self):
        # TODO probably don't need this - just for convenience
        return self._relMgr

    def clear(self):
        # TODO probably don't need this - just for convenience
        self._relMgr.clear()

    def addNewFor(self, stage, primPaths):
        # TODO not sure we'll continue to need this - currently just a passthrough
        # to RelationshipCollectionManager's addNewFor()
        self._relMgr.addNewFor(stage, primPaths)

    #
    # state preservation/restoration
    #
    def getSessionState(self):
        return dict(
            auto_fit=self._relationshipView.shouldAutoFitOnChanges(),
            show_grid=self._relationshipScene.isGridViewEnabled(),
            splitter_sizes=self._mainViewSplitter.sizes(),
            # include the singleton instance of filtering options, which should
            # be a good choice/starting point
            filtering_options=RelationshipFilteringOptions.getInstance().toDict(),
        )

    def restoreSessionState(self, stateDict):
        wantAutoFit = stateDict.get("auto_fit")
        if wantAutoFit is not None:
            self._relationshipView.setAutoFitOnChanges(wantAutoFit)
        showGrid = stateDict.get("show_grid")
        if showGrid is not None:
            self._relationshipScene.enableGridView(showGrid)
        splitterSizes = stateDict.get("splitter_sizes")
        if splitterSizes is not None:
            self._initialSplitterSizes = splitterSizes
            self._mainViewSplitter.setSizes(splitterSizes)
        filteringOptionsDict = stateDict.get("filtering_options")
        if filteringOptionsDict is not None:
            RelationshipFilteringOptions.getInstance().initFromDict(
                filteringOptionsDict
            )

    #
    # DoOnFirstShowMixin overrides
    #
    @waitThisLongBeforeRunning(numMilliseconds=1)
    def _doAfterFirstShow(self, showEvent_notUsed):
        self._filterCountBubble.setFixedHeight(
            self._rightToolBar.widgetForAction(self._autoFitAction).height()
        )
        if not self._initialSplitterSizes:
            width = self.width()
            sceneRatio = 1.0 - self.DETAILS_PANEL_WIDTH_RATIO
            self._initialSplitterSizes = [
                int(width * sceneRatio),
                int(width * self.DETAILS_PANEL_WIDTH_RATIO),
            ]
            self._mainViewSplitter.setSizes(self._initialSplitterSizes)

    #
    # slots & callbacks
    #
    def _sceneGridEnabledChangedToSLOT(self, gridEnabled):
        self._showGridAction.setChecked(gridEnabled)

    def _sceneSelectionChangedSLOT(self, selectedNodeItems, selectedWireItems_notUsed):
        relRecords = [
            nodeItem.getRelationshipRecord() for nodeItem in selectedNodeItems
        ]
        self._relationshipDetailViewer.setRecords(relRecords)

    def _sceneNodeClickedSLOT(self, nodeItem, mouseEvent):
        pass  # TODO implement?

    def _sceneNodeDoubleClickedSLOT(self, nodeItem, mouseEvent):
        if self.hasActiveRelationshipCollection():
            self._handlePrimDoubleClicked(nodeItem.getRelationshipRecord(), mouseEvent)

    def _sceneWireClickedSLOT(self, wireItem, mouseEvent):
        pass  # TODO implement?

    def _sceneWireDoubleClickedSLOT(self, wireItem, mouseEvent):
        pass  # TODO implement?

    def _sceneContextMenuRequestedSLOT(self, nodeItem, wireItem, event):
        pass  # TODO implement?

    def _relationshipViewAutoFitChangedToSLOT(self, autoFitOn):
        self._autoFitAction.setChecked(autoFitOn)

    def _relMgrActiveChangedSLOT(self):
        self._initFromActiveCollection()

    def _activeCollectionUpdatedSLOT(self):
        self._initFromActiveCollection()

    def _goBackTriggeredSLOT(self):
        self._relMgr.goBack()

    def _goForwardTriggeredSLOT(self):
        self._relMgr.goForward()

    def _filterBubbleClickedSLOT(self):
        if not self.hasActiveRelationshipCollection():
            return

        dlg = RelationshipFilteringOptionsDialog(
            self._activeCollection.getFilteringOptions()
        )
        dlg.exec_()

    def _clearTriggeredSLOT(self):
        self._relMgr.clear()

    def _frameSelectedTriggeredSLOT(self):
        self._relationshipView.fitToSelected()

    def _autoFitTriggeredSLOT(self, isChecked):
        self._relationshipView.setAutoFitOnChanges(isChecked)

    def _showGridTriggeredSLOT(self, isChecked):
        self._relationshipScene.enableGridView(isChecked)

    def _stageObjectsChangedCallback(self, notice, sender=None):
        self._doDeferredUpdate()

    def _detailViewPrimClickedSLOT(self, relationshipRecord, mouseEvent):
        pass  # TODO anything?

    def _detailViewPrimDoubleClickedSLOT(self, relationshipRecord, mouseEvent):
        if self.hasActiveRelationshipCollection():
            self._handlePrimDoubleClicked(relationshipRecord, mouseEvent)

    #
    # private helper methods
    #
    def _buildUI(self):
        self.setWindowIcon(QtGui.QIcon(icons.WINDOW_ICON_PATH))

        self._createActions()

        self._layout = QtWidgets.QVBoxLayout()
        self.TOP_LAYOUT_MODS.modify(self._layout)
        self.setLayout(self._layout)

        self._topBarWidget = QtWidgets.QWidget(self)
        self._layout.addWidget(self._topBarWidget, 0)

        self._topBarLayout = QtWidgets.QHBoxLayout()
        self.TOP_BAR_LAYOUT_MODS.modify(self._topBarLayout)
        self._topBarWidget.setLayout(self._topBarLayout)

        # create and populate left side toolbar
        self._leftToolBar = QtWidgets.QToolBar(self._topBarWidget)
        self._leftToolBar.setIconSize(self.TOOLBAR_ICON_SIZE)
        self._topBarLayout.addWidget(self._leftToolBar, 0, QtCore.Qt.AlignVCenter)

        for action in self._leftToolbarActions:
            self._leftToolBar.addAction(action)

        # note on self._currentPathsEdit, below - we basically just want a label,
        # but a read-only QLineEdit looks a little more interesting, plus allows
        # selecting of paths, in case that's something a user might want to do :shrug:
        self._currentPathsEdit = QtWidgets.QLineEdit("", self._topBarWidget)
        self._currentPathsEdit.setReadOnly(True)
        # note: for some reason, changing the background role doesn't work, so
        # we'll change the background color in the palette
        bgColor = (
            self.parentWidget().palette().color(self.parentWidget().backgroundRole())
            if self.parentWidget()
            else self.palette().color(QtGui.QPalette.Window)
        )
        lineEditPalette = QtGui.QPalette(self._currentPathsEdit.palette())
        lineEditPalette.setColor(self._currentPathsEdit.backgroundRole(), bgColor)
        self._currentPathsEdit.setPalette(lineEditPalette)
        self._currentPathsEdit.setAutoFillBackground(True)
        self._currentPathsEdit.setFocusPolicy(QtCore.Qt.NoFocus)  # don't want focus
        self._topBarLayout.addWidget(self._currentPathsEdit, 1, QtCore.Qt.AlignVCenter)

        self._filterCountBubble = FilterCountBubble(self._topBarWidget)
        self._topBarLayout.addWidget(self._filterCountBubble, 0, QtCore.Qt.AlignVCenter)

        # create and populate right side toolbar
        self._rightToolBar = QtWidgets.QToolBar(self._topBarWidget)
        self._rightToolBar.setIconSize(self.TOOLBAR_ICON_SIZE)
        self._topBarLayout.addWidget(self._rightToolBar, 0, QtCore.Qt.AlignVCenter)

        for action in self._rightToolbarActions:
            self._rightToolBar.addAction(action)

        # splitter to hold node/scene view on left, details panel on right
        self._mainViewSplitter = QtWidgets.QSplitter(self)
        self._layout.addWidget(self._mainViewSplitter, 1)

        self._relationshipScene = self.REL_SCENE_CLASS(
            width=self.SCENE_WIDTH,
            height=self.SCENE_HEIGHT,
            parent=self,
        )
        self._relationshipScene.enableGridView(self.DEFAULT_SHOW_GRID)

        self._relationshipView = self.REL_VIEW_CLASS(self._mainViewSplitter)
        self._relationshipView.setScene(self._relationshipScene)
        self._relationshipView.setAutoFitOnChanges(self.DEFAULT_AUTO_FIT)

        self._relationshipDetailViewer = self.REL_DETAIL_VIEW_CLASS(
            self._mainViewSplitter
        )

        # now that we've got the scene & view, update some action states
        self._autoFitAction.setChecked(self._relationshipView.shouldAutoFitOnChanges())
        self._showGridAction.setChecked(self._relationshipScene.isGridViewEnabled())

    def _createActions(self):
        self._goBackAction = QtWidgets.QAction(
            QtGui.QIcon(icons.GO_BACK_ICON_PATH), "Go Back", self
        )
        self._goBackAction.setToolTip("Go Back")

        self._goForwardAction = QtWidgets.QAction(
            QtGui.QIcon(icons.GO_FORWARD_ICON_PATH), "Go Forward", self
        )
        self._goForwardAction.setToolTip("Go Forward")

        self._autoFitAction = QtWidgets.QAction(
            QtGui.QIcon(icons.AUTO_FIT_ICON_PATH), "Auto-Fit", self
        )
        self._autoFitAction.setCheckable(True)
        self._autoFitAction.setChecked(self.DEFAULT_AUTO_FIT)
        self._autoFitAction.setToolTip("Toggle Auto-Fit")

        self._showGridAction = QtWidgets.QAction(
            QtGui.QIcon(icons.SHOW_GRID_ICON_PATH), "Show Grid", self
        )
        self._showGridAction.setCheckable(True)
        self._showGridAction.setChecked(self.DEFAULT_SHOW_GRID)
        self._showGridAction.setToolTip("Toggle Grid Visibility")

        self._frameSelectedAction = QtWidgets.QAction(
            QtGui.QIcon(icons.FRAME_SELECTED_ICON_PATH), "Frame Selected", self
        )
        self._frameSelectedAction.setToolTip("Frame Selected")

        self._clearAction = QtWidgets.QAction(
            QtGui.QIcon(icons.CLEAR_ICON_PATH), "Clear", self
        )
        self._clearAction.setToolTip("Clear All")

        self._leftToolbarActions = [self._goBackAction, self._goForwardAction]
        self._rightToolbarActions = [
            self._autoFitAction,
            self._showGridAction,
            self._frameSelectedAction,
            self._clearAction,
        ]
        self._actionsNeedingCollection = [
            self._goBackAction,
            self._goForwardAction,
            self._frameSelectedAction,
            self._clearAction,
        ]

    def _makeConnections(self):
        # scene -> me
        self._relationshipScene.GridEnabledChangedTo.connect(
            self._sceneGridEnabledChangedToSLOT
        )
        self._relationshipScene.SelectionChanged.connect(
            self._sceneSelectionChangedSLOT
        )
        self._relationshipScene.NodeClicked.connect(self._sceneNodeClickedSLOT)
        self._relationshipScene.NodeDoubleClicked.connect(
            self._sceneNodeDoubleClickedSLOT
        )
        self._relationshipScene.WireClicked.connect(self._sceneWireClickedSLOT)
        self._relationshipScene.WireDoubleClicked.connect(
            self._sceneWireDoubleClickedSLOT
        )
        self._relationshipScene.ContextMenuRequested.connect(
            self._sceneContextMenuRequestedSLOT
        )

        # view -> me
        self._relationshipView.AutoFitChangedTo.connect(
            self._relationshipViewAutoFitChangedToSLOT
        )

        # detail view -> me
        self._relationshipDetailViewer.PrimClicked.connect(
            self._detailViewPrimClickedSLOT
        )
        self._relationshipDetailViewer.PrimDoubleClicked.connect(
            self._detailViewPrimDoubleClickedSLOT
        )

        # other things -> me
        self._relMgr.ActiveChanged.connect(self._relMgrActiveChangedSLOT)
        self._filterCountBubble.clicked.connect(self._filterBubbleClickedSLOT)

        self._connectToActions()

    def _connectToActions(self):
        self._goBackAction.triggered.connect(self._goBackTriggeredSLOT)
        self._goForwardAction.triggered.connect(self._goForwardTriggeredSLOT)
        self._clearAction.triggered.connect(self._clearTriggeredSLOT)
        self._frameSelectedAction.triggered.connect(self._frameSelectedTriggeredSLOT)
        self._autoFitAction.triggered.connect(self._autoFitTriggeredSLOT)
        self._showGridAction.triggered.connect(self._showGridTriggeredSLOT)

    def _initFromActiveCollection(self):
        self._disconnectFromActiveCollection()
        self._activeCollection = self._relMgr.getActiveCollection()

        for action in self._actionsNeedingCollection:
            action.setEnabled(bool(self._activeCollection))

        self._goBackAction.setEnabled(self._relMgr.canGoBack())
        self._goForwardAction.setEnabled(self._relMgr.canGoForward())

        self._initCurrentPathsLabel()
        self._updateFilterCount()

        self._relationshipScene.setRelationshipCollection(self._activeCollection)
        if not self._activeCollection:
            self._relationshipView.clear()

        self._connectToActiveCollection()

    def _initCurrentPathsLabel(self):
        primPaths = (
            list(self._activeCollection.getPrimPaths())
            if self._activeCollection
            else []
        )
        if not primPaths:
            self._currentPathsEdit.setText("(none)")
            self._currentPathsEdit.setToolTip("")
            return

        primPaths.sort()
        textStr = primPaths[0].pathString
        numPaths = len(primPaths)
        if numPaths > 1:
            textStr += f" + {numPaths - 1} other{'s' if numPaths > 2 else ''}"

        self._currentPathsEdit.setText(textStr)
        toolTipText = "\n".join([p.pathString for p in primPaths])
        self._currentPathsEdit.setToolTip(toolTipText)

    def _updateFilterCount(self):
        count = 0
        if self.hasActiveRelationshipCollection():
            filterOpts = self._activeCollection.getFilteringOptions()
            count = filterOpts.getNumFilterExclusions()
        self._filterCountBubble.setCount(count)
        self._filterCountBubble.setToolTip(
            f"{count} Exclusions Applied" if count else "Filters"
        )

    def _connectToActiveCollection(self):
        if not self._activeCollection:
            return

        self._activeCollection.Updated.connect(self._activeCollectionUpdatedSLOT)

        self._objectsChangedKey = Tf.Notice.Register(
            Usd.Notice.ObjectsChanged,
            self._stageObjectsChangedCallback,
            self._activeCollection.getStage(),
        )

    def _disconnectFromActiveCollection(self):
        if not self._activeCollection:
            return

        self._activeCollection.Updated.disconnect(self._activeCollectionUpdatedSLOT)
        self._objectsChangedKey.Revoke()
        self._objectsChangedKey = None

    @callOnceDeferred(
        callsPendingAttrName="_willUpdateDueToStageChanges", waitTimeoutMs=500
    )
    def _doDeferredUpdate(self):
        if self.hasActiveRelationshipCollection():
            self.getActiveRelationshipCollection().update()
        self._initFromActiveCollection()
        self._relationshipView.update()

    def _handlePrimDoubleClicked(self, relRecord, mouseEvent):
        # double clicking a node representing a prim with "additional relationships"
        # means the user wants to expand the relationship view to include that
        # prim's relationships as well - with the shift key pressed, that prim's
        # relationships will be added in to the current collection, otherwise (shift
        # key not pressed) a new collection will be created with the current prims
        # plus the one just double clicked
        if not relRecord.hasAdditionalToRelationships():
            return

        clickedPrimPath = relRecord.getPrimPath()
        currentHomePaths = self._activeCollection.getPrimPaths()
        if clickedPrimPath in currentHomePaths:
            return  # this shouldn't happen, but still...

        if mouseEvent.modifiers() & QtCore.Qt.ShiftModifier:
            # the shift key is pressed - add clickedPrimPath to active collection
            self._activeCollection.addPrimPaths([clickedPrimPath])
        else:
            # the shift key is not pressed - create a new collection with currentPaths
            # plus clickedPrimPath
            self._relMgr.addNewFor(
                self._activeCollection.getStage(),
                list(currentHomePaths) + [clickedPrimPath],
            )
        self._relationshipScene.selectOnlyNodeItemsFor([clickedPrimPath])
