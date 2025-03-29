from Qt import QtGui


#
# functions
#
def getNodeStylingForPrimsOfType(primTypeStr):
    return NodeStylingRegistry.getInstance().getNodeStylingForPrimsOfType(primTypeStr)


def getIconForPrimsOfType(primTypeStr):
    nodeStyling = getNodeStylingForPrimsOfType(primTypeStr)
    return nodeStyling.getIcon() if nodeStyling and nodeStyling.hasIcon() else None


def getIconPathForPrimsOfType(primTypeStr):
    nodeStyling = getNodeStylingForPrimsOfType(primTypeStr)
    return nodeStyling.getIconPath() if nodeStyling and nodeStyling.hasIcon() else None


#
# classes
#
class NodeStylingRegistry(object):
    """Singleton registry of NodeStyling objects, keyed by prim type name. Used
    for styling PrimNodeItem instances as seen in the relationship view. Typically
    this will be used from relview plugins like:

    nodeStylingReg = NodeStylingRegistry.getInstance()
    nodeStylingReg.setNodeStylingForPrimsOfType(
        "KickassXForm",
        NodeStyling(iconPath="/etc/primIcons/kickassXForm.svg")
    )
    ...
    """

    _INSTANCE = None

    @classmethod
    def getInstance(cls):
        if cls._INSTANCE is None:
            cls._INSTANCE = cls()
        return cls._INSTANCE

    def __init__(self):
        self._defaultNodeStyling = None
        self._nodeStylingObjsByPrimTypeName = {}

    def getDefaultNodeStyling(self):
        return self._defaultNodeStyling

    def setDefaultNodeStyling(self, defaultNodeStyling):
        self._defaultNodeStyling = defaultNodeStyling

    def setNodeStylingForPrimsOfType(self, primTypeName, nodeStylingObj):
        self._nodeStylingObjsByPrimTypeName[primTypeName] = nodeStylingObj

    def getNodeStylingForPrimsOfType(self, primTypeName):
        return self._nodeStylingObjsByPrimTypeName.get(
            primTypeName, self.getDefaultNodeStyling()
        )


class NodeStyling(object):
    """Encapsulates a foreground color (QColor), background color (QColor), and
    icon (QIcon) to use for styling a PrimNodeItem in a relationship view.
    """

    def __init__(self, backgroundColor=None, foregroundColor=None, iconPath=None):
        self._backgroundColor = backgroundColor
        self._foregroundColor = foregroundColor
        self._iconPath = iconPath or None
        self._icon = QtGui.QIcon(self._iconPath) if self._iconPath else None
        self._isSvgIcon = self._iconPath and self._iconPath.endswith(".svg")  # :shrug:

    def hasBackgroundColor(self):
        return self._backgroundColor is not None

    def getBackgroundColor(self):
        return self._backgroundColor

    def hasForegroundColor(self):
        return self._foregroundColor is not None

    def getForegroundColor(self):
        return self._foregroundColor

    def hasIcon(self):
        return self._icon is not None

    def getIcon(self):
        return self._icon

    def getIconPath(self):
        return self._iconPath

    def isSvgIcon(self):
        return self._isSvgIcon
