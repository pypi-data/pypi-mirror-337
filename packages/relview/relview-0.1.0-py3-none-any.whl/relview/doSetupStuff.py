"""This is where we do some "setup stuff" for the default configuration of the
Relationship Viewer. Plug-ins can obivously change things from here, as needed...
"""

from .data import (
    filterUpdating,
    PrimTypeFilter,
    PropertyNameFilter,
    RelationshipFiltering,
    RelationshipNameFilter,
)

# default filter classes/categories
for filterClass in [
    RelationshipNameFilter.RelationshipNameFilter,
    PrimTypeFilter.PrimTypeFilter,
    PropertyNameFilter.PropertyNameFilter,
]:
    RelationshipFiltering.RelationshipFilteringOptions.registerFilterClass(filterClass)


# filter updaters
filterUpdating.registerFilteringOptionsUpdater(filterUpdating.CoreOptionsUpdater())
filterUpdating.registerFilteringOptionsUpdater(filterUpdating.FilterCloningUpdater())

filterUpdating.registerFilteringOptionsUpdater(
    RelationshipNameFilter.RelationshipNameFilterUpdater()
)
filterUpdating.registerFilteringOptionsUpdater(PrimTypeFilter.PrimTypeFilterUpdater())
filterUpdating.registerFilteringOptionsUpdater(
    PropertyNameFilter.PropertyNameFilterUpdater()
)
