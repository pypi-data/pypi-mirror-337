from unittest import mock, TestCase

from pxr import Sdf

from relview.data.PrimTypeFilter import PrimTypeFilter, PrimTypeFilterUpdater


class PrimTypeFilter_TestCase(TestCase):
    """Tests the PrimTypeFilter class."""

    def test_getCategoryName(self):
        self.assertEqual(PrimTypeFilter.getCategoryName(), "Prim Type")

    def test_shouldFollowRelationshipsOf_active(self):
        ptf = PrimTypeFilter("someType")
        with mock.patch.object(
            ptf, "_shouldFollowForPrim", return_value="zoiks"
        ) as mock_shouldFollowForPrim:
            self.assertIsNone(ptf.shouldFollowRelationshipsOf("daPrim"))
        mock_shouldFollowForPrim.assert_not_called()

    def test_shouldFollowRelationshipsOf_inactive(self):
        ptf = PrimTypeFilter("someType")
        ptf.setActive(False)
        with mock.patch.object(
            ptf, "_shouldFollowForPrim", return_value="zoiks"
        ) as mock_shouldFollowForPrim:
            self.assertEqual(ptf.shouldFollowRelationshipsOf("daPrim"), "zoiks")
        mock_shouldFollowForPrim.assert_called_once_with("daPrim")

    def test_shouldFollowRelationshipTarget_active(self):
        ptf = PrimTypeFilter("someType")
        self.assertIsNone(
            ptf.shouldFollowRelationshipTarget("daPrim", "daRel", "someTargetPath")
        )

    def test_shouldFollowRelationshipTarget_noTargetPrim(self):
        ptf = PrimTypeFilter("someType")
        ptf.setActive(False)
        prim = MockPrim()
        stage = MockStage()
        targetPath = Sdf.Path("/path/to/target")
        with mock.patch.object(prim, "GetStage", return_value=stage):
            self.assertIsNone(
                ptf.shouldFollowRelationshipTarget(prim, "daRel", targetPath)
            )

    def test_shouldFollowRelationshipTarget_callsShouldFollow(self):
        ptf = PrimTypeFilter("someType")
        ptf.setActive(False)
        prim = MockPrim()
        stage = MockStage()
        targetPath = Sdf.Path("/path/to/target")
        targetPrim = "daTargetPrim"
        with mock.patch.object(prim, "GetStage", return_value=stage):
            with mock.patch.object(stage, "GetPrimAtPath", return_value=targetPrim):
                with mock.patch.object(
                    ptf, "_shouldFollowForPrim", return_value="sure"
                ) as mock_shouldFollowForPrim:
                    self.assertEqual(
                        ptf.shouldFollowRelationshipTarget(prim, "daRel", targetPath),
                        "sure",
                    )
        mock_shouldFollowForPrim.assert_called_once_with(targetPrim)

    def test__shouldFollowForPrim(self):
        ptf = PrimTypeFilter("someType")
        prim = MockPrim()
        with mock.patch.object(prim, "GetTypeName", return_value="someType"):
            self.assertFalse(ptf._shouldFollowForPrim(prim))
        with mock.patch.object(prim, "GetTypeName", return_value="anotherType"):
            self.assertIsNone(ptf._shouldFollowForPrim(prim))


class PrimTypeFilterUpdater_TestCase(TestCase):
    """Tests the PrimTypeFilterUpdater class"""

    def test_classData(self):
        self.assertEqual(PrimTypeFilterUpdater.CATEGORY_NAME, "Prim Type")
        self.assertEqual(PrimTypeFilterUpdater.FILTER_CLASS, PrimTypeFilter)

    def test__getDataFromInfoCollector(self):
        updater = PrimTypeFilterUpdater()
        relInfoCollector = MockRelationshipInfoCollector()
        with mock.patch.object(
            relInfoCollector, "getPrimTypeNames", return_value=["sweet"]
        ):
            self.assertEqual(
                updater._getDataFromInfoCollector(relInfoCollector), ["sweet"]
            )


#
# some mocks
#
class MockPrim(object):
    def GetStage(self):
        return None

    def GetTypeName(self):
        return None


class MockStage(object):
    def GetPrimAtPath(self, primPath):
        return None


class MockRelationshipInfoCollector(object):
    def getPrimTypeNames(self):
        return None
