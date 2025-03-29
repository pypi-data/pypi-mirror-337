class RelationshipInfoCollector(object):
    """Used to collect information about the relationships seen on the USD stage
    in the course of traversal. Gets used to populate things like filters for
    relationship names, prim types, etc.
    """

    def __init__(self):
        self.clear()

    def clear(self):
        self._relationshipNames = set()
        self._primTypeNames = set()
        self._propertyNames = set()

    def addRelationshipName(self, relName):
        self._relationshipNames.add(relName)

    def getRelationshipNames(self):
        return self._relationshipNames

    def addPrimTypeName(self, primTypeName):
        self._primTypeNames.add(primTypeName)

    def getPrimTypeNames(self):
        return self._primTypeNames

    def addPropertyName(self, propName):
        self._propertyNames.add(propName)

    def getPropertyNames(self):
        return self._propertyNames
