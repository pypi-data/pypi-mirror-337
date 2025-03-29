from Qt import QtCore


#
# first, some mixins that are used by the decorators below
#
class EnsureAttrExistsMixin(object):
    """Several of the decorators meant to be applied to class methods make use
    of an attribute to be set on the object at some point - just putting this
    _ensureAttrExistsOn() method in a mixin so as to be inherited by those that
    need it.
    """

    def _ensureAttrExistsOn(self, objInstance, attrName, defaultVal=None):
        if not hasattr(objInstance, attrName):
            setattr(objInstance, attrName, defaultVal)


#
# and now, the decorators
#
class waitThisLongBeforeRunning(object):
    """Uses Qt's QTimer.singleShot(timeout, slot) to call the wrapped function
    after the specified number of milliseconds. See doWhenReady and doMomentarily,
    below for some examples.
    """

    def __init__(self, numMilliseconds=1):
        self._numMilliseconds = numMilliseconds

    def __call__(self, func):
        def inner(*args, **kwargs):
            def _innerSLOT():
                func(*args, **kwargs)

            QtCore.QTimer.singleShot(self._numMilliseconds, _innerSLOT)

        return inner


class callOnceDeferred(EnsureAttrExistsMixin):
    """Decorator to be used on a class method to call the wrapped function only
    once, after some predefined timeout, such that subsequent calls during the
    wait period will be ignored. Handy for things like coalescing a bunch of
    individual data-has-been-changed calls into one UI update.
    """

    def __init__(self, callsPendingAttrName, waitTimeoutMs=1):
        self._callsPendingAttrName = callsPendingAttrName
        self._waitTimeoutMs = waitTimeoutMs

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            objInstance = args[0]

            @waitThisLongBeforeRunning(self._waitTimeoutMs)
            def worker(*args, **kwargs):
                func(*args, **kwargs)
                setattr(objInstance, self._callsPendingAttrName, False)

            self._ensureAttrExistsOn(objInstance, self._callsPendingAttrName)
            if getattr(objInstance, self._callsPendingAttrName):
                return  # calls are scheduled, so do nothing

            setattr(objInstance, self._callsPendingAttrName, True)
            worker(*args, **kwargs)

        return wrapper
