from unittest import mock, TestCase

from pxr import Sdf

from relview.data import PrimRelationshipRecord
from relview.data.NamedRelationship import NamedRelationship


#
# test cases
#
class PrimRelationshipRecord_TestCase(TestCase):
    """Tests the PrimRelationshipRecord class."""

    def setUp(self):
        self._stage = MockStage()
        self._primPath = "/path/to/a/prim"
        self._relationshipCollection = MockRelationshipCollection()
        self._relRecord = PrimRelationshipRecord.PrimRelationshipRecord(
            self._stage, self._primPath, self._relationshipCollection
        )

    def test_init(self):
        self.assertEqual(self._relRecord._stage, self._stage)
        self.assertEqual(self._relRecord._primPath, self._primPath)
        self.assertEqual(
            self._relRecord._relationshipCollection, self._relationshipCollection
        )
        self.assertEqual(self._relRecord._toRelsByName, {})
        self.assertEqual(self._relRecord._fromRelsByName, {})
        self.assertEqual(self._relRecord._additionalRelsByName, {})

    #
    # general things
    #
    def test_getStage(self):
        self.assertEqual(self._relRecord.getStage(), self._stage)

    def test_getPrimPath(self):
        self.assertEqual(self._relRecord.getPrimPath(), self._primPath)

    def test_getPrim(self):
        with mock.patch.object(self._stage, "GetPrimAtPath", return_value="daPrim"):
            self.assertEqual(self._relRecord.getPrim(), "daPrim")

    def test_hasRelationshipCollection(self):
        self.assertTrue(self._relRecord.hasRelationshipCollection())
        otherRelRecord = PrimRelationshipRecord.PrimRelationshipRecord(
            self._stage, self._primPath
        )
        self.assertIsNone(otherRelRecord._relationshipCollection)
        self.assertFalse(otherRelRecord.hasRelationshipCollection())

    def test_getRelationshipCollection(self):
        self.assertEqual(
            self._relRecord.getRelationshipCollection(), self._relationshipCollection
        )

    def test_hasAnyRelationships(self):
        self.assertFalse(self._relRecord.hasAnyRelationships())
        for toRels, fromRels, additionalRels, expectedVal in [
            (None, None, None, False),
            ("sdfsdfg", None, None, True),
            (None, "sdfsdfg", None, True),
            (None, None, "sdfsdfg", True),
            ("wertwert", "gfhjfghj", "sdfsdfg", True),
        ]:
            self._relRecord._toRelsByName = toRels
            self._relRecord._fromRelsByName = fromRels
            self._relRecord._additionalRelsByName = additionalRels
            self.assertEqual(self._relRecord.hasAnyRelationships(), expectedVal)

    #
    # "to" relationship stuff
    #
    def test_hasToRelationships(self):
        self.assertFalse(self._relRecord.hasToRelationships())
        self._relRecord._toRelsByName = "asdasdas"
        self.assertTrue(self._relRecord.hasToRelationships())

    def test_getToRelationshipNames(self):
        self.assertEqual(self._relRecord.getToRelationshipNames(), [])
        self._relRecord._toRelsByName["nooice"].append("adsfgadg")
        self.assertEqual(self._relRecord.getToRelationshipNames(), ["nooice"])

    def test_getToRelationshipsNamed(self):
        self.assertEqual(self._relRecord.getToRelationshipsNamed("nooice"), [])
        self._relRecord._toRelsByName["nooice"].append("adsfgadg")
        self.assertEqual(
            self._relRecord.getToRelationshipsNamed("nooice"), ["adsfgadg"]
        )

    def test_getToRelationships(self):
        self.assertEqual(self._relRecord.getToRelationships(), [])
        self._relRecord._toRelsByName["nooice"].append("adsfgadg")
        self._relRecord._toRelsByName["dude"].append("qwerty")
        self._relRecord._toRelsByName["dude"].append("asdf")
        self._relRecord._toRelsByName["sweet"].append("zxcv")
        self.assertEqual(
            set(self._relRecord.getToRelationships()),
            set(["adsfgadg", "qwerty", "asdf", "zxcv"]),
        )

    def test_getPrimsWithToRelationships(self):
        with mock.patch.object(
            self._relRecord, "getToRelationships", return_value="theToRelationships"
        ):
            with mock.patch(
                "relview.data.PrimRelationshipRecord._getUniquePrimPathsFromRelList",
                return_value="thePrimPaths",
            ) as mock_getUniquePrimPathsFromRelList:
                self.assertEqual(
                    self._relRecord.getPrimsWithToRelationships(False), "thePrimPaths"
                )
        self.assertEqual(
            mock_getUniquePrimPathsFromRelList.call_args_list,
            [[("theToRelationships", False)]],
        )

    def test_getNumPrimsWithToRelationships(self):
        with mock.patch.object(
            self._relRecord,
            "getPrimsWithToRelationships",
            return_value=[234, "dsfgsdfg", 5678, {}],
        ) as mock_getPrimsWithToRelationships:
            self.assertEqual(self._relRecord.getNumPrimsWithToRelationships(), 4)
        self.assertEqual(mock_getPrimsWithToRelationships.call_args_list, [[(True,)]])
        with mock.patch.object(
            self._relRecord,
            "getPrimsWithToRelationships",
            return_value=[234, "dsfgsdfg", 5678, {}],
        ) as mock_getPrimsWithToRelationships:
            self.assertEqual(self._relRecord.getNumPrimsWithToRelationships(False), 4)
        self.assertEqual(mock_getPrimsWithToRelationships.call_args_list, [[(False,)]])

    def test_addRelationshipTo_adds_new(self):
        self.assertEqual(self._relRecord._toRelsByName, {})
        primPath = Sdf.Path("/path/to/thing")
        with mock.patch(
            "relview.data.PrimRelationshipRecord._isRelInList", return_value=False
        ):
            self._relRecord.addRelationshipTo("someRelationship", primPath)
        self.assertEqual(len(self._relRecord._toRelsByName["someRelationship"]), 1)
        self.assertEqual(
            self._relRecord._toRelsByName["someRelationship"][0].getName(),
            "someRelationship",
        )
        self.assertEqual(
            self._relRecord._toRelsByName["someRelationship"][0].getPath(), primPath
        )

    def test_addRelationshipTo_already_present(self):
        self.assertEqual(self._relRecord._toRelsByName, {})
        primPath = Sdf.Path("/path/to/thing")
        with mock.patch(
            "relview.data.PrimRelationshipRecord._isRelInList", return_value=True
        ):
            self._relRecord.addRelationshipTo("someRelationship", primPath)
        self.assertEqual(len(self._relRecord._toRelsByName["someRelationship"]), 0)

    def test_addUntargetedToRelationships(self):
        with mock.patch.object(
            self._relRecord, "addRelationshipTo"
        ) as mock_addRelationshipTo:
            self._relRecord.addUntargetedToRelationships(["foo", "bar", "baz"])
        self.assertEqual(
            mock_addRelationshipTo.call_args_list,
            [
                [("foo", Sdf.Path())],
                [("bar", Sdf.Path())],
                [("baz", Sdf.Path())],
            ],
        )

    def test_hasRelationshipTo(self):
        namedRel1 = NamedRelationship("kickassRel", Sdf.Path("/path/to/thing"))
        namedRel2 = NamedRelationship("someOtherRel", Sdf.Path("/some/other/thing"))
        namedRels = [namedRel1, namedRel2]
        with mock.patch.object(
            self._relRecord, "getToRelationships", return_value=namedRels
        ):
            self.assertTrue(
                self._relRecord.hasRelationshipTo(Sdf.Path("/path/to/thing"))
            )
            self.assertTrue(
                self._relRecord.hasRelationshipTo(Sdf.Path("/some/other/thing"))
            )
            self.assertFalse(
                self._relRecord.hasRelationshipTo(Sdf.Path("/yet/another/thing"))
            )

    def test_hasAnyInvalidToRelationships_False(self):
        namedRel1 = NamedRelationship("kickassRel", Sdf.Path("/path/to/thing"))
        namedRel2 = NamedRelationship("someOtherRel", Sdf.Path("/some/other/thing"))
        namedRels = [namedRel1, namedRel2]
        with mock.patch.object(
            self._relRecord, "getToRelationships", return_value=namedRels
        ):
            self.assertFalse(self._relRecord.hasAnyInvalidToRelationships())

    def test_hasAnyInvalidToRelationships_True(self):
        namedRel1 = NamedRelationship("kickassRel", Sdf.Path("/path/to/thing"))
        namedRel2 = NamedRelationship(
            "someOtherRel",
            Sdf.Path("/some/other/thing"),
            messageIfInvalid="Nope, no good",
        )
        namedRels = [namedRel1, namedRel2]
        with mock.patch.object(
            self._relRecord, "getToRelationships", return_value=namedRels
        ):
            self.assertTrue(self._relRecord.hasAnyInvalidToRelationships())

    #
    # "from" relationship stuff
    #
    def test_hasFromRelationships(self):
        self.assertFalse(self._relRecord.hasFromRelationships())
        self._relRecord._fromRelsByName = "asdasd"
        self.assertTrue(self._relRecord.hasFromRelationships())

    def test_getFromRelationshipNames(self):
        self.assertEqual(self._relRecord.getFromRelationshipNames(), [])
        self._relRecord._fromRelsByName["dude"] = []
        self._relRecord._fromRelsByName["sweet"] = []
        self.assertEqual(self._relRecord.getFromRelationshipNames(), ["dude", "sweet"])

    def test_getFromRelationshipsNamed(self):
        self.assertEqual(self._relRecord.getFromRelationshipsNamed("someName"), [])
        self._relRecord._fromRelsByName["someName"] = ["thing", "thang"]
        self.assertEqual(
            self._relRecord.getFromRelationshipsNamed("someName"), ["thing", "thang"]
        )

    def test_getFromRelationships(self):
        self.assertEqual(self._relRecord.getFromRelationships(), [])
        self._relRecord._fromRelsByName["things"] = [1, 2, 3]
        self._relRecord._fromRelsByName["thangs"] = [4, 5, 6]
        self.assertEqual(
            set(self._relRecord.getFromRelationships()), set([1, 2, 3, 4, 5, 6])
        )

    def test_getPrimsWithFromRelationships(self):
        with mock.patch(
            "relview.data.PrimRelationshipRecord._getUniquePrimPathsFromRelList",
            return_value="daPrimPaths",
        ) as mock_getUniquePrimPathsFromRelList:
            with mock.patch.object(
                self._relRecord, "getFromRelationships", return_value="daFromRels"
            ) as mock_getFromRelationships:
                self.assertEqual(
                    self._relRecord.getPrimsWithFromRelationships(), "daPrimPaths"
                )
        mock_getFromRelationships.assert_called_once_with()
        mock_getUniquePrimPathsFromRelList.assert_called_once_with("daFromRels", True)

    def test_getNumPrimsWithFromRelationships(self):
        with mock.patch.object(
            self._relRecord,
            "getPrimsWithFromRelationships",
            return_value=[234, 567, "whatever"],
        ) as mock_getPrimsWithFromRelationships:
            self.assertEqual(self._relRecord.getNumPrimsWithFromRelationships(), 3)
        mock_getPrimsWithFromRelationships.assert_called_once_with(True)

    def test_addRelationshipFrom_alreadyThere(self):
        relName = "someRelationship"
        sourcePath = Sdf.Path("/path/to/prim")
        with mock.patch(
            "relview.data.PrimRelationshipRecord._isRelInList",
            return_value=True,
        ) as mock_isRelInList:
            self._relRecord.addRelationshipFrom(
                relName,
                sourcePath,
            )
        self.assertEqual(self._relRecord._fromRelsByName, {relName: []})
        self.assertEqual(len(mock_isRelInList.call_args_list), 1)
        namedRel = mock_isRelInList.call_args_list[0][0][0]
        self.assertEqual(namedRel.getName(), relName)
        self.assertEqual(namedRel.getPath(), sourcePath)
        self.assertFalse(namedRel.isInvalid())
        self.assertEqual(mock_isRelInList.call_args_list[0][0][1], [])

    def test_addRelationshipFrom_addsNew(self):
        relName = "someRelationship"
        sourcePath = Sdf.Path("/path/to/prim")
        with mock.patch(
            "relview.data.PrimRelationshipRecord._isRelInList",
            return_value=False,
        ) as mock_isRelInList:
            self._relRecord.addRelationshipFrom(
                relName,
                sourcePath,
            )
        self.assertEqual(len(self._relRecord._fromRelsByName[relName]), 1)
        self.assertEqual(len(mock_isRelInList.call_args_list), 1)

        for namedRel in [
            self._relRecord._fromRelsByName[relName][0],
            mock_isRelInList.call_args_list[0][0][0],
        ]:
            self.assertEqual(namedRel.getName(), relName)
            self.assertEqual(namedRel.getPath(), sourcePath)
            self.assertFalse(namedRel.isInvalid())

    def test_hasAnyInvalidFromRelationships(self):
        self._relRecord.addRelationshipFrom("someThing", Sdf.Path("/path/to/thing"))
        self.assertFalse(self._relRecord.hasAnyInvalidFromRelationships())
        self._relRecord.addRelationshipFrom(
            "otherThing", Sdf.Path("/path/to/other/thing"), "Bad!"
        )
        self.assertTrue(self._relRecord.hasAnyInvalidFromRelationships())

    #
    # "additional" relationships stuff
    #
    def test_hasAdditionalToRelationships(self):
        self.assertFalse(self._relRecord.hasAdditionalToRelationships())
        self._relRecord._additionalRelsByName = "asdasda"
        self.assertTrue(self._relRecord.hasAdditionalToRelationships())

    def test_getAdditionalToRelationshipNames(self):
        self.assertEqual(self._relRecord.getAdditionalToRelationshipNames(), [])
        self._relRecord._additionalRelsByName["things"] = [1, 2, 3]
        self.assertEqual(self._relRecord.getAdditionalToRelationshipNames(), ["things"])

    def test_getAdditionalToRelationshipsNamed(self):
        self.assertEqual(
            self._relRecord.getAdditionalToRelationshipsNamed("things"), []
        )
        self._relRecord._additionalRelsByName["things"] = [1, 2, 3]
        self.assertEqual(
            self._relRecord.getAdditionalToRelationshipsNamed("things"), [1, 2, 3]
        )

    def test_getAdditionalToRelationships(self):
        self.assertEqual(self._relRecord.getAdditionalToRelationships(), [])
        self._relRecord._additionalRelsByName["things"] = [1, 2, 3]
        self._relRecord._additionalRelsByName["otherThings"] = [7, 8, 9]
        self.assertEqual(
            set(self._relRecord.getAdditionalToRelationships()), set([1, 2, 3, 7, 8, 9])
        )

    def test_getNumAdditionalToRelationships(self):
        with mock.patch.object(
            self._relRecord,
            "getAdditionalToRelationships",
            return_value=[5, 4, 3, 2, 1],
        ):
            self.assertEqual(self._relRecord.getNumAdditionalToRelationships(), 5)

    def test_addAdditionalToRelationship_alreadyThere(self):
        relName = "someRelationship"
        sourcePath = Sdf.Path("/path/to/prim")
        with mock.patch(
            "relview.data.PrimRelationshipRecord._isRelInList",
            return_value=True,
        ) as mock_isRelInList:
            self._relRecord.addAdditionalToRelationship(
                relName,
                sourcePath,
            )
        self.assertEqual(self._relRecord._additionalRelsByName, {relName: []})
        self.assertEqual(len(mock_isRelInList.call_args_list), 1)
        namedRel = mock_isRelInList.call_args_list[0][0][0]
        self.assertEqual(namedRel.getName(), relName)
        self.assertEqual(namedRel.getPath(), sourcePath)
        self.assertFalse(namedRel.isInvalid())
        self.assertEqual(mock_isRelInList.call_args_list[0][0][1], [])

    def test_addAdditionalToRelationship_addsNew(self):
        relName = "someRelationship"
        sourcePath = Sdf.Path("/path/to/prim")
        with mock.patch(
            "relview.data.PrimRelationshipRecord._isRelInList",
            return_value=False,
        ) as mock_isRelInList:
            self._relRecord.addAdditionalToRelationship(
                relName,
                sourcePath,
            )
        self.assertEqual(len(self._relRecord._additionalRelsByName[relName]), 1)
        self.assertEqual(len(mock_isRelInList.call_args_list), 1)

        for namedRel in [
            self._relRecord._additionalRelsByName[relName][0],
            mock_isRelInList.call_args_list[0][0][0],
        ]:
            self.assertEqual(namedRel.getName(), relName)
            self.assertEqual(namedRel.getPath(), sourcePath)
            self.assertFalse(namedRel.isInvalid())


class PrimRelationshipRecord_privateHelperFunctions_TestCase(TestCase):
    """Tests the private helper functions in PrimRelationshipRecord.py"""

    def test__isRelInList(self):
        self.assertTrue(PrimRelationshipRecord._isRelInList(5, [1, 2, 5, 8]))
        self.assertFalse(PrimRelationshipRecord._isRelInList(3, [1, 2, 5, 8]))

    def test__getUniquePrimPathsFromRelList_omitInvalid(self):
        namedRel1 = NamedRelationship("rel1", Sdf.Path())  # empty
        namedRel2 = NamedRelationship(
            "rel2", Sdf.Path("/path/to/prim"), "BAD!"
        )  # invalid
        namedRel3 = NamedRelationship("rel3", Sdf.Path("/other/path/to/prim"))
        namedRel4 = NamedRelationship("rel3", Sdf.Path("/final/path/to/prim"))
        self.assertEqual(
            PrimRelationshipRecord._getUniquePrimPathsFromRelList(
                [namedRel1, namedRel2, namedRel3, namedRel4]
            ),
            set([Sdf.Path("/other/path/to/prim"), Sdf.Path("/final/path/to/prim")]),
        )

    def test__getUniquePrimPathsFromRelList_doNotOmitInvalid(self):
        namedRel1 = NamedRelationship("rel1", Sdf.Path())  # empty
        namedRel2 = NamedRelationship(
            "rel2", Sdf.Path("/path/to/prim"), "BAD!"
        )  # invalid
        namedRel3 = NamedRelationship("rel3", Sdf.Path("/other/path/to/prim"))
        namedRel4 = NamedRelationship("rel3", Sdf.Path("/final/path/to/prim"))
        self.assertEqual(
            PrimRelationshipRecord._getUniquePrimPathsFromRelList(
                [namedRel1, namedRel2, namedRel3, namedRel4], False
            ),
            set(
                [
                    Sdf.Path("/path/to/prim"),
                    Sdf.Path("/other/path/to/prim"),
                    Sdf.Path("/final/path/to/prim"),
                ]
            ),
        )


#
# some mocks
#
class MockStage(object):
    def GetPrimAtPath(self, primPath):
        return None  # just here for mocking


class MockRelationshipCollection(object):
    pass
