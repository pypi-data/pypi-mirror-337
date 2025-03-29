from unittest import mock, TestCase
from Qt import QtCore

from relview.data.RelationshipCollectionManager import RelationshipCollectionManager

from .utilsForTesting import SignalReceiver


class RelationshipCollectionManager_TestCase(TestCase):
    """Tests the RelationshipCollectionManager class."""

    def setUp(self):
        self._clearOut()

    def tearDown(self):
        self._clearOut()

    def _clearOut(self):
        RelationshipCollectionManager._INSTANCE = None

    def test_getInstance(self):
        inst = RelationshipCollectionManager.getInstance()
        self.assertEqual(inst.__class__, RelationshipCollectionManager)
        self.assertEqual(inst, RelationshipCollectionManager._INSTANCE)

    def test_init(self):
        relCollMgr = RelationshipCollectionManager()
        self.assertIsNone(relCollMgr._activeIndex)
        self.assertEqual(relCollMgr._relationshipCollections, [])

    #
    # public API
    #
    def test_clear_nothingToDo(self):
        relCollMgr = RelationshipCollectionManager()
        with mock.patch.object(relCollMgr, "_dropCollection") as mock_dropCollection:
            with mock.patch.object(relCollMgr, "_setActiveTo") as mock_setActiveTo:
                relCollMgr.clear()
        mock_dropCollection.assert_not_called()
        mock_setActiveTo.assert_not_called()

    def test_clear_doesWork(self):
        relCollMgr = RelationshipCollectionManager()
        relCollMgr._relationshipCollections = ["dude"]
        with mock.patch.object(relCollMgr, "_dropCollection") as mock_dropCollection:
            with mock.patch.object(relCollMgr, "_setActiveTo") as mock_setActiveTo:
                relCollMgr.clear()
        mock_dropCollection.assert_called_once_with("dude")
        mock_setActiveTo.assert_called_once_with(None)

    def test_hasActiveCollection(self):
        relCollMgr = RelationshipCollectionManager()
        with mock.patch.object(relCollMgr, "getActiveCollection", return_value=None):
            self.assertFalse(relCollMgr.hasActiveCollection())
        with mock.patch.object(relCollMgr, "getActiveCollection", return_value="yup"):
            self.assertTrue(relCollMgr.hasActiveCollection())

    def test_getActiveCollection(self):
        relCollMgr = RelationshipCollectionManager()
        self.assertIsNone(relCollMgr.getActiveCollection())
        relCollMgr._relationshipCollections = ["foo", "bar", "baz"]
        relCollMgr._activeIndex = 1
        self.assertEqual(relCollMgr.getActiveCollection(), "bar")

    def test_addNew(self):
        relCollMgr = RelationshipCollectionManager()
        relColl = MockRelationshipCollection()
        self.assertIsNone(relColl.parent())
        with mock.patch.object(
            relCollMgr, "_dropCollectionsAfterCurrent"
        ) as mock_dropCollectionsAfterCurrent:
            with mock.patch.object(
                relCollMgr, "_connectToCollection"
            ) as mock_connectToCollection:
                with mock.patch.object(
                    relCollMgr, "_setActiveToLast"
                ) as mock_setActiveToLast:
                    relCollMgr.addNew(relColl)

        self.assertEqual(relColl.parent(), relCollMgr)
        self.assertEqual(relCollMgr._relationshipCollections, [relColl])
        mock_dropCollectionsAfterCurrent.assert_called_once_with()
        mock_connectToCollection.assert_called_once_with(relColl)
        mock_setActiveToLast.assert_called_once_with()

    def test_addNewFor(self):
        relCollMgr = RelationshipCollectionManager()
        with mock.patch(
            "relview.data.RelationshipCollectionManager.RelationshipCollection",
            new=MockRelationshipCollection,
        ):
            with mock.patch.object(relCollMgr, "addNew") as mock_addNew:
                relCollMgr.addNewFor("daStage", "daPrimPaths")
        self.assertEqual(len(mock_addNew.call_args_list), 1)
        args, kwargs = mock_addNew.call_args_list[0]
        self.assertEqual(kwargs, {})
        self.assertEqual(len(args), 1)
        relCollObj = args[0]
        self.assertEqual(relCollObj.__class__, MockRelationshipCollection)
        self.assertEqual(relCollObj.parent(), relCollMgr)
        self.assertEqual(relCollObj._primPaths, "daPrimPaths")
        self.assertEqual(relCollObj._stage, "daStage")

    def test_canAddTheseToActiveCollection_noActiveColl(self):
        relCollMgr = RelationshipCollectionManager()
        primPaths = ["prim1", "prim2"]
        self.assertFalse(relCollMgr.canAddTheseToActiveCollection(primPaths, None))
        self.assertTrue(
            relCollMgr.canAddTheseToActiveCollection(primPaths, "someStage")
        )

    def test_canAddTheseToActiveCollection_differentStage(self):
        relCollMgr = RelationshipCollectionManager()
        primPaths = ["prim1", "prim2"]
        activeColl = MockRelationshipCollection(
            stage="relCollStage", primPaths=primPaths, parent=relCollMgr
        )
        with mock.patch.object(
            relCollMgr, "getActiveCollection", return_value=activeColl
        ):
            self.assertFalse(
                relCollMgr.canAddTheseToActiveCollection(primPaths, "newStage")
            )

    def test_canAddTheseToActiveCollection_noNewPaths(self):
        relCollMgr = RelationshipCollectionManager()
        primPaths = ["prim1", "prim2"]
        activeColl = MockRelationshipCollection(
            stage="relCollStage", primPaths=primPaths, parent=relCollMgr
        )
        with mock.patch.object(
            relCollMgr, "getActiveCollection", return_value=activeColl
        ):
            self.assertFalse(
                relCollMgr.canAddTheseToActiveCollection(primPaths, "relCollStage")
            )

    def test_canAddTheseToActiveCollection_yes(self):
        relCollMgr = RelationshipCollectionManager()
        primPaths = ["prim1", "prim2"]
        activeColl = MockRelationshipCollection(
            stage="relCollStage", primPaths=primPaths, parent=relCollMgr
        )
        with mock.patch.object(
            relCollMgr, "getActiveCollection", return_value=activeColl
        ):
            self.assertTrue(
                relCollMgr.canAddTheseToActiveCollection(
                    ["prim1", "prim3"], "relCollStage"
                )
            )

    def test_addToActiveCollection_cannotAdd(self):
        relCollMgr = RelationshipCollectionManager()
        primPaths = ["prim1", "prim2"]
        stage = "relCollStage"
        activeColl = MockRelationshipCollection(
            stage=stage, primPaths=primPaths, parent=relCollMgr
        )
        with mock.patch.object(
            relCollMgr, "canAddTheseToActiveCollection", return_value=False
        ) as mock_canAddTheseToActiveCollection:
            with mock.patch.object(
                relCollMgr, "getActiveCollection", return_value=activeColl
            ) as mock_getActiveCollection:
                with mock.patch.object(relCollMgr, "addNewFor") as mock_addNewFor:
                    with mock.patch.object(
                        activeColl, "addPrimPaths"
                    ) as mock_addPrimPaths:
                        with self.assertRaises(AssertionError) as cm:
                            relCollMgr.addToActiveCollection(primPaths, stage)

        mock_canAddTheseToActiveCollection.assert_called_once_with(
            primPaths, "relCollStage"
        )
        mock_getActiveCollection.assert_not_called()
        mock_addNewFor.assert_not_called()
        mock_addPrimPaths.assert_not_called()

    def test_addToActiveCollection_addsToExisting(self):
        relCollMgr = RelationshipCollectionManager()
        primPaths = ["prim1", "prim2"]
        stage = "relCollStage"
        activeColl = MockRelationshipCollection(
            stage=stage, primPaths=primPaths, parent=relCollMgr
        )
        with mock.patch.object(
            relCollMgr, "canAddTheseToActiveCollection", return_value=True
        ) as mock_canAddTheseToActiveCollection:
            with mock.patch.object(
                relCollMgr, "getActiveCollection", return_value=activeColl
            ) as mock_getActiveCollection:
                with mock.patch.object(relCollMgr, "addNewFor") as mock_addNewFor:
                    with mock.patch.object(
                        activeColl, "addPrimPaths"
                    ) as mock_addPrimPaths:
                        relCollMgr.addToActiveCollection(primPaths, stage)

        mock_canAddTheseToActiveCollection.assert_called_once_with(
            primPaths, "relCollStage"
        )
        mock_getActiveCollection.assert_called_once_with()
        mock_addPrimPaths.assert_called_once_with(primPaths)
        mock_addNewFor.assert_not_called()

    def test_addToActiveCollection_calls_addNewFor(self):
        relCollMgr = RelationshipCollectionManager()
        primPaths = ["prim1", "prim2"]
        stage = "relCollStage"
        activeColl = MockRelationshipCollection(
            stage=stage, primPaths=primPaths, parent=relCollMgr
        )
        with mock.patch.object(
            relCollMgr, "canAddTheseToActiveCollection", return_value=True
        ) as mock_canAddTheseToActiveCollection:
            with mock.patch.object(
                relCollMgr, "getActiveCollection", return_value=None
            ) as mock_getActiveCollection:
                with mock.patch.object(relCollMgr, "addNewFor") as mock_addNewFor:
                    with mock.patch.object(
                        activeColl, "addPrimPaths"
                    ) as mock_addPrimPaths:
                        relCollMgr.addToActiveCollection(primPaths, stage)

        mock_canAddTheseToActiveCollection.assert_called_once_with(
            primPaths, "relCollStage"
        )
        mock_getActiveCollection.assert_called_once_with()
        mock_addPrimPaths.assert_not_called()
        mock_addNewFor.assert_called_once_with(stage, primPaths)

    def test_canGoBack(self):
        relCollMgr = RelationshipCollectionManager()
        for activeIdxVal, expectedResult in [
            (None, False),
            (0, False),
            (1, True),
            (5, True),
        ]:
            relCollMgr._activeIndex = activeIdxVal
            self.assertEqual(relCollMgr.canGoBack(), expectedResult)

    def test_goBack_cannot(self):
        relCollMgr = RelationshipCollectionManager()
        with mock.patch.object(relCollMgr, "canGoBack", return_value=False):
            with self.assertRaises(AssertionError) as cm:
                relCollMgr.goBack()
        self.assertEqual(str(cm.exception), "Can't go back!")

    def test_goBack_ok(self):
        relCollMgr = RelationshipCollectionManager()
        relCollMgr._activeIndex = 5
        with mock.patch.object(relCollMgr, "canGoBack", return_value=True):
            with mock.patch.object(relCollMgr, "_setActiveTo") as mock_setActiveTo:
                relCollMgr.goBack()
        mock_setActiveTo.assert_called_once_with(4)

    def test_canGoForward(self):
        relCollMgr = RelationshipCollectionManager()
        for activeIdxVal, relColls, expectedResult in [
            (None, [], False),
            (0, [], False),
            (0, ["thing1"], False),
            (0, ["thing1", "thing2"], True),
            (1, [], False),
            (1, ["thing1"], False),
            (1, ["thing1", "thing2"], False),
            (1, ["thing1", "thing2", "thing3"], True),
        ]:
            relCollMgr._activeIndex = activeIdxVal
            relCollMgr._relationshipCollections = relColls
            self.assertEqual(relCollMgr.canGoForward(), expectedResult)

    def test_goForward_cannot(self):
        relCollMgr = RelationshipCollectionManager()
        with mock.patch.object(relCollMgr, "canGoForward", return_value=False):
            with self.assertRaises(AssertionError) as cm:
                relCollMgr.goForward()
        self.assertEqual(str(cm.exception), "Can't go forward!")

    def test_goForward_ok(self):
        relCollMgr = RelationshipCollectionManager()
        relCollMgr._activeIndex = 2
        with mock.patch.object(relCollMgr, "canGoForward", return_value=True):
            with mock.patch.object(relCollMgr, "_setActiveTo") as mock_setActiveTo:
                relCollMgr.goForward()
        mock_setActiveTo.assert_called_once_with(3)

    #
    # slots
    #
    def test__relCollFilteringOptionsChangedSLOT(self):
        relCollMgr = RelationshipCollectionManager()
        with mock.patch(
            "relview.data.RelationshipCollectionManager.RelationshipFilteringOptions.getInstance",
            return_value="nooice",
        ):
            with mock.patch(
                "relview.data.RelationshipCollectionManager.updateFilteringOptionsFromOther"
            ) as mock_updateFilteringOptionsFromOther:
                relCollMgr._relCollFilteringOptionsChangedSLOT("daFilteringOptions")
        mock_updateFilteringOptionsFromOther.assert_called_once_with(
            "nooice", "daFilteringOptions"
        )

    def test__setActiveToLast_None(self):
        relCollMgr = RelationshipCollectionManager()
        with mock.patch.object(relCollMgr, "_setActiveTo") as mock_setActiveTo:
            relCollMgr._setActiveToLast()
        mock_setActiveTo.assert_called_once_with(None)

    def test__setActiveToLast_ok(self):
        relCollMgr = RelationshipCollectionManager()
        relCollMgr._relationshipCollections = [1, 2, 3]
        with mock.patch.object(relCollMgr, "_setActiveTo") as mock_setActiveTo:
            relCollMgr._setActiveToLast()
        mock_setActiveTo.assert_called_once_with(2)

    def test__setActiveTo(self):
        relCollMgr = RelationshipCollectionManager()
        signalReceiver = SignalReceiver()
        relCollMgr.ActiveChanged.connect(signalReceiver.theSlot)
        relCollMgr._setActiveTo(5)
        self.assertEqual(relCollMgr._activeIndex, 5)
        self.assertEqual(signalReceiver.getSignalData(), [tuple()])

    def test__connectToCollection_disconnectFromCollection(self):
        relCollMgr = RelationshipCollectionManager()
        relColl = MockRelationshipCollection(parent=relCollMgr)
        # connect and emit
        relCollMgr._connectToCollection(relColl)
        with mock.patch(
            "relview.data.RelationshipCollectionManager.RelationshipFilteringOptions.getInstance",
            return_value="nooice",
        ):
            with mock.patch(
                "relview.data.RelationshipCollectionManager.updateFilteringOptionsFromOther"
            ) as mock_updateFilteringOptionsFromOther:
                relColl.FilteringOptionsChanged.emit("daFilteringOptions")
        mock_updateFilteringOptionsFromOther.assert_called_once_with(
            "nooice", "daFilteringOptions"
        )

        # disconnect and emit again
        relCollMgr._disconnectFromCollection(relColl)
        with mock.patch(
            "relview.data.RelationshipCollectionManager.RelationshipFilteringOptions.getInstance",
            return_value="nooice",
        ):
            with mock.patch(
                "relview.data.RelationshipCollectionManager.updateFilteringOptionsFromOther"
            ) as mock_updateFilteringOptionsFromOther:
                relColl.FilteringOptionsChanged.emit("daFilteringOptions")
        mock_updateFilteringOptionsFromOther.assert_not_called()

    def test__dropCollectionsAfterCurrent_nothingToDo(self):
        relCollMgr = RelationshipCollectionManager()
        with mock.patch.object(relCollMgr, "canGoForward", return_value=False):
            with mock.patch.object(
                relCollMgr, "_dropCollection"
            ) as mock_dropCollection:
                relCollMgr._dropCollectionsAfterCurrent()
        mock_dropCollection.assert_not_called()

    def test__dropCollectionsAfterCurrent_drops(self):
        relCollMgr = RelationshipCollectionManager()
        relCollMgr._relationshipCollections = ["dude", "sweet"]
        relCollMgr._activeIndex = 0
        with mock.patch.object(relCollMgr, "canGoForward", return_value=True):
            with mock.patch.object(
                relCollMgr, "_dropCollection"
            ) as mock_dropCollection:
                relCollMgr._dropCollectionsAfterCurrent()
        mock_dropCollection.assert_called_once_with("sweet")

    def test__dropCollection_invalid(self):
        relCollMgr = RelationshipCollectionManager()
        relCollMgr._relationshipCollections = [1, 2, 3]
        with self.assertRaises(AssertionError) as cm:
            relCollMgr._dropCollection("four")
        self.assertEqual(str(cm.exception), "Invalid collection!")

    def test__dropCollection_ok(self):
        relCollMgr = RelationshipCollectionManager()
        relColl = MockRelationshipCollection(parent=relCollMgr)
        relCollMgr._relationshipCollections = ["dude", relColl]
        with mock.patch.object(
            relCollMgr, "_disconnectFromCollection"
        ) as mock_disconnectFromCollection:
            relCollMgr._dropCollection(relColl)
        mock_disconnectFromCollection.assert_called_once_with(relColl)
        self.assertEqual(relColl.parent(), None)
        self.assertEqual(relCollMgr._relationshipCollections, ["dude"])


#
# some mocks
#
class MockRelationshipCollection(QtCore.QObject):
    FilteringOptionsChanged = QtCore.Signal(object)

    def __init__(self, stage=None, primPaths=None, parent=None):
        super().__init__(parent)
        self._stage = stage
        self._primPaths = primPaths

    def getStage(self):
        return self._stage

    def getPrimPaths(self):
        return self._primPaths

    def addPrimPaths(self):
        pass  # here for mocking
