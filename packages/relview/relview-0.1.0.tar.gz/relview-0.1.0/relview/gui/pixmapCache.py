from Qt import QtGui


ICONS_BY_PATH = {}
PIXMAPS_BY_PATH_AND_SIZE = {}


#
# main API
#
def getOrCreatePixmapFor(iconFilePath, desiredSize):
    """Little cache for QPixmap instances, to be used for pixmaps that get used
    frequently and/or when there might be many of the same pixmap shown at a time.
    Basically just a wrapper around QPixmapCache. Speeds up creation and reduces
    memory usage a bit. Note that QPixmap is a QPaintDevice, so make sure to not
    call this before the QApplication instance is created!
    """
    keyStr = _getKeyFor(iconFilePath, desiredSize)
    pixmap = QtGui.QPixmapCache.find(keyStr)
    if pixmap is not None:
        return pixmap

    icon = QtGui.QIcon(iconFilePath)
    pixmap = icon.pixmap(desiredSize)
    QtGui.QPixmapCache.insert(keyStr, pixmap)
    return pixmap


#
# private helper methods
#
def _getKeyFor(filePath, qSize):
    return f"{filePath}@@{qSize.width()}x{qSize.height()}"
