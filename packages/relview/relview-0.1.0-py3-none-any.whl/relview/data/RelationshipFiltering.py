from collections import defaultdict, OrderedDict
from Qt import QtCore

from .decorators import callOnceDeferred


class RelationshipFilteringOptions(QtCore.QObject):
    """Encapsulates a set of directives for determining what relationships are
    considered/captured/followed while a RelationshipCollection is traversing
    the USD stage. Has a set of "core" considerations (whether to follow target,
    incoming, prim, and/or property relationships) as well as different categories
    of configurarable, updatable "relationship filters" (see RelationshipFilter,
    below). Note that there's a singleton instance available, which will typically
    be updated from the most recently user-modified instance of this class. Each
    RelationshipCollection object will have its own instance of this class, usually
    cloned from another.
    """

    # signals
    FollowTargetRelationshipsChangedTo = QtCore.Signal(bool)
    FollowIncomingRelationshipsChangedTo = QtCore.Signal(bool)
    IncludePrimRelationshipsChangedTo = QtCore.Signal(bool)
    IncludePropertyRelationshipsChangedTo = QtCore.Signal(bool)

    FilterRegistered = QtCore.Signal(object)
    FilterActivationChanged = QtCore.Signal(object, bool)

    Changed = QtCore.Signal()

    # class constants
    FILTER_CLASSES_BY_CATEGORY_NAME = OrderedDict()

    # the singleton instance
    _INSTANCE = None

    # instance state
    _includeTargetRels = True
    _includeIncomingRels = True
    _includePrimRels = True
    _includePropertyRels = True

    @classmethod
    def registerFilterClass(cls, filterClass):
        cls.FILTER_CLASSES_BY_CATEGORY_NAME[filterClass.getCategoryName()] = filterClass

    @classmethod
    def getInstance(cls):
        if cls._INSTANCE is None:
            cls._INSTANCE = cls()
        return cls._INSTANCE

    def __init__(self, parent=None):
        super().__init__(parent)
        self._filtersByCategory = defaultdict(set)
        self.clearFilters()
        self._makeConnections()

    #
    # public API
    #
    def getNumFilterExclusions(self):
        numPossible, currentlyActive = 0, 0
        for func in [
            self.shouldFollowTargetRelationships,
            self.shouldFollowIncomingRelationships,
            self.shouldIncludePrimRelationships,
            self.shouldIncludePropertyRelationships,
        ]:
            numPossible += 1
            if func():
                currentlyActive += 1

        for filterObj in self.getAllFilters():
            numPossible += 1
            if filterObj.isActive():
                currentlyActive += 1

        return numPossible - currentlyActive

    def shouldFollowTargetRelationships(self):
        return self._includeTargetRels

    def followTargetRelationships(self, follow=True, signal=True):
        if follow != self._includeTargetRels:
            self._includeTargetRels = bool(follow)
            if signal:
                self.FollowTargetRelationshipsChangedTo.emit(self._includeTargetRels)

    def shouldFollowIncomingRelationships(self):
        return self._includeIncomingRels

    def followIncomingRelationships(self, follow=True, signal=True):
        if follow != self._includeIncomingRels:
            self._includeIncomingRels = bool(follow)
            if signal:
                self.FollowIncomingRelationshipsChangedTo.emit(
                    self._includeIncomingRels
                )

    def shouldIncludePrimRelationships(self):
        return self._includePrimRels

    def includePrimRelationships(self, include=True, signal=True):
        if include != self._includePrimRels:
            self._includePrimRels = bool(include)
            if signal:
                self.IncludePrimRelationshipsChangedTo.emit(self._includePrimRels)

    def shouldIncludePropertyRelationships(self):
        return self._includePropertyRels

    def includePropertyRelationships(self, include=True, signal=True):
        if include != self._includePropertyRels:
            self._includePropertyRels = bool(include)
            if signal:
                self.IncludePropertyRelationshipsChangedTo.emit(
                    self._includePropertyRels
                )

    #
    # individual filtering
    #
    def registerFilter(self, filterObj, signal=True):
        # filterObj should be an instance of RelationshipFilter
        self.registerFilterClass(filterObj.__class__)  # just in case it's not already
        catName = filterObj.getCategoryName()
        if filterObj not in self._filtersByCategory[catName]:
            self._filtersByCategory[catName].add(filterObj)
            filterObj.setParent(self)
            self._connectToFilter(filterObj)
            if signal:
                self.FilterRegistered.emit(filterObj)

    def clearFilters(self):
        for catName in self.FILTER_CLASSES_BY_CATEGORY_NAME.keys():
            for filterObj in self._filtersByCategory[catName]:
                filterObj.setParent(None)
                filterObj.deleteLater()
            self._filtersByCategory[catName] = set()

    def getFilterCategoryNames(self):
        return list(self._filtersByCategory.keys())

    def getFiltersInCategory(self, categoryName):
        return sorted(self._filtersByCategory[categoryName], key=lambda f: f.getName())

    def getFilterInCategoryNamed(self, categoryName, filterName):
        for filterObj in self._filtersByCategory[categoryName]:
            if filterObj.getName() == filterName:
                return filterObj
        return None

    def getAllFilters(self):
        filterObjs = []
        for categoryName in self.getFilterCategoryNames():
            filterObjs += self.getFiltersInCategory(categoryName)
        return filterObjs

    #
    # Methods which consider each registered RelationshipFilter instance with
    # the provided data. RelationshipCollection will call these during different
    # phases of collecting relationships from the USD stage.
    #
    def shouldFollowRelationshipsOf(self, prim):
        return self._visitFiltersWith(self._shouldFollowRelationshipsOfFunc, prim)

    def shouldFollowRelationship(self, prim, relationship):
        return self._visitFiltersWith(
            self._shouldFollowRelationshipFunc, prim, relationship
        )

    def shouldFollowRelationshipTarget(self, prim, relationship, targetPath):
        return self._visitFiltersWith(
            self._shouldFollowRelationshipTargetFunc, prim, relationship, targetPath
        )

    #
    # cloning - typically from the singleton instance
    #
    def clone(self, parent=None):
        return self.createFromDict(self.toDict(), parent)

    #
    # serialization/deserialization stuff
    #
    @classmethod
    def createFromDict(cls, dataDict, parent=None):
        newObj = cls(parent)
        newObj.initFromDict(dataDict, emitSignals=False)
        return newObj

    def initFromDict(self, dataDict, emitSignals=True):
        for attrName, method in [
            ("follow_target_rels", self.followTargetRelationships),
            ("follow_incoming_rels", self.followIncomingRelationships),
            ("include_prim_rels", self.includePrimRelationships),
            ("include_property_rels", self.includePropertyRelationships),
        ]:
            val = dataDict.get(attrName)
            if val is not None:
                method(val, signal=emitSignals)

        self.clearFilters()  # just in case there already are some
        filtersDict = dataDict.get("filters", {})
        for catName, filterDataDictList in filtersDict.items():
            if catName not in self.FILTER_CLASSES_BY_CATEGORY_NAME:
                continue  # TODO error/assert?

            filterClass = self.FILTER_CLASSES_BY_CATEGORY_NAME[catName]
            for filterDataDict in filterDataDictList:
                filterObj = filterClass.createFromDict(filterDataDict, self)
                self.registerFilter(filterObj, signal=emitSignals)

    def toDict(self):
        dataDict = dict(
            follow_target_rels=self.shouldFollowTargetRelationships(),
            follow_incoming_rels=self.shouldFollowIncomingRelationships(),
            include_prim_rels=self.shouldIncludePrimRelationships(),
            include_property_rels=self.shouldIncludePropertyRelationships(),
        )
        filtersDict = {}
        for categoryName in self.getFilterCategoryNames():
            catFilters = self.getFiltersInCategory(categoryName)
            filtersDict[categoryName] = [filterObj.toDict() for filterObj in catFilters]
        dataDict["filters"] = filtersDict
        return dataDict

    #
    # slots
    #
    def _filterActiveChangedToSLOT(self, nowActive):
        self.FilterActivationChanged.emit(self.sender(), nowActive)

    @callOnceDeferred("_willCallGenericEmittingChangedSLOT")
    def _genericEmittingChangedSLOT(self, *args_notUsed):
        # Note: using @callOnceDeferred so a bunch of calls from something like
        # a filter dialog being OK'ed don't cause a whole ton of changed signals
        # to be emitted, when it's really just one "big change")
        self.Changed.emit()

    #
    # private helper methods
    #
    def _makeConnections(self):
        # connect each of our specific "something changed" signals to one slot
        # that will just emit Changed (which is likely what most clients really
        # care about)
        for signal in [
            self.FollowTargetRelationshipsChangedTo,
            self.FollowIncomingRelationshipsChangedTo,
            self.IncludePrimRelationshipsChangedTo,
            self.IncludePropertyRelationshipsChangedTo,
            self.FilterRegistered,
            self.FilterActivationChanged,
        ]:
            signal.connect(self._genericEmittingChangedSLOT)

    def _connectToFilter(self, filterObj):
        filterObj.ActiveChangedTo.connect(self._filterActiveChangedToSLOT)

    def _visitFiltersWith(self, perFilterCallback, *args):
        for _, filterSet in self._filtersByCategory.items():
            for filterObj in filterSet:
                answer = perFilterCallback(filterObj, *args)
                if answer is not None:
                    # one of the filter's "should" methods (shouldFollowRelationshipsOf(),
                    # shouldFollowRelationship(), and shouldFollowRelationshipTarget())
                    # can return True or False to short circuit to an answer - the
                    # typical None response is "I have no opinion on that"
                    return answer

        # by default, YES, visit prims/properties and capture relationships
        return True

    def _shouldFollowRelationshipsOfFunc(self, filterObj, prim):
        return filterObj.shouldFollowRelationshipsOf(prim)

    def _shouldFollowRelationshipFunc(self, filterObj, prim, relationship):
        return filterObj.shouldFollowRelationship(prim, relationship)

    def _shouldFollowRelationshipTargetFunc(
        self, filterObj, prim, relationship, targetPath
    ):
        return filterObj.shouldFollowRelationshipTarget(prim, relationship, targetPath)


class RelationshipFilter(QtCore.QObject):
    """Instances of this class get registered with a RelationshipFilteringOptions
    object and instruct the exclusion of certain relationships. Think of "is active"
    as being "is included" - so when _inactive_, a RelationshipFilter will be
    _excluding_ relationships according to its category/criteria. Seems weird that
    these things effectively do their work when they're "inactive" but that's what
    we've got... (TODO would "is excluding" be a better term, and not confusing due
    to the double-negative?)

    Subclasses should implement getCategoryName(), getName(), getCloneConstructorArgs(),
    and one or more of the "should" methods: shouldFollowRelationshipsOf(),
    shouldFollowRelationship(), and/or shouldFollowRelationshipTarget().
    """

    # signals
    NameChangedTo = QtCore.Signal(str)
    DescriptionChangedTo = QtCore.Signal(str)
    ActiveChangedTo = QtCore.Signal(bool)

    # instance state
    _isActive = True
    _name = ""
    _description = ""

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self._name = name

    #
    # public API
    #
    @classmethod
    def getCategoryName(cls):
        raise NotImplementedError("getCategoryName() must be implemented")

    def getName(self):
        return self._name

    def setName(self, newName):
        if newName != self._name:
            self._name = newName
            self.NameChangedTo.emit(self._name)

    def getDescription(self):
        return self._description

    def setDescription(self, newDesc):
        if newDesc != self._description:
            self._description = newDesc
            self.DescriptionChangedTo.emit(self._description)

    def isActive(self):
        return self._isActive

    def setActive(self, active=True, signalIt=True):
        if active != self._isActive:
            self._isActive = bool(active)
            if signalIt:
                self.ActiveChangedTo.emit(self._isActive)

    #
    # "should" methods
    #  - return None to indicate "I have no opinion on the matter"
    #  - return True or False to answer (which will short-circuit the remaining
    #    filters of the parent RelationshipFilteringOptions)
    #  - typically only return something other than None when _inactive_ ("inactive"
    #    meaning "is excluding")
    #
    def shouldFollowRelationshipsOf(self, prim):
        return None

    def shouldFollowRelationship(self, prim, relationship):
        return None

    def shouldFollowRelationshipTarget(self, prim, relationship, targetPath):
        return None

    #
    # cloning
    #
    def clone(self, parent=None):
        return self.createFromDict(self.toDict(), parent)

    #
    # serialization/deserialization stuff
    #
    @classmethod
    def createFromDict(cls, dataDict, parent=None):
        obj = cls(*cls.getConstructorArgsFrom(dataDict, parent))
        obj.initFromDict(dataDict)
        return obj

    @classmethod
    def getConstructorArgsFrom(cls, dataDict, parent=None):
        # subclasses can override if needed
        return (dataDict.get("name", ""), parent)

    def initFromDict(self, dataDict):
        # subclasses can further implement if needed
        for attrName, method in [
            ("is_active", self.setActive),
            ("name", self.setName),
            ("description", self.setDescription),
        ]:
            val = dataDict.get(attrName)
            if val is not None:
                method(val)

    def toDict(self):
        # subclasses should implement further
        return dict(
            is_active=self.isActive(),
            name=self.getName(),
            description=self.getDescription(),
        )
