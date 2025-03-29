from unittest import mock, TestCase

from relview.data.RelationshipInfoCollector import RelationshipInfoCollector


class RelationshipInfoCollector_TestCase(TestCase):
    """Tests the RelationshipInfoCollector class"""

    def setUp(self):
        self._relInfoColl = RelationshipInfoCollector()

    def test_init(self):
        self.assertEqual(self._relInfoColl._relationshipNames, set())
        self.assertEqual(self._relInfoColl._primTypeNames, set())
        self.assertEqual(self._relInfoColl._propertyNames, set())

    def test_clear(self):
        self._relInfoColl._relationshipNames = "asdasd"
        self._relInfoColl._primTypeNames = [1, 2, 3]
        self._relInfoColl._propertyNames = {"whatevs"}
        self._relInfoColl.clear()
        self.assertEqual(self._relInfoColl._relationshipNames, set())
        self.assertEqual(self._relInfoColl._primTypeNames, set())
        self.assertEqual(self._relInfoColl._propertyNames, set())

    def test_addRelationshipName(self):
        self._relInfoColl.addRelationshipName("relName")
        self.assertEqual(self._relInfoColl._relationshipNames, {"relName"})
        self._relInfoColl.addRelationshipName("nooice")
        self.assertEqual(self._relInfoColl._relationshipNames, {"relName", "nooice"})

    def test_getRelationshipNames(self):
        self.assertEqual(self._relInfoColl.getRelationshipNames(), set())
        self._relInfoColl._relationshipNames = {"relName", "nooice"}
        self.assertEqual(
            self._relInfoColl.getRelationshipNames(), {"relName", "nooice"}
        )

    def test_addPrimTypeName(self):
        self._relInfoColl.addPrimTypeName("kickassType")
        self._relInfoColl.addPrimTypeName("someOtherType")
        self.assertEqual(
            self._relInfoColl._primTypeNames, {"kickassType", "someOtherType"}
        )

    def test_getPrimTypeNames(self):
        self._relInfoColl._primTypeNames = {"kickassType", "someOtherType"}
        self.assertEqual(
            self._relInfoColl.getPrimTypeNames(), {"kickassType", "someOtherType"}
        )

    def test_addPropertyName(self):
        self._relInfoColl.addPropertyName("prop1")
        self._relInfoColl.addPropertyName("someOtherProp")
        self.assertEqual(self._relInfoColl._propertyNames, {"prop1", "someOtherProp"})

    def test_getPropertyNames(self):
        self._relInfoColl._propertyNames = {"prop1", "someOtherProp"}
        self.assertEqual(
            self._relInfoColl.getPropertyNames(), {"prop1", "someOtherProp"}
        )
