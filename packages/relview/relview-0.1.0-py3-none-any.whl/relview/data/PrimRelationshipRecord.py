from collections import defaultdict

from pxr import Sdf

from .NamedRelationship import NamedRelationship


class PrimRelationshipRecord(object):
    """Holds onto relationships to and from a certain prim, via different
    lists of NamedRelationship objects. Typical usage is by RelationshipCollection,
    which keeps a dictionary of these objects by prim path, and adds relationships
    to and from as it's traversing the stage. This class also encapsulates
    "additional" relationships, which are those that are just outside the current
    scope of the prims whose relationships are being viewed.

    TODO maybe cache outputs from some of the "get" methods (and invalidate
    caches after any "add" calls), for performance
    """

    def __init__(self, stage, primPath, relationshipCollection=None):
        self._stage = stage
        self._primPath = primPath
        self._relationshipCollection = relationshipCollection

        # below are lists of NamedRelationship, keyed by relationship name
        self._toRelsByName = defaultdict(list)
        self._fromRelsByName = defaultdict(list)
        self._additionalRelsByName = defaultdict(list)

    #
    # public API
    #
    def getStage(self):
        return self._stage

    def getPrimPath(self):
        return self._primPath

    def getPrim(self):
        return self.getStage().GetPrimAtPath(self.getPrimPath())

    def hasRelationshipCollection(self):
        return self._relationshipCollection is not None

    def getRelationshipCollection(self):
        return self._relationshipCollection

    def hasAnyRelationships(self):
        return bool(
            self._toRelsByName or self._fromRelsByName or self._additionalRelsByName
        )

    #
    # "to" relationships - these are for the relationships authored on this prim
    # to other prims/properties
    #
    def hasToRelationships(self):
        return bool(self._toRelsByName)

    def getToRelationshipNames(self):
        return list(self._toRelsByName.keys())

    def getToRelationshipsNamed(self, relName):
        return self._toRelsByName[relName]

    def getToRelationships(self):
        return [nr for relList in self._toRelsByName.values() for nr in relList]

    def getPrimsWithToRelationships(self, omitInvalid=True):
        return _getUniquePrimPathsFromRelList(self.getToRelationships(), omitInvalid)

    def getNumPrimsWithToRelationships(self, omitInvalid=True):
        return len(self.getPrimsWithToRelationships(omitInvalid))

    def addRelationshipTo(self, relName, targetPath, messageIfInvalid=None):
        relTo = NamedRelationship(relName, targetPath, messageIfInvalid)
        if not _isRelInList(relTo, self._toRelsByName[relName]):
            # only if not already there
            self._toRelsByName[relName].append(relTo)

    def addUntargetedToRelationships(self, relNames):
        for relName in relNames:
            self.addRelationshipTo(relName, Sdf.Path())

    def hasAnyUntargetedToRelationships(self):
        # TODO test for this
        for namedRel in self.getToRelationships():
            if namedRel.isEmpty():
                return True
        return False

    def hasRelationshipTo(self, targetPath):
        for namedRel in self.getToRelationships():
            if namedRel.getPath() == targetPath:
                return True
        return False

    def hasAnyInvalidToRelationships(self):
        for namedRel in self.getToRelationships():
            if namedRel.isInvalid():
                return True
        return False

    #
    # "from" relationships - these are for the relationships authored on other
    # prims that are targeting this one
    #
    def hasFromRelationships(self):
        return bool(self._fromRelsByName)

    def getFromRelationshipNames(self):
        return list(self._fromRelsByName.keys())

    def getFromRelationshipsNamed(self, relName):
        return self._fromRelsByName[relName]

    def getFromRelationships(self):
        return [nr for relList in self._fromRelsByName.values() for nr in relList]

    def getPrimsWithFromRelationships(self, omitInvalid=True):
        return _getUniquePrimPathsFromRelList(self.getFromRelationships(), omitInvalid)

    def getNumPrimsWithFromRelationships(self, omitInvalid=True):
        return len(self.getPrimsWithFromRelationships(omitInvalid))

    def addRelationshipFrom(self, relName, sourcePath, messageIfInvalid=None):
        relFrom = NamedRelationship(relName, sourcePath, messageIfInvalid)
        if not _isRelInList(relFrom, self._fromRelsByName[relName]):
            # only if not already there
            self._fromRelsByName[relName].append(relFrom)

    def hasAnyInvalidFromRelationships(self):
        for namedRel in self.getFromRelationships():
            if namedRel.isInvalid():
                return True
        return False

    #
    # "additional" relationships - these are "to" relationships authored on
    # this prim that are outside the scope of the relationships currently being
    # viewed
    #
    def hasAdditionalToRelationships(self):
        return bool(self._additionalRelsByName)

    def getAdditionalToRelationshipNames(self):
        return list(self._additionalRelsByName.keys())

    def getAdditionalToRelationshipsNamed(self, relName):
        return self._additionalRelsByName[relName]

    def getAdditionalToRelationships(self):
        return [nr for relList in self._additionalRelsByName.values() for nr in relList]

    def getNumAdditionalToRelationships(self):
        return len(self.getAdditionalToRelationships())

    def addAdditionalToRelationship(self, relName, toPath):
        relTo = NamedRelationship(relName, toPath)
        if not _isRelInList(relTo, self._additionalRelsByName[relName]):
            # only if not already in there
            self._additionalRelsByName[relName].append(relTo)


#
# private helper functions
#
def _isRelInList(rel, relList):
    for otherRel in relList:
        if otherRel == rel:
            return True
    return False


def _getUniquePrimPathsFromRelList(namedRelList, omitInvalid=True):
    primPathsSeenSoFar = set()
    for namedRel in namedRelList:
        if namedRel.isEmpty():
            continue
        if omitInvalid and namedRel.isInvalid():
            continue
        primPathsSeenSoFar.add(namedRel.getPrimPath())
    return primPathsSeenSoFar
