from .filterUpdating import BaseRelationshipFilterUpdater
from .RelationshipFiltering import RelationshipFilter


PROP_NAME_CATEGORY_NAME = "Property Name"


class PropertyNameFilter(RelationshipFilter):
    """RelationshipFilter that, when disabled, excludes relationships based on
    property name. Note: name in this class is the property name.
    """

    #
    # RelationshipFilter overrides
    #
    @classmethod
    def getCategoryName(cls):
        return PROP_NAME_CATEGORY_NAME

    def shouldFollowRelationshipTarget(self, prim, relationship, targetPath):
        if self.isActive():
            return None

        return (
            False
            if (targetPath.IsPropertyPath() and targetPath.name == self._name)
            else None
        )


class PropertyNameFilterUpdater(BaseRelationshipFilterUpdater):
    """Updater for PropertyNameFilter instances."""

    CATEGORY_NAME = PROP_NAME_CATEGORY_NAME
    FILTER_CLASS = PropertyNameFilter

    def _getDataFromInfoCollector(self, relInfoCollector):
        return relInfoCollector.getPropertyNames()
