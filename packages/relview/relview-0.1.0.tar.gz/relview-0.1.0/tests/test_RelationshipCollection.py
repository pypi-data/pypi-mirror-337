from unittest import mock, TestCase

from pxr import Sdf

from relview.data.RelationshipCollection import RelationshipCollection

from .utilsForTesting import SignalReceiver


class RelationshipCollection_TestCase(TestCase):
    """Tests the RelationshipCollection class."""

    def test_init(self):
        relColl = RelationshipCollection("stage", [])
        self.assertEqual(relColl._stage, "stage")
        self.assertEqual(relColl._primPaths, set())
        self.assertEqual(
            relColl._filteringOptions.__class__.__name__, "RelationshipFilteringOptions"
        )
        self.assertEqual(relColl._relsByPrimPath, {})
        self.assertEqual(
            relColl._relInfoCollector.__class__.__name__, "RelationshipInfoCollector"
        )

    #
    # public API
    #
    def test_update(self):
        relColl = RelationshipCollection("stage", [])
        signalReceiver = SignalReceiver()
        relColl.Updated.connect(signalReceiver.theSlot)

        with mock.patch.object(
            relColl, "_prunePrimsNotFound"
        ) as mock_prunePrimsNotFound:
            with mock.patch.object(
                relColl, "_collectRelationshipsFromStage"
            ) as mock_collectRelationshipsFromStage:
                relColl.update(signal=False)
                self.assertFalse(signalReceiver.hasReceivedAnySignals())
                mock_prunePrimsNotFound.assert_called_once_with()
                mock_collectRelationshipsFromStage.assert_called_once_with()

        with mock.patch.object(
            relColl, "_prunePrimsNotFound"
        ) as mock_prunePrimsNotFound:
            with mock.patch.object(
                relColl, "_collectRelationshipsFromStage"
            ) as mock_collectRelationshipsFromStage:
                relColl.update(signal=True)
                self.assertTrue(signalReceiver.hasReceivedAnySignals())
                self.assertEqual(signalReceiver.getSignalData(), [tuple()])
                mock_prunePrimsNotFound.assert_called_once_with()
                mock_collectRelationshipsFromStage.assert_called_once_with()

    def test_getStage(self):
        relColl = RelationshipCollection("stage", [])
        self.assertEqual(relColl.getStage(), "stage")

    def test_getPrimPaths(self):
        relColl = RelationshipCollection("stage", [])
        self.assertEqual(relColl.getPrimPaths(), set())
        relColl._primPaths = set([1, 3, 5])
        self.assertEqual(relColl.getPrimPaths(), set([1, 3, 5]))

    def test_addPrimPaths_nothingAdded(self):
        with mock.patch(
            "relview.data.RelationshipCollection.RelationshipCollection._prunePrimsNotFound"
        ):
            with mock.patch(
                "relview.data.RelationshipCollection.RelationshipCollection._collectRelationshipsFromStage"
            ):
                relColl = RelationshipCollection("stage", [1, 3, 5])
                with mock.patch.object(relColl, "update") as mock_update:
                    relColl.addPrimPaths([1, 5])
                mock_update.assert_not_called()

    def test_addPrimPaths_added(self):
        with mock.patch(
            "relview.data.RelationshipCollection.RelationshipCollection._prunePrimsNotFound"
        ):
            with mock.patch(
                "relview.data.RelationshipCollection.RelationshipCollection._collectRelationshipsFromStage"
            ):
                relColl = RelationshipCollection("stage", [1, 3, 5])
                with mock.patch.object(relColl, "update") as mock_update:
                    relColl.addPrimPaths([1, 5, 7, 8])
                mock_update.assert_called_once_with()

    def test_getFilteringOptions(self):
        relColl = RelationshipCollection("stage", [])
        self.assertEqual(relColl.getFilteringOptions(), relColl._filteringOptions)

    def test_getRelationshipInfoCollector(self):
        relColl = RelationshipCollection("stage", [])
        self.assertEqual(
            relColl.getRelationshipInfoCollector(), relColl._relInfoCollector
        )

    def test_hasRecordFor(self):
        relColl = RelationshipCollection("stage", [])
        relColl._relsByPrimPath = {"daPath": 5}
        self.assertTrue(relColl.hasRecordFor("daPath"))
        self.assertFalse(relColl.hasRecordFor("otherPath"))

    def test_getRecordFor(self):
        relColl = RelationshipCollection("stage", [])
        relColl._relsByPrimPath = {"daPath": 5}
        self.assertIsNone(relColl.getRecordFor("somePath"))
        self.assertEqual(relColl.getRecordFor("daPath"), 5)

    def test_getAllPrimPaths(self):
        relColl = RelationshipCollection("stage", [])
        relColl._relsByPrimPath = {"daPath": 5, "otherPath": "tom"}
        self.assertEqual(set(relColl.getAllPrimPaths()), set(["daPath", "otherPath"]))

    def test_getAllRecords(self):
        relColl = RelationshipCollection("stage", [])
        relColl._relsByPrimPath = {"daPath": 5, "otherPath": "tom"}
        self.assertEqual(set(relColl.getAllRecords()), set([5, "tom"]))

    #
    # slots
    #
    def test__filteringOptionsChangedSLOT(self):
        relColl = RelationshipCollection("stage", [])
        relColl._filteringOptions = "daFilteringOptions"
        signalReceiver = SignalReceiver()
        relColl.FilteringOptionsChanged.connect(signalReceiver.theSlot)
        with mock.patch.object(relColl, "update") as mock_update:
            relColl._filteringOptionsChangedSLOT()
        mock_update.assert_called_once_with()
        self.assertEqual(signalReceiver.getSignalData(), [("daFilteringOptions",)])

    #
    # private helper methods etc.
    #
    def test__prunePrimsNotFound(self):
        stage = MockStage({"/path/to/prim1": "prim1", "/path/to/prim2": "prim2"})
        relColl = RelationshipCollection(stage, [])
        relColl._primPaths = set(["/path/to/prim1", "/path/to/prim2", "/path/to/prim3"])
        relColl._prunePrimsNotFound()
        self.assertEqual(relColl._primPaths, set(["/path/to/prim1", "/path/to/prim2"]))

    def test__collectRelationshipsFromStage_noIncomings_primNotFound(self):
        stage = MockStage({"/path/to/prim1": "prim1", "/path/to/prim2": "prim2"})
        relColl = RelationshipCollection(stage, [])
        relColl.getFilteringOptions().followIncomingRelationships(False)
        relColl._primPaths = set(["/not/a/valid/path"])

        with mock.patch.object(
            relColl, "_getOrCreateRecordFor"
        ) as mock_getOrCreateRecordFor:
            with mock.patch.object(
                relColl, "_captureAdditionalRelationshipsOf"
            ) as mock_captureAdditionalRelationshipsOf:
                with mock.patch(
                    "relview.data.RelationshipCollection.updateFilteringOptionsFromInfoCollector"
                ) as mock_updateFilteringOptionsFromInfoCollector:
                    relColl._collectRelationshipsFromStage()

        mock_getOrCreateRecordFor.assert_not_called()
        mock_captureAdditionalRelationshipsOf.assert_not_called()
        mock_updateFilteringOptionsFromInfoCollector.assert_called_once_with(
            relColl._filteringOptions, relColl._relInfoCollector
        )

    def test__collectRelationshipsFromStage_noIncomings_noAdditionals(self):
        stage = MockStage({"/path/to/prim1": "prim1", "/path/to/prim2": "prim2"})
        relColl = RelationshipCollection(stage, [])
        relColl.getFilteringOptions().followIncomingRelationships(False)
        relColl._primPaths = set(["/path/to/prim2"])

        with mock.patch.object(
            relColl, "_getOrCreateRecordFor"
        ) as mock_getOrCreateRecordFor:
            with mock.patch.object(
                relColl, "_collectTargetRelationshipsOf"
            ) as mock_collectTargetRelationshipsOf:
                with mock.patch.object(
                    relColl, "_captureAdditionalRelationshipsOf"
                ) as mock_captureAdditionalRelationshipsOf:
                    with mock.patch(
                        "relview.data.RelationshipCollection.updateFilteringOptionsFromInfoCollector"
                    ) as mock_updateFilteringOptionsFromInfoCollector:
                        relColl._collectRelationshipsFromStage()

        mock_getOrCreateRecordFor.assert_called_once_with("/path/to/prim2")
        mock_collectTargetRelationshipsOf.assert_called_once_with(
            "/path/to/prim2", "prim2", set()
        )
        mock_captureAdditionalRelationshipsOf.assert_not_called()
        mock_updateFilteringOptionsFromInfoCollector.assert_called_once_with(
            relColl._filteringOptions, relColl._relInfoCollector
        )

    def test__collectRelationshipsFromStage_noTargets_notCaptured(self):
        path1 = "/path/to/prim1"
        prim1 = MockPrim(path1)
        path2 = "/path/to/prim2"
        prim2 = MockPrim(path2)
        stage = MockStage({path1: prim1, path2: prim2})
        relColl = RelationshipCollection(stage, [])
        relColl.getFilteringOptions().followTargetRelationships(False)
        relColl._primPaths = set([path2])

        with mock.patch.object(
            relColl, "_getOrCreateRecordFor"
        ) as mock_getOrCreateRecordFor:
            with mock.patch.object(
                relColl, "_collectTargetRelationshipsOf"
            ) as mock_collectTargetRelationshipsOf:
                with mock.patch(
                    "relview.data.RelationshipCollection.Usd.PrimRange.AllPrims",
                    return_value=[prim2],
                ) as mock_AllPrims:
                    with mock.patch.object(
                        relColl, "_collectIncomingRelationshipsOf"
                    ) as mock_collectIncomingRelationshipsOf:
                        with mock.patch.object(
                            relColl, "_captureAdditionalRelationshipsOf"
                        ) as mock_captureAdditionalRelationshipsOf:
                            with mock.patch(
                                "relview.data.RelationshipCollection.updateFilteringOptionsFromInfoCollector"
                            ) as mock_updateFilteringOptionsFromInfoCollector:
                                relColl._collectRelationshipsFromStage()

        mock_getOrCreateRecordFor.assert_called_once_with(path2)
        mock_collectTargetRelationshipsOf.assert_not_called()
        mock_AllPrims.assert_called_once_with("daPseudoRoot")
        mock_collectIncomingRelationshipsOf.assert_not_called()
        mock_captureAdditionalRelationshipsOf.assert_not_called()
        mock_updateFilteringOptionsFromInfoCollector.assert_called_once_with(
            relColl._filteringOptions, relColl._relInfoCollector
        )

    def test__collectRelationshipsFromStage_noTargets_captured(self):
        path1 = "/path/to/prim1"
        prim1 = MockPrim(path1)
        path2 = "/path/to/prim2"
        prim2 = MockPrim(path2)
        path3 = "/path/to/prim3"
        prim3 = MockPrim(path3)
        stage = MockStage({path1: prim1, path2: prim2, path3: prim3})
        relColl = RelationshipCollection(stage, [])
        relColl.getFilteringOptions().followTargetRelationships(False)
        relColl._primPaths = set([path2])

        with mock.patch.object(
            relColl, "_getOrCreateRecordFor"
        ) as mock_getOrCreateRecordFor:
            with mock.patch.object(
                relColl, "_collectTargetRelationshipsOf"
            ) as mock_collectTargetRelationshipsOf:
                with mock.patch(
                    "relview.data.RelationshipCollection.Usd.PrimRange.AllPrims",
                    return_value=[prim3],
                ) as mock_AllPrims:
                    with mock.patch.object(
                        relColl, "_collectIncomingRelationshipsOf"
                    ) as mock_collectIncomingRelationshipsOf:
                        with mock.patch.object(
                            relColl, "_captureAdditionalRelationshipsOf"
                        ) as mock_captureAdditionalRelationshipsOf:
                            with mock.patch(
                                "relview.data.RelationshipCollection.updateFilteringOptionsFromInfoCollector"
                            ) as mock_updateFilteringOptionsFromInfoCollector:
                                relColl._collectRelationshipsFromStage()

        mock_getOrCreateRecordFor.assert_called_once_with(path2)
        mock_collectTargetRelationshipsOf.assert_not_called()
        mock_AllPrims.assert_called_once_with("daPseudoRoot")
        mock_collectIncomingRelationshipsOf.assert_called_once_with(path3, prim3, set())
        mock_captureAdditionalRelationshipsOf.assert_not_called()
        mock_updateFilteringOptionsFromInfoCollector.assert_called_once_with(
            relColl._filteringOptions, relColl._relInfoCollector
        )

    def test__collectRelationshipsFromStage_noTargets_captured_additionals(self):
        path1 = "/path/to/prim1"
        prim1 = MockPrim(path1)
        path2 = "/path/to/prim2"
        prim2 = MockPrim(path2)
        path3 = "/path/to/prim3"
        prim3 = MockPrim(path3)
        stage = MockStage({path1: prim1, path2: prim2, path3: prim3})
        relColl = RelationshipCollection(stage, [])
        relColl.getFilteringOptions().followTargetRelationships(False)
        relColl._primPaths = set([path2])

        def _my_collectIncomingRelationshipsOf(
            primPath, prim, returnToPathsForAdditionals
        ):
            returnToPathsForAdditionals.add("/this/one/here")

        with mock.patch.object(
            relColl, "_getOrCreateRecordFor"
        ) as mock_getOrCreateRecordFor:
            with mock.patch.object(
                relColl, "_collectTargetRelationshipsOf"
            ) as mock_collectTargetRelationshipsOf:
                with mock.patch(
                    "relview.data.RelationshipCollection.Usd.PrimRange.AllPrims",
                    return_value=[prim3],
                ) as mock_AllPrims:
                    with mock.patch.object(
                        relColl,
                        "_collectIncomingRelationshipsOf",
                        side_effect=_my_collectIncomingRelationshipsOf,
                    ):
                        with mock.patch.object(
                            relColl, "_captureAdditionalRelationshipsOf"
                        ) as mock_captureAdditionalRelationshipsOf:
                            with mock.patch(
                                "relview.data.RelationshipCollection.updateFilteringOptionsFromInfoCollector"
                            ) as mock_updateFilteringOptionsFromInfoCollector:
                                relColl._collectRelationshipsFromStage()

        mock_getOrCreateRecordFor.assert_called_once_with(path2)
        mock_collectTargetRelationshipsOf.assert_not_called()
        mock_AllPrims.assert_called_once_with("daPseudoRoot")
        mock_captureAdditionalRelationshipsOf.assert_called_once_with(
            set(["/this/one/here"])
        )
        mock_updateFilteringOptionsFromInfoCollector.assert_called_once_with(
            relColl._filteringOptions, relColl._relInfoCollector
        )

    def test__collectTargetRelationshipsOf_hasTargets(self):
        relColl = RelationshipCollection("daStage", [])
        primPath = Sdf.Path("/path/to/prim")
        prim = MockPrim(primPath)
        rel = MockRelationship("someRel")
        primRelationships = [rel]
        returnToPathsForAdditionals = set()
        otherPath = Sdf.Path("/some/other/path")

        with mock.patch.object(prim, "GetTypeName", return_value="KickassPrim"):
            with mock.patch.object(rel, "GetTargets", return_value=[otherPath]):
                with mock.patch.object(
                    prim, "GetRelationships", return_value=primRelationships
                ):
                    with mock.patch.object(
                        relColl, "_validateRelTargetPath", return_value=(True, "")
                    ) as mock_validateRelTargetPath:
                        relColl._collectTargetRelationshipsOf(
                            primPath, prim, returnToPathsForAdditionals
                        )

        mock_validateRelTargetPath.assert_called_once_with(otherPath, otherPath)

        self.assertEqual(len(relColl._relsByPrimPath), 2)
        self.assertEqual(set(relColl._relsByPrimPath.keys()), {primPath, otherPath})
        # primPath should have one target relationship only, to otherPath
        primPathRelRecord = relColl._relsByPrimPath[primPath]
        self.assertTrue(primPathRelRecord.hasToRelationships())
        toRels = primPathRelRecord.getToRelationships()
        self.assertEqual(len(toRels), 1)
        toRel = toRels[0]
        self.assertEqual(toRel.getName(), "someRel")
        self.assertEqual(toRel.getPath(), otherPath)
        self.assertFalse(primPathRelRecord.hasAnyInvalidToRelationships())
        self.assertFalse(primPathRelRecord.hasFromRelationships())
        self.assertFalse(primPathRelRecord.hasAdditionalToRelationships())
        self.assertFalse(primPathRelRecord.hasAnyUntargetedToRelationships())
        # otherPath should have one incoming relationship only, to primPath
        otherPathRelRecord = relColl._relsByPrimPath[otherPath]
        self.assertTrue(otherPathRelRecord.hasFromRelationships())
        fromRels = otherPathRelRecord.getFromRelationships()
        self.assertEqual(len(fromRels), 1)
        fromRel = fromRels[0]
        self.assertEqual(fromRel.getName(), "someRel")
        self.assertEqual(fromRel.getPath(), primPath)
        self.assertFalse(otherPathRelRecord.hasToRelationships())
        self.assertFalse(otherPathRelRecord.hasAnyInvalidToRelationships())
        self.assertFalse(otherPathRelRecord.hasAdditionalToRelationships())
        self.assertFalse(otherPathRelRecord.hasAnyUntargetedToRelationships())

    def test__collectTargetRelationshipsOf_noTargets(self):
        relColl = RelationshipCollection("daStage", [])
        primPath = Sdf.Path("/path/to/prim")
        prim = MockPrim(primPath)
        rel = MockRelationship("someRel")
        primRelationships = [rel]
        returnToPathsForAdditionals = set()

        with mock.patch.object(prim, "GetTypeName", return_value="KickassPrim"):
            with mock.patch.object(rel, "GetTargets", return_value=[]):
                with mock.patch.object(
                    prim, "GetRelationships", return_value=primRelationships
                ):
                    with mock.patch.object(
                        relColl, "_validateRelTargetPath", return_value=(True, "")
                    ) as mock_validateRelTargetPath:
                        relColl._collectTargetRelationshipsOf(
                            primPath, prim, returnToPathsForAdditionals
                        )

        mock_validateRelTargetPath.assert_not_called()
        self.assertEqual(len(relColl._relsByPrimPath), 1)
        self.assertEqual(list(relColl._relsByPrimPath.keys())[0], primPath)
        relRecord = relColl._relsByPrimPath[primPath]
        self.assertTrue(relRecord.hasAnyUntargetedToRelationships())
        toRels = relRecord.getToRelationships()
        self.assertEqual(len(toRels), 1)
        toRel = toRels[0]
        self.assertTrue(toRel.isEmpty())
        self.assertEqual(toRel.getName(), "someRel")
        self.assertFalse(relRecord.hasFromRelationships())
        self.assertFalse(relRecord.hasAdditionalToRelationships())
        self.assertFalse(relRecord.hasAnyInvalidToRelationships())

    def test__collectIncomingRelationshipsOf_target_do_not_care(self):
        relColl = RelationshipCollection("daStage", [])
        primPath = Sdf.Path("/path/to/prim")
        prim = MockPrim(primPath)
        rel = MockRelationship("someRel")
        primRelationships = [rel]
        returnToPathsForAdditionals = set()
        relColl._primPaths = set()
        otherPath = Sdf.Path("/some/other/path")

        with mock.patch.object(prim, "GetTypeName", return_value="KickassPrim"):
            with mock.patch.object(rel, "GetTargets", return_value=[otherPath]):
                with mock.patch.object(
                    prim, "GetRelationships", return_value=primRelationships
                ):
                    with mock.patch.object(
                        relColl, "_validateRelTargetPath", return_value=(True, "")
                    ) as mock_validateRelTargetPath:
                        relColl._collectIncomingRelationshipsOf(
                            primPath, prim, returnToPathsForAdditionals
                        )

        mock_validateRelTargetPath.assert_not_called()
        self.assertEqual(relColl._relsByPrimPath, {})

    def test__collectIncomingRelationshipsOf_targetOkay(self):
        relColl = RelationshipCollection("daStage", [])
        primPath = Sdf.Path("/path/to/prim")
        prim = MockPrim(primPath)
        rel = MockRelationship("kickassRel")
        primRelationships = [rel]
        returnToPathsForAdditionals = set()
        otherPath = Sdf.Path("/some/other/path")
        relColl._primPaths = {otherPath}

        with mock.patch.object(prim, "GetTypeName", return_value="KickassPrim"):
            with mock.patch.object(rel, "GetTargets", return_value=[otherPath]):
                with mock.patch.object(
                    prim, "GetRelationships", return_value=primRelationships
                ):
                    with mock.patch.object(
                        relColl,
                        "_validateRelTargetPath",
                        return_value=(False, "Bad relationship!"),
                    ) as mock_validateRelTargetPath:
                        relColl._collectIncomingRelationshipsOf(
                            primPath, prim, returnToPathsForAdditionals
                        )

        mock_validateRelTargetPath.assert_called_once_with(otherPath, otherPath)
        self.assertEqual(len(relColl._relsByPrimPath), 2)
        self.assertEqual(set(relColl._relsByPrimPath.keys()), {primPath, otherPath})
        # primPath should have a target relationship to otherPath
        primPathRelRecord = relColl._relsByPrimPath[primPath]
        self.assertTrue(primPathRelRecord.hasToRelationships())
        self.assertFalse(primPathRelRecord.hasFromRelationships())
        self.assertFalse(primPathRelRecord.hasAdditionalToRelationships())
        self.assertTrue(primPathRelRecord.hasAnyInvalidToRelationships())
        toRels = primPathRelRecord.getToRelationships()
        self.assertEqual(len(toRels), 1)
        toRel = toRels[0]
        self.assertEqual(toRel.getName(), "kickassRel")
        self.assertEqual(toRel.getPath(), otherPath)
        self.assertTrue(toRel.isInvalid())
        self.assertEqual(toRel.getInvalidMessage(), "Bad relationship!")
        # otherPath should have an incoming relationship from primPath
        otherPathRelRecord = relColl._relsByPrimPath[otherPath]
        self.assertFalse(otherPathRelRecord.hasToRelationships())
        self.assertTrue(otherPathRelRecord.hasFromRelationships())
        self.assertFalse(otherPathRelRecord.hasAdditionalToRelationships())
        self.assertTrue(otherPathRelRecord.hasAnyInvalidFromRelationships())
        fromRels = otherPathRelRecord.getFromRelationships()
        self.assertEqual(len(fromRels), 1)
        fromRel = fromRels[0]
        self.assertEqual(fromRel.getName(), "kickassRel")
        self.assertEqual(fromRel.getPath(), primPath)
        self.assertTrue(fromRel.isInvalid())
        self.assertEqual(fromRel.getInvalidMessage(), "Bad relationship!")

    def test__collectIncomingRelationshipsOf_noTargets(self):
        relColl = RelationshipCollection("daStage", [])
        primPath = Sdf.Path("/path/to/prim")
        prim = MockPrim(primPath)
        rel = MockRelationship("someRel")
        primRelationships = [rel]
        returnToPathsForAdditionals = set()
        relColl._primPaths = set()

        primPathRelRecord = relColl._getOrCreateRecordFor(primPath)

        with mock.patch.object(prim, "GetTypeName", return_value="KickassPrim"):
            with mock.patch.object(rel, "GetTargets", return_value=[]):
                with mock.patch.object(
                    prim, "GetRelationships", return_value=primRelationships
                ):
                    with mock.patch.object(
                        relColl, "_validateRelTargetPath", return_value=(True, "")
                    ) as mock_validateRelTargetPath:
                        relColl._collectIncomingRelationshipsOf(
                            primPath, prim, returnToPathsForAdditionals
                        )

        mock_validateRelTargetPath.assert_not_called()
        self.assertTrue(primPathRelRecord.hasAnyUntargetedToRelationships())
        self.assertFalse(primPathRelRecord.hasFromRelationships())
        self.assertFalse(primPathRelRecord.hasAdditionalToRelationships())
        toRels = primPathRelRecord.getToRelationships()
        self.assertEqual(len(toRels), 1)
        toRel = toRels[0]
        self.assertEqual(toRel.getName(), "someRel")
        self.assertTrue(toRel.isEmpty())
        self.assertFalse(toRel.isInvalid())

    def test__visitRelationshipsOf_doNotFollowRelsOfPrim(self):
        primPath = Sdf.Path("/path/to/prim")
        prim = MockPrim(primPath)
        relColl = RelationshipCollection("daStage", [])
        filterOpts = relColl.getFilteringOptions()

        def _perTargetCallback(*args):
            pass

        def _noTargetsCallback(*args):
            pass

        with mock.patch.object(prim, "GetTypeName", return_vale="KickassPrim"):
            with mock.patch.object(
                filterOpts, "shouldFollowRelationshipsOf", return_value=False
            ) as mock_shouldFollowRelationshipsOf:
                relColl._visitRelationshipsOf(
                    prim, _perTargetCallback, _noTargetsCallback
                )

        mock_shouldFollowRelationshipsOf.assert_called_once_with(prim)

    def test__visitRelationshipsOf_shouldNotFollowRel(self):
        primPath = Sdf.Path("/path/to/prim")
        prim = MockPrim(primPath)
        relationship = MockRelationship("sweetRel")
        relColl = RelationshipCollection("daStage", [])
        filterOpts = relColl.getFilteringOptions()

        def _perTargetCallback(*args):
            pass

        def _noTargetsCallback(*args):
            pass

        with mock.patch.object(prim, "GetTypeName", return_vale="KickassPrim"):
            with mock.patch.object(
                prim, "GetRelationships", return_value=[relationship]
            ):
                with mock.patch.object(
                    filterOpts, "shouldFollowRelationship", return_value=False
                ) as mock_shouldFollowRelationship:
                    relColl._visitRelationshipsOf(
                        prim, _perTargetCallback, _noTargetsCallback
                    )

        mock_shouldFollowRelationship.assert_called_once_with(prim, relationship)

    def test__visitRelationshipsOf_propName_shouldNotFollowPropRels(self):
        primPath = Sdf.Path("/path/to/prim")
        prim = MockPrim(primPath)
        relationship = MockRelationship("sweetRel")
        relColl = RelationshipCollection("daStage", [])
        filterOpts = relColl.getFilteringOptions()
        filterOpts.includePropertyRelationships(False)
        targetPath = Sdf.Path("/path/to/other/prim.propertyName")

        def _perTargetCallback(*args):
            pass

        def _noTargetsCallback(*args):
            pass

        with mock.patch.object(relationship, "GetTargets", return_value=[targetPath]):
            with mock.patch.object(prim, "GetTypeName", return_vale="KickassPrim"):
                with mock.patch.object(
                    prim, "GetRelationships", return_value=[relationship]
                ):
                    with mock.patch.object(
                        filterOpts, "shouldFollowRelationship", return_value=True
                    ) as mock_shouldFollowRelationship:
                        relColl._visitRelationshipsOf(
                            prim, _perTargetCallback, _noTargetsCallback
                        )

        mock_shouldFollowRelationship.assert_called_once_with(prim, relationship)

    def test__visitRelationshipsOf_shouldNotFollowPrimRels(self):
        primPath = Sdf.Path("/path/to/prim")
        prim = MockPrim(primPath)
        relationship = MockRelationship("sweetRel")
        relColl = RelationshipCollection("daStage", [])
        filterOpts = relColl.getFilteringOptions()
        filterOpts.includePrimRelationships(False)
        targetPath = Sdf.Path("/path/to/other/prim")

        def _perTargetCallback(*args):
            pass

        def _noTargetsCallback(*args):
            pass

        with mock.patch.object(relationship, "GetTargets", return_value=[targetPath]):
            with mock.patch.object(prim, "GetTypeName", return_vale="KickassPrim"):
                with mock.patch.object(
                    prim, "GetRelationships", return_value=[relationship]
                ):
                    with mock.patch.object(
                        filterOpts, "shouldFollowRelationship", return_value=True
                    ) as mock_shouldFollowRelationship:
                        relColl._visitRelationshipsOf(
                            prim, _perTargetCallback, _noTargetsCallback
                        )

        mock_shouldFollowRelationship.assert_called_once_with(prim, relationship)

    def test__visitRelationshipsOf_shouldNotFollowRelTarget(self):
        primPath = Sdf.Path("/path/to/prim")
        prim = MockPrim(primPath)
        relationship = MockRelationship("sweetRel")
        relColl = RelationshipCollection("daStage", [])
        filterOpts = relColl.getFilteringOptions()
        targetPath = Sdf.Path("/path/to/other/prim")

        def _perTargetCallback(*args):
            pass

        def _noTargetsCallback(*args):
            pass

        with mock.patch.object(relationship, "GetTargets", return_value=[targetPath]):
            with mock.patch.object(prim, "GetTypeName", return_vale="KickassPrim"):
                with mock.patch.object(
                    prim, "GetRelationships", return_value=[relationship]
                ):
                    with mock.patch.object(
                        filterOpts, "shouldFollowRelationshipTarget", return_value=False
                    ) as mock_shouldFollowRelationshipTarget:
                        relColl._visitRelationshipsOf(
                            prim, _perTargetCallback, _noTargetsCallback
                        )

        mock_shouldFollowRelationshipTarget.assert_called_once_with(
            prim, relationship, targetPath
        )

    def test__captureAdditionalRelationshipsOf_noRecord(self):
        relColl = RelationshipCollection("daStage", [])
        with mock.patch.object(
            relColl, "_visitRelationshipsOf"
        ) as mock_visitRelationshipsOf:
            relColl._captureAdditionalRelationshipsOf(["/path/to/prim"])
        mock_visitRelationshipsOf.assert_not_called()

    def test__captureAdditionalRelationshipsOf_invalidPrim(self):
        path1 = Sdf.Path("/path/to/prim1")
        path2 = Sdf.Path("/path/to/prim2")
        stage = MockStage({path1: "prim1"})
        relColl = RelationshipCollection(stage, [])
        relColl._getOrCreateRecordFor(path2)
        with mock.patch.object(
            relColl, "_visitRelationshipsOf"
        ) as mock_visitRelationshipsOf:
            relColl._captureAdditionalRelationshipsOf([path2])
        mock_visitRelationshipsOf.assert_not_called()

    def test__captureAdditionalRelationshipsOf_primOkay(self):
        path1 = Sdf.Path("/path/to/prim1")
        path2 = Sdf.Path("/path/to/prim2")
        targetPath = Sdf.Path("/path/to/target")
        stage = MockStage({path1: "prim1", path2: "prim2"})
        relColl = RelationshipCollection(stage, [])
        path2RelRecord = relColl._getOrCreateRecordFor(path2)

        def _my_visitRelationshipsOf(self, perTargetCallback):
            perTargetCallback("someRelName", targetPath, targetPath)

        with mock.patch.object(
            relColl, "_visitRelationshipsOf", side_effect=_my_visitRelationshipsOf
        ):
            relColl._captureAdditionalRelationshipsOf([path2])

        self.assertEqual(
            path2RelRecord.getAdditionalToRelationshipNames(), ["someRelName"]
        )

    def test__validateRelTargetPath_noTargetPrim(self):
        path1 = Sdf.Path("/path/to/prim1")
        path2 = Sdf.Path("/path/to/prim2")
        targetPath = Sdf.Path("/path/to/target")
        stage = MockStage({path1: "prim1", path2: "prim2"})
        relColl = RelationshipCollection(stage, [])
        valid, errMsg = relColl._validateRelTargetPath(targetPath, targetPath)
        self.assertFalse(valid)
        self.assertEqual(errMsg, "The specified prim does not exist")

    def test__validateRelTargetPath_badProperty(self):
        path1 = Sdf.Path("/path/to/prim1")
        path2 = Sdf.Path("/path/to/prim2.propertyName")
        prim2 = MockPrim(path2)
        stage = MockStage({path1: "prim1", path2.GetPrimPath(): prim2})
        relColl = RelationshipCollection(stage, [])
        valid, errMsg = relColl._validateRelTargetPath(path2, path2.GetPrimPath())
        self.assertFalse(valid)
        self.assertEqual(errMsg, "The specified property does not exist")

    def test__validateRelTargetPath_ok(self):
        path1 = Sdf.Path("/path/to/prim1")
        path2 = Sdf.Path("/path/to/prim2")
        prim2 = MockPrim(path2)
        stage = MockStage({path1: "prim1", path2: prim2})
        relColl = RelationshipCollection(stage, [])
        valid, errMsg = relColl._validateRelTargetPath(path2, path2)
        self.assertTrue(valid)
        self.assertIsNone(errMsg)


#
# some mocks
#
class MockStage(object):
    def __init__(self, primsByPath):
        self._primsByPath = primsByPath

    def GetPrimAtPath(self, primPath):
        return self._primsByPath.get(primPath)

    def GetPseudoRoot(self):
        return "daPseudoRoot"


class MockPrim(object):
    def __init__(self, primPath):
        self._primPath = primPath

    def GetPath(self):
        return self._primPath

    def GetTypeName(self):
        return None  # here for mocking

    def GetRelationships(self):
        return None  # here for mocking

    def GetProperty(self, propName):
        return None  # here for mocking


class MockRelationship(object):
    def __init__(self, relName):
        self._relName = relName

    def GetName(self):
        return self._relName

    def GetTargets(self):
        return None  # here for mocking
