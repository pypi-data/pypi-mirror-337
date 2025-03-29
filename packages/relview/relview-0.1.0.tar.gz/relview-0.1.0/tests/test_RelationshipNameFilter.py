from unittest import mock, TestCase

from relview.data.RelationshipNameFilter import (
    RelationshipNameFilter,
    RelationshipNameFilterUpdater,
)


class RelationshipNameFilter_TestCase(TestCase):
    """Tests the RelationshipNameFilter class."""

    def test_getCategoryName(self):
        self.assertEqual(RelationshipNameFilter.getCategoryName(), "Relationship Name")

    def test_shouldFollowRelationship_active(self):
        ptf = RelationshipNameFilter("someProperty")
        self.assertIsNone(ptf.shouldFollowRelationship("daPrim", "daRelationship"))

    def test_shouldFollowRelationship_inactive(self):
        ptf = RelationshipNameFilter("someProperty")
        ptf.setActive(False)
        rel = MockRelationship()
        with mock.patch.object(rel, "GetName", return_value="otherProperty"):
            self.assertIsNone(ptf.shouldFollowRelationship("daPrim", rel))
        with mock.patch.object(rel, "GetName", return_value="someProperty"):
            self.assertFalse(ptf.shouldFollowRelationship("daPrim", rel))


class RelationshipNameFilterUpdater_TestCase(TestCase):
    """Tests the RelationshipNameFilterUpdater class"""

    def test_classData(self):
        self.assertEqual(
            RelationshipNameFilterUpdater.CATEGORY_NAME, "Relationship Name"
        )
        self.assertEqual(
            RelationshipNameFilterUpdater.FILTER_CLASS, RelationshipNameFilter
        )

    def test__getDataFromInfoCollector(self):
        updater = RelationshipNameFilterUpdater()
        relInfoCollector = MockRelationshipInfoCollector()
        with mock.patch.object(
            relInfoCollector, "getRelationshipNames", return_value=["nooice"]
        ):
            self.assertEqual(
                updater._getDataFromInfoCollector(relInfoCollector), ["nooice"]
            )


#
# some mocks
#
class MockRelationship(object):
    def GetName(self):
        return None


class MockRelationshipInfoCollector(object):
    def getRelationshipNames(self):
        return None
