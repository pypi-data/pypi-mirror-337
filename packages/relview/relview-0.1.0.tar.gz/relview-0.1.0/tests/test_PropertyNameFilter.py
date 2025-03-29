from unittest import mock, TestCase

from pxr import Sdf

from relview.data.PropertyNameFilter import (
    PropertyNameFilter,
    PropertyNameFilterUpdater,
)


class PropertyNameFilter_TestCase(TestCase):
    """Tests the PropertyNameFilter class."""

    def test_getCategoryName(self):
        self.assertEqual(PropertyNameFilter.getCategoryName(), "Property Name")

    def test_shouldFollowRelationshipTarget_active(self):
        ptf = PropertyNameFilter("someProperty")
        self.assertIsNone(
            ptf.shouldFollowRelationshipTarget(
                "daPrim", "daRelationship", "daTargetPath"
            )
        )

    def test_shouldFollowRelationshipTarget_inactive(self):
        ptf = PropertyNameFilter("someProperty")
        ptf.setActive(False)
        primPath = Sdf.Path("/path/to/prim")
        otherPropertyPath = Sdf.Path("/path/to/prim.otherProp")
        thisPropertyPath = Sdf.Path("/path/to/prim.someProperty")
        self.assertIsNone(
            ptf.shouldFollowRelationshipTarget("daPrim", "daRelationship", primPath)
        )
        self.assertIsNone(
            ptf.shouldFollowRelationshipTarget(
                "daPrim", "daRelationship", otherPropertyPath
            )
        )
        self.assertFalse(
            ptf.shouldFollowRelationshipTarget(
                "daPrim", "daRelationship", thisPropertyPath
            )
        )


class PropertyNameFilterUpdater_TestCase(TestCase):
    """Tests the PropertyNameFilterUpdater class"""

    def test_classData(self):
        self.assertEqual(PropertyNameFilterUpdater.CATEGORY_NAME, "Property Name")
        self.assertEqual(PropertyNameFilterUpdater.FILTER_CLASS, PropertyNameFilter)

    def test__getDataFromInfoCollector(self):
        updater = PropertyNameFilterUpdater()
        relInfoCollector = MockRelationshipInfoCollector()
        with mock.patch.object(
            relInfoCollector, "getPropertyNames", return_value=["dude"]
        ):
            self.assertEqual(
                updater._getDataFromInfoCollector(relInfoCollector), ["dude"]
            )


#
# some mocks
#
class MockRelationshipInfoCollector(object):
    def getPropertyNames(self):
        return None
