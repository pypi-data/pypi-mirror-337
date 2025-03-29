class NamedRelationship(object):
    """Encapsulates a relationship name and an Sdf.Path (which could be a prop-
    erty path).
    """

    def __init__(self, relName, sdfPath, messageIfInvalid=None):
        self._relName = relName
        self._sdfPath = sdfPath  # note: could be a property path (see below)
        self._messageIfInvalid = messageIfInvalid

    #
    # public API
    #
    def getName(self):
        return self._relName

    def isPropertyRelationship(self):
        return self._sdfPath.IsPropertyPath()

    def getPropertyName(self):
        return self._sdfPath.name if self.isPropertyRelationship() else None

    def getPath(self):
        return self._sdfPath

    def getPrimPath(self):
        return self.getPath().GetPrimPath()

    def isEmpty(self):
        return not bool(self._sdfPath)

    def isInvalid(self):
        return bool(self._messageIfInvalid)

    def getInvalidMessage(self):
        return self._messageIfInvalid or ""

    def __eq__(self, other):
        return (
            self.getName() == other.getName()
            and self.getPath() == other.getPath()
            and self.getInvalidMessage() == other.getInvalidMessage()
        )
