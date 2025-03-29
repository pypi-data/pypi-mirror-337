from Qt import QtCore

from pxr import Usd

from .filterUpdating import updateFilteringOptionsFromInfoCollector
from .PrimRelationshipRecord import PrimRelationshipRecord
from .RelationshipFiltering import RelationshipFilteringOptions
from .RelationshipInfoCollector import RelationshipInfoCollector


class RelationshipCollection(QtCore.QObject):
    """Encapsulates relationships (PrimRelationshipRecord objects) for a certain
    set of prims on a given USD stage.
    """

    FilteringOptionsChanged = QtCore.Signal(object)
    Updated = QtCore.Signal()

    def __init__(self, stage, primPaths, sourceFilteringOptions=None, parent=None):
        super().__init__(parent)
        self._stage = stage
        self._primPaths = set(primPaths)
        if sourceFilteringOptions is None:
            sourceFilteringOptions = RelationshipFilteringOptions.getInstance()
        self._filteringOptions = sourceFilteringOptions.clone(self)
        self._filteringOptions.Changed.connect(self._filteringOptionsChangedSLOT)
        self._relsByPrimPath = {}  # PrimRelationshipRecord objects, keyed by prim path
        self._relInfoCollector = RelationshipInfoCollector()
        self.update(signal=False)

    #
    # public API
    #
    def update(self, signal=True):
        self._prunePrimsNotFound()
        self._collectRelationshipsFromStage()
        if signal:
            self.Updated.emit()

    def getStage(self):
        return self._stage

    def getPrimPaths(self):
        # note: these are the paths of the "home prims" - that is, the prims
        # whose relationships are to be _viewed_, not all of the prims among
        # which relationships are present - use getAllPrimPaths() (below) for
        # all of the prims for which relationships exist
        return self._primPaths

    def addPrimPaths(self, newPrimPaths):
        addedAnything = False
        for primPath in newPrimPaths:
            if primPath not in self._primPaths:
                self._primPaths.add(primPath)
                addedAnything = True
        if addedAnything:
            self.update()

    def getFilteringOptions(self):
        return self._filteringOptions

    def getRelationshipInfoCollector(self):
        return self._relInfoCollector

    def hasRecordFor(self, primPath):
        return primPath in self._relsByPrimPath

    def getRecordFor(self, primPath):
        return self._relsByPrimPath.get(primPath)

    def getAllPrimPaths(self):
        return list(self._relsByPrimPath.keys())

    def getAllRecords(self):
        return list(self._relsByPrimPath.values())

    #
    # slots
    #
    def _filteringOptionsChangedSLOT(self):
        self.FilteringOptionsChanged.emit(self._filteringOptions)
        self.update()

    #
    # private helper methods etc.
    #
    def _prunePrimsNotFound(self):
        pathsToRemove = set()
        for primPath in self._primPaths:
            prim = self._stage.GetPrimAtPath(primPath)
            if not prim:
                pathsToRemove.add(primPath)
        self._primPaths -= pathsToRemove

    def _collectRelationshipsFromStage(self):
        # TODO figure out where relationship path-collection plugins ought to, well,
        # plug into here

        # collect the "to" relationships first, since those are more immediately
        # available
        self._relsByPrimPath = {}
        returnToPathsForAdditionals = set()

        if not self._primPaths:
            return  # nothing to do, yo

        for primPath in self._primPaths:
            prim = self._stage.GetPrimAtPath(primPath)
            if not prim:
                continue  # TODO also warn? This really shouldn't happen...

            # create records for the specified prims at least, even if they
            # might not have any relationships (due to current filtering options etc.)
            _ = self._getOrCreateRecordFor(primPath)

            if self._filteringOptions.shouldFollowTargetRelationships():
                self._collectTargetRelationshipsOf(
                    primPath, prim, returnToPathsForAdditionals
                )

        # now traverse the whole stage to get the "from" relationships to all needed
        # prims
        if self._filteringOptions.shouldFollowIncomingRelationships():
            primRangeIter = iter(Usd.PrimRange.AllPrims(self._stage.GetPseudoRoot()))
            for prim in primRangeIter:
                primPath = prim.GetPath()
                if primPath in self._primPaths:
                    continue  # no need to capture again

                self._collectIncomingRelationshipsOf(
                    primPath, prim, returnToPathsForAdditionals
                )

        if returnToPathsForAdditionals:
            self._captureAdditionalRelationshipsOf(returnToPathsForAdditionals)

        updateFilteringOptionsFromInfoCollector(
            self._filteringOptions, self._relInfoCollector
        )

    def _collectTargetRelationshipsOf(
        self, primPath, prim, returnToPathsForAdditionals
    ):
        record = self._getOrCreateRecordFor(primPath)

        def perTargetCallback(relName, targetPath, targetPrimPath):
            targetPrimExists, invalidMessage = self._validateRelTargetPath(
                targetPath, targetPrimPath
            )
            if targetPrimExists:
                targetRecord = self._getOrCreateRecordFor(targetPrimPath)
                targetRecord.addRelationshipFrom(relName, primPath)
                if not invalidMessage:
                    returnToPathsForAdditionals.add(targetPrimPath)
            record.addRelationshipTo(relName, targetPath, invalidMessage)

        def noTargetsCallback(relNames):
            record.addUntargetedToRelationships(relNames)

        self._visitRelationshipsOf(prim, perTargetCallback, noTargetsCallback)

    def _collectIncomingRelationshipsOf(
        self, primPath, prim, returnToPathsForAdditionals
    ):
        # note: primPath/prim here is a prim that is _not_ in self._primPaths,
        # so it's some _other_ prim on the stage, which _might_ have a relationship
        # to one of the prims in self._primPaths
        def perTargetCallback(relName, targetPath, targetPrimPath):
            if targetPrimPath not in self._primPaths:
                # this relationship isn't targeting one of the prims that we
                # care about, so disregard it
                return

            # _ should always be true below ("target prim exists"), since
            # targetPrimPath will be in self._primPaths - but we validate anyway,
            # in case it's a property path for a property that might not exist
            _, invalidMessage = self._validateRelTargetPath(targetPath, targetPrimPath)
            sourceRecord = self._getOrCreateRecordFor(primPath)
            sourceRecord.addRelationshipTo(relName, targetPath, invalidMessage)
            targetRecord = self._getOrCreateRecordFor(targetPrimPath)
            targetRecord.addRelationshipFrom(relName, primPath, invalidMessage)

        def noTargetsCallback(relNames):
            record = self.getRecordFor(primPath)
            if record:
                record.addUntargetedToRelationships(relNames)

        self._visitRelationshipsOf(prim, perTargetCallback, noTargetsCallback)
        # if we ended up with an entry for this prim after processing all of its
        # relationships, return to it for possible "additionals"
        if self.hasRecordFor(primPath):
            returnToPathsForAdditionals.add(primPath)

    def _visitRelationshipsOf(self, prim, perTargetCallback, noTargetsCallback=None):
        # just putting the relationship & target traversal in one place, using
        # callbacks passed in to grab what they want...
        self._relInfoCollector.addPrimTypeName(prim.GetTypeName())
        if not self._filteringOptions.shouldFollowRelationshipsOf(prim):
            return

        relsWithNoTargets = []
        for rel in prim.GetRelationships():
            relName = rel.GetName()
            self._relInfoCollector.addRelationshipName(relName)

            if not self._filteringOptions.shouldFollowRelationship(prim, rel):
                continue

            relTargets = rel.GetTargets()
            if not relTargets:
                relsWithNoTargets.append(relName)

            for targetPath in relTargets:
                if targetPath.IsPropertyPath():
                    # it's a property relationship target
                    self._relInfoCollector.addPropertyName(targetPath.name)
                    if not self._filteringOptions.shouldIncludePropertyRelationships():
                        continue
                else:
                    # it's a prim relationship target
                    if not self._filteringOptions.shouldIncludePrimRelationships():
                        continue

                if not self._filteringOptions.shouldFollowRelationshipTarget(
                    prim, rel, targetPath
                ):
                    continue

                targetPrimPath = targetPath.GetPrimPath()
                perTargetCallback(relName, targetPath, targetPrimPath)

        if relsWithNoTargets and noTargetsCallback:
            noTargetsCallback(relsWithNoTargets)

    def _captureAdditionalRelationshipsOf(self, primPaths):
        """This is used to capture additional relationships that are currently
        outside the scope of the relationships of concern, so we can at least
        list them, for the user to potentially follow...
        """
        for primPath in primPaths:
            relRecord = self.getRecordFor(primPath)
            if not relRecord:
                # no record for this path, so no need to include it for additionals
                continue

            prim = self._stage.GetPrimAtPath(primPath)
            if not prim:
                continue  # must be a broken relationship or something?

            def perTargetCallback(relName, targetPath, targetPrimPath):
                # only add additionals for paths that aren't already in relRecord's
                # "to relationships" - since there could be invalid relationships
                # for which we don't have records
                if not self.hasRecordFor(
                    targetPrimPath
                ) and not relRecord.hasRelationshipTo(targetPath):
                    relRecord.addAdditionalToRelationship(relName, targetPath)

            self._visitRelationshipsOf(prim, perTargetCallback)

    def _getOrCreateRecordFor(self, primPath):
        if not self.hasRecordFor(primPath):
            primRelRecord = PrimRelationshipRecord(
                stage=self.getStage(), primPath=primPath, relationshipCollection=self
            )
            self._relsByPrimPath[primPath] = primRelRecord
        return self._relsByPrimPath[primPath]

    def _validateRelTargetPath(self, targetPath, targetPrimPath):
        targetPrim = self._stage.GetPrimAtPath(targetPrimPath)
        if not targetPrim:
            return False, "The specified prim does not exist"

        if targetPath.IsPropertyPath():
            prop = targetPrim.GetProperty(targetPath.name)
            if not prop:
                return False, "The specified property does not exist"

        return True, None
