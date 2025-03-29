from collections import OrderedDict
from unittest import mock, TestCase

from relview.data.RelationshipFiltering import (
    RelationshipFilteringOptions,
    RelationshipFilter,
)

from .utilsForTesting import SignalReceiver


class RelationshipFilteringOptions_TestCase(TestCase):
    """Tests the RelationshipFilteringOptions class."""

    def setUp(self):
        self._clearOut()

    def tearDown(self):
        self._clearOut()

    def _clearOut(self):
        RelationshipFilteringOptions.FILTER_CLASSES_BY_CATEGORY_NAME = OrderedDict()
        RelationshipFilteringOptions._INSTANCE = None

    def test_classData(self):
        self.assertEqual(
            RelationshipFilteringOptions.FILTER_CLASSES_BY_CATEGORY_NAME, {}
        )
        self.assertIsNone(RelationshipFilteringOptions._INSTANCE)
        self.assertTrue(RelationshipFilteringOptions._includeTargetRels)
        self.assertTrue(RelationshipFilteringOptions._includeIncomingRels)
        self.assertTrue(RelationshipFilteringOptions._includePrimRels)
        self.assertTrue(RelationshipFilteringOptions._includePropertyRels)

    def test_registerFilterClass(self):
        class TestFilterClass(object):
            @classmethod
            def getCategoryName(cls):
                return "Some Test Category"

        RelationshipFilteringOptions.registerFilterClass(TestFilterClass)
        self.assertEqual(
            RelationshipFilteringOptions.FILTER_CLASSES_BY_CATEGORY_NAME,
            {"Some Test Category": TestFilterClass},
        )

    def test_getInstance(self):
        inst = RelationshipFilteringOptions.getInstance()
        self.assertEqual(inst.__class__, RelationshipFilteringOptions)
        self.assertEqual(inst, RelationshipFilteringOptions._INSTANCE)
        RelationshipFilteringOptions._INSTANCE = "Steve"
        self.assertEqual(RelationshipFilteringOptions.getInstance(), "Steve")

    def test_init(self):
        filterOpts = RelationshipFilteringOptions()
        self.assertEqual(filterOpts._filtersByCategory, {})

        class TestFilterClass(object):
            @classmethod
            def getCategoryName(cls):
                return "Some Test Category"

        RelationshipFilteringOptions.registerFilterClass(TestFilterClass)
        filterOpts = RelationshipFilteringOptions()
        self.assertEqual(filterOpts._filtersByCategory, {"Some Test Category": set()})

    #
    # public API
    #
    def test_getNumFilterExclusions(self):
        filterOpts = RelationshipFilteringOptions()
        self.assertEqual(filterOpts.getNumFilterExclusions(), 0)
        filterOpts._includeTargetRels = False
        filterOpts._includeIncomingRels = False
        filterOpts._includePrimRels = False
        filterOpts._includePropertyRels = False
        self.assertEqual(filterOpts.getNumFilterExclusions(), 4)

        class MockFilter(object):
            def isActive(self):
                return None

        filter1 = MockFilter()
        filter2 = MockFilter()
        with mock.patch.object(filter1, "isActive", return_value=False):
            with mock.patch.object(filter2, "isActive", return_value=True):
                with mock.patch.object(
                    filterOpts, "getAllFilters", return_value=[filter1, filter2]
                ):
                    self.assertEqual(filterOpts.getNumFilterExclusions(), 5)

    def test_FollowTargetRelationships_get_set(self):
        self._test_core_getters_setters(
            getterMethodName="shouldFollowTargetRelationships",
            setterMethodName="followTargetRelationships",
            setterSignalEmitted="FollowTargetRelationshipsChangedTo",
        )

    def test_FollowIncomingRelationships_get_set(self):
        self._test_core_getters_setters(
            getterMethodName="shouldFollowIncomingRelationships",
            setterMethodName="followIncomingRelationships",
            setterSignalEmitted="FollowIncomingRelationshipsChangedTo",
        )

    def test_IncludePrimRelationships_get_set(self):
        self._test_core_getters_setters(
            getterMethodName="shouldIncludePrimRelationships",
            setterMethodName="includePrimRelationships",
            setterSignalEmitted="IncludePrimRelationshipsChangedTo",
        )

    def test_IncludePropertyRelationships_get_set(self):
        self._test_core_getters_setters(
            getterMethodName="shouldIncludePropertyRelationships",
            setterMethodName="includePropertyRelationships",
            setterSignalEmitted="IncludePropertyRelationshipsChangedTo",
        )

    def _test_core_getters_setters(
        self,
        getterMethodName,
        setterMethodName,
        setterSignalEmitted,
        expectedInitialVal=True,
    ):
        filterOpts = RelationshipFilteringOptions()
        getMethod = getattr(filterOpts, getterMethodName)
        setMethod = getattr(filterOpts, setterMethodName)
        signal = getattr(filterOpts, setterSignalEmitted)
        initialValue = getMethod()
        self.assertEqual(initialValue, expectedInitialVal)
        signalReceiver = SignalReceiver()
        signal.connect(signalReceiver.theSlot)
        # set to same value - shouldn't emit a signal
        setMethod(initialValue)
        self.assertFalse(signalReceiver.hasReceivedAnySignals())
        # set to different value - should emit signal
        setMethod(not initialValue)
        newValue = getMethod()
        self.assertTrue(signalReceiver.hasReceivedAnySignals())
        self.assertEqual(signalReceiver.getNumSignalsReceived(), 1)
        self.assertEqual(signalReceiver.getSignalData(), [(newValue,)])
        self.assertEqual(getMethod(), not initialValue)

    #
    # individual filtering
    #
    def test_registerFilter(self):
        class TestFilter(RelationshipFilter):
            @classmethod
            def getCategoryName(cls):
                return "Test Category"

        testFilterObj = TestFilter("A test filter")
        filterOpts = RelationshipFilteringOptions()
        signalReceiver = SignalReceiver()
        filterOpts.FilterRegistered.connect(signalReceiver.theSlot)
        filterOpts.registerFilter(testFilterObj)
        self.assertEqual(
            filterOpts._filtersByCategory, {"Test Category": set([testFilterObj])}
        )
        self.assertEqual(testFilterObj.parent(), filterOpts)
        self.assertEqual(signalReceiver.getNumSignalsReceived(), 1)
        self.assertEqual(signalReceiver.getSignalData(), [(testFilterObj,)])

    def test_clearFilters(self):
        class TestFilter(RelationshipFilter):
            @classmethod
            def getCategoryName(cls):
                return "Test Category"

        testFilterObj = TestFilter("A test filter")
        filterOpts = RelationshipFilteringOptions()
        filterOpts.registerFilter(testFilterObj)
        self.assertEqual(
            filterOpts._filtersByCategory, {"Test Category": set([testFilterObj])}
        )
        filterOpts.clearFilters()
        self.assertIsNone(testFilterObj.parent())
        self.assertEqual(filterOpts._filtersByCategory, {"Test Category": set()})

    def test_getFilterCategoryNames(self):
        filterOpts = RelationshipFilteringOptions()
        self.assertEqual(filterOpts.getFilterCategoryNames(), [])
        filterOpts._filtersByCategory["Some category"] = set()
        filterOpts._filtersByCategory["Another category"] = set()
        self.assertEqual(
            filterOpts.getFilterCategoryNames(), ["Some category", "Another category"]
        )

    def test_getFiltersInCategory(self):
        class Test1Filter(RelationshipFilter):
            @classmethod
            def getCategoryName(cls):
                return "Test1 Category"

        class Test2Filter(RelationshipFilter):
            @classmethod
            def getCategoryName(cls):
                return "Test2 Category"

        filter1 = Test1Filter("Cool test filter1")
        filter2 = Test1Filter("Another test filter1")
        filter3 = Test2Filter("Test filter2")

        filterOpts = RelationshipFilteringOptions()
        for filterObj in [filter1, filter2, filter3]:
            filterOpts.registerFilter(filterObj)

        self.assertEqual(
            filterOpts.getFiltersInCategory("Test1 Category"), [filter2, filter1]
        )
        self.assertEqual(filterOpts.getFiltersInCategory("Test2 Category"), [filter3])
        self.assertEqual(filterOpts.getFiltersInCategory("asdasdas"), [])

    def test_getFilterInCategoryNamed(self):
        class Test1Filter(RelationshipFilter):
            @classmethod
            def getCategoryName(cls):
                return "Test1 Category"

        class Test2Filter(RelationshipFilter):
            @classmethod
            def getCategoryName(cls):
                return "Test2 Category"

        filter1 = Test1Filter("Cool test filter1")
        filter2 = Test1Filter("Another test filter1")
        filter3 = Test2Filter("Test filter2")

        filterOpts = RelationshipFilteringOptions()
        for filterObj in [filter1, filter2, filter3]:
            filterOpts.registerFilter(filterObj)

        self.assertIsNone(
            filterOpts.getFilterInCategoryNamed("Test1 Category", "asdfasdf")
        )
        self.assertIsNone(
            filterOpts.getFilterInCategoryNamed("sdfgsdfg", "Another test filter1")
        )
        self.assertIsNone(filterOpts.getFilterInCategoryNamed("dfhdfgh", "ghjkghjk"))

        self.assertEqual(
            filterOpts.getFilterInCategoryNamed(
                "Test1 Category", "Another test filter1"
            ),
            filter2,
        )

    def test_getAllFilters(self):
        class Test1Filter(RelationshipFilter):
            @classmethod
            def getCategoryName(cls):
                return "Test1 Category"

        class Test2Filter(RelationshipFilter):
            @classmethod
            def getCategoryName(cls):
                return "Test2 Category"

        filter1 = Test1Filter("Cool test filter1")
        filter2 = Test1Filter("Another test filter1")
        filter3 = Test2Filter("Test filter2")

        filterOpts = RelationshipFilteringOptions()
        allFilters = [filter1, filter2, filter3]
        for filterObj in allFilters:
            filterOpts.registerFilter(filterObj)

        self.assertEqual(set(filterOpts.getAllFilters()), set(allFilters))

    #
    # Methods which consider each registered RelationshipFilter instance with
    # the provided data.
    #
    def test_shouldFollowRelationshipsOf(self):
        filterOpts = RelationshipFilteringOptions()
        with mock.patch.object(
            filterOpts, "_visitFiltersWith", return_value="visited!"
        ) as mock_visitFiltersWith:
            self.assertEqual(
                filterOpts.shouldFollowRelationshipsOf("daPrim"), "visited!"
            )
        mock_visitFiltersWith.assert_called_once_with(
            filterOpts._shouldFollowRelationshipsOfFunc, "daPrim"
        )

    def test_shouldFollowRelationship(self):
        filterOpts = RelationshipFilteringOptions()
        with mock.patch.object(
            filterOpts, "_visitFiltersWith", return_value="visited!"
        ) as mock_visitFiltersWith:
            self.assertEqual(
                filterOpts.shouldFollowRelationship("daPrim", "daRelationship"),
                "visited!",
            )
        mock_visitFiltersWith.assert_called_once_with(
            filterOpts._shouldFollowRelationshipFunc, "daPrim", "daRelationship"
        )

    def test_shouldFollowRelationshipTarget(self):
        filterOpts = RelationshipFilteringOptions()
        with mock.patch.object(
            filterOpts, "_visitFiltersWith", return_value="visited!"
        ) as mock_visitFiltersWith:
            self.assertEqual(
                filterOpts.shouldFollowRelationshipTarget(
                    "daPrim", "daRelationship", "daTarget"
                ),
                "visited!",
            )
        mock_visitFiltersWith.assert_called_once_with(
            filterOpts._shouldFollowRelationshipTargetFunc,
            "daPrim",
            "daRelationship",
            "daTarget",
        )

    #
    # cloning
    #
    def test_clone(self):
        filterOpts = RelationshipFilteringOptions()
        with mock.patch.object(filterOpts, "toDict", return_value="daDict"):
            with mock.patch.object(
                filterOpts, "createFromDict", return_value="theClone"
            ) as mock_createFromDict:
                self.assertEqual(filterOpts.clone("daParent"), "theClone")
        mock_createFromDict.assert_called_once_with("daDict", "daParent")

    #
    # serialization/deserialization stuff
    #
    def test_createFromDict(self):
        with mock.patch(
            "relview.data.RelationshipFiltering.RelationshipFilteringOptions.initFromDict"
        ) as mock_initFromDict:
            filterOpts = RelationshipFilteringOptions.createFromDict("daDataDict")
            self.assertEqual(filterOpts.__class__, RelationshipFilteringOptions)
        mock_initFromDict.assert_called_once_with("daDataDict", emitSignals=False)

    def test_initFromDict(self):
        class Test1Filter(RelationshipFilter):
            @classmethod
            def getCategoryName(cls):
                return "Test1 Category"

        class Test2Filter(RelationshipFilter):
            @classmethod
            def getCategoryName(cls):
                return "Test2 Category"

        filterOpts = RelationshipFilteringOptions()
        filter1 = Test1Filter("Filter1")
        filter2 = Test2Filter("Filter2")
        filterOpts.registerFilter(filter1)
        filterOpts.registerFilter(filter2)

        self.assertTrue(filterOpts.shouldFollowTargetRelationships())
        self.assertTrue(filterOpts.shouldFollowIncomingRelationships())
        self.assertTrue(filterOpts.shouldIncludePrimRelationships())
        self.assertTrue(filterOpts.shouldIncludePropertyRelationships())

        self.assertEqual(filterOpts.getAllFilters(), [filter1, filter2])

        dataDict = dict(
            follow_target_rels=False,
            follow_incoming_rels=False,
            include_prim_rels=False,
            include_property_rels=False,
            filters={
                "Test1 Category": [
                    dict(
                        is_active=False,
                        name="Filter1",
                    )
                ],
                "Unknown Category": [],
            },
        )
        filterOpts.initFromDict(dataDict)

        self.assertFalse(filterOpts.shouldFollowTargetRelationships())
        self.assertFalse(filterOpts.shouldFollowIncomingRelationships())
        self.assertFalse(filterOpts.shouldIncludePrimRelationships())
        self.assertFalse(filterOpts.shouldIncludePropertyRelationships())
        allFilters = filterOpts.getAllFilters()
        self.assertEqual(len(allFilters), 1)
        filter = allFilters[0]
        self.assertFalse(filter.isActive())
        self.assertEqual(filter.getName(), "Filter1")
        self.assertEqual(filter.__class__, Test1Filter)

    def test_toDict(self):
        class Test2Filter(RelationshipFilter):
            @classmethod
            def getCategoryName(cls):
                return "Test2 Category"

        filterOpts = RelationshipFilteringOptions()
        filter2 = Test2Filter("Filter2")
        filterOpts.registerFilter(filter2)
        filterOpts.followIncomingRelationships(False)
        filterOpts.includePropertyRelationships(False)
        filter2.setActive(False)
        filter2.setDescription("A kickass filter")

        actualDataDict = filterOpts.toDict()
        expectedDataDict = dict(
            follow_target_rels=True,
            follow_incoming_rels=False,
            include_prim_rels=True,
            include_property_rels=False,
            filters={
                "Test2 Category": [
                    dict(
                        is_active=False,
                        name="Filter2",
                        description="A kickass filter",
                    )
                ]
            },
        )
        self.assertEqual(actualDataDict, expectedDataDict)

    #
    # slots
    #
    def test__filterActiveChangedToSLOT(self):
        filterOpts = RelationshipFilteringOptions()
        signalReceiver = SignalReceiver()
        filterOpts.FilterActivationChanged.connect(signalReceiver.theSlot)
        randomObj = object()
        with mock.patch.object(filterOpts, "sender", return_value=randomObj):
            filterOpts._filterActiveChangedToSLOT(True)
        self.assertEqual(signalReceiver.getSignalData(), [(randomObj, True)])

    def test__genericEmittingChangedSLOT(self):
        def _mockSingleShot(numMilliseconds, funcToCall):
            # just making this synchronous for testing purposes
            funcToCall()

        filterOpts = RelationshipFilteringOptions()
        signalReceiver = SignalReceiver()
        filterOpts.Changed.connect(signalReceiver.theSlot)
        with mock.patch(
            "relview.data.decorators.QtCore.QTimer.singleShot",
            side_effect=_mockSingleShot,
        ):
            filterOpts._genericEmittingChangedSLOT("asdasd")
        self.assertEqual(signalReceiver.getSignalData(), [tuple()])

    #
    # private helper methods
    #
    def test__visitFiltersWith(self):
        class MockFilter(object):
            def __init__(self, name, returnVal):
                self._name = name
                self._returnVal = returnVal

            def getName(self):
                return self._name

            def getReturnVal(self):
                return self._returnVal

        callData = []

        def perFilterCallback(filterObj, *args):
            callData.append(dict(filter_name=filterObj.getName(), args=args))
            return filterObj.getReturnVal()

        filterOpts = RelationshipFilteringOptions()
        filter1 = MockFilter("filter1", None)
        filterOpts._filtersByCategory["cat1"].add(filter1)
        self.assertTrue(filterOpts._visitFiltersWith(perFilterCallback, "nooice"))
        self.assertEqual(callData, [dict(filter_name="filter1", args=("nooice",))])

        callData = []

        filter2 = MockFilter("filter2", False)
        filterOpts._filtersByCategory["cat2"].add(filter2)
        self.assertFalse(filterOpts._visitFiltersWith(perFilterCallback, "sweet"))
        self.assertEqual(
            callData,
            [
                dict(filter_name="filter1", args=("sweet",)),
                dict(filter_name="filter2", args=("sweet",)),
            ],
        )

    def test__shouldFollowRelationshipsOfFunc(self):
        class MockFilter(object):
            def shouldFollowRelationshipsOf(self, prim):
                pass

        filterOpts = RelationshipFilteringOptions()
        filterObj = MockFilter()
        with mock.patch.object(
            filterObj, "shouldFollowRelationshipsOf", return_value="sure"
        ) as mock_shouldFollowRelationshipsOf:
            self.assertEqual(
                filterOpts._shouldFollowRelationshipsOfFunc(filterObj, "daPrim"), "sure"
            )
        mock_shouldFollowRelationshipsOf.assert_called_once_with("daPrim")

    def test__shouldFollowRelationshipFunc(self):
        class MockFilter(object):
            def shouldFollowRelationship(self, prim, relationship):
                pass

        filterOpts = RelationshipFilteringOptions()
        filterObj = MockFilter()
        with mock.patch.object(
            filterObj, "shouldFollowRelationship", return_value="sure"
        ) as mock_shouldFollowRelationship:
            self.assertEqual(
                filterOpts._shouldFollowRelationshipFunc(filterObj, "daPrim", "daRel"),
                "sure",
            )
        mock_shouldFollowRelationship.assert_called_once_with("daPrim", "daRel")

    def test__shouldFollowRelationshipTargetFunc(self):
        class MockFilter(object):
            def shouldFollowRelationshipTarget(self, prim, relationship, targetPath):
                pass

        filterOpts = RelationshipFilteringOptions()
        filterObj = MockFilter()
        with mock.patch.object(
            filterObj, "shouldFollowRelationshipTarget", return_value="sure"
        ) as mock_shouldFollowRelationshipTarget:
            self.assertEqual(
                filterOpts._shouldFollowRelationshipTargetFunc(
                    filterObj, "daPrim", "daRel", "daPath"
                ),
                "sure",
            )
        mock_shouldFollowRelationshipTarget.assert_called_once_with(
            "daPrim", "daRel", "daPath"
        )


class RelationshipFilter_TestCase(TestCase):
    """Tests the RelationshipFilter class."""

    def test_classData(self):
        self.assertTrue(RelationshipFilter._isActive)
        self.assertEqual(RelationshipFilter._name, "")
        self.assertEqual(RelationshipFilter._description, "")

    def test_init(self):
        filterObj = RelationshipFilter("Kickass filter")
        self.assertEqual(filterObj._name, "Kickass filter")

    #
    # public API
    #
    def test_getCategoryName(self):
        filterObj = RelationshipFilter("Nice filter")
        with self.assertRaises(NotImplementedError) as cm:
            filterObj.getCategoryName()
        self.assertEqual(str(cm.exception), "getCategoryName() must be implemented")

    def test_getName(self):
        filterObj = RelationshipFilter("Nice filter")
        self.assertEqual(filterObj.getName(), "Nice filter")

    def test_setName(self):
        filterObj = RelationshipFilter("Nice filter")
        signalReceiver = SignalReceiver()
        filterObj.NameChangedTo.connect(signalReceiver.theSlot)
        filterObj.setName("Nice filter")
        self.assertFalse(signalReceiver.hasReceivedAnySignals())
        filterObj.setName("Very nice filter")
        self.assertTrue(signalReceiver.hasReceivedAnySignals())
        self.assertEqual(signalReceiver.getSignalData(), [("Very nice filter",)])
        self.assertEqual(filterObj._name, "Very nice filter")

    def test_getDescription(self):
        filterObj = RelationshipFilter("Nice filter")
        self.assertEqual(filterObj.getDescription(), "")
        filterObj._description = "It's fine"
        self.assertEqual(filterObj.getDescription(), "It's fine")

    def test_setDescription(self):
        filterObj = RelationshipFilter("Nice filter")
        signalReceiver = SignalReceiver()
        filterObj.DescriptionChangedTo.connect(signalReceiver.theSlot)
        filterObj.setDescription("")
        self.assertFalse(signalReceiver.hasReceivedAnySignals())
        filterObj.setDescription("New description")
        self.assertTrue(signalReceiver.hasReceivedAnySignals())
        self.assertEqual(signalReceiver.getSignalData(), [("New description",)])
        self.assertEqual(filterObj._description, "New description")

    def test_isActive(self):
        filterObj = RelationshipFilter("Nice filter")
        self.assertTrue(filterObj.isActive())
        filterObj._isActive = False
        self.assertFalse(filterObj.isActive())

    def test_setActive(self):
        filterObj = RelationshipFilter("Nice filter")
        signalReceiver = SignalReceiver()
        filterObj.ActiveChangedTo.connect(signalReceiver.theSlot)
        filterObj.setActive(True)
        self.assertFalse(signalReceiver.hasReceivedAnySignals())
        filterObj.setActive(False)
        self.assertTrue(signalReceiver.hasReceivedAnySignals())
        self.assertEqual(signalReceiver.getSignalData(), [(False,)])
        self.assertEqual(filterObj._isActive, False)

    #
    # "should" methods
    #
    def test_shouldFollowRelationshipsOf(self):
        filterObj = RelationshipFilter("Nice filter")
        self.assertIsNone(filterObj.shouldFollowRelationshipsOf("asdasd"))

    def test_shouldFollowRelationship(self):
        filterObj = RelationshipFilter("Nice filter")
        self.assertIsNone(filterObj.shouldFollowRelationship("asdasd", "qwert"))

    def test_shouldFollowRelationshipTarget(self):
        filterObj = RelationshipFilter("Nice filter")
        self.assertIsNone(
            filterObj.shouldFollowRelationshipTarget("asdasd", "qwert", "ertyerty")
        )

    #
    # cloning
    #
    def test_clone(self):
        filterObj = RelationshipFilter("Nice filter")
        with mock.patch.object(filterObj, "toDict", return_value="daDict"):
            with mock.patch.object(
                filterObj, "createFromDict", return_value="daClone"
            ) as mock_createFromDict:
                self.assertEqual(filterObj.clone("daParent"), "daClone")
        mock_createFromDict.assert_called_once_with("daDict", "daParent")

    #
    # serialization/deserialization stuff
    #
    def test_createFromDict(self):
        with mock.patch(
            "relview.data.RelationshipFiltering.RelationshipFilter.getConstructorArgsFrom",
            return_value=("Nice filter", None),
        ) as mock_getConstructorArgsFrom:
            with mock.patch(
                "relview.data.RelationshipFiltering.RelationshipFilter.initFromDict"
            ) as mock_initFromDict:
                filterObj = RelationshipFilter.createFromDict("daDataDict")
        self.assertEqual(filterObj.getName(), "Nice filter")
        self.assertIsNone(filterObj.parent())
        mock_getConstructorArgsFrom.assert_called_once_with("daDataDict", None)
        mock_initFromDict.assert_called_once_with("daDataDict")

    def test_getConstructorArgsFrom(self):
        self.assertEqual(
            RelationshipFilter.getConstructorArgsFrom(
                dict(name="Steve"), "Steve's Dad"
            ),
            ("Steve", "Steve's Dad"),
        )

    def test_initFromDict(self):
        filterObj = RelationshipFilter("Nice filter")
        filterObj.initFromDict(
            dict(is_active=False, name="New name", description="New description")
        )
        self.assertEqual(filterObj._isActive, False)
        self.assertEqual(filterObj._name, "New name")
        self.assertEqual(filterObj._description, "New description")

    def test_toDict(self):
        filterObj = RelationshipFilter("Nice filter")
        filterObj.setActive(False)
        filterObj.setDescription("I filter things")
        filterObj.setName("Tommy")
        self.assertEqual(
            filterObj.toDict(),
            dict(is_active=False, name="Tommy", description="I filter things"),
        )
