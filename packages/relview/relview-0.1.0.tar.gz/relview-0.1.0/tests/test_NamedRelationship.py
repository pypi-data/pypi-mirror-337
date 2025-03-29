from unittest import mock, TestCase

from pxr import Sdf

from relview.data import NamedRelationship


#
# test cases
#
class NamedRelationship_TestCase(TestCase):
    """Tests the NamedRelationship class."""

    def setUp(self):
        self._relName = "someRelationship"
        self._sdfPath = Sdf.Path("/path/to/thing")
        self._namedRel = NamedRelationship.NamedRelationship(
            self._relName, self._sdfPath
        )

    def test_init(self):
        self.assertEqual(self._namedRel._relName, self._relName)
        self.assertEqual(self._namedRel._sdfPath, self._sdfPath)
        self.assertIsNone(self._namedRel._messageIfInvalid)

    def test_getName(self):
        self.assertEqual(self._namedRel.getName(), self._relName)

    def test_isPropertyRelationship(self):
        self.assertFalse(self._namedRel.isPropertyRelationship())
        propPath = self._sdfPath.AppendProperty("daProp")
        propNamedRel = NamedRelationship.NamedRelationship(self._relName, propPath)
        self.assertTrue(propNamedRel.isPropertyRelationship())

    def test_getPropertyName(self):
        self.assertIsNone(self._namedRel.getPropertyName())
        propPath = self._sdfPath.AppendProperty("daProp")
        propNamedRel = NamedRelationship.NamedRelationship(self._relName, propPath)
        self.assertEqual(propNamedRel.getPropertyName(), "daProp")

    def test_getPath(self):
        self.assertEqual(self._namedRel.getPath(), self._sdfPath)

    def test_getPrimPath(self):
        self.assertEqual(self._namedRel.getPrimPath(), self._sdfPath)
        propPath = self._sdfPath.AppendProperty("daProp")
        propNamedRel = NamedRelationship.NamedRelationship(self._relName, propPath)
        self.assertEqual(propNamedRel.getPrimPath(), self._sdfPath)

    def test_isEmpty(self):
        self.assertFalse(self._namedRel.isEmpty())
        emptyNamedRel = NamedRelationship.NamedRelationship("proxyPrim", None)
        self.assertTrue(emptyNamedRel.isEmpty())

    def test_isInvalid(self):
        self.assertFalse(self._namedRel.isInvalid())
        invalidNamedRel = NamedRelationship.NamedRelationship(
            self._relName, self._sdfPath, "Nope, no good, bruv"
        )
        self.assertTrue(invalidNamedRel.isInvalid())

    def test_getInvalidMessage(self):
        self.assertEqual(self._namedRel.getInvalidMessage(), "")
        invalidNamedRel = NamedRelationship.NamedRelationship(
            self._relName, self._sdfPath, "Nope, no good, bruv"
        )
        self.assertEqual(invalidNamedRel.getInvalidMessage(), "Nope, no good, bruv")

    def test___eq__(self):
        thisNamedRel = NamedRelationship.NamedRelationship(
            self._relName, self._sdfPath, messageIfInvalid="no good"
        )
        for relName, path, invalidMessage, expectedVal in [
            (self._relName, self._sdfPath, "no good", True),
            ("somethingElse", self._sdfPath, "no good", False),  # different rel name
            (
                self._relName,
                Sdf.Path("/some/thing"),
                "no good",
                False,
            ),  # different path
            (
                self._relName,
                self._sdfPath,
                "ugh bad",
                False,
            ),  # different invalid message
        ]:
            otherNamedRel = NamedRelationship.NamedRelationship(
                relName, path, invalidMessage
            )
            self.assertEqual(otherNamedRel == thisNamedRel, expectedVal)
