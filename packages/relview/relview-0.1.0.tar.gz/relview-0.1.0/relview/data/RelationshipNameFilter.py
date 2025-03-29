from .filterUpdating import BaseRelationshipFilterUpdater
from .RelationshipFiltering import RelationshipFilter


REL_NAME_CATEGORY_NAME = "Relationship Name"


class RelationshipNameFilter(RelationshipFilter):
    """RelationshipFilter that, when disabled, excludes relationships based on
    relationship name. Note: name in this class is the relationship name.
    """

    #
    # RelationshipFilter overrides
    #
    @classmethod
    def getCategoryName(cls):
        return REL_NAME_CATEGORY_NAME

    def shouldFollowRelationship(self, prim, relationship):
        return (
            False
            if (not self.isActive() and relationship.GetName() == self._name)
            else None
        )


class RelationshipNameFilterUpdater(BaseRelationshipFilterUpdater):
    """Updater for RelationshipNameFilter instances."""

    CATEGORY_NAME = REL_NAME_CATEGORY_NAME
    FILTER_CLASS = RelationshipNameFilter

    def _getDataFromInfoCollector(self, relInfoCollector):
        return relInfoCollector.getRelationshipNames()
