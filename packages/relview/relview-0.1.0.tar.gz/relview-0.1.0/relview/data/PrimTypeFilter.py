from .filterUpdating import BaseRelationshipFilterUpdater
from .RelationshipFiltering import RelationshipFilter


PRIM_TYPE_CATEGORY_NAME = "Prim Type"


class PrimTypeFilter(RelationshipFilter):
    """RelationshipFilter that, when disabled, excludes relationships based on
    prim type name. Note: name in this class is the prim type name.
    """

    #
    # RelationshipFilter overrides
    #
    @classmethod
    def getCategoryName(cls):
        return PRIM_TYPE_CATEGORY_NAME

    def shouldFollowRelationshipsOf(self, prim):
        return self._shouldFollowForPrim(prim) if not self.isActive() else None

    def shouldFollowRelationshipTarget(self, prim, relationship, targetPath):
        if self.isActive():
            return None

        stage = prim.GetStage()
        targetPrim = stage.GetPrimAtPath(targetPath.GetPrimPath())
        if not targetPrim:
            return None

        return self._shouldFollowForPrim(targetPrim)

    def _shouldFollowForPrim(self, prim):
        return False if prim.GetTypeName() == self._name else None


class PrimTypeFilterUpdater(BaseRelationshipFilterUpdater):
    """Updater for PrimTypeFilter instances."""

    CATEGORY_NAME = PRIM_TYPE_CATEGORY_NAME
    FILTER_CLASS = PrimTypeFilter

    def _getDataFromInfoCollector(self, relInfoCollector):
        return relInfoCollector.getPrimTypeNames()
