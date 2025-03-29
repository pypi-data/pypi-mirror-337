"""Functions and classes in here are for "updating" RelationshipFilteringOptions
instances, either from RelationshipInfoCollector objects or from other
RelationshipFilteringOptions. Subclass RelationshipFilteringOptionsUpdater and
register an instance of it via registerFilteringOptionsUpdater() to make the
magic happen.
"""

_FILTERING_OPTIONS_UPDATERS = []


def registerFilteringOptionsUpdater(updaterObj):
    """Adds the provided instance of RelationshipFilteringOptionsUpdater to the
    global list of updaters to be used when needed.
    """
    global _FILTERING_OPTIONS_UPDATERS
    _FILTERING_OPTIONS_UPDATERS.append(updaterObj)


def updateFilteringOptionsFromInfoCollector(toUpdate, relInfoCollector):
    """Uses the available updaters to update toUpdate (RelationshipFilteringOptions
    object) from relInfoCollector (RelationshipInfoCollector object).
    """
    for updater in _FILTERING_OPTIONS_UPDATERS:
        updater.updateFilteringOptionsFromInfoCollector(toUpdate, relInfoCollector)


def updateFilteringOptionsFromOther(toUpdate, updateFrom):
    """Uses the available updaters to update toUpdate (RelationshipFilteringOptions
    object) from updateFrom (another RelationshipFilteringOptions object).
    """
    for updater in _FILTERING_OPTIONS_UPDATERS:
        updater.updateFilteringOptionsFromOther(toUpdate, updateFrom)


#
# filtering option "updaters"
#
class RelationshipFilteringOptionsUpdater(object):
    """Base class of object for updating a RelationshipFilteringOptions object
    from a RelationshipInfoCollector and/or another RelationshipFilteringOptions.
    Subclass and register via registerFilteringOptionsUpdater(), then when calls
    to updateFilteringOptionsFromInfoCollector() and updateFilteringOptionsFromOther()
    are called, the updated can do its thing.
    """

    def updateFilteringOptionsFromInfoCollector(self, toUpdate, relInfoCollector):
        pass

    def updateFilteringOptionsFromOther(self, toUpdate, updateFrom):
        pass


class CoreOptionsUpdater(RelationshipFilteringOptionsUpdater):
    """Updates the "core" options of one RelationshipFilteringOptions object
    from another.
    """

    def updateFilteringOptionsFromOther(self, toUpdate, updateFrom):
        toUpdate.followTargetRelationships(updateFrom.shouldFollowTargetRelationships())
        toUpdate.followIncomingRelationships(
            updateFrom.shouldFollowIncomingRelationships()
        )
        toUpdate.includePrimRelationships(updateFrom.shouldIncludePrimRelationships())
        toUpdate.includePropertyRelationships(
            updateFrom.shouldIncludePropertyRelationships()
        )


class FilterCloningUpdater(RelationshipFilteringOptionsUpdater):
    """Updates the RelationshipFilter instances of one RelationshipFilteringOptions
    from those of another.
    """

    def updateFilteringOptionsFromOther(self, toUpdate, updateFrom):
        """Want the available filters and their active statuses to be the same
        in toUpdate as they are in updateFrom - so clone from updateFrom whatever
        filters don't exist in toUpdate and enable/disable them all to match.
        """
        for categoryName in updateFrom.getFilterCategoryNames():
            for fromFilterObj in updateFrom.getFiltersInCategory(categoryName):
                toFilterObj = toUpdate.getFilterInCategoryNamed(
                    categoryName, fromFilterObj.getName()
                )
                if toFilterObj is not None:
                    toFilterObj.initFromDict(fromFilterObj.toDict())
                else:
                    toFilterObj = fromFilterObj.clone(toUpdate)
                    toUpdate.registerFilter(toFilterObj)


class BaseRelationshipFilterUpdater(RelationshipFilteringOptionsUpdater):
    """Convenience base class for updating a RelationshipFilteringOptions's child
    RelationshipFilter objects from a RelationshipInfoCollector. (FilterCloningUpdater,
    above, takes care of updating the filters of one RelationshipFilteringOptions
    from another.
    """

    CATEGORY_NAME = None  # subclasses must define
    FILTER_CLASS = None  # subclasses must define

    def updateFilteringOptionsFromInfoCollector(self, toUpdate, relInfoCollector):
        for nameStr in self._getDataFromInfoCollector(relInfoCollector):
            filterObj = toUpdate.getFilterInCategoryNamed(self.CATEGORY_NAME, nameStr)
            if filterObj is None:
                filterObj = self.FILTER_CLASS(nameStr, toUpdate)
                toUpdate.registerFilter(filterObj)

    def _getDataFromInfoCollector(self, relInfoCollector):
        raise NotImplementedError("_getDataFromInfoCollector() must be implemented!")
