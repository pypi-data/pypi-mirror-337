from collections import OrderedDict
from unittest import mock, TestCase

from relview.data import filterUpdating
from relview.data import RelationshipFiltering


#
# test cases
#
class BaseFilterUpdatingTestCase(TestCase):
    """Base class for testing filter updating stuff. Clears out the updaters
    etc. before & after test runs.
    """

    def setUp(self):
        self._clearOut()

    def tearDown(self):
        self._clearOut()

    def _clearOut(self):
        RelationshipFiltering.RelationshipFilteringOptions.FILTER_CLASSES_BY_CATEGORY_NAME = (
            OrderedDict()
        )
        filterUpdating._FILTERING_OPTIONS_UPDATERS = []


class filterUpdatingFunctions_TestCase(BaseFilterUpdatingTestCase):
    """Tests the filter-updating-related functions:
    - registerFilteringOptionsUpdater()
    - updateFilteringOptionsFromInfoCollector()
    - updateFilteringOptionsFromOther()
    """

    def test_registerFilteringOptionsUpdater(self):
        self.assertEqual(filterUpdating._FILTERING_OPTIONS_UPDATERS, [])
        filterUpdating.registerFilteringOptionsUpdater("ugh")
        filterUpdating.registerFilteringOptionsUpdater("nooice")
        self.assertEqual(filterUpdating._FILTERING_OPTIONS_UPDATERS, ["ugh", "nooice"])

    def test_updateFilteringOptionsFromInfoCollector(self):
        updater1 = MockFilterUpdater()
        updater2 = MockFilterUpdater()
        updaters = [updater1, updater2]
        for updater in updaters:
            filterUpdating.registerFilteringOptionsUpdater(updater)
        filterUpdating.updateFilteringOptionsFromInfoCollector(
            "toUpdate", "relInfoCollector"
        )
        for updater in updaters:
            self.assertEqual(
                updater._updatedFromInfoCollectors, [("toUpdate", "relInfoCollector")]
            )

    def test_updateFilteringOptionsFromOther(self):
        updater1 = MockFilterUpdater()
        updater2 = MockFilterUpdater()
        updaters = [updater1, updater2]
        for updater in updaters:
            filterUpdating.registerFilteringOptionsUpdater(updater)
        filterUpdating.updateFilteringOptionsFromOther("toUpdate", "updateFrom")
        for updater in updaters:
            self.assertEqual(updater._updatedFromOthers, [("toUpdate", "updateFrom")])


class RelationshipFilteringOptionsUpdater_TestCase(TestCase):
    """Tests the RelationshipFilteringOptionsUpdater (just here for the coverage)."""

    def test_updateFilteringOptionsFromInfoCollector(self):
        obj = filterUpdating.RelationshipFilteringOptionsUpdater()
        obj.updateFilteringOptionsFromInfoCollector("dude", "sweet")

    def test_updateFilteringOptionsFromOther(self):
        obj = filterUpdating.RelationshipFilteringOptionsUpdater()
        obj.updateFilteringOptionsFromOther("foo", "bar")


class CoreOptionsUpdater_TestCase(TestCase):
    """Tests the CoreOptionsUpdater class."""

    def test_updateFilteringOptionsFromOther(self):
        toUpdate = RelationshipFiltering.RelationshipFilteringOptions()
        updateFrom = RelationshipFiltering.RelationshipFilteringOptions()
        toUpdate.followTargetRelationships(False)
        toUpdate.followIncomingRelationships(False)
        toUpdate.includePrimRelationships(False)
        toUpdate.includePropertyRelationships(False)
        self.assertFalse(toUpdate.shouldFollowTargetRelationships())
        self.assertFalse(toUpdate.shouldFollowIncomingRelationships())
        self.assertFalse(toUpdate.shouldIncludePrimRelationships())
        self.assertFalse(toUpdate.shouldIncludePropertyRelationships())
        self.assertTrue(updateFrom.shouldFollowTargetRelationships())
        self.assertTrue(updateFrom.shouldFollowIncomingRelationships())
        self.assertTrue(updateFrom.shouldIncludePrimRelationships())
        self.assertTrue(updateFrom.shouldIncludePropertyRelationships())

        obj = filterUpdating.CoreOptionsUpdater()
        obj.updateFilteringOptionsFromOther(toUpdate, updateFrom)
        self.assertTrue(toUpdate.shouldFollowTargetRelationships())
        self.assertTrue(toUpdate.shouldFollowIncomingRelationships())
        self.assertTrue(toUpdate.shouldIncludePrimRelationships())
        self.assertTrue(toUpdate.shouldIncludePropertyRelationships())
        self.assertTrue(updateFrom.shouldFollowTargetRelationships())
        self.assertTrue(updateFrom.shouldFollowIncomingRelationships())
        self.assertTrue(updateFrom.shouldIncludePrimRelationships())
        self.assertTrue(updateFrom.shouldIncludePropertyRelationships())


class FilterCloningUpdater_TestCase(BaseFilterUpdatingTestCase):
    """Tests the FilterCloningUpdater class."""

    def test_updateFilteringOptionsFromOther(self):
        class KickassFilter(RelationshipFiltering.RelationshipFilter):
            @classmethod
            def getCategoryName(cls):
                return "Kickass"

        class NooiceFilter(RelationshipFiltering.RelationshipFilter):
            @classmethod
            def getCategoryName(cls):
                return "Nooice"

        RelationshipFiltering.RelationshipFilteringOptions.registerFilterClass(
            KickassFilter
        )
        RelationshipFiltering.RelationshipFilteringOptions.registerFilterClass(
            NooiceFilter
        )

        updateFrom = RelationshipFiltering.RelationshipFilteringOptions()
        updateFromKickassFilter = KickassFilter("Super kickass")
        updateFromKickassFilter.setActive(False)
        updateFrom.registerFilter(updateFromKickassFilter)
        updateFromNooiceFilter = NooiceFilter("Very nooice")
        updateFrom.registerFilter(updateFromNooiceFilter)

        toUpdate = RelationshipFiltering.RelationshipFilteringOptions()
        toUpdateKickassFilter = KickassFilter("Super kickass")
        toUpdate.registerFilter(toUpdateKickassFilter)

        filterCloningUpdater = filterUpdating.FilterCloningUpdater()
        filterCloningUpdater.updateFilteringOptionsFromOther(toUpdate, updateFrom)

        # toUpdate and updateFrom should now both have the same filters, with
        # the same options
        self.assertEqual(toUpdate.toDict(), updateFrom.toDict())


class BaseRelationshipFilterUpdater_TestCase(TestCase):
    """Tests the BaseRelationshipFilterUpdater class"""

    def test_updateFilteringOptionsFromInfoCollector(self):
        class TestFilter(RelationshipFiltering.RelationshipFilter):
            @classmethod
            def getCategoryName(cls):
                return "Supderduper"

        updater = filterUpdating.BaseRelationshipFilterUpdater()
        updater.CATEGORY_NAME = TestFilter.getCategoryName()
        updater.FILTER_CLASS = TestFilter

        toUpdate = RelationshipFiltering.RelationshipFilteringOptions()
        self.assertEqual(toUpdate.getFilterCategoryNames(), [])

        with mock.patch.object(
            updater, "_getDataFromInfoCollector", return_value=["dude", "sweet"]
        ):
            updater.updateFilteringOptionsFromInfoCollector(toUpdate, "asdasdas")

        self.assertEqual(toUpdate.getFilterCategoryNames(), ["Supderduper"])
        filterNames = set(
            [f.getName() for f in toUpdate.getFiltersInCategory("Supderduper")]
        )
        self.assertEqual(filterNames, set(["dude", "sweet"]))

    def test__getDataFromInfoCollector_error(self):
        updater = filterUpdating.BaseRelationshipFilterUpdater()
        with self.assertRaises(NotImplementedError) as cm:
            updater._getDataFromInfoCollector("asdasd")
        self.assertEqual(
            str(cm.exception), "_getDataFromInfoCollector() must be implemented!"
        )


#
# some mocks
#
class MockFilterUpdater(object):
    def __init__(self):
        self._updatedFromInfoCollectors = []
        self._updatedFromOthers = []

    def updateFilteringOptionsFromInfoCollector(self, toUpdate, relInfoCollector):
        self._updatedFromInfoCollectors.append((toUpdate, relInfoCollector))

    def updateFilteringOptionsFromOther(self, toUpdate, updateFrom):
        self._updatedFromOthers.append((toUpdate, updateFrom))
