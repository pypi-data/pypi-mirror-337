from unittest import mock, TestCase

from relview.data.decorators import callOnceDeferred


#
# test cases
#
class callOnceDeferred_TestCase(TestCase):
    """Tests the callOnceDeferred decorator. (other things get exercised in
    the course of this test case, so this is good enough for now)
    """

    def test_callOnceDeferred_new(self):
        with mock.patch(
            "relview.data.decorators.QtCore.QTimer.singleShot",
            new=_mock_singleShot,
        ):
            class MyTestClass(object):
                didAThing = False

                @callOnceDeferred("_willDoAThing", 23)
                def doAThing(self):
                    self.didAThing = True

            testObj = MyTestClass()
            self.assertFalse(testObj.didAThing)
            self.assertFalse(hasattr(testObj, "_willDoAThing"))
            testObj.doAThing()
            self.assertTrue(testObj.didAThing)

        self.assertTrue(hasattr(testObj, "_willDoAThing"))
        self.assertEqual(testObj._willDoAThing, False)

    def test_callOnceDeferred_alreadyScheduled(self):
        with mock.patch(
            "relview.data.decorators.QtCore.QTimer.singleShot",
            new=_mock_singleShot,
        ):

            class MyTestClass(object):
                didAThing = False

                @callOnceDeferred("_willDoAThing", 23)
                def doAThing(self):
                    self.didAThing = True

            testObj = MyTestClass()
            testObj._willDoAThing = True
            testObj.doAThing()
            self.assertFalse(testObj.didAThing)


#
# some mocks
#
def _mock_singleShot(numMilliseconds, func):
    func()
