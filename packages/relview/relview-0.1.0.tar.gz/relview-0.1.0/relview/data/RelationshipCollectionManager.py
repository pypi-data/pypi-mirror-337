from Qt import QtCore

from .filterUpdating import updateFilteringOptionsFromOther
from .RelationshipCollection import RelationshipCollection
from .RelationshipFiltering import RelationshipFilteringOptions


class RelationshipCollectionManager(QtCore.QObject):
    """This is the top-level thing that holds RelationshipCollection objects
    and allows navigating among them etc. The singleton instance, retrievable
    via the getInstance() class method, is for use with applications where there
    is just one relationship viewer window. It's convenient. But instances of
    this class can be created as needed - other than the singleton - just fine.
    """

    ActiveChanged = QtCore.Signal()

    _INSTANCE = None

    @classmethod
    def getInstance(cls):
        if cls._INSTANCE is None:
            cls._INSTANCE = cls()
        return cls._INSTANCE

    def __init__(self, parent=None):
        super().__init__(parent)
        self._activeIndex = None
        self._relationshipCollections = []

    #
    # public API
    #
    def clear(self):
        if not self._relationshipCollections:
            return  # nothing to clear

        colls = [c for c in self._relationshipCollections]
        for c in colls:
            self._dropCollection(c)
        self._setActiveTo(None)

    def hasActiveCollection(self):
        return self.getActiveCollection() is not None

    def getActiveCollection(self):
        return (
            self._relationshipCollections[self._activeIndex]
            if self._activeIndex is not None
            else None
        )

    def addNew(self, relColl):
        relColl.setParent(self)
        self._dropCollectionsAfterCurrent()
        self._relationshipCollections.append(relColl)
        self._connectToCollection(relColl)
        self._setActiveToLast()

    def addNewFor(self, stage, primPaths):
        relColl = RelationshipCollection(stage=stage, primPaths=primPaths, parent=self)
        self.addNew(relColl)

    def canAddTheseToActiveCollection(self, primPaths, stage=None):
        relColl = self.getActiveCollection()
        if not relColl:
            return stage is not None

        if stage is not None and relColl.getStage() != stage:
            return False

        activePaths = relColl.getPrimPaths()
        for pp in primPaths:
            if pp not in activePaths:
                return True

        return False

    def addToActiveCollection(self, primPaths, stage=None):
        assert self.canAddTheseToActiveCollection(primPaths, stage)

        relColl = self.getActiveCollection()
        if relColl:
            relColl.addPrimPaths(primPaths)
        else:
            self.addNewFor(stage, primPaths)

    def canGoBack(self):
        return self._activeIndex is not None and self._activeIndex > 0

    def goBack(self):
        assert self.canGoBack(), "Can't go back!"
        self._setActiveTo(self._activeIndex - 1)

    def canGoForward(self):
        return self._activeIndex is not None and self._activeIndex < (
            len(self._relationshipCollections) - 1
        )

    def goForward(self):
        assert self.canGoForward(), "Can't go forward!"
        self._setActiveTo(self._activeIndex + 1)

    #
    # slots
    #
    def _relCollFilteringOptionsChangedSLOT(self, filteringOptions):
        # update the RelationshipFilteringOptions singleton instance based on
        # filteringOptions (just updated) such that new relationship collections
        # will start with those options
        updateFilteringOptionsFromOther(
            RelationshipFilteringOptions.getInstance(), filteringOptions
        )

    #
    # private helper methods
    #
    def _setActiveToLast(self):
        activeIdx = (
            (len(self._relationshipCollections) - 1)
            if self._relationshipCollections
            else None
        )
        self._setActiveTo(activeIdx)

    def _setActiveTo(self, activeIdx):
        self._activeIndex = activeIdx
        self.ActiveChanged.emit()

    def _connectToCollection(self, relColl):
        relColl.FilteringOptionsChanged.connect(
            self._relCollFilteringOptionsChangedSLOT
        )

    def _disconnectFromCollection(self, relColl):
        relColl.FilteringOptionsChanged.disconnect(
            self._relCollFilteringOptionsChangedSLOT
        )

    def _dropCollectionsAfterCurrent(self):
        if not self.canGoForward():
            return  # nothing to do

        numRelColls = len(self._relationshipCollections)
        indices = range(self._activeIndex + 1, numRelColls)
        collsToRemove = [self._relationshipCollections[idx] for idx in indices]
        for relColl in collsToRemove:
            self._dropCollection(relColl)

    def _dropCollection(self, relColl):
        assert relColl in self._relationshipCollections, "Invalid collection!"
        self._relationshipCollections.remove(relColl)
        self._disconnectFromCollection(relColl)
        relColl.setParent(None)
        relColl.deleteLater()
